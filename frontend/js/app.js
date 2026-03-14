let currentPeriod = "1y";
let currentTicker = null;
let assetsList = [];

document.addEventListener("DOMContentLoaded", () => {
    loadAssets();
    setupPeriodButtons();
    setupRefreshButton();
});

async function loadAssets() {
    try {
        assetsList = await fetchAssets();
        initAutocomplete(assetsList, (ticker) => {
            currentTicker = ticker;
            loadData(ticker);
        });
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

            if (currentTicker) loadData(currentTicker);
        });
    });
}

async function loadData(ticker) {
    if (!ticker) return;

    showLoading(true);

    try {
        const asset = assetsList.find(a => a.ticker === ticker);

        const [indicators, prices] = await Promise.all([
            fetchIndicators(ticker, currentPeriod),
            fetchPrices(ticker, currentPeriod),
        ]);

        renderCards(indicators, asset);
        renderChart(prices, ticker);

    } catch (err) {
        console.error("Erro ao carregar dados:", err);
    } finally {
        showLoading(false);
    }
}

function setupRefreshButton() {
    document.getElementById("refresh-btn").addEventListener("click", async () => {
        const btn = document.getElementById("refresh-btn");
        btn.disabled = true;
        btn.textContent = "Atualizando...";

        try {
            const result = await collectAll(currentPeriod);
            console.log("Atualização concluída:", result);
            if (currentTicker) loadData(currentTicker);
        } catch (err) {
            console.error("Erro ao atualizar:", err);
        } finally {
            btn.disabled = false;
            btn.textContent = "Atualizar dados";
        }
    });
}