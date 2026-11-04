package store

import (
	"context"
	"database/sql"
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"sync"
	"time"

	_ "modernc.org/sqlite"

	"github.com/Renato1909/url-shortener-go/internal/shortener"
)

const maxCreateAttempts = 5

var ErrNotFound = errors.New("codigo nao encontrado")

type Entry struct {
	Code      string    `json:"code"`
	LongURL   string    `json:"long_url"`
	Clicks    int64     `json:"clicks"`
	CreatedAt time.Time `json:"created_at"`
}

type Store struct {
	db    *sql.DB
	mu    sync.RWMutex
	cache map[string]Entry
}

func Open(path string) (*Store, error) {
	if dir := filepath.Dir(path); dir != "." && dir != "" {
		if err := os.MkdirAll(dir, 0o755); err != nil {
			return nil, fmt.Errorf("criando diretorio do banco: %w", err)
		}
	}

	dsn := path + "?_pragma=busy_timeout(5000)&_pragma=journal_mode(WAL)"
	db, err := sql.Open("sqlite", dsn)
	if err != nil {
		return nil, fmt.Errorf("abrindo sqlite: %w", err)
	}
	db.SetMaxOpenConns(1)

	const schema = `
CREATE TABLE IF NOT EXISTS urls (
	code       TEXT PRIMARY KEY,
	long_url   TEXT NOT NULL,
	clicks     INTEGER NOT NULL DEFAULT 0,
	created_at TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_urls_long_url ON urls(long_url);`
	if _, err := db.Exec(schema); err != nil {
		db.Close()
		return nil, fmt.Errorf("criando schema: %w", err)
	}

	return &Store{db: db, cache: make(map[string]Entry)}, nil
}

func (s *Store) Close() error { return s.db.Close() }

func isUniqueViolation(err error) bool {
	return err != nil && strings.Contains(err.Error(), "UNIQUE constraint failed")
}

func (s *Store) Create(ctx context.Context, longURL string) (Entry, error) {
	for attempt := 0; attempt < maxCreateAttempts; attempt++ {
		code, err := shortener.NewCode()
		if err != nil {
			return Entry{}, err
		}
		entry := Entry{Code: code, LongURL: longURL, CreatedAt: time.Now().UTC()}
		_, err = s.db.ExecContext(ctx,
			`INSERT INTO urls (code, long_url, clicks, created_at) VALUES (?, ?, 0, ?)`,
			entry.Code, entry.LongURL, entry.CreatedAt)
		if isUniqueViolation(err) {
			continue
		}
		if err != nil {
			return Entry{}, fmt.Errorf("inserindo url: %w", err)
		}
		s.mu.Lock()
		s.cache[entry.Code] = entry
		s.mu.Unlock()
		return entry, nil
	}
	return Entry{}, errors.New("esgotaram-se as tentativas de gerar codigo unico")
}

func (s *Store) Resolve(ctx context.Context, code string) (Entry, error) {
	s.mu.RLock()
	e, ok := s.cache[code]
	s.mu.RUnlock()
	if ok {
		return e, nil
	}

	var dbEntry Entry
	err := s.db.QueryRowContext(ctx,
		`SELECT code, long_url, clicks, created_at FROM urls WHERE code = ?`, code).
		Scan(&dbEntry.Code, &dbEntry.LongURL, &dbEntry.Clicks, &dbEntry.CreatedAt)
	if errors.Is(err, sql.ErrNoRows) {
		return Entry{}, ErrNotFound
	}
	if err != nil {
		return Entry{}, fmt.Errorf("consultando url: %w", err)
	}

	s.mu.Lock()
	s.cache[dbEntry.Code] = dbEntry
	s.mu.Unlock()
	return dbEntry, nil
}

func (s *Store) IncrementClicks(ctx context.Context, code string) error {
	res, err := s.db.ExecContext(ctx,
		`UPDATE urls SET clicks = clicks + 1 WHERE code = ?`, code)
	if err != nil {
		return fmt.Errorf("incrementando cliques: %w", err)
	}
	if n, _ := res.RowsAffected(); n == 0 {
		return ErrNotFound
	}

	s.mu.Lock()
	if e, ok := s.cache[code]; ok {
		e.Clicks++
		s.cache[code] = e
	}
	s.mu.Unlock()
	return nil
}
