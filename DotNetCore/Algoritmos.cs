// Algoritmos.cs
// -----------------------------------------------------------------------------------------
// Implementação fiel dos algoritmos de Dijkstra, Bellman-Ford e Floyd-Warshall (pseudocódigo)
// PORT 1:1 do Algoritmos.py (mesma lógica / mesmos loops / mesma estrutura)
// -----------------------------------------------------------------------------------------

using System;
using System.Collections.Generic;

namespace Grafos
{
    public static class Algoritmos
    {
        // INF = float("inf")
        public static readonly double INF = double.PositiveInfinity;

        public static (double[] distancias, int?[] predecessor) dijkstra_iniciante(dynamic grafo, int origem)
        {
            // total_vertices = grafo.numVertices
            int total_vertices = (int)grafo.numVertices;

            // distancias = [INF] * total_vertices
            var distancias = new double[total_vertices];
            for (int i = 0; i < total_vertices; i++) distancias[i] = INF;

            // predecessor = [None] * total_vertices
            var predecessor = new int?[total_vertices];

            // distancias[origem] = 0
            distancias[origem] = 0;

            // predecessor[origem] = origem
            predecessor[origem] = origem;

            // abertos = set(range(total_vertices))
            var abertos = new HashSet<int>();
            for (int i = 0; i < total_vertices; i++) abertos.Add(i);

            // fechados = set()
            var fechados = new HashSet<int>();

            // while fechados != set(range(total_vertices)):
            while (!SetsIguaisComRange(fechados, total_vertices))
            {
                // vertice_atual = next(iter(abertos))
                int vertice_atual = PrimeiroDeSet(abertos);

                // menor_distancia = distancias[vertice_atual]
                double menor_distancia = distancias[vertice_atual];

                // for v in abertos:
                foreach (int v in abertos)
                {
                    if (distancias[v] < menor_distancia)
                    {
                        menor_distancia = distancias[v];
                        vertice_atual = v;
                    }
                }

                // fechados.add(vertice_atual)
                fechados.Add(vertice_atual);

                // abertos.remove(vertice_atual)
                abertos.Remove(vertice_atual);

                // for (vizinho, peso) in grafo.vizinhos(vertice_atual):
                foreach (var par in grafo.vizinhos(vertice_atual))
                {
                    int vizinho = par.Item1;
                    int peso = par.Item2;

                    // if vizinho not in fechados:
                    if (!fechados.Contains(vizinho))
                    {
                        // distancia_alternativa = distancias[vertice_atual] + peso
                        double distancia_alternativa = distancias[vertice_atual] + peso;

                        // if distancias[vizinho] > distancia_alternativa:
                        if (distancias[vizinho] > distancia_alternativa)
                        {
                            // distancias[vizinho] = distancia_alternativa
                            distancias[vizinho] = distancia_alternativa;

                            // predecessor[vizinho] = vertice_atual
                            predecessor[vizinho] = vertice_atual;
                        }
                    }
                }
            }

            return (distancias, predecessor);
        }

        public static (double[] distancias, int?[] predecessor) dijkstra_iniciante_otimizado(dynamic grafo, int origem)
        {
            int total_vertices = (int)grafo.numVertices;

            var distancias = new double[total_vertices];
            for (int i = 0; i < total_vertices; i++) distancias[i] = INF;

            var predecessor = new int?[total_vertices];

            distancias[origem] = 0;
            predecessor[origem] = origem;

            var abertos = new HashSet<int>();
            for (int i = 0; i < total_vertices; i++) abertos.Add(i);

            var fechados = new HashSet<int>();

            // while abertos:
            while (abertos.Count > 0)
            {
                int vertice_atual = PrimeiroDeSet(abertos);
                double menor_distancia = distancias[vertice_atual];

                foreach (int v in abertos)
                {
                    if (distancias[v] < menor_distancia)
                    {
                        menor_distancia = distancias[v];
                        vertice_atual = v;
                    }
                }

                // OTIMIZAÇÃO: se o menor ainda é INF, não existe caminho para o restante
                if (menor_distancia == INF)
                {
                    break;
                }

                fechados.Add(vertice_atual);
                abertos.Remove(vertice_atual);

                foreach (var par in grafo.vizinhos(vertice_atual))
                {
                    int vizinho = par.Item1;
                    int peso = par.Item2;

                    if (!fechados.Contains(vizinho))
                    {
                        double distancia_alternativa = distancias[vertice_atual] + peso;

                        if (distancias[vizinho] > distancia_alternativa)
                        {
                            distancias[vizinho] = distancia_alternativa;
                            predecessor[vizinho] = vertice_atual;
                        }
                    }
                }
            }

            return (distancias, predecessor);
        }

        public static (double[] distancias, int?[] predecessor) bellman_ford_iniciante(dynamic grafo, int origem)
        {
            int total_vertices = (int)grafo.numVertices;

            var distancias = new double[total_vertices];
            for (int i = 0; i < total_vertices; i++) distancias[i] = INF;

            var predecessor = new int?[total_vertices];

            distancias[origem] = 0;
            predecessor[origem] = origem;

            // for _ in range(total_vertices - 1):
            for (int _ = 0; _ < total_vertices - 1; _++)
            {
                bool houve_atualizacao = false;

                // for u in range(total_vertices):
                for (int u = 0; u < total_vertices; u++)
                {
                    // for (v, peso) in grafo.vizinhos(u):
                    foreach (var par in grafo.vizinhos(u))
                    {
                        int v = par.Item1;
                        int peso = par.Item2;

                        // if distancias[v] > distancias[u] + peso:
                        if (distancias[v] > distancias[u] + peso)
                        {
                            distancias[v] = distancias[u] + peso;
                            predecessor[v] = u;
                            houve_atualizacao = true;
                        }
                    }
                }

                if (!houve_atualizacao)
                {
                    break;
                }
            }

            return (distancias, predecessor);
        }

        public static (double[,] distancias, int?[,] predecessor) floyd_warshall_iniciante(dynamic grafo)
        {
            int total_vertices = (int)grafo.numVertices;

            // distancias = [[INF] * total_vertices for _ in range(total_vertices)]
            var distancias = new double[total_vertices, total_vertices];
            for (int i = 0; i < total_vertices; i++)
                for (int j = 0; j < total_vertices; j++)
                    distancias[i, j] = INF;

            // predecessor = [[None] * total_vertices for _ in range(total_vertices)]
            var predecessor = new int?[total_vertices, total_vertices];

            // inicialização
            for (int i = 0; i < total_vertices; i++)
            {
                for (int j = 0; j < total_vertices; j++)
                {
                    if (i == j)
                    {
                        distancias[i, j] = 0;
                        predecessor[i, j] = i;
                    }
                    else if ((bool)grafo.possuiAresta(i, j))
                    {
                        // busca o peso da aresta (i, j) varrendo vizinhos(i) (1:1 do Python)
                        foreach (var par in grafo.vizinhos(i))
                        {
                            int vizinho = par.Item1;
                            int peso = par.Item2;

                            if (vizinho == j)
                            {
                                distancias[i, j] = peso;
                                predecessor[i, j] = i;
                            }
                        }
                    }
                    // else: mantém INF e None (já inicializado)
                }
            }

            // laços principais
            for (int k = 0; k < total_vertices; k++)
            {
                for (int i = 0; i < total_vertices; i++)
                {
                    for (int j = 0; j < total_vertices; j++)
                    {
                        if (distancias[i, j] > distancias[i, k] + distancias[k, j])
                        {
                            distancias[i, j] = distancias[i, k] + distancias[k, j];
                            predecessor[i, j] = predecessor[k, j];
                        }
                    }
                }
            }

            return (distancias, predecessor);
        }

        // -----------------------------
        // Reconstrução de Caminho (prev por vértice)
        // -----------------------------
        public static List<int> reconstruir_caminho_prev(int?[] prev, int s, int t)
        {
            if (s == t)
            {
                return new List<int> { s };
            }

            if (prev[t] == null)
            {
                return new List<int>();
            }

            var caminho = new List<int>();
            int? vertice_atual = t;

            int max_passos = prev.Length;
            int passos = 0;

            while (true)
            {
                if (vertice_atual == null) return new List<int>();

                caminho.Add(vertice_atual.Value);

                if (vertice_atual.Value == s)
                {
                    break;
                }

                vertice_atual = prev[vertice_atual.Value];

                if (vertice_atual == null)
                {
                    return new List<int>();
                }

                passos += 1;
                if (passos > max_passos)
                {
                    return new List<int>();
                }
            }

            caminho.Reverse();
            return caminho;
        }

        // -----------------------------
        // Reconstrução de Caminho (prev por par i->j do Floyd-Warshall)
        // -----------------------------
        public static List<int> reconstruir_caminho_floyd(int?[,] prev, int s, int t)
        {
            if (prev[s, t] == null)
            {
                return new List<int>();
            }

            var caminho = new List<int>();
            int? vertice_atual = t;

            int total_vertices = prev.GetLength(0);
            int max_passos = total_vertices;
            int passos = 0;

            while (true)
            {
                if (vertice_atual == null) return new List<int>();

                caminho.Add(vertice_atual.Value);

                if (vertice_atual.Value == s)
                {
                    break;
                }

                vertice_atual = prev[s, vertice_atual.Value];

                if (vertice_atual == null)
                {
                    return new List<int>();
                }

                passos += 1;
                if (passos > max_passos)
                {
                    return new List<int>();
                }
            }

            caminho.Reverse();
            return caminho;
        }

        // -----------------------------
        // Helpers (mantém comportamento do Python)
        // -----------------------------
        private static int PrimeiroDeSet(HashSet<int> set)
        {
            foreach (int v in set) return v;
            throw new InvalidOperationException("Set vazio.");
        }

        private static bool SetsIguaisComRange(HashSet<int> fechados, int total_vertices)
        {
            // equivalente a: fechados != set(range(total_vertices))
            if (fechados.Count != total_vertices) return false;
            for (int i = 0; i < total_vertices; i++)
            {
                if (!fechados.Contains(i)) return false;
            }
            return true;
        }
    }
}
