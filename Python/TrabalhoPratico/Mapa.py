# mapa.py
# ------------------------------------------------------------------------------------
# Responsável por carregar o mapa, converter células em vértices e gerar o grafo final
# ------------------------------------------------------------------------------------

INF = float("inf")

def custo_terreno(c):
    # Custo conforme especificação do trabalho
    if c == 'W': return 5
    if c == 'S': return 3
    if c == 'G': return 1
    if c in ['I', 'F']: return 0
    raise ValueError(f"Terreno inválido: {c}")

def carregar_mapa(nome_arquivo):
    grid = []

    with open(nome_arquivo, 'r') as f:
        for linha in f:
            linha = linha.strip().replace(" ", "")
            if linha:
                grid.append(list(linha))

    linhas = len(grid)
    colunas = len(grid[0])

    # Identifica I e F
    inicio = fim = None
    for i in range(linhas):
        for j in range(colunas):
            if grid[i][j] == 'I':
                inicio = i * colunas + j
            elif grid[i][j] == 'F':
                fim = i * colunas + j

    if inicio is None or fim is None:
        raise ValueError("Mapa deve conter exatamente um I e um F.")

    # Gera o grafo como lista de adjacências
    from Grafo import ListaAdjacencias
    grafo = ListaAdjacencias(linhas * colunas)

    # Direções de movimento (4-vizinhos)
    direcoes = [(-1,0),(1,0),(0,-1),(0,1)]

    for i in range(linhas):
        for j in range(colunas):
            if grid[i][j] == '#':
                continue

            u = i * colunas + j

            for di, dj in direcoes:
                ni, nj = i + di, j + dj
                if 0 <= ni < linhas and 0 <= nj < colunas:
                    if grid[ni][nj] != '#':
                        v = ni * colunas + nj
                        peso = custo_terreno(grid[ni][nj])
                        grafo.addAresta(u, v, peso)

    return grid, linhas, colunas, inicio, fim, grafo


def marcar_caminho(grid, linhas, colunas, caminho):
    novo = [linha[:] for linha in grid]

    for v in caminho:
        r = v // colunas
        c = v % colunas
        if novo[r][c] not in ['I', 'F']:
            novo[r][c] = '*'

    return novo

def salvar_mapa(grid, nome_arquivo):
    with open(nome_arquivo, 'w') as f:
        for linha in grid:
            f.write("".join(linha) + "\n")
