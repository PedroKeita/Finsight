let chart = null;

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