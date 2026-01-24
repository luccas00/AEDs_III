# Representação computacional de um grafo por meio de matriz de adjacências:
class MatrizAdjacencias:
    # Inicializa o grafo:
    def __init__(self, numVertices):
      self.numVertices = numVertices
      self.numArestas = 0
      self.grauVertice = [0] * self.numVertices
      self.matriz = [[0] * self.numVertices for i in range(self.numVertices)]

    # Retorna a ordem do grafo:
    def ordem(self):
      return self.numVertices

    # Retorna o tamanho do grafo:
    def tamanho(self):
      return self.numArestas

    # retorna a densidade do grafo:
    def densidade(self):
      maxArestas = self.numVertices * (self.numVertices - 1)
      return self.numArestas / maxArestas

    # Adiciona uma aresta (v1, v2) no grafo:
    # peso é um parametro opcional
    def addAresta(self, v1, v2, peso = 1):
      if self.matriz[v1][v2] == 0:
        self.numArestas += 1
        self.grauVertice[v1] += 1

      self.matriz[v1][v2] = peso

    # retorna True se existe uma aresta (v1,v2) no grafo:
    def possuiAresta(self, v1, v2):
      return self.matriz[v1][v2] != 0

    # retorna uma lista de tuplas (vertice, peso) com os vizinhos de v:
    def vizinhos(self, v):
      viz = []
      for i in range(self.numVertices):
        if self.matriz[v][i] != 0:
          viz.append((i, self.matriz[v][i]))

      return viz

    # retorna o grau (saida) de um vertice:
    def grau(self, v):
      return self.grauVertice[v]

    # exibe o grafo no formato de matriz de adjacencias:
    def printGrafo(self):
      for i in range(self.numVertices):
        for j in range(self.numVertices):
          print(self.matriz[i][j], end=" ")
        print()

    # retorna um subgrafo induzido pelo conjunto de vertices:
    def subgrafo(self, vertices):
      print("Metodo subgrafo(grafo, vertices) nao foi implementado ainda!")
      return None


# Representação computacional de um grafo por meio de lista de adjacências:
class ListaAdjacencias:
    # Inicializa o grafo:
    def __init__(self, numVertices):
        self.numVertices = numVertices
        self.numArestas = 0
        self.lista = [[] for i in range(self.numVertices)]

        # as linhas a seguir têm o mesmo efeito da linha 7:
        # self.lista = []
        # for i in range(self.numVertices):
        #   self.lista.append([])

    # Retorna a ordem do grafo:
    def ordem(self):
      return self.numVertices

    # Retorna o tamanho do grafo:
    def tamanho(self):
      return self.numArestas

    # retorna a densidade do grafo:
    def densidade(self):
      maxArestas = self.numVertices * (self.numVertices - 1)
      return self.numArestas / maxArestas

    # Adiciona uma aresta (v1, v2) no grafo:
    # peso é um parametro opcional
    def addAresta(self, v1, v2, peso = 1):
      self.lista[v1].append((v2, peso))
      self.numArestas += 1

    # retorna True se existe uma aresta (v1,v2) no grafo:
    def possuiAresta(self, v1, v2):
      for (vertice, peso) in self.lista[v1]:
        if vertice == v2:
          return True

      return False

    # retorna uma lista de tuplas (vertice, peso) com os vizinhos de v:
    def vizinhos(self, v):
      return self.lista[v]

    # retorna o grau (saida) de um vertice:
    def grau(self, v):
      return len(self.lista[v])

    # exibe o grafo no formato de matriz de adjacencias:
    def printGrafo(self):
      for i in range(self.numVertices):
        print(f"Vertice {i}:", end=" ")
        for (j, p) in self.lista[i]:
          print({(j, p)}, end=" ")
        print()

    # retorna um subgrafo induzido pelo conjunto de vertices:
    def subgrafo(self, vertices):
      print("Metodo subgrafo(vertices) nao foi implementado ainda!")
      return None

# cria um grafo a partir de um arquivo:
def leitura(nomeArquivo):
  arquivo = open(nomeArquivo)
  linha = arquivo.readline()
  vLinha = linha.split(" ")
  numVertices = int(vLinha[0])
  numArestas = int(vLinha[1])

  # grafo = MatrizAdjacencias(numVertices)
  grafo = ListaAdjacencias(numVertices)

  for i in range(numArestas):
    linha = arquivo.readline()
    vLinha = linha.split(" ")
    origem = int(vLinha[0])
    destino = int(vLinha[1])
    peso = int(vLinha[2])
    grafo.addAresta(origem, destino, peso)

  return grafo


def dfsRecursivo(grafo, R, visitado, u):
  visitado[u] = True
  R.append(u)

  for (v, peso) in grafo.vizinhos(u):
    if not visitado[v]:
      dfsRecursivo(grafo, R, visitado, v)

def dfs(grafo, s):
  R = []
  visitado = [False] * grafo.numVertices
  dfsRecursivo(grafo, R, visitado, s)
  return R

def dfsIterativo(grafo, s):
  R = []
  pilha = []
  visitado = [False] * grafo.numVertices
  pilha.append(s)
  visitado[s] = True

  while len(pilha) > 0:
    u = pilha.pop()
    R.append(u)
    for (v, peso) in grafo.vizinhos(u):
      if not visitado[v]:
        pilha.append(v)
        visitado[v] = True

  return R


# =====================================================================
# A PARTIR DAQUI: IMPLEMENTAÇÃO DO TRABALHO (MAPA, DIJKSTRA, BELLMAN-FORD, FLOYD-WARSHALL)
# =====================================================================

import sys
import time

INF = float("inf")

def custo_terreno(c):
  if c == 'W':
    return 5
  if c == 'S':
    return 3
  if c == 'G':
    return 1
  if c == 'I':
    return 0
  if c == 'F':
    return 0
  raise ValueError(f"Terreno invalido: {c}")


def carregar_mapa(nome_arquivo):
  grid = []

  with open(nome_arquivo, 'r') as f:
    for linha in f:
      linha = linha.rstrip('\n')
      if not linha:
        continue
      linha = linha.replace(" ", "")
      grid.append(list(linha))

  if len(grid) == 0:
    raise ValueError("Mapa vazio")

  linhas = len(grid)
  colunas = len(grid[0])

  for i in range(linhas):
    if len(grid[i]) != colunas:
      raise ValueError("Mapa nao eh retangular")

  inicio = None
  fim = None

  for i in range(linhas):
    for j in range(colunas):
      if grid[i][j] == 'I':
        if inicio is not None:
          raise ValueError("Mapa possui mais de um inicio")
        inicio = i * colunas + j
      elif grid[i][j] == 'F':
        if fim is not None:
          raise ValueError("Mapa possui mais de um fim")
        fim = i * colunas + j

  if inicio is None or fim is None:
    raise ValueError("Mapa deve conter exatamente um I e um F")

  numVertices = linhas * colunas
  grafo = ListaAdjacencias(numVertices)

  direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]

  for i in range(linhas):
    for j in range(colunas):
      terreno_origem = grid[i][j]
      if terreno_origem == '#':
        continue

      u = i * colunas + j

      for (di, dj) in direcoes:
        ni = i + di
        nj = j + dj

        if 0 <= ni < linhas and 0 <= nj < colunas:
          terreno_destino = grid[ni][nj]
          if terreno_destino == '#':
            continue

          v = ni * colunas + nj

          if terreno_destino == 'F':
            peso = 0
          else:
            peso = custo_terreno(terreno_destino)

          grafo.addAresta(u, v, peso)

  return grid, linhas, colunas, inicio, fim, grafo


def reconstruir_caminho_prev(prev, s, t):
  if s == t:
    return [s]

  if prev[t] is None and t != s:
    return []

  caminho = []
  atual = t

  while True:
    caminho.append(atual)
    if atual == s:
      break
    atual = prev[atual]
    if atual is None:
      return []

  caminho.reverse()
  return caminho


def marcar_caminho(grid, linhas, colunas, caminho):
  novo = [linha[:] for linha in grid]

  for v in caminho:
    r = v // colunas
    c = v % colunas
    ch = novo[r][c]
    if ch != 'I' and ch != 'F':
      novo[r][c] = '*'

  return novo


def salvar_mapa(grid, nome_arquivo):
  with open(nome_arquivo, 'w') as f:
    for linha in grid:
      f.write("".join(linha) + "\n")


# ---------------------------------------------------------
# DIJKSTRA (conforme pseudocodigo)
# ---------------------------------------------------------
# ---------------------------------------------------------
# DIJKSTRA (EXATAMENTE COMO NO PSEUDOCÓDIGO DO PROFESSOR)
# ---------------------------------------------------------
def dijkstra(grafo, s):
    V = grafo.numVertices

    # Linha 1–3 do pseudocódigo
    dist = [float('inf')] * V
    prev = [None] * V

    # Linha 4–5
    dist[s] = 0
    prev[s] = s

    # Linha 6–7
    O = set(range(V))   # conjunto de abertos
    C = set()           # conjunto de fechados

    # Linha 8
    while C != set(range(V)):
        
        # Linha 9: escolher u em O com dist[u] mínimo
        u = None
        menor = float('inf')
        for v in O:
            if dist[v] < menor:
                menor = dist[v]
                u = v

        # Pode acontecer se o grafo for desconexo
        if u is None:
            break

        # Linha 10–11
        C.add(u)
        O.remove(u)

        # Linha 12–15: relaxar vizinhos
        for (v, peso) in grafo.vizinhos(u):
            if v not in C:
                if dist[v] > dist[u] + peso:
                    dist[v] = dist[u] + peso
                    prev[v] = u

    return dist, prev


# def dijkstra(grafo, s):
#   V = grafo.numVertices
#   dist = [INF] * V
#   prev = [None] * V

#   dist[s] = 0
#   prev[s] = s

#   visitado = [False] * V

#   for _ in range(V):
#     u = -1
#     menor = INF

#     for v in range(V):
#       if not visitado[v] and dist[v] < menor:
#         menor = dist[v]
#         u = v

#     if u == -1:
#       break

#     visitado[u] = True

#     for (v, peso) in grafo.vizinhos(u):
#       if not visitado[v] and dist[v] > dist[u] + peso:
#         dist[v] = dist[u] + peso
#         prev[v] = u

#   return dist, prev


# ---------------------------------------------------------
# BELLMAN-FORD (conforme pseudocodigo)
# ---------------------------------------------------------
def bellman_ford(grafo, s):
    V = grafo.numVertices

    # Linha 1–3
    dist = [float('inf')] * V
    prev = [None] * V

    # Linha 4–5
    dist[s] = 0
    prev[s] = s

    # Linha 6
    for k in range(V - 1):
        atualizou = False  # Linha 7

        # Linha 8
        for u in range(V):

            # Linha 9
            for (v, peso) in grafo.vizinhos(u):

                # Linha 10
                if dist[v] > dist[u] + peso:
                    # Linha 11
                    dist[v] = dist[u] + peso
                    # Linha 12
                    prev[v] = u
                    # Linha 13
                    atualizou = True

        # Linha 14–15
        if atualizou == False:
            break

    return dist, prev



# ---------------------------------------------------------
# FLOYD-WARSHALL (conforme pseudocodigo)
# ---------------------------------------------------------
def floyd_warshall(grafo):
    V = grafo.numVertices

    # Linha 1–11
    dist = [[float('inf')] * V for _ in range(V)]
    prev = [[None] * V for _ in range(V)]

    for i in range(V):
        for j in range(V):

            # Linha 3–5
            if i == j:
                dist[i][j] = 0
                prev[i][j] = i

            # Linha 6–8
            elif grafo.possuiAresta(i, j):
                # buscar peso w(i,j)
                for (v, peso) in grafo.vizinhos(i):
                    if v == j:
                        dist[i][j] = peso
                        prev[i][j] = i
                        break

            # Linha 9–11
            else:
                dist[i][j] = float('inf')
                prev[i][j] = None

    # Linha 12–17
    for k in range(V):
        for i in range(V):
            for j in range(V):

                # Linha 15
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    # Linha 16
                    dist[i][j] = dist[i][k] + dist[k][j]
                    # Linha 17
                    prev[i][j] = prev[k][j]

    return dist, prev



def reconstruir_caminho_floyd(prev, s, t):
  if s == t:
    return [s]

  if prev[s][t] is None:
    return []

  caminho = []
  atual = t

  while True:
    caminho.append(atual)
    if atual == s:
      break
    atual = prev[s][atual]
    if atual is None:
      return []

  caminho.reverse()
  return caminho


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
def executar_algoritmo(nome, func_execucao, grid, linhas, colunas, inicio, fim, grafo, arquivo_saida):
  inicio_tempo = time.perf_counter()
  resultado = func_execucao(grafo, inicio)
  fim_tempo = time.perf_counter()

  if nome == "Floyd-Warshall":
    dist, prev = resultado
    custo = dist[inicio][fim]
    if custo == INF:
      print(f"----- {nome} -----")
      print("Nao existe caminho entre I e F")
      print("------------------------------")
      return
    caminho = reconstruir_caminho_floyd(prev, inicio, fim)
  else:
    dist, prev = resultado
    custo = dist[fim]
    if custo == INF:
      print(f"----- {nome} -----")
      print("Nao existe caminho entre I e F")
      print("------------------------------")
      return
    caminho = reconstruir_caminho_prev(prev, inicio, fim)

  grid_saida = marcar_caminho(grid, linhas, colunas, caminho)
  salvar_mapa(grid_saida, arquivo_saida)

  print("-------------------------------------------------")
  print(f"Algoritmo de {nome}:")
  print(f"Custo: {custo}")
  print(f"Tempo execucao: {fim_tempo - inicio_tempo:.6f} s")
  print("-------------------------------------------------")


def exec_floyd_wrapper(grafo, s):
  dist, prev = floyd_warshall(grafo)
  return dist, prev


def main():
  if len(sys.argv) != 2:
    print("Uso: python main.py <arquivo_mapa>")
    return

  nome_mapa = sys.argv[1]

  grid, linhas, colunas, inicio, fim, grafo = carregar_mapa(nome_mapa)

  executar_algoritmo(
    "Dijkstra",
    dijkstra,
    grid,
    linhas,
    colunas,
    inicio,
    fim,
    grafo,
    "saida_dijkstra.txt"
  )

  executar_algoritmo(
    "Bellman-Ford",
    lambda g, s: bellman_ford(g, s),
    grid,
    linhas,
    colunas,
    inicio,
    fim,
    grafo,
    "saida_bellman_ford.txt"
  )

  executar_algoritmo(
    "Floyd-Warshall",
    exec_floyd_wrapper,
    grid,
    linhas,
    colunas,
    inicio,
    fim,
    grafo,
    "saida_floyd_warshall.txt"
  )


if __name__ == "__main__":
  main()

