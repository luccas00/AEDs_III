// Mapa.cs
// ------------------------------------------------------------------------------------
// Responsável por carregar o mapa, converter células em vértices e gerar o grafo final
// PORT 1:1 do Mapa.py (mesma lógica / mesmas validações / mesmos índices)
// ------------------------------------------------------------------------------------

using System;
using System.Collections.Generic;
using System.IO;

namespace Grafos
{
    public static class Mapa
    {
        // INF = float("inf")  # não utilizado aqui, mantido para consistência com o restante do projeto
        public static readonly double INF = double.PositiveInfinity;

        public static int custo_terreno(char c)
        {
            // Retorna o custo para ENTRAR em uma célula do tipo 'c' (conforme especificação)
            if (c == 'W') return 5;                 // Water
            if (c == 'S') return 3;                 // Sand
            if (c == 'G') return 1;                 // Ground
            if (c == 'I' || c == 'F') return 0;     // Início e Fim não adicionam custo

            throw new ArgumentException($"Terreno inválido: {c}");
        }

        public static (List<List<char>> grid, int total_linhas, int total_colunas, int indice_inicio, int indice_fim, ListaAdjacencias grafo)
            carregar_mapa(string nome_arquivo)
        {
            // grid será uma matriz de caracteres (lista de listas)
            var grid = new List<List<char>>();

            // lê o arquivo linha a linha
            using (var arquivo = new StreamReader(nome_arquivo))
            {
                string? linha;
                while ((linha = arquivo.ReadLine()) != null)
                {
                    // remove espaços e quebras de linha
                    linha = linha.Trim().Replace(" ", "");

                    // ignora linhas vazias
                    if (linha.Length > 0)
                    {
                        // converte a string em lista de caracteres
                        var lista = new List<char>(linha.Length);
                        for (int i = 0; i < linha.Length; i++)
                            lista.Add(linha[i]);

                        grid.Add(lista);
                    }
                }
            }

            // validação básica: mapa não pode ser vazio
            if (grid.Count == 0)
                throw new ArgumentException("Mapa vazio ou arquivo inválido.");

            // dimensões do grid
            int total_linhas = grid.Count;
            int total_colunas = grid[0].Count;

            // valida se todas as linhas têm o mesmo tamanho (evita index error)
            for (int i = 0; i < total_linhas; i++)
            {
                if (grid[i].Count != total_colunas)
                    throw new ArgumentException("Mapa inválido: linhas com tamanhos diferentes.");
            }

            // localiza posições de início (I) e fim (F) e valida unicidade
            int? indice_inicio = null;
            int? indice_fim = null;
            int quantidade_inicio = 0;
            int quantidade_fim = 0;

            for (int i = 0; i < total_linhas; i++)
            {
                for (int j = 0; j < total_colunas; j++)
                {
                    if (grid[i][j] == 'I')
                    {
                        quantidade_inicio += 1;
                        indice_inicio = i * total_colunas + j; // converte (i,j) para índice de vértice
                    }
                    else if (grid[i][j] == 'F')
                    {
                        quantidade_fim += 1;
                        indice_fim = i * total_colunas + j;    // converte (i,j) para índice de vértice
                    }
                }
            }

            // exige exatamente um I e um F (conforme mensagem do seu erro)
            if (quantidade_inicio != 1 || quantidade_fim != 1)
                throw new ArgumentException("Mapa deve conter exatamente um I e um F.");

            // cria grafo com um vértice para cada célula do grid
            var grafo = new ListaAdjacencias(total_linhas * total_colunas);

            // movimentos permitidos: cima, baixo, esquerda, direita (4-vizinhos)
            var direcoes_movimento = new (int di, int dj)[]
            {
                (-1, 0),
                ( 1, 0),
                ( 0,-1),
                ( 0, 1)
            };

            // percorre todas as células para criar arestas
            for (int i = 0; i < total_linhas; i++)
            {
                for (int j = 0; j < total_colunas; j++)
                {
                    // parede não vira vértice "utilizável" (sem arestas saindo)
                    if (grid[i][j] == '#')
                        continue;

                    // vértice atual u (célula i,j)
                    int u = i * total_colunas + j;

                    // tenta mover nas 4 direções
                    foreach (var (di, dj) in direcoes_movimento)
                    {
                        int proxima_linha = i + di;
                        int proxima_coluna = j + dj;

                        // verifica se está dentro dos limites do grid
                        if (0 <= proxima_linha && proxima_linha < total_linhas &&
                            0 <= proxima_coluna && proxima_coluna < total_colunas)
                        {
                            // não entra em parede
                            if (grid[proxima_linha][proxima_coluna] != '#')
                            {
                                // vértice de destino v
                                int v = proxima_linha * total_colunas + proxima_coluna;

                                // custo para entrar na célula de destino
                                int peso = custo_terreno(grid[proxima_linha][proxima_coluna]);

                                // adiciona aresta direcionada u -> v com peso
                                grafo.addAresta(u, v, peso);
                            }
                        }
                    }
                }
            }

            return (grid, total_linhas, total_colunas, indice_inicio!.Value, indice_fim!.Value, grafo);
        }

        public static List<List<char>> marcar_caminho(List<List<char>> grid, int linhas, int colunas, List<int> caminho)
        {
            // cria uma cópia do grid para não alterar o original
            var grid_marcado = new List<List<char>>(linhas);
            for (int i = 0; i < linhas; i++)
            {
                var novaLinha = new List<char>(colunas);
                for (int j = 0; j < colunas; j++)
                    novaLinha.Add(grid[i][j]);
                grid_marcado.Add(novaLinha);
            }

            // para cada vértice do caminho, converte para (linha, coluna) e marca '*'
            foreach (int vertice in caminho)
            {
                int linha = vertice / colunas;
                int coluna = vertice % colunas;

                // não sobrescreve início e fim
                if (grid_marcado[linha][coluna] != 'I' && grid_marcado[linha][coluna] != 'F')
                {
                    grid_marcado[linha][coluna] = '*';
                }
            }

            // retorna o novo grid com o caminho marcado
            return grid_marcado;
        }

        public static void salvar_mapa(List<List<char>> grid, string nome_arquivo)
        {
            // grava o grid no arquivo, uma linha por vez
            using (var arquivo = new StreamWriter(nome_arquivo, false))
            {
                for (int i = 0; i < grid.Count; i++)
                {
                    var linha = grid[i];
                    var chars = new char[linha.Count];
                    for (int j = 0; j < linha.Count; j++) chars[j] = linha[j];

                    arquivo.Write(new string(chars));
                    arquivo.Write('\n');
                }
            }
        }
    }
}
