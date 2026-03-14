let onAssetSelect = null;

function initAutocomplete(assets, onSelect) {
    onAssetSelect = onSelect;

    const selected  = document.getElementById("autocomplete-selected");
    const input     = document.getElementById("search-input");
    const list      = document.getElementById("autocomplete-list");
    let activeIndex = -1;

    // Abre o campo de busca ao clicar
    selected.addEventListener("click", () => {
        selected.classList.add("hidden");
        input.classList.remove("hidden");
        input.focus();
        renderList(assets);
        list.classList.remove("hidden");
    });

    // Filtra enquanto digita
    input.addEventListener("input", () => {
        const query = input.value.toLowerCase();
        const filtered = assets.filter(a =>
            a.name.toLowerCase().includes(query) ||
            a.ticker.toLowerCase().includes(query)
        );
        activeIndex = -1;
        renderList(filtered);
    });

    // Navegação por teclado
    input.addEventListener("keydown", (e) => {
        const items = list.querySelectorAll("li");
        if (e.key === "ArrowDown") {
            activeIndex = Math.min(activeIndex + 1, items.length - 1);
            updateActive(items);
        } else if (e.key === "ArrowUp") {
            activeIndex = Math.max(activeIndex - 1, 0);
            updateActive(items);
        } else if (e.key === "Enter" && activeIndex >= 0) {
            items[activeIndex].click();
        } else if (e.key === "Escape") {
            closeDropdown();
        }
    });

    // Fecha ao clicar fora
    document.addEventListener("click", (e) => {
        if (!e.target.closest(".autocomplete-wrapper")) closeDropdown();
    });

    function renderList(filtered) {
        if (filtered.length === 0) {
            list.innerHTML = `<li style="color:#888; cursor:default">Nenhum ativo encontrado</li>`;
            return;
        }

        list.innerHTML = filtered.map((a, i) => `
            <li data-ticker="${a.ticker}" data-index="${i}">
                <img src="${a.logo_url || ''}" onerror="this.style.display='none'" />
                <span class="item-name">${a.name}</span>
                <span class="item-ticker">${a.ticker}</span>
                <span class="item-category">${a.category}</span>
            </li>
        `).join("");

        list.querySelectorAll("li").forEach(li => {
            li.addEventListener("click", () => {
                const ticker = li.dataset.ticker;
                const asset  = assets.find(a => a.ticker === ticker);
                selectAsset(asset);
            });
        });
    }

    function selectAsset(asset) {
        const logo = document.getElementById("selected-logo");
        const name = document.getElementById("selected-name");

        if (asset.logo_url) {
            logo.src = asset.logo_url;
            logo.classList.remove("hidden");
        } else {
            logo.classList.add("hidden");
        }

        name.textContent = `${asset.name} (${asset.ticker})`;
        closeDropdown();
        if (onAssetSelect) onAssetSelect(asset.ticker);
    }

    function updateActive(items) {
        items.forEach((item, i) => item.classList.toggle("active", i === activeIndex));
        if (items[activeIndex]) items[activeIndex].scrollIntoView({ block: "nearest" });
    }

    function closeDropdown() {
        input.value = "";
        input.classList.add("hidden");
        selected.classList.remove("hidden");
        list.classList.add("hidden");
        activeIndex = -1;
    }

    if (assets.length > 0) selectAsset(assets[0]);
}

function renderCards(indicators, asset) {
    const logo = asset?.logo_url
        ? `<img src="${asset.logo_url}" class="asset-logo" onerror="this.style.display='none'" />`
        : "";

    document.getElementById("asset-header").innerHTML = `${logo} ${asset?.name || ""}`;

    setCard("val-return",     indicators["return"],  "%");
    setCard("val-volatility", indicators.volatility, "%");
    setCard("val-drawdown",   indicators.drawdown,   "%");
    setCard("val-sharpe",     indicators.sharpe,     "");

    setDailyVariation(indicators.daily_variation);
}

function setCard(id, value, suffix) {
    const el = document.getElementById(id);
    el.textContent = `${value}${suffix}`;
    el.className = "card-value";

    if (value > 0) el.classList.add("positive");
    if (value < 0) el.classList.add("negative");
}

function setDailyVariation(value) {
    const el = document.getElementById("val-daily");
    if (!el) return;

    const sign = value >= 0 ? "+" : "";
    el.textContent = `${sign}${value}%`;
    el.className = "card-value " + (value >= 0 ? "positive" : "negative");

    // Alerta no card
    const card = document.getElementById("card-daily");
    card.classList.remove("alert-up", "alert-down");

    if (value >= 3)       card.classList.add("alert-up");
    else if (value <= -3) card.classList.add("alert-down");
}

function showLoading(show) {
    document.getElementById("loading").classList.toggle("hidden", !show);
}

function showError(message) {
    document.getElementById("selected-name").textContent = message;
}