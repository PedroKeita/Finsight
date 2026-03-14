let currentPeriod = "1y";

document.addEventListener("DOMContentLoaded", () => {
    loadAssets();
    setupPeriodButtons();
});

async function loadAssets() {
    try {
        const assets = await fetchAssets();
        populateSelect(assets);

        const select = document.getElementById("asset-select");
        select.addEventListener("change", (e) => loadData(e.target.value));
        loadData(select.value);

    } catch (err) {
        showError("Erro ao carregar ativos");
        console.error(err);
    }
}

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

async function loadData(ticker) {
    if (!ticker) return;

    showLoading(true);

    try {
        const [indicators, prices] = await Promise.all([
            fetchIndicators(ticker, currentPeriod),
            fetchPrices(ticker, currentPeriod),
        ]);

        renderCards(indicators);
        renderChart(prices, ticker);

    } catch (err) {
        console.error("Erro ao carregar dados:", err);
    } finally {
        showLoading(false);
    }
}