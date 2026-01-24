# main_benchmark_v2.py
# ------------------------------------------------------------------------------------
# Benchmark TP1 (V2) - SEM LIMITE DE TEMPO:
# - Para cada mapa em uma pasta, executa 10 vezes cada algoritmo
# - Calcula média do tempo e do custo
# - Executa também o Dijkstra Otimizado
# - Não usa timeout e não usa multiprocessing (mais iniciante e direto)
# - Gera log.txt com o mesmo conteúdo do console
# - Tabela 1 final consolidada (uma linha por mapa)
# - Resumo por mapa contém nome do mapa no título (facilita leitura)
# ------------------------------------------------------------------------------------

import os
import sys
import time

from Mapa import carregar_mapa

from Algoritmos import (
    dijkstra_iniciante,
    dijkstra_iniciante_otimizado,
    bellman_ford_iniciante,
    floyd_warshall_iniciante
)

INF = float("inf")

# -----------------------------
# LOG (console + arquivo)
# -----------------------------
log_file = None

def print_log(texto=""):
    print(texto)
    if log_file is not None:
        log_file.write(texto + "\n")


# -----------------------------
# Funções auxiliares
# -----------------------------
def listar_mapas(pasta_mapas):
    mapas_encontrados = []

    for nome_arquivo in os.listdir(pasta_mapas):
        caminho_arquivo = os.path.join(pasta_mapas, nome_arquivo)
        if os.path.isfile(caminho_arquivo) and nome_arquivo.lower().endswith(".txt"):
            mapas_encontrados.append(caminho_arquivo)

    mapas_encontrados.sort()
    return mapas_encontrados


def media(valores):
    if not valores:
        return None
    return sum(valores) / len(valores)


def fmt_tempo(valor):
    if valor is None:
        return "-"
    return f"{valor:.6f}"


def fmt_custo(valor):
    if valor is None:
        return "-"
    if valor == INF:
        return "INF"
    if isinstance(valor, float) and valor.is_integer():
        return str(int(valor))
    return str(valor)


def repetir_char(c, n):
    return c * n


def print_cabecalho_mapa(nome_mapa):
    print_log("")
    print_log(repetir_char("=", 110))
    print_log(f"MAPA: {nome_mapa}")
    print_log(repetir_char("=", 110))


def print_tabela_rodadas(nome_algoritmo, tempos_execucao, custos_execucao):
    # Tabela: Rodada | Tempo | Custo
    print_log("")
    print_log(f"[{nome_algoritmo}] Resultados Por Rodada")
    print_log(repetir_char("-", 110))
    print_log(f"{'Rodada':<10} | {'Tempo (s)':<12} | {'Custo':<12}")
    print_log(repetir_char("-", 110))

    for i in range(len(tempos_execucao)):
        rodada = i + 1
        tempo_str = f"{tempos_execucao[i]:.6f}"
        custo_str = fmt_custo(custos_execucao[i])
        print_log(f"{rodada:<10} | {tempo_str:<12} | {custo_str:<12}")

    print_log(repetir_char("-", 110))


def print_resumo_mapa(nome_mapa, resultados):
    # Resumo em tabela: Algoritmo | Tempo Médio | Custo Médio
    print_log("")
    print_log(f"[Resumo Do Mapa] {nome_mapa} — Médias (10 execuções)")
    print_log(repetir_char("-", 110))
    print_log(f"{'Algoritmo':<25} | {'Tempo Médio (s)':<18} | {'Custo Médio':<15}")
    print_log(repetir_char("-", 110))

    ordem = ["Dijkstra", "Dijkstra Otimizado", "Bellman-Ford", "Floyd-Warshall"]
    for alg in ordem:
        tempo_medio, custo_medio = resultados[alg]
        print_log(f"{alg:<25} | {fmt_tempo(tempo_medio):<18} | {fmt_custo(custo_medio):<15}")

    print_log(repetir_char("-", 110))


def print_tabela1_final(linhas_tabela):
    # imprime a "Tabela 1" final consolidada (uma linha por mapa)
    print_log("")
    print_log(repetir_char("=", 150))
    print_log("TABELA 1 — Comparação Entre Algoritmos De Caminhos Mínimos (Médias Em 10 Execuções)")
    print_log(repetir_char("=", 150))
    print_log(
        f"{'Grafo':<20} | "
        f"{'Dijkstra T.médio(s)':<18} | {'Dijkstra Custo médio':<20} | "
        f"{'Dijkstra Otim. T.médio(s)':<24} | {'Dijkstra Otim. Custo médio':<28} | "
        f"{'Bellman-Ford T.médio(s)':<22} | {'Bellman-Ford Custo médio':<24} | "
        f"{'Floyd-Warshall T.médio(s)':<24} | {'Floyd-Warshall Custo médio':<26}"
    )
    print_log(repetir_char("-", 150))

    for linha in linhas_tabela:
        print_log(linha)

    print_log(repetir_char("=", 150))


# -----------------------------
# Execução SEM timeout (rodando direto)
# -----------------------------
def executar_algoritmo_sem_timeout(nome_algoritmo, grafo, inicio, fim):
    inicio_tempo = time.perf_counter()

    if nome_algoritmo == "Dijkstra":
        distancias, _prev = dijkstra_iniciante(grafo, inicio)
        custo_total = distancias[fim]

    elif nome_algoritmo == "Dijkstra Otimizado":
        distancias, _prev = dijkstra_iniciante_otimizado(grafo, inicio)
        custo_total = distancias[fim]

    elif nome_algoritmo == "Bellman-Ford":
        distancias, _prev = bellman_ford_iniciante(grafo, inicio)
        custo_total = distancias[fim]

    elif nome_algoritmo == "Floyd-Warshall":
        distancias, _prev = floyd_warshall_iniciante(grafo)
        custo_total = distancias[inicio][fim]

    else:
        raise ValueError("Algoritmo inválido")

    fim_tempo = time.perf_counter()
    tempo_execucao = fim_tempo - inicio_tempo

    return tempo_execucao, custo_total


# -----------------------------
# Benchmark por mapa/algoritmo
# -----------------------------
def benchmark_mapa_algoritmo(nome_algoritmo, grafo, inicio, fim, repeticoes):
    tempos_execucao = []
    custos_execucao = []

    for _ in range(repeticoes):
        tempo_execucao, custo_total = executar_algoritmo_sem_timeout(nome_algoritmo, grafo, inicio, fim)
        tempos_execucao.append(tempo_execucao)
        custos_execucao.append(custo_total)

    tempo_medio = media(tempos_execucao)

    # custo médio: se qualquer execução for INF, mantém INF
    if any(c == INF for c in custos_execucao):
        custo_medio = INF
    else:
        custo_medio = media(custos_execucao)

    return tempo_medio, custo_medio, tempos_execucao, custos_execucao


# -----------------------------
# MAIN
# -----------------------------
def main():
    global log_file

    # uso: python main_benchmark_v2.py <pasta_mapas>
    if len(sys.argv) != 2:
        print("Uso: python main_benchmark_v2.py <pasta_mapas>")
        return

    # abre log
    log_file = open("log.txt", "w", encoding="utf-8")

    pasta_mapas = sys.argv[1]
    if not os.path.isdir(pasta_mapas):
        print_log("Pasta inválida: " + str(pasta_mapas))
        log_file.close()
        return

    mapas = listar_mapas(pasta_mapas)
    if not mapas:
        print_log("Nenhum mapa .txt encontrado em: " + str(pasta_mapas))
        log_file.close()
        return

    repeticoes = 10

    algoritmos = ["Dijkstra", "Dijkstra Otimizado", "Bellman-Ford", "Floyd-Warshall"]

    # guarda linhas para a Tabela 1 final (uma por mapa)
    linhas_tabela = []

    for caminho_mapa in mapas:
        nome_mapa = os.path.basename(caminho_mapa)
        print_cabecalho_mapa(nome_mapa)

        # carrega mapa e cria grafo (fora do tempo do algoritmo, igual no main)
        grid, linhas, colunas, inicio, fim, grafo = carregar_mapa(caminho_mapa)

        resultados = {}

        for alg in algoritmos:
            print_log(f"Executando {alg} (10 rodadas, sem timeout)...")

            tempo_medio, custo_medio, tempos_execucao, custos_execucao = benchmark_mapa_algoritmo(
                alg, grafo, inicio, fim, repeticoes
            )

            # tabela das rodadas
            print_tabela_rodadas(alg, tempos_execucao, custos_execucao)

            # média do algoritmo
            print_log(f"MÉDIA {alg}: Tempo = {fmt_tempo(tempo_medio)} s | Custo = {fmt_custo(custo_medio)}")

            resultados[alg] = (tempo_medio, custo_medio)

        # resumo do mapa com nome do mapa no título
        print_resumo_mapa(nome_mapa, resultados)

        # prepara a linha do mapa para a Tabela 1 final
        d_t, d_c = resultados["Dijkstra"]
        do_t, do_c = resultados["Dijkstra Otimizado"]
        b_t, b_c = resultados["Bellman-Ford"]
        f_t, f_c = resultados["Floyd-Warshall"]

        linha_tabela = (
            f"{nome_mapa:<20} | "
            f"{fmt_tempo(d_t):<18} | {fmt_custo(d_c):<20} | "
            f"{fmt_tempo(do_t):<24} | {fmt_custo(do_c):<28} | "
            f"{fmt_tempo(b_t):<22} | {fmt_custo(b_c):<24} | "
            f"{fmt_tempo(f_t):<24} | {fmt_custo(f_c):<26}"
        )

        linhas_tabela.append(linha_tabela)

    # imprime a Tabela 1 final consolidada
    print_tabela1_final(linhas_tabela)

    print_log("")
    print_log(repetir_char("=", 110))
    print_log("FIM DO BENCHMARK V2 (SEM TIMEOUT)")
    print_log(repetir_char("=", 110))

    log_file.close()


if __name__ == "__main__":
    main()
