#include <assert.h>
#include <stdio.h>

#include "../complexidade.h"

/* Os testes afirmam o numero exato de operacoes, nao milissegundos: a contagem e
   identica em qualquer maquina e nas quatro linguagens da trilha. */

static void test_soma_ate(void)
{
    static const int tamanhos[] = {0, 1, 2, 3, 4, 7, 8, 100, 1024, 10000};
    for (unsigned k = 0; k < sizeof tamanhos / sizeof tamanhos[0]; k++) {
        int n = tamanhos[k];
        Contador cont = {0, 0};
        assert(soma_ate_contado(n, &cont) == (long long)n * (n - 1) / 2);
        assert(cont.iteracoes == n);
        assert(soma_ate(n) == soma_ate_contado(n, &(Contador){0, 0}));
    }
    puts("soma_ate: n iteracoes, forma fechada conferida em 10 tamanhos");
}

static void test_quantas_metades(void)
{
    static const int valores[] = {1, 2, 3, 4, 7, 8, 9, 1024, 1000000};
    static const int passos[] = {0, 1, 1, 2, 2, 3, 3, 10, 19};
    for (unsigned k = 0; k < sizeof valores / sizeof valores[0]; k++) {
        Contador cont = {0, 0};
        assert(quantas_metades_contado(valores[k], &cont) == passos[k]);
        assert(cont.iteracoes == passos[k]);
        assert(quantas_metades(valores[k]) == passos[k]);
    }
    puts("quantas_metades: floor(log2 n) confirmado, incluindo os nao-potencias");
}

static void test_tem_repetido(void)
{
    static const int tamanhos[] = {0, 1, 2, 3, 4, 7, 8, 100, 250};
    int valores[250];
    for (unsigned k = 0; k < sizeof tamanhos / sizeof tamanhos[0]; k++) {
        int n = tamanhos[k];
        for (int i = 0; i < n; i++) {
            valores[i] = i;
        }
        Contador cont = {0, 0};
        assert(tem_repetido_contado(valores, n, &cont) == 0);
        assert(cont.comparacoes == (long long)n * (n - 1) / 2);
        assert(tem_repetido(valores, n) == 0);
    }
    puts("tem_repetido: sem repeticao, todas as n(n-1)/2 comparacoes");
}

static void test_tem_repetido_decide_cedo(void)
{
    int valores[] = {0, 1, 2, 3, 4, 5, 0};
    Contador cont = {0, 0};
    assert(tem_repetido_contado(valores, 7, &cont) == 1);
    assert(cont.comparacoes == 6);
    puts("tem_repetido: para na comparacao que decide (duplicado no ultimo par: n-1)");
}

static void test_pares_sobre_metades(void)
{
    static const int tamanhos[] = {0, 1, 2, 3, 4, 7, 8, 100, 1024, 10000};
    for (unsigned k = 0; k < sizeof tamanhos / sizeof tamanhos[0]; k++) {
        int n = tamanhos[k];
        long long esperado = (n / 2) * (long long)quantas_metades(n);
        Contador cont = {0, 0};
        assert(pares_sobre_metades_contado(n, &cont) == esperado);
        assert(cont.iteracoes == esperado);
    }
    puts("pares_sobre_metades: contagem exata igual a (n/2) * floor(log2 n)");
}

int main(void)
{
    test_soma_ate();
    test_quantas_metades();
    test_tem_repetido();
    test_tem_repetido_decide_cedo();
    test_pares_sobre_metades();
    puts("todos os testes do tema 01 passaram");
    return 0;
}
