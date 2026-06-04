import csv
import json
import math
import random
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUTPUTS = ROOT / "analysis" / "outputs"
SRC = ROOT / "src"

random.seed(42)


def money(value):
    return round(value, 2)


def write_csv(path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_text(path, body):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def weighted_choice(options):
    total = sum(weight for _, weight in options)
    pick = random.uniform(0, total)
    upto = 0
    for value, weight in options:
        if upto + weight >= pick:
            return value
        upto += weight
    return options[-1][0]


def build_entities():
    device_types = [
        ("ATM", 12),
        ("Cash recycler", 9),
        ("Smart safe", 7),
        ("Air vac", 5),
        ("Financial services kiosk", 3),
    ]
    merchant_segments = [
        "Convenience",
        "Grocery",
        "Travel center",
        "Fuel and c-store",
        "Restaurant",
        "Cash intensive retail",
    ]
    regions = ["Midwest", "Southeast", "Southwest", "Northeast", "West"]
    rows = []
    counter = 1
    for device_type, count in device_types:
        for _ in range(count):
            route = f"Route {chr(64 + ((counter - 1) % 8) + 1)}"
            segment = merchant_segments[(counter - 1) % len(merchant_segments)]
            region = regions[(counter + 1) % len(regions)]
            rows.append(
                {
                    "entity_id": f"DEV{counter:03d}",
                    "entity_name": f"{segment} {device_type} {counter:02d}",
                    "entity_type": device_type,
                    "segment": segment,
                    "owner_team": weighted_choice(
                        [
                            ("Field service", 32),
                            ("Cash logistics", 24),
                            ("Processing operations", 18),
                            ("Reporting analytics", 14),
                            ("Merchant support", 12),
                        ]
                    ),
                    "region_or_scope": region,
                    "route": route,
                    "business_priority": weighted_choice(
                        [("Critical", 18), ("High", 34), ("Medium", 34), ("Low", 14)]
                    ),
                    "risk_tier": weighted_choice(
                        [("High", 18), ("Medium", 38), ("Low", 44)]
                    ),
                    "monitoring_tool": weighted_choice(
                        [("Web monitoring portal", 45), ("Mobile app", 25), ("Portfolio portal", 20), ("Prep extract", 10)]
                    ),
                }
            )
            counter += 1
    return rows


def build_daily_metrics(entities):
    rows = []
    start = date(2026, 1, 1)
    for offset in range(120):
        day = start + timedelta(days=offset)
        weekday_factor = 1.12 if day.weekday() in [4, 5] else 1.0
        for entity in entities:
            risk = {"High": 1.35, "Medium": 1.0, "Low": 0.72}[entity["risk_tier"]]
            type_factor = {
                "ATM": 1.35,
                "Cash recycler": 1.1,
                "Smart safe": 0.95,
                "Air vac": 0.55,
                "Financial services kiosk": 0.8,
            }[entity["entity_type"]]
            base_txn = random.randint(65, 360) * type_factor * weekday_factor
            withdrawals = int(max(0, random.gauss(base_txn, base_txn * 0.16)))
            deposits = int(max(0, random.gauss(base_txn * 0.42, base_txn * 0.1)))
            uptime = min(100, max(80, random.gauss(98.7 - risk * 0.9, 1.6)))
            variance = random.gauss(0, 95 * risk * type_factor)
            if random.random() < 0.055 * risk:
                variance += random.choice([-1, 1]) * random.uniform(550, 2600)
            settlement_variance = variance * random.uniform(0.18, 0.42)
            jams = max(0, int(random.gauss(0.35 * risk * type_factor, 0.8)))
            downtime = max(0, (100 - uptime) * random.uniform(7, 19) + jams * random.randint(18, 70))
            quality_score = max(55, min(100, 100 - abs(variance) / 90 - downtime / 28 - jams * 1.8))
            priority = min(100, max(1, (100 - uptime) * 5.5 + abs(variance) / 55 + jams * 8 + risk * 11))
            rows.append(
                {
                    "date": day.isoformat(),
                    "entity_id": entity["entity_id"],
                    "metric_name": "device_daily_operations",
                    "withdrawal_transactions": withdrawals,
                    "deposit_transactions": deposits,
                    "surcharge_revenue": money(withdrawals * random.uniform(2.75, 3.65)),
                    "cash_loaded": money(max(0, withdrawals * random.uniform(54, 94))),
                    "cash_variance": money(variance),
                    "settlement_variance": money(settlement_variance),
                    "uptime_pct": round(uptime, 2),
                    "jam_count": jams,
                    "service_minutes_down": round(downtime, 1),
                    "automation_minutes_saved": int(max(12, random.gauss(42, 15)) if quality_score > 82 else random.gauss(22, 10)),
                    "quality_score": round(quality_score, 1),
                    "priority_score": round(priority, 1),
                    "report_ready_flag": "Y" if quality_score >= 82 and abs(variance) < 900 else "N",
                }
            )
    return rows


def build_source_events(entities):
    event_types = [
        "cash_load",
        "jam_clearance",
        "comms_alert",
        "cash_out_risk",
        "route_service",
        "report_refresh_delay",
        "merchant_question",
        "settlement_review",
    ]
    systems = [
        "ATM processor",
        "Cash logistics file",
        "Field service queue",
        "Merchant portal",
        "Tableau Prep extract",
        "Excel exception workbook",
    ]
    rows = []
    start = date(2026, 1, 1)
    for idx in range(720):
        entity = entities[idx % len(entities)]
        risk = {"High": 1.55, "Medium": 1.0, "Low": 0.65}[entity["risk_tier"]]
        event_type = weighted_choice(
            [
                ("cash_load", 16),
                ("jam_clearance", 15),
                ("comms_alert", 13),
                ("cash_out_risk", 12),
                ("route_service", 15),
                ("report_refresh_delay", 13),
                ("merchant_question", 8),
                ("settlement_review", 8),
            ]
        )
        age = max(1, int(random.gauss(16 * risk, 8)))
        severity = "High" if age > 28 or random.random() < 0.08 * risk else "Medium" if age > 13 else "Low"
        rows.append(
            {
                "event_id": f"EVT{idx + 1:04d}",
                "event_date": (start + timedelta(days=idx % 120)).isoformat(),
                "entity_id": entity["entity_id"],
                "source_system": random.choice(systems),
                "event_type": event_type,
                "owner_team": entity["owner_team"],
                "route": entity["route"],
                "severity": severity,
                "minutes_to_close": age * random.randint(11, 36),
                "evidence_note": f"{event_type.replace('_', ' ')} needs {entity['owner_team'].lower()} review",
                "status": weighted_choice([("open", 22), ("watch", 30), ("closed", 48)]),
            }
        )
    return rows


def build_quality_checks():
    rows = []
    start = date(2026, 4, 1)
    tables = [
        ("atm_transactions", "ATM processor"),
        ("cash_loads", "Cash logistics file"),
        ("service_tickets", "Field service queue"),
        ("device_master", "Merchant portal"),
        ("merchant_master", "Merchant portal"),
        ("report_output", "Tableau Prep extract"),
    ]
    check_types = ["freshness", "duplicate_key", "null_required_field", "threshold_breach", "definition_drift", "vlookup_reconcile"]
    counter = 1
    for offset in range(60):
        for table_name, system in tables:
            records = random.randint(7200, 224000)
            check_type = random.choice(check_types)
            base_rate = {
                "freshness": 0.012,
                "duplicate_key": 0.006,
                "null_required_field": 0.009,
                "threshold_breach": 0.018,
                "definition_drift": 0.004,
                "vlookup_reconcile": 0.015,
            }[check_type]
            if table_name in ["cash_loads", "service_tickets"]:
                base_rate *= 1.28
            fail_rate = max(0, random.gauss(base_rate, base_rate * 0.42))
            failed = int(records * fail_rate)
            severity = "High" if fail_rate > 0.04 else "Medium" if fail_rate > 0.018 else "Low"
            status = "fail" if severity == "High" else "watch" if severity == "Medium" else "pass"
            rows.append(
                {
                    "check_id": f"CHK{counter:04d}",
                    "run_date": (start + timedelta(days=offset)).isoformat(),
                    "source_system": system,
                    "table_name": table_name,
                    "check_type": check_type,
                    "records_checked": records,
                    "failed_records": failed,
                    "failure_rate_pct": round(fail_rate * 100, 2),
                    "severity": severity,
                    "status": status,
                    "business_rule": business_rule_for(check_type),
                }
            )
            counter += 1
    return rows


def business_rule_for(check_type):
    return {
        "freshness": "Source delivered before daily reporting cutoff",
        "duplicate_key": "Device, merchant, and date keys are unique",
        "null_required_field": "Required reporting dimensions are populated",
        "threshold_breach": "Cash and settlement variance remain inside tolerance",
        "definition_drift": "Metric logic matches the documented reporting definition",
        "vlookup_reconcile": "Excel lookup output agrees with SQL reconciliation",
    }[check_type]


def build_requirements():
    questions = [
        ("Operations leadership", "Which devices need action before the morning huddle?", "priority_score", "prioritize daily exceptions", "daily"),
        ("Cash logistics", "Which routes have repeat cash variance outside tolerance?", "cash_variance", "plan cash loads", "daily"),
        ("Field service", "Which machines are driving downtime and jam repeats?", "service_minutes_down", "dispatch technicians", "daily"),
        ("Merchant support", "Which merchant questions need evidence from transaction data?", "event_status", "resolve support questions", "daily"),
        ("Finance", "Which settlement variance needs review before payout?", "settlement_variance", "approve monthly payout", "weekly"),
        ("Analytics", "Which Prep checks block a trusted Tableau refresh?", "failed_records", "release certified report", "daily"),
        ("Executive team", "How many scheduled reports shipped on time?", "report_sla", "monitor reporting reliability", "weekly"),
        ("Processing operations", "Where are transaction feeds delayed or incomplete?", "freshness_status", "stabilize extracts", "daily"),
        ("Route managers", "Which routes combine high value and high risk?", "route_priority", "sequence route work", "weekly"),
    ]
    rows = []
    for idx, item in enumerate(questions, start=1):
        group, question, metric, decision, cadence = item
        rows.append(
            {
                "requirement_id": f"REQ{idx:03d}",
                "stakeholder_group": group,
                "business_question": question,
                "required_metric": metric,
                "decision_supported": decision,
                "refresh_cadence": cadence,
                "acceptance_test": weighted_choice(
                    [
                        ("sample reconciles to source extract", 28),
                        ("owner and next action are populated", 24),
                        ("daily refresh finishes before 8 AM", 22),
                        ("variance threshold is documented", 16),
                        ("report definition approved by stakeholder", 10),
                    ]
                ),
                "status": weighted_choice([("certified", 45), ("in build", 28), ("triaged", 18), ("new", 9)]),
            }
        )
    return rows


def build_report_runs():
    reports = [
        ("Daily exception queue", "daily", "Operations leadership"),
        ("Cash variance reconciliation", "daily", "Cash logistics"),
        ("Field service aging", "daily", "Field service"),
        ("Merchant payout review", "weekly", "Finance"),
        ("Prep validation scorecard", "daily", "Analytics"),
        ("Executive operating packet", "weekly", "Executive team"),
        ("Monthly performance close", "monthly", "Finance"),
    ]
    rows = []
    start = date(2026, 1, 1)
    idx = 1
    for offset in range(120):
        day = start + timedelta(days=offset)
        for name, cadence, owner in reports:
            if cadence == "weekly" and day.weekday() != 0:
                continue
            if cadence == "monthly" and day.day != 1:
                continue
            records = random.randint(1800, 260000)
            delay = max(0, int(random.gauss(8, 14)))
            if random.random() < 0.08:
                delay += random.randint(22, 84)
            status = "on time" if delay <= 40 else "late" if delay <= 90 else "blocked"
            rows.append(
                {
                    "run_id": f"RUN{idx:04d}",
                    "run_date": day.isoformat(),
                    "report_name": name,
                    "cadence": cadence,
                    "business_owner": owner,
                    "records_loaded": records,
                    "refresh_delay_minutes": delay,
                    "validation_status": weighted_choice([("passed", 76), ("warning", 18), ("failed", 6)]),
                    "distribution_status": status,
                }
            )
            idx += 1
    return rows


def build_actions(entities, metrics, events):
    latest_date = max(row["date"] for row in metrics)
    recent_dates = sorted({row["date"] for row in metrics})[-14:]
    metrics_by_entity = defaultdict(list)
    open_events = defaultdict(list)
    for row in metrics:
        if row["date"] in recent_dates:
            metrics_by_entity[row["entity_id"]].append(row)
    for row in events:
        if row["status"] != "closed":
            open_events[row["entity_id"]].append(row)
    entity_lookup = {row["entity_id"]: row for row in entities}
    rows = []
    for entity_id, entity_metrics in metrics_by_entity.items():
        entity = entity_lookup[entity_id]
        avg_priority = sum(float(row["priority_score"]) for row in entity_metrics) / len(entity_metrics)
        avg_uptime = sum(float(row["uptime_pct"]) for row in entity_metrics) / len(entity_metrics)
        variance = sum(abs(float(row["cash_variance"])) for row in entity_metrics)
        downtime = sum(float(row["service_minutes_down"]) for row in entity_metrics)
        jam_count = sum(int(row["jam_count"]) for row in entity_metrics)
        event_count = len(open_events[entity_id])
        composite = min(100, avg_priority + event_count * 2.8 + variance / 4200 + jam_count * 1.7)
        if composite < 45:
            continue
        reason = "cash variance" if variance > 9000 else "downtime" if downtime > 420 else "open service events"
        next_action = {
            "cash variance": "Reconcile cash load, deposit, and settlement extracts in SQL before payout review.",
            "downtime": "Dispatch field service and confirm machine health after the route visit.",
            "open service events": "Assign owner, close stale event notes, and refresh the exception report.",
        }[reason]
        rows.append(
            {
                "action_id": f"ACT{len(rows) + 1:03d}",
                "entity_id": entity_id,
                "entity_name": entity["entity_name"],
                "owner_team": entity["owner_team"],
                "route": entity["route"],
                "risk_driver": reason,
                "avg_uptime_pct": round(avg_uptime, 2),
                "fourteen_day_cash_variance": money(variance),
                "open_event_count": event_count,
                "composite_priority": round(composite, 1),
                "expected_value_or_cost_avoidance": int(variance * 0.58 + downtime * 38 + event_count * 420),
                "confidence": round(max(0.58, min(0.94, 0.68 + len(entity_metrics) / 100 + event_count / 80)), 2),
                "next_step": next_action,
                "target_report_date": latest_date,
            }
        )
    return sorted(rows, key=lambda row: row["composite_priority"], reverse=True)[:24]


def summarize(entities, metrics, quality_checks, actions, report_runs, requirements):
    latest_dates = sorted({row["date"] for row in metrics})[-14:]
    recent_metrics = [row for row in metrics if row["date"] in latest_dates]
    total_variance = sum(abs(float(row["cash_variance"])) for row in recent_metrics)
    uptime = sum(float(row["uptime_pct"]) for row in recent_metrics) / len(recent_metrics)
    downtime = sum(float(row["service_minutes_down"]) for row in recent_metrics)
    qa_saved = sum(int(row["automation_minutes_saved"]) for row in recent_metrics)
    high_actions = len([row for row in actions if float(row["composite_priority"]) >= 70])
    pass_checks = len([row for row in quality_checks if row["status"] == "pass"])
    quality_pass_rate = pass_checks / len(quality_checks)
    on_time = len([row for row in report_runs if row["distribution_status"] == "on time"])
    report_sla = on_time / len(report_runs)
    latest_quality = sorted(quality_checks, key=lambda row: row["run_date"])[-42:]
    prep_groups = []
    by_table = defaultdict(list)
    for row in latest_quality:
        by_table[row["table_name"]].append(row)
    for table, rows in sorted(by_table.items()):
        failed = sum(int(row["failed_records"]) for row in rows)
        status = "Blocked" if any(row["status"] == "fail" for row in rows) else "Watch" if any(row["status"] == "watch" for row in rows) else "Certified"
        prep_groups.append(
            {
                "source": table.replace("_", " ").title(),
                "checks": len(rows),
                "failedRecords": failed,
                "status": status,
                "rule": rows[-1]["business_rule"],
            }
        )
    report_groups = []
    by_report = defaultdict(list)
    for row in report_runs:
        by_report[row["report_name"]].append(row)
    for report, rows in sorted(by_report.items()):
        on_time_rate = len([row for row in rows if row["distribution_status"] == "on time"]) / len(rows)
        report_groups.append(
            {
                "report": report,
                "cadence": rows[-1]["cadence"],
                "owner": rows[-1]["business_owner"],
                "runs": len(rows),
                "onTimeRate": round(on_time_rate * 100, 1),
                "status": "Certified" if on_time_rate >= 0.9 else "Watch" if on_time_rate >= 0.78 else "Blocked",
            }
        )
    route_priority = defaultdict(float)
    route_count = defaultdict(int)
    for row in actions:
        route_priority[row["route"]] += float(row["composite_priority"])
        route_count[row["route"]] += 1
    route_chart = [
        {"route": route, "priority": round(route_priority[route] / route_count[route], 1)}
        for route in sorted(route_priority)
    ]
    device_mix = []
    for device_type in sorted({row["entity_type"] for row in entities}):
        count = len([row for row in entities if row["entity_type"] == device_type])
        device_mix.append({"type": device_type, "count": count})
    return {
        "cards": [
            {"label": "Scheduled report SLA", "value": f"{report_sla * 100:.0f}%", "detail": "on time distribution"},
            {"label": "Validation pass rate", "value": f"{quality_pass_rate * 100:.0f}%", "detail": "Prep checks passed"},
            {"label": "High priority exceptions", "value": str(high_actions), "detail": "need owner follow up"},
            {"label": "Avg device uptime", "value": f"{uptime:.1f}%", "detail": "last 14 days"},
            {"label": "Cash variance reviewed", "value": f"${total_variance / 1000:.0f}k", "detail": "absolute variance"},
            {"label": "QA hours saved", "value": f"{qa_saved / 60:.0f}", "detail": "estimated in 14 days"},
        ],
        "executive": {
            "findings": [
                "Report reliability is strongest where source freshness and owner assignment are checked before Tableau refresh.",
                "Cash variance and service downtime should be triaged together because repeated jams often create reconciliation noise.",
                "The daily exception queue is the highest leverage scheduled report because it converts device, route, and merchant signals into assigned work.",
            ],
            "routeChart": route_chart,
            "deviceMix": device_mix,
        },
        "exceptions": actions[:12],
        "prep": {
            "sources": sorted(prep_groups, key=lambda row: row["failedRecords"], reverse=True),
            "reports": sorted(report_groups, key=lambda row: row["onTimeRate"]),
            "requirements": requirements,
        },
        "summary": {
            "entities": len(entities),
            "dailyRows": len(metrics),
            "qualityChecks": len(quality_checks),
            "reportRuns": len(report_runs),
            "actions": len(actions),
        },
    }


def write_outputs(payload, actions, quality_checks):
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    write_text(OUTPUTS / "app_payload.json", json.dumps(payload, indent=2))
    write_csv(
        OUTPUTS / "exception_action_queue.csv",
        actions,
        [
            "action_id",
            "entity_id",
            "entity_name",
            "owner_team",
            "route",
            "risk_driver",
            "avg_uptime_pct",
            "fourteen_day_cash_variance",
            "open_event_count",
            "composite_priority",
            "expected_value_or_cost_avoidance",
            "confidence",
            "next_step",
            "target_report_date",
        ],
    )
    by_check = defaultdict(lambda: {"failed": 0, "records": 0, "count": 0})
    for row in quality_checks:
        key = row["check_type"]
        by_check[key]["failed"] += int(row["failed_records"])
        by_check[key]["records"] += int(row["records_checked"])
        by_check[key]["count"] += 1
    check_rows = []
    for check_type, values in sorted(by_check.items()):
        check_rows.append(
            {
                "check_type": check_type,
                "runs": values["count"],
                "records_checked": values["records"],
                "failed_records": values["failed"],
                "failure_rate_pct": round(values["failed"] / values["records"] * 100, 2),
                "business_rule": business_rule_for(check_type),
            }
        )
    write_csv(
        OUTPUTS / "prep_validation_summary.csv",
        check_rows,
        ["check_type", "runs", "records_checked", "failed_records", "failure_rate_pct", "business_rule"],
    )
    data_js = "window.dashboardData = " + json.dumps(payload, indent=2) + ";\n"
    write_text(SRC / "data.js", data_js)


def write_docs(payload):
    findings = payload["executive"]["findings"]
    top_action = payload["exceptions"][0]
    write_text(
        ROOT / "analysis" / "executive_findings.md",
        "\n".join(
            [
                "# Executive Findings",
                "",
                f"- {findings[0]}",
                f"- {findings[1]}",
                f"- {findings[2]}",
                f"- Top ranked exception: {top_action['entity_name']} on {top_action['route']} because of {top_action['risk_driver']}.",
                "",
                "## Recommendations",
                "",
                "- Certify Tableau Prep inputs only after source freshness, key uniqueness, variance thresholds, and Excel-to-SQL reconciliation checks pass.",
                "- Run the daily exception queue before operations huddles so field service, cash logistics, and reporting analytics share the same priority list.",
                "- Convert recurring VLOOKUP checks into documented SQL controls with owner notes and acceptance tests.",
            ]
        )
        + "\n",
    )
    write_text(
        ROOT / "analysis" / "analysis_plan.md",
        "\n".join(
            [
                "# Analysis Plan",
                "",
                "1. Profile device, route, and merchant reporting dimensions for missing owners and stale identifiers.",
                "2. Score the last 14 days of device metrics by uptime, cash variance, jam count, open event count, and data quality.",
                "3. Validate scheduled report runs against freshness, duplicate key, null field, definition drift, threshold, and reconciliation checks.",
                "4. Convert the highest priority exceptions into owner-specific next steps that can be distributed daily or weekly.",
            ]
        )
        + "\n",
    )
    write_text(
        ROOT / "analysis" / "recommendations.md",
        "\n".join(
            [
                "# Recommendations",
                "",
                "- Build a certified daily Tableau extract from ATM transactions, cash loads, service tickets, device master, merchant master, and report output checks.",
                "- Keep a human-readable exception queue for non-technical stakeholders and a SQL appendix for analyst review.",
                "- Retire manual spreadsheet lookups only after sample reconciliation passes and the business owner signs off on each metric definition.",
            ]
        )
        + "\n",
    )
    write_text(
        ROOT / "analysis" / "data_profile.md",
        "\n".join(
            [
                "# Data Profile",
                "",
                f"- Device and location master records: {payload['summary']['entities']}",
                f"- Daily device metric records: {payload['summary']['dailyRows']:,}",
                f"- Prep validation checks: {payload['summary']['qualityChecks']:,}",
                f"- Scheduled report runs: {payload['summary']['reportRuns']:,}",
                f"- Ranked exception actions: {payload['summary']['actions']}",
                "",
                "The synthetic source tables model common retail cash operations grains: device by day metrics, route and service events, scheduled report runs, stakeholder requirements, and source validation checks.",
            ]
        )
        + "\n",
    )
    write_text(
        ROOT / "analysis" / "sql_checks.sql",
        """-- Portfolio SQL appendix for a retail cash operations reporting workbench.
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
""",
    )
    write_text(
        ROOT / "data" / "README.md",
        "\n".join(
            [
                "# Data Sources",
                "",
                "Synthetic but role-realistic source tables for a retail cash operations reporting environment. The data is designed to be inspectable as a reporting and Tableau Prep artifact, not presented as real company performance.",
                "",
                "| File | Grain | Rows | Why it exists |",
                "|---|---:|---:|---|",
                f"| entities.csv | Device or location | {payload['summary']['entities']} | Device master with route, owner, region, risk, and monitoring tool fields. |",
                f"| daily_metrics.csv | Device by day | {payload['summary']['dailyRows']:,} | Daily ATM, cash-management, settlement, uptime, jam, and report-readiness metrics. |",
                "| source_events.csv | Source-system event | 720 | Service, cash-load, comms, refresh, merchant, and settlement events. |",
                "| stakeholder_requirements.csv | Requirement | 9 | Stakeholder questions, required metrics, decisions, cadence, and acceptance tests. |",
                f"| data_quality_checks.csv | Prep validation check | {payload['summary']['qualityChecks']:,} | Freshness, duplicate key, null, threshold, definition drift, and reconciliation checks. |",
                f"| report_runs.csv | Scheduled report run | {payload['summary']['reportRuns']:,} | Daily, weekly, and monthly distribution outcomes for recurring reports. |",
                f"| recommended_actions.csv | Ranked action | {payload['summary']['actions']} | Prioritized action queue with owner, evidence, value, confidence, and next step. |",
                "",
                "The generator in `scripts/score_operating_data.py` creates the source data, computed output tables, analysis notes, and static frontend payload.",
            ]
        )
        + "\n",
    )
    write_text(
        ROOT / "data_dictionary.md",
        "\n".join(
            [
                "# Data Dictionary",
                "",
                "| Field | Meaning |",
                "|---|---|",
                "| entity_id | Synthetic device or retail cash management object key. |",
                "| entity_type | ATM, cash recycler, smart safe, air vac, or financial services kiosk. |",
                "| route | Field service or cash logistics route. |",
                "| withdrawal_transactions | Daily withdrawal count for ATM and kiosk activity. |",
                "| deposit_transactions | Daily deposit count for store cash management activity. |",
                "| cash_variance | Absolute or signed variance between cash load, deposit, and reporting extract. |",
                "| settlement_variance | Variance requiring payout or finance review. |",
                "| uptime_pct | Daily machine availability percentage. |",
                "| jam_count | Daily jam or mechanical exception count. |",
                "| report_ready_flag | Whether the row is safe for certified reporting after quality checks. |",
                "| check_type | Tableau Prep or SQL validation rule category. |",
                "| business_rule | Human-readable rule a report owner can approve. |",
                "| composite_priority | Deterministic rank for the exception queue, based on operations risk and action value. |",
            ]
        )
        + "\n",
    )
    write_text(
        ROOT / "STATUS.md",
        "\n".join(
            [
                "# Retail Cash Operations Reporting Console Status",
                "",
                "- Status: upgraded through the Portfolio Artifact Upgrade Workflow.",
                "- Artifact type: BI reporting console plus Tableau Prep validation workbench.",
                "- Surfaces: executive report pulse, exception action queue, and Prep validation hub.",
                "- Data: synthetic, generated from documented retail cash operations assumptions.",
            ]
        )
        + "\n",
    )


def main():
    entities = build_entities()
    metrics = build_daily_metrics(entities)
    events = build_source_events(entities)
    quality_checks = build_quality_checks()
    requirements = build_requirements()
    report_runs = build_report_runs()
    actions = build_actions(entities, metrics, events)
    payload = summarize(entities, metrics, quality_checks, actions, report_runs, requirements)

    write_csv(
        DATA / "entities.csv",
        entities,
        ["entity_id", "entity_name", "entity_type", "segment", "owner_team", "region_or_scope", "route", "business_priority", "risk_tier", "monitoring_tool"],
    )
    write_csv(
        DATA / "daily_metrics.csv",
        metrics,
        [
            "date",
            "entity_id",
            "metric_name",
            "withdrawal_transactions",
            "deposit_transactions",
            "surcharge_revenue",
            "cash_loaded",
            "cash_variance",
            "settlement_variance",
            "uptime_pct",
            "jam_count",
            "service_minutes_down",
            "automation_minutes_saved",
            "quality_score",
            "priority_score",
            "report_ready_flag",
        ],
    )
    write_csv(
        DATA / "source_events.csv",
        events,
        ["event_id", "event_date", "entity_id", "source_system", "event_type", "owner_team", "route", "severity", "minutes_to_close", "evidence_note", "status"],
    )
    write_csv(
        DATA / "stakeholder_requirements.csv",
        requirements,
        ["requirement_id", "stakeholder_group", "business_question", "required_metric", "decision_supported", "refresh_cadence", "acceptance_test", "status"],
    )
    write_csv(
        DATA / "data_quality_checks.csv",
        quality_checks,
        ["check_id", "run_date", "source_system", "table_name", "check_type", "records_checked", "failed_records", "failure_rate_pct", "severity", "status", "business_rule"],
    )
    write_csv(
        DATA / "report_runs.csv",
        report_runs,
        ["run_id", "run_date", "report_name", "cadence", "business_owner", "records_loaded", "refresh_delay_minutes", "validation_status", "distribution_status"],
    )
    write_csv(
        DATA / "recommended_actions.csv",
        actions,
        [
            "action_id",
            "entity_id",
            "entity_name",
            "owner_team",
            "route",
            "risk_driver",
            "avg_uptime_pct",
            "fourteen_day_cash_variance",
            "open_event_count",
            "composite_priority",
            "expected_value_or_cost_avoidance",
            "confidence",
            "next_step",
            "target_report_date",
        ],
    )
    write_outputs(payload, actions, quality_checks)
    write_docs(payload)

    print("Generated retail cash operations reporting artifact")
    print(json.dumps(payload["summary"], indent=2))


if __name__ == "__main__":
    main()
