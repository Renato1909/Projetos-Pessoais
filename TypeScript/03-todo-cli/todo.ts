declare const process: any;
interface Tarefa { id: number; titulo: string; feita: boolean; }
let tarefas: Tarefa[] = [];
let nextId = 1;

const [cmd, ...rest] = process.argv.slice(2);
const arg = rest.join(" ");

switch (cmd) {
  case "add": tarefas.push({ id: nextId++, titulo: arg, feita: false }); console.log("Adicionado."); break;
  case "ls": tarefas.forEach(t => console.log(`${t.id}. [${t.feita ? "x" : " "}] ${t.titulo}`)); break;
  default: console.log("Comandos: add <titulo> | ls  (ex: npx tsx todo.ts add \"Estudar TS\")");
}
// Nota: lista em memória (próximo nível: salvar em JSON com fs)


