#ifndef TEMA_01_COMPLEXIDADE_H
#define TEMA_01_COMPLEXIDADE_H

/* Tema 01: os mesmos quatro ciclos das outras tres linguagens da trilha.
   As versoes "contado" incrementam um contador por operacao basica; os testes
   afirmam a forma fechada exata. As puras sao as que medir.c cronometra.

   Em janelas LLP64 o `long` tem 32 bits e a soma ate 10^6 passa de 5*10^11, por
   isso os acumuladores sao `long long` em vez de `long`. */

typedef struct {
    long long iteracoes;
    long long comparacoes;
} Contador;

long long soma_ate(int n);
long long soma_ate_contado(int n, Contador *cont);

int tem_repetido(const int *valores, int n);
int tem_repetido_contado(const int *valores, int n, Contador *cont);

int quantas_metades(int n);
int quantas_metades_contado(int n, Contador *cont);

long long pares_sobre_metades(int n);
long long pares_sobre_metades_contado(int n, Contador *cont);

#endif /* TEMA_01_COMPLEXIDADE_H */
