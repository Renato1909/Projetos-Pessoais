# Registro de consolidação dos projetos pessoais

## Objetivo e revisão base

Padronizar os sete projetos técnicos já incorporados em `Linguagem/Area/Projeto/`, mantendo cada projeto independente. Não se trata de uma nova cópia dos repositórios nem de uma importação de seus históricos.

Revisão base de `Projetos-Pessoais`: [`f2eb8e67f2d9028e2bfcee9fbdf7fbe28f144d5f`](https://github.com/Renato1909/Projetos-Pessoais/commit/f2eb8e67f2d9028e2bfcee9fbdf7fbe28f144d5f).

## Correspondência de caminhos

| Origem preservada | Caminho anterior | Caminho atual |
|---|---|---|
| [http-server-c](https://github.com/Renato1909/http-server-c) | `C/http-server/` | [`C/Redes/http-server/`](../C/Redes/http-server/) |
| [url-shortener-go](https://github.com/Renato1909/url-shortener-go) | `Go/url-shortener/` | [`Go/APIs/url-shortener/`](../Go/APIs/url-shortener/) |
| [tasks-api-py](https://github.com/Renato1909/tasks-api-py) | `Python/tasks-api/` | [`Python/APIs/tasks-api/`](../Python/APIs/tasks-api/) |
| [lan-scanner](https://github.com/Renato1909/lan-scanner) | `Python/lan-scanner/` | [`Python/Redes/lan-scanner/`](../Python/Redes/lan-scanner/) |
| [password-strength-analyzer](https://github.com/Renato1909/password-strength-analyzer) | `Python/password-strength-analyzer/` | [`Python/Seguranca/password-strength-analyzer/`](../Python/Seguranca/password-strength-analyzer/) |
| [phishing-detector](https://github.com/Renato1909/phishing-detector) | `JavaScript/phishing-detector/` | [`JavaScript/Seguranca/phishing-detector/`](../JavaScript/Seguranca/phishing-detector/) |
| [chat-realtime-ts](https://github.com/Renato1909/chat-realtime-ts) | `TypeScript/chat-realtime/` | [`TypeScript/Comunicacao/chat-realtime/`](../TypeScript/Comunicacao/chat-realtime/) |

## Preservação e limites

- A movimentação reutiliza as árvores Git existentes, preservando os hashes e modos dos arquivos. Código-fonte, testes, dependências declaradas e licenças não são modificados.
- Os READMEs recebem caminhos e badges atualizados. A referência de versão do Go acompanha o `go.mod` existente.
- Os sete workflows aninhados são substituídos pelo [workflow da raiz](../.github/workflows/projetos-consolidados.yml), com jobs e diretórios de trabalho específicos.
- Exercícios e demais diretórios de `Projetos-Pessoais` mantêm seus caminhos nesta etapa.
- Nenhum repositório de origem é modificado, excluído ou arquivado. O histórico já existente no destino é preservado; os históricos completos das origens não são importados.
- `Portfolio2DS-AMS`, projetos acadêmicos, aplicações independentes, repositórios privados, perfil e forks ficam fora desta alteração.
- `CEP-API-PHP` e `EscolaFutebol` permanecem como repositórios independentes.

## Execução e validação

Entre no caminho atual do projeto antes de instalar dependências, compilar ou executar testes. Consulte seu README para os comandos e requisitos específicos. Os testes de scanner são restritos à validação de alvos e ao loopback local; os testes do analisador de senhas não consultam serviços externos.

O workflow verifica compilação e integração no Windows para C; análise estática, testes com detector de concorrência e build para Go; lint e cobertura para a API Python; testes para os utilitários Python; manifesto e heurísticas da extensão; tipos e integração do chat TypeScript.

Os resultados efetivamente executados e eventuais limitações do ambiente de validação são registrados no pull request. A existência do workflow não significa que todas as verificações já foram concluídas.

## Aditamento: trilha de algoritmos

Este aditamento documenta uma **adição** ao repositório, não uma revisão da consolidação acima. Nenhum caminho congelado nas seções anteriores foi movido, renomeado ou removido: os 144 ficheiros rastreados da revisão `71ff899`, a última anterior à trilha, seguem nos mesmos sítios, e a trilha apenas acrescenta caminhos novos.

- A área `Algoritmos` passa a existir dentro das linguagens, com o padrão `Linguagem/Algoritmos/<tema>/`, ao lado das áreas já registradas (APIs, Redes, Seguranca, Comunicacao).
- `Rust` entra como nova pasta de linguagem na raiz, com um único crate em `Rust/Algoritmos/`, para que a trilha tenha quatro linguagens comparáveis. Usar o toolchain `x86_64-pc-windows-gnu` na máquina local é escolha de ambiente e não afeta o conteúdo versionado.
- Go também agrupa os temas num único módulo em `Go/Algoritmos/go.mod`, porque os exercícios não têm dependências externas; os projetos consolidados mantêm os seus `go.mod` próprios.
- O workflow `projetos-consolidados.yml` não foi alterado: os seus filtros de caminho são uma lista explícita e `*/Algoritmos/**` não a integra. A trilha é validada pelo workflow separado `algoritmos.yml`.
- A `.gitignore` da raiz ganhou `build/` e `.pytest_cache/`; `target/` e `*.exe` já eram cobertos antes desta mudança.
- A `.gitignore` ganhou também a re-inclusão `!Rust/Algoritmos/src/bin/`. A regra `bin/`, escrita para as saídas de C#/dotnet, ignorava o diretório `src/bin/` que em Rust contém **código-fonte** dos binários do crate — sem esta linha o `medir.rs` da célula nunca chegaria ao repositório. A exceção é um caminho exato: `bin/` continua a apanhar qualquer outra pasta de saída.
- Nada de `Algoritmos` depende de material de terceiro: enunciados, implementações, testes e medições são próprios. A licença MIT da raiz cobre o código.

O índice e os critérios da trilha estão em [ALGORITMOS.md](ALGORITMOS.md).
