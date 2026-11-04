import { describe, it, expect, beforeAll, afterAll } from "vitest";
import { WebSocket } from "ws";
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { createServer } from "node:http";
import { WebSocketServer } from "ws";
import { openDb, saveMessage, listMessages } from "../src/db.js";

let server: any;
let wss: any;
let port = 3457;
let tmpDir: string;

function createTestServer(p: number) {
  const httpServer = createServer((req, res) => {
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
    res.writeHead(404, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ error: "not found" }));
  });
  const wssLocal = new WebSocketServer({ server: httpServer });
  type Client = { ws: any; room: string; user: string };
  const clients = new Set<Client>();
  function broadcast(room: string, payload: unknown, except?: any) {
    const msg = JSON.stringify(payload);
    for (const c of clients) if (c.room === room && c.ws !== except && c.ws.readyState === WebSocket.OPEN) c.ws.send(msg);
  }
  wssLocal.on("connection", (ws: any, req: any) => {
    const url = new URL(req.url || "/", `http://${req.headers.host}`);
    const room = url.searchParams.get("room") || "geral";
    const user = url.searchParams.get("user") || "anon";
    const client: Client = { ws, room, user };
    clients.add(client);
    ws.send(JSON.stringify({ type: "history", messages: listMessages(room) }));
    broadcast(room, { type: "join", user, room }, ws);
    ws.on("message", (raw: any) => {
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
    });
  });
  return { httpServer, wssLocal };
}

beforeAll(async () => {
  tmpDir = mkdtempSync(join(tmpdir(), "chat-test-"));
  openDb(join(tmpDir, "test.db"));
  const app = createTestServer(port);
  server = app.httpServer;
  wss = app.wssLocal;
  await new Promise<void>(res => server.listen(port, res));
}, 10000);

afterAll(async () => {
  await new Promise<void>(res => wss.close(() => res()));
  await new Promise<void>(res => server.close(() => res()));
  try { rmSync(tmpDir, { recursive: true, force: true }); } catch {}
});

function connect(room: string, user: string): Promise<WebSocket> {
  return new Promise((resolve, reject) => {
    const ws = new WebSocket(`ws://localhost:${port}?room=${room}&user=${user}`);
    ws.once("open", () => resolve(ws));
    ws.once("error", reject);
  });
}

function onceMessage(ws: WebSocket): Promise<any> {
  return new Promise(resolve => ws.once("message", d => resolve(JSON.parse(d.toString()))));
}

describe("chat realtime", () => {
  it("health responde ok", async () => {
    const r = await fetch(`http://localhost:${port}/health`);
    expect(r.status).toBe(200);
    expect(await r.json()).toEqual({ status: "ok" });
  });

  it("broadcast entre dois clientes na mesma sala", async () => {
    const a = await connect("sala1", "alice");
    const b = await connect("sala1", "bob");
    await new Promise(r => setTimeout(r, 200));
    a.removeAllListeners("message");
    b.removeAllListeners("message");
    const p = onceMessage(b);
    a.send(JSON.stringify({ type: "message", text: "ola bob" }));
    const msg = await p;
    expect(msg.type).toBe("message");
    expect(msg.text).toBe("ola bob");
    expect(msg.user).toBe("alice");
    a.close(); b.close();
  });

  it("isolamento por sala", async () => {
    const a = await connect("salaA", "alice");
    const b = await connect("salaB", "bob");
    await new Promise(r => setTimeout(r, 200));
    a.removeAllListeners("message");
    b.removeAllListeners("message");
    let got = false;
    b.on("message", () => { got = true; });
    a.send(JSON.stringify({ type: "message", text: "so salaA" }));
    await new Promise(r => setTimeout(r, 400));
    expect(got).toBe(false);
    a.close(); b.close();
  });

  it("history persiste", async () => {
    const a = await connect("hist", "alice");
    await new Promise(r => setTimeout(r, 150));
    a.removeAllListeners("message");
    a.send(JSON.stringify({ type: "message", text: "primeira" }));
    await new Promise(r => setTimeout(r, 200));
    a.close();
    const r = await fetch(`http://localhost:${port}/api/history/hist`);
    const msgs = await r.json() as any[];
    expect(msgs.some(m => m.text === "primeira")).toBe(true);
  });
});
