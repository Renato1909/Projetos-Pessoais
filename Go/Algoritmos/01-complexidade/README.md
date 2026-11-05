# Tema 01 — complexidade e medição (Go)

Exercício e explicação do tema estão em [`docs/ALGORITMOS.md`](../../../docs/ALGORITMOS.md). Esta pasta documenta só o que é específico de Go.

Os quatro temas partilham um módulo (`Go/Algoritmos/go.mod`), por causa dos exercícios sem dependências; os projetos consolidados continuam com o seu `go.mod` próprio.

## Ficheiros

| ficheiro | papel |
|---|---|
| `complexidade.go` | os quatro ciclos, em versão pura e versão contada (`Contador`) |
| `complexidade_test.go` | testes de contagem exata + `Benchmark*` por tamanho de input |

## Como correr

```bash
cd Go/Algoritmos
go vet ./...
go test ./...
go test -run '^$' -bench . ./01-complexidade
go test -race ./...        # exige CGO_ENABLED=1 e um gcc no PATH
```

Neste Windows, `-race` precisa de `D:\Dev\MSYS2\ucrt64\bin` no `PATH` e `CGO_ENABLED=1`. Com essa combinação o binário de teste linkado com cgo foi **bloqueado pelo Controle de Aplicativo do Windows** ao ser executado a partir do diretório temporário de build; os benchmarks correm com `CGO_ENABLED=0`, que é o comportamento padrão. No CI Ubuntu as duas coisas funcionam sem ajuste.

## Ambiente da medição

```
goos: windows  goarch: amd64
cpu: Intel(R) Core(TM) i3-7100 CPU @ 3.90GHz  (2 núcleos / 4 threads)
go version go1.26.7 windows/amd64 | 2026-11-05
```

## Benchmarks

| benchmark | n | ops/s | ns/op | razão |
|---|---:|---:|---:|---:|
| `SomaAte` | 100 | 34 772 428 | 53,45 | — |
| | 1 000 | 3 187 725 | 372,9 | 7,0× |
| | 10 000 | 385 735 | 3 057 | 8,2× |
| | 100 000 | 39 147 | 30 343 | 9,9× |
| | 1 000 000 | 4 252 | 329 397 | 10,9× |
| `TemRepetido` | 100 | 323 584 | 3 400 | — |
| | 200 | 95 809 | 12 651 | 3,7× |
| | 500 | 15 957 | 76 407 | 6,0× |
| | 1 000 | 3 786 | 303 322 | 4,0× |
| | 2 000 | 1 017 | 1 277 130 | 4,2× |
| `QuantasMetades` | 2¹⁰ | 261 844 022 | 5,179 | — |
| | 2¹⁴ | 178 360 686 | 6,083 | 1,2× |
| | 2¹⁸ | 169 631 638 | 6,959 | 1,1× |
| | 2²⁴ | 135 880 533 | 9,385 | 1,3× |
| | 2³⁰ | 100 000 000 | 12,00 | 1,3× |
| `ParesSobreMetades` | 1 000 | 514 184 | 2 317 | — |
| | 10 000 | 43 030 | 28 035 | 12,1× |
| | 100 000 | 3 790 | 327 935 | 11,7× |

## Leitura

- **Linear.** Cada ×10 em `n` custa ×8,2 → ×9,9 → ×10,9. Os primeiros degraus (7,0×) estão abaixo de 10× porque 53 ns já é dominado pelo custo fixo da chamada, não pelo ciclo — é o piso de medição, não uma violação da forma.
- **Quadrático.** ×2 em `n` dá 3,7× / 6,0× / 4,0× / 4,2×. O ponto de 500 (6,0× em vez de 4×) é o preço de saltar de 19 900 para 124 750 comparações: sai do cache L1 e entra no ruído. Ainda assim a média dos quatro degraus é 4,0×, que é a assinatura de `n²`.
- **Logarítmico.** `n` multiplicado por 1 048 576 (2¹⁰ → 2³⁰) custa 2,3× em tempo. É o único ponto da tabela em que a curva se pode ver a olho sem estatística.
- **n log n.** ×10 em `n` dá 12,1× e 11,7×, acima dos 10× lineares — o excedente é o fator log que cresce 13→16 passos, exatamente o que a composição dos dois ciclos prevê.

Comparando com a célula de Python: o mesmo `tem_repetido` dá aqui razões estáveis em torno de 4×, e ali 2,1×/11,8×. A diferença não é de algoritmo, é de instrumento — Go compila o ciclo em palavras de máquina com predição de ramo previsível, e o CPython paga um objeto por iteração. É a primeira vez na trilha que a comparação entre linguagens é o resultado, e não um detalhe.
