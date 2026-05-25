#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_CONTATOS 100
#define TAM_NOME 50
#define TAM_TELEFONE 20

// Estrutura para armazenar um contato
typedef struct {
    char nome[TAM_NOME];
    char telefone[TAM_TELEFONE];
} Contato;

// Variável global para armazenar os contatos
Contato agenda[MAX_CONTATOS];
int totalContatos = 0;

// Função para cadastrar um novo contato
void cadastrarContato() {
    if (totalContatos >= MAX_CONTATOS) {
        printf("\nAgenda cheia! Não é possível cadastrar mais contatos.\n");
        return;
    }

    Contato novoContato;

    printf("\n=== CADASTRAR CONTATO ===\n");
    printf("Nome: ");
    fgets(novoContato.nome, TAM_NOME, stdin);
    // Remove a quebra de linha do final
    novoContato.nome[strcspn(novoContato.nome, "\n")] = 0;

    printf("Telefone: ");
    fgets(novoContato.telefone, TAM_TELEFONE, stdin);
    novoContato.telefone[strcspn(novoContato.telefone, "\n")] = 0;

    agenda[totalContatos] = novoContato;
    totalContatos++;

    printf("Contato cadastrado com sucesso!\n");
}

// Função para listar todos os contatos
void listarContatos() {
    printf("\n=== LISTA DE CONTATOS ===\n");

    if (totalContatos == 0) {
        printf("Nenhum contato cadastrado.\n");
        return;
    }

    for (int i = 0; i < totalContatos; i++) {
        printf("%d. %s - %s\n", i + 1, agenda[i].nome, agenda[i].telefone);
    }
}

// Função para remover um contato pelo índice
void removerContato() {
    if (totalContatos == 0) {
        printf("\nNenhum contato cadastrado.\n");
        return;
    }

    listarContatos();

    int indice;
    printf("\nDigite o número do contato que deseja remover: ");
    scanf("%d", &indice);
    // Limpa o buffer do teclado
    while (getchar() != '\n');

    if (indice < 1 || indice > totalContatos) {
        printf("Índice inválido!\n");
        return;
    }

    // Remove o contato deslocando os demais
    for (int i = indice - 1; i < totalContatos - 1; i++) {
        agenda[i] = agenda[i + 1];
    }
    totalContatos--;

    printf("Contato removido com sucesso!\n");
}

// Função para buscar um contato pelo nome
void buscarContato() {
    if (totalContatos == 0) {
        printf("\nNenhum contato cadastrado.\n");
        return;
    }

    char nomeBusca[TAM_NOME];
    printf("\n=== BUSCAR CONTATO ===\n");
    printf("Digite o nome a ser buscado: ");
    fgets(nomeBusca, TAM_NOME, stdin);
    nomeBusca[strcspn(nomeBusca, "\n")] = 0;

    int encontrado = 0;
    for (int i = 0; i < totalContatos; i++) {
        if (strcmp(agenda[i].nome, nomeBusca) == 0) {
            printf("\nContato encontrado:\n");
            printf("Nome: %s\n", agenda[i].nome);
            printf("Telefone: %s\n", agenda[i].telefone);
            encontrado = 1;
            break;
        }
    }

    if (!encontrado) {
        printf("Contato não encontrado.\n");
    }
}

// Função para exibir o menu principal
void exibirMenu() {
    printf("\n=== GERENCIADOR DE CONTATOS ===\n");
    printf("1. Cadastrar contato\n");
    printf("2. Listar contatos\n");
    printf("3. Remover contato\n");
    printf("4. Buscar contato\n");
    printf("5. Sair\n");
    printf("Escolha uma opção: ");
}

int main() {
    int opcao;

    do {
        exibirMenu();
        scanf("%d", &opcao);
        // Limpa o buffer do teclado
        while (getchar() != '\n');

        switch (opcao) {
            case 1:
                cadastrarContato();
                break;
            case 2:
                listarContatos();
                break;
            case 3:
                removerContato();
                break;
            case 4:
                buscarContato();
                break;
            case 5:
                printf("Saindo do programa...\n");
                break;
            default:
                printf("Opção inválida! Tente novamente.\n");
        }
    } while (opcao != 5);

    return 0;
}