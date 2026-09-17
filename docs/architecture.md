# Architecture

`template.html` is the primary UI and is served by Flask. Browser-side API calls use `fetch` and only call `/api/*`; no provider secret is sent to the browser.

Routes are split by responsibility: authentication, businesses, leads, scoring, outreach, analytics, exports, and follow-ups. Services contain external-provider work and business logic. SQLite makes the project runnable without infrastructure; setting `DATABASE_URL` selects PostgreSQL for Supabase/Render.

Existing legacy licensing tables (`licenses`, `sales`, `usage`) are never created, changed, or deleted by `database/schema.sql`.
