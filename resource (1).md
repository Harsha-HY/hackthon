# HackMysuru 1.0 — Phase 1 Submission Index

> This is the landing file for your submission. Reviewers open this file first. Every evaluation artifact is uploaded to **Google Drive** and linked below. No files in the repo, no other platforms. Freeze: **20 September 2026, 23:59 IST**. Anything not linked here before the freeze does not exist for judging.

---

## 1. Team Details

| Field | Value |
|---|---|
| Team ID (from dashboard) | `HM26-337B` |
| Team Name | `Cryptile` |
| College(s) | `GSSS SSFGC` |
| Team Leader | `Harsha HY` · `harshayogesh12@gmail.com` · `8951525788` |
| Repository | `https://github.com/Harsha-HY/hackthon` (branch `hack`) |

| # | Member | Program & Year | GitHub Handle | Primary Role |
|---|---|---|---|---|
| 1 | `Harsha HY` (Lead) | `BCA,2028` | `` | `<role>` |
| 2 | `Dimple Kumar` | `BCA,2028` | `@<handle>` | `<...>` |
| 3 | `Gargie yogish` | `BCA,2027` | `@<handle>` | `<...>` |
| 4 | `Suman Seervi` | `BCA,2027` | `@<handle>` | `<...>` |

---

## 2. What We Built (one-liner)

**Sub-problem:** Routing

**In one sentence:** Dhaara is a web app that routes construction-and-demolition waste requests in Mysuru to the correct authority (MCC, Town Panchayat or Gram Panchayat) using the pincode or location, so an officer can review the request and an inspector can verify the site.

---

## 3. Repository Documents

| Document | What it covers |
|---|---|
| [README.md](./README.md) | Problem, users, solution overview, links to everything below |
| [ai.md](./ai.md) | AI tools used in development and AI/ML inside the product |
| [docs/architecture.md](./docs/architecture.md) | Diagram, components, data model, APIs, tech stack |
| [docs/constraints.md](./docs/constraints.md) | Technical and project constraints of Dhaara |
| [docs/setup.md](./docs/setup.md) | Local setup, environment variables, demo accounts |
| [docs/limitations.md](./docs/limitations.md) | Known gaps, security issues and suggested fixes |
| [resource-templates/](./resource-templates) | Decision log, presentation outline and demo video script |

---

## 4. Submission Artifacts (Google Drive)

| # | Artifact | Google Drive Link | File Name | SHA-256 |
|---|---|---|---|---|
| 1 | Pitch + Code Walkthrough Video (≤ 10 min, MP4) |[open Video](https://drive.google.com/file/d/192uzlkESFvdssvq-ZPC_QtslmV2pCRxh/view?usp=drivesdk) | `<HM26-337B>_video.mp4` | `<...>` |
| 2 | Decision Log (1 page, PDF) | [open Decision Log](https://drive.google.com/file/d/1-6gfQ-0lTgQVWcpcar2sJv7yIo_nUalI/view?usp=drivesdk)| `<HM26-337D>_decision-log.pdf` | `<...>` |
| 3 | Presentation (≤ 10 slides, PDF) | [open Presentation](https://docs.google.com/presentation/d/1LeDL_zenFMHtF2BpFimdZOoHGYegKOYZ/edit?usp=drivesdk&ouid=116819381280222425259&rtpof=true&sd=true) | `<HM26-337B>_presentation.pdf` | `<...>` |

### Video Chapters

| Timestamp | Section |
|---|---|
| `00:00` | Part 1: Problem & target users |
| `00:40` | Part 1: Live demo, core flow |
| `01:50` | Part 1: Bad-input handling |
| `02:30` | Part 1: Offline / airplane mode |
| `03:00` | Part 2: Architecture overview |
| `04:30` | Part 2: Data model & APIs |
| `05:30` | Part 2: Key code walkthrough |
| `07:30` | Part 2: Decisions & trade-offs |
| `08:30` | Part 2: Scaling & limitations |
| `09:15` | Part 2: AI usage (see [ai.md](./ai.md)) |

---

## 5. Live MVP

| Field | Value |
|---|---|
| Live URL | https://hackthon-baz7.vercel.app/ |
| Platform | Web (deployed on Vercel); open in a desktop or mobile browser and allow camera and location |
| Test login (if any) | Citizen: `citizen@gmail.com / 123` · Staff: `inspector.mcc@gmail.com / 123` (MCC officer: `mcc@gmail.com / 123`) · Admin: `admin@gmail.com / 123` |
| Sample data loaded? | Yes. Demo applications, demo accounts and pincode lists are built into the pages. |
| How to test offline mode | Not supported. The app needs a network connection. See [docs/limitations.md](./docs/limitations.md). |
| If the live link is down | Follow [docs/setup.md](./docs/setup.md) |

---

## 6. Quick Reviewer Path (≤ 3 minutes)

1. Open the live URL and sign in as the citizen (`citizen@gmail.com / 123`).
2. Enter pincode `570001`, fill the details, capture the live photo and submit the request.
3. Observe the routing: the status card shows the authority (MCC) and the assigned inspector.
4. Sign in as the MCC inspector (`inspector.mcc@gmail.com / 123`) and find the request in the queue.
5. Sign in as the admin (`admin@gmail.com / 123`) and see the request and the pincode mapping in the dashboard.

---

## 7. Declaration

- [ ] All Drive links open in an incognito window with **Viewer** access (no "Request access").
- [ ] The video is one continuous recording, ≤ 10 minutes, Part 1 then Part 2.
- [ ] The decision log is one page and written by us in our own words.
- [ ] All AI tools used (development and in-product) are disclosed in [ai.md](./ai.md).
- [ ] No code specific to this challenge was written before 18 Sept 2026, 00:00 IST.
- [ ] We will not modify or replace any linked file after 20 Sept 2026, 23:59 IST.

**Submitted by:** `Harsha HY` · **Date/Time (IST):** `<20-09-2026>`
