using System;
using System.Collections.Generic;
using System.Linq;

record Tarefa(int Id, string Titulo, bool Feita);

class Program
{
    static void Main()
    {
        var tarefas = new List<Tarefa>();
        int nextId = 1;
        Console.WriteLine("03 - To-do Console C# (List<T> + LINQ)");
        Console.WriteLine("Comandos: add <titulo> | done <id> | rm <id> | ls | sair");
        while (true)
        {
            Console.Write("> ");
            var line = Console.ReadLine();
            if (string.IsNullOrWhiteSpace(line)) continue;
            var parts = line.Split(' ', 2);
            var cmd = parts[0].ToLower();
            if (cmd == "sair" || cmd == "exit") break;
            if (cmd == "add" && parts.Length == 2) { tarefas.Add(new Tarefa(nextId++, parts[1], false)); }
            else if (cmd == "done" && int.TryParse(parts[1], out var did)) {
                var idx = tarefas.FindIndex(t => t.Id == did);
                if (idx >= 0) tarefas[idx] = tarefas[idx] with { Feita = true };
            }
            else if (cmd == "rm" && int.TryParse(parts[1], out var rid)) tarefas.RemoveAll(t => t.Id == rid);
            else if (cmd == "ls") {
                foreach (var t in tarefas.OrderBy(t => t.Feita))
                    Console.WriteLine($"{t.Id}. [{(t.Feita ? "x" : " ")}] {t.Titulo}");
                if (!tarefas.Any()) Console.WriteLine("(vazia)");
                continue;
            }
            else { Console.WriteLine("Comando invalido."); continue; }
            Console.WriteLine("OK.");
        }
    }
}
