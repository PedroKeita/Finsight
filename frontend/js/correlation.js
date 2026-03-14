function renderCorrelation(data) {
    const container = document.getElementById("correlation-matrix");
    if (!data || !data.tickers) {
        container.innerHTML = "<p style='color:#888'>Nenhum dado disponível</p>";
        return;
    }

    const { tickers, matrix } = data;

    // Linha de cabeçalho
    let html = `<div class="correlation-matrix">`;

    // Header row com tickers na vertical
    html += `<div class="corr-row">`;
    html += `<div class="corr-label"></div>`; // célula vazia no canto
    tickers.forEach(ticker => {
        html += `<div class="corr-header">${ticker.replace(".SA", "")}</div>`;
    });
    html += `</div>`;

    // Linhas da matriz
    matrix.forEach(row => {
        html += `<div class="corr-row">`;
        html += `<div class="corr-label">${row.ticker.replace(".SA", "")}</div>`;

        row.values.forEach(value => {
            const color = getCorrColor(value);
            const textColor = Math.abs(value) > 0.5 ? "#fff" : "#ccc";
            html += `
                <div class="corr-cell" 
                     style="background:${color}; color:${textColor}"
                     title="${value}">
                    ${value.toFixed(2)}
                </div>`;
        });

        html += `</div>`;
    });

    html += `</div>`;
    container.innerHTML = html;
}

function getCorrColor(value) {
    // Diagonal (1.0) = azul
    if (value === 1) return "#1A5276";

    // Correlação alta (> 0.7) = vermelho forte
    if (value >= 0.7)  return "#922B21";
    if (value >= 0.5)  return "#C0392B";
    if (value >= 0.3)  return "#E74C3C";

    // Correlação baixa (< 0.3) = verde
    if (value >= 0.1)  return "#1E8449";
    if (value >= 0)    return "#27AE60";

    // Correlação negativa = verde escuro
    return "#117A65";
}
