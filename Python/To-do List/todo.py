import json
import os

ARQUIVO_TAREFAS = "tarefas.json"


def carregar_tarefas():
    """Carrega as tarefas salvas no arquivo JSON, se existir."""
    if os.path.exists(ARQUIVO_TAREFAS):
        with open(ARQUIVO_TAREFAS, "r", encoding="utf-8") as arquivo:
            try:
                return json.load(arquivo)
            except json.JSONDecodeError:
                return []
    return []


def salvar_tarefas(tarefas):
    """Salva a lista de tarefas no arquivo JSON."""
    with open(ARQUIVO_TAREFAS, "w", encoding="utf-8") as arquivo:
        json.dump(tarefas, arquivo, indent=4, ensure_ascii=False)


def adicionar_tarefa(tarefas):
    """Pede uma descrição ao usuário e adiciona uma nova tarefa."""
    descricao = input("Digite a descrição da tarefa: ").strip()
    if not descricao:
        print("A descricao nao pode estar vazia.\n")
        return

    nova_tarefa = {"descricao": descricao, "concluida": False}
    tarefas.append(nova_tarefa)
    salvar_tarefas(tarefas)
    print(f"Tarefa '{descricao}' adicionada com sucesso!\n")


def listar_tarefas(tarefas):
    """Exibe todas as tarefas cadastradas com seu status."""
    if not tarefas:
        print("Nenhuma tarefa cadastrada.\n")
        return

    print("\nLista de Tarefas:")
    for indice, tarefa in enumerate(tarefas, start=1):
        status = "[X]" if tarefa["concluida"] else "[ ]"
        print(f"{indice}. {status} {tarefa['descricao']}")
    print()


def concluir_tarefa(tarefas):
    """Marca uma tarefa existente como concluida."""
    listar_tarefas(tarefas)
    if not tarefas:
        return

    try:
        numero = int(input("Digite o numero da tarefa concluida: "))
        if 1 <= numero <= len(tarefas):
            tarefas[numero - 1]["concluida"] = True
            salvar_tarefas(tarefas)
            print("Tarefa marcada como concluida!\n")
        else:
            print("Numero invalido.\n")
    except ValueError:
        print("Digite um numero valido.\n")


def remover_tarefa(tarefas):
    """Remove uma tarefa da lista pelo numero."""
    listar_tarefas(tarefas)
    if not tarefas:
        return

    try:
        numero = int(input("Digite o numero da tarefa a remover: "))
        if 1 <= numero <= len(tarefas):
            removida = tarefas.pop(numero - 1)
            salvar_tarefas(tarefas)
            print(f"Tarefa '{removida['descricao']}' removida com sucesso!\n")
        else:
            print("Numero invalido.\n")
    except ValueError:
        print("Digite um numero valido.\n")


def exibir_menu():
    """Mostra as opcoes disponiveis para o usuario."""
    print("=" * 35)
    print("      GERENCIADOR DE TAREFAS")
    print("=" * 35)
    print("1. Adicionar tarefa")
    print("2. Listar tarefas")
    print("3. Concluir tarefa")
    print("4. Remover tarefa")
    print("5. Sair")
    print("=" * 35)


def main():
    """Funcao principal: carrega dados e roda o loop do programa."""
    tarefas = carregar_tarefas()

    while True:
        exibir_menu()
        opcao = input("Escolha uma opcao: ").strip()

        if opcao == "1":
            adicionar_tarefa(tarefas)
        elif opcao == "2":
            listar_tarefas(tarefas)
        elif opcao == "3":
            concluir_tarefa(tarefas)
        elif opcao == "4":
            remover_tarefa(tarefas)
        elif opcao == "5":
            print("Ate logo!")
            break
        else:
            print("Opcao invalida. Tente novamente.\n")


if __name__ == "__main__":
    main()