// Grafo.cs
// --------------------------------------------------------------------
// Estruturas de Grafo utilizadas pelo TP1 (matriz/lista de adjacências)
// PORT 1:1 do Grafo.py (mesma lógica / mesmas estruturas)
// --------------------------------------------------------------------

using System;
using System.Collections.Generic;

namespace Grafos
{
    public class MatrizAdjacencias
    {
        // Implementação baseada no material da disciplina
        public int numVertices;
        public int numArestas;
        public int[] grauVertice;
        public int[][] matriz;

        public MatrizAdjacencias(int numVertices)
        {
            this.numVertices = numVertices;
            this.numArestas = 0;
            this.grauVertice = new int[numVertices];

            this.matriz = new int[numVertices][];
            for (int i = 0; i < numVertices; i++)
            {
                this.matriz[i] = new int[numVertices];
            }
        }

        public int ordem()
        {
            return this.numVertices;
        }

        public int tamanho()
        {
            return this.numArestas;
        }

        public double densidade()
        {
            double maxArestas = this.numVertices * (this.numVertices - 1);
            return this.numArestas / maxArestas;
        }

        public void addAresta(int v1, int v2, int peso = 1)
        {
            if (this.matriz[v1][v2] == 0)
            {
                this.numArestas += 1;
                this.grauVertice[v1] += 1;
            }
            this.matriz[v1][v2] = peso;
        }

        public bool possuiAresta(int v1, int v2)
        {
            return this.matriz[v1][v2] != 0;
        }

        public List<(int, int)> vizinhos(int v)
        {
            var ret = new List<(int, int)>();
            for (int i = 0; i < this.numVertices; i++)
            {
                if (this.matriz[v][i] != 0)
                {
                    ret.Add((i, this.matriz[v][i]));
                }
            }
            return ret;
        }

        public int grau(int v)
        {
            return this.grauVertice[v];
        }

        public void printGrafo()
        {
            for (int i = 0; i < this.numVertices; i++)
            {
                // equivalente ao: " ".join(str(x) for x in self.matriz[i])
                for (int j = 0; j < this.numVertices; j++)
                {
                    if (j > 0) Console.Write(" ");
                    Console.Write(this.matriz[i][j]);
                }
                Console.WriteLine();
            }
        }
    }

    public class ListaAdjacencias
    {
        // Estrutura mais eficiente para grafos esparsos
        public int numVertices;
        public int numArestas;
        public List<(int, int)>[] lista;

        public ListaAdjacencias(int numVertices)
        {
            this.numVertices = numVertices;
            this.numArestas = 0;

            this.lista = new List<(int, int)>[numVertices];
            for (int i = 0; i < numVertices; i++)
            {
                this.lista[i] = new List<(int, int)>();
            }
        }

        public int ordem()
        {
            return this.numVertices;
        }

        public int tamanho()
        {
            return this.numArestas;
        }

        public double densidade()
        {
            double maxArestas = this.numVertices * (this.numVertices - 1);
            return this.numArestas / maxArestas;
        }

        public void addAresta(int v1, int v2, int peso = 1)
        {
            this.lista[v1].Add((v2, peso));
            this.numArestas += 1;
        }

        public bool possuiAresta(int v1, int v2)
        {
            // return any(vertice == v2 for vertice, _ in self.lista[v1])
            foreach (var item in this.lista[v1])
            {
                if (item.Item1 == v2) return true;
            }
            return false;
        }

        public List<(int, int)> vizinhos(int v)
        {
            return this.lista[v];
        }

        public int grau(int v)
        {
            return this.lista[v].Count;
        }

        public void printGrafo()
        {
            for (int i = 0; i < this.numVertices; i++)
            {
                Console.Write($"Vertice {i}: ");
                Console.WriteLine($"[{string.Join(", ", this.lista[i])}]");
            }
        }
    }
}
