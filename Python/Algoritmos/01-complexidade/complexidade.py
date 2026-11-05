"""Tema 01 — complexidade: quatro funcoes e a contagem exata do seu trabalho.

Cada exercicio existe em duas versoes. A pura e a que se cronometra em medir.py.
A contada faz o mesmo ciclo e incrementa um contador por operacao basica, para que
os testes possam afirmar o numero exato de iteracoes — deterministico entre
linguagens, ao contrario do tempo de parede.
"""

from __future__ import annotations


class Contador:
    """Registra quantas operacoes basicas um ciclo executou."""

    def __init__(self) -> None:
        self.iteracoes = 0
        self.comparacoes = 0


def soma_ate(n: int) -> int:
    """Acumula 0 + 1 + ... + (n-1). Roda exatamente n iteracoes."""
    total = 0
    for i in range(n):
        total += i
    return total


def soma_ate_contado(n: int, cont: Contador) -> int:
    total = 0
    for i in range(n):
        cont.iteracoes += 1
        total += i
    return total


def tem_repetido(valores: list[int]) -> bool:
    """Verificacao ingenua de duplicado: compara todos os pares."""
    n = len(valores)
    for i in range(n):
        for j in range(i + 1, n):
            if valores[i] == valores[j]:
                return True
    return False


def tem_repetido_contado(valores: list[int], cont: Contador) -> bool:
    """Mesmo ciclo; conta as comparacoes feitas ate decidir."""
    n = len(valores)
    for i in range(n):
        for j in range(i + 1, n):
            cont.comparacoes += 1
            if valores[i] == valores[j]:
                return True
    return False


def quantas_metades(n: int) -> int:
    """Quantas divisoes por 2 ate chegar a 1. Zero quando n <= 1."""
    passos = 0
    while n > 1:
        n //= 2
        passos += 1
    return passos


def quantas_metades_contado(n: int, cont: Contador) -> int:
    passos = 0
    while n > 1:
        cont.iteracoes += 1
        n //= 2
        passos += 1
    return passos


def pares_sobre_metades(n: int) -> int:
    """Ciclo externo de n//2 pasos, cada um varrendo as metades de n.

    Serve para ver a forma n log n nascer da composicao de dois ciclos, nao de
    uma formula decorada.
    """
    total = 0
    for _ in range(n // 2):
        total += quantas_metades(n)
    return total


def pares_sobre_metades_contado(n: int, cont: Contador) -> int:
    total = 0
    for _ in range(n // 2):
        m = n
        while m > 1:
            cont.iteracoes += 1
            m //= 2
            total += 1
    return total
