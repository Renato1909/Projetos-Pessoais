#include <iostream>
#include <limits>

using namespace std;

// Exibe o menu de operações
void exibirMenu() {
    cout << "\n===== CALCULADORA SIMPLES =====\n";
    cout << "1 - Somar (+)\n";
    cout << "2 - Subtrair (-)\n";
    cout << "3 - Multiplicar (*)\n";
    cout << "4 - Dividir (/)\n";
    cout << "5 - Sair\n";
    cout << "===============================\n";
    cout << "Escolha uma opcao: ";
}

// Le um numero do usuario com validacao
double lerNumero(const string& mensagem) {
    double valor;
    while (true) {
        cout << mensagem;
        cin >> valor;

        if (cin.fail()) {
            cout << "Entrada invalida! Digite um numero valido.\n";
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
        } else {
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            return valor;
        }
    }
}

int main() {
    int opcao;

    cout << "Bem-vindo a Calculadora Simples!\n";

    do {
        exibirMenu();
        cin >> opcao;

        // Valida a opcao do menu
        if (cin.fail()) {
            cout << "Opcao invalida! Digite um numero de 1 a 5.\n";
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            continue;
        }
        cin.ignore(numeric_limits<streamsize>::max(), '\n');

        if (opcao == 5) {
            cout << "\nEncerrando a calculadora. Ate logo!\n";
            break;
        }

        if (opcao < 1 || opcao > 5) {
            cout << "Opcao invalida! Escolha uma opcao de 1 a 5.\n";
            continue;
        }

        double num1 = lerNumero("Digite o primeiro numero: ");
        double num2 = lerNumero("Digite o segundo numero: ");
        double resultado;

        switch (opcao) {
            case 1:
                resultado = num1 + num2;
                cout << "Resultado: " << num1 << " + " << num2 << " = " << resultado << "\n";
                break;
            case 2:
                resultado = num1 - num2;
                cout << "Resultado: " << num1 << " - " << num2 << " = " << resultado << "\n";
                break;
            case 3:
                resultado = num1 * num2;
                cout << "Resultado: " << num1 << " * " << num2 << " = " << resultado << "\n";
                break;
            case 4:
                if (num2 == 0) {
                    cout << "Erro: Divisao por zero nao e permitida!\n";
                } else {
                    resultado = num1 / num2;
                    cout << "Resultado: " << num1 << " / " << num2 << " = " << resultado << "\n";
                }
                break;
        }

    } while (true);

    return 0;
}
