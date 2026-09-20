# Architecture

[← Back to README](../README.md)

**Project:** Dhaara — Construction & Demolition Waste Routing, Mysuru
**Team:** Cryptile
**Live app:** https://hackthon-baz7.vercel.app/
**Repository:** https://github.com/Harsha-HY/hackthon (branch `hack`)

Dhaara is a web application that routes a construction-waste request to the correct local authority (MCC, Town Panchayat or Gram Panchayat) based on the pincode or location, lets the officer accept it and assign an inspector, and lets the citizen track the status. This document describes what is in the repository.

## System Diagram

```mermaid
flowchart LR
    subgraph Client["Browser: static pages, no build step"]
        IDX[index.html<br/>public landing page]
        AUTH[auth.html<br/>sign in / register]
        CIT[citizen.html<br/>application + tracking]
        OFF[officer.html<br/>department officer console]
        INS[inspector.html<br/>field inspector queue]
        DASH[dashboard.html<br/>admin console + analytics]
    end

    AUTH -->|POST /api/auth/login, /api/auth/register| API
    CIT -->|fetch /api/applications| API
    INS -->|fetch /api/auth/users, /api/applications| API
    DASH -->|fetch /api/dashboard/stats, /api/applications,<br/>/api/pin-mappings, /api/auth/users, /api/inspections| API

    API["api/index.js<br/>Vercel serverless function<br/>(vercel.json rewrite)"] --> SB[(Supabase<br/>@supabase/supabase-js)]

    Client -. localStorage + BroadcastChannel<br/>civic_sync_channel .- Client
    CIT -->|reverse geocode| OSM[OpenStreetMap Nominatim]
```

## Request Flow

This is the flow from the Decision Log, mapped to the pages that implement it:

**User → Pincode/Location → Authority → Officer Review → Request Accepted → Inspector Assigned → Site Inspection → Status/Notification**

1. **Sign in** (`auth.html`): the page calls `POST /api/auth/login`. If the API is unavailable, it falls back to demo accounts defined in the page. The user is stored in `localStorage` and `sessionStorage` and redirected by role (`citizen.html`, `officer.html?auth=<dept>`, `inspector.html` or `dashboard.html`).
2. **Location and pincode** (`citizen.html`): the citizen enters a pincode, or uses the browser Geolocation API. `autoDetectCustomerGPS()` calls OpenStreetMap Nominatim to fill the address and pincode, with a fixed Mysuru-zone fallback if geolocation or the network call fails.
3. **Authority routing** (`citizen.html`): `resolveAuthorityAndInspector(pin)` matches the pincode against the `GP_PINS`, `TP_PINS` and `MCC_PINS` lists (plus any inspector pincodes saved in `localStorage['civic_inspectors']`) to pick the authority and a named inspector.
4. **Site photo** (`citizen.html`): one live camera photo is captured with `getUserMedia` and a canvas, stamped with GPS coordinates and a timestamp. There is no file-upload option.
5. **Submit and sync:** the application is saved to `localStorage['civic_applications']` and announced on `BroadcastChannel('civic_sync_channel')`, so other open pages re-render. The application is also expected to be saved through the API; the exact create endpoint is not confirmed (see Not Covered).
6. **Review and inspection** (`officer.html`, `inspector.html`, `dashboard.html`): these pages load `GET /api/applications`, merge it with `localStorage` and seed data, remove duplicates by `id`, and render. The status steps shown to the citizen are Submitted, Scheduled, Audited and Approved.

## Components

| Component | Responsibility | Tech | Code location |
|---|---|---|---|
| Landing page | Public information page, no login, no API calls | Static HTML, `assets/styles.css`, Google Fonts | `index.html` |
| Auth page | Sign in and registration, role-based redirect | Static HTML, Tailwind CDN, inline JS | `auth.html` |
| Citizen portal | Application form, pincode routing, GPS, camera photo, status tracking, history | Static HTML, Tailwind CDN, inline JS, Nominatim | `citizen.html` |
| Officer console | Department view (MCC / Gram Panchayat / Town Panchayat); reviews requests, accepts them and assigns an inspector | Static HTML | `officer.html` |
| Inspector console | Assigned-request queue and on-site inspection workflow | Static HTML, Tailwind CDN, inline JS | `inspector.html` |
| Admin console | City-wide stats, pincode/ward mapping, departments, inspectors, requests | Static HTML, Tailwind CDN, React 18 + Babel (CDN, analytics panel only), Chart.js | `dashboard.html` |
| API layer | Auth, applications, dashboard stats, pincode mappings, inspections | Vercel serverless function, routed by `vercel.json` | `api/index.js` |
| Local server | `npm start` entry point | Node.js | `server.js` |
| Database | Stores users, applications and inspections | Supabase via `@supabase/supabase-js` | configured with `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` (`.env.example`) |
| Static assets | Hero images and landing-page stylesheet | — | `assets/` |

## Data Model

There is no schema file or migration in the repository. The fields below are taken from the objects used in the client code, so treat them as the working shape, not a confirmed database schema.

| Entity | Fields seen in client code |
|---|---|
| Application | `id`, `applicantName`, `phone`, `propertyId` (8 digits), `address`, `pincode`, `ward`, `status`, `authority`, `authorityKey`, `assignedInspectorName`, `assignedInspectorEmail`, `scheduledDate`, `completionDate`, `verifiedMaterial`, `verifiedTonnage`, `certificateStatus`, `certificateNo`, `gpsLocation`, `photos`, `inspectorNotes` |
| User | `id`, `name`, `email`, `role` (`citizen` / `inspector` / `officer` / `admin`), `department` (`mcc` / `gp` / `tp`), `assignedPin`, `assignedArea`, `designation`, `phone` |
| Pincode mapping | Pincode, ward/area, responsible authority, assigned officer and inspector |

## Key APIs

These routes are called from the browser pages. All `/api/*` traffic is rewritten by `vercel.json` to the single entry point `api/index.js`, which dispatches internally.

| Method | Endpoint | Called from | Purpose |
|---|---|---|---|
| `POST` | `/api/auth/register` | `auth.html` | Create a citizen account |
| `POST` | `/api/auth/login` | `auth.html` | Authenticate a user |
| `GET` | `/api/auth/users` | `auth.html`, `dashboard.html`, `inspector.html` | List users for officer and inspector rosters |
| `GET` | `/api/applications` | `dashboard.html`, `inspector.html` | List all requests |
| `GET` | `/api/dashboard/stats` | `dashboard.html` | Totals, pending inspections and hotspots |
| `GET` | `/api/pin-mappings` | `dashboard.html` | Pincode → ward/authority table |
| `GET` | `/api/inspections` | `dashboard.html` | Scheduled and completed inspections |

## Tech Stack

| Layer | Choice | Why |
|---|---|---|
| Frontend | HTML, CSS, JavaScript; Tailwind via CDN; Google Fonts | Technologies the team was already comfortable with (Decision Log) |
| Analytics panel | React 18 + Babel Standalone and Chart.js, loaded from CDNs, in `dashboard.html` only | No build step needed |
| Backend | Node.js: `server.js` locally, `api/index.js` as the Vercel function | Same language as the Supabase client; runs on Vercel without a separate server |
| Database | Supabase (`@supabase/supabase-js` ^2.116.0) | Hosted database with no server to manage during a 72-hour build |
| Config | `dotenv` ^18.0.1 | Keeps Supabase keys out of the code |
| Deployment | Vercel | Web deployment for the live MVP |
| Geocoding | OpenStreetMap Nominatim (public reverse-geocode endpoint) | Free, no API key |

## Data Sources

| Dataset | Source | Real or synthetic | Used for |
|---|---|---|---|
| Pincode → authority lists | Arrays in `citizen.html`, `dashboard.html`, `inspector.html` (`GP_PINS`, `TP_PINS`, `MCC_PINS`, `AUTHORITY_CONFIGS`) | Team-authored demo data, not an official dataset | Routing a request to the authority |
| Demo accounts | `SYSTEM_ACCOUNTS` in `auth.html` | Synthetic | Fallback sign-in when the API is unavailable |
| Demo applications | `BASELINE_SUBMITTED_APPLICATIONS` in `inspector.html` | Synthetic | Seed data in the inspector queue |
| Seed-record photos | `images.unsplash.com` URLs | Stock photos | Placeholder images |
| Reverse geocoding | OpenStreetMap Nominatim | Real, external | Address and pincode from GPS |

## Known Limitations

- **Pincode routing is a fixed list, not official boundary data.** A pincode can cover areas that belong to different authorities. Connecting official MCC, Town Panchayat and Gram Panchayat boundaries is the first planned improvement.
- **Routing and demo data live in the browser code**, so the routing tables are duplicated across pages and would need one shared source in production.
- **Demo sign-in accounts are hardcoded in `auth.html`** and used when the API cannot be reached. They should be removed before real use.
- **`localStorage` is used alongside the API** to keep open tabs in sync, so a page can show data that is not yet saved in the database.

## Not Covered

The contents of `api/`, `lib/`, `src/` and `server.js` were not read when writing this document. The API table above comes from the `fetch()` calls in the pages, not from the handler code, and the endpoint that saves a new application is not confirmed. Before submitting, open those files and confirm the routes and the Supabase table names.
