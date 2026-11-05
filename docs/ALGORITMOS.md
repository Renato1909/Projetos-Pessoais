# Trilha de algoritmos e lógica de programação

Índice da trilha de treino deste repositório. Diferente dos projetos consolidados — que resolvem um problema de cada vez e trazem servidor, testes e dependências — aqui cada entrada é um exercício pequeno, implementado em várias linguagens para que a comparação entre elas seja o ponto.

## Como está organizado

O eixo continua a ser `Linguagem/Area/Projeto/`, definido no [registro de consolidação](CONSOLIDACAO.md). A trilha usa `Algoritmos` como área e o tema como projeto:

```
Python/Algoritmos/01-complexidade/
Go/Algoritmos/01-complexidade/
C/Algoritmos/01-complexidade/
Rust/Algoritmos/src/complexidade.rs
```

Go e Rust agrupam os temas num único manifesto (`Go/Algoritmos/go.mod`, `Rust/Algoritmos/Cargo.toml`): um `go.mod` por tema obrigaria a quatro ficheiros de módulo sem dependências, e em Rust um crate por tema repetiria quatro `Cargo.lock` idênticos. Python e C mantêm uma pasta por tema porque nelas o tema já é a unidade de execução.

A explicação de cada tema vive **aqui**, uma vez só. O `README.md` de cada pasta de linguagem documenta apenas os comandos daquela linguagem e os números que saíram dela — repetir a teoria quatro vezes seria a primeira coisa a entrar em contradição consigo própria.

## Índice de temas

| Tema | O que exercita | Python | Go | C | Rust |
|---|---|---|---|---|---|
| 01-complexidade | Contar operações e medir a curva em vez de recitar big-O | — | — | — | — |
| 02-busca-e-ordenacao | Invariantes de fronteira na busca binária; ordenação própria vs stdlib | — | — | — | — |
| 03-estruturas-lineares | Lista ligada, pilha, fila e deque escritos à mão | — | — | — | — |
| 04-hashing | Colisões, load factor, rehash e as três aplicações clássicas | — | — | — | — |

A linha de cada tema ganha o link para a sua secção e os links das quatro implementações no commit que entregar esse tema. Célula com `—` é tema ainda não entregue naquela linguagem.

## Como correr

Todos os comandos correm **de dentro da pasta do tema**, não da raiz do repositório — os testes Python dependem do diretório atual para importar o módulo do tema, e é assim que o CI também os executa.

```bash
cd Python/Algoritmos/01-complexidade && python -m pytest -q && python medir.py
cd Go/Algoritmos && go test ./... && go test -run '^$' -bench . ./01-complexidade
cd C/Algoritmos/01-complexidade && make test && make bench
cd Rust/Algoritmos && cargo test && cargo run --release --bin medir
```

Detalhes do ambiente Windows, porque nenhuma destas ferramentas está no `PATH` do sistema:

- Python 3.12 em `D:\Dev\Python312`, Go 1.26 em `D:\Dev\Go\bin`, gcc 16.2 e `mingw32-make` em `D:\Dev\MSYS2\ucrt64\bin`, Rust 1.99 (`x86_64-pc-windows-gnu`, `RUSTUP_HOME`/`CARGO_HOME` em `D:\Dev\Rust`).
- No Windows o `make` chama-se `mingw32-make`; o Makefile usa `$(MAKE)`-compatível com os dois.
- O toolchain Rust é o **gnu** de propósito: linka com o gcc do MSYS2 e por isso não exige Visual Studio Build Tools. Em compensação, `cargo test` precisa de `D:\Dev\MSYS2\ucrt64\bin` no `PATH` para encontrar o linker e as DLLs de runtime.

## Sobre os números

Os tempos publicados nas tabelas não são provas de complexidade — são medidas desta máquina: Intel Core i3-7100, 2 núcleos / 4 threads a 3,9 GHz, SSD para o código e HDD para artefactos. Um i3 de 2017 ordena menos bem que um EPYC do GitHub Actions, por isso os números do CI divergem dos locais e ambos estão certos.

O que se publica então:

- **Mediana de 5 repetições** por tamanho de entrada, não o mínimo nem a última corrida.
- **Tamanhos em potência de 10** (10² a 10⁶), porque a inclinação da curva é o que interessa, não o valor absoluto.
- **Flags de compilação declaradas**: `gcc -O2` versus `-O0` mudou a mesma medição de 0,39 ms para 2,51 ms em `n = 10⁶` — quase 6,5×. Um número sem a flag ao lado não é informação.
- **Cronómetro de alta resolução**: `clock_gettime(CLOCK_MONOTONIC)` em C. O `clock()` do Windows quantiza a 1 ms e produzia `3.000`/`2.000 ms` para trabalho que demora 0,4 ms — inútil para curvas.
- **Ruido de alocação**: em C e Rust as medições incluem a construção dos dados de entrada e a medição é feita sobre a estrutura já populada, para que `O(n)` de build não se esconda dentro de `O(log n)` de busca.

O que se conclui não é "este algoritmo é 6,5× mais rápido", e sim "a curva é plana enquanto o input cresce 10× e o tempo multiplica por ~10" — que é a definição operacional de linearidade. Os testes automatizados verificam a *razão* entre pontos consecutivos com tolerância, não os milissegundos.

## Licença

Código desta trilha coberto pela [MIT](../LICENSE) da raiz. Os enunciados dos temas foram escritos a partir da prática de exercícios de curso; a implementação, a prosa e as medições são próprias, sem copiar soluções de terceiros.
