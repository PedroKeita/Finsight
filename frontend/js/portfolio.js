let portfolioAssets = [];
let portfolioSelectedTicker = null;
let portfolioChart = null;
let portfolioPeriod = "1y";

function initPortfolio(assets) {
    initPortfolioAutocomplete(assets);
    setupPortfolioAddButton();
    setupPortfolioSimulateButton();
    setupPortfolioPeriodButtons();
}

function initPortfolioAutocomplete(assets) {
    const selected = document.getElementById("portfolio-selected");
    const input    = document.getElementById("portfolio-search");
    const list     = document.getElementById("portfolio-list");
    let activeIndex = -1;

    selected.addEventListener("click", () => {
        selected.classList.add("hidden");
        input.classList.remove("hidden");
        input.focus();
        renderPortfolioList(assets);
        list.classList.remove("hidden");
    });

    input.addEventListener("input", () => {
        const query = input.value.toLowerCase();
        const filtered = assets.filter(a =>
            a.name.toLowerCase().includes(query) ||
            a.ticker.toLowerCase().includes(query)
        );
        activeIndex = -1;
        renderPortfolioList(filtered);
    });

    input.addEventListener("keydown", (e) => {
        const items = list.querySelectorAll("li");
        if (e.key === "ArrowDown") {
            activeIndex = Math.min(activeIndex + 1, items.length - 1);
            items.forEach((item, i) => item.classList.toggle("active", i === activeIndex));
        } else if (e.key === "ArrowUp") {
            activeIndex = Math.max(activeIndex - 1, 0);
            items.forEach((item, i) => item.classList.toggle("active", i === activeIndex));
        } else if (e.key === "Enter" && activeIndex >= 0) {
            items[activeIndex].click();
        } else if (e.key === "Escape") {
            closePortfolioDropdown();
        }
    });

    document.addEventListener("click", (e) => {
        if (!e.target.closest("#portfolio-autocomplete-wrapper")) closePortfolioDropdown();
    });

    function renderPortfolioList(filtered) {
        list.innerHTML = filtered.map(a => `
            <li data-ticker="${a.ticker}">
                <img src="${a.logo_url || ''}" onerror="this.style.display='none'" />
                <span class="item-name">${a.name}</span>
                <span class="item-ticker">${a.ticker}</span>
            </li>
        `).join("");

        list.querySelectorAll("li").forEach(li => {
            li.addEventListener("click", () => {
                const ticker = li.dataset.ticker;
                const asset  = assets.find(a => a.ticker === ticker);
                portfolioSelectedTicker = ticker;

                const logo = document.getElementById("portfolio-logo");
                const name = document.getElementById("portfolio-name");

                if (asset.logo_url) {
                    logo.src = asset.logo_url;
                    logo.classList.remove("hidden");
                } else {
                    logo.classList.add("hidden");
                }

                name.textContent = `${asset.name} (${asset.ticker})`;
                closePortfolioDropdown();
            });
        });
    }

    function closePortfolioDropdown() {
        input.value = "";
        input.classList.add("hidden");
        selected.classList.remove("hidden");
        list.classList.add("hidden");
    }
}

function setupPortfolioAddButton() {
    document.getElementById("portfolio-add-btn").addEventListener("click", () => {
        const weightInput = document.getElementById("portfolio-weight");
        const weight = parseFloat(weightInput.value);

        if (!portfolioSelectedTicker) {
            alert("Selecione um ativo!");
            return;
        }
        if (!weight || weight <= 0 || weight > 100) {
            alert("Digite um peso válido entre 1 e 100!");
            return;
        }
        if (portfolioAssets.find(a => a.ticker === portfolioSelectedTicker)) {
            alert("Ativo já adicionado!");
            return;
        }

        portfolioAssets.push({
            ticker: portfolioSelectedTicker,
            weight: weight,
            name: document.getElementById("portfolio-name").textContent,
            logo: document.getElementById("portfolio-logo").src
        });

        weightInput.value = "";
        portfolioSelectedTicker = null;
        document.getElementById("portfolio-name").textContent = "Selecione um ativo...";
        document.getElementById("portfolio-logo").classList.add("hidden");

        renderPortfolioItems();
        updatePortfolioTotal();
    });
}

function renderPortfolioItems() {
    const container = document.getElementById("portfolio-items");
    container.innerHTML = portfolioAssets.map((a, i) => `
        <div class="portfolio-item">
            <img src="${a.logo}" onerror="this.style.display='none'" />
            <span class="portfolio-item-name">${a.name}</span>
            <span class="portfolio-item-weight">${a.weight}%</span>
            <button class="portfolio-item-remove" data-index="${i}">✕</button>
        </div>
    `).join("");

    container.querySelectorAll(".portfolio-item-remove").forEach(btn => {
        btn.addEventListener("click", () => {
            portfolioAssets.splice(parseInt(btn.dataset.index), 1);
            renderPortfolioItems();
            updatePortfolioTotal();
        });
    });
}

function updatePortfolioTotal() {
    const total = portfolioAssets.reduce((sum, a) => sum + a.weight, 0);
    const el    = document.getElementById("portfolio-total");
    const btn   = document.getElementById("portfolio-simulate-btn");

    el.textContent = `Total: ${total.toFixed(1)}%`;
    el.className   = "portfolio-total";

    if (total === 100) {
        el.classList.add("valid");
        btn.disabled = false;
    } else if (total > 100) {
        el.classList.add("invalid");
        btn.disabled = true;
    } else {
        btn.disabled = true;
    }
}

function setupPortfolioSimulateButton() {
    document.getElementById("portfolio-simulate-btn").addEventListener("click", async () => {
        const btn = document.getElementById("portfolio-simulate-btn");
        btn.disabled = true;
        btn.textContent = "Simulando...";

        try {
            const allocations = portfolioAssets.map(a => ({
                ticker: a.ticker,
                weight: a.weight / 100
            }));

            const result = await simulatePortfolio(allocations, portfolioPeriod);

            renderPortfolioResult(result);

        } catch (err) {
            console.error("Erro ao simular carteira:", err);
        } finally {
            btn.disabled = false;
            btn.textContent = "Simular Carteira";
        }
    });
}

function renderPortfolioResult(result) {
    document.getElementById("portfolio-result").classList.remove("hidden");

    const retEl = document.getElementById("port-return");
    retEl.textContent = `${result.return}%`;
    retEl.className = "card-value " + (result.return >= 0 ? "positive" : "negative");

    const volEl = document.getElementById("port-volatility");
    volEl.textContent = `${result.volatility}%`;
    volEl.className = "card-value";

    const shrEl = document.getElementById("port-sharpe");
    shrEl.textContent = result.sharpe;
    shrEl.className = "card-value " + (result.sharpe >= 1 ? "positive" : "");

    renderPortfolioChart(result.history);
}

function renderPortfolioChart(history) {
    const labels = history.map(h => h.date);
    const values = history.map(h => h.value);

    const finalValue = values[values.length - 1];
     console.log("Final value:", finalValue);
    console.log("Is positive:", finalValue >= 0);
    const isPositive = finalValue >= 0;

    const lineColor = isPositive ? "#81c784" : "#ef5350";
    const bgColor   = isPositive ? "rgba(129, 199, 132, 0.05)" : "rgba(239, 83, 80, 0.05)";

    if (portfolioChart) portfolioChart.destroy();

    const ctx = document.getElementById("portfolio-chart").getContext("2d");

    portfolioChart = new Chart(ctx, {
        type: "line",
        data: {
            labels,
            datasets: [{
                label: "Retorno da Carteira (%)",
                data: values,
                borderColor: lineColor,
                backgroundColor: bgColor,
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
                        label: ctx => `Retorno: ${ctx.parsed.y.toFixed(2)}%`
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
                        callback: val => `${val}%`
                    },
                    grid: { color: "#2e3250" }
                }
            }
        }
    });
}

function setupPortfolioPeriodButtons() {
    document.querySelectorAll(".portfolio-period-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            document.querySelectorAll(".portfolio-period-btn").forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            portfolioPeriod = btn.dataset.period;

            if (portfolioAssets.length > 0 && !document.getElementById("portfolio-result").classList.contains("hidden")) {
                document.getElementById("portfolio-simulate-btn").click();
            }
        });
    });
}