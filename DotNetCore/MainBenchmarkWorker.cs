using System;
using System.Diagnostics;
using System.Globalization;

namespace Grafos
{
    static class MainBenchmarkWorker
    {
        public static void Executar(string nomeAlgoritmo, string caminhoMapa)
        {
            try
            {
                var m = Mapa.carregar_mapa(caminhoMapa);

                int vertice_inicio = m.indice_inicio;
                int vertice_fim = m.indice_fim;
                var grafo = m.grafo;

                var sw = Stopwatch.StartNew();

                double custo_total;

                if (nomeAlgoritmo == "Dijkstra")
                {
                    var r = Algoritmos.dijkstra_iniciante(grafo, vertice_inicio);
                    custo_total = r.distancias[vertice_fim];
                }
                else if (nomeAlgoritmo == "Bellman-Ford")
                {
                    var r = Algoritmos.bellman_ford_iniciante(grafo, vertice_inicio);
                    custo_total = r.distancias[vertice_fim];
                }
                else if (nomeAlgoritmo == "Floyd-Warshall")
                {
                    var r = Algoritmos.floyd_warshall_iniciante(grafo);
                    custo_total = r.distancias[vertice_inicio, vertice_fim];
                }
                else
                {
                    throw new ArgumentException("Algoritmo inválido");
                }

                sw.Stop();

                double tempo_segundos = sw.Elapsed.TotalSeconds;

                // Formato: OK|tempo|custo  (parse simples no processo pai)
                Console.WriteLine(
                    "OK|" +
                    tempo_segundos.ToString("0.################", CultureInfo.InvariantCulture) + "|" +
                    custo_total.ToString("0.################", CultureInfo.InvariantCulture)
                );
            }
            catch (Exception ex)
            {
                Console.WriteLine("ERRO|0|" + ex.Message.Replace("\n", " ").Replace("\r", " "));
            }
        }
    }
}
