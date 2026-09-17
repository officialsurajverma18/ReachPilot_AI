ReachPilot AI uses a Flask REST API to connect the frontend with lead generation, lead management, ML scoring, AI outreach, analytics, and export services.

Base URL
/api
Authentication
POST /api/auth/login
POST /api/auth/register
POST /api/auth/logout

Authentication is handled by the backend middleware. API credentials and secret keys are stored using environment variables.

Business & Lead APIs
Search Businesses
POST /api/businesses/search

Searches businesses using configured data sources such as Google Places.

Get Business
GET /api/businesses/{id}

Returns details of a specific business.

Get Leads
GET /api/leads

Returns collected leads.

Create Lead
POST /api/leads

Creates a new lead from collected business information.

Update Lead
PUT /api/leads/{id}

Updates lead information or status.

Delete Lead
DELETE /api/leads/{id}

Deletes a lead.

ML Scoring APIs
Generate Lead Score
POST /api/leads/{id}/score

Processes the lead through the ML model and returns a quality score.

Example response:

{
  "lead_id": "123",
  "score": 91.5,
  "classification": "Hot"
}
Get Lead Score
GET /api/leads/{id}/score

Returns the latest calculated score.

AI Outreach
Generate Message
POST /api/outreach/generate-message

Generates personalized outreach content using the available lead information.

Email
POST /api/outreach/email

Handles email outreach functionality.

WhatsApp
POST /api/outreach/whatsapp

Handles WhatsApp communication functionality where configured.

Analytics
GET /api/analytics/dashboard

Returns dashboard statistics such as lead counts, lead classifications, and scoring information.

Follow-ups
GET /api/followups
POST /api/followups
PUT /api/followups/{id}

Used to create, view, and update lead follow-ups.

Export
Export Leads
GET /api/export/leads/csv

Exports lead information in CSV format.

API Flow
Frontend
   ↓
Flask REST API
   ↓
Routes
   ↓
Services
   ↓
ML / AI / External APIs
   ↓
Supabase / PostgreSQL
   ↓
API Response
   ↓
Frontend
Main API Modules
Module	Responsibility
auth_routes.py	Authentication
business_routes.py	Business search
lead_routes.py	Lead management
scoring_routes.py	ML lead scoring
outreach_routes.py	AI communication
analytics_routes.py	Dashboard analytics
export_routes.py	CSV export