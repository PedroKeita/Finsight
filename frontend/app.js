const API = "http://127.0.0.1:8000"
let chart = null
let currentPeriod = "1y";

// Inicializar
document.addEventListener("DOMContentLoaded", () => {
    loadAssets();
    setupPeriodButtons();
});

// Ativos
async function loadAssets() {
    const select = document.getElementById("asset-select");

    try {
        const res = await fetch(`${API}/assets`);
        const assets = await res.json()

        select.innerHTML = assets
            .map(a => `<option value="${a.ticker}">${a.name} (${a.ticker})</option>`)
            .join("");
        

        select.addEventListener("change", (e) => loadData(e.target.value));
        loadData(select.value);    
        
    } catch (err) {
        select.innerHTML = `<option>Erro ao carregar ativos</option>`;
        console.error(err);
    }
}

// Período
function setupPeriodButtons() {
    document.querySelectorAll(".period-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            document.querySelectorAll(".period-btn").forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            currentPeriod = btn.dataset.period;

            const ticker = document.getElementById("asset-select").value;
            if (ticker) loadData(ticker);
        });
    });
}

// Loading Data
async function loadData(ticker) {
    if (!ticker) return;

    showLoading(true);

    try {
        const [indicators, prices] = await Promise.all([
            fetch(`${API}/indicators/${ticker}?period=${currentPeriod}`).then(r => r.json()),
            fetch(`${API}/prices/${ticker}?period=${currentPeriod}`).then(r => r.json()),
        ]);

        renderCards(indicators);
        renderChart(prices, ticker);

    } catch (err) {
        console.error("Erro ao carregar dados:", err);
    } finally {
        showLoading(false);
    }
}

// Cards
function renderCards(indicators) {
    setCard("val-return", indicators.return, "%");
    setCard("val-volatility", indicators.volatility, "%");
    setCard("val-drawdown", indicators.drawdown, "%");
    setCard("val-sharpe", indicators.sharpe, "");
}

function setCard(id, value, suffix) {
    const el =  document.getElementById(id);
    el.textContent = `${value}${suffix}`;
    el.className = "card-value";

    if (value > 0) el.classList.add("positive");
    if (value < 0) el.classList.add("negative");
}

// Gráfico
function renderChart(prices, ticker) {
    const labels = prices.map(p => p.date);
    const values = prices.map(p => parseFloat(p.close_price));

    if (chart) chart.destroy();

    const ctx = document.getElementById("price-chart").getContext("2d");

  chart = new Chart(ctx, {
    type: "line",
    data: {
      labels,
      datasets: [{
        label: `${ticker} — Preço de Fechamento`,
        data: values,
        borderColor: "#4fc3f7",
        backgroundColor: "rgba(79, 195, 247, 0.05)",
        borderWidth: 2,
        pointRadius: 0,
        fill: true,
        tension: 0.3,
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { labels: { color: "#888" } },
        tooltip: {
          callbacks: {
            label: ctx => `R$ ${ctx.parsed.y.toFixed(2)}`
          }
        }
      },
      scales: {
        x: {
          ticks: { color: "#888", maxTicksLimit: 8 },
          grid: { color: "#1e2130" }
        },
        y: {
          ticks: {
            color: "#888",
            callback: val => `R$ ${val.toFixed(2)}`
          },
          grid: { color: "#2e3250" }
        }
      }
    }
  });
}

// Loading
function showLoading(show) {
    document.getElementById("loading").classList.toggle("hidden", !show);
}