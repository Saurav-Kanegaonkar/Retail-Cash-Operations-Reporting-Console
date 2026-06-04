# Executive Findings

- Report reliability is strongest where source freshness and owner assignment are checked before Tableau refresh.
- Cash variance and service downtime should be triaged together because repeated jams often create reconciliation noise.
- The daily exception queue is the highest leverage scheduled report because it converts device, route, and merchant signals into assigned work.
- Top ranked exception: Travel center Smart safe 27 on Route C because of downtime.

## Recommendations

- Certify Tableau Prep inputs only after source freshness, key uniqueness, variance thresholds, and Excel-to-SQL reconciliation checks pass.
- Run the daily exception queue before operations huddles so field service, cash logistics, and reporting analytics share the same priority list.
- Convert recurring VLOOKUP checks into documented SQL controls with owner notes and acceptance tests.
