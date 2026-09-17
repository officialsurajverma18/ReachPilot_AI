# Architecture

                         ┌─────────────────────┐
                         │        USER         │
                         └──────────┬──────────┘
                                    │
                                    ▼
                  ┌─────────────────────────────┐
                  │          FRONTEND           │
                  │ HTML + CSS + Vanilla JS     │
                  │                             │
                  │ Dashboard │ Search │ Leads  │
                  │ Analytics │ Outreach        │
                  └─────────────┬───────────────┘
                                │
                                ▼
                  ┌─────────────────────────────┐
                  │       FLASK REST API        │
                  │                             │
                  │ Routes → Services → Utils   │
                  └──────┬──────────┬───────────┘
                         │          │
              ┌──────────┘          └─────────────┐
              ▼                                   ▼
   ┌─────────────────────┐             ┌─────────────────────┐
   │   DATA COLLECTION    │             │   AI / ML LAYER     │
   │                     │             │                     │
   │ Google Places       │             │ Data Cleaning       │
   │ Instagram           │             │ Feature Engineering │
   │ Facebook            │             │ ML Model            │
   │ Reddit              │             │ Lead Prediction     │
   └──────────┬──────────┘             └──────────┬──────────┘
              │                                   │
              └────────────────┬──────────────────┘
                               ▼
                    ┌─────────────────────┐
                    │   SUPABASE /        │
                    │   POSTGRESQL        │
                    │                     │
                    │ Leads               │
                    │ Lead Features       │
                    │ Lead Scores         │
                    │ Lead Outcomes       │
                    │ Licenses            │
                    │ Sales               │
                    │ Usage               │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     DASHBOARD       │
                    │                     │
                    │ Lead Score: 92      │
                    │ Status: HOT         │
                    │ Priority: High     │
                    └─────────────────────┘



# DataFlow

Google / Instagram / Facebook / Reddit
                  ↓
            Lead Collection
                  ↓
          Data Cleaning
                  ↓
         Normalization
                  ↓
        Duplicate Removal
                  ↓
        Feature Engineering
                  ↓
          ML Prediction
                  ↓
       Lead Quality Score
                  ↓
        Hot / Warm / Cold
                  ↓
       Store in Supabase
                  ↓
        Display on Dashboard
                  ↓
       AI-assisted Outreach
                  ↓
        Follow-up & Analytics


# Technology Architecture


Frontend
   │
   ├── HTML5
   ├── CSS3
   └── Vanilla JavaScript
          │
          ▼
Backend
   │
   ├── Python
   ├── Flask
   └── REST API
          │
    ┌─────┴─────────┐
    ▼               ▼
Database          ML / AI
    │               │
    ├── Supabase    ├── Scikit-learn
    └── PostgreSQL  ├── Pandas
                    ├── NumPy
                    └── OpenAI API