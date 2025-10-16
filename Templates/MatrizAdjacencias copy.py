# Representação computacional de um grafo por meio de matriz de adjacências:

class MatrizAdjacencias:

    #__init__ = construtor da classe
    #self = o que eu quero receber como parametro
    #para acessar qualquer atributo é só usar self.atributo

    # Inicializa o grafo:
    def __init__(self, numVertices): #Tem que passar a quantidade de vertices 
        print("Implementar construtor...")
        self.numVertices = numVertices
        self.numArestas = 0``
        self.matriz = []

     #cria uma lista que começa com elementos do 0, ou seja, o range ta incrementando o i
        for i in range(self.numVertices):
            self.matriz.append([0] * self.numVertices)

    # Retorna a ordem do grafo(numVertices):
    def ordem(self):
        print("Implementar ordem")
        return self.numVertices

    # Retorna o tamanho do grafo:
    def tamanho(self):
        return self.numArestas

    # Adiciona uma aresta (v1, v2) no grafo:
    # peso é um parametro opcional
    def addAresta(self, v1, v2, peso = 1):
        if self.matriz[v1][v2] == 0:
            self.numArestas += 1 #o python não aceita self.numArestas++

            self.matriz[v1][v2] = peso

    # retorna True se existe uma aresta (v1,v2) no grafo:
    def possuiAresta(self, v1, v2):
        return self.matriz[v1][v2] != 0  # se na linha tiver um valor diferente de 0, é pq tem ligacao
           

    # retorna uma lista de tuplas (vertice, peso) com os vizinhos de v:
    def vizinhos(self, v):
        print("Implementar vizinhos")
        return None

    # retorna o grau (saida) de um vertice:
    def grau(self, v):
        print("Implementar grau")
        return None

    # exibe o grafo no formato de matriz de adjacencias:
    def printGrafo(self):
        print("Implementar printGrafo")
        return None
    


    test = [0] * 5
    print (test)

grafo = MatrizAdjacencias(4)
grafo.addAresta(0,1,5)
grafo.addAresta(1,2,2)
grafo.addAresta(1,3,3)
grafo.addAresta(2,3,6)

print(f"Ordem do Grafo: {grafo.ordem()}")
print(f"Tamanho do Grafo: {grafo.tamanho()}")
print(f"Possui Arestra entre 0 e 1? : {grafo.possuiAresta(0,1)}")
print(f"Possui Arestra entre 0 e 1? : {grafo.possuiAresta(3,1)}")