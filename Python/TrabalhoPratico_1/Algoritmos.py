
# -----------------------------------------------------------------------------------------
# Implementação dos algoritmos de Dijkstra, Bellman-Ford e Floyd-Warshall conforme pseudocódigo
# -----------------------------------------------------------------------------------------

INF = float("inf") 

def dijkstra(grafo, origem):
    
    total_vertices = grafo.numVertices
    
    distancias = [INF] * total_vertices
    predecessor = [None] * total_vertices
    
    distancias[origem] = 0
    predecessor[origem] = origem

    abertos = set(range(total_vertices))
    fechados = set()

    while fechados != set(range(total_vertices)):
    
        vertice_atual = next(iter(abertos))
    
        menor_distancia = distancias[vertice_atual]

        for v in abertos:
            if distancias[v] < menor_distancia:
                menor_distancia = distancias[v]
                vertice_atual = v

        fechados.add(vertice_atual)

        abertos.remove(vertice_atual)

        for (vizinho, peso) in grafo.vizinhos(vertice_atual):
    
            if vizinho not in fechados:
    
                distancia_alternativa = distancias[vertice_atual] + peso

                if distancias[vizinho] > distancia_alternativa:
    
                    distancias[vizinho] = distancia_alternativa
                    predecessor[vizinho] = vertice_atual

    # retorna as listas dist e prev
    return distancias, predecessor

def bellman_ford(grafo, origem):

    total_vertices = grafo.numVertices

    distancias = [INF] * total_vertices
    predecessor = [None] * total_vertices

    distancias[origem] = 0
    predecessor[origem] = origem

    for _ in range(total_vertices - 1):

        houve_atualizacao = False

        for u in range(total_vertices):

            for (v, peso) in grafo.vizinhos(u):

                if distancias[v] > distancias[u] + peso:

                    distancias[v] = distancias[u] + peso
                    predecessor[v] = u

                    houve_atualizacao = True

        # se nenhuma distância foi atualizada, o algoritmo pode parar
        if not houve_atualizacao:
            break

    # retorna as distâncias mínimas e os predecessores
    return distancias, predecessor

def floyd_warshall(grafo):

    total_vertices = grafo.numVertices

    distancias = [[INF] * total_vertices for _ in range(total_vertices)]
    predecessor = [[None] * total_vertices for _ in range(total_vertices)]

    # inicialização das matrizes dist e predecessor
    for i in range(total_vertices):
        for j in range(total_vertices):

            if i == j:
                distancias[i][j] = 0
                predecessor[i][j] = i

            elif grafo.possuiAresta(i, j):

                for (vizinho, peso) in grafo.vizinhos(i):
                    if vizinho == j:
                        distancias[i][j] = peso
                        predecessor[i][j] = i

    for k in range(total_vertices):

        for i in range(total_vertices):

            for j in range(total_vertices):

                if distancias[i][j] > distancias[i][k] + distancias[k][j]:

                    distancias[i][j] = distancias[i][k] + distancias[k][j]
                    predecessor[i][j] = predecessor[k][j]

    # retorna a matriz de distâncias e predecessores
    return distancias, predecessor

# -----------------------------
# Reconstrução de Caminho (prev por vértice)
# -----------------------------
def reconstruir_caminho_prev(prev, s, t):
    
    if s == t:
        return [s]

    if prev[t] is None:
        return []

    caminho = []

    # começa pelo destino e volta usando o vetor de predecessores
    vertice_atual = t

    max_passos = len(prev)
    passos = 0

    while True:
        # adiciona o vértice atual ao caminho
        caminho.append(vertice_atual)

        # se chegou na origem, finaliza
        if vertice_atual == s:
            break

        # anda para o predecessor do vértice atual
        vertice_atual = prev[vertice_atual]

        if vertice_atual is None:
            return []

        passos += 1
        if passos > max_passos:
            return []  # prev contém ciclo/inconsistência

    # inverte para ficar na ordem correta: s -> ... -> t
    caminho.reverse()
    return caminho


# -----------------------------
# Reconstrução de Caminho do Floyd-Warshall
# -----------------------------
def reconstruir_caminho_floyd(prev, s, t):
    
    if prev[s][t] is None:
        return []

    caminho = []

    vertice_atual = t

    max_passos = len(prev)  # total de vértices
    passos = 0

    while True:
        # adiciona o vértice atual ao caminho
        caminho.append(vertice_atual)

        # se chegou na origem, finaliza
        if vertice_atual == s:
            break

        # anda para o predecessor de 'vertice_atual' no caminho que sai de s
        vertice_atual = prev[s][vertice_atual]

        # se em algum ponto não existir predecessor, não há caminho válido
        if vertice_atual is None:
            return []

        passos += 1
        if passos > max_passos:
            return []  # prev contém ciclo

    # inverte para ficar na ordem correta
    caminho.reverse()
    return caminho
