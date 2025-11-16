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