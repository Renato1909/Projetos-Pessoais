# url-shortener-go

![CI](https://github.com/Renato1909/url-shortener-go/actions/workflows/ci.yml/badge.svg)
![Go](https://img.shields.io/badge/Go-1.22%2B-00ADD8)
![Banco](https://img.shields.io/badge/SQLite-WAL-blue)

API REST de **encurtador de URLs** escrita em Go puro, com contador de cliques,
cache em memória e persistência SQLite (driver sem CGO).

## Destaques técnicos

- **Go 1.22+ pattern routing**: `GET /{code}` com `r.PathValue`, sem frameworks
- **Códigos curtos base62** gerados com `crypto/rand` (7 caracteres ≈ 3,5 trilhões de combinações) e tratamento de colisão por retry
- **SQLite em WAL** via `modernc.org/sqlite` — 100% Go, sem CGO, cross-compila fácil
- **Cache read-through** (`sync.RWMutex`): redirecionamentos quentes não tocam no disco
- **Shutdown gracioso** com `signal.NotifyContext` + `server.Shutdown`
- **Observabilidade** com `log/slog`: log estruturado por request (status, duração, IP)
- Testes unitários + integração com `httptest` (incl. limite de body, 404, 405, redirect)
- CI no GitHub Actions com `go vet`, `go test -race` e build

## Endpoints

| Método | Rota              | Descrição                                   |
|--------|-------------------|---------------------------------------------|
| GET    | `/health`         | Health check                                |
| POST   | `/api/shorten`    | Encurta uma URL → `201` + JSON do link      |
| GET    | `/{code}`         | Redireciona `302` para o destino (+1 clique)|
| GET    | `/{code}/stats`   | Estatísticas: cliques, criado em, destino   |

### Exemplos

```bash
# Encurtar
curl -s -X POST http://localhost:8080/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://exemplo.com/pagina?a=1"}'
# {"code":"aB3x9Kp","long_url":"https://exemplo.com/pagina?a=1","short_url":"http://localhost:8080/aB3x9Kp"}

# Redirecionar
curl -i http://localhost:8080/aB3x9Kp
# HTTP/1.1 302 Found
# Location: https://exemplo.com/pagina?a=1

# Estatísticas
curl -s http://localhost:8080/aB3x9Kp/stats
# {"code":"aB3x9Kp","long_url":"https://...","clicks":1,"created_at":"2026-08-23T21:00:00Z"}
```

## Como rodar

Requisitos: Go 1.22+

```powershell
go run ./cmd/server                 # porta padrão 8080, banco em data/shortener.db
```

Variáveis de ambiente opcionais:

| Variável   | Padrão                    | Descrição                        |
|------------|---------------------------|----------------------------------|
| `PORT`     | `8080`                    | Porta HTTP                       |
| `DB_PATH`  | `data/shortener.db`       | Caminho do SQLite                |
| `BASE_URL` | `http://localhost:$PORT`  | Base dos links encurtados        |

## Como testar

```powershell
go test ./...          # toda a suíte
go test -race ./...    # com detector de corridas
make vet               # análise estática
```

## Arquitetura

```
cmd/server/main.go ─── wiring: env → store → api → http.Server
                          │
internal/
├── shortener/      códigos base62 (crypto/rand) + validação de URL
├── store/          SQLite (WAL, single-conn) + cache RWMutex + cliques
└── api/            handlers HTTP, JSON helpers, logging middleware
```

Fluxo do redirecionamento:

```
GET /{code} → cache hit? ──sim──► Location + clicks++
                │ não
                ▼
          SELECT no SQLite ──► popula cache ──► 302
```

## Decisões técnicas

- **Sem framework web**: o router de patterns da stdlib cobre tudo; menos dependência = mais clareza.
- **`302` em vez de `301`**: mantém o código temporário para poder trocar o destino no futuro (roadmap).
- **Driver sem CGO** (`modernc.org/sqlite`): builds simples no Windows/CI, sem exigir GCC.
- **Uma conexão SQL por vez** (`SetMaxOpenConns(1)`): SQLite escreve serialmente; evita `SQLITE_BUSY`.
- **Mesma URL gera códigos diferentes**: simplicidade deliberada; dedupe fica para o roadmap.

## Limitações conhecidas (por design)

- Sem autenticação/rate limiting (roadmap: token simples + sliding window)
- Cache não expira nem invalida entre processos
- Não há API de deleção/atualização ainda

## Roadmap

- [ ] Rate limiting por IP (token bucket)
- [ ] Endpoint `DELETE /{code}`
- [ ] Métricas Prometheus (`/metrics`)
- [ ] Dockerfile multi-stage + deploy

## Licença

[MIT](LICENSE)
