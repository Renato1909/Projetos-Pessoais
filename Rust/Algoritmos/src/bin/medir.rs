//! Cronometra os quatro exercícios do tema 01: `cargo run --release --bin medir`.
//!
//! Como em C, cada linha repete a chamada um fator escolhido para cronometrar ~10⁷
//! operações; publica-se ns por chamada (span ÷ fator), a mesma unidade do `ns/op`
//! do Go e da célula de C. Sem isso, um ciclo de 10 iterações cronometra 0 e a razão
//! entre pontos sai `inf` ou `NaN`.
//!
//! O input é construído fora da zona cronometrada e `black_box` impede que o otimizador
//! elimine a chamada — medir um ciclo que foi comido pelo compilador é medir nada.
//!
//! Em Rust, `black_box` no argumento não basta: um ciclo redutível a forma fechada é
//! reescrito pelo LLVM mesmo com `n` opaco. A tabela linear publica as duas versões, e
//! a diferença entre elas é o conteúdo da lição. Ver [`soma_ate_opaca`].

use algoritmos::complexidade::{pares_sobre_metades, quantas_metades, soma_ate, tem_repetido};
use std::hint::black_box;
use std::time::Instant;

const REPETICOES: usize = 5;
const ALVO_OPERACOES_POR_LINHA: i64 = 10_000_000;

fn fator_para(operacoes: i64) -> i64 {
    if operacoes <= 0 {
        1
    } else {
        (ALVO_OPERACOES_POR_LINHA / operacoes).max(1)
    }
}

fn mediana(mut valores: Vec<f64>) -> f64 {
    valores.sort_by(f64::total_cmp);
    valores[valores.len() / 2]
}

fn tabela(
    titulo: &str,
    exercicio: &str,
    entradas: &[i64],
    operacoes: fn(i64) -> i64,
    preparar: fn(i64) -> Vec<i64>,
    mut chamada: impl FnMut(i64, &[i64]),
) {
    println!("\n{titulo}  [{exercicio}]");
    println!(
        "{:>14} {:>20} {:>16} {:>13} {:>9}",
        "n", "operacoes previstas", "fator", "ns/chamada", "razao"
    );

    let mut anterior = -1.0f64;
    for &n in entradas {
        let trabalho = operacoes(n);
        let fator = fator_para(trabalho);
        // So o exercicio quadratico precisa de lista; construir (0..2^30) por
        // habitos seriam 8 GB de alocacao fora da zona cronometrada.
        let valores = preparar(n);

        let tempos: Vec<f64> = (0..REPETICOES)
            .map(|_| {
                let inicio = Instant::now();
                for _ in 0..fator {
                    chamada(n, &valores);
                }
                inicio.elapsed().as_nanos() as f64 / fator as f64
            })
            .collect();

        let ns = mediana(tempos);
        let razao = if anterior > 0.0 && ns > 0.0 {
            format!("{:.1}x", ns / anterior)
        } else {
            "-".to_string()
        };
        println!(
            "{:>14} {:>20} {:>16} {:>13.1} {:>9}",
            n, trabalho, fator, ns, razao
        );
        anterior = ns;
    }
}

fn sem_lista(_: i64) -> Vec<i64> {
    Vec::new()
}

/// O mesmo ciclo `0..n` de [`soma_ate`], com o acumulador entregue a `black_box` a
/// cada passo. Existe só neste binário, nunca no módulo do exercício.
///
/// Sem isto não há medição linear possível em Rust: em `--release` o LLVM reconhece
/// a série aritmética e substitui o ciclo pela forma fechada `n(n-1)/2`, que custa
/// ~5 ns independentemente de `n`. A mesma técnica salva a versão contada, porque
/// `cont.iteracoes += 1` num ciclo de `n` passos também é redutível a `+= n`.
#[inline(never)]
fn soma_ate_opaca(n: i64) -> i64 {
    let mut total = 0i64;
    for i in 0..n {
        total = black_box(total + i);
    }
    total
}

fn distintos(n: i64) -> Vec<i64> {
    (0..n).collect()
}

fn operacoes_lineares(n: i64) -> i64 {
    n
}

fn operacoes_quadraticas(n: i64) -> i64 {
    n * (n - 1) / 2
}

fn operacoes_log(n: i64) -> i64 {
    quantas_metades(n)
}

fn operacoes_nlogn(n: i64) -> i64 {
    (n / 2) * quantas_metades(n)
}

fn main() {
    println!("Tema 01 em Rust - mediana de {REPETICOES} repeticoes, cargo --release");
    println!("Maquina e data no README desta celula.");

    tabela(
        "linear PURO: o ciclo nao existe, o LLVM fechou a serie em O(1)",
        "soma_ate",
        &[100, 1_000, 10_000, 100_000, 1_000_000],
        operacoes_lineares,
        sem_lista,
        |n, _| {
            black_box(soma_ate(black_box(n)));
        },
    );

    tabela(
        "linear OPACO: acumulador por black_box, o ciclo de n iteracoes corre",
        "soma_ate_opaca",
        &[100, 1_000, 10_000, 100_000, 1_000_000],
        operacoes_lineares,
        sem_lista,
        |n, _| {
            black_box(soma_ate_opaca(black_box(n)));
        },
    );

    tabela(
        "quadratico: compara todos os pares, input sem repeticao",
        "tem_repetido",
        &[100, 200, 500, 1_000, 2_000, 5_000],
        operacoes_quadraticas,
        distintos,
        |_, valores| {
            black_box(tem_repetido(black_box(valores)));
        },
    );

    tabela(
        "logaritmico: divide por 2 ate chegar a 1",
        "quantas_metades",
        &[1 << 10, 1 << 14, 1 << 18, 1 << 24, 1 << 30],
        operacoes_log,
        sem_lista,
        |n, _| {
            black_box(quantas_metades(black_box(n)));
        },
    );

    tabela(
        "n log n: compoe os dois ciclos anteriores",
        "pares_sobre_metades",
        &[1_000, 10_000, 100_000],
        operacoes_nlogn,
        sem_lista,
        |n, _| {
            black_box(pares_sobre_metades(black_box(n)));
        },
    );

    println!("\nLeitura: a coluna de operacoes previstas e a forma fechada exata; ns/chamada e");
    println!("desta maquina, mediana de {REPETICOES} repeticoes. Um tempo que nao escale com a");
    println!("contagem indica chamada eliminada. Em Rust black_box no argumento nao chega: o");
    println!("LLVM fecha um ciclo redutivel mesmo com n opaco, por isso a linear vem em duas");
    println!("tabelas - a plana e a que corre.");
}
