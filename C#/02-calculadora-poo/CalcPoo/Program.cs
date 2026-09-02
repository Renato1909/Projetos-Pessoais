using System;

class Calculadora
{
    public static double Calcular(double a, double b, char op) => op switch
    {
        '+' => a + b,
        '-' => a - b,
        '*' => a * b,
        '/' => b != 0 ? a / b : throw new DivideByZeroException(),
        _ => throw new ArgumentException("Operador invalido")
    };
}

class Program
{
    static void Main()
    {
        Console.WriteLine("02 - Calculadora POO C#");
        Console.Write("Digite: <num> <op> <num> ex: 10 * 3 > ");
        var parts = Console.ReadLine()?.Split(' ');
        if (parts?.Length != 3 || !double.TryParse(parts[0], out var a) || !double.TryParse(parts[2], out var b))
        {
            Console.WriteLine("Entrada invalida.");
            return;
        }
        try
        {
            var r = Calculadora.Calcular(a, b, parts[1][0]);
            Console.WriteLine($"Resultado: {r:F2}");
        }
        catch (Exception ex) { Console.WriteLine($"Erro: {ex.Message}"); }
    }
}
