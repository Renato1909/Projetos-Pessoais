import { createServer } from "node:http";
import { readFileSync, existsSync } from "node:fs";
import { join, extname } from "node:path";
import { WebSocketServer, WebSocket } from "ws";
import { openDb, saveMessage, listMessages } from "./db.js";

const PORT = Number(process.env.PORT || 3000);
openDb(process.env.DB_PATH || "data/chat.db");

const mime: Record<string, string> = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".json": "application/json",
};

const server = createServer((req, res) => {
  const url = new URL(req.url || "/", `http://${req.headers.host}`);
  if (url.pathname === "/health") {
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ status: "ok" }));
    return;
  }
  if (url.pathname.startsWith("/api/history/")) {
    const room = decodeURIComponent(url.pathname.slice("/api/history/".length) || "geral");
    const msgs = listMessages(room);
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify(msgs));
    return;
  }
  let file = url.pathname === "/" ? "/index.html" : url.pathname;
  const full = join(process.cwd(), "public", file);
  if (existsSync(full)) {
    res.writeHead(200, { "Content-Type": mime[extname(full)] || "application/octet-stream" });
    res.end(readFileSync(full));
    return;
  }
  res.writeHead(404, { "Content-Type": "application/json" });
  res.end(JSON.stringify({ error: "not found" }));
});

const wss = new WebSocketServer({ server });

type Client = { ws: WebSocket; room: string; user: string };

const clients = new Set<Client>();

function broadcast(room: string, payload: unknown, except?: WebSocket) {
  const msg = JSON.stringify(payload);
  for (const c of clients) if (c.room === room && c.ws !== except && c.ws.readyState === WebSocket.OPEN) c.ws.send(msg);
}

wss.on("connection", (ws, req) => {
  const url = new URL(req.url || "/", `http://${req.headers.host}`);
  const room = url.searchParams.get("room") || "geral";
  const user = url.searchParams.get("user") || "anon";
  const client: Client = { ws, room, user };
  clients.add(client);

  ws.send(JSON.stringify({ type: "history", messages: listMessages(room) }));
  broadcast(room, { type: "join", user, room }, ws);
  console.log(`[ws] ${user} entrou em #${room}`);

  ws.on("message", (raw) => {
    try {
      const data = JSON.parse(raw.toString());
      if (data.type !== "message" || typeof data.text !== "string" || !data.text.trim()) return;
      const text = data.text.trim().slice(0, 500);
      const saved = saveMessage(room, user, text);
      broadcast(room, { type: "message", ...saved });
    } catch {}
  });

  ws.on("close", () => {
    clients.delete(client);
    broadcast(room, { type: "leave", user, room });
    console.log(`[ws] ${user} saiu de #${room}`);
  });
});

server.listen(PORT, () => console.log(`chat em http://localhost:${PORT}  ws://localhost:${PORT}?room=geral&user=anon`));
