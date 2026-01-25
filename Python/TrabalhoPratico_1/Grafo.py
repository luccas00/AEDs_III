
# --------------------------------------------------------------------
# Estruturas de Grafo utilizadas Matriz ou Lista de adjacências
# Implementação baseada no material da disciplina
# --------------------------------------------------------------------

class MatrizAdjacencias:
    def __init__(self, numVertices):
        self.numVertices = numVertices
        self.numArestas = 0
        self.grauVertice = [0] * numVertices
        self.matriz = [[0] * numVertices for _ in range(numVertices)]

    def ordem(self):
        return self.numVertices

    def tamanho(self):
        return self.numArestas

    def densidade(self):
        maxArestas = self.numVertices * (self.numVertices - 1)
        return self.numArestas / maxArestas

    def addAresta(self, v1, v2, peso=1):
        if self.matriz[v1][v2] == 0:
            self.numArestas += 1
            self.grauVertice[v1] += 1
        self.matriz[v1][v2] = peso

    def possuiAresta(self, v1, v2):
        return self.matriz[v1][v2] != 0

    def vizinhos(self, v):
        return [(i, self.matriz[v][i]) for i in range(self.numVertices) if self.matriz[v][i] != 0]

    def grau(self, v):
        return self.grauVertice[v]

    def printGrafo(self):
        for i in range(self.numVertices):
            print(" ".join(str(x) for x in self.matriz[i]))


class ListaAdjacencias:
    # Estrutura mais eficiente para grafos esparsos
    def __init__(self, numVertices):
        self.numVertices = numVertices
        self.numArestas = 0
        self.lista = [[] for _ in range(numVertices)]

    def ordem(self):
        return self.numVertices

    def tamanho(self):
        return self.numArestas

    def densidade(self):
        maxArestas = self.numVertices * (self.numVertices - 1)
        return self.numArestas / maxArestas

    def addAresta(self, v1, v2, peso=1):
        self.lista[v1].append((v2, peso))
        self.numArestas += 1

    def possuiAresta(self, v1, v2):
        return any(vertice == v2 for vertice, _ in self.lista[v1])

    def vizinhos(self, v):
        return self.lista[v]

    def grau(self, v):
        return len(self.lista[v])

    def printGrafo(self):
        for i in range(self.numVertices):
            print(f"Vertice {i}:", self.lista[i])
