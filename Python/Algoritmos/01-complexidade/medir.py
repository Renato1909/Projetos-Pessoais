"""Cronometra os quatro exercicios do tema 01 e imprime a tabela do README.

Correr de dentro da pasta do tema:  python medir.py

Publicamos a mediana de 5 repeticoes. A leitura util e a razao entre pontos
consecutivos: input x10 com tempo x~10 e curva linear, x~100 e quadratica. Os
valores absolutos pertencem a esta maquina e a estas flags, por isso o README da
celula registra onde foi medido.

Os dados de entrada sao construidos ANTES da zona cronometrada. Incluir o build
dentro do tempo misturaria o O(n) de montar a lista com o que se quer medir.
"""

from __future__ import annotations

import platform
import statistics
import sys
import time
from typing import Callable

from complexidade import (
    pares_sobre_metades,
    quantas_metades,
    soma_ate,
    tem_repetido,
)

REPETICOES = 5
CASO = tuple[int, object, int]


def mediar(chamada: Callable[[], object]) -> float:
    """Milissegundos da mediana de REPETICOES chamadas."""
    tempos = []
    for _ in range(REPETICOES):
        inicio = time.perf_counter()
        chamada()
        tempos.append((time.perf_counter() - inicio) * 1000.0)
    return statistics.median(tempos)


def tabela(titulo: str, fn: Callable[[object], object], casos: list[CASO]) -> None:
    print(f"\n{titulo}  [{fn.__name__}]")
    print(f"{'n':>14} {'operacoes previstas':>20} {'ms (mediana)':>14} {'razao':>8}")
    anterior = None
    for n, argumento, operacoes in casos:
        ms = mediar(lambda a=argumento: fn(a))
        razao = "     -" if anterior is None else f"{ms / anterior:6.1f}x"
        print(f"{n:>14,} {operacoes:>20,} {ms:>14.3f} {razao:>8}")
        anterior = ms


def main() -> int:
    print(
        f"Tema 01 - mediana de {REPETICOES} repeticoes | "
        f"{platform.python_implementation()} {platform.python_version()} | "
        f"{platform.processor() or 'cpu desconhecida'}"
    )

    tabela(
        "linear: acumula n valores",
        soma_ate,
        [(n, n, n) for n in (10**2, 10**3, 10**4, 10**5, 10**6)],
    )

    tabela(
        "quadratico: compara todos os pares, input sem repeticao",
        tem_repetido,
        [(n, list(range(n)), n * (n - 1) // 2) for n in (10**2, 2 * 10**2, 5 * 10**2, 10**3, 2 * 10**3)],
    )

    tabela(
        "logaritmico: divide por 2 ate chegar a 1",
        quantas_metades,
        [(n, n, quantas_metades(n)) for n in (2**10, 2**14, 2**18, 2**24, 2**30)],
    )

    tabela(
        "n log n: compoe os dois ciclos anteriores",
        pares_sobre_metades,
        [(n, n, (n // 2) * quantas_metades(n)) for n in (10**3, 10**4, 10**5)],
    )

    print(
        "\nLeitura: a coluna de operacoes previstas e a forma fechada exata; a de ms e "
        "desta maquina. Afirma-se a inclinacao da curva, nao o valor absoluto."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
