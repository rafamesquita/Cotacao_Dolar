const API_URL = "/api/dolar";
const HISTORY_LIMIT = 7;
const CHART_LIMIT = 15;
let chartInstance = null;

function formatValue(value) {
  return `R$ ${parseFloat(value).toFixed(3)}`;
}

function formatDateTime(dateTime) {
  return dateTime ? dateTime.split(" ")[0] : "--";
}

function setError(message) {
  const errorState = document.getElementById("errorState");
  errorState.classList.remove("sr-only");
  errorState.innerText = message;
}

function clearError() {
  const errorState = document.getElementById("errorState");
  errorState.classList.add("sr-only");
  errorState.innerText = "";
}

function renderHero(last, prev) {
  const isUp = parseFloat(last.valor) > parseFloat(prev.valor);
  document.getElementById("currentVal").innerText = formatValue(last.valor);
  document.getElementById("lastUpdate").innerText = `Última sincronização: ${last.data_hora}`;
  const trendEl = document.getElementById("trend");
  trendEl.innerText = isUp ? "▲" : "▼";
  trendEl.className = `hero-trend ${isUp ? "up" : "down"}`;
}

function renderHistory(data) {
  const table = document.getElementById("historyTable");
  table.innerHTML = data.slice(-HISTORY_LIMIT).reverse().map((item) => `
    <div class="table-row">
      <span class="t-date">${formatDateTime(item.data_hora)}</span>
      <span class="t-val">${formatValue(item.valor)}</span>
    </div>
  `).join("");
}

function renderChart(data) {
  const ctx = document.getElementById("mainChart").getContext("2d");
  const lastPoints = data.slice(-CHART_LIMIT);
  if (chartInstance) chartInstance.destroy();
  chartInstance = new Chart(ctx, {
    type: "line",
    data: {
      labels: lastPoints.map((d) => formatDateTime(d.data_hora)),
      datasets: [{
        label: "Dólar",
        data: lastPoints.map((d) => parseFloat(d.valor)),
        borderColor: "#4ade80",
        backgroundColor: "rgba(74, 222, 128, 0.1)",
        fill: true,
        tension: 0.4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: { grid: { color: "#1e2230" }, ticks: { color: "#6b7280" } },
        x: { grid: { display: false }, ticks: { color: "#6b7280" } }
      }
    }
  });
}

async function fetchData() {
  try {
    const response = await fetch(API_URL);
    const data = await response.json();
    if (!Array.isArray(data) || data.length === 0) {
      setError("Nenhum dado de cotação disponível no momento.");
      return;
    }
    clearError();
    render(data);
  } catch (e) {
    console.error("Erro ao carregar dados:", e);
    setError("Não foi possível carregar a cotação agora.");
  }
}

function render(data) {
  const last = data[data.length - 1];
  const prev = data.length > 1 ? data[data.length - 2] : last;
  renderHero(last, prev);
  renderHistory(data);
  renderChart(data);
}

fetchData();
