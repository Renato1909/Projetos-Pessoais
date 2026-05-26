using System;

namespace Primeiro
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Olá, Mundo!");
            Console.WriteLine("Bem-vindo ao meu primeiro projeto C#!");
            
            // Pedir nome do usuário
            Console.Write("\nDigite seu nome: ");
            string? nome = Console.ReadLine();
            
            if (!string.IsNullOrEmpty(nome))
            {
                Console.WriteLine($"\nPrazer em conhecê-lo, {nome}!");
            }
            
            // Exibir informações básicas
            Console.WriteLine("\n=== Informações do Sistema ===");
            Console.WriteLine($"Versão do .NET: {Environment.Version}");
            Console.WriteLine($"Sistema Operacional: {Environment.OSVersion}");
            Console.WriteLine($"Nome da Máquina: {Environment.MachineName}");
            
            Console.WriteLine("\nPressione qualquer tecla para sair...");
            Console.ReadKey();
        }
    }
}