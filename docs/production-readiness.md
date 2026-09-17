# Production readiness

## Implemented baseline

- Flask runs through Gunicorn using `wsgi.py`; debug mode is off by default.
- Render blueprint: `render.yaml` has a health-check endpoint and required production environment variables.
- `DATABASE_URL`, Google Maps, OpenAI, SMTP, and Supabase credentials are server-only environment variables.
- Security headers, secure production session cookies, request-size limits, and proxy awareness are enabled.
- The sign-up and license lookup flows use Flask APIs; no database connection string or Supabase secret enters browser JavaScript.
- When `REQUIRE_LICENSE=true`, business discovery requires an active key in `licenses` and records successful result counts in the existing `usage` table by month.
- Google Places discovery, normalization, deduplication, lead records, scores, follow-ups, outreach drafts, and CSV export have API coverage.

## Required before a public launch

1. Set a real Supabase PostgreSQL `DATABASE_URL`, a strong `SECRET_KEY`, and all third-party keys in Render. Run a staging smoke test against a non-production Supabase project first.
2. Apply `database/schema.sql` using a migration workflow and confirm it does not alter the existing `licenses`, `sales`, or `usage` tables.
3. Configure a custom domain, HTTPS, backup/restore policy, error monitoring, and log retention.
4. Add consent, privacy, retention, and deletion policies before storing personal contact information.
5. Obtain approved official API access for Meta (Facebook/Instagram) and Reddit. Do not scrape protected pages or bypass platform restrictions.
6. Train and validate an ML model only after collecting legitimate, labelled outcomes such as reply or conversion. The present score is intentionally an explainable rubric, not a trained production ML model.
7. Perform load testing, security review, provider quota testing, and end-to-end license/usage tests in staging.

## Environment variables

Required: `ENVIRONMENT=production`, `SECRET_KEY`, `DATABASE_URL`, `REQUIRE_LICENSE=true`, `GOOGLE_MAPS_API_KEY`.

Optional by enabled feature: `OPENAI_API_KEY`, `SMTP_HOST`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD`, `SMTP_FROM`.
