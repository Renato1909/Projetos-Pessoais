# Tema 01 — complexidade e medição (C)

Exercício e explicação do tema estão em [`docs/ALGORITMOS.md`](../../../docs/ALGORITMOS.md). Esta pasta documenta só o que é específico de C.

## Ficheiros

| ficheiro | papel |
|---|---|
| `complexidade.h` / `complexidade.c` | os quatro ciclos, em versão pura e versão contada (`Contador`) |
| `tests/test_complexidade.c` | asserções da contagem exata |
| `medir.c` | tabela de medições com mediana de 5 repetições |
| `Makefile` | `test`, `bench`, `clean`; artefactos em `build/` (ignorado) |

## Como correr

As receitas do Makefile são POSIX: no Windows corres a partir do Git Bash ou do MSYS2, com `mingw32-make` em vez de `make`.

```bash
cd C/Algoritmos/01-complexidade
make test          # Windows: mingw32-make test
make bench         # Windows: mingw32-make bench
make clean
```

O CI Ubuntu acrescenta uma passada com sanitizadores, que esta toolchain local não tem:

```bash
make SANITIZE='-fsanitize=address,undefined -fno-omit-frame-pointer' test
```

`gcc` do MSYS2 ucrt64 **não traz o runtime do AddressSanitizer** (linka com `-lasan` e falha), por isso os sanitizadores correm só no job `c-sanitizadores`. A compilação local usa `-std=c11 -Wall -Wextra -Werror -O2`.

## Ambiente da medição

```
gcc 16.2.0 (Rev3, MSYS2) -O2 | GNU Make 4.4.1 (mingw32-make)
Intel Core i3-7100 @ 3,90 GHz (2 núcleos / 4 threads) | Windows 11 | 2026-11-05
```

## Medições

Cada linha repete a chamada um `fator` escolhido para cronometrar ~10⁷ operações; o que se publica é `ns/chamada` (span ÷ fator), a mesma unidade do `ns/op` do Go.

| exercício | n | operações previstas | ns/chamada | razão |
|---|---:|---:|---:|---:|
| `soma_ate` | 100 | 100 | 24,4 | — |
| | 1 000 | 1 000 | 361,0 | 14,8× |
| | 10 000 | 10 000 | 3 849,9 | 10,7× |
| | 100 000 | 100 000 | 38 659,0 | 10,0× |
| | 1 000 000 | 1 000 000 | 386 330,0 | 10,0× |
| `tem_repetido` | 100 | 4 950 | 2 489,6 | — |
| | 200 | 19 900 | 7 716,3 | 3,1× |
| | 500 | 124 750 | 39 075,0 | 5,1× |
| | 1 000 | 499 500 | 144 760,0 | 3,7× |
| | 2 000 | 1 999 000 | 547 000,0 | 3,8× |
| | 5 000 | 12 497 500 | 3 327 900,0 | 6,1× |
| `quantas_metades` | 2¹⁰ | 10 | 5,2 | — |
| | 2¹⁴ | 14 | 6,3 | 1,2× |
| | 2¹⁸ | 18 | 7,5 | 1,2× |
| | 2²⁴ | 24 | 9,2 | 1,2× |
| | 2³⁰ | 30 | 21,6 | **2,4×** |
| `pares_sobre_metades` | 1 000 | 4 500 | 3 114,9 | — |
| | 10 000 | 65 000 | 40 214,4 | 12,9× |
| | 100 000 | 800 000 | 500 858,3 | 12,5× |

## Leitura

- **Linear.** Os três degraus de regime dão 10,7× / 10,0× / 10,0×. O primeiro (14,8×) é o piso do instrumento: 24 ns por chamada já é dominado pelo custo da chamada, não pelo ciclo.
- **Quadrático.** ×2 em `n` dá 3,1× / 3,7× / 3,8× e ×2,5 dá 5,1× e 6,1× contra os 6,25× que a forma pede. O ponto a 3,1× (100 → 200) é o mesmo efeito de piso: 4 950 comparações cabem todas no L1 e a chamada sai barato.
- **Logarítmico.** `n` vai de 2¹⁰ a 2³⁰ — multiplicado por um milhão — e o tempo passa de 5,2 ns para 21,6 ns. Os primeiros quatro degraus são 1,2× cada, exatamente o acréscimo de 4 passos de ciclo; o salto de 2,4× no último degrau (24 → 30 passos) não tem explicação na forma fechada e fica assinalado em vez de maquilhado. Hipótese: com 30 iterações o preditor de ramo passa a acertar o standard do loop, e o ganho de predição não compensa os 6 passos extra no ponto anterior.
- **n log n.** 12,9× e 12,5× por ×10 de `n`, quando linear dá 10× — o excedente é o fator log que cresce de 9 para 16 passos.

## Por que a coluna do meio é a prova

O `pares_sobre_metades` a 500 µs por chamada faz 800 000 iterações: 0,63 ns por iteração. Se o gcc tivesse reconhecido a invariância do ciclo interno e comido a chamada, o tempo seria plano nos três degraus — e é precisamente a escala de ×12,5 que diz que o ciclo correu. Daí os `volatile` nas chamadas de `medir.c`: sem eles, medir um loop que o otimizador eliminou é medir nada.

Comparação entre as quatro células, no mesmo ponto `soma_ate(10⁶)`: C 386 µs, Go 329 µs, Python 71 050 µs. O Python leva 183× mais porque paga um objeto por iteração, não porque o ciclo seja diferente. Essa razão — e não "C é melhor que Python" — é o que o tema 01 tinha para mostrar.
