# Visão Geral
O FinSight é um sistema end-to-end de análise de carteiras de investimentos. Ele coleta dados reais de ativos financeiros, armazena em banco de dados relaciona, calcula indicadores de performance e os exibe em um dashboard web interativo, cobrindo todo o fluxo de dados que analistas de fundos operam no dia a dia.

## Problema que resolve
- Analistas perdem tempo consolidando manualmente dados de múltiplas fontes
- Indicadores financeiros (Sharpe, drawdown, volatilidade) são calculados de forma descentralizada e sem histórico
- Não há uma visão unificada e automatizada da performance de uma carteira

## Proposta de valor
- Pipeline automatizado de coleta -> armazenanto -> cálculo -> visualização
- Indicadores financeiros calculados com SQL + Python sobre dados históricos reais
- Dashboard web acessível, sem necessidade de ferramentas pagas ou complexas


## STACK 


| Camada          | Tecnologia        | Justificativa                                                                               |
| --------------- | ----------------- | ------------------------------------------------------------------------------------------- |
| Coleta de Dados | Python + yfinance | Acesso gratuito a dados reais de ativos brasileiros (B3) e internacionais via Yahoo Finance |
| Manipulação     | pandas + NumPy    | Padrão da indústria financeira para transformação e análise de séries temporais             |
| Banco de Dados  | PostgreSQL        | Bnaco relacional robusto, mais usado em ambientes corporativos financeiros que MySQL        |
| Backend / API   | Python + FastAPI  | Framework moderno, leve e com documentação automática via Swagger. Ideal para APIs de dados |
| Frontend        | HTML + CSS + JS   | Sem frameworks, para evitar complexidade desnecessária                                      |
| Gráficos        | Chart.js          | Biblioteca JS leve e popular para dashboards financeiros interativos                        |
| Versionamento   | Git + GitHub      | Controle de versão com histórico claro de commits para demonstrar evolução do projeto       |
