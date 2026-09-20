# Decision Log — Dhaara: Routing Requests by Pincode

[← Back to resource.md](../resource.md)

---

**Project:** Dhaara **Decision area:** Routing logic (request → correct authority) **Date:** 20 September 2026 **Author(s):** Team Cryptile

## Q1. What approach did we take, and what did we consider instead?

**Our approach:** Route each construction-waste request to the correct local authority using the pincode or location the user enters, then let that authority review it and send an inspector.

The user submits a request with their location or pincode. The citizen page (`citizen.html`, function `resolveAuthorityAndInspector`) matches the pincode to the responsible authority (MCC, Town Panchayat or Gram Panchayat), and the request is saved in our Supabase database through the API. The officer reviews and accepts it on the authority dashboard, and an inspector is assigned to visit the site. The user follows the progress through status tracking and notifications.

Flow: User → Pincode/Location → Authority → Officer Review → Request Accepted → Inspector Assigned → Site Inspection → Status/Notification.

**Alternative(s) considered:**
1. A broad waste-management platform that tries to solve every waste-related problem at once.
2. Making photo-based waste detection the main feature instead of an officer-and-inspector process.

## Q2. Why this approach? What did we give up?

| Dimension | Our approach (pincode routing + inspection) | Alternatives (broad platform / photo detection) |
|---|---|---|
| Build speed | One complete request flow could be built and demonstrated within the 72 hours. | Would have been only partly working in 72 hours. |
| Routing accuracy | Pincode is simple to use, but may not match authority boundaries exactly. | Boundary-based lookup is more exact but needs official boundary data we did not have. |
| Verification | An inspector visits and verifies the site before further action. | Automated photo detection is faster per request but harder to build and trust. |
| User adoption | Users get a certificate valid for 2 years that gives a 10% discount on electricity and water bills. | A plain reporting website gives users no direct benefit to come back for. |

Build speed decided it: we chose one complete, working flow over many half-finished features. What we gave up is accuracy and automation. Pincode areas do not always match MCC, Town Panchayat and Gram Panchayat boundaries, so some requests can reach the wrong office, and every request still needs a manual inspector visit.

## Q3. What breaks first at larger scale or in production, and how would it be fixed?

| What breaks first | Why (with a rough number if possible) | How it would be fixed |
|---|---|---|
| Wrong routing at boundaries | One pincode can cover areas that belong to more than one of the 3 authority types, so the request may go to the wrong office. | Connect official MCC, Town Panchayat and Gram Panchayat boundary data and use GIS mapping. |
| Officer and inspector backlog | Every request needs a manual review and a site visit, so delays grow as requests increase. | Escalation for delayed requests, automated inspection reports and better analytics. |
| Manual site checking | An inspector has to visit every site, even for clear cases. | Add photo-based waste detection to support the inspector. |
| Certificate benefit | The 10% discount for 2 years works only if electricity and water providers accept the certificate. | Integrate with existing civic systems. |

**First change to make:** connect official boundary data, because every later step depends on the request reaching the right office.
