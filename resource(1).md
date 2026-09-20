# Repository Documentation Index & Design Decisions

[← Back to README](./README.md)

**Project:** Dhaara · **Team:** Cryptile · **Live app:** https://hackthon-baz7.vercel.app/

This file lists the documents in this repository and records the important implementation and design decisions. Section 2 comes from the team's Decision Log and includes the reasoning. Section 3 lists decisions that can be seen in the code, with the file where each one is visible. Where the reasoning was not written down anywhere, that is stated.

## 1. Repository Documents

| Document | What it covers |
|---|---|
| [README.md](./README.md) | Problem, users, solution overview, links to everything below |
| Decision Log (`decisionlog.pdf`) | The team's Q1–Q3 decision log: approach, alternatives, trade-offs and what breaks first at scale |
| [ai.md](./ai.md) | AI tools used in development and AI inside the product |
| [docs/architecture.md](./docs/architecture.md) | Diagram, components, data model, APIs, tech stack |
| [docs/constraints.md](./docs/constraints.md) | Technical and project constraints |
| [docs/setup.md](./docs/setup.md) | Local setup, environment variables, run instructions, demo accounts |
| [docs/limitations.md](./docs/limitations.md) | Known gaps and suggested fixes |
| [resource-templates/decision-log-template.md](./resource-templates/decision-log-template.md) | Reusable template for recording a decision in the Q1–Q3 format |

## 2. Decisions From the Team's Decision Log

### 2.1 Solve one gap: routing a request to the correct authority

**What was decided:** build Dhaara around the gap between submitting a request and getting it to the right authority, instead of every waste-related problem.
**Why:** the main difficulty is knowing which of MCC, Town Panchayat or Gram Panchayat is responsible for a location. A narrow, practical process could be finished and demonstrated in 72 hours.

### 2.2 Use pincode or location as the main input

**What was decided:** the pincode or location identifies the responsible authority, and the request is sent to the associated MCC, Town Panchayat or Gram Panchayat office.
**Why:** it routes the request to the appropriate office without asking the citizen to know the administrative boundaries.
**What was given up:** pincode areas do not always match authority boundaries exactly. Official boundary data is the planned fix.

### 2.3 Officer review and a site inspection before action

**What was decided:** the concerned officer reviews and accepts the request, then an inspector is assigned to visit and inspect the site.
**Why:** the inspection step lets the authority verify the site before taking further action.

### 2.4 Status tracking and notifications

**What was decided:** the citizen can follow a request through status tracking and is informed of changes through notifications.
**Why:** it gives the citizen and the authority a clear flow from submission to inspection.

### 2.5 Certificate incentive for citizens

**What was decided:** people who use Dhaara receive a certificate valid for 2 years, which gives a 10% discount on their electricity and water bills.
**Why:** it gives people a clear reason to use the website instead of dumping waste.
**Dependency:** the discount relies on utility providers accepting the certificate. No integration with them exists in the repository yet.

### 2.6 Known tools and one complete flow within 72 hours

**What was decided:** use HTML, CSS and JavaScript for the frontend, Supabase for the database and Vercel for deployment, and prioritize the complete request flow over extra features.
**Why:** the team already knew these tools, which left more time for building and testing, and a flow that works end to end could be demonstrated within the hackathon time.

## 3. Design Decisions Observed in the Code

### 3.1 Two parallel data layers: API and `localStorage`

**What was built:** every role page fetches from the `/api/...` endpoints and also reads and writes `localStorage` keys (`current_user`, `civic_registered_users`, `civic_inspectors`, `civic_additional_officers`, `civic_departments_config`, `civic_applications`, `civic_deleted_users`, `cust_my_requests`), then merges and removes duplicates by record `id`.
**Where:** `loadData()` in `dashboard.html`, `loadInspectorData()` and `getMyAssignedApplications()` in `inspector.html`, `getAllUsers()` in `auth.html`.
**Reasoning:** not recorded in the repository.

### 3.2 Sign-in with a hardcoded account list instead of Supabase Auth

**What was built:** `auth.html` checks a hardcoded `SYSTEM_ACCOUNTS` array and `checkUserCredentials()`, and also tries `POST /api/auth/login`.
**Where:** `auth.html`.
**Reasoning:** not recorded in the repository. This is listed as a limitation in [docs/limitations.md](./docs/limitations.md).

### 3.3 No build step; React only where needed

**What was built:** every page is static HTML with Tailwind from a CDN. Only `dashboard.html` loads React 18 and Babel Standalone from CDNs for one analytics panel (`#react-panchayat-analytics-root`).
**Where:** the `<script>` tags at the top of `dashboard.html`.
**Reasoning:** not recorded in the repository.

### 3.4 Photo evidence: live camera only, no file upload

**What was built:** the site photo is captured with `getUserMedia` and a canvas (`triggerCameraCapture()`, `snapPhoto()`). There is no file picker.
**Where:** `citizen.html`, the "Real Location Live Photo Evidence" section.
**Reasoning:** the page text says the photo is stamped with real GPS coordinates, the site address and a timestamp. The aim appears to be that the photo is taken live at the location.

### 3.5 Routing through hardcoded pincode tables

**What was built:** the pincode is matched against fixed arrays (`GP_PINS`, `TP_PINS`, `MCC_PINS`) to pick the authority and inspector, instead of a shared boundary dataset or a server-side lookup.
**Where:** `resolveAuthorityAndInspector()` in `citizen.html`, with equivalent arrays in `dashboard.html` and `inspector.html`.
**Reasoning:** not recorded in the repository. The same lists are repeated in three files, which makes them harder to maintain.

### 3.6 Cross-tab sync with `BroadcastChannel`

**What was built:** pages that change shared state post a message on `BroadcastChannel('civic_sync_channel')`. Other open tabs re-fetch and re-render, and a `storage` event listener acts as a second trigger.
**Where:** `citizen.html`, `dashboard.html`, `inspector.html`.
**Reasoning:** not recorded in the repository.
