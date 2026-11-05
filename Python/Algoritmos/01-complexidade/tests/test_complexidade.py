"""Testes do tema 01: a contagem exata bate com a forma fechada, em n inteiro.

Estes testes nao cronometram nada. Verificam o numero de operacoes, que e o mesmo
em qualquer maquina e em qualquer uma das quatro linguagens da trilha.
"""

from complexidade import (
    Contador,
    pares_sobre_metades,
    pares_sobre_metades_contado,
    quantas_metades,
    quantas_metades_contado,
    soma_ate,
    soma_ate_contado,
    tem_repetido,
    tem_repetido_contado,
)

TAMANHOS = [0, 1, 2, 3, 4, 7, 8, 100, 1024, 10_000]
# O ciclo duplo a 10^4 custa 5*10^7 comparacoes; em Python puro levaria segundos por
# teste. A contagem exata nao precisa de escalas grandes para provar a forma fechada.
TAMANHOS_QUADRATICOS = [0, 1, 2, 3, 4, 7, 8, 100, 250]


def piso_log2(x: int) -> int:
    """floor(log2(x)) em inteiro puro; -1 para x <= 0 para nao esconder erro."""
    return x.bit_length() - 1 if x > 0 else -1


def test_soma_ate_roda_n_iteracoes() -> None:
    for n in TAMANHOS:
        cont = Contador()
        assert soma_ate_contado(n, cont) == n * (n - 1) // 2
        assert cont.iteracoes == n
        assert soma_ate(n) == soma_ate_contado(n, Contador())


def test_metades_contam_log2_e_nao_aformula_decorada() -> None:
    casos = {1: 0, 2: 1, 3: 1, 4: 2, 7: 2, 8: 3, 9: 3, 1024: 10, 1_000_000: 19}
    for n, esperado in casos.items():
        cont = Contador()
        assert quantas_metades_contado(n, cont) == esperado
        assert cont.iteracoes == esperado
        assert piso_log2(n) == esperado
        assert quantas_metades(n) == esperado


def test_tem_repetido_compara_todos_os_pares_quando_nao_ha_repetido() -> None:
    for n in TAMANHOS_QUADRATICOS:
        valores = list(range(n))
        cont = Contador()
        assert tem_repetido_contado(valores, cont) is False
        assert cont.comparacoes == n * (n - 1) // 2
        assert tem_repetido(valores) is False


def test_tem_repetido_para_na_primeira_comparacao_que_decide() -> None:
    # O duplicado esta no ultimo par possivel: o ciclo externo ainda e o primeiro.
    valores = [0, 1, 2, 3, 4, 5, 0]
    cont = Contador()
    assert tem_repetido_contado(valores, cont) is True
    assert cont.comparacoes == len(valores) - 1


def test_pares_sobre_metades_eh_n_log_n_em_contagem_exata() -> None:
    for n in TAMANHOS:
        cont = Contador()
        total = pares_sobre_metades_contado(n, cont)
        esperado = (n // 2) * quantas_metades(n)
        assert total == esperado
        assert cont.iteracoes == esperado
        assert pares_sobre_metades(n) == esperado
