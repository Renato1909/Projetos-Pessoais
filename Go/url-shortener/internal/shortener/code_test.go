package shortener

import "testing"

func TestNewCode(t *testing.T) {
	seen := make(map[string]bool)
	for i := 0; i < 1000; i++ {
		code, err := NewCode()
		if err != nil {
			t.Fatalf("erro inesperado: %v", err)
		}
		if len(code) != CodeLength {
			t.Fatalf("codigo com tamanho errado: %q", code)
		}
		if !IsValidCode(code) {
			t.Fatalf("codigo fora do alfabeto: %q", code)
		}
		if seen[code] {
			t.Fatalf("codigo duplicado em 1000 geracoes: %q", code)
		}
		seen[code] = true
	}
}

func TestIsValidCode(t *testing.T) {
	cases := []struct {
		in   string
		want bool
	}{
		{"abc123X", true},
		{"0000000", true},
		{"zzzZZZ9", true},
		{"curto", false},
		{"bem-longo-demais", false},
		{"invalid!", false},
		{"", false},
	}
	for _, c := range cases {
		if got := IsValidCode(c.in); got != c.want {
			t.Errorf("IsValidCode(%q) = %v; want %v", c.in, got, c.want)
		}
	}
}
