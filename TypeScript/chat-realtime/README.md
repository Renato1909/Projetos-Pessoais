# chat-realtime-ts

![CI](https://github.com/Renato1909/chat-realtime-ts/actions/workflows/ci.yml/badge.svg)
![Node](https://img.shields.io/badge/Node-24%2B-339933)
![TypeScript](https://img.shields.io/badge/TypeScript-5.6-3178C6)
![SQLite](https://img.shields.io/badge/SQLite-node%3Asqlite-lightgrey)

Chat em **tempo real** com **WebSockets** (`ws`), salas, histórico persistido em **SQLite nativo do Node 24** (`node:sqlite`) e front minimalista.

## Destaques técnicos

- **WS por sala** (`?room=geral&user=anon`) com `join/leave` + `broadcast` isolado
- **Persistência** `DatabaseSync` sem dependência nativa (sem `better-sqlite3`/`node-gyp`)
- **REST** `GET /api/history/:room` + `GET /health`
- **Front vanilla** `public/index.html` consome WS direto
- Testes **vitest + ws client** (4 cenários: health, broadcast, isolamento, persistência)

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/health` | health check |
| GET | `/api/history/:room` | histórico JSON da sala |
| WS | `ws://host/?room=X&user=Y` | `{"type":"message","text":"..."}` ↔ `{"type":"message",...}` |

Mensagens WS: `history` (ao conectar), `message`, `join`, `leave`.

## Como rodar

Requisitos: Node 24+

```powershell
npm install
npm run dev      # tsx watch src/server.ts  → http://localhost:3000
npm run build; npm start  # build tsc
```

Variáveis: `PORT` (default 3000), `DB_PATH` (default `data/chat.db`).

## Como testar

```powershell
npm test         # vitest run
```

## Arquitetura

```
src/
├── server.ts  # http + ws, roteamento REST, broadcast por sala
└── db.ts      # node:sqlite, saveMessage/listMessages
public/
└── index.html # front WS
tests/
└── chat.test.ts # 4 testes integrados (health, broadcast, isolamento, history)
```

## Limitações (por design)

- Sem auth real (user via query)
- Histórico limitado a 50 msgs por sala
- Sem rate limiting

## Roadmap

- [ ] Auth JWT no handshake WS
- [ ] Paginação `/api/history?limit&before`
- [ ] Métricas `/metrics`

## Licença

[MIT](LICENSE)
