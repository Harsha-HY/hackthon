# Constraints

[← Back to README](../README.md)

**Project:** Dhaara — Construction & Demolition Waste Routing, Mysuru
**Team:** Cryptile
**Live app:** https://hackthon-baz7.vercel.app/

These are the technical and project constraints that can be seen in the repository's code and configuration, plus the time and scope limits recorded in the Decision Log. Where a rule is enforced only in the browser, that is stated, because it is not a real security or data-integrity boundary. For the full structure, see [architecture.md](./architecture.md).

## Time and scope constraints

- **72-hour build.** Dhaara was built and demonstrated within the hackathon's 72 hours, so the team prioritized one complete working flow over many features: User → Pincode/Location → Authority → Officer Review → Request Accepted → Inspector Assigned → Site Inspection → Status/Notification.
- **Known tools only.** The team chose technologies it already knew so that time went into building and testing the solution.
- **Deferred features.** Official authority boundary data, photo-based waste detection, automated inspection reports, escalation for delayed requests, better analytics and integration with existing civic systems were left for later.

## Deployment / hosting constraints

- **One serverless function for all API traffic.** `vercel.json` rewrites every request under `/api/:match*` to `/api/index.js`. Auth, applications, dashboard stats, pincode mappings and inspections are all served from that one function, so splitting or scaling the backend means changing `vercel.json` first.
- **Vercel is the only deployment target.** The live app runs at `https://hackthon-baz7.vercel.app/`. No Docker, VM or other hosting is configured.
- **Local run:** `npm start` runs `node server.js`.

## Backend / data constraints

- **Supabase is the only database.** `package.json` has two dependencies, `@supabase/supabase-js` and `dotenv`. No other database driver is listed.
- **Environment variables** required by `.env.example`: `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY` and `PORT`. The service-role key is a privileged server-side credential, so it must stay in the server's environment settings (for example Vercel project settings) and never appear in any HTML page.
- **No schema files.** No ORM or migration files were found, so the database schema is not version-controlled in this repository.

## Frontend constraints

- **No build step.** Every page (`index.html`, `auth.html`, `citizen.html`, `officer.html`, `inspector.html`, `dashboard.html`) is a static HTML file with inline scripts and styles. Tailwind is loaded from a CDN (`cdn.tailwindcss.com`), not compiled. `dashboard.html` loads React 18 and Babel Standalone from a CDN for one analytics panel, and there is still no bundling.
- **Camera-only photo.** In `citizen.html` the site photo is captured with `getUserMedia`, a video element and a canvas. There is no `<input type="file">`, so a citizen cannot upload an existing photo, and only one photo is allowed per order.
- **Property ID is exactly 8 digits.** This is enforced in the browser with `maxlength="8" pattern="[0-9]{8}"`. It is a form rule only and is not confirmed to be checked again on the server.
- **Pincode routing uses fixed lists.** `citizen.html` matches the pincode against hardcoded `GP_PINS`, `TP_PINS` and `MCC_PINS` arrays. A pincode outside those lists defaults to the MCC authority.

## Third-party service constraints

- **Reverse geocoding uses the public OpenStreetMap Nominatim API**, called from the browser with a 2.6-second timeout. If it fails or times out, a fixed table of Mysuru zones supplies the address and pincode. It is a free, rate-limited public service, and there is no second geocoding provider.
- **Fonts and styling need internet access.** Google Fonts (`fonts.googleapis.com`, `fonts.gstatic.com`) and the Tailwind CDN are loaded at run time. There are no local copies, so the pages will not look as intended offline.
- **Camera and location need browser permission.** The photo and GPS features use the browser camera and Geolocation APIs, which need the user's permission and a secure (HTTPS) page.

## Authentication constraint

- **Authentication is not handled by Supabase Auth.** Sign-in in `auth.html` first calls `POST /api/auth/login`. If that fails, it falls back to demo accounts defined in the page. The login validation inside the API was not reviewed for this document.

## Not found in the repository

- No CI/CD configuration (for example GitHub Actions) in the root files.
- No tests. `package.json` has only a `start` script and no `test` script.
- No `LICENSE` file, although `package.json` declares the MIT license.
- No `CONTRIBUTING.md` or issue and pull-request templates.
