# ReachPilot AI

ReachPilot AI is a Flask and vanilla-JavaScript lead discovery and management project. The original glassmorphism dashboard remains the visual source of truth in `template.html`; its design system has been split into reusable frontend pages, CSS, and JavaScript modules served by Flask.

## Run locally

1. Create and activate a Python 3.11+ virtual environment.
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env`; set `GOOGLE_MAPS_API_KEY` to enable live business discovery.
4. Start: `python -m backend.app`
5. Open `http://localhost:5000`.

Without `DATABASE_URL`, data is stored locally in `instance/reachpilot.sqlite3`. On Render, set `DATABASE_URL` to the Supabase PostgreSQL connection URL and add all secrets in Render's environment settings.

## Existing Supabase licensing database

The activation screen looks up a purchase email in the existing `licenses` table, fills the matching active key, then validates it before opening the workspace. Configure Render with the Supabase PostgreSQL connection string as `DATABASE_URL`; the app expects the existing columns shown in the project: `key`, `email`, `plan`, `status`, `lead_cap`, `active`, `created_at`, and `expires_at`. A missing, inactive, or expired record returns **“No active key found”** in the UI.

Do not add Supabase keys, `DATABASE_URL`, `ADMIN_SECRET`, Google Maps keys, or OpenAI keys to frontend files. Store them only in Render environment variables or the local `.env` file.

## Scoring note

The current score is a transparent, deterministic qualification rubric based on rating, review volume, website, and phone availability. It is intentionally not labelled as a trained ML prediction: the included project contains no verified historical outcome dataset. Score factors are returned with each lead for a clear viva/demo explanation.

## API highlights

- `POST /api/businesses/search` — Google Places search, normalization, deduplication, lead creation
- `GET/POST/PUT/DELETE /api/leads` — lead management
- `POST /api/leads/<id>/score` — recalculate transparent score
- `POST /api/outreach/generate-message` — OpenAI if configured, otherwise a disclosed template fallback
- `GET /api/analytics/dashboard`, `GET /api/export/leads/csv`
- `GET/POST/PUT /api/followups`

The legacy desktop project is intentionally retained unchanged under `old_project/` as a reference for its CSV workflow, email discovery/sending, WhatsApp links, and license server integration.

See [production readiness](docs/production-readiness.md) before deploying publicly. `render.yaml` provides the Render service definition; set its secret variables in the Render dashboard rather than committing them.
