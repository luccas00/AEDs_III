# CSI115 – 25.2 – Algoritmos e Estruturas de Dados III

## 👤 Discentes
- **Luccas Carneiro**

---

## 📄 Descrição Geral
Este projeto implementa e avalia **algoritmos clássicos de caminhos mínimos em grafos**, aplicados a mapas bidimensionais com diferentes dimensões e custos de terreno.

Foram implementados os algoritmos **Dijkstra**, **Dijkstra Otimizado**, **Bellman-Ford** e **Floyd-Warshall**, seguindo **fielmente os pseudocódigos apresentados em sala**, além de **módulos de benchmark** responsáveis por executar experimentos computacionais e coletar métricas de desempenho conforme a especificação do trabalho prático.

---

## 📌 Interpretação do Problema (Mapa → Grafo → Caminho Mínimo)

### Objetivo
Dado um mapa em formato `.txt`, com:
- `I` = início
- `F` = fim
- `#` = obstáculo (célula inválida)
- `W`, `S`, `G` = tipos de terreno com custo de movimentação

O programa deve calcular o **menor custo total** para ir de `I` até `F`, movendo-se apenas em **4 direções** (cima/baixo/esquerda/direita).

### Como o mapa vira grafo
O grid (matriz de caracteres) é convertido em um grafo ponderado dirigido, onde:

- Cada célula `(linha, coluna)` vira um vértice `v`.
- O índice do vértice é calculado por:
  - `v = linha * colunas + coluna`

Exemplo (mapa com `colunas = 10`):
- `(0,0) -> 0`
- `(0,1) -> 1`
- `(1,0) -> 10`
- `(1,1) -> 11`

### Arestas e pesos
Para cada célula válida (≠ `#`), o código cria arestas para seus vizinhos válidos (4-direções).
O peso da aresta `u -> v` é o custo **de entrar na célula de destino**.

Custos (conforme `Mapa.py`):
- `W = 5`
- `S = 3`
- `G = 1`
- `I` e `F = 0`

Isso significa que o algoritmo minimiza a soma dos custos das células visitadas (exceto início, que fica com custo 0 na prática).

### Como cada algoritmo é usado no projeto
- **Dijkstra** / **Bellman-Ford**: calculam menor caminho a partir de `I` para todos os vértices, e o programa utiliza `dist[F]`.
- **Floyd-Warshall**: calcula menor caminho entre **todos os pares (i, j)**, e o programa utiliza `dist[I][F]`.

O Floyd-Warshall faz mais trabalho do que o necessário para este problema (pois resolve all-pairs), mas é exigido para comparação de desempenho no relatório.

### Impacto do tamanho do mapa no desempenho
Se o mapa tem `L x C` células:
- `V = L*C` vértices
- `E ≈ 4V` arestas (em mapas sem muitos obstáculos)

Consequências:
- Dijkstra e Bellman-Ford tendem a rodar bem em mapas médios.
- Floyd-Warshall cresce com `V³`, ficando inviável em mapas grandes.

---

## 📌 Escopo

### Implementações Obrigatórias
- Modelagem de grafos direcionados e ponderados.
- Representação de grafos por:
  - **Lista de Adjacências**
  - **Matriz de Adjacências** (estrutura fornecida pelo professor).
- Implementação fiel dos algoritmos:
  - **Dijkstra**
  - **Bellman-Ford**
  - **Floyd-Warshall**
- Implementação adicional:
  - **Dijkstra Otimizado** (quebra antecipada para nós desconexos).
- Reconstrução do caminho mínimo a partir da estrutura de predecessores.
- Leitura de mapas em formato `.txt` contendo:
  - Terrenos com diferentes custos.
  - Ponto inicial (`I`) e ponto final (`F`).
- Geração de arquivos de saída com o caminho mínimo marcado.
- Impressão no terminal:
  - Custo do caminho mínimo.
  - Tempo de execução de cada algoritmo.

---

### Implementações de Experimentos Computacionais
- Execução de **10 rodadas por algoritmo e por mapa**.
- Cálculo da **média aritmética**:
  - Tempo de execução.
  - Custo do caminho mínimo.
- Comparação sistemática entre algoritmos.
- Benchmark com timeout (600s) quando habilitado.
- Registro automático de resultados no console **e em arquivo `log.txt`**.
- Saída formatada em **tabelas legíveis**, incluindo:
  - Tabelas por rodada (10 execuções)
  - Resumo por mapa
  - **Tabela 1 final consolidada** (uma linha por mapa)

---

## ⚙️ Tecnologias Utilizadas
- **Python 3**

---

## ✅ Funcionalidades Implementadas

### Grafos
- Estruturas:
  - `ListaAdjacencias`
  - `MatrizAdjacencias`
- Operações:
  - Inserção de arestas com peso.
  - Consulta de vizinhos.
  - Verificação de existência de arestas.

---

### Algoritmos de Caminhos Mínimos
- **Dijkstra**
  - Implementação didática, sem estruturas avançadas.
  - Calcula `dist[F]` a partir da origem `I`.
- **Dijkstra Otimizado**
  - Mesma lógica do pseudocódigo.
  - Adiciona quebra antecipada quando o menor valor em abertos é `INF` (nós desconexos).
- **Bellman-Ford**
  - Implementação fiel ao pseudocódigo.
  - Interrupção antecipada quando não há atualização.
- **Floyd-Warshall**
  - Cálculo de todos os pares de caminhos mínimos.
  - O projeto utiliza apenas `dist[I][F]` após o cálculo.

---

## 🗂️ Estrutura do Projeto (arquivos-chave)

- **Algoritmos de Caminho Mínimo**  
  `Algoritmos.py`
- **Estruturas de Grafo (fornecidas pelo professor)**  
  `Grafo.py`
- **Leitura de Mapas e Geração de Grafos**  
  `Mapa.py`

### Execuções
- **Execução simples (3 algoritmos)**  
  `main.py`
- **Execução simples V2 (4 algoritmos, inclui Dijkstra Otimizado)**  
  `main_v2.py`

### Benchmarks
- **Benchmark com timeout (600s) + log.txt + tabela por rodada + Tabela 1 final**  
  `main_benchmark.py`
- **Benchmark V2 sem timeout (inclui Dijkstra Otimizado) + log.txt + Tabela 1 final**  
  `main_benchmark_v2.py`

---

## 🧭 Fluxo de Execução
1. O programa lê um mapa `.txt`.
2. O mapa é convertido em um grafo ponderado:
   - Cada célula válida vira um vértice.
   - Movimentos 4-direções viram arestas.
   - O peso da aresta é o custo do terreno de destino.
3. O algoritmo calcula as distâncias mínimas.
4. O caminho é reconstruído via predecessores.
5. O mapa de saída é salvo com o caminho marcado (`*`).
6. Nos benchmarks:
   - Cada algoritmo é executado **10 vezes por mapa**.
   - O programa calcula **tempo médio** e **custo médio**.
   - O console imprime tabelas por rodada e resumo.
   - O mesmo conteúdo é gravado em `log.txt`.

---

## ▶️ Execução

### Execução Simples (3 algoritmos)
```
python main.py <arquivo_mapa.txt>
```

### Execução Simples V2 (inclui Dijkstra Otimizado)
```
python main_v2.py <arquivo_mapa.txt>
```

### Benchmark (com timeout 600s)
```
python main_benchmark.py <pasta_mapas>
```

### Benchmark V2 (sem timeout, inclui Dijkstra Otimizado)
```
python main_benchmark_v2.py <pasta_mapas>
```

Exemplo:
```
python main_benchmark.py mapas/
python main_benchmark_v2.py mapas/
```

---

## 📊 Saída Esperada

### Arquivos de saída do caminho
- `saida_dijkstra.txt`
- `saida_dijkstra_otimizado.txt` (apenas no V2)
- `saida_bellman_ford.txt`
- `saida_floyd_warshall.txt`

### Logs e Relatórios de Experimento
- `log.txt`  
  Contém exatamente o mesmo conteúdo impresso no terminal durante o benchmark.

---

## 📈 Análise Experimental
Os resultados permitem discutir:
- Qual algoritmo apresenta melhor desempenho e maior adequação ao problema.
- Diferenças entre a complexidade teórica e o comportamento observado.
- Impacto do tamanho e da estrutura do mapa nos tempos e custos.
- Limitações práticas do Floyd-Warshall em grafos grandes.

---

## 🎓 Disciplina
**CSI115 – 25.2 – Algoritmos e Estruturas de Dados III**
