#grafo = MatrizAdjacencias(4)
from ListaAdjacencias import ListaAdjacencias
from Helpers import dfs, dfsIterativo 

grafo = ListaAdjacencias(9) #grafo com 9 vertices (0 a 8)

grafo.addAresta(0, 3)
grafo.addAresta(0, 5)
grafo.addAresta(0, 6)
grafo.addAresta(6, 8)
grafo.addAresta(3, 6)
grafo.addAresta(5, 7)
grafo.addAresta(7, 0)
grafo.addAresta(7, 1)
grafo.addAresta(1, 4)
grafo.addAresta(2, 4)
grafo.addAresta(2, 1)

# grafo = leitura("grafo.txt")

# print(f"Ordem: {grafo.ordem()}")
# print(f"Tamanho: {grafo.tamanho()}")
# print(f"Possui aresta (3, 2) ? {grafo.possuiAresta(3, 2)}")
# print(f"Possui aresta (1, 3) ? {grafo.possuiAresta(1, 3)}")
# print(f"Vizinhos do vertice 1: {grafo.vizinhos(1)}")
# print(f"Grau do vertice 1: {grafo.grau(1)}")

grafo.printGrafo()

# print(f"densidade do grafo: {grafo.densidade()}")

R = dfs(grafo, 0)
print(f"DFS: {R}")

R = dfsIterativo(grafo, 0)
print(f"DFS iterativo: {R}")