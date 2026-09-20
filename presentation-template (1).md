# Presentation Outline — Dhaara

[← Back to resource.md](../resource.md)

**Project:** Dhaara **Team:** Cryptile **Event:** HackMysuru 1.0 – Phase 1 **Length:** 5–7 minutes, 10 slides (about 35 seconds each)
**Live app:** https://hackthon-baz7.vercel.app/ **Repository:** https://github.com/Harsha-HY/hackthon

---

## Slide 1. Title

- **Dhaara:** routes construction-waste requests in Mysuru to the correct local authority.
- Team Cryptile · HackMysuru 1.0 – Phase 1.
- Live app link. *Say once that the app's pages are titled "Smart Civic C&D Mysuru"; it is the same project.*

## Slide 2. The problem

- Construction waste is being dumped in places where it should not be.
- It is hard to know which authority is responsible for a location. Mysuru City Corporation (MCC), Town Panchayats and Gram Panchayats are all involved, so people do not know where to submit a request.
- **Example:** pincode 570026 (Bogadi) belongs to a Gram Panchayat, 570018 (Hootagalli) to a Town Panchayat and 570001 (central Mysuru) to the MCC. Three nearby areas, three different offices.
- **Our focus:** the gap between submitting a request and getting it to the correct authority for action.

## Slide 3. Users

| User | What Dhaara gives them |
|---|---|
| Citizen | Submit a request with location, pincode, property ID and a live geotagged photo; track its status |
| Department officer (MCC, Town Panchayat, Gram Panchayat) | A dashboard scoped to their authority |
| Field inspector | A queue of requests for their pincode or department, and the on-site inspection workflow |
| Admin | City-wide statistics, pincode/ward mapping, inspectors, requests and certificates |

## Slide 4. The solution

- **One line:** enter a location or pincode, and Dhaara sends the request to the right office.
- **Flow:** User → Pincode/Location → Authority → Officer Review → Request Accepted → Inspector Assigned → Site Inspection → Status/Notification.
- **Why people will use it:** a certificate valid for 2 years that gives a 10% discount on electricity and water bills.

## Slide 5. Live demo (screens in order)

1. **Landing page and sign-in:** citizen signs in (or uses Citizen Sign Up).
2. **Request form:** name, mobile number, pincode, address (GPS autofill), 8-digit property ID, and one live camera photo stamped with GPS coordinates and time.
3. **Routing result:** the tracker shows the authority and the assigned inspector for the pincode.
4. **Status tracker:** Submitted → Scheduled → Audited → Approved, plus the full application tracking view.
5. **Inspector and officer views:** the request appears for the matching authority.
6. **Admin dashboard:** city-wide statistics and pincode mapping.

*Keep screenshots of these six screens as a backup in case the network or camera fails.*

## Slide 6. Architecture

- Static HTML pages (Tailwind from a CDN) → `api/index.js` (Vercel serverless function) → Supabase.
- OpenStreetMap Nominatim turns GPS coordinates into an address and pincode.
- `localStorage` and `BroadcastChannel` keep open tabs in sync.
- **Stack:** HTML, CSS, JavaScript · Node.js · Supabase · Vercel. We used tools the team already knew, so more time went into building and testing.

## Slide 7. Key decisions and trade-offs

| Decision | Alternative considered | What we gave up |
|---|---|---|
| One complete flow in 72 hours | A broad platform for every waste problem | Breadth of features |
| Pincode-based routing | Boundary-based (GIS) lookup | Accuracy: a pincode can cover more than one authority |
| Inspector visits the site | Photo-based waste detection | Automation: every request needs a manual visit |
| Live camera photo only | Uploading any existing photo | Convenience, in exchange for a photo taken on site with GPS and time |

## Slide 8. AI usage

- **Used to build it:** a Gemini-based local workspace for the early prototype, and Claude for the submission documents (Decision Log, README, docs, this outline). Details in `ai.md`.
- **Inside the product:** none. Routing is a fixed pincode lookup and site verification is done by a human inspector.

## Slide 9. Limitations and what's next

| What breaks first | The fix |
|---|---|
| Wrong routing where a pincode covers more than one authority | Official MCC, Town Panchayat and Gram Panchayat boundary data with GIS mapping |
| Officer and inspector backlog as requests grow | Escalation for delayed requests, automated inspection reports, better analytics |
| Manual site checking for every request | Photo-based waste detection |
| Discount depends on utility providers accepting the certificate | Integration with existing civic systems |

- **Also to fix:** the demo sign-in accepts common passwords; it needs real server-side authentication.
- **First change to make:** connect official boundary data, because every later step depends on the request reaching the right office.

## Slide 10. Team and links

- Team Cryptile.
- Live app: https://hackthon-baz7.vercel.app/
- Repository: https://github.com/Harsha-HY/hackthon
- Documents: README, Decision Log, architecture, constraints, setup, limitations, `ai.md`.

---

### Before presenting

- [ ] The live app loads and one demo account is signed in.
- [ ] Do not quote the landing-page numbers (65 wards, 9 recycling facilities, 4.2-hour resolution) as results. They are page copy, not measured data.
- [ ] The AI slide matches `ai.md`.
- [ ] Every team member can answer a question about any slide.
- [ ] The deck fits the time limit, with screenshots ready as a backup.
