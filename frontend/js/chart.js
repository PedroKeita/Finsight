let chart = null;

const COLORS = [
    "#4fc3f7",
    "#81c784",
    "#ffb74d",
    "#f06292",
    "#ce93d8",
    "#ff8a65",
]

function normalizeprices(prices) {
    if (prices.length === 0) return [];
    const base = parseFloat(prices[0].close_price);
    return prices.map(p => (((parseFloat(p.close_price) - base) / base) * 100 ).toFixed(2));
}

function renderChart(pricesMap, comparing = false) {
    if (chart) chart.destroy();

    const ctx = document.getElementById("price-chart").getContext("2d");

    const datasets = Object.entries(pricesMap).map(([ticker, prices], i) => {
        const values = comparing
            ? normalizeprices(prices)
            : prices.map(p => parseFloat(p.close_price));

        return {
            label: ticker,
            data: values,
            borderColor: COLORS[i % COLORS.length],
            backgroundColor: COLORS[i % COLORS.length],
            borderWidth: 2,
            pointRadius: 0,
            tension: 0.3,
            fill: false,
        };
    });

    // Usa as labels do primeiro ativo
    const firstTicker = Object.keys(pricesMap)[0];
    const labels = pricesMap[firstTicker].map(p => p.date);

    chart = new Chart(ctx, {
        type: "line",
        data: { labels, datasets },
        options: {
            responsive: true,
            plugins: {
                legend: { labels: { 
                    color: "#888",
                    usePointStyle: false,
                    boxWidth: 12,
                    boxHeight: 12, 
                } 
            },
                tooltip: {
                    callbacks: {
                        label: ctx => comparing
                            ? `${ctx.dataset.label}: ${ctx.parsed.y}%`
                            : `${ctx.dataset.label}: R$ ${ctx.parsed.y.toFixed(2)}`
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
                        callback: val => comparing
                            ? `${val}%`
                            : `R$ ${val.toFixed(2)}`
                    },
                    grid: { color: "#2e3250" }
                }
            }
        }
    });
}