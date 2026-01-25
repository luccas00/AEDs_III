using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Globalization;
using System.IO;

namespace Grafos
{
    static class MainBenchmark
    {
        static StreamWriter? log_file;

        static readonly double INF = double.PositiveInfinity;

        // -----------------------------
        // LOG (console + arquivo)
        // -----------------------------
        static void print_log(string texto = "")
        {
            Console.WriteLine(texto);
            if (log_file != null)
            {
                log_file.WriteLine(texto);
                log_file.Flush();
            }
        }

        // -----------------------------
        // Funções auxiliares (Mapas / Médias / Formatação)
        // -----------------------------
        static List<string> listar_mapas(string pasta_mapas)
        {
            var mapas_encontrados = new List<string>();

            foreach (var nome_arquivo in Directory.GetFiles(pasta_mapas))
            {
                if (File.Exists(nome_arquivo) && nome_arquivo.ToLowerInvariant().EndsWith(".txt"))
                {
                    mapas_encontrados.Add(nome_arquivo);
                }
            }

            mapas_encontrados.Sort(StringComparer.Ordinal);
            return mapas_encontrados;
        }

        static double? media(List<double> valores)
        {
            if (valores.Count == 0) return null;
            double soma = 0;
            for (int i = 0; i < valores.Count; i++) soma += valores[i];
            return soma / valores.Count;
        }

        static string fmt_tempo(object? valor)
        {
            if (valor is string s && s == "TEMPO LIMITE") return "TEMPO LIMITE";
            if (valor == null) return "-";
            if (valor is double d) return d.ToString("0.000000", CultureInfo.InvariantCulture);
            return valor.ToString() ?? "-";
        }

        static string fmt_custo(object? valor)
        {
            if (valor is string s && s == "TEMPO LIMITE") return "TEMPO LIMITE";
            if (valor == null) return "-";
            if (valor is double d)
            {
                if (double.IsPositiveInfinity(d)) return "INF";
                if (Math.Abs(d - Math.Round(d)) < 1e-12) return ((int)Math.Round(d)).ToString(CultureInfo.InvariantCulture);
                return d.ToString("0.################", CultureInfo.InvariantCulture);
            }
            return valor.ToString() ?? "-";
        }

        static string repetir_char(string c, int n)
        {
            return new string(c[0], n);
        }

        static void print_cabecalho_mapa(string nome_mapa)
        {
            print_log("");
            print_log(repetir_char("=", 90));
            print_log($"MAPA: {nome_mapa}");
            print_log(repetir_char("=", 90));
        }

        static void print_tabela_rodadas(string nome_algoritmo, List<double> tempos_execucao, List<double> custos_execucao, List<string> status_lista)
        {
            print_log("");
            print_log($"[{nome_algoritmo}] Resultados Por Rodada");
            print_log(repetir_char("-", 90));
            print_log($"{PadRight("Rodada", 10)} | {PadRight("Tempo (s)", 12)} | {PadRight("Custo", 12)} | {PadRight("Status", 20)}");
            print_log(repetir_char("-", 90));

            int total_rodadas = status_lista.Count;
            int indice_ok = 0;

            for (int i = 0; i < total_rodadas; i++)
            {
                int rodada = i + 1;
                string status = status_lista[i];

                string tempo_str;
                string custo_str;

                if (status == "OK")
                {
                    tempo_str = tempos_execucao[indice_ok].ToString("0.000000", CultureInfo.InvariantCulture);
                    custo_str = fmt_custo(custos_execucao[indice_ok]);
                    indice_ok += 1;
                }
                else if (status == "TEMPO LIMITE")
                {
                    tempo_str = "TEMPO LIMITE";
                    custo_str = "TEMPO LIMITE";
                }
                else
                {
                    tempo_str = "-";
                    custo_str = "-";
                }

                print_log($"{PadRight(rodada.ToString(CultureInfo.InvariantCulture), 10)} | {PadRight(tempo_str, 12)} | {PadRight(custo_str, 12)} | {PadRight(status, 20)}");
            }

            print_log(repetir_char("-", 90));
        }

        static void print_resumo_mapa(string nome_mapa, Dictionary<string, (object? tempo_medio, object? custo_medio)> resultados)
        {
            print_log("");
            print_log($"[Resumo Do Mapa] {nome_mapa} — Médias (10 execuções)");
            print_log(repetir_char("-", 90));
            print_log($"{PadRight("Algoritmo", 20)} | {PadRight("Tempo Médio (s)", 18)} | {PadRight("Custo Médio", 15)}");
            print_log(repetir_char("-", 90));

            foreach (var alg in new[] { "Dijkstra", "Bellman-Ford", "Floyd-Warshall" })
            {
                var (tempo_medio, custo_medio) = resultados[alg];
                print_log($"{PadRight(alg, 20)} | {PadRight(fmt_tempo(tempo_medio), 18)} | {PadRight(fmt_custo(custo_medio), 15)}");
            }

            print_log(repetir_char("-", 90));
        }

        static void print_tabela1_final(List<string> linhas_tabela)
        {
            print_log("");
            print_log(repetir_char("=", 130));
            print_log("TABELA 1 — Comparação Entre Algoritmos De Caminhos Mínimos (Médias Em 10 Execuções)");
            print_log(repetir_char("=", 130));
            print_log(
                $"{PadRight("Grafo", 20)} | " +
                $"{PadRight("Dijkstra T.médio(s)", 18)} | {PadRight("Dijkstra Custo médio", 20)} | " +
                $"{PadRight("Bellman-Ford T.médio(s)", 22)} | {PadRight("Bellman-Ford Custo médio", 24)} | " +
                $"{PadRight("Floyd-Warshall T.médio(s)", 24)} | {PadRight("Floyd-Warshall Custo médio", 26)}"
            );
            print_log(repetir_char("-", 130));

            foreach (var linha in linhas_tabela)
            {
                print_log(linha);
            }

            print_log(repetir_char("=", 130));
        }

        // -----------------------------
        // Execução do algoritmo em processo separado (timeout real)
        // -----------------------------
        static (string status, double? tempo_execucao, object? custo_total) executar_com_timeout(
            string nome_algoritmo,
            string caminho_mapa,
            int timeout_segundos
        )
        {
            string exe = Environment.ProcessPath ?? throw new InvalidOperationException("ProcessPath não disponível.");

            var psi = new ProcessStartInfo
            {
                FileName = exe,
                Arguments = $"--worker \"{nome_algoritmo}\" \"{caminho_mapa}\"",
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };

            using var p = new Process { StartInfo = psi };

            p.Start();

            bool saiu = p.WaitForExit(timeout_segundos * 1000);

            if (!saiu)
            {
                try { p.Kill(entireProcessTree: true); } catch { }
                try { p.WaitForExit(); } catch { }
                return ("TEMPO LIMITE", null, null);
            }

            string saida = p.StandardOutput.ReadToEnd().Trim();

            if (string.IsNullOrWhiteSpace(saida))
            {
                return ("ERRO", null, "Sem retorno do processo");
            }

            // OK|tempo|custo  ou  ERRO|0|mensagem
            var partes = saida.Split('|');
            if (partes.Length < 3)
            {
                return ("ERRO", null, saida);
            }

            string status = partes[0];

            if (status == "OK")
            {
                if (!double.TryParse(partes[1], NumberStyles.Float, CultureInfo.InvariantCulture, out double tempo))
                    return ("ERRO", null, "Tempo inválido");

                if (!double.TryParse(partes[2], NumberStyles.Float, CultureInfo.InvariantCulture, out double custo))
                    return ("ERRO", null, "Custo inválido");

                return ("OK", tempo, custo);
            }

            // ERRO
            return ("ERRO", null, partes[2]);
        }

        // -----------------------------
        // Benchmark por mapa e por algoritmo (retorna rodadas)
        // -----------------------------
        static (object? tempo_medio, object? custo_medio, List<double> tempos_execucao, List<double> custos_execucao, List<string> status_lista)
            benchmark_mapa_algoritmo(string nome_algoritmo, string caminho_mapa, int repeticoes, int timeout_segundos)
        {
            var tempos_execucao = new List<double>();
            var custos_execucao = new List<double>();
            var status_lista = new List<string>();

            for (int _ = 0; _ < repeticoes; _++)
            {
                var (status, tempo_execucao, custo_total) = executar_com_timeout(nome_algoritmo, caminho_mapa, timeout_segundos);

                status_lista.Add(status);

                if (status == "TEMPO LIMITE")
                {
                    return ("TEMPO LIMITE", "TEMPO LIMITE", tempos_execucao, custos_execucao, status_lista);
                }

                if (status == "ERRO")
                {
                    return ("ERRO", custo_total, tempos_execucao, custos_execucao, status_lista);
                }

                // OK
                tempos_execucao.Add(tempo_execucao!.Value);
                custos_execucao.Add((double)custo_total!);
            }

            double? tempo_m = media(tempos_execucao);

            object? custo_m;
            bool temInf = false;
            for (int i = 0; i < custos_execucao.Count; i++)
            {
                if (double.IsPositiveInfinity(custos_execucao[i]))
                {
                    temInf = true;
                    break;
                }
            }

            if (temInf) custo_m = INF;
            else custo_m = media(custos_execucao);

            return (tempo_m, custo_m, tempos_execucao, custos_execucao, status_lista);
        }

        // -----------------------------
        // MAIN (benchmark)
        // -----------------------------
        public static void Executar(string pasta_mapas)
        {
            log_file = new StreamWriter("log_benchmark.txt", false);

            if (!Directory.Exists(pasta_mapas))
            {
                print_log("Pasta inválida: " + pasta_mapas);
                log_file.Close();
                return;
            }

            var mapas = listar_mapas(pasta_mapas);

            if (mapas.Count == 0)
            {
                print_log("Nenhum mapa .txt encontrado em: " + pasta_mapas);
                log_file.Close();
                return;
            }

            int repeticoes = 10;

            // REPLICA O PYTHON: está 1800 no arquivo enviado
            int timeout_segundos = 1800;

            var algoritmos = new[] { "Dijkstra", "Bellman-Ford", "Floyd-Warshall" };

            var linhas_tabela = new List<string>();

            foreach (var caminho_mapa in mapas)
            {
                string nome_mapa = Path.GetFileName(caminho_mapa);

                print_cabecalho_mapa(nome_mapa);

                var resultados = new Dictionary<string, (object? tempo_medio, object? custo_medio)>();

                foreach (var alg in algoritmos)
                {
                    print_log($"Executando {alg} (10 rodadas, com timeout)...");

                    var (tempo_medio, custo_medio, tempos_execucao, custos_execucao, status_lista) =
                        benchmark_mapa_algoritmo(alg, caminho_mapa, repeticoes, timeout_segundos);

                    print_tabela_rodadas(alg, tempos_execucao, custos_execucao, status_lista);

                    resultados[alg] = (tempo_medio, custo_medio);

                    print_log($"MÉDIA {alg}: Tempo = {fmt_tempo(tempo_medio)} s | Custo = {fmt_custo(custo_medio)}");
                }

                print_resumo_mapa(nome_mapa, resultados);

                var (d_t, d_c) = resultados["Dijkstra"];
                var (b_t, b_c) = resultados["Bellman-Ford"];
                var (f_t, f_c) = resultados["Floyd-Warshall"];

                string linha_tabela =
                    $"{PadRight(nome_mapa, 20)} | " +
                    $"{PadRight(fmt_tempo(d_t), 18)} | {PadRight(fmt_custo(d_c), 20)} | " +
                    $"{PadRight(fmt_tempo(b_t), 22)} | {PadRight(fmt_custo(b_c), 24)} | " +
                    $"{PadRight(fmt_tempo(f_t), 24)} | {PadRight(fmt_custo(f_c), 26)}";

                linhas_tabela.Add(linha_tabela);
            }

            print_tabela1_final(linhas_tabela);

            print_log("");
            print_log(repetir_char("=", 90));
            print_log("FIM DO BENCHMARK (COM TIMEOUT)");
            print_log(repetir_char("=", 90));

            log_file.Close();
        }

        static string PadRight(string s, int n)
        {
            if (s.Length >= n) return s;
            return s.PadRight(n);
        }
    }
}
