import { DatabaseSync } from "node:sqlite";
import { mkdirSync } from "node:fs";
import { dirname } from "node:path";

export type Message = { id: number; room: string; user: string; text: string; ts: string };

let db: DatabaseSync;

export function openDb(path = "data/chat.db"): DatabaseSync {
  mkdirSync(dirname(path), { recursive: true });
  db = new DatabaseSync(path);
  db.exec(`
    CREATE TABLE IF NOT EXISTS messages (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      room TEXT NOT NULL,
      user TEXT NOT NULL,
      text TEXT NOT NULL,
      ts TEXT NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_messages_room ON messages(room, id);
  `);
  return db;
}

export function getDb(): DatabaseSync {
  if (!db) return openDb();
  return db;
}

export function saveMessage(room: string, user: string, text: string): Message {
  const ts = new Date().toISOString();
  const d = getDb();
  const r = d.prepare("INSERT INTO messages (room, user, text, ts) VALUES (?, ?, ?, ?)").run(room, user, text, ts);
  return { id: Number(r.lastInsertRowid), room, user, text, ts };
}

export function listMessages(room: string, limit = 50): Message[] {
  const d = getDb();
  return d.prepare("SELECT id, room, user, text, ts FROM messages WHERE room = ? ORDER BY id DESC LIMIT ?").all(room, limit).reverse() as Message[];
}
