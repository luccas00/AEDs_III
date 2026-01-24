# algoritmos.py
# -----------------------------------------------------------------------------------------
# Implementação fiel dos algoritmos de Dijkstra, Bellman-Ford e Floyd-Warshall (pseudocódigo)
# -----------------------------------------------------------------------------------------

INF = float("inf")

# -----------------------------
# DIJKSTRA
# -----------------------------
def dijkstra(grafo, s):
    V = grafo.numVertices

    dist = [INF] * V
    prev = [None] * V

    dist[s] = 0
    prev[s] = s

    O = set(range(V))  # abertos
    C = set()          # fechados

    while C != set(range(V)):
        u = None
        menor = INF
        for v in O:
            if dist[v] < menor:
                menor = dist[v]
                u = v

        if u is None:
            break

        C.add(u)
        O.remove(u)

        for (v, peso) in grafo.vizinhos(u):
            if v not in C and dist[v] > dist[u] + peso:
                dist[v] = dist[u] + peso
                prev[v] = u

    return dist, prev


# -----------------------------
# BELLMAN-FORD
# -----------------------------
def bellman_ford(grafo, s):
    V = grafo.numVertices

    dist = [INF] * V
    prev = [None] * V

    dist[s] = 0
    prev[s] = s

    for k in range(V - 1):
        atualizou = False

        for u in range(V):
            for (v, peso) in grafo.vizinhos(u):
                if dist[v] > dist[u] + peso:
                    dist[v] = dist[u] + peso
                    prev[v] = u
                    atualizou = True

        if not atualizou:
            k = V - 1

    return dist, prev


# -----------------------------
# FLOYD-WARSHALL
# -----------------------------
def floyd_warshall(grafo):
    V = grafo.numVertices

    dist = [[INF]*V for _ in range(V)]
    prev = [[None]*V for _ in range(V)]

    for i in range(V):
        for j in range(V):

            if i == j:
                dist[i][j] = 0
                prev[i][j] = i

            elif grafo.possuiAresta(i,j):
                for (v, peso) in grafo.vizinhos(i):
                    if v == j:
                        dist[i][j] = peso
                        prev[i][j] = i

    for k in range(V):
        for i in range(V):
            for j in range(V):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    prev[i][j] = prev[k][j]

    return dist, prev


# -----------------------------
# Reconstrução de Caminho
# -----------------------------
def reconstruir_caminho_prev(prev, s, t):
    if s == t:
        return [s]

    if prev[t] is None:
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


def reconstruir_caminho_floyd(prev, s, t):
    if prev[s][t] is None:
        return []

    caminho = []
    atual = t

    while True:
        caminho.append(atual)
        if atual == s:
            break
        atual = prev[s][atual]

    caminho.reverse()
    return caminho
