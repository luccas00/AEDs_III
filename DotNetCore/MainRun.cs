using System;
using System.Diagnostics;

namespace Grafos
{
    static class MainRun
    {
        public static void Executar(string nome_arquivo)
        {
            var resultado = Mapa.carregar_mapa(nome_arquivo);

            var grid = resultado.grid;
            int total_linhas = resultado.total_linhas;
            int total_colunas = resultado.total_colunas;
            int indice_inicio = resultado.indice_inicio;
            int indice_fim = resultado.indice_fim;
            var grafo = resultado.grafo;

            Console.WriteLine("Mapa carregado com sucesso.");
            Console.WriteLine($"Dimensões: {total_linhas} x {total_colunas}");
            Console.WriteLine($"Início: {indice_inicio}");
            Console.WriteLine($"Fim: {indice_fim}");
            Console.WriteLine();

            var stopwatch = new Stopwatch();

            // =============================
            // Dijkstra
            // =============================
            Console.WriteLine("Executando Dijkstra...");
            stopwatch.Restart();

            var rD = Algoritmos.dijkstra_iniciante(grafo, indice_inicio);
            stopwatch.Stop();

            Console.WriteLine($"Custo Dijkstra: {rD.distancias[indice_fim]}");
            Console.WriteLine(
                $"Tempo Dijkstra: {stopwatch.Elapsed.TotalSeconds:F6} s ({stopwatch.Elapsed.TotalMilliseconds:F3} ms)"
            );

            var caminhoD = Algoritmos.reconstruir_caminho_prev(
                rD.predecessor, indice_inicio, indice_fim
            );

            var gridD = Mapa.marcar_caminho(grid, total_linhas, total_colunas, caminhoD);
            Mapa.salvar_mapa(gridD, "saida_dijkstra.txt");

            Console.WriteLine();

            // =============================
            // Bellman-Ford
            // =============================
            Console.WriteLine("Executando Bellman-Ford...");
            stopwatch.Restart();

            var rB = Algoritmos.bellman_ford_iniciante(grafo, indice_inicio);
            stopwatch.Stop();

            Console.WriteLine($"Custo Bellman-Ford: {rB.distancias[indice_fim]}");
            Console.WriteLine(
                $"Tempo Bellman-Ford: {stopwatch.Elapsed.TotalSeconds:F6} s ({stopwatch.Elapsed.TotalMilliseconds:F3} ms)"
            );

            var caminhoB = Algoritmos.reconstruir_caminho_prev(
                rB.predecessor, indice_inicio, indice_fim
            );

            var gridB = Mapa.marcar_caminho(grid, total_linhas, total_colunas, caminhoB);
            Mapa.salvar_mapa(gridB, "saida_bellman_ford.txt");

            Console.WriteLine();

            // =============================
            // Floyd-Warshall
            // =============================
            Console.WriteLine("Executando Floyd-Warshall...");
            stopwatch.Restart();

            var rF = Algoritmos.floyd_warshall_iniciante(grafo);
            stopwatch.Stop();

            Console.WriteLine($"Custo Floyd-Warshall: {rF.distancias[indice_inicio, indice_fim]}");
            Console.WriteLine(
                $"Tempo Floyd-Warshall: {stopwatch.Elapsed.TotalSeconds:F6} s ({stopwatch.Elapsed.TotalMilliseconds:F3} ms)"
            );

            var caminhoF = Algoritmos.reconstruir_caminho_floyd(
                rF.predecessor, indice_inicio, indice_fim
            );

            var gridF = Mapa.marcar_caminho(grid, total_linhas, total_colunas, caminhoF);
            Mapa.salvar_mapa(gridF, "saida_floyd_warshall.txt");

            Console.WriteLine();
            Console.WriteLine("Execução finalizada.");
        }
    }
}
