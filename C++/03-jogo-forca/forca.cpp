#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <cctype>

int main() {
    std::vector<std::string> palavras = {"computador", "programacao", "biblioteca", "algoritmo"};
    std::string secreta = palavras[rand() % palavras.size()];
    std::string visivel(secreta.size(), '_');
    int vidas = 6;
    std::string tentadas;

    std::cout << "03 - Jogo da Forca (C++)\n";
    while (vidas > 0 && visivel != secreta) {
        std::cout << "\nPalavra: ";
        for (char c : visivel) std::cout << c << ' ';
        std::cout << " | Vidas: " << vidas << " | Tentadas: " << tentadas << "\n> ";
        char ch; std::cin >> ch;
        ch = std::tolower(ch);
        if (tentadas.find(ch) != std::string::npos) { std::cout << "Ja tentou.\n"; continue; }
        tentadas += ch;
        bool achou = false;
        for (size_t i = 0; i < secreta.size(); ++i)
            if (secreta[i] == ch) { visivel[i] = ch; achou = true; }
        if (!achou) { vidas--; std::cout << "Errou!\n"; }
    }
    if (visivel == secreta) std::cout << "\nVenceu! Palavra: " << secreta << "\n";
    else std::cout << "\nPerdeu! Palavra era: " << secreta << "\n";
}
