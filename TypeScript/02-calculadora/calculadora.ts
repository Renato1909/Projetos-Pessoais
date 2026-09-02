declare const process: any;
type Op = '+' | '-' | '*' | '/';

function calcular(a: number, b: number, op: Op): number {
  switch (op) {
    case '+': return a + b;
    case '-': return a - b;
    case '*': return a * b;
    case '/': if (b === 0) throw new Error("Divisão por zero"); return a / b;
  }
}

const [a, op, b] = process.argv.slice(2);
if (!a || !op || !b) { console.log("Uso: npx tsx calculadora.ts <num> <op> <num>  ex: 10 * 3"); process.exit(1); }
try {
  console.log(`Resultado: ${calcular(Number(a), Number(b), op as Op)}`);
} catch (e: any) { console.error("Erro:", e.message); }


