using System;

namespace Grafos
{
    class Program
    {
        static void Main(string[] args)
        {
            if (args.Length == 0)
            {
                Console.WriteLine("Uso:");
                Console.WriteLine("  dotnet run <arquivo_mapa>");
                Console.WriteLine("  dotnet run --test <pasta_mapas>");
                return;
            }

            if (args[0] == "--test")
            {
                if (args.Length < 2)
                {
                    Console.WriteLine("Uso: dotnet run --test <pasta_mapas>");
                    return;
                }

                MainBenchmark.Executar(args[1]);
                return;
            }

            if (args[0] == "--worker")
            {
                // Uso interno do benchmark (equivalente ao _worker_algoritmo do Python)
                if (args.Length < 3)
                {
                    Console.WriteLine("ERRO|0|Argumentos insuficientes");
                    return;
                }

                MainBenchmarkWorker.Executar(args[1], args[2]);
                return;
            }

            // modo normal: dotnet run mapa.txt
            MainRun.Executar(args[0]);
        }
    }
}
