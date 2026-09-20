# Known Limitations

[← Back to README](../README.md)

These are limitations found in the current implementation. None of them has been fixed yet. Each item includes a suggested fix.

## Security & authentication

| Limitation | Where | Suggested fix |
|---|---|---|
| **Universal password fallback.** If the exact password does not match, `checkUserCredentials()` accepts a fixed list of common passwords (`123`, `123456`, `admin123`, `password`, `1234`, `1111`, `12345`, `pass123`) for any account, including the admin. | `auth.html` | Remove the fallback and check passwords only on the server. |
| **Plaintext credentials in the page.** The `SYSTEM_ACCOUNTS` array holds account emails and passwords in the shipped JavaScript, visible to anyone viewing the source, with no hashing. | `auth.html` | Remove the array and use hashed passwords, or Supabase Auth. |
| **Admin guard grants access by default.** `checkAdminAuth()` is commented "Open Access". If no `current_user` is found, it creates a default Super Admin session instead of redirecting to `auth.html`, so opening `dashboard.html` directly gives admin access. | `dashboard.html` | Redirect to `auth.html` when no valid session exists, and check the role on the server for every admin API call. |
| **Service-role key in use.** `SUPABASE_SERVICE_ROLE_KEY` is the configured key. It bypasses row-level security and is meant for trusted servers only. It is used from the server side, but it was not confirmed that it is never exposed to the browser, because `api/index.js` was not reviewed. | `.env.example`, `api/index.js` | Confirm it is never sent to the client, and use row-level security with a lower-privilege key where possible. |
| **No CSRF protection, rate limiting or session expiry** in any client file reviewed. `current_user` stays in `localStorage` and `sessionStorage` until the user signs out. | All pages | Add session expiry and rate limiting on the API. |

## Data integrity

- **Routing runs in the browser.** `resolveAuthorityAndInspector()` in `citizen.html` picks the authority from hardcoded pincode lists. Someone who edits browser state or the request could submit a mismatched authority. Whether the server checks this again was not confirmed. *Suggested fix:* resolve the authority on the server from one shared table.
- **`localStorage` acts as a source of truth, not only a cache.** `dashboard.html` (`loadData()`) and `inspector.html` (`getMyAssignedApplications()`) merge API data, `localStorage` and hardcoded seed data, then remove duplicates by `id`. If the API is unreachable, seed data such as `BASELINE_SUBMITTED_APPLICATIONS` is shown as if it were live, with nothing to tell it apart from real submissions. *Suggested fix:* mark seed data clearly or remove it, and treat the database as the single source of truth.
- **Cross-tab sync has no server confirmation.** `BroadcastChannel('civic_sync_channel')` messages make other tabs reload from whatever `localStorage` or API state exists at that moment, without checking the message.

## Product and scope limitations

These come from the Decision Log's list of what was left for later:

- **Pincode is not an exact boundary.** A pincode can cover areas that belong to more than one authority. Official MCC, Town Panchayat and Gram Panchayat boundary data would fix this.
- **Every request needs a manual review and site visit.** There is no photo-based waste detection or automated inspection report, and no escalation for delayed requests.
- **Analytics are basic.** Better analytics and integration with existing civic systems are still to be done.
- **The 10% bill discount is not connected to any utility.** The certificate (valid for 2 years) gives a discount only if electricity and water providers accept it. No integration with them was found in the repository.

## Repository consistency

- **Old prototype files remain.** `build_index.py` and the hero images in `assets/` belong to an earlier "Smart Civic Waste Routing" prototype copied from `hello-web-magic-70.lovable.app`. `build_index.py` writes to a local Windows path (`C:\Users\harsh\.gemini\antigravity\scratch\mysuru-civic-routing\index.html`), so nobody else can run it as it is. *Suggested fix:* remove these files or move them to a separate folder.

## Coverage gaps in this documentation

- The contents of `api/`, `lib/`, `src/` and `server.js` were not reviewed. The real implementation of each `/api/...` endpoint (validation, error handling, Supabase queries) is not documented here.
- `officer.html` and `main_content.html` were not read in detail. `officer.html` is reached from `auth.html` through `officer.html?auth=<dept>`, and the purpose of `main_content.html` was not determined.
- `package-lock.json` was not read. Only the two top-level dependencies in `package.json` are documented.

## Other gaps

- **No offline support.** The app needs network access to Supabase (through the API), Nominatim, Google Fonts and the Tailwind CDN to work and look right.
- **No automated tests.** `package.json` has no `test` script.
- **English only, with no accessibility work.** No Kannada copy, accessibility features or low-bandwidth fallback were found, and each page loads several CDN scripts (Tailwind, and React, Babel and Chart.js on `dashboard.html`).
