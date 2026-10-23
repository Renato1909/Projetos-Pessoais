package shortener

import (
	"errors"
	"testing"
)

func TestNormalizeURL(t *testing.T) {
	cases := []struct {
		in      string
		want    string
		wantErr bool
	}{
		{"https://exemplo.com", "https://exemplo.com", false},
		{"http://exemplo.com/pagina?a=1", "http://exemplo.com/pagina?a=1", false},
		{"  https://EXEMPLO.com/Path  ", "https://EXEMPLO.com/Path", false},
		{"https://exemplo.com/#secao", "https://exemplo.com/", false},
		{"exemplo.com", "", true},
		{"ftp://exemplo.com/arq.zip", "", true},
		{"javascript:alert(1)", "", true},
		{"", "", true},
		{"http://", "", true},
	}
	for _, c := range cases {
		got, err := NormalizeURL(c.in)
		if c.wantErr {
			if err == nil || !errors.Is(err, ErrInvalidURL) {
				t.Errorf("NormalizeURL(%q) erro = %v; want ErrInvalidURL", c.in, err)
			}
			continue
		}
		if err != nil {
			t.Errorf("NormalizeURL(%q) erro inesperado: %v", c.in, err)
			continue
		}
		if got != c.want {
			t.Errorf("NormalizeURL(%q) = %q; want %q", c.in, got, c.want)
		}
	}
}
