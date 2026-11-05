// Package complexidade exerce o tema 01 da trilha: contar o trabalho de um ciclo
// antes de falar da sua classe.
//
// Cada exercicio tem duas versoes, espelhadas nas outras tres linguagens da trilha:
// a pura, que os benchmarks cronometram, e a contada, que incrementa um Contador por
// operacao basica para que os testes afirmem o numero exato de iteracoes.
package complexidade

// Contador registra quantas operacoes basicas um ciclo executou.
type Contador struct {
	Iteracoes   int64
	Comparacoes int64
}

// SomaAte acumula 0 + 1 + ... + (n-1). Roda exatamente n iteracoes.
func SomaAte(n int) int {
	total := 0
	for i := range n {
		total += i
	}
	return total
}

// SomaAteContado faz o mesmo ciclo de SomaAte e conta cada iteracao.
func SomaAteContado(n int, cont *Contador) int {
	total := 0
	for i := range n {
		cont.Iteracoes++
		total += i
	}
	return total
}

// TemRepetido compara todos os pares ate encontrar uma repeticao.
func TemRepetido(valores []int) bool {
	n := len(valores)
	for i := range n {
		for j := i + 1; j < n; j++ {
			if valores[i] == valores[j] {
				return true
			}
		}
	}
	return false
}

// TemRepetidoContado conta as comparacoes feitas ate decidir.
func TemRepetidoContado(valores []int, cont *Contador) bool {
	n := len(valores)
	for i := range n {
		for j := i + 1; j < n; j++ {
			cont.Comparacoes++
			if valores[i] == valores[j] {
				return true
			}
		}
	}
	return false
}

// QuantasMetades conta quantas divisoes por 2 levam de n ate 1; zero quando n <= 1.
func QuantasMetades(n int) int {
	passos := 0
	for n > 1 {
		n /= 2
		passos++
	}
	return passos
}

// QuantasMetadesContado faz o mesmo ciclo e registra cada divisao.
func QuantasMetadesContado(n int, cont *Contador) int {
	passos := 0
	for n > 1 {
		cont.Iteracoes++
		n /= 2
		passos++
	}
	return passos
}

// ParesSobreMetades compoe os dois ciclos anteriores: n/2 passos externas, cada um
// varrendo as metades de n. Da a forma n log n sem decorar formula.
func ParesSobreMetades(n int) int {
	total := 0
	for range n / 2 {
		total += QuantasMetades(n)
	}
	return total
}

// ParesSobreMetadesContado conta apenas o ciclo interno, que e o trabalho dominante.
func ParesSobreMetadesContado(n int, cont *Contador) int {
	total := 0
	for range n / 2 {
		m := n
		for m > 1 {
			cont.Iteracoes++
			m /= 2
			total++
		}
	}
	return total
}
