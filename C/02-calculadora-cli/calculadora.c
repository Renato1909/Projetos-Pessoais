#include <stdio.h>

int main(void) {
    double a, b;
    char op;
    printf("02 - Calculadora CLI em C\n");
    printf("Digite: <numero> <operador + - * /> <numero>\n> ");
    if (scanf("%lf %c %lf", &a, &op, &b) != 3) {
        printf("Entrada invalida.\n");
        return 1;
    }
    double r = 0;
    int ok = 1;
    switch (op) {
        case '+': r = a + b; break;
        case '-': r = a - b; break;
        case '*': r = a * b; break;
        case '/':
            if (b == 0) { printf("Erro: divisao por zero.\n"); return 1; }
            r = a / b; break;
        default: ok = 0;
    }
    if (!ok) printf("Operador invalido. Use + - * /\n");
    else printf("Resultado: %.2f\n", r);
    return 0;
}
