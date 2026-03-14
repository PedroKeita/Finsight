function populateSelect(assets) {
    const select = document.getElementById("asset-select");
    select.innerHTML = assets
        .map(a => `<option value="${a.ticker}">${a.name} (${a.ticker})</option>`)
        .join("");
}

function renderCards(indicators) {
    setCard("val-return",     indicators.return,     "%");
    setCard("val-volatility", indicators.volatility, "%");
    setCard("val-drawdown",   indicators.drawdown,   "%");
    setCard("val-sharpe",     indicators.sharpe,     "");
}

function setCard(id, value, suffix) {
    const el = document.getElementById(id);
    el.textContent = `${value}${suffix}`;
    el.className = "card-value";

    if (value > 0) el.classList.add("positive");
    if (value < 0) el.classList.add("negative");
}

function showLoading(show) {
    document.getElementById("loading").classList.toggle("hidden", !show);
}

function showError(message) {
    const select = document.getElementById("asset-select");
    select.innerHTML = `<option>${message}</option>`;
}