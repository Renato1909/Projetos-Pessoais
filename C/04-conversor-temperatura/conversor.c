#include <stdio.h>

double cParaF(double c) { return c * 9.0 / 5.0 + 32; }
double fParaC(double f) { return (f - 32) * 5.0 / 9.0; }

int main(void) {
    char tipo;
    double v;
    printf("04 - Conversor C<->F\nDigite: <valor> <C|F>  ex: 30 C\n> ");
    if (scanf("%lf %c", &v, &tipo) != 2) { printf("Entrada invalida.\n"); return 1; }
    if (tipo == 'C' || tipo == 'c') printf("%.2f C = %.2f F\n", v, cParaF(v));
    else if (tipo == 'F' || tipo == 'f') printf("%.2f F = %.2f C\n", v, fParaC(v));
    else printf("Use C ou F.\n");
    return 0;
}
