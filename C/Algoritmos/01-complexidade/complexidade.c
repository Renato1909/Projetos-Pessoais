#include "complexidade.h"

long long soma_ate(int n)
{
    long long total = 0;
    for (int i = 0; i < n; i++) {
        total += i;
    }
    return total;
}

long long soma_ate_contado(int n, Contador *cont)
{
    long long total = 0;
    for (int i = 0; i < n; i++) {
        cont->iteracoes++;
        total += i;
    }
    return total;
}

int tem_repetido(const int *valores, int n)
{
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            if (valores[i] == valores[j]) {
                return 1;
            }
        }
    }
    return 0;
}

int tem_repetido_contado(const int *valores, int n, Contador *cont)
{
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            cont->comparacoes++;
            if (valores[i] == valores[j]) {
                return 1;
            }
        }
    }
    return 0;
}

int quantas_metades(int n)
{
    int passos = 0;
    while (n > 1) {
        n /= 2;
        passos++;
    }
    return passos;
}

int quantas_metades_contado(int n, Contador *cont)
{
    int passos = 0;
    while (n > 1) {
        cont->iteracoes++;
        n /= 2;
        passos++;
    }
    return passos;
}

/* Ciclo externo de n/2 passos, cada um varrendo as metades de n: a forma
   n log n a nascer da composicao, nao de uma formula decorada. */
long long pares_sobre_metades(int n)
{
    long long total = 0;
    for (int i = 0; i < n / 2; i++) {
        total += quantas_metades(n);
    }
    return total;
}

long long pares_sobre_metades_contado(int n, Contador *cont)
{
    long long total = 0;
    for (int i = 0; i < n / 2; i++) {
        int m = n;
        while (m > 1) {
            cont->iteracoes++;
            m /= 2;
            total++;
        }
    }
    return total;
}
