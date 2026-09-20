# Demo Video Guide — Dhaara

[← Back to resource.md](../resource.md)

**Project:** Dhaara **Team:** Cryptile **Target length:** 3 minutes **Live app:** https://hackthon-baz7.vercel.app/

---

## 1. Before you record

- [ ] Use a device with a camera and location turned on, and allow both when the browser asks. The photo step works only through the live camera.
- [ ] Sign in ahead of time in separate browser windows: a citizen, the MCC inspector and the admin (accounts are in [setup.md](../docs/setup.md)). Do not show the password fields on screen.
- [ ] **Use pincode 570001 for the submitted request** so it goes to the MCC, whose inspector (`inspector.mcc@gmail.com`) and officer (`mcc@gmail.com`) accounts are listed in `setup.md`. Show 570026 and 570018 only as typed examples.
- [ ] Prepare the values to type: a name, a 10-digit mobile number, the address (or use Autofill by GPS), and an 8-digit property ID such as `40291001`.
- [ ] If the citizen page shows a lock banner because that account already has an active request, use a fresh citizen account for the take (Citizen Sign Up).
- [ ] Close other tabs and notifications. **Never show `.env`, the Supabase key or any token.**

## 2. Script and timing

| Time | Section | What to say | What to show |
|---|---|---|---|
| 0:00–0:15 | Intro | "This is Dhaara by Team Cryptile. It sends construction-waste requests in Mysuru to the correct local authority." | Landing page |
| 0:15–0:35 | Problem | "Mysuru has the MCC, Town Panchayats and Gram Panchayats. People do not know which office to approach, so requests go to the wrong place or nowhere." | Landing page, or a slide with pincodes 570026, 570018 and 570001 |
| 0:35–1:35 | Citizen demo | "The citizen signs in and fills the form. The pincode decides the authority. The photo is taken live and stamped with GPS and time." | Sign in → form → enter pincode `570001` → autofill address → capture the live photo → **Submit Application** |
| 1:35–1:55 | Tracking | "The citizen sees the authority, the assigned inspector and the status: Submitted, Scheduled, Audited, Approved." | Live status card, then **View Full Application Tracking** |
| 1:55–2:20 | Inspector, officer and admin | "The same request appears for the MCC inspector. The admin sees city-wide statistics and pincode mapping." | Inspector queue → officer page → admin dashboard (a few seconds each) |
| 2:20–2:45 | How it is built and one trade-off | "Static pages, a Vercel function and Supabase. We chose one complete flow in 72 hours. The trade-off is that pincode routing is not exact for boundary areas." | Architecture diagram from `architecture.md` |
| 2:45–3:00 | Limits and close | "Next: official boundary data and photo-based detection. Dhaara: the right request to the right office." | Live link and team names |

*If the video must be shorter, cut the officer and admin views first and keep the citizen demo.*

## 3. Notes for the narration

- Say what the user sees and why it matters, not only what you click.
- Mention the certificate once: people who use Dhaara get a certificate valid for 2 years that gives a 10% discount on electricity and water bills.
- Do not quote the landing-page numbers (65 wards, 9 recycling facilities, 4.2-hour resolution) as results. They are page copy.
- If the camera or GPS fails, say so, then show the backup screenshots. Do not cut the problem out.

## 4. Recording tips

- Record at 1080p or higher, with the browser zoomed so text is readable on a phone.
- Use a quiet room and a headset or phone microphone.
- Speak a little slower than normal and pause between steps.
- Hide the bookmarks bar and use a clean browser window.

## 5. Upload and share

- Export as MP4 and check the sound before uploading.
- Set the link so it opens without signing in, and test it in a private window.
- Add the video link to `README.md`.

---

### Before submitting

- [ ] The video is within the time limit.
- [ ] It shows one full request, from the citizen form to the tracker.
- [ ] It states the problem, one trade-off and one next step.
- [ ] No keys, tokens or password fields appear on screen.
