# Analytical Recommendations

## What Stands Out

- Service exceptions explain more operational risk than cash volume alone when machines repeatedly miss uptime targets.
- Excel-heavy reporting creates avoidable delays where branch, route, and device identifiers are not standardized.
- The highest-value automation is a daily exception queue that tells operations which machines need action first.

## Recommended Operating Moves

- Standardize branch, route, and device identifiers before automating Tableau Prep flows.
- Create a daily exception report that ranks devices by downtime, cash variance, and service aging.
- Move weekly VLOOKUP reconciliation into SQL-backed validation checks with clear owner notes.

## How I Would Use The Data

1. Start with `daily_metrics.csv` to identify entities with worsening priority scores.
2. Join `source_events.csv` to separate true business movement from freshness or definition issues.
3. Use `stakeholder_requirements.csv` to confirm whether the dashboard is answering a decision, not just visualizing a number.
4. Use `data_quality_checks.csv` to block recommendations where the source is unreliable.
5. Push the final action queue from `recommended_actions.csv` into roadmap or operating review follow-up.
