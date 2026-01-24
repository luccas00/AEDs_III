# main.py
# ------------------------------------------------------------------------------------
# Ponto de entrada do programa. Executa Dijkstra, Bellman-Ford e Floyd-Warshall.
# ------------------------------------------------------------------------------------

import sys

from Mapa import carregar_mapa, marcar_caminho, salvar_mapa
from Algoritmos import (
    dijkstra,
    bellman_ford,
    floyd_warshall,
    reconstruir_caminho_prev,
    reconstruir_caminho_floyd
)

INF = float("inf")

# Função padrão para execução dos algoritmos
def executar_algoritmo(nome, func_execucao, grid, linhas, colunas, inicio, fim, grafo, arquivo_saida):
    import time
    inicio_tempo = time.perf_counter()
    resultado = func_execucao(grafo, inicio)
    fim_tempo = time.perf_counter()

    if nome == "Floyd-Warshall":
        dist, prev = resultado
        custo = dist[inicio][fim]
        caminho = reconstruir_caminho_floyd(prev, inicio, fim)
    else:
        dist, prev = resultado
        custo = dist[fim]
        caminho = reconstruir_caminho_prev(prev, inicio, fim)

    if custo == INF:
        print(f"----- {nome} -----")
        print("Nao existe caminho entre I e F")
        print("------------------------------")
        return

    grid_saida = marcar_caminho(grid, linhas, colunas, caminho)
    salvar_mapa(grid_saida, arquivo_saida)

    print("-------------------------------------------------")
    print(f"Algoritmo de {nome}:")
    print(f"Custo: {custo}")
    print(f"Tempo execucao: {fim_tempo - inicio_tempo:.6f} s")
    print("-------------------------------------------------")


# Wrapper para Floyd (mantém assinatura uniforme)
def exec_floyd_wrapper(grafo, s):
    return floyd_warshall(grafo)


def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py <arquivo_mapa>")
        return

    nome_mapa = sys.argv[1]

    grid, linhas, colunas, inicio, fim, grafo = carregar_mapa(nome_mapa)

    executar_algoritmo("Dijkstra", dijkstra, grid, linhas, colunas, inicio, fim, grafo, "saida_dijkstra.txt")
    executar_algoritmo("Bellman-Ford", bellman_ford, grid, linhas, colunas, inicio, fim, grafo, "saida_bellman_ford.txt")
    executar_algoritmo("Floyd-Warshall", exec_floyd_wrapper, grid, linhas, colunas, inicio, fim, grafo, "saida_floyd_warshall.txt")


if __name__ == "__main__":
    main()
