#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(void) {
    srand((unsigned)time(NULL));
    int secreto = rand() % 100 + 1;
    int palpite, tentativas = 0;
    printf("03 - Jogo Adivinhacao (1 a 100)\n");
    while (1) {
        printf("Seu palpite: ");
        if (scanf("%d", &palpite) != 1) { printf("Digite um numero.\n"); return 1; }
        tentativas++;
        if (palpite == secreto) { printf("Acertou em %d tentativas!\n", tentativas); break; }
        else if (palpite < secreto) printf("Mais alto...\n");
        else printf("Mais baixo...\n");
    }
    return 0;
}
