# Data Dictionary

| Field | Meaning |
|---|---|
| entity_id | Synthetic device or retail cash management object key. |
| entity_type | ATM, cash recycler, smart safe, air vac, or financial services kiosk. |
| route | Field service or cash logistics route. |
| withdrawal_transactions | Daily withdrawal count for ATM and kiosk activity. |
| deposit_transactions | Daily deposit count for store cash management activity. |
| cash_variance | Absolute or signed variance between cash load, deposit, and reporting extract. |
| settlement_variance | Variance requiring payout or finance review. |
| uptime_pct | Daily machine availability percentage. |
| jam_count | Daily jam or mechanical exception count. |
| report_ready_flag | Whether the row is safe for certified reporting after quality checks. |
| check_type | Tableau Prep or SQL validation rule category. |
| business_rule | Human-readable rule a report owner can approve. |
| composite_priority | Deterministic rank for the exception queue, based on operations risk and action value. |
