package complexidade

import (
	"fmt"
	"testing"
)

// sink impede que o compilador elimine o resultado dos benchmarks.
var sink int

func TestSomaAteRodaNIteracoes(t *testing.T) {
	for _, n := range []int{0, 1, 2, 3, 4, 7, 8, 100, 1024, 10_000} {
		cont := &Contador{}
		if got := SomaAteContado(n, cont); got != n*(n-1)/2 {
			t.Fatalf("SomaAteContado(%d) = %d, queria %d", n, got, n*(n-1)/2)
		}
		if cont.Iteracoes != int64(n) {
			t.Fatalf("n=%d: %d iteracoes, queria %d", n, cont.Iteracoes, n)
		}
		if SomaAte(n) != SomaAteContado(n, &Contador{}) {
			t.Fatalf("n=%d: versao pura divergiu da contada", n)
		}
	}
}

func TestQuantasMetadesContaDivisoesReais(t *testing.T) {
	casos := map[int]int{1: 0, 2: 1, 3: 1, 4: 2, 7: 2, 8: 3, 9: 3, 1024: 10, 1_000_000: 19}
	for n, queria := range casos {
		cont := &Contador{}
		if got := QuantasMetadesContado(n, cont); got != queria {
			t.Fatalf("n=%d: %d passos, queria %d", n, got, queria)
		}
		if cont.Iteracoes != int64(queria) {
			t.Fatalf("n=%d: contador marcou %d, queria %d", n, cont.Iteracoes, queria)
		}
		if QuantasMetades(n) != queria {
			t.Fatalf("n=%d: versao pura deu %d, queria %d", n, QuantasMetades(n), queria)
		}
	}
}

func TestTemRepetidoVarreParesInteirosQuandoNaoHaRepeticao(t *testing.T) {
	for _, n := range []int{0, 1, 2, 3, 4, 7, 8, 100, 250} {
		valores := fazerDistintos(n)
		cont := &Contador{}
		if TemRepetidoContado(valores, cont) {
			t.Fatalf("n=%d: achou repeticao onde nao ha", n)
		}
		if queria := int64(n * (n - 1) / 2); cont.Comparacoes != queria {
			t.Fatalf("n=%d: %d comparacoes, queria %d", n, cont.Comparacoes, queria)
		}
	}
}

func TestTemRepetidoParaNaComparacaoQueDecide(t *testing.T) {
	valores := []int{0, 1, 2, 3, 4, 5, 0}
	cont := &Contador{}
	if !TemRepetidoContado(valores, cont) {
		t.Fatal("nao achou o duplicado no ultimo par")
	}
	if cont.Comparacoes != int64(len(valores)-1) {
		t.Fatalf("%d comparacoes, queria %d", cont.Comparacoes, len(valores)-1)
	}
}

func TestParesSobreMetadesEhNLogNEmContagemExata(t *testing.T) {
	for _, n := range []int{0, 1, 2, 3, 4, 7, 8, 100, 1024, 10_000} {
		cont := &Contador{}
		queria := (n / 2) * QuantasMetades(n)
		if got := ParesSobreMetadesContado(n, cont); got != queria {
			t.Fatalf("n=%d: total %d, queria %d", n, got, queria)
		}
		if cont.Iteracoes != int64(queria) {
			t.Fatalf("n=%d: contador %d, queria %d", n, cont.Iteracoes, queria)
		}
		if ParesSobreMetades(n) != queria {
			t.Fatalf("n=%d: versao pura %d, queria %d", n, ParesSobreMetades(n), queria)
		}
	}
}

func fazerDistintos(n int) []int {
	valores := make([]int, n)
	for i := range valores {
		valores[i] = i
	}
	return valores
}

func BenchmarkSomaAte(b *testing.B) {
	for _, n := range []int{100, 1_000, 10_000, 100_000, 1_000_000} {
		b.Run(fmt.Sprintf("n=%d", n), func(b *testing.B) {
			for range b.N {
				sink += SomaAte(n)
			}
		})
	}
}

func BenchmarkTemRepetido(b *testing.B) {
	for _, n := range []int{100, 200, 500, 1_000, 2_000} {
		b.Run(fmt.Sprintf("n=%d", n), func(b *testing.B) {
			valores := fazerDistintos(n)
			b.ResetTimer()
			for range b.N {
				if TemRepetido(valores) {
					b.Fatal("input de benchmark nao pode ter repeticao")
				}
			}
		})
	}
}

func BenchmarkQuantasMetades(b *testing.B) {
	for _, n := range []int{1 << 10, 1 << 14, 1 << 18, 1 << 24, 1 << 30} {
		b.Run(fmt.Sprintf("n=%d", n), func(b *testing.B) {
			for range b.N {
				sink += QuantasMetades(n)
			}
		})
	}
}

func BenchmarkParesSobreMetades(b *testing.B) {
	for _, n := range []int{1_000, 10_000, 100_000} {
		b.Run(fmt.Sprintf("n=%d", n), func(b *testing.B) {
			for range b.N {
				sink += ParesSobreMetades(n)
			}
		})
	}
}
