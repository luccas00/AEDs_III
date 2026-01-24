# main_v2.py
# ------------------------------------------------------------------------------------
# Ponto de entrada (V2). Executa:
# - Dijkstra (versão iniciante)
# - Dijkstra Otimizado (versão iniciante com quebra para nós desconexos)
# - Bellman-Ford (versão iniciante)
# - Floyd-Warshall (versão iniciante)
# Gera arquivos de saída e imprime custo + tempo no terminal.
# ------------------------------------------------------------------------------------

import sys
import time

from Mapa import carregar_mapa, marcar_caminho, salvar_mapa

from Algoritmos import (
    dijkstra_iniciante,
    dijkstra_iniciante_otimizado,
    bellman_ford_iniciante,
    floyd_warshall_iniciante,
    reconstruir_caminho_prev,
    reconstruir_caminho_floyd
)

INF = float("inf")  # usado para identificar ausência de caminho


def executar_algoritmo(nome_algoritmo, func_execucao, grid, linhas, colunas, inicio, fim, grafo, arquivo_saida):
    # mede tempo de execução do algoritmo (somente o cálculo do caminho mínimo)
    inicio_tempo = time.perf_counter()
    resultado = func_execucao(grafo, inicio)
    fim_tempo = time.perf_counter()

    # separa as estruturas retornadas
    distancias, predecessor = resultado

    # Floyd-Warshall usa matriz de distâncias
    if nome_algoritmo == "Floyd-Warshall":
        custo_total = distancias[inicio][fim]
        caminho = reconstruir_caminho_floyd(predecessor, inicio, fim)
    else:
        # Dijkstra / Bellman-Ford usam vetor de distâncias
        custo_total = distancias[fim]
        caminho = reconstruir_caminho_prev(predecessor, inicio, fim)

    # se o custo é infinito, não existe caminho entre I e F
    if custo_total == INF:
        print("-------------------------------------------------")
        print(f"Algoritmo de {nome_algoritmo}:")
        print("Nao existe caminho entre I e F")
        print(f"Tempo execucao: {fim_tempo - inicio_tempo:.6f} s")
        print("-------------------------------------------------")
        return

    # marca caminho no grid e salva em arquivo
    grid_saida = marcar_caminho(grid, linhas, colunas, caminho)
    salvar_mapa(grid_saida, arquivo_saida)

    # imprime relatório
    print("-------------------------------------------------")
    print(f"Algoritmo de {nome_algoritmo}:")
    print(f"Custo: {custo_total}")
    print(f"Tempo execucao: {fim_tempo - inicio_tempo:.6f} s")
    print("-------------------------------------------------")


# Wrapper para Floyd-Warshall para manter assinatura (grafo, origem)
def exec_floyd_wrapper(grafo, origem):
    return floyd_warshall_iniciante(grafo)


def main():
    # uso: python main_v2.py <arquivo_mapa>
    if len(sys.argv) != 2:
        print("Uso: python main_v2.py <arquivo_mapa>")
        return

    nome_mapa = sys.argv[1]

    # carrega mapa e gera grafo
    grid, linhas, colunas, inicio, fim, grafo = carregar_mapa(nome_mapa)

    # executa algoritmos
    executar_algoritmo("Dijkstra", dijkstra_iniciante, grid, linhas, colunas, inicio, fim, grafo, "saida_dijkstra.txt")
    executar_algoritmo("Dijkstra Otimizado", dijkstra_iniciante_otimizado, grid, linhas, colunas, inicio, fim, grafo, "saida_dijkstra_otimizado.txt")
    executar_algoritmo("Bellman-Ford", bellman_ford_iniciante, grid, linhas, colunas, inicio, fim, grafo, "saida_bellman_ford.txt")
    executar_algoritmo("Floyd-Warshall", exec_floyd_wrapper, grid, linhas, colunas, inicio, fim, grafo, "saida_floyd_warshall.txt")


if __name__ == "__main__":
    main()
