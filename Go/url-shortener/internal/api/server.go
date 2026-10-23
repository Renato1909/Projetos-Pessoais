package api

import (
	"context"
	"encoding/json"
	"errors"
	"log/slog"
	"net/http"
	"time"

	"github.com/Renato1909/url-shortener-go/internal/shortener"
	"github.com/Renato1909/url-shortener-go/internal/store"
)

const maxBodyBytes = 64 << 10

type Server struct {
	store   *store.Store
	baseURL string
}

func New(st *store.Store, baseURL string) *Server {
	return &Server{store: st, baseURL: baseURL}
}

func (s *Server) Handler() http.Handler {
	mux := http.NewServeMux()
	mux.HandleFunc("GET /health", s.handleHealth)
	mux.HandleFunc("POST /api/shorten", s.handleShorten)
	mux.HandleFunc("GET /{code}", s.handleRedirect)
	mux.HandleFunc("GET /{code}/stats", s.handleStats)
	return s.logRequests(mux)
}

func (s *Server) handleHealth(w http.ResponseWriter, _ *http.Request) {
	writeJSON(w, http.StatusOK, map[string]string{"status": "ok"})
}

type shortenRequest struct {
	URL string `json:"url"`
}

type shortenResponse struct {
	Code     string `json:"code"`
	LongURL  string `json:"long_url"`
	ShortURL string `json:"short_url"`
}

func (s *Server) handleShorten(w http.ResponseWriter, r *http.Request) {
	r.Body = http.MaxBytesReader(w, r.Body, maxBodyBytes)

	var req shortenRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeError(w, http.StatusBadRequest, "corpo JSON invalido")
		return
	}

	longURL, err := shortener.NormalizeURL(req.URL)
	if err != nil {
		writeError(w, http.StatusBadRequest, err.Error())
		return
	}

	ctx, cancel := contextWithTimeout(r)
	defer cancel()

	entry, err := s.store.Create(ctx, longURL)
	if err != nil {
		slog.Error("criando url curta", "err", err)
		writeError(w, http.StatusInternalServerError, "erro interno")
		return
	}

	writeJSON(w, http.StatusCreated, shortenResponse{
		Code:     entry.Code,
		LongURL:  entry.LongURL,
		ShortURL: s.baseURL + "/" + entry.Code,
	})
}

func (s *Server) handleRedirect(w http.ResponseWriter, r *http.Request) {
	code := r.PathValue("code")
	if !shortener.IsValidCode(code) {
		writeError(w, http.StatusNotFound, "codigo nao encontrado")
		return
	}

	ctx, cancel := contextWithTimeout(r)
	defer cancel()

	entry, err := s.store.Resolve(ctx, code)
	if errors.Is(err, store.ErrNotFound) {
		writeError(w, http.StatusNotFound, "codigo nao encontrado")
		return
	}
	if err != nil {
		slog.Error("resolvendo codigo", "err", err)
		writeError(w, http.StatusInternalServerError, "erro interno")
		return
	}

	if err := s.store.IncrementClicks(ctx, code); err != nil {
		slog.Warn("incrementando cliques", "code", code, "err", err)
	}

	http.Redirect(w, r, entry.LongURL, http.StatusFound)
}

func (s *Server) handleStats(w http.ResponseWriter, r *http.Request) {
	code := r.PathValue("code")
	if !shortener.IsValidCode(code) {
		writeError(w, http.StatusNotFound, "codigo nao encontrado")
		return
	}

	ctx, cancel := contextWithTimeout(r)
	defer cancel()

	entry, err := s.store.Resolve(ctx, code)
	if errors.Is(err, store.ErrNotFound) {
		writeError(w, http.StatusNotFound, "codigo nao encontrado")
		return
	}
	if err != nil {
		slog.Error("consultando estatisticas", "err", err)
		writeError(w, http.StatusInternalServerError, "erro interno")
		return
	}

	writeJSON(w, http.StatusOK, entry)
}

func (s *Server) logRequests(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()
		rec := &statusRecorder{ResponseWriter: w, status: http.StatusOK}
		next.ServeHTTP(rec, r)
		slog.Info("request",
			"method", r.Method,
			"path", r.URL.Path,
			"status", rec.status,
			"dur_ms", time.Since(start).Milliseconds(),
			"ip", clientIP(r))
	})
}

type statusRecorder struct {
	http.ResponseWriter
	status int
	wrote  bool
}

func (r *statusRecorder) WriteHeader(code int) {
	if !r.wrote {
		r.status = code
		r.wrote = true
	}
	r.ResponseWriter.WriteHeader(code)
}

func clientIP(r *http.Request) string {
	host := r.RemoteAddr
	if i := len(host) - 1; i >= 0 {
		for ; i >= 0 && host[i] != ':'; i-- {
		}
		if i > 0 {
			return host[:i]
		}
	}
	return host
}

func contextWithTimeout(r *http.Request) (context.Context, context.CancelFunc) {
	return context.WithTimeout(r.Context(), 3*time.Second)
}
func writeJSON(w http.ResponseWriter, status int, v any) {
	w.Header().Set("Content-Type", "application/json; charset=utf-8")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(v)
}

func writeError(w http.ResponseWriter, status int, msg string) {
	writeJSON(w, status, map[string]string{"error": msg})
}
