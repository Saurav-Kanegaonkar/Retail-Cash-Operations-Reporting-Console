-- Portfolio SQL appendix for a retail cash operations reporting workbench.
-- These examples are written against the synthetic CSV table names in this repository.

-- 1. Daily exception queue for the morning operations huddle.
select
  a.entity_id,
  a.entity_name,
  a.owner_team,
  a.route,
  a.risk_driver,
  a.composite_priority,
  a.next_step
from recommended_actions a
where a.composite_priority >= 70
order by a.composite_priority desc;

-- 2. Tableau Prep validation checks that should block a certified refresh.
select
  run_date,
  source_system,
  table_name,
  check_type,
  failed_records,
  business_rule
from data_quality_checks
where status = 'fail'
order by run_date desc, failed_records desc;

-- 3. Excel lookup replacement check using source keys and variance tolerance.
select
  entity_id,
  date,
  cash_variance,
  settlement_variance,
  report_ready_flag
from daily_metrics
where abs(cash_variance) > 900
   or abs(settlement_variance) > 350
   or report_ready_flag = 'N';

-- 4. Scheduled reports that missed distribution SLA.
select
  report_name,
  cadence,
  business_owner,
  refresh_delay_minutes,
  validation_status,
  distribution_status
from report_runs
where distribution_status <> 'on time'
order by refresh_delay_minutes desc;
