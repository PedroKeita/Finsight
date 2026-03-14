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
- [X] Criar função insert_asset(ticker, name, category)
- [X] Adicionar validação de ticker duplicado
- [X] Criar seed.py com 5 ativos iniciais (PETR4, VALE3, BVSP, ITUB4, BBAS3)
- [X] Testar inserção e verificar no banco

### US-04
"Como analista, quero que o sistema colete automaticamente o histórico de preços de um ativo via API external."
#### Critérios de Aceitação
- yfinance retorna dados para todos os tickers cadastrados
- Preços salvos com date, close_price e volume
- Coleta não duplica registros
- Erros de coleta são logados sem quebrar o processo
- Histórico mínimo de 1 ano disponível
#### Task
- [X] Criar collector.py com função fetch_prices(ticker, period)
- [X] Integrar yfinance e converter para DataFrame pandas
- [X] Criar função save_prices() com upsert no PostgreSQL
- [X] Adicionar try/except com logging de erros
- [X] Testar coleta para todos os ativos do seed
- [X] Validar dados no banco via query SQL

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
- [X] Criar indicators.py
- [] Buscar série de preços do PostgreSQL via SQL
- [X] Calcular retornos diários com pandas 
- [X] Calcular retorno acumulado 
- [X] Calcular volatilidade
- [X] Testar com dados reais e validar resultado

### US-06
"Como analista, quero ver o Drawdown máximo e o Sharpe Ratio do ativo para avaliar seu reisco austero."
#### Critérios de Aceitação
- Drawdown máximo calculado como maior queda do pico ao vale
- Sharpe Ratio usando taxa livre de risco do CDI
- Sharpe retornado com 2 casas decimais
- Drawdown retornado em % negativa
- Todos os 4 indicadores retornados em uma única chamada
#### Task
- [X] Implementar cálculo de drawdown
- [X] Buscar taxa CDI de variável de ambiente
- [X] Implementar Sharpe
- [X] Criar função get_indicators unificada
- [X] Escrever comentários que explique cada fórmula no código para melhor legibildiade
- [X] Testar todos os 4 indicadores para 3 ativos diferentes


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
- [X] Criar main.py com instância FastAPI
- [X] Criar endpoint GET /assets
- [X] Criar endpoint GET /prices/{ticker} com query param period
- [X] Adicionar tratamento de erro 404
- [X] Testar no Swagger

### US-08
"Como analista, quero um endpoint que retorne todos os indicadores de um ativo de uma só vez."

#### Critérios de Aceitação
- GET /indicators/{ticker} retorna retorno, volatilidade, drawdown e sharpe
- Aceita parâmetro ?period=1y como padrão ou 6m, 3m
- Tempo de resposta abaixo de 2 segundos
- POST /collect/{ticker} dispara coleta e retorna status
- Todos os endpoints documentados no Swagger

#### Task
- [X] Criar endpoint GET /indicators/{ticker}
- [X] integrar com indicators.py
- [X] Criar endpoint POST /collect/{ticker}
- [X] Adicionar CORS para permitir chamadas no frontend
- [X] Testar todos os endpoints via Swagger
- [X] Documentar endpoints no README
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
- [X] Criar index.html com estrutura base
- [X] Criar style.css com layout de cards em grid
- [X] Criar app.js com fetch() para GET /assets
- [X] Popular dropdown dinamicamente
- [X] Implementar fetch para GET /indicators/{ticker}
- [X] Renderizar os 4 cards com formatação condicional de cores

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
- [X] Incluir Chart.js via CDN
- [X] Criar canvas para o gráfico
- [X] Implementar fetch para GET /prices/{ticker}?period=X
- [X] Renderizar LineChart com dados da API
- [X] Criar botões de período e lógica de troca
- [X] Ajustar CSS para responsividade básica
- [X] Testar no browser com dados reais

# EP-06 - Melhorias e Evolução do Sistema
## Objetivo
Evoluir o sistema com funcionalidades que aumentam a qualidade técnica e a experiência do usuário.

## User Stories

### US-11
"Como desenvolvedor, quero separar o código em módulos com responsabilidades únicas para facilitar manutenção e evolução."

#### Critérios de Aceitação
- Frontend separado em api.js, chart.js, ui.js e app.js
- Backend separado em routers individuais por domínio
- main.py apenas orquestra os routers
- Nenhuma função acessa o DOM e a API no mesmo arquivo

#### Task
- [X] Criar pasta frontend/js com módulos separados
- [X] Criar pasta backend/routers com routers por domínio
- [X] Refatorar main.py para usar include_router
- [X] Validar que todos os endpoints continuam funcionando

### US-12
"Como analista, quero atualizar os dados de todos os ativos com um clique para garantir que as informações estejam sempre frescos."

#### Critérios de Aceitação
- Botão "Atualizar dados" visível no dashboard
- Botão fica desabilitado durante a atualização
- Endpoint POST /collect/all atualiza todos os ativos cadastrados
- Após atualização, dashboard recarrega os dados automaticamente
- Resultado da coleta retorna status por ativo

#### Task
- [X] Criar endpoint POST /collect/all no backend
- [X] Corrigir ordem das rotas para /all não conflitar com /{ticker}
- [X] Adicionar botão de atualização no index.html
- [X] Estilizar botão no style.css
- [X] Implementar setupRefreshButton() no app.js
- [X] Adicionar collectAll() no api.js

# EP-07 - Expansão de Ativos e Identidade Visual
## Objetivo
Ampliar a base de ativos monitorados e enriquecer a interface com identidade visual de cada empresa.

## User Stories

### US-13
"Como analista, quero ver mais ativos disponíveis no dashboard para ter uma visão mais ampla do mercado."

#### Critérios de Aceitação
- Pelo menos 20 ativos cadastrados cobrindo ações, índices e FIIs
- Ativos organizados por categoria
- Novos ativos coletados e com histórico de 1 ano disponível
- seed.py atualizado com os novos ativos

#### Task
- [X] Adicionar coluna logo_url na tabela assets via migration SQL
- [X] Atualizar models.py com o novo campo
- [X] Atualizar seed.py com 20+ ativos e suas logo_urls
- [X] Executar seed e coletar dados dos novos ativos
- [X] Validar no banco que todos têm histórico

### US-14
"Como usuário, quero ver o ícone de cada empresa no dashboard para identificar os ativos visualmente com mais facilidade."

#### Critérios de Aceitação
- Logo aparece no dropdown ao lado do nome do ativo
- Logo aparece no card de indicadores do ativo selecionado
- Fallback visual quando logo não estiver disponível
- Logos carregadas via URL salva no banco

#### Task
- [X] Atualizar GET /assets para retornar logo_url
- [X] Renderizar logo no dropdown em ui.js
- [X] Renderizar logo no header dos cards
- [X] Adicionar CSS para logo circular e fallback

---

# EP-08 - Busca com Autocomplete
## Objetivo
Substituir o dropdown simples por um campo de busca inteligente que escala para muitos ativos.

## User Stories

### US-15
"Como usuário, quero digitar o nome ou ticker de um ativo para encontrá-lo rapidamente sem precisar rolar uma lista longa."

#### Critérios de Aceitação
- Campo de busca filtra por ticker e por nome simultaneamente
- Resultados aparecem em tempo real enquanto o usuário digita
- Mínimo de 1 caractere para exibir resultados
- Teclado navegável (setas + Enter para selecionar)
- Campo limpa ao selecionar um ativo

#### Task
- [X] Remover select do index.html
- [X] Criar componente de autocomplete em ui.js
- [X] Implementar lógica de filtro em app.js
- [X] Estilizar dropdown de resultados no style.css
- [X] Testar navegação por teclado

---

# EP-09 - Comparação de Ativos
## Objetivo
Permitir comparar a performance de múltiplos ativos no mesmo gráfico de forma visual e justa.

## User Stories

### US-16
"Como analista, quero adicionar múltiplos ativos ao gráfico para comparar suas performances no mesmo período."

#### Critérios de Aceitação
- Usuário pode adicionar até 5 ativos para comparação
- Cada ativo tem uma cor diferente no gráfico
- Botão para remover ativo da comparação
- Lista de ativos selecionados visível na interface

#### Task
- [X] Criar estado de ativos selecionados em app.js
- [X] Adicionar botão "Comparar" ao selecionar ativo
- [X] Renderizar chips dos ativos selecionados com botão de remover
- [X] Atualizar renderChart para suportar múltiplos datasets
- [X] Definir paleta de cores para cada ativo

### US-17
"Como analista, quero que o gráfico comparativo use retorno normalizado para comparar ativos com preços muito diferentes de forma justa."

#### Critérios de Aceitação
- Eixo Y mostra retorno em % em vez de preço absoluto em R$
- Base 0% no primeiro dia do período para todos os ativos
- Tooltip mostra retorno acumulado no ponto selecionado
- Legenda identifica cada ativo pela cor

#### Task
- [X] Implementar normalização dos preços em chart.js
- [X] Atualizar eixo Y para exibir %
- [X] Atualizar tooltip para mostrar retorno acumulado
- [X] Testar com ativos de escalas muito diferentes (ex: PETR4 vs Ibovespa)

# EP-10 - Qualidade Técnica
## Objetivo
Garantir confiabilidade, performance e boas práticas de engenharia no projeto.

## User Stories

### US-18
"Como desenvolvedor, quero testes automatizados no backend para garantir que os cálculos financeiros estão corretos."

#### Critérios de Aceitação
- Testes cobrem todas as funções do indicators.py
- Testes cobrem os endpoints principais da API
- Todos os testes passam com pytest
- Cobertura mínima de 80% do backend

#### Task
- [X] Instalar pytest e pytest-cov
- [X] Criar pasta tests/ com __init__.py
- [X] Criar test_indicators.py com testes de retorno, volatilidade, drawdown e sharpe
- [X] Criar test_api.py com testes dos endpoints
- [X] Rodar pytest e validar cobertura

### US-19
"Como desenvolvedor, quero cache nas respostas da API para reduzir consultas repetidas ao banco de dados."

#### Critérios de Aceitação
- Respostas de /indicators e /prices são cacheadas por 5 minutos
- Cache é invalidado ao rodar /collect
- Tempo de resposta reduz significativamente na segunda chamada
- Cache implementado sem biblioteca externa

#### Task
- [X] Implementar cache em memória com dicionário Python
- [X] Aplicar cache nos endpoints /indicators e /prices
- [X] Invalidar cache no endpoint /collect
- [X] Testar diferença de tempo com e sem cache

### US-20
"Como analista, quero que os dados sejam coletados automaticamente todo dia sem precisar clicar no botão."

#### Critérios de Aceitação
- Coleta agendada para rodar todo dia às 18h (após fechamento do mercado)
- Agendamento configurável via variável de ambiente
- Logs indicam quando a coleta automática foi executada
- Sistema continua funcionando normalmente durante a coleta

#### Task
- [X] Instalar APScheduler
- [X] Criar scheduler.py com job de coleta diária
- [X] Configurar horário via variável de ambiente
- [X] Integrar scheduler com o startup do FastAPI
- [X] Testar agendamento com intervalo curto

### US-21
"Como desenvolvedor, quero que URLs e configurações sensíveis estejam em variáveis de ambiente para facilitar o deploy."

#### Critérios de Aceitação
- URL do frontend configurável via .env
- Porta da API configurável via .env
- .env.example com todas as variáveis documentadas
- Nenhuma URL hardcoded no código

#### Task
- [X] Adicionar FRONTEND_URL e API_PORT no .env
- [X] Atualizar CORS para usar FRONTEND_URL do .env
- [X] Criar .env.example com valores de exemplo
- [X] Atualizar README com as novas variáveis

---

# EP-11 - Documentação e Apresentação
## Objetivo
Tornar o projeto visualmente atrativo e fácil de entender para usuários.

## User Stories

### US-22
"Como visitante do repositório, quero ver badges no README para entender rapidamente as tecnologias usadas."

#### Critérios de Aceitação
- Badges de Python, FastAPI, PostgreSQL, Chart.js visíveis no topo
- Badge de status do projeto
- Badges clicáveis apontando para documentação oficial

#### Task
- [ ] Adicionar badges via shields.io no README
- [ ] Organizar badges em uma linha no topo do README

### US-23
"Como visitante do repositório, quero entender o fluxo do sistema sem precisar ler o código."

#### Critérios de Aceitação
- Seção "Como funciona" com diagrama do pipeline
- Diagrama mostra fluxo: Yahoo Finance → Python → PostgreSQL → API → Dashboard
- Linguagem acessível para não desenvolvedores

#### Task
- [X] Criar diagrama do pipeline em ASCII art ou Mermaid
- [X] Adicionar seção "Como funciona" no README
- [X] Revisar README completo para clareza

### US-24
"Como visitante do repositório, quero ver o dashboard em funcionamento sem precisar rodar o projeto."

#### Critérios de Aceitação
- GIF animado mostrando seleção de ativo, indicadores e comparação
- GIF no README logo abaixo do título
- Duração máxima de 15 segundos

#### Task
- [X] Gravar o dashboard em uso com ScreenToGif ou similar
- [X] Otimizar o GIF para tamanho razoável
- [X] Adicionar no README substituindo o screenshot estático

---

# EP-12 - Funcionalidades Financeiras Avançadas
## Objetivo
Adicionar análises financeiras mais sofisticadas que demonstrem domínio do domínio de investimentos.

## User Stories

### US-25
"Como analista, quero ver uma tabela de correlação entre os ativos para entender como eles se movem juntos."

#### Critérios de Aceitação
- Matriz de correlação exibe todos os ativos cadastrados
- Células coloridas: verde para correlação baixa, vermelho para alta
- Valores entre -1 e 1 com 2 casas decimais
- Endpoint GET /correlation retorna a matriz

#### Task
- [X] Criar endpoint GET /correlation no backend
- [X] Calcular matriz de correlação com pandas (.corr())
- [X] Criar seção de correlação no dashboard
- [X] Renderizar matriz com CSS grid e cores condicionais

### US-26
"Como analista, quero simular uma carteira definindo o percentual de cada ativo para ver o retorno consolidado."

#### Critérios de Aceitação
- Usuário define % para cada ativo (soma deve ser 100%)
- Sistema calcula retorno, volatilidade e sharpe da carteira
- Gráfico mostra evolução da carteira vs Ibovespa
- Endpoint POST /portfolio recebe alocações e retorna indicadores

#### Task
- [X] Criar endpoint POST /portfolio no backend
- [X] Calcular retorno ponderado da carteira
- [X] Criar interface de alocação no frontend
- [X] Renderizar gráfico comparativo carteira vs benchmark

### US-27
"Como analista, quero ser alertado visualmente quando um ativo tiver variação significativa no dia."

#### Critérios de Aceitação
- Cards destacados em amarelo quando variação diária > 3%
- Cards destacados em vermelho quando variação diária < -3%
- Variação diária exibida em cada card
- Limiar de alerta configurável

#### Task
- [X] Calcular variação diária no indicators.py
- [X] Retornar variação diária no endpoint /indicators
- [X] Aplicar estilo condicional nos cards baseado na variação
- [X] Adicionar CSS para estado de alerta

---

# EP-13 - Visual e UX
## Objetivo
Polir a interface com recursos visuais que melhoram a experiência de uso.

## User Stories

### US-28
"Como usuário, quero alternar entre tema claro e escuro para usar o dashboard em diferentes ambientes."

#### Critérios de Aceitação
- Toggle de tema visível no header
- Tema persiste ao recarregar a página (localStorage)
- Transição suave entre temas
- Todos os componentes adaptados para os dois temas

#### Task
- [ ] Definir variáveis CSS para cores de cada tema
- [ ] Criar toggle no header
- [ ] Implementar troca de tema via classe no body
- [ ] Salvar preferência no localStorage
- [ ] Testar todos os componentes nos dois temas

### US-29
"Como usuário, quero ver um gráfico de pizza com a distribuição dos ativos por categoria."

#### Critérios de Aceitação
- Gráfico de pizza mostra % de ações, FIIs e índices
- Atualiza ao adicionar ou remover ativos da comparação
- Tooltip mostra quantidade e % de cada categoria

#### Task
- [ ] Adicionar canvas para gráfico de pizza
- [ ] Implementar renderPieChart em chart.js
- [ ] Calcular distribuição por categoria em app.js
- [ ] Estilizar container do gráfico

### US-30
"Como usuário, quero ver animações nos cards ao carregar para ter uma experiência mais fluida."

#### Critérios de Aceitação
- Cards aparecem com fade-in ao carregar dados
- Valores nos cards animam de 0 até o valor final
- Animação dura no máximo 1 segundo
- Animação não bloqueia interação

#### Task
- [ ] Criar animação CSS de fade-in para os cards
- [ ] Implementar contador animado em ui.js
- [ ] Testar animações em diferentes velocidades de conexão