# Dhaara — Construction & Demolition Waste Routing, Mysuru

> Dhaara connects citizens with the correct local authority for construction-waste requests. **Team Cryptile · HackMysuru 1.0 – Phase 1**
> **Live app:** https://hackthon-baz7.vercel.app/ · **Repository:** https://github.com/Harsha-HY/hackthon (branch `hack`)

| 🚀 Open app | 👤 Citizen | 🧾 Officer | 🕵️ Inspector | 📊 Dashboard | 🧠 AI docs | ⚠️ Limitations |
|---|---|---|---|---|---|---|
| [index.html](./index.html) | [citizen.html](./citizen.html) | [officer.html](./officer.html) | [inspector.html](./inspector.html) | [dashboard.html](./dashboard.html) | [ai (1).md](./ai%20(1).md) | [limitations (1).md](./limitations%20(1).md) |

---

## Repository note

This repository also contains files from an earlier prototype called "Smart Civic Waste Routing" (a general garbage-reporting page copied from an external site). `build_index.py` and the hero image assets are kept for reference, but the current working app is the Dhaara flow described below.

---

## 1. Problem Understanding

Construction waste is being dumped in places where it should not be. One of the main difficulties is knowing which authority is responsible for a particular location. With the Mysuru City Corporation, Town Panchayat and Gram Panchayat all involved, the system needs a route that sends requests to the correct office and tracks them at each step.

We chose to focus on this gap: the step between submitting a request and getting it to the correct authority for action. We did not try to solve every waste-related problem at once.

## 2. Target Users & Context

| User | What Dhaara gives them | Page |
|---|---|---|
| Citizen | Submit a construction-waste request with location, pincode, property ID and a live geotagged photo; track its status | `citizen.html` |
| Department officer (MCC, Town Panchayat or Gram Panchayat) | A dashboard scoped to their authority, to review and manage requests | `officer.html?auth=<dept>` |
| Field inspector | A queue of requests assigned to their pincode or department, and the on-site inspection workflow | `inspector.html` |
| Admin | City-wide statistics, pincode/ward mapping, departments, inspectors, requests and certificates | `dashboard.html` |

**Local context:** requests are routed by pincode across three kinds of authority: MCC (urban wards), Gram Panchayat (for example Bogadi Rural) and Town Panchayat (for example Hootagalli). The pages were designed to show how a request moves from citizen input to final verification.

## 3. Solution Overview

Dhaara is a web application. The citizen enters a location or pincode, and the system identifies the authority for that pincode and sends the request to the right office. The officer reviews it, and the inspector then verifies the site before the request is approved.

**Request flow:** User → Pincode/Location → Authority → Officer Review → Request Accepted → Inspector Assigned → Site Inspection → Status/Notification

**Why people will use it:** people who use Dhaara receive a certificate valid for 2 years, which gives a 10% discount on their electricity and water bills.

**What the application includes:**
- A request form with GPS autofill, an 8-digit property ID and one live camera photo stamped with coordinates and time.
- Automatic routing by pincode to MCC, Town Panchayat or Gram Panchayat.
- An authority dashboard, an inspector queue and status tracking for the citizen.
- A four-step progress tracker: Submitted, Scheduled, Audited, Approved.

**Screenshots:** not included. Please use the live app.

## 4. Architecture

Static HTML pages (Tailwind from a CDN) call a Vercel serverless function (`api/index.js`) backed by Supabase. The browser also uses `localStorage` and `BroadcastChannel` as a cache and to keep operations synchronized across tabs.

➡️ Diagram, components, data flow and APIs: **[architecture (1).md](./architecture%20(1).md)**

## 5. Tech Stack & AI Usage

**Stack:** HTML, CSS and JavaScript · Tailwind CSS (CDN) · React 18 + Babel Standalone and Chart.js (CDN, `dashboard.html` only) · Node.js (`server.js` locally, `api/index.js` on Vercel) · Supabase for data + auth.

**AI tools used in development:** a Gemini-based local workspace for the early prototype, and Claude for the submission documents. See [ai (1).md](./ai%20(1).md).
**AI inside the product:** none. Routing is a fixed pincode lookup, and site verification is done by a human inspector.

➡️ Full disclosure: **[ai (1).md](./ai%20(1).md)**

## 6. Decision Log (Summary)

- **Problem:** focus on routing requests to the correct authority, not every waste problem.
- **Build:** a web application that routes by pincode or location to MCC, Town Panchayat or Gram Panchayat.
- **Officer and inspector:** the officer reviews and accepts the request and an inspector verifies the site before further action.
- **Focus for 72 hours:** one complete, demonstrable request flow instead of many half-finished features.
- **Incentive:** a 2-year certificate with a 10% discount on electricity and water bills gives people a reason to use the site.
- **Later:** official boundary data, photo-based waste detection, automated inspection reports, escalation for delayed requests, better analytics and civic-system integration.

➡️ Decisions with reasoning: **[resource (1).md](./resource%20(1).md)**

## 7. Setup & Run

```bash
git clone https://github.com/Harsha-HY/hackthon.git
cd hackthon
git checkout hack
npm install
# create a .env file based on .env.example (see setup (1).md)
npm start
```

Or try the deployed app at https://hackthon-baz7.vercel.app/.

➡️ Prerequisites, environment variables and demo accounts: **[setup (1).md](./setup%20(1).md)**

## 8. Known Limitations

- **Sign-in is not secure yet.** Demo accounts are hardcoded in `auth.html`, and a short list of common passwords is accepted for any account.
- **Routing uses fixed pincode lists,** not official authority boundaries, so a pincode that covers more than one authority can be routed to the wrong office.
- **Some data is browser-side.** Demo and seed data ship inside the HTML files, and `localStorage` is used alongside the database.
- **The 10% discount needs utility providers.** No integration with electricity or water providers exists in the repository.

➡️ Full list with suggested fixes: **[limitations (1).md](./limitations%20(1).md)**

## 9. Team

**Team Cryptile** — [add member names and roles here].
GitHub: repository owner `Harsha-HY`; contributor through merged pull requests: `DimplekumarAJ`.

## 10. License

MIT, as declared in `package.json`. A separate `LICENSE` file has not been added yet.

## Quick file links

- [README.md](./README.md)
- [index.html](./index.html)
- [auth.html](./auth.html)
- [citizen.html](./citizen.html)
- [officer.html](./officer.html)
- [inspector.html](./inspector.html)
- [dashboard.html](./dashboard.html)
- [main_content.html](./main_content.html)
- [assets/](./assets)
- [src/](./src)
- [package.json](./package.json)
- [server.js](./server.js)
- [build_index.py](./build_index.py)
- [supabase-client.js](./supabase-client.js)
- [vercel.json](./vercel.json)
- [architecture (1).md](./architecture%20(1).md)
- [constraints (1).md](./constraints%20(1).md)
- [setup (1).md](./setup%20(1).md)
- [ai (1).md](./ai%20(1).md)
- [limitations (1).md](./limitations%20(1).md)
- [resource (1).md](./resource%20(1).md)
