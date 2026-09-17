# Lead scoring methodology

This release uses an explainable rules-based lead qualification score, not a fabricated machine-learning model. The signals are public rating, review volume, website availability, and direct phone availability. Each applied signal is returned as a score factor.

Before replacing this with scikit-learn, collect real outcome labels (for example, contacted/replied/converted) under a documented consent and retention policy. Split by time or campaign, evaluate against a simple baseline, and disclose limitations in the project report. Until then, do not market this component as a trained production ML model.
