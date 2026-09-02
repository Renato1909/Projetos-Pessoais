async function buscar() {
  const r = await fetch("https://jsonplaceholder.typicode.com/todos/1");
  if (!r.ok) throw new Error(`HTTP ${r.status}`);
  const data = await r.json() as { title: string; completed: boolean };
  console.log(`Título: ${data.title} | Feita: ${data.completed}`);
}
buscar().catch(e => console.error("Erro:", e.message));
