# Data Sources

Synthetic but role-realistic source tables for retail cash operations reporting. The goal is to make the project inspectable as an analytical artifact, not just a screen mockup.

| File | Grain | Rows | Why it exists |
|---|---:|---:|---|
| entities.csv | Entity / domain object | 24 | Defines the core operating objects, owners, segments, and risk tiers. |
| daily_metrics.csv | Entity x day x metric | 2880 | Tracks movement, comparison values, quality, defect rate, and automation savings over 120 days. |
| source_events.csv | Source-system event | 720 | Captures refresh delays, QA failures, stakeholder asks, release reviews, and manual overrides. |
| stakeholder_requirements.csv | Requirement | 80 | Connects stakeholder questions to metrics, decisions, refresh cadence, and acceptance tests. |
| data_quality_checks.csv | Data quality check | 360 | Shows freshness, duplicates, nulls, definition drift, and threshold failures by source table. |
| recommended_actions.csv | Recommendation | 90 | Converts analysis into prioritized actions with owner, value estimate, confidence, and next step. |

The data is intentionally shaped like something a product, analytics, or operations team could load into SQL, a notebook, or a BI layer.
