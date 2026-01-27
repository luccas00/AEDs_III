
# ------------------------------------------------------------------------------------
# Benchmark - COM LIMITE DE TEMPO:
# - Para cada mapa em uma pasta, executa 10 vezes cada algoritmo
# - Calcula média do tempo e do custo
# - Gera log.txt com o mesmo conteúdo do console
# ------------------------------------------------------------------------------------

import os
import sys
import time
import multiprocessing as mp

from Mapa import carregar_mapa
from Algoritmos import (
    dijkstra as dijkstra,
    bellman_ford as bellman_ford,
    floyd_warshall as floyd_warshall
)

INF = float("inf")

# -----------------------------
# LOG (console + arquivo)
# -----------------------------
log_file = None  # arquivo global de log (aberto no main)

def print_log(texto=""):
    # imprime no console
    print(texto)

    # escreve no arquivo de log, se estiver aberto
    if log_file is not None:
        log_file.write(texto + "\n")


# -----------------------------
# Funções auxiliares (Mapas / Médias / Formatação)
# -----------------------------
def listar_mapas(pasta_mapas):
    # lista todos os arquivos .txt dentro da pasta de mapas
    mapas_encontrados = []

    for nome_arquivo in os.listdir(pasta_mapas):
        caminho_arquivo = os.path.join(pasta_mapas, nome_arquivo)

        # adiciona apenas arquivos .txt
        if os.path.isfile(caminho_arquivo) and nome_arquivo.lower().endswith(".txt"):
            mapas_encontrados.append(caminho_arquivo)

    # ordena para manter execução consistente (map_10x10, map_10x20, etc.)
    mapas_encontrados.sort()
    return mapas_encontrados


def media(valores):
    # calcula média aritmética simples
    if not valores:
        return None
    return sum(valores) / len(valores)


def fmt_tempo(valor):
    # formata o tempo para impressão
    if valor == "TEMPO LIMITE":
        return "TEMPO LIMITE"
    if valor is None:
        return "-"
    return f"{valor:.6f}"


def fmt_custo(valor):
    # formata o custo para impressão
    if valor == "TEMPO LIMITE":
        return "TEMPO LIMITE"
    if valor is None:
        return "-"
    if valor == INF:
        return "INF"

    if isinstance(valor, float) and valor.is_integer():
        return str(int(valor))

    return str(valor)


def repetir_char(c, n):
    # cria uma linha repetida para separação visual
    return c * n


def print_cabecalho_mapa(nome_mapa):
    # cabeçalho do bloco do mapa
    print_log("")
    print_log(repetir_char("=", 90))
    print_log(f"MAPA: {nome_mapa}")
    print_log(repetir_char("=", 90))


def print_tabela_rodadas(nome_algoritmo, tempos_execucao, custos_execucao, status_lista):
    # imprime tabela das rodadas (Rodada | Tempo | Custo | Status)
    print_log("")
    print_log(f"[{nome_algoritmo}] Resultados Por Rodada")
    print_log(repetir_char("-", 90))
    print_log(f"{'Rodada':<10} | {'Tempo (s)':<12} | {'Custo':<12} | {'Status':<20}")
    print_log(repetir_char("-", 90))

    total_rodadas = len(status_lista)

    # tempos_execucao/custos_execucao só têm itens para status OK
    indice_ok = 0

    for i in range(total_rodadas):
        rodada = i + 1
        status = status_lista[i]

        if status == "OK":
            tempo_str = f"{tempos_execucao[indice_ok]:.6f}"
            custo_str = fmt_custo(custos_execucao[indice_ok])
            indice_ok += 1
        elif status == "TEMPO LIMITE":
            tempo_str = "TEMPO LIMITE"
            custo_str = "TEMPO LIMITE"
        else:
            tempo_str = "-"
            custo_str = "-"

        print_log(f"{rodada:<10} | {tempo_str:<12} | {custo_str:<12} | {status:<20}")

    print_log(repetir_char("-", 90))


def print_resumo_mapa(nome_mapa, resultados):
    # imprime resumo do mapa em formato de tabela (médias)
    print_log("")
    print_log(f"[Resumo Do Mapa] {nome_mapa} — Médias (10 execuções)")
    print_log(repetir_char("-", 90))
    print_log(f"{'Algoritmo':<20} | {'Tempo Médio (s)':<18} | {'Custo Médio':<15}")
    print_log(repetir_char("-", 90))

    for alg in ["Dijkstra", "Bellman-Ford", "Floyd-Warshall"]:
        tempo_medio, custo_medio = resultados[alg]
        print_log(f"{alg:<20} | {fmt_tempo(tempo_medio):<18} | {fmt_custo(custo_medio):<15}")

    print_log(repetir_char("-", 90))


def print_tabela_final(linhas_tabela):
    # imprime a "Tabela" final consolidada (uma linha por mapa)
    print_log("")
    print_log(repetir_char("=", 130))
    print_log("TABELA — Comparação Entre Algoritmos De Caminhos Mínimos (Médias Em 10 Execuções)")
    print_log(repetir_char("=", 130))
    print_log(
        f"{'Grafo':<20} | "
        f"{'Dijkstra T.médio(s)':<18} | {'Dijkstra Custo médio':<20} | "
        f"{'Bellman-Ford T.médio(s)':<22} | {'Bellman-Ford Custo médio':<24} | "
        f"{'Floyd-Warshall T.médio(s)':<24} | {'Floyd-Warshall Custo médio':<26}"
    )
    print_log(repetir_char("-", 130))

    for linha in linhas_tabela:
        print_log(linha)

    print_log(repetir_char("=", 130))


# -----------------------------
# Execução do algoritmo em processo separado
# (necessário para aplicar timeout por execução)
# -----------------------------
def _worker_algoritmo(nome_algoritmo, grafo, vertice_inicio, vertice_fim, fila_resultado):
    try:
        # marca o tempo inicial (somente do algoritmo)
        inicio_tempo = time.perf_counter()

        # executa o algoritmo solicitado e extrai o custo do caminho I -> F
        if nome_algoritmo == "Dijkstra":
            distancias, _prev = dijkstra(grafo, vertice_inicio)
            custo_total = distancias[vertice_fim]

        elif nome_algoritmo == "Bellman-Ford":
            distancias, _prev = bellman_ford(grafo, vertice_inicio)
            custo_total = distancias[vertice_fim]

        elif nome_algoritmo == "Floyd-Warshall":
            distancias, _prev = floyd_warshall(grafo)
            custo_total = distancias[vertice_inicio][vertice_fim]

        else:
            raise ValueError("Algoritmo inválido")

        # marca o tempo final e calcula tempo total de execução do algoritmo
        fim_tempo = time.perf_counter()
        tempo_execucao = fim_tempo - inicio_tempo

        # devolve para o processo principal o status, tempo e custo
        fila_resultado.put(("OK", tempo_execucao, custo_total))

    except Exception as erro:
        # devolve erro para o processo principal
        fila_resultado.put(("ERRO", 0.0, str(erro)))


def executar_com_timeout(nome_algoritmo, grafo, vertice_inicio, vertice_fim, timeout_segundos):
    # cria fila para receber resultado do processo
    fila_resultado = mp.Queue()

    # cria processo separado para rodar o algoritmo
    processo = mp.Process(
        target=_worker_algoritmo,
        args=(nome_algoritmo, grafo, vertice_inicio, vertice_fim, fila_resultado)
    )

    # inicia o processo
    processo.start()

    # aguarda até o limite de tempo
    processo.join(timeout_segundos)

    # se ainda está rodando, estourou o tempo limite
    if processo.is_alive():
        processo.terminate()
        processo.join()
        return ("TEMPO LIMITE", None, None)

    # se terminou mas não escreveu nada na fila, algo deu errado
    if fila_resultado.empty():
        return ("ERRO", None, "Sem retorno do processo")

    # lê o resultado do processo
    status, tempo_execucao, custo_total = fila_resultado.get()

    # se deu certo, devolve tempo e custo
    if status == "OK":
        return ("OK", tempo_execucao, custo_total)

    # se deu erro, devolve a mensagem no lugar do custo
    return ("ERRO", None, custo_total)


# -----------------------------
# Benchmark por mapa e por algoritmo
# (retorna também as rodadas, para imprimir tabela detalhada)
# -----------------------------
def benchmark_mapa_algoritmo(nome_algoritmo, grafo, vertice_inicio, vertice_fim, repeticoes, timeout_segundos):
    # lista de tempos coletados nas execuções (somente status OK)
    tempos_execucao = []

    # lista de custos coletados nas execuções (somente status OK)
    custos_execucao = []

    # lista de status por rodada (OK / TEMPO LIMITE / ERRO)
    status_lista = []

    # executa o mesmo algoritmo N vezes
    for _ in range(repeticoes):
        status, tempo_execucao, custo_total = executar_com_timeout(
            nome_algoritmo, grafo, vertice_inicio, vertice_fim, timeout_segundos
        )

        # registra status
        status_lista.append(status)

        # se estourou tempo limite, retorna imediatamente
        if status == "TEMPO LIMITE":
            return ("TEMPO LIMITE", "TEMPO LIMITE", tempos_execucao, custos_execucao, status_lista)

        # se deu erro, retorna imediatamente
        if status == "ERRO":
            return ("ERRO", custo_total, tempos_execucao, custos_execucao, status_lista)

        # status OK: guarda tempo e custo
        tempos_execucao.append(tempo_execucao)
        custos_execucao.append(custo_total)

    # calcula tempo médio
    tempo_medio = media(tempos_execucao)

    # calcula custo médio
    # se qualquer execução deu INF, considera INF (não existe caminho)
    if any(c == INF for c in custos_execucao):
        custo_medio = INF
    else:
        custo_medio = media(custos_execucao)

    return (tempo_medio, custo_medio, tempos_execucao, custos_execucao, status_lista)


# -----------------------------
# MAIN
# -----------------------------
def main():
    global log_file  # permite escrever no log dentro do print_log

    # valida parâmetros: uso correto é "python main_benchmark.py <pasta_mapas>"
    if len(sys.argv) != 2:
        print("Uso: python main_benchmark.py <pasta_mapas>")
        return

    # abre log no início (mesmo conteúdo do console)
    log_file = open("log_benchmark.txt", "w", encoding="utf-8")

    # pasta onde estão os arquivos .txt dos mapas
    pasta_mapas = sys.argv[1]

    # verifica se a pasta existe
    if not os.path.isdir(pasta_mapas):
        print_log("Pasta inválida: " + str(pasta_mapas))
        log_file.close()
        return

    # lista os mapas .txt disponíveis na pasta
    mapas = listar_mapas(pasta_mapas)

    # se não encontrou mapas, encerra
    if not mapas:
        print_log("Nenhum mapa .txt encontrado em: " + str(pasta_mapas))
        log_file.close()
        return

    # conforme especificação: 10 execuções por algoritmo e mapa
    repeticoes = 10

    # conforme especificação: 600 segundos como tempo limite por execução
    timeout_segundos = 300

    # lista de algoritmos que serão testados
    algoritmos = ["Dijkstra", "Bellman-Ford", "Floyd-Warshall"]

    # guarda linhas para a Tabela 1 final (uma por mapa)
    linhas_tabela = []

    # percorre cada mapa da pasta
    for caminho_mapa in mapas:
        # nome do arquivo do mapa (ex: map_10x10.txt)
        nome_mapa = os.path.basename(caminho_mapa)

        # imprime cabeçalho do mapa
        print_cabecalho_mapa(nome_mapa)

        # carrega o mapa e cria o grafo (fora do tempo dos algoritmos, como no main.py)
        grid, linhas, colunas, vertice_inicio, vertice_fim, grafo = carregar_mapa(caminho_mapa)

        # dicionário para guardar médias finais
        resultados = {}

        # executa benchmark para cada algoritmo
        for alg in algoritmos:
            print_log(f"Executando {alg} (10 rodadas, com timeout)...")

            tempo_medio, custo_medio, tempos_execucao, custos_execucao, status_lista = benchmark_mapa_algoritmo(
                alg, grafo, vertice_inicio, vertice_fim, repeticoes, timeout_segundos
            )

            # imprime tabela detalhada das rodadas
            print_tabela_rodadas(alg, tempos_execucao, custos_execucao, status_lista)

            # guarda média para o resumo do mapa
            resultados[alg] = (tempo_medio, custo_medio)

            # imprime médias do algoritmo logo após a tabela
            print_log(f"MÉDIA {alg}: Tempo = {fmt_tempo(tempo_medio)} s | Custo = {fmt_custo(custo_medio)}")

        # imprime resumo final do mapa (com nome do mapa no título)
        print_resumo_mapa(nome_mapa, resultados)

        # prepara a linha do mapa para a Tabela 1 final
        d_t, d_c = resultados["Dijkstra"]
        b_t, b_c = resultados["Bellman-Ford"]
        f_t, f_c = resultados["Floyd-Warshall"]

        linha_tabela = (
            f"{nome_mapa:<20} | "
            f"{fmt_tempo(d_t):<18} | {fmt_custo(d_c):<20} | "
            f"{fmt_tempo(b_t):<22} | {fmt_custo(b_c):<24} | "
            f"{fmt_tempo(f_t):<24} | {fmt_custo(f_c):<26}"
        )

        linhas_tabela.append(linha_tabela)

    # imprime a Tabela final
    print_tabela_final(linhas_tabela)

    print_log("")
    print_log(repetir_char("=", 90))
    print_log("FIM DO BENCHMARK (COM TIMEOUT)")
    print_log(repetir_char("=", 90))

    # fecha o log no final
    log_file.close()


if __name__ == "__main__":
    # necessário principalmente no Windows por causa do multiprocessing
    mp.freeze_support()

    # inicia o benchmark
    main()
