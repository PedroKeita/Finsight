# Épicas e User Stories
O projeto é dividido em 5 épicas, cada uma representando uma camada do sistema.


# EP-01 - Infraestrutura e Banco de Dados
## Objetivo
ter o ambiente rodando e o banco modelado antes de escrever qualquer lógica de negócio

## User Stories

### US-01
"Como desenvolvedor, quero configurar o ambiente de desenvolvimento local para que todos os serviços rodem de forma isolada e reproduzível."

#### Critérios de Aceitação
- Python 3.11+ instalado com venv
- PostgreSQL rodando localmente
- Arquivo .env com credenciais funcionando
- requirements.txt com dependências fixadas
- .gitignore corretamente configurado

#### Task
- [X] Criar repositório no GitHub
- [X] Configurar venv e instalar dependências
- [X] Instalar e iniciar PostgreSQL
- [X] Criar arquivo .env com DATABASE_URL
- [X] Criar .gitignore padronizado para Python
- [X] Dar primeiro commit com o setup do projeto

### US-02
"Como desenvolvedor, quero modelar o banco de dados com as tabelas necessárias para armazenar ativos e histórico de preços."

#### Critérios de Aceitação
- Tabela assets criada com id, ticker, name e category
- Tabela prices criada com id, asset_id FK, date, close_price e volume
- Colcoar índice em prices(asset_id, date) para melhor performance
- Constraint UNIQUE em prices(asset_id, date)
- Script SQL versionado no repositório

#### Task
- [X] Criar arquivo schema.sql
- [X] Escrever DDL da tabela assets
- [X] Escrever DDL da tabela prices com FK
- [X] Criar indices e constraints
- [X] Executar script e validar no banco

# EP-02 - Coleta e Ingestão de Dados
## Objetivo
Ter dados reais de ativos financeiros populando o banco de maneira confiável.

## User Stories

### US-03
"Como analista, quero cadastrar ativos financeiros no sistema para que seus dados históricos possam ser coletados."
#### Critérios de Aceitação
- Função de inserção em assets sem duplicar tickers.
- Suporte a categorias: ação, índice, fundo
- Pelo menos 5 ativos cadastrados para teste
- Validação de ticker antes de inserir
#### Task
- [X] Criar database.py com conexão SQLAlchemy
- [ ] Criar função insert_asset(ticker, name, category)
- [ ] Adicionar validação de ticker duplicado
- [ ] Criar seed.py com 5 ativos iniciais (PETR4, VALE3, BVSP, ITUB4, BBAS3)
- [ ] Testar inserção e verificar no banco

### US-04
"Como analista, quero que o sistema colete automaticamente o histórico de preços de um ativo via API external."
#### Critérios de Aceitação
- yfinance retorna dados para todos os tickers cadastrados
- Preços salvos com date, close_price e volume
- Coleta não duplica registros
- Erros de coleta são logados sem quebrar o processo
- Histórico mínimo de 1 ano disponível
#### Task
- [ ] Criar collector.py com função fetch_prices(ticker, period)
- [ ] Integrar yfinance e converter para DataFrame pandas
- [ ] Criar função save_prices() com upsert no PostgreSQL
- [ ] Adicionar try/except com logging de erros
- [ ] Testar coleta para todos os ativos do seed
- [ ] Validar dados no banco via query SQL

# EP-03 - Cálculo de Indicadores Financeiros
## Objetivo:
Transformar os dados brutos em indicadores que medem risco e performance de cada ativo.

## User Stories

### US-05
"Como analista, quero cadastrar ativos financeiros no sistema para que seus dados históricos possam ser coletados."
#### Critérios de Aceitação
- Retorno acumulado calculado corretamente para qualquer período
- Volatilidade anualizada usando raiz de 252 dias úteis
- Função aceita ticker e período como parâmetros
- Resultado retornado em % com 2 casas decimais
#### Task
- [ ] Criar indicators.py
- [ ] Buscar série de preços do PostgreSQL via SQL
- [ ] Calcular retornos diários com pandas 
- [ ] Calcular retorno acumulado 
- [ ] Calcular volatilidade
- [ ] Testar com dados reais e validar resultado

### US-06
"Como analista, quero ver o Drawdown máximo e o Sharpe Ratio do ativo para avaliar seu reisco austero."
#### Critérios de Aceitação
- Drawdown máximo calculado como maior queda do pico ao vale
- Sharpe Ratio usando taxa livre de risco do CDI
- Sharpe retornado com 2 casas decimais
- Drawdown retornado em % negativa
- Todos os 4 indicadores retornados em uma única chamada
#### Task
- [ ] Implementar cálculo de drawdown
- [ ] Buscar taxa CDI de variável de ambiente
- [ ] Implementar Sharpe
- [ ] Criar função get_indicators unificada
- [ ] Escrever comentários que explique cada fórmula no código para melhor legibildiade
- [ ] Testar todos os 4 indicadores para 3 ativos diferentes


# EP-04 - API REST
## Objetivo
Expor os dados e indicadores via endpoints HTTP para que o frontend e qualquer cliente consuma.

## User Stories

### US-07
"Como desenvolvedor frontend, quero uma API que liste os ativos cadastrados e retorne seu histórico de preços."

#### Critérios de Aceitação
- GET /assets retorna lista completa com id, ticker, name, category
- GET /prices/{ticker} retorna array de {date, close_price}
- GET /prices/{ticker} aceita parâmetro ?period=1y,6m,3m
- API retorna 404 com mensagem clara para ticker inválido
- Swagger disponível em /docs

#### Task
- [ ] Criar main.py com instância FastAPI
- [ ] Criar endpoint GET /assets
- [ ] Criar endpoint GET /prices/{ticker} com query param period
- [ ] Adicionar tratamento de erro 404
- [ ] Testar no Swagger

### US-08
"Como analista, quero um endpoint que retorne todos os indicadores de um ativo de uma só vez."

#### Critérios de Aceitação
- GET /indicators/{ticker} retorna retorno, volatilidade, drawdown e sharpe
- Aceita parâmetro ?period=1y como padrão ou 6m, 3m
- Tempo de resposta abaixo de 2 segundos
- POST /collect/{ticker} dispara coleta e retorna status
- Todos os endpoints documentados no Swagger

#### Task
- [ ] Criar endpoint GET /indicators/{ticker}
- [ ] integrar com indicators.py
- [ ] Criar endpoint POST /collect/{ticker}
- [ ] Adicionar CORS para permitir chamadas no frontend
- [ ] Testar todos os endpoints via Swagger
- [ ] Documentar endpoints no README
# EP-05 - Dashboard Web
## Objetivo
Interface limpa e funcional que transforma os dados da API em informação visual de fácil leitura

## User Stories

### US-09
"Como usuário, quero selecionar um ativo e ver seus 4 indicadores exibidos em cards visuais de forma clara."

#### Critérios de Aceitação
- Dropdown carrega lista de ativos da API automaticamente
- 4 cards exibem Retorno, Volatilidade, Drawdown e Sharpe
- Drawdown aparece em vermelho, já o Retorno positivo em verde
- Cards atualizam ao trocar o ativo no dropdown
- Loading indicator aparece durante chamada da API

#### Task
- [ ] Criar index.html com estrutura base
- [ ] Criar style.css com layout de cards em grid
- [ ] Criar app.js com fetch() para GET /assets
- [ ] Popular dropdown dinamicamente
- [ ] Implementar fetch para GET /indicators/{ticker}
- [ ] Renderizar os 4 cards com formatação condicional de cores

### US-10
"Como usuário, quero ver um gráfico de linha com o histórico de preços do ativo selecionado no período escolhido."

#### Critérios de Aceitação
- Gráfico de linha renderizado com Chart.js
- Botões de período: 3M, 6M e 1A
- Gráfico atualizado ao trocar ativo ou período
- Eixo Y com valores em R$, eixo X com datas formatadas
- Tooltip exibe data e preço ao passar o mouse
- Página responsiva em telas menores

#### Task
- [ ] Incluir Chart.js via CDN
- [ ] Criar canvas para o gráfico
- [ ] Implementar fetch para GET /prices/{ticker}?period=X
- [ ] Renderizar LineChart com dados da API
- [ ] Criar botões de período e lógica de troca
- [ ] Ajustar CSS para responsividade básica
- [ ] Testar no browser com dados reais