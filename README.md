# CSI115 – 25.2 – Algoritmos e Estruturas de Dados III

## 👤 Discente
**Luccas Vinicius P. A. Santos Carneiro**

---

## 📄 Descrição Geral
Este projeto implementa e avalia **algoritmos clássicos de caminhos mínimos em grafos**, aplicados a mapas bidimensionais com diferentes dimensões e custos de terreno.

Foram implementados os algoritmos **Dijkstra**, **Bellman-Ford** e **Floyd-Warshall**, seguindo **fielmente os pseudocódigos apresentados em sala**, além de um **módulo de benchmark** responsável por executar experimentos computacionais e coletar métricas de desempenho conforme a especificação do trabalho prático.

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
- Aplicação de **timeout de 600 segundos** por execução (quando habilitado).
- Registro automático de resultados no console **e em arquivo `log.txt`**.
- Saída formatada em **tabelas legíveis**, facilitando análise e uso no relatório.

---

## ⚙️ Tecnologias Utilizadas
- **Python 3**
- Conceitos fundamentais de:
  - Grafos
  - Algoritmos de Caminhos Mínimos
  - Análise de Complexidade
  - Programação Multiprocessada (para controle de tempo)

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
  - Versão com e sem otimização para nós desconexos.
- **Bellman-Ford**
  - Implementação fiel ao pseudocódigo.
  - Interrupção antecipada quando não há atualização.
- **Floyd-Warshall**
  - Cálculo de todos os pares de caminhos mínimos.
  - Uso de matrizes de distância e predecessores.

---

### Benchmark e Análise Experimental
- Execução automática em múltiplos mapas.
- Coleta de:
  - Tempo individual por rodada.
  - Custo individual por rodada.
- Geração de:
  - Tabelas por algoritmo (10 execuções).
  - Resumo consolidado por mapa.
- Registro completo no:
  - **Console**
  - **Arquivo `log.txt`**

---

## 🗂️ Estrutura do Projeto (arquivos-chave)

- **Algoritmos de Caminho Mínimo**  
  `Algoritmos.py`
- **Estruturas de Grafo**  
  `Grafo.py`
- **Leitura de Mapas e Geração de Grafos**  
  `Mapa.py`
- **Execução simples (1 rodada por algoritmo)**  
  `main.py`
- **Execução de Experimentos Computacionais (benchmark)**  
  `main_benchmark.py`
- **Registro automático dos resultados**  
  `log.txt`

---

## 🧭 Fluxo de Execução
1. O programa lê um mapa `.txt`.
2. O mapa é convertido em um grafo ponderado.
3. O algoritmo escolhido calcula o caminho mínimo entre `I` e `F`.
4. O caminho é reconstruído via predecessores.
5. O mapa de saída é salvo com o caminho marcado.
6. No modo benchmark:
   - Cada algoritmo é executado **10 vezes por mapa**.
   - São calculadas médias de tempo e custo.
   - Resultados são exibidos em tabela e gravados em `log.txt`.

---

## ▶️ Execução

### Execução Simples (1 rodada por algoritmo)
```
python main.py <arquivo_mapa.txt>
```

### Execução dos Experimentos Computacionais (Benchmark)
```
python main_benchmark.py <pasta_mapas>
```

Exemplo:
```
python main_benchmark.py mapas/
```

---

## 📊 Saída Esperada
- Console:
  - Tabelas detalhadas por algoritmo.
  - Médias por mapa.
- Arquivos:
  - `saida_dijkstra.txt`
  - `saida_bellman_ford.txt`
  - `saida_floyd_warshall.txt`
  - `log.txt`

---

## 📈 Análise Experimental
Os resultados obtidos permitem discutir:
- Qual algoritmo apresenta melhor desempenho para mapas grandes.
- Diferenças entre a complexidade teórica e o comportamento observado.
- Impacto do tamanho e da estrutura do mapa no tempo de execução.
- Limitações práticas do Floyd-Warshall em grafos grandes.

---

## 🎓 Disciplina
**CSI115 – 25.2 – Algoritmos e Estruturas de Dados III**
