# algoritmos.py
# -----------------------------------------------------------------------------------------
# Implementação fiel dos algoritmos de Dijkstra, Bellman-Ford e Floyd-Warshall (pseudocódigo)
# -----------------------------------------------------------------------------------------

INF = float("inf")  # representa "infinito" para distâncias desconhecidas

def dijkstra_iniciante(grafo, origem):
    # total de vértices do grafo (assumindo índices 0..V-1)
    total_vertices = grafo.numVertices

    # distancias[i] = melhor distância conhecida da origem até o vértice i
    distancias = [INF] * total_vertices

    # predecessor[i] = vértice anterior no caminho mínimo até i (ou None se não definido)
    predecessor = [None] * total_vertices

    # distância da origem para ela mesma é 0 (linha 4 do pseudocódigo)
    distancias[origem] = 0

    # predecessor da origem é ela mesma (linha 5 do pseudocódigo)
    predecessor[origem] = origem

    # abertos = conjunto O (vértices ainda não "fechados") (linha 6: O <- V)
    abertos = set(range(total_vertices))

    # fechados = conjunto C (vértices já processados/finalizados) (linha 7: C <- ∅)
    fechados = set()

    # enquanto C != V (linha 8)
    while fechados != set(range(total_vertices)):
        # escolhe um vértice qualquer de "abertos" como candidato inicial
        vertice_atual = next(iter(abertos))

        # menor_distancia guarda a menor dist encontrada dentro do conjunto "abertos"
        menor_distancia = distancias[vertice_atual]

        # varre todos os vértices em "abertos" para achar aquele com menor dist (linha 9)
        for v in abertos:
            if distancias[v] < menor_distancia:
                menor_distancia = distancias[v]
                vertice_atual = v

        # adiciona o vértice escolhido ao conjunto "fechados" (linha 10)
        fechados.add(vertice_atual)

        # remove o vértice escolhido do conjunto "abertos" (linha 11)
        abertos.remove(vertice_atual)

        # percorre cada vizinho do vértice_atual (linha 12)
        # grafo.vizinhos(u) deve devolver pares (vizinho, peso_da_aresta)
        for (vizinho, peso) in grafo.vizinhos(vertice_atual):
            # só considera vizinho que ainda NÃO está fechado (condição v ∉ C da linha 12)
            if vizinho not in fechados:
                # calcula a distância alternativa indo origem -> ... -> vertice_atual -> vizinho
                distancia_alternativa = distancias[vertice_atual] + peso

                # se essa rota for melhor do que a distância atual do vizinho (linha 13)
                if distancias[vizinho] > distancia_alternativa:
                    # atualiza a melhor distância do vizinho (linha 14)
                    distancias[vizinho] = distancia_alternativa

                    # registra que o predecessor do vizinho no melhor caminho é vertice_atual (linha 15)
                    predecessor[vizinho] = vertice_atual

    # retorna as listas dist e prev (como no seu código)
    return distancias, predecessor


def dijkstra_iniciante_otimizado(grafo, origem):
    total_vertices = grafo.numVertices
    distancias = [INF] * total_vertices
    predecessor = [None] * total_vertices

    distancias[origem] = 0
    predecessor[origem] = origem

    abertos = set(range(total_vertices))
    fechados = set()

    while abertos:  # com otimização, basta rodar enquanto ainda há abertos
        vertice_atual = next(iter(abertos))
        menor_distancia = distancias[vertice_atual]

        for v in abertos:
            if distancias[v] < menor_distancia:
                menor_distancia = distancias[v]
                vertice_atual = v

        # OTIMIZAÇÃO: se o menor ainda é INF, não existe caminho para o restante
        if menor_distancia == INF:
            break

        fechados.add(vertice_atual)
        abertos.remove(vertice_atual)

        for (vizinho, peso) in grafo.vizinhos(vertice_atual):
            if vizinho not in fechados:
                distancia_alternativa = distancias[vertice_atual] + peso
                if distancias[vizinho] > distancia_alternativa:
                    distancias[vizinho] = distancia_alternativa
                    predecessor[vizinho] = vertice_atual

    return distancias, predecessor


# -----------------------------
# BELLMAN-FORD (VERSÃO DIDÁTICA)
# -----------------------------
def bellman_ford_iniciante(grafo, origem):
    # quantidade total de vértices do grafo
    total_vertices = grafo.numVertices

    # distancias[i] = menor distância conhecida da origem até o vértice i
    distancias = [INF] * total_vertices

    # predecessor[i] = vértice anterior no caminho mínimo até i
    predecessor = [None] * total_vertices

    # distância da origem para ela mesma é zero (linha 4 do pseudocódigo)
    distancias[origem] = 0

    # predecessor da origem é ela mesma (linha 5)
    predecessor[origem] = origem

    # repete o processo no máximo |V| - 1 vezes (linha 6)
    for _ in range(total_vertices - 1):
        # indica se alguma distância foi atualizada nesta iteração
        houve_atualizacao = False

        # percorre todos os vértices u do grafo (linha 8)
        for u in range(total_vertices):
            # percorre todos os vizinhos v de u (linha 9)
            # grafo.vizinhos(u) retorna pares (vizinho, peso_da_aresta)
            for (v, peso) in grafo.vizinhos(u):
                # verifica se o caminho passando por u melhora a distância até v (linha 10)
                if distancias[v] > distancias[u] + peso:
                    # atualiza a melhor distância até v (linha 11)
                    distancias[v] = distancias[u] + peso

                    # registra u como predecessor de v no caminho mínimo (linha 12)
                    predecessor[v] = u

                    # marca que houve atualização nesta iteração (linha 13)
                    houve_atualizacao = True

        # se nenhuma distância foi atualizada, o algoritmo pode parar (linhas 14–15)
        if not houve_atualizacao:
            break

    # retorna as distâncias mínimas e os predecessores
    return distancias, predecessor


# -----------------------------
# FLOYD-WARSHALL (VERSÃO DIDÁTICA)
# -----------------------------
def floyd_warshall_iniciante(grafo):
    # número total de vértices do grafo
    total_vertices = grafo.numVertices

    # distancias[i][j] = menor distância conhecida de i até j
    distancias = [[INF] * total_vertices for _ in range(total_vertices)]

    # predecessor[i][j] = vértice anterior a j no melhor caminho de i até j
    predecessor = [[None] * total_vertices for _ in range(total_vertices)]

    # inicialização das matrizes dist e predecessor (linhas 1 a 11)
    for i in range(total_vertices):
        for j in range(total_vertices):

            # caso i == j: distância zero e predecessor é o próprio i
            if i == j:
                distancias[i][j] = 0
                predecessor[i][j] = i

            # caso exista aresta direta de i para j
            elif grafo.possuiAresta(i, j):
                # busca o peso da aresta (i, j)
                for (vizinho, peso) in grafo.vizinhos(i):
                    if vizinho == j:
                        distancias[i][j] = peso
                        predecessor[i][j] = i

            # caso não exista caminho direto, mantém infinito e None
            # (já inicializado anteriormente)

    # laços principais do Floyd-Warshall (linhas 12 a 17)
    # k é o vértice intermediário considerado
    for k in range(total_vertices):
        # i é o vértice de origem
        for i in range(total_vertices):
            # j é o vértice de destino
            for j in range(total_vertices):
                # verifica se passar por k melhora o caminho de i até j
                if distancias[i][j] > distancias[i][k] + distancias[k][j]:
                    # atualiza a menor distância
                    distancias[i][j] = distancias[i][k] + distancias[k][j]

                    # atualiza o predecessor conforme o pseudocódigo
                    predecessor[i][j] = predecessor[k][j]

    # retorna a matriz de distâncias e predecessores
    return distancias, predecessor

# -----------------------------
# Reconstrução de Caminho (prev por vértice)
# -----------------------------
def reconstruir_caminho_prev(prev, s, t):
    # caso trivial: origem e destino são o mesmo vértice
    if s == t:
        return [s]

    # se não existe predecessor para o destino, não existe caminho
    if prev[t] is None:
        return []

    # caminho irá armazenar o trajeto ao contrário (de t até s)
    caminho = []

    # começa pelo destino e volta usando o vetor de predecessores
    vertice_atual = t

    # proteção contra loop infinito caso o vetor prev esteja inconsistente
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

        # se em algum ponto não existir predecessor, não há caminho válido
        if vertice_atual is None:
            return []

        # incrementa contador de segurança
        passos += 1
        if passos > max_passos:
            return []  # prev contém ciclo/inconsistência

    # inverte para ficar na ordem correta: s -> ... -> t
    caminho.reverse()
    return caminho


# -----------------------------
# Reconstrução de Caminho (prev por par i->j do Floyd-Warshall)
# -----------------------------
def reconstruir_caminho_floyd(prev, s, t):
    # se não existe predecessor para o par (s, t), não existe caminho
    if prev[s][t] is None:
        return []

    # caminho irá armazenar o trajeto ao contrário (de t até s)
    caminho = []

    # começa pelo destino e volta usando predecessor[s][*]
    vertice_atual = t

    # proteção contra loop infinito caso a matriz prev esteja inconsistente
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

        # incrementa contador de segurança
        passos += 1
        if passos > max_passos:
            return []  # prev contém ciclo/inconsistência

    # inverte para ficar na ordem correta: s -> ... -> t
    caminho.reverse()
    return caminho
