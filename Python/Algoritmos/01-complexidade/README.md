# Tema 01 — complexidade e medição (Python)

Exercício e explicação do tema estão em [`docs/ALGORITMOS.md`](../../../docs/ALGORITMOS.md). Esta pasta documenta só o que é específico de Python: como correr e o que saiu aqui.

## Ficheiros

| ficheiro | papel |
|---|---|
| `complexidade.py` | os quatro ciclos, em versão pura e versão contada |
| `medir.py` | imprime a tabela de tempos com mediana de 5 repetições |
| `tests/test_complexidade.py` | afirma o número **exato** de iterações/comparações |

## Como correr

De dentro desta pasta — os testes importam o módulo do tema a partir do diretório atual, e é assim que o CI os executa:

```bash
python -m pytest -q
python medir.py
```

## Ambiente da medição

```
CPython 3.12.10 | Intel64 Family 6 Model 158 Stepping 9, GenuineIntel
Intel Core i3-7100 @ 3,90 GHz (2 núcleos / 4 threads) | Windows 11 | 2026-11-05
```

## Tempos medidos

`medir.py` constrói o input **fora** da zona cronometrada.

| exercício | n | operações previstas | ms (mediana) | razão |
|---|---:|---:|---:|---:|
| `soma_ate` | 100 | 100 | 0,010 | — |
| | 1 000 | 1 000 | 0,039 | 3,7× |
| | 10 000 | 10 000 | 0,411 | 10,6× |
| | 100 000 | 100 000 | 4,397 | 10,7× |
| | 1 000 000 | 1 000 000 | 71,050 | **16,2×** |
| `tem_repetido` | 100 | 4 950 | 0,165 | — |
| | 200 | 19 900 | 0,972 | 5,9× |
| | 500 | 124 750 | 11,460 | 11,8× |
| | 1 000 | 499 500 | 23,532 | **2,1×** |
| | 2 000 | 1 999 000 | 112,869 | 4,8× |
| `quantas_metades` | 2¹⁰ | 10 | 0,001 | — |
| | 2¹⁴ | 14 | 0,001 | 1,4× |
| | 2¹⁸ | 18 | 0,001 | 1,1× |
| | 2²⁴ | 24 | 0,001 | 1,3× |
| | 2³⁰ | 30 | 0,002 | 1,4× |
| `pares_sobre_metades` | 1 000 | 4 500 | 0,245 | — |
| | 10 000 | 65 000 | 4,415 | 18,0× |
| | 100 000 | 800 000 | 76,951 | 17,4× |

## O que estes números não sustentam

Dois pontos fogem da teoria, e ficam aqui em vez de serem limpos:

- **`soma_ate` acelera 16,2× no último degrau, não 10×.** Em `n = 10⁶` o acumulador já passou de 5×10¹¹ e o CPython deixou de somar em palavra de máquina: `int` com mais de um dígito de 30 bits custa mais por iteração, e o custo cresce com o próprio `n`. A função continua linear no número de iterações — o teste que o prova é `test_soma_ate_roda_n_iteracoes` — mas deixou de ser linear em tempo.
- **`tem_repetido` dá 2,1× entre 500 e 1 000**, onde a forma quadrática pede 4×, e 11,8× entre 200 e 500, onde pede 6,25×. Os pontos individuais em CPython são ruidosos: indexação de lista, iteradores e alocação ofuscam a inclinação. A comparação honesta é com a célula de Go, onde a mesma curva sai 3,7× / 6,0× / 4,0× / 4,2×.

Conclusão que o tema 01 tira disto, e que vale para as quatro linguagens: **a contagem exata é a prova; o tempo é a ilustração.** Os milissegundos desta tabela pertencem a um i3 de 2017 e ao interpretador; a coluna das operações é a mesma em qualquer máquina e nas quatro linguagens da trilha.
