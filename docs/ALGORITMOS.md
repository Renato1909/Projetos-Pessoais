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
| [01-complexidade](#tema-01--complexidade-e-medição) | Contar operações e medir a curva em vez de recitar big-O | [célula](../Python/Algoritmos/01-complexidade/README.md) | [célula](../Go/Algoritmos/01-complexidade/README.md) | [célula](../C/Algoritmos/01-complexidade/README.md) | [célula](../Rust/Algoritmos/README.md) |
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

## Tema 01 — complexidade e medição

[Python](../Python/Algoritmos/01-complexidade/README.md) · [Go](../Go/Algoritmos/01-complexidade/README.md) · [C](../C/Algoritmos/01-complexidade/README.md) · [Rust](../Rust/Algoritmos/README.md)

O exercício não é recitar big-O: é **contar operações básicas num ciclo próprio** e depois **cronometrar o mesmo ciclo**, para ver se as duas respostas concordam. Quando não concordam, o erro está quase sempre no cronómetro ou no otimizador — e é isso que o tema treina.

Quatro ciclos, dos mais baratos aos mais caros de pagar:

| função | ciclo | operações básicas (forma fechada exata) | classe |
|---|---|---|---|
| `soma_ate(n)` | um accumulation sobre `0..n` | `n` adições | O(n) |
| `tem_repetido(v)` | dois ciclos aninhados sobre os pares, sai quando decide | pior caso (sem repetição) `n(n-1)/2`; melhor caso (repetido logo no primeiro par) `1` comparações | O(n²) |
| `quantas_metades(n)` | divide por 2 enquanto `> 1` | `⌊log₂ n⌋` divisões | O(log n) |
| `pares_sobre_metades(n)` | `n/2` passos, cada um a varrer as metades de `n` | `(n/2)·⌊log₂ n⌋` iterações | O(n log n) |

Cada uma existe em duas versões. A **pura** é a que se cronometra. A **contada** recebe um `Contador` e incrementa-o por operação básica; são os seus números que os testes afirmam, valor a valor, contra a forma fechada. Assim a asserção é determinística entre máquinas, entre flags e entre linguagens, e o tempo fica onde deve ficar: na documentação.

Três coisas que o tema obriga a descobrir:

1. **Contar e cronometrar são provas diferentes.** A contagem diz o que o código *faz*; o tempo diz o que a máquina *fez*. Um i3 de 2017 e um EPYC do CI dão curvas com a mesma inclinação e valores diferentes.
2. **Um tempo que não escala é um tempo medido a nada.** Se `n` cresce 10× e o tempo fica plano, o ciclo não correu. A regra apanhou o `soma_ate` de Rust, onde o LLVM fecha a série aritmética em forma fechada mesmo com o argumento opaco.
3. **O melhor caso tem de ser dito, não insinuado.** `tem_repetido` sobre um input com repetição no início custa uma comparação; sobre um input com todos os valores distintos custa `n(n-1)/2`. Mesmo código, dois preços — por isso as tabelas dizem sempre qual foi o input.

## Sobre os números

Os tempos publicados nas tabelas não são provas de complexidade — são medidas desta máquina: Intel Core i3-7100, 2 núcleos / 4 threads a 3,9 GHz, com o repositório e os artefactos no HDD (`D:\Dev`). Um i3 de 2017 ordena menos bem que um EPYC do GitHub Actions, por isso os números do CI divergem dos locais e ambos estão certos.

O que se publica então:

- **Mediana de 5 repetições** por tamanho de entrada, não o mínimo nem a última corrida.
- **Entrada multiplicada por fator fixo por linha** — potências de 10 nos exercícios lineares e quadráticos, potências de 2 no logarítmico, porque ali a forma fechada conta halving e só a base 2 produz pontos alinhados com a contagem.
- **Fator de repetição por linha**, calculado para que cada célula da tabela cronometre ~10⁷ operações. Sem isso um ciclo de 10 iterações cronometra 0 e a razão entre pontos sai `inf` ou `NaN`; a unidade publicada é `ns/chamada`, a mesma do `ns/op` do Go.
- **Flags de compilação declaradas**: `gcc -O2` versus `-O0` mudou a mesma medição de 0,39 ms para 2,51 ms em `n = 10⁶` — quase 6,5×. Um número sem a flag ao lado não é informação.
- **Cronómetro de alta resolução**: `clock_gettime(CLOCK_MONOTONIC)` em C, `Instant` em Rust, `time.perf_counter` em Python. O `clock()` do Windows quantiza a 1 ms e produzia `3.000`/`2.000 ms` para trabalho que demora 0,4 ms — inútil para curvas.
- **Input construído fora da zona cronometrada**, tanto em C como em Rust, para que o `O(n)` de preparação não se esconda dentro do `O(log n)` de busca; em C a lista é alocada e preenchida antes do laço de repetições, e `free` vem depois.
- **Otimizador impedido de comer a chamada**: `volatile` em C, `std::hint::black_box` em Rust, `sink` em Go. A prova de que nada foi eliminado é a própria escala — o `n log n` multiplica por ~13 quando as operações previstas multiplicam por ~14.

O que se conclui não é "este algoritmo é 6,5× mais rápido", e sim "a curva escala com a contagem declarada" — que é a definição operacional de complexidade. O que os testes automatizados verificam são as **contagens exatas** de operações básicas (n, n(n−1)/2, ⌊log₂ n⌋, (n/2)·⌊log₂ n⌋) através das versões `_contado` de cada exercício: não dependem de máquina, nem de flag, nem de mediana. Os milissegundos ficam na documentação; as formas fechadas ficam no teste.

## Licença

Código desta trilha coberto pela [MIT](../LICENSE) da raiz. Os enunciados dos temas foram escritos a partir da prática de exercícios de curso; a implementação, a prosa e as medições são próprias, sem copiar soluções de terceiros.
