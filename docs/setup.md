# Setup & Run

[← Back to README](../README.md)

This describes how to install and run Dhaara as the repository currently defines it. The commands come from `package.json`.

## Try the live app

Open https://hackthon-baz7.vercel.app/ and sign in with one of the [demo accounts](#demo-accounts) below. No installation is needed.

## Prerequisites

- **Node.js.** The version is not pinned anywhere in the repository (no `.nvmrc`, no `engines` field), so use a current LTS release.
- **npm**, since `package-lock.json` is present.
- **A Supabase project**, to supply the two required environment variables below.
- **Git**, to clone the repository and switch to the `hack` branch, which holds the current application.

## Getting the code

```bash
git clone https://github.com/Harsha-HY/hackthon.git
cd hackthon
git checkout hack
```

## Environment variables

The repository ships `.env.example` with these three variables (the values are placeholders, not real credentials):

```bash
# Supabase Database Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key

# Server Port
PORT=8000
```

Create a `.env` file at the repository root with your own `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` (from your Supabase project's API settings), and set `PORT` to the port you want. `.env` is excluded by `.gitignore`, so it will not be committed. The service-role key is a privileged server-side key: keep it in `.env` or in your hosting environment settings, and never put it in an HTML page.

## Install dependencies

```bash
npm install
```

This installs the two dependencies in `package.json`: `@supabase/supabase-js` (^2.116.0) and `dotenv` (^18.0.1).

## Run

```bash
npm start
```

This runs `node server.js`, as set in the `start` script. Then open the page you want in the browser, for example `index.html`. The pages link to each other with relative links (`auth.html`, `citizen.html`, `dashboard.html`, `inspector.html`, `officer.html?auth=<dept>`), so any of them can be the entry point once the API is reachable.

## Deployment

`vercel.json` rewrites every `/api/:match*` request to `/api/index.js`, so the project deploys on **Vercel**, where `api/index.js` runs as a serverless function. Locally, `npm start` runs `server.js` instead. The live deployment is https://hackthon-baz7.vercel.app/. To deploy your own copy, import the repository into Vercel and add `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` in the project's environment variable settings.

## Demo accounts

`auth.html` contains a `SYSTEM_ACCOUNTS` list that works as a fallback sign-in. These are **demo credentials for testing only**, and they are visible to anyone who views the page source.

| Role | Email | Password |
|---|---|---|
| Admin | `admin@gmail.com` | `123` |
| MCC officer | `mcc@gmail.com` | `123` |
| Gram Panchayat officer | `gp@gmail.com` | `123` |
| Town Panchayat officer | `tp@gmail.com` | `123` |
| MCC inspector | `inspector.mcc@gmail.com` | `123` |
| Citizen | `citizen@gmail.com` | `123` |

The sign-in code also accepts a short list of common fallback passwords (`123`, `123456`, `admin123`, `password`, `1234`, `1111`, `12345`, `pass123`) for any registered email, so these passwords are interchangeable. This is recorded in [limitations.md](./limitations.md). Remove the demo accounts and the fallback before any real use.

**Suggested way to check the flow:** sign in as the citizen and submit a request with a pincode from the lists in `citizen.html` (for example `570001` for MCC, `570026` for Gram Panchayat, `570018` for Town Panchayat), then sign in as the inspector and officer accounts to see the request from their side.

## Not specified in the repository

- No seed-data script for Supabase. The demo data lives in client-side JavaScript, not in a SQL seed file or migration.
- No offline mode: no service worker, offline queue or PWA manifest.
- No automated test command in `package.json`.
- The contents of `server.js` were not reviewed for this document, so the exact port and startup behavior are not confirmed. The `PORT` variable is the likely control point.

See also [architecture.md](./architecture.md).
