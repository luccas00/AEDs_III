class MatrizAdjacencias:
    # Construtor: cria uma matriz vazia
    def __init__(self, num_vertices):
        self.num_vertices = num_vertices
        # Inicializa uma matriz num_vertices x num_vertices com zeros
        self.matriz = [[0 for _ in range(num_vertices)] for _ in range(num_vertices)]

    # Retorna a ordem do grafo (número de vértices)
    def ordem(self):
        return self.num_vertices

    # Retorna o tamanho do grafo (número de arestas)
    def tamanho(self):
        count = 0
        for i in range(self.num_vertices):
            for j in range(self.num_vertices):
                if self.matriz[i][j] != 0:
                    count += 1
        return count

    # Adiciona uma aresta (v1, v2)
    def addAresta(self, v1, v2, peso=1):
        self.matriz[v1][v2] = peso
        self.matriz[v2][v1] = peso  # Remove se quiser grafo direcionado

    # Verifica se existe uma aresta (v1, v2)
    def possuiAresta(self, v1, v2):
        return self.matriz[v1][v2] != 0

    # Retorna uma lista de tuplas (vizinho, peso)
    def vizinhos(self, v):
        viz = []
        for i in range(self.num_vertices):
            if self.matriz[v][i] != 0:
                viz.append((i, self.matriz[v][i]))
        return viz

    # Retorna o grau do vértice
    def grau(self, v):
        grau = 0
        for i in range(self.num_vertices):
            if self.matriz[v][i] != 0:
                grau += 1
        return grau

    # Exibe o grafo no formato de matriz de adjacências
    def printGrafo(self):
        for linha in self.matriz:
            print(linha)
