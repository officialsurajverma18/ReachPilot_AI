# Lead scoring methodology

ReachPilot AI uses Machine Learning to analyze collected business and social-media data and generate a Lead Quality Score (0–100).

ML Pipeline
Google / Instagram / Facebook / Reddit
                ↓
          Data Cleaning
                ↓
       Feature Engineering
                ↓
        Random Forest Model
                ↓
        Lead Quality Score
                ↓
       Hot / Warm / Cold
Main Features
Business rating and review count
Website, phone, and email availability
Social-media activity
Instagram/Facebook followers
Reddit mentions
Contact completeness
ML Technologies
Scikit-learn — model training
Pandas — data processing
NumPy — numerical operations
Random Forest — lead classification/scoring

The trained model is integrated with the Flask backend and stores lead scores in Supabase/PostgreSQL for display and prioritization in the dashboard.
