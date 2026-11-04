package api

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"github.com/Renato1909/url-shortener-go/internal/store"
)

type testEnv struct {
	t      *testing.T
	ts     *httptest.Server
	client *http.Client
}

func newTestEnv(t *testing.T) *testEnv {
	t.Helper()
	st, err := store.Open(t.TempDir() + "/api.db")
	if err != nil {
		t.Fatalf("abrindo store: %v", err)
	}
	t.Cleanup(func() { st.Close() })

	ts := httptest.NewServer(New(st, "http://test.local").Handler())
	t.Cleanup(ts.Close)

	return &testEnv{
		t:  t,
		ts: ts,
		client: &http.Client{
			CheckRedirect: func(_ *http.Request, _ []*http.Request) error {
				return http.ErrUseLastResponse
			},
		},
	}
}

func (e *testEnv) do(method, path, body string) (*http.Response, map[string]any) {
	e.t.Helper()
	var rdr *strings.Reader
	if body != "" {
		rdr = strings.NewReader(body)
	} else {
		rdr = strings.NewReader("")
	}
	req, err := http.NewRequest(method, e.ts.URL+path, rdr)
	if err != nil {
		e.t.Fatalf("montando request: %v", err)
	}
	if body != "" {
		req.Header.Set("Content-Type", "application/json")
	}

	resp, err := e.client.Do(req)
	if err != nil {
		e.t.Fatalf("executando request: %v", err)
	}
	defer resp.Body.Close()

	var out map[string]any
	if err := json.NewDecoder(resp.Body).Decode(&out); err != nil && !errors.Is(err, fmt.Errorf("")) {
		out = nil
	}
	return resp, out
}

func TestShortenFlow(t *testing.T) {
	env := newTestEnv(t)

	resp, body := env.do(http.MethodPost, "/api/shorten", `{"url":"https://exemplo.com/pagina?a=1"}`)
	if resp.StatusCode != http.StatusCreated {
		t.Fatalf("status = %d; want 201", resp.StatusCode)
	}
	code, _ := body["code"].(string)
	if len(code) != 7 {
		t.Fatalf("code invalido no corpo: %v", code)
	}
	if short, _ := body["short_url"].(string); short != "http://test.local/"+code {
		t.Errorf("short_url = %v", body["short_url"])
	}

	resp2, _ := env.do(http.MethodGet, "/"+code, "")
	if resp2.StatusCode != http.StatusFound {
		t.Fatalf("redirect status = %d; want 302", resp2.StatusCode)
	}
	if loc := resp2.Header.Get("Location"); loc != "https://exemplo.com/pagina?a=1" {
		t.Errorf("Location = %q", loc)
	}

	resp3, stats := env.do(http.MethodGet, "/"+code+"/stats", "")
	if resp3.StatusCode != http.StatusOK {
		t.Fatalf("stats status = %d; want 200", resp3.StatusCode)
	}
	if clicks, _ := stats["clicks"].(float64); clicks != 1 {
		t.Errorf("clicks = %v; want 1", stats["clicks"])
	}
	if longURL, _ := stats["long_url"].(string); longURL != "https://exemplo.com/pagina?a=1" {
		t.Errorf("long_url = %v", stats["long_url"])
	}
}

func TestShortenNormalizesFragment(t *testing.T) {
	env := newTestEnv(t)
	_, body := env.do(http.MethodPost, "/api/shorten", `{"url":"https://exemplo.com/x#topo"}`)
	longURL, _ := body["long_url"].(string)
	if strings.Contains(longURL, "#") {
		t.Errorf("fragmento deveria ser removido: %q", longURL)
	}
}

func TestShortenInvalidInputs(t *testing.T) {
	env := newTestEnv(t)

	cases := []struct {
		name string
		body string
	}{
		{"sem esquema", `{"url":"exemplo.com"}`},
		{"ftp", `{"url":"ftp://x.com/a"}`},
		{"vazio", `{"url":""}`},
		{"json quebrado", `{invalido`},
	}
	for _, c := range cases {
		resp, _ := env.do(http.MethodPost, "/api/shorten", c.body)
		if resp.StatusCode != http.StatusBadRequest {
			t.Errorf("%s: status = %d; want 400", c.name, resp.StatusCode)
		}
	}
}

func TestUnknownCodeReturns404(t *testing.T) {
	env := newTestEnv(t)

	for _, path := range []string{"/aaaaaaa", "/aaaaaaa/stats"} {
		resp, _ := env.do(http.MethodGet, path, "")
		if resp.StatusCode != http.StatusNotFound {
			t.Errorf("%s: status = %d; want 404", path, resp.StatusCode)
		}
	}
}

func TestMalformedCodeFormatIs404(t *testing.T) {
	env := newTestEnv(t)

	for _, path := range []string{"/curto", "/com!caracter@invalido"} {
		resp, _ := env.do(http.MethodGet, path, "")
		if resp.StatusCode != http.StatusNotFound {
			t.Errorf("%s: status = %d; want 404", path, resp.StatusCode)
		}
	}
}

func TestMethodNotAllowedOnShorten(t *testing.T) {
	env := newTestEnv(t)
	resp, _ := env.do(http.MethodGet, "/api/shorten", "")
	if resp.StatusCode != http.StatusMethodNotAllowed {
		t.Errorf("status = %d; want 405", resp.StatusCode)
	}
}

func TestHealthEndpoint(t *testing.T) {
	env := newTestEnv(t)
	resp, body := env.do(http.MethodGet, "/health", "")
	if resp.StatusCode != http.StatusOK {
		t.Fatalf("status = %d; want 200", resp.StatusCode)
	}
	if status, _ := body["status"].(string); status != "ok" {
		t.Errorf("status body = %v", body["status"])
	}
}

func TestBodySizeLimit(t *testing.T) {
	env := newTestEnv(t)

	huge := bytes.Repeat([]byte("a"), 100<<10)
	payload, err := json.Marshal(map[string]string{"url": "https://exemplo.com/" + string(huge)})
	if err != nil {
		t.Fatalf("marshal: %v", err)
	}

	req, _ := http.NewRequest(http.MethodPost, env.ts.URL+"/api/shorten", bytes.NewReader(payload))
	req.Header.Set("Content-Type", "application/json")
	resp, err := env.client.Do(req)
	if err != nil {
		t.Fatalf("do: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusBadRequest {
		t.Errorf("status = %d; want 400", resp.StatusCode)
	}
}
