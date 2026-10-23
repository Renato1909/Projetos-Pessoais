package store

import (
	"context"
	"errors"
	"testing"

	"github.com/Renato1909/url-shortener-go/internal/shortener"
)

func openTestStore(t *testing.T) *Store {
	t.Helper()
	st, err := Open(t.TempDir() + "/test.db")
	if err != nil {
		t.Fatalf("abrindo store: %v", err)
	}
	t.Cleanup(func() { st.Close() })
	return st
}

func TestCreateAndResolve(t *testing.T) {
	st := openTestStore(t)
	ctx := context.Background()

	e, err := st.Create(ctx, "https://exemplo.com/pagina")
	if err != nil {
		t.Fatalf("Create: %v", err)
	}
	if len(e.Code) != shortener.CodeLength || !shortener.IsValidCode(e.Code) {
		t.Fatalf("codigo invalido gerado: %q", e.Code)
	}

	got, err := st.Resolve(ctx, e.Code)
	if err != nil {
		t.Fatalf("Resolve: %v", err)
	}
	if got.LongURL != "https://exemplo.com/pagina" {
		t.Errorf("long_url = %q; want %q", got.LongURL, "https://exemplo.com/pagina")
	}
	if got.Clicks != 0 {
		t.Errorf("clicks = %d; want 0", got.Clicks)
	}
	if got.CreatedAt.IsZero() {
		t.Error("created_at deveria estar preenchido")
	}
}

func TestSameURLGetsDistinctCodes(t *testing.T) {
	st := openTestStore(t)
	ctx := context.Background()

	a, err := st.Create(ctx, "https://exemplo.com/x")
	if err != nil {
		t.Fatalf("Create a: %v", err)
	}
	b, err := st.Create(ctx, "https://exemplo.com/x")
	if err != nil {
		t.Fatalf("Create b: %v", err)
	}
	if a.Code == b.Code {
		t.Errorf("codigos iguais para mesma URL: %s", a.Code)
	}
}

func TestClicksIncrement(t *testing.T) {
	st := openTestStore(t)
	ctx := context.Background()
	e, _ := st.Create(ctx, "https://exemplo.com/y")

	for i := 0; i < 3; i++ {
		if err := st.IncrementClicks(ctx, e.Code); err != nil {
			t.Fatalf("IncrementClicks %d: %v", i+1, err)
		}
	}

	got, err := st.Resolve(ctx, e.Code)
	if err != nil {
		t.Fatalf("Resolve: %v", err)
	}
	if got.Clicks != 3 {
		t.Errorf("clicks = %d; want 3", got.Clicks)
	}
}

func TestResolveUnknownCode(t *testing.T) {
	st := openTestStore(t)

	if _, err := st.Resolve(context.Background(), "aaaaaaa"); !errors.Is(err, ErrNotFound) {
		t.Errorf("erro = %v; want ErrNotFound", err)
	}
}

func TestCacheSurvivesStoreReopen(t *testing.T) {
	dir := t.TempDir()
	path := dir + "/persist.db"

	st1, err := Open(path)
	if err != nil {
		t.Fatalf("Open 1: %v", err)
	}
	e, err := st1.Create(context.Background(), "https://exemplo.com/z")
	if err != nil {
		t.Fatalf("Create: %v", err)
	}
	st1.Close()

	st2, err := Open(path)
	if err != nil {
		t.Fatalf("Open 2: %v", err)
	}
	defer st2.Close()

	if _, err := st2.Resolve(context.Background(), e.Code); err != nil {
		t.Errorf("persistencia falhou apos reabrir: %v", err)
	}
}
