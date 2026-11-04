# Projetos-Pessoais

Repositório central para projetos pessoais de programação em diferentes linguagens. Cada projeto permanece em sua própria pasta, com código, testes, dependências e instruções de execução quando disponíveis.

## Organização por linguagem e área

Os sete projetos técnicos consolidados seguem o padrão `Linguagem/Area/Projeto/`: **APIs**, **Redes**, **Seguranca** e **Comunicacao**. Cada projeto mantém seu código, dependências, testes e licença. Exercícios e demais projetos permanecem nos caminhos anteriores nesta etapa.

## Projetos por linguagem

### C
- [Servidor HTTP](C/Redes/http-server/) — servidor HTTP/1.1 com implementação própria, interface estática e testes.

### Go
- [URL Shortener](Go/APIs/url-shortener/) — API REST para encurtamento de URLs, armazenamento SQLite, cache e testes.
- [Calculadora](Go/02-calculadora/)
- [HTTP Hello](Go/03-http-hello/)

### Python
- [Tasks API](Python/APIs/tasks-api/) — API de tarefas com autenticação e testes.
- [Password Strength Analyzer](Python/Seguranca/password-strength-analyzer/) — análise defensiva de robustez de senhas.
- [LAN Scanner](Python/Redes/lan-scanner/) — scanner restrito a redes IPv4 privadas.
- [Bot Simples](Python/Bot%20Simples/)
- [To-do List](Python/To-do%20List/)

### TypeScript
- [Chat em tempo real](TypeScript/Comunicacao/chat-realtime/) — servidor e cliente web, com testes.
- [Calculadora](TypeScript/02-calculadora/)
- [To-do CLI](TypeScript/03-todo-cli/)
- [Fetch API](TypeScript/04-fetch-api/)

### JavaScript
- [Detector de phishing](JavaScript/Seguranca/phishing-detector/) — extensão de navegador com heurísticas locais.
- [Calculadora DOM](JavaScript/02-dom-calculadora/)

### C#
- [Calculadora com POO](C%23/02-calculadora-poo/)
- [To-do Console](C%23/03-todo-console/)
- [Exercícios iniciais](C%23/Iniciante/)

### C++
- [Biblioteca com classes](C%2B%2B/02-biblioteca-classes/)
- [Jogo da forca](C%2B%2B/03-jogo-forca/)
- [Exercícios iniciais](C%2B%2B/Iniciante/)

### PHP
- [Calculadora](PHP/02-calculadora/)
- [Tabuada](PHP/03-tabuada/)
- [Lista de compras](PHP/04-lista-compras/)
- [Formulário de contato](PHP/05-form-contato/)
- [Mini blog](PHP/06-mini-blog/)
- [Login e sessão](PHP/07-login-sessao/)

## Como executar

As instruções específicas estão no README de cada projeto. Entre na pasta correspondente e siga os requisitos da linguagem, como go run, dotnet run, npm install/npm test, pytest, php -S localhost:8000 ou compilação com GCC, conforme aplicável.

## Organização

- Projetos independentes ficam em subpastas próprias.
- Cada projeto deve manter seus testes, licença e instruções de execução.
- Evite versionar saídas de compilação, dependências instaladas, segredos ou arquivos locais de IDE.
- Projetos acadêmicos maiores e trabalhos que precisam de repositório próprio permanecem separados.

## Integração contínua

O [workflow dos projetos consolidados](.github/workflows/projetos-consolidados.yml) fica na raiz do repositório, como exigido pelo GitHub Actions. Ele valida os sete projetos em jobs separados, com diretórios de trabalho específicos, ao abrir ou atualizar PRs para `main`, após pushes em `main` que afetem esses projetos ou por execução manual.

A compilação do servidor HTTP utiliza Windows/MinGW-w64. O encurtador usa a versão declarada no seu `go.mod`; os projetos Python usam Python 3.12 no CI, e os projetos JavaScript/TypeScript usam Node.js 24. Execute os comandos locais sempre a partir da pasta do projeto, não da raiz deste repositório.

## Proveniência e escopo

Consulte o [registro de consolidação](docs/CONSOLIDACAO.md) para a correspondência entre caminhos anteriores e atuais e os repositórios de origem. Esta organização não exclui nem arquiva origens, não incorpora novos projetos acadêmicos e não importa o histórico completo dos repositórios de origem.
