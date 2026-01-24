
# cria um grafo a partir de um arquivo:
def leitura(nomeArquivo):
    arquivo = open(nomeArquivo)
    linha = arquivo.readline()
    vLinha = linha.split(" ")
    numVertices = int(vLinha[0])
    numArestas = int(vLinha[1])

    # grafo = MatrizAdjacencias(numVertices)
    grafo = ListaAdjacencias(numVertices)

    for i in range(numArestas):
        linha = arquivo.readline()
        vLinha = linha.split(" ")
        origem = int(vLinha[0])
        destino = int(vLinha[1])
        peso = int(vLinha[2])
        grafo.addAresta(origem, destino, peso)

    return grafo


def dfsRecursivo(grafo, R, visitado, u):
    visitado[u] = True
    R.append(u)

    for (v, peso) in grafo.vizinhos(u):
        if not visitado[v]:
            dfsRecursivo(grafo, R, visitado, v)


def dfs(grafo, s):
    R = []
    visitado = [False] * grafo.numVertices
    dfsRecursivo(grafo, R, visitado, s)
    return R


def dfsIterativo(grafo, s):
    R = []
    pilha = []
    visitado = [False] * grafo.numVertices
    pilha.append(s)
    visitado[s] = True

    while len(pilha) > 0:
        u = pilha.pop()
        R.append(u)
        for (v, peso) in grafo.vizinhos(u):
            if not visitado[v]:
                pilha.append(v)
                visitado[v] = True

    return R
