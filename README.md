# 📈 FinSight
O FinSight é um sistema end-to-end de análise de carteiras de investimentos. Ele coleta dados reais de ativos financeiros, armazena em banco de dados relacional, calcula indicadores de performance e os exibe em um dashboard web interativo, cobrindo todo o fluxo de dados que analistas de fundos operam no dia a dia.

## Problema que resolve
- Analistas perdem tempo consolidando manualmente dados de múltiplas fontes
- Indicadores financeiros (Sharpe, drawdown, volatilidade) são calculados de forma descentralizada e sem histórico
- Não há uma visão unificada e automatizada da performance de uma carteira

## Proposta de valor
- Pipeline automatizado de coleta -> armazenanto -> cálculo -> visualização
- Indicadores financeiros calculados com SQL + Python sobre dados históricos reais
- Dashboard web acessível, sem necessidade de ferramentas pagas ou complexas

## Preview
![FinSight Dashboard](docs/finsight_screenshot.png)
---

## STACK 


| Camada          | Tecnologia        | Justificativa                                                                               |
| --------------- | ----------------- | ------------------------------------------------------------------------------------------- |
| Coleta de Dados | Python + yfinance | Acesso gratuito a dados reais de ativos brasileiros (B3) e internacionais via Yahoo Finance |
| Manipulação     | pandas + NumPy    | Padrão da indústria financeira para transformação e análise de séries temporais             |
| Banco de Dados  | PostgreSQL        | Banco relacional robusto, mais usado em ambientes corporativos financeiros que MySQL        |
| Backend / API   | Python + FastAPI  | Framework moderno, leve e com documentação automática via Swagger. Ideal para APIs de dados |
| Frontend        | HTML + CSS + JS   | Sem frameworks, para evitar complexidade desnecessária                                      |
| Gráficos        | Chart.js          | Biblioteca JS leve e popular para dashboards financeiros interativos                        |
| Versionamento   | Git + GitHub      | Controle de versão com histórico claro de commits para demonstrar evolução do projeto       |


---

## Como rodar localmente

### Pré-requisitos
- Python 3.11+
- PostgreSQL 17

### 1. Clone o repositório
```bash
git clone https://github.com/PedroKeita/Finsight.git
cd finsight
```
### 2. Crie e ative o ambiente virtual
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### 3. Instale as dependências
```bash
python -m pip install -r requirements.txt
```

### 4. Configure o banco de dados
```bash
psql -U postgres -d finsight -f schema.sql
```

### 5. Configure o arquivo .env
```
DATABASE_URL=postgresql://finsight_user:suasenha@localhost:5432/finsight
RISK_FREE_RATE=0.13
```

### 6. Popule os ativos iniciais
```bash
cd backend
python seed.py
```

### 7. Colete os dados históricos
```bash
python collector.py
```

### 8. Suba a API
```bash
uvicorn main:app --reload
```

Acesse a documentação em: **http://127.0.0.1:8000/docs**

---

## Endpoints

### GET /assets
Lista todos os ativos cadastrados no sistema.

**Resposta:**
```json
[
  {"id": 1, "ticker": "PETR4.SA", "name": "Petrobras", "category": "ação"},
  {"id": 2, "ticker": "VALE3.SA", "name": "Vale", "category": "ação"}
]
```

---

### GET /prices/{ticker}
Retorna o histórico de preços de um ativo.

**Parâmetros:**
| Parâmetro | Tipo | Padrão | Descrição |
|---|---|---|---|
| ticker | path | — | Código do ativo (ex: PETR4.SA) |
| period | query | 1y | Período: `1y`, `6m`, `3m` |

**Exemplo:** `GET /prices/PETR4.SA?period=6m`

**Resposta:**
```json
[
  {"date": "2025-03-13", "close_price": 36.50},
  {"date": "2025-03-14", "close_price": 37.20}
]
```

---

### GET /indicators/{ticker}
Retorna os 4 indicadores financeiros de um ativo calculados sobre os dados históricos.

**Parâmetros:**
| Parâmetro | Tipo | Padrão | Descrição |
|---|---|---|---|
| ticker | path | — | Código do ativo (ex: PETR4.SA) |
| period | query | 1y | Período: `1y`, `6m`, `3m` |

**Exemplo:** `GET /indicators/PETR4.SA?period=1y`

**Resposta:**
```json
{
  "return": 37.57,
  "volatility": 24.46,
  "drawdown": -19.32,
  "sharpe": 0.99
}
```

**Indicadores:**
- **return** — retorno acumulado do período em %
- **volatility** — volatilidade anualizada em % (desvio padrão × √252)
- **drawdown** — maior queda do pico ao vale em %
- **sharpe** — retorno ajustado ao risco (retorno excessivo / volatilidade)

---

### POST /collect/{ticker}
Dispara a coleta de dados históricos de um ativo no Yahoo Finance e salva no banco.

**Parâmetros:**
| Parâmetro | Tipo | Padrão | Descrição |
|---|---|---|---|
| ticker | path | — | Código do ativo (ex: PETR4.SA) |
| period | query | 1y | Período: `1y`, `6m`, `3m` |

**Exemplo:** `POST /collect/PETR4.SA`

**Resposta:**
```json
{"status": "ok", "message": "Dados de PETR4.SA coletados com sucesso"}
```

---

## Indicadores Financeiros

| Indicador | Fórmula | O que mede |
|---|---|---|
| Retorno Acumulado | (Preço final / Preço inicial) - 1 | Quanto o ativo valorizou no período |
| Volatilidade | Desvio padrão dos retornos diários × √252 | Risco do ativo, indica quanto o preço oscila |
| Drawdown Máximo | Maior queda do pico ao vale | Pior momento do ativo no período |
| Sharpe Ratio | (Retorno - CDI) / Volatilidade | Qualidade do retorno ajustado ao risco |

## Planejamento do Projeto

O FinSight foi planejado seguindo metodologia ágil, com épicas, histórias de usuário, critérios de aceitação e tasks técnicas definidas antes do desenvolvimento.

| Épica | Descrição | Status |
|---|---|---|
| EP-01 — Infraestrutura | Ambiente, PostgreSQL e modelagem do banco | ✅ Concluída |
| EP-02 — Coleta de Dados | Pipeline yfinance → PostgreSQL | ✅ Concluída |
| EP-03 — Indicadores | Retorno, Volatilidade, Drawdown, Sharpe | ✅ Concluída |
| EP-04 — API REST | Endpoints FastAPI com documentação Swagger | ✅ Concluída |
| EP-05 — Dashboard | Interface web com gráficos interativos | ✅ Concluída |
| EP-06 — Melhorias | Refatoração por módulos e atualização automática | ✅ Concluída |
| EP-07 — Expansão de Ativos | Mais tickers, logos e identidade visual | ✅ Concluída |
| EP-08 — Autocomplete | Campo de busca inteligente | ✅ Concluída |
| EP-09 — Comparação | Gráfico comparativo normalizado | ✅ Concluída |
| EP-10 — Qualidade Técnica | Testes, cache, agendamento e configuração | 🚧  Em Andamento |
| EP-11 — Documentação | Badges, diagrama e GIF animado | 🔜 Planejado |
| EP-12 — Funcionalidades Financeiras | Correlação, simulador e alertas | 🔜 Planejado |
| EP-13 — Visual e UX | Tema claro/escuro, pizza e animações | 🔜 Planejado |

> O planejamento completo com histórias de usuário e critérios de aceitação está disponível em [`Documentação Épicas e User Stories`](docs/Epics_UserStories.md) 

