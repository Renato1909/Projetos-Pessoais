# Tema 01 — complexidade e medição (Rust)

Exercício e explicação do tema estão em [`docs/ALGORITMOS.md`](../../../docs/ALGORITMOS.md). Esta pasta documenta só o que é específico de Rust.

## Ficheiros

Os quatro exercícios vivem num único crate (`Rust/Algoritmos`), um módulo por tema — é o módulo `complexidade` deste tema 01.

| ficheiro | papel |
|---|---|
| `src/lib.rs` | declara os módulos da trilha; um `pub mod` por tema |
| `src/complexidade.rs` | os quatro ciclos, em versão pura e versão contada (`Contador`) |
| `tests/complexidade.rs` | asserções da contagem exata, correm fora do crate |
| `src/bin/medir.rs` | tabela de medições com mediana de 5 repetições |
| `Cargo.toml` | `edition = "2024"`, `publish = false`, MIT |

## Como correr

```bash
cd Rust/Algoritmos
cargo test                        # as 5 asserções de contagem exata
cargo fmt --check
cargo clippy --all-targets -- --deny warnings
cargo run --release --bin medir   # as tabelas abaixo
```

No Windows, com o toolchain portátil em `D:\Dev\Rust` (nada foi para o `PATH` do sistema):

```bash
export RUSTUP_HOME='D:/Dev/Rust/rustup' CARGO_HOME='D:/Dev/Rust/cargo'
export PATH="/d/Dev/Rust/cargo/bin:/d/Dev/MSYS2/ucrt64/bin:$PATH"
```

O `ucrt64` é obrigatório: o toolchain é o `x86_64-pc-windows-gnu` de propósito, para linkar com o gcc do MSYS2 e não exigir Visual Studio Build Tools.

## Ambiente da medição

```
rustc 1.99.1 (58cf8f9c3 2026-10-13) cargo 1.99.1 -C opt-level=3 (release)
x86_64-pc-windows-gnu | Intel Core i3-7100 @ 3,90 GHz (2 núcleos / 4 threads) | Windows 11 | 2026-11-05
```

Cada ponto é a mediana de 5 repetições dentro do binário; a tabela publica a mediana de **três corridas completas** do mesmo `medir.exe`, porque entre corridas a máquina deu até ±15 % e uma quarta corrida feita por `cargo run` deu 5,7 ms no ponto `n = 5 000` onde as outras três deram 3,4–4,0 ms.

## Medições

| exercício | n | operações previstas | ns/chamada | razão |
|---|---:|---:|---:|---:|
| `soma_ate` (puro) | 100 | 100 | 1,1 | — |
| | 1 000 | 1 000 | 1,0 | 0,9× |
| | 10 000 | 10 000 | 1,1 | 1,1× |
| | 100 000 | 100 000 | 2,0 | 1,8× |
| | 1 000 000 | 1 000 000 | 10,0 | 5,0× |
| `soma_ate_opaca` | 100 | 100 | 119,5 | — |
| | 1 000 | 1 000 | 1 385,8 | 11,6× |
| | 10 000 | 10 000 | 14 039,7 | 10,1× |
| | 100 000 | 100 000 | 139 443,0 | 9,9× |
| | 1 000 000 | 1 000 000 | 1 407 000,0 | 10,1× |
| `tem_repetido` | 100 | 4 950 | 2 360,5 | — |
| | 200 | 19 900 | 7 681,3 | 3,3× |
| | 500 | 124 750 | 38 268,8 | 5,0× |
| | 1 000 | 499 500 | 147 185,0 | 3,8× |
| | 2 000 | 1 999 000 | 558 600,0 | 3,8× |
| | 5 000 | 12 497 500 | 3 473 600,0 | 6,2× |
| `quantas_metades` | 2¹⁰ | 10 | 4,2 | — |
| | 2¹⁴ | 14 | 5,5 | 1,3× |
| | 2¹⁸ | 18 | 6,9 | 1,3× |
| | 2²⁴ | 24 | 8,9 | 1,3× |
| | 2³⁰ | 30 | 11,6 | 1,3× |
| `pares_sobre_metades` | 1 000 | 4 500 | 1 939,9 | — |
| | 10 000 | 65 000 | 29 304,6 | 15,1× |
| | 100 000 | 800 000 | 376 000,0 | 12,8× |

## A linha plana é o resultado, não um acidente

`soma_ate(10⁶)` custa 10 ns. Um milhão de iterações em 10 ns seriam 0,01 ns por iteração — menos de um vigésimo de ciclo de relógio a 3,9 GHz. O ciclo não correu.

A culpa não é do `black_box`, que está lá. Em `--release` o LLVM reconhece o padrão `for i in 0..n { total += i }` e substitui-o pela forma fechada `n(n-1)/2`. Como o resultado continua a ser uma função correta de `n`, o argumento opaco não salva nada: a otimização é válida *para todo* `n`.

Estranhamente, a versão contada (`soma_ate_contado`) também saía a 5 ns: `cont.iteracoes += 1` dentro de um ciclo de `n` passos é redutível a `cont.iteracoes += n`, que a mesma análise come. Confirmado por uma sonda com os dois no mesmo binário — puro 5,0 ns, contado 5,0 ns, e o mesmo ciclo com o acumulador por `black_box` 1 578 120 ns.

Daí as duas tabelas lineares. `soma_ate_opaca` (`src/bin/medir.rs`) é o mesmo `0..n` com `total = black_box(total + i)`, que obriga o compilador a materializar cada passo. Só existe no binário de medição: o módulo do exercício mantém-se puro, e são os testes de contagem — não o cronómetro — que provam que `soma_ate` roda `n` iterações.

## Leitura

- **Linear.** Na versão que corre: 11,6× / 10,1× / 9,9× / 10,1× por ×10 de `n`. 1,41 ns por iteração, contra os 0,39 ns/iteração do `soma_ate` de C a `-O2`. A diferença não é "Rust mais lento que C", é o preço da barreira: `black_box` por iteração força store e reload que o ciclo de C não tem. Onde nenhuma das duas linguagens precisa de barreira (`tem_repetido`), ficam coladas: 0,28 ns/comparação em Rust, 0,27 ns em C — 1,04× de um para o outro.
- **Quadrático.** ×2 em `n` dá 3,3× / 3,8× / 3,8× e ×2,5 dá 5,0× e 6,2×, contra os 4× e 6,25× da forma fechada. O degrau 100 → 200 a 3,3× é o piso do instrumento outra vez: 4 950 comparações de 64 bits não saem do L1.
- **Logaritmico.** É a curva mais limpa das quatro linguagens: cada degrau multiplica por ~1,3 exatamente como as operações previstas (10 → 14 → 18 → 24 → 30 passos), e `n` cresce um milhão de vezes. Custa 0,39 ns por divisão. Aqui o LLVM não fechou o ciclo — reduzir `while resto > 1 { resto /= 2 }` a `63 - n.leading_zeros()` é uma idiom que ele não aplicou neste `i64` com guarda assinada, e a escala 1,3×/degrau é a prova.
- **n log n.** 15,1× e 12,8× por ×10 de `n`, quando o linear dá ~10× — o excedente é o fator log que cresce de 9 para 16 passos. 0,47 ns por iteração interna, coerente com os 0,39 ns do `quantas_metades` isolado.

## O que esta célula acrescenta ao tema

As outras três linguagens mostram a curva. Rust mostra que **a curva que cronometras pode não ser a curva que escreveste**, e que um otimizador suficientemente bom não elimina o trabalho — dá-te o resultado do trabalho por outro caminho, correto e instantâneo. A regra que `docs/ALGORITMOS.md` enuncia ("um tempo que não escale com a contagem indica chamada eliminada") foi a que apanhou isto; em C e Go a mesma regra não apanhou nada, e é por isso que vale a pena escrevê-la.
