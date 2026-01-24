# mapa.py
# ------------------------------------------------------------------------------------
# Responsável por carregar o mapa, converter células em vértices e gerar o grafo final
# ------------------------------------------------------------------------------------

INF = float("inf")  # não utilizado aqui, mantido para consistência com o restante do projeto

def custo_terreno(c):
    # Retorna o custo para ENTRAR em uma célula do tipo 'c' (conforme especificação)
    if c == 'W': return 5  # Water
    if c == 'S': return 3  # Sand
    if c == 'G': return 1  # Ground
    if c in ['I', 'F']: return 0  # Início e Fim não adicionam custo
    raise ValueError(f"Terreno inválido: {c}")  # qualquer símbolo fora do esperado

def carregar_mapa(nome_arquivo):
    # grid será uma matriz de caracteres (lista de listas)
    grid = []

    # lê o arquivo linha a linha
    with open(nome_arquivo, 'r') as arquivo:
        for linha in arquivo:
            # remove espaços e quebras de linha
            linha = linha.strip().replace(" ", "")

            # ignora linhas vazias
            if linha:
                # converte a string em lista de caracteres
                grid.append(list(linha))

    # validação básica: mapa não pode ser vazio
    if not grid:
        raise ValueError("Mapa vazio ou arquivo inválido.")

    # dimensões do grid
    total_linhas = len(grid)
    total_colunas = len(grid[0])

    # valida se todas as linhas têm o mesmo tamanho (evita index error)
    for linha in grid:
        if len(linha) != total_colunas:
            raise ValueError("Mapa inválido: linhas com tamanhos diferentes.")

    # localiza posições de início (I) e fim (F) e valida unicidade
    indice_inicio = None
    indice_fim = None
    quantidade_inicio = 0
    quantidade_fim = 0

    for i in range(total_linhas):
        for j in range(total_colunas):
            if grid[i][j] == 'I':
                quantidade_inicio += 1
                indice_inicio = i * total_colunas + j  # converte (i,j) para índice de vértice
            elif grid[i][j] == 'F':
                quantidade_fim += 1
                indice_fim = i * total_colunas + j  # converte (i,j) para índice de vértice

    # exige exatamente um I e um F (conforme mensagem do seu erro)
    if quantidade_inicio != 1 or quantidade_fim != 1:
        raise ValueError("Mapa deve conter exatamente um I e um F.")

    # importa a estrutura de grafo definida pelo professor
    from Grafo import ListaAdjacencias

    # cria grafo com um vértice para cada célula do grid
    grafo = ListaAdjacencias(total_linhas * total_colunas)

    # movimentos permitidos: cima, baixo, esquerda, direita (4-vizinhos)
    direcoes_movimento = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # percorre todas as células para criar arestas
    for i in range(total_linhas):
        for j in range(total_colunas):
            # parede não vira vértice "utilizável" (sem arestas saindo)
            if grid[i][j] == '#':
                continue

            # vértice atual u (célula i,j)
            u = i * total_colunas + j

            # tenta mover nas 4 direções
            for di, dj in direcoes_movimento:
                proxima_linha = i + di
                proxima_coluna = j + dj

                # verifica se está dentro dos limites do grid
                if 0 <= proxima_linha < total_linhas and 0 <= proxima_coluna < total_colunas:
                    # não entra em parede
                    if grid[proxima_linha][proxima_coluna] != '#':
                        # vértice de destino v
                        v = proxima_linha * total_colunas + proxima_coluna

                        # custo para entrar na célula de destino
                        peso = custo_terreno(grid[proxima_linha][proxima_coluna])

                        # adiciona aresta direcionada u -> v com peso
                        grafo.addAresta(u, v, peso)

    # retorna o grid e metadados para uso pelo restante do sistema
    return grid, total_linhas, total_colunas, indice_inicio, indice_fim, grafo


def marcar_caminho(grid, linhas, colunas, caminho):
    # cria uma cópia do grid para não alterar o original
    grid_marcado = [linha[:] for linha in grid]

    # para cada vértice do caminho, converte para (linha, coluna) e marca '*'
    for vertice in caminho:
        linha = vertice // colunas
        coluna = vertice % colunas

        # não sobrescreve início e fim
        if grid_marcado[linha][coluna] not in ['I', 'F']:
            grid_marcado[linha][coluna] = '*'

    # retorna o novo grid com o caminho marcado
    return grid_marcado


def salvar_mapa(grid, nome_arquivo):
    # grava o grid no arquivo, uma linha por vez
    with open(nome_arquivo, 'w') as arquivo:
        for linha in grid:
            arquivo.write("".join(linha) + "\n")
