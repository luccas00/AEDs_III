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
