const API = "http://127.0.0.1:8000";

async function fetchAssets() {
    const res = await fetch(`${API}/assets`);
    return res.json();
}

async function fetchIndicators(ticker, period) {
    const res = await fetch(`${API}/indicators/${ticker}?period=${period}`);
    return res.json();
}

async function fetchPrices(ticker, period) {
    const res = await fetch(`${API}/prices/${ticker}?period=${period}`);
    return res.json();
}

async function collectAll(period) {
    const res = await fetch(`${API}/collect/all?period=${period}`, { method: "POST" });
    return res.json();
}

async function fetchCorrelation(period) {
    const res = await fetch(`${API}/correlation/?period=${period}`);
    return res.json();
}