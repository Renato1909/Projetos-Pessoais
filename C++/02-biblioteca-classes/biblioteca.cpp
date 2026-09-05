#include <iostream>
#include <vector>
#include <string>
#include <algorithm>

class Livro {
public:
    std::string titulo;
    std::string autor;
    bool emprestado = false;
    Livro(std::string t, std::string a) : titulo(t), autor(a) {}
};

class Biblioteca {
    std::vector<Livro> acervo;
public:
    void adicionar(const std::string& t, const std::string& a) {
        acervo.emplace_back(t, a);
        std::cout << "Adicionado: " << t << "\n";
    }
    void listar() const {
        if (acervo.empty()) { std::cout << "(vazia)\n"; return; }
        for (size_t i = 0; i < acervo.size(); ++i)
            std::cout << i+1 << ". " << acervo[i].titulo << " - " << acervo[i].autor
                      << (acervo[i].emprestado ? " [emprestado]" : "") << "\n";
    }
    void emprestar(int idx) {
        if (idx < 1 || idx > (int)acervo.size()) { std::cout << "Indice invalido.\n"; return; }
        if (acervo[idx-1].emprestado) std::cout << "Ja emprestado.\n";
        else { acervo[idx-1].emprestado = true; std::cout << "Emprestado!\n"; }
    }
};

int main() {
    Biblioteca bib;
    std::cout << "02 - Biblioteca com Classes (C++)\nComandos: add <titulo>;<autor> | ls | emp <n> | sair\n";
    std::string line;
    while (true) {
        std::cout << "> ";
        if (!std::getline(std::cin, line)) break;
        if (line == "sair" || line == "exit") break;
        if (line.rfind("add ", 0) == 0) {
            auto resto = line.substr(4);
            auto sep = resto.find(';');
            if (sep == std::string::npos) std::cout << "Use: add Titulo;Autor\n";
            else bib.adicionar(resto.substr(0, sep), resto.substr(sep+1));
        } else if (line == "ls") bib.listar();
        else if (line.rfind("emp ", 0) == 0) bib.emprestar(std::stoi(line.substr(4)));
        else std::cout << "Comando invalido.\n";
    }
}
