/* Cronometra os quatro exercicios do tema 01. Correr com `make bench`.

   Cada linha e repetida um fator escolhido para que o span medido seja da ordem de
   10 ms. Sem isso, um ciclo de 30 iteracoes cronometra 0,000 ms e a divisao entre
   pontos consecutivos da nan ou inf -- que foi exatamente o que aconteceu na primeira
   versao deste ficheiro. O tempo publicado e por chamada (span / fator), como o
   ns/op que o `go test -bench` calcula sozinho.

   O input e construido ANTES da zona cronometrada. O cronometro e clock_gettime,
   nao clock(): em Windows o clock() quantiza a 1 ms e mostrava 3.000/2.000 ms para
   trabalho de 0,4 ms. */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "complexidade.h"

#define REPETICOES 5
#define ALVO_OPERACOES_POR_LINHA 10000000LL

static double agora_ms(void)
{
    struct timespec ts;
    if (clock_gettime(CLOCK_MONOTONIC, &ts) != 0) {
        return -1.0;
    }
    return (double)ts.tv_sec * 1000.0 + (double)ts.tv_nsec / 1e6;
}

static int comparar(const void *a, const void *b)
{
    double x = *(const double *)a;
    double y = *(const double *)b;
    return (x > y) - (x < y);
}

static double mediana(double *valores)
{
    qsort(valores, REPETICOES, sizeof *valores, comparar);
    return valores[REPETICOES / 2];
}

/* Fator minimo para que a linha cronometre trabalho suficiente; nunca menos que 1. */
static long long fator_para(long long operacoes)
{
    if (operacoes <= 0) {
        return 1;
    }
    long long fator = ALVO_OPERACOES_POR_LINHA / operacoes;
    return fator > 0 ? fator : 1;
}

typedef double (*Cronometro)(int n, const int *valores);

static void tabela(const char *titulo, const char *exercicio, const int *ns, int quantidade,
                   long long (*operacoes)(int), Cronometro cronometrar)
{
    printf("\n%s  [%s]\n", titulo, exercicio);
    printf("%14s %20s %16s %13s %9s\n", "n", "operacoes previstas", "fator", "ns/chamada", "razao");
    double anterior = -1.0;
    for (int k = 0; k < quantidade; k++) {
        int n = ns[k];
        long long trabalho = operacoes(n);
        long long fator = fator_para(trabalho);

        int *valores = calloc((size_t)(n > 0 ? n : 1), sizeof *valores);
        if (valores == NULL) {
            puts("falha ao alocar input; aborta");
            exit(EXIT_FAILURE);
        }
        for (int i = 0; i < n; i++) {
            valores[i] = i;
        }

        double tempos[REPETICOES];
        for (int r = 0; r < REPETICOES; r++) {
            double inicio = agora_ms();
            for (long long f = 0; f < fator; f++) {
                cronometrar(n, valores);
            }
            tempos[r] = agora_ms() - inicio;
        }
        free(valores);

        double ms_por_chamada = mediana(tempos) / (double)fator;
        double ns = ms_por_chamada * 1e6;
        printf("%14d %20lld %16lld %13.1f", n, trabalho, fator, ns);
        if (anterior <= 0.0 || ns <= 0.0) {
            printf("%9s\n", "-");
        } else {
            printf("%8.1fx\n", ns / anterior);
        }
        anterior = ns;
    }
}

static long long op_linear(int n)
{
    return n;
}

static long long op_quadratico(int n)
{
    return (long long)n * (n - 1) / 2;
}

static long long op_log(int n)
{
    return quantas_metades(n);
}

static long long op_nlogn(int n)
{
    return (n / 2) * (long long)quantas_metades(n);
}

/* O resultado passa por volatile: sem isto o gcc -O2 pode eliminar a chamada
   inteira, e a tabela mediria uma funcao que nao existe. */
static double tempo_soma(int n, const int *valores)
{
    (void)valores;
    volatile long long resultado = soma_ate(n);
    return (double)resultado * 0.0;
}

static double tempo_repetido(int n, const int *valores)
{
    volatile int resultado = tem_repetido(valores, n);
    return (double)resultado * 0.0;
}

static double tempo_metades(int n, const int *valores)
{
    (void)valores;
    volatile int resultado = quantas_metades(n);
    return (double)resultado * 0.0;
}

static double tempo_pares(int n, const int *valores)
{
    (void)valores;
    volatile long long resultado = pares_sobre_metades(n);
    return (double)resultado * 0.0;
}

int main(void)
{
    static const int lineares[] = {100, 1000, 10000, 100000, 1000000};
    static const int quadraticos[] = {100, 200, 500, 1000, 2000, 5000};
    static const int logaritmos[] = {1 << 10, 1 << 14, 1 << 18, 1 << 24, 1 << 30};
    static const int compostos[] = {1000, 10000, 100000};

    puts("Tema 01 em C - mediana de 5 repeticoes, gcc -O2");
    puts("Maquina e data no README desta celula.");

    tabela("linear: acumula n valores", "soma_ate", lineares, 5, op_linear, tempo_soma);
    tabela("quadratico: compara todos os pares, input sem repeticao", "tem_repetido", quadraticos, 6,
           op_quadratico, tempo_repetido);
    tabela("logaritmico: divide por 2 ate chegar a 1", "quantas_metades", logaritmos, 5, op_log,
           tempo_metades);
    tabela("n log n: compoe os dois ciclos anteriores", "pares_sobre_metades", compostos, 3, op_nlogn,
           tempo_pares);

    puts("\nLeitura: a coluna de operacoes previstas e a forma fechada exata; ns/chamada e");
    puts("desta maquina. Se um tempo nao escalar com a contagem, o otimizador comeu o");
    puts("ciclo -- essa e a diferenca entre trabalho do programa e trabalho da maquina.");
    return 0;
}
