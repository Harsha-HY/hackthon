# AI Usage Disclosure

[← Back to README](./README.md)

**Project:** Dhaara — Smart Civic C&D Waste Routing, Mysuru
**Team:** Cryptile
**Live app:** https://hackthon-baz7.vercel.app/
**Repository:** https://github.com/Harsha-HY/hackthon (branch `hack`)

This separates AI tools used **to build** this project from AI **inside the product itself**. Tool usage is claimed only where there is direct evidence for it.

## Summary

| Question | Answer |
|---|---|
| Were AI tools used during development? | Yes — a Gemini-based local workspace (see Section 1) and Claude for documentation |
| Does the product use AI/ML at runtime? | yes |
| Roughly how much of the code was AI-assisted? | [Tfrontend 35% database 10% server.js 20%] |

## 1. AI Tools Used During Development

| Tool | Model / plan | Used by | What it was used for |
|---|---|---|---|
| Gemini-based local workspace (`.gemini\antigravity\scratch` path) | Not specified | Team | Early prototype: `build_index.py` writes its output to `C:\Users\harsh\.gemini\antigravity\scratch\mysuru-civic-routing\index.html`, which shows this folder was created in that workspace |
| Claude (Anthropic), claude.ai chat | Not specified | Team | Submission documents only: reformatting the Decision Log to one page and into the Q1–Q3 template, converting it to PDF, and drafting this disclosure. No application code was written in this chat |

**Reference design:** the README states the first UI was replicated from a Lovable-hosted app (`hello-web-magic-70.lovable.app`). Lovable is an AI app-building platform. The repository does not say whether that original app was AI-generated.

## 2. Where AI Helped in the Codebase

- **`build_index.py` and the earlier prototype `README.md`:** the Gemini-based workspace path above ties these to that tool.
- **Other files** (`auth.html`, `citizen.html`, `dashboard.html`, `inspector.html`, `officer.html`, `server.js`, `api/`): the repository contains no file-level record of AI assistance, so none is claimed here beyond what the team states in the Summary table.
- **Note:** `README.md` still describes the earlier general waste-routing prototype ("Exact Clone"), not the current Construction & Demolition platform that is deployed.

## 3. AI Inside the Product (runtime)

**None.** `package.json` lists only two dependencies, `@supabase/supabase-js` and `dotenv`. There is no LLM API, ML model, inference SDK or AI-branded package. The "smart" behavior in the product is:

- **Hardcoded PIN-to-authority lookup tables** in `citizen.html` (`resolveAuthorityAndInspector`) that route a request to the MCC, Town Panchayat or Gram Panchayat. This is a fixed lookup, not a trained model.
- **OpenStreetMap Nominatim** for reverse geocoding, with a fixed coordinate-zone fallback. This is a geocoding service, not an AI/ML service.
- **Browser camera and GPS capture** to attach a geotagged site photo. The photo is stamped with coordinates and a timestamp; no image recognition is performed.

## 4. Key Prompts

Not retained. No prompt history is stored in the repository.

## 5. How AI Output Was Verified

The team tested the request flow end to end (citizen → pincode routing → officer → inspector → status) and demonstrated it as a live MVP deployed on Vercel. Routing rules and inspector assignment are plain code that can be read and checked, and site verification is done by a human inspector.

## 6. What Was Deliberately Not Done With AI

- **Routing** is a fixed, readable PIN lookup, not an AI decision.
- **Site verification** is done by an inspector visiting the location, not by automated analysis.
- **Photo-based waste detection** was left as a future improvement and is not in the product.

---

**Note:** Sections 1–3 are based on the repository contents (README, `build_index.py`, `package.json`, `citizen.html`) and on how Claude was used in preparing the submission documents. Sections 4–6 describe the team's process and the product's design.
