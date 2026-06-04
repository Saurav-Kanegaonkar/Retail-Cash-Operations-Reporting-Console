const data = window.dashboardData;
const node = (tag, className, html) => {
  const el = document.createElement(tag);
  if (className) el.className = className;
  if (html) el.innerHTML = html;
  return el;
};
document.querySelector("#metrics").replaceChildren(...data.cards.map((card) => node("article", "metric", `<small>${card[0]}</small><strong>${card[1]}</strong><small>${card[2]}</small>`)));
document.querySelector("#table").innerHTML = `<table><thead><tr><th>Signal</th><th>Owner</th><th>Status</th><th>Finding</th><th>Risk</th></tr></thead><tbody>${data.table.map((row) => `<tr><td>${row[0]}</td><td>${row[1]}</td><td>${row[2]}</td><td>${row[3]}</td><td class="${row[4]}">${row[4]}</td></tr>`).join("")}</tbody></table>`;
document.querySelector("#signals").replaceChildren(...data.dataSays.map((item) => node("div", "signal", item)));
document.querySelector("#recs").replaceChildren(node("div", "rec-grid", data.recs.map((item, index) => `<article class="rec"><b>${index + 1}. Recommendation</b>${item}</article>`).join("")));