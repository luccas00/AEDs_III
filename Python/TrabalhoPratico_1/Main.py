
# ------------------------------------------------------------------------------------
# Ponto de entrada do programa. Executa Dijkstra, Bellman-Ford e Floyd-Warshall.
# ------------------------------------------------------------------------------------

import sys
import time

from Mapa import carregar_mapa, marcar_caminho, salvar_mapa

from Algoritmos import (
    dijkstra as dijkstra,
    bellman_ford as bellman_ford,
    floyd_warshall as floyd_warshall,
    reconstruir_caminho_prev,
    reconstruir_caminho_floyd
)

INF = float("inf")

def executar_algoritmo(nome_algoritmo, func_execucao, grid, linhas, colunas, inicio, fim, grafo, arquivo_saida):
    # mede tempo de execução do algoritmo
    inicio_tempo = time.perf_counter()
    resultado = func_execucao(grafo, inicio)
    fim_tempo = time.perf_counter()

    # separa as estruturas retornadas (distâncias e predecessores)
    distancias, predecessor = resultado

    # tratamento específico do Floyd-Warshall (distância é matriz)
    if nome_algoritmo == "Floyd-Warshall":
        custo_total = distancias[inicio][fim]
        caminho = reconstruir_caminho_floyd(predecessor, inicio, fim)
    else:
        # Dijkstra e Bellman-Ford retornam vetor de distâncias
        custo_total = distancias[fim]
        caminho = reconstruir_caminho_prev(predecessor, inicio, fim)

    # se o custo é infinito, não existe caminho entre I e F
    if custo_total == INF:
        print(f"----- {nome_algoritmo} -----")
        print("Nao existe caminho entre I e F")
        print("------------------------------")
        return

    # marca o caminho no grid e salva no arquivo de saída
    grid_saida = marcar_caminho(grid, linhas, colunas, caminho)
    salvar_mapa(grid_saida, arquivo_saida)

    # imprime relatório de execução
    print("-------------------------------------------------")
    print(f"Algoritmo de {nome_algoritmo}:")
    print(f"Custo: {custo_total}")
    print(f"Tempo execucao: {fim_tempo - inicio_tempo:.6f} s")
    print("-------------------------------------------------")


# Wrapper para o Floyd-Warshall para manter assinatura (grafo, origem) igual aos outros
def exec_floyd_wrapper(grafo, origem):
    return floyd_warshall(grafo)


def main():
    # valida parâmetros: precisa de 1 argumento (arquivo de mapa)
    if len(sys.argv) != 2:
        print("Uso: python main.py <arquivo_mapa>")
        return

    # nome do arquivo do mapa recebido pela linha de comando
    nome_mapa = sys.argv[1]

    # carrega o mapa e gera o grafo
    grid, linhas, colunas, inicio, fim, grafo = carregar_mapa(nome_mapa)

    # executa cada algoritmo e gera um arquivo de saída com o caminho marcado
    executar_algoritmo("Dijkstra", dijkstra, grid, linhas, colunas, inicio, fim, grafo, "saida_dijkstra.txt")
    executar_algoritmo("Bellman-Ford", bellman_ford, grid, linhas, colunas, inicio, fim, grafo, "saida_bellman_ford.txt")
    executar_algoritmo("Floyd-Warshall", exec_floyd_wrapper, grid, linhas, colunas, inicio, fim, grafo, "saida_floyd_warshall.txt")

if __name__ == "__main__":
    main()
