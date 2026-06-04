window.dashboardData = {
  "cards": [
    [
      "Report freshness",
      "96%",
      "+10 pp"
    ],
    [
      "Service exceptions",
      "23",
      "open"
    ],
    [
      "Cash variance",
      "$18k",
      "weekly"
    ],
    [
      "QA hours saved",
      "8",
      "weekly"
    ]
  ],
  "table": [
    [
      "ATM uptime",
      "Route A",
      "Alert",
      "Below target",
      "High"
    ],
    [
      "Cash variance",
      "Branch 12",
      "Review",
      "Deposit mismatch",
      "High"
    ],
    [
      "Report feed",
      "Ops",
      "Clean",
      "On schedule",
      "Low"
    ],
    [
      "Device master",
      "Fleet",
      "Stale",
      "Missing owner",
      "Medium"
    ]
  ],
  "dataSays": [
    "Service exceptions explain more operational risk than cash volume alone when machines repeatedly miss uptime targets.",
    "Excel-heavy reporting creates avoidable delays where branch, route, and device identifiers are not standardized.",
    "The highest-value automation is a daily exception queue that tells operations which machines need action first."
  ],
  "recs": [
    "Standardize branch, route, and device identifiers before automating Tableau Prep flows.",
    "Create a daily exception report that ranks devices by downtime, cash variance, and service aging.",
    "Move weekly VLOOKUP reconciliation into SQL-backed validation checks with clear owner notes."
  ]
};
