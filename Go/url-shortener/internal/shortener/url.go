package shortener

import (
	"errors"
	"fmt"
	"net/url"
	"strings"
)

var ErrInvalidURL = errors.New("URL inválida: informe uma URL http(s) completa")

func NormalizeURL(raw string) (string, error) {
	raw = strings.TrimSpace(raw)
	if raw == "" {
		return "", ErrInvalidURL
	}
	u, err := url.Parse(raw)
	if err != nil {
		return "", fmt.Errorf("%w: %v", ErrInvalidURL, err)
	}
	if u.Scheme != "http" && u.Scheme != "https" {
		return "", ErrInvalidURL
	}
	if u.Host == "" {
		return "", ErrInvalidURL
	}
	u.Fragment = ""
	return u.String(), nil
}
