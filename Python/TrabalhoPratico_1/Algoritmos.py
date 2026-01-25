
# -----------------------------------------------------------------------------------------
# Implementação dos algoritmos de Dijkstra, Bellman-Ford e Floyd-Warshall conforme pseudocódigo
# -----------------------------------------------------------------------------------------

INF = float("inf")  # representa "infinito"

def dijkstra(grafo, origem):
    # total de vértices do grafo (assumindo índices 0..V-1)
    total_vertices = grafo.numVertices

    # distancias[i] = melhor distância conhecida da origem até o vértice i
    distancias = [INF] * total_vertices

    # predecessor[i] = vértice anterior no caminho mínimo até i (ou None se não definido)
    predecessor = [None] * total_vertices

    # distância da origem para ela mesma é 0
    distancias[origem] = 0

    # predecessor da origem é ela mesma
    predecessor[origem] = origem

    # abertos = conjunto O (vértices ainda não "fechados")
    abertos = set(range(total_vertices))

    # fechados = conjunto C (vértices já processados/finalizados)
    fechados = set()

    # enquanto C != V
    while fechados != set(range(total_vertices)):
        # escolhe um vértice qualquer de "abertos" como candidato inicial
        vertice_atual = next(iter(abertos))

        # menor_distancia guarda a menor dist encontrada dentro do conjunto "abertos"
        menor_distancia = distancias[vertice_atual]

        # varre todos os vértices em "abertos" para achar aquele com menor dist
        for v in abertos:
            if distancias[v] < menor_distancia:
                menor_distancia = distancias[v]
                vertice_atual = v

        # adiciona o vértice escolhido ao conjunto "fechados"
        fechados.add(vertice_atual)

        # remove o vértice escolhido do conjunto "abertos"
        abertos.remove(vertice_atual)

        # percorre cada vizinho do vértice_atual
        # grafo.vizinhos(u) deve devolver pares (vizinho, peso_da_aresta)
        for (vizinho, peso) in grafo.vizinhos(vertice_atual):
            # só considera vizinho que ainda NÃO está fechado
            if vizinho not in fechados:
                # calcula a distância alternativa indo origem -> ... -> vertice_atual -> vizinho
                distancia_alternativa = distancias[vertice_atual] + peso

                # se essa rota for melhor do que a distância atual do vizinho 
                if distancias[vizinho] > distancia_alternativa:
                    # atualiza a melhor distância do vizinho)
                    distancias[vizinho] = distancia_alternativa

                    # registra que o predecessor do vizinho no melhor caminho é vertice_atual
                    predecessor[vizinho] = vertice_atual

    # retorna as listas dist e prev
    return distancias, predecessor

def bellman_ford(grafo, origem):
    # quantidade total de vértices do grafo
    total_vertices = grafo.numVertices

    # distancias[i] = menor distância conhecida da origem até o vértice i
    distancias = [INF] * total_vertices

    # predecessor[i] = vértice anterior no caminho mínimo até i
    predecessor = [None] * total_vertices

    # distância da origem para ela mesma é zero
    distancias[origem] = 0

    # predecessor da origem é ela mesma
    predecessor[origem] = origem

    # repete o processo no máximo |V| - 1 vezes
    for _ in range(total_vertices - 1):
        # indica se alguma distância foi atualizada nesta iteração
        houve_atualizacao = False

        # percorre todos os vértices u do grafo
        for u in range(total_vertices):
            # percorre todos os vizinhos v de u
            # grafo.vizinhos(u) retorna pares (vizinho, peso_da_aresta)
            for (v, peso) in grafo.vizinhos(u):
                # verifica se o caminho passando por u melhora a distância até v
                if distancias[v] > distancias[u] + peso:
                    # atualiza a melhor distância até v
                    distancias[v] = distancias[u] + peso

                    # registra u como predecessor de v no caminho mínimo
                    predecessor[v] = u

                    # marca que houve atualização nesta iteração
                    houve_atualizacao = True

        # se nenhuma distância foi atualizada, o algoritmo pode parar
        if not houve_atualizacao:
            break

    # retorna as distâncias mínimas e os predecessores
    return distancias, predecessor

def floyd_warshall(grafo):
    # número total de vértices do grafo
    total_vertices = grafo.numVertices

    # distancias[i][j] = menor distância conhecida de i até j
    distancias = [[INF] * total_vertices for _ in range(total_vertices)]

    # predecessor[i][j] = vértice anterior a j no melhor caminho de i até j
    predecessor = [[None] * total_vertices for _ in range(total_vertices)]

    # inicialização das matrizes dist e predecessor
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

    # laços do Floyd-Warshall
    # k é o vértice intermediário
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
# Reconstrução de Caminho do Floyd-Warshall)
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
            return []  # prev contém ciclo

    # inverte para ficar na ordem correta
    caminho.reverse()
    return caminho
