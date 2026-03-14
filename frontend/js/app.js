let currentPeriod = "1y";
let currentTicker = null;
let assetsList = [];
let comparisonTickers = [];

const MAX_COMPARISON = 4;

document.addEventListener("DOMContentLoaded", () => {
    loadAssets();
    setupPeriodButtons();
    setupRefreshButton();
    setupComparisonControls();
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

async function loadData() {
    if (!currentTicker) return;

    showLoading(true);

    try {
        const tickersToLoad = comparisonTickers.length > 0
            ? [currentTicker, ...comparisonTickers.filter(t => t !== currentTicker)]
            : [currentTicker];

        const asset = assetsList.find(a => a.ticker === currentTicker);

        const [indicators, ...allPrices] = await Promise.all([
            fetchIndicators(currentTicker, currentPeriod),
            ...tickersToLoad.map(t => fetchPrices(t, currentPeriod))
        ]);

        // Monta o mapa { ticker: prices[] }
        const pricesMap = {};
        tickersToLoad.forEach((ticker, i) => {
            pricesMap[ticker] = allPrices[i];
        });

        renderCards(indicators, asset);
        renderChart(pricesMap, comparisonTickers.length > 0);

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
            if (currentTicker) loadData();

        } catch (err) {
            console.error("Erro ao atualizar:", err);
        } finally {
            btn.disabled = false;
            btn.textContent = "Atualizar dados";
        }
    });
}

function setupComparisonControls() {
    document.getElementById("compare-btn").addEventListener("click", () => {
        if (!currentTicker) return;
        if (comparisonTickers.includes(currentTicker)) return;
        if (comparisonTickers.length >= MAX_COMPARISON) return;

        comparisonTickers.push(currentTicker);
        updateComparisonBar();
        loadData();
    });

    document.getElementById("clear-comparison").addEventListener("click", () => {
        comparisonTickers = [];
        updateComparisonBar();
        loadData();
    });
}

function updateComparisonBar() {
    const bar   = document.getElementById("comparison-bar");
    const chips = document.getElementById("comparison-chips");

    if (comparisonTickers.length === 0) {
        bar.classList.add("hidden");
        return;
    }

    bar.classList.remove("hidden");
    chips.innerHTML = comparisonTickers.map(ticker => {
        const asset = assetsList.find(a => a.ticker === ticker);
        const logo  = asset?.logo_url
            ? `<img src="${asset.logo_url}" onerror="this.style.display='none'" />`
            : "";
        return `
            <div class="chip">
                ${logo}
                <span>${asset?.name || ticker} (${ticker})</span>
                <button class="chip-remove" data-ticker="${ticker}">✕</button>
            </div>
        `;
    }).join("");

    chips.querySelectorAll(".chip-remove").forEach(btn => {
        btn.addEventListener("click", () => {
            comparisonTickers = comparisonTickers.filter(t => t !== btn.dataset.ticker);
            updateComparisonBar();
            loadData();
        });
    });
}