const data = window.dashboardData;
const view = document.querySelector("#view");

const node = (tag, className, html = "") => {
  const el = document.createElement(tag);
  if (className) el.className = className;
  el.innerHTML = html;
  return el;
};

const money = (value) =>
  Number(value).toLocaleString("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  });

const pctClass = (value) => {
  if (value >= 90) return "good";
  if (value >= 78) return "watch";
  return "bad";
};

const priorityClass = (value) => {
  if (value >= 76) return "bad";
  if (value >= 62) return "watch";
  return "good";
};

function renderMetrics() {
  document.querySelector("#metrics").replaceChildren(
    ...data.cards.map((card) =>
      node(
        "article",
        "metric",
        `<small>${card.label}</small><strong>${card.value}</strong><span>${card.detail}</span>`
      )
    )
  );
}

function barChart(rows, labelField, valueField, options = {}) {
  const max = Math.max(...rows.map((row) => Number(row[valueField])), 1);
  return rows
    .map((row) => {
      const value = Number(row[valueField]);
      const width = Math.max(4, (value / max) * 100);
      const label = row[labelField];
      const suffix = options.suffix || "";
      return `<div class="bar-row">
        <span>${label}</span>
        <div class="bar-track"><div class="bar-fill" style="width:${width}%"></div></div>
        <b>${value}${suffix}</b>
      </div>`;
    })
    .join("");
}

function renderExecutive() {
  const routeRows = [...data.executive.routeChart].sort((a, b) => b.priority - a.priority).slice(0, 8);
  const deviceRows = data.executive.deviceMix;
  view.replaceChildren(
    node(
      "section",
      "surface executive-grid",
      `<article class="panel span-2">
        <div class="section-head">
          <span>Surface 1</span>
          <h2>Executive report pulse</h2>
        </div>
        <div class="finding-list">
          ${data.executive.findings.map((item) => `<p>${item}</p>`).join("")}
        </div>
      </article>
      <article class="panel">
        <div class="section-head">
          <span>Route score</span>
          <h2>Priority by route</h2>
        </div>
        ${barChart(routeRows, "route", "priority")}
      </article>
      <article class="panel">
        <div class="section-head">
          <span>Portfolio</span>
          <h2>Device mix</h2>
        </div>
        ${barChart(deviceRows, "type", "count")}
      </article>`
    )
  );
}

function renderExceptions() {
  const rows = data.exceptions
    .map(
      (row) => `<tr>
        <td><b>${row.entity_name}</b><small>${row.entity_id} · ${row.route}</small></td>
        <td>${row.owner_team}</td>
        <td><span class="pill ${priorityClass(row.composite_priority)}">${row.composite_priority}</span></td>
        <td>${row.risk_driver}</td>
        <td>${money(row.fourteen_day_cash_variance)}</td>
        <td>${row.open_event_count}</td>
        <td>${row.next_step}</td>
      </tr>`
    )
    .join("");
  view.replaceChildren(
    node(
      "section",
      "surface",
      `<article class="panel">
        <div class="section-head">
          <span>Surface 2</span>
          <h2>Daily exception action queue</h2>
        </div>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Device</th>
                <th>Owner</th>
                <th>Priority</th>
                <th>Driver</th>
                <th>14 day variance</th>
                <th>Open events</th>
                <th>Next step</th>
              </tr>
            </thead>
            <tbody>${rows}</tbody>
          </table>
        </div>
      </article>`
    )
  );
}

function renderPrep() {
  const sourceRows = data.prep.sources
    .map(
      (row) => `<tr>
        <td><b>${row.source}</b><small>${row.rule}</small></td>
        <td>${row.checks}</td>
        <td>${Number(row.failedRecords).toLocaleString()}</td>
        <td><span class="pill ${row.status === "Certified" ? "good" : row.status === "Watch" ? "watch" : "bad"}">${row.status}</span></td>
      </tr>`
    )
    .join("");
  const reportCards = data.prep.reports
    .slice(0, 6)
    .map(
      (row) => `<article class="report-card">
        <span>${row.cadence}</span>
        <b>${row.report}</b>
        <small>${row.owner}</small>
        <div class="progress"><i style="width:${row.onTimeRate}%"></i></div>
        <em class="${pctClass(row.onTimeRate)}">${row.onTimeRate}% on time</em>
      </article>`
    )
    .join("");
  const requirementRows = data.prep.requirements
    .map(
      (row) => `<tr>
        <td>${row.stakeholder_group}</td>
        <td>${row.business_question}</td>
        <td>${row.required_metric}</td>
        <td>${row.acceptance_test}</td>
        <td>${row.status}</td>
      </tr>`
    )
    .join("");
  view.replaceChildren(
    node(
      "section",
      "surface prep-grid",
      `<article class="panel span-2">
        <div class="section-head">
          <span>Surface 3</span>
          <h2>Tableau Prep validation hub</h2>
        </div>
        <div class="table-wrap">
          <table>
            <thead>
              <tr><th>Source</th><th>Checks</th><th>Failed records</th><th>Status</th></tr>
            </thead>
            <tbody>${sourceRows}</tbody>
          </table>
        </div>
      </article>
      <article class="panel">
        <div class="section-head">
          <span>Distribution</span>
          <h2>Scheduled reports</h2>
        </div>
        <div class="report-grid">${reportCards}</div>
      </article>
      <article class="panel span-3">
        <div class="section-head">
          <span>Requirements</span>
          <h2>Stakeholder acceptance tests</h2>
        </div>
        <div class="table-wrap compact">
          <table>
            <thead>
              <tr><th>Group</th><th>Question</th><th>Metric</th><th>Acceptance test</th><th>Status</th></tr>
            </thead>
            <tbody>${requirementRows}</tbody>
          </table>
        </div>
      </article>`
    )
  );
}

const renderers = {
  executive: renderExecutive,
  exceptions: renderExceptions,
  prep: renderPrep,
};

document.querySelectorAll(".tabs button").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelectorAll(".tabs button").forEach((tab) => tab.classList.remove("active"));
    button.classList.add("active");
    renderers[button.dataset.view]();
  });
});

renderMetrics();
renderExecutive();
