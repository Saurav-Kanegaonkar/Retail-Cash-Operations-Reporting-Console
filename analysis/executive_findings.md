# Executive Findings

- Service exceptions explain more operational risk than cash volume alone when machines repeatedly miss uptime targets.
- Excel-heavy reporting creates avoidable delays where branch, route, and device identifiers are not standardized.
- The highest-value automation is a daily exception queue that tells operations which machines need action first.

## Recommendations

- Standardize branch, route, and device identifiers before automating Tableau Prep flows.
- Create a daily exception report that ranks devices by downtime, cash variance, and service aging.
- Move weekly VLOOKUP reconciliation into SQL-backed validation checks with clear owner notes.
