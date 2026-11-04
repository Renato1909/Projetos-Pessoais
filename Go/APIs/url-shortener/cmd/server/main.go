package main

import (
	"context"
	"errors"
	"log/slog"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/Renato1909/url-shortener-go/internal/api"
	"github.com/Renato1909/url-shortener-go/internal/store"
)

func envOr(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}

func main() {
	slog.SetDefault(slog.New(slog.NewTextHandler(os.Stdout, nil)))

	port := envOr("PORT", "8080")
	dbPath := envOr("DB_PATH", "data/shortener.db")
	baseURL := envOr("BASE_URL", "http://localhost:"+port)

	st, err := store.Open(dbPath)
	if err != nil {
		slog.Error("abrindo banco de dados", "err", err)
		os.Exit(1)
	}
	defer st.Close()

	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
	defer stop()

	srv := &http.Server{
		Addr:              ":" + port,
		Handler:           api.New(st, baseURL).Handler(),
		ReadHeaderTimeout: 5 * time.Second,
		ReadTimeout:       10 * time.Second,
		WriteTimeout:      15 * time.Second,
		IdleTimeout:       60 * time.Second,
	}

	errCh := make(chan error, 1)
	go func() {
		slog.Info("servidor ouvindo", "addr", srv.Addr, "db", dbPath, "base_url", baseURL)
		errCh <- srv.ListenAndServe()
	}()

	select {
	case <-ctx.Done():
		slog.Info("sinal recebido, encerrando graciosamente")
		shutdownCtx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
		defer cancel()
		if err := srv.Shutdown(shutdownCtx); err != nil {
			slog.Error("durante o shutdown", "err", err)
		}
	case err := <-errCh:
		if err != nil && !errors.Is(err, http.ErrServerClosed) {
			slog.Error("servidor encerrado com erro", "err", err)
			os.Exit(1)
		}
	}

	slog.Info("servidor finalizado")
}
