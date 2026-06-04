# Data Sources

Synthetic but role-realistic source tables for a retail cash operations reporting environment. The data is designed to be inspectable as a reporting and Tableau Prep artifact, not presented as real company performance.

| File | Grain | Rows | Why it exists |
|---|---:|---:|---|
| entities.csv | Device or location | 36 | Device master with route, owner, region, risk, and monitoring tool fields. |
| daily_metrics.csv | Device by day | 4,320 | Daily ATM, cash-management, settlement, uptime, jam, and report-readiness metrics. |
| source_events.csv | Source-system event | 720 | Service, cash-load, comms, refresh, merchant, and settlement events. |
| stakeholder_requirements.csv | Requirement | 9 | Stakeholder questions, required metrics, decisions, cadence, and acceptance tests. |
| data_quality_checks.csv | Prep validation check | 360 | Freshness, duplicate key, null, threshold, definition drift, and reconciliation checks. |
| report_runs.csv | Scheduled report run | 518 | Daily, weekly, and monthly distribution outcomes for recurring reports. |
| recommended_actions.csv | Ranked action | 24 | Prioritized action queue with owner, evidence, value, confidence, and next step. |

The generator in `scripts/score_operating_data.py` creates the source data, computed output tables, analysis notes, and static frontend payload.
