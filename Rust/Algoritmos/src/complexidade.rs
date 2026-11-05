//! Tema 01 — complexidade: os mesmos quatro ciclos das outras três linguagens.
//!
//! Cada exercício existe em versão pura (a que `src/bin/medir.rs` cronometra) e em
//! versão contada, que incrementa um [`Contador`] por operação básica. Os testes
//! afirmam a forma fechada exata da contagem — determinística entre máquinas e
//! entre linguagens — em vez de razões de tempo.

/// Registra quantas operações básicas um ciclo executou.
#[derive(Default)]
pub struct Contador {
    pub iteracoes: i64,
    pub comparacoes: i64,
}

/// Acumula `0 + 1 + ... + (n-1)`. Roda exatamente `n` iterações.
pub fn soma_ate(n: i64) -> i64 {
    let mut total = 0;
    for i in 0..n {
        total += i;
    }
    total
}

/// Mesmo ciclo de [`soma_ate`], contando cada iteração.
pub fn soma_ate_contado(n: i64, cont: &mut Contador) -> i64 {
    let mut total = 0;
    for i in 0..n {
        cont.iteracoes += 1;
        total += i;
    }
    total
}

/// Compara todos os pares até encontrar uma repetição.
pub fn tem_repetido(valores: &[i64]) -> bool {
    let n = valores.len();
    for i in 0..n {
        for j in (i + 1)..n {
            if valores[i] == valores[j] {
                return true;
            }
        }
    }
    false
}

/// Mesmo ciclo, contando as comparações feitas até decidir.
pub fn tem_repetido_contado(valores: &[i64], cont: &mut Contador) -> bool {
    let n = valores.len();
    for i in 0..n {
        for j in (i + 1)..n {
            cont.comparacoes += 1;
            if valores[i] == valores[j] {
                return true;
            }
        }
    }
    false
}

/// Quantas divisões por 2 levam de `n` até 1; zero quando `n <= 1`.
pub fn quantas_metades(n: i64) -> i64 {
    let mut resto = n;
    let mut passos = 0;
    while resto > 1 {
        resto /= 2;
        passos += 1;
    }
    passos
}

/// Mesmo ciclo, registrando cada divisão.
pub fn quantas_metades_contado(n: i64, cont: &mut Contador) -> i64 {
    let mut resto = n;
    let mut passos = 0;
    while resto > 1 {
        cont.iteracoes += 1;
        resto /= 2;
        passos += 1;
    }
    passos
}

/// Ciclo externo de `n/2` passos, cada um varrendo as metades de `n`: a forma
/// `n log n` a nascer da composição dos dois ciclos anteriores.
pub fn pares_sobre_metades(n: i64) -> i64 {
    let mut total = 0;
    for _ in 0..(n / 2) {
        total += quantas_metades(n);
    }
    total
}

/// Mesma composição, contando apenas o ciclo interno (o trabalho dominante).
pub fn pares_sobre_metades_contado(n: i64, cont: &mut Contador) -> i64 {
    let mut total = 0;
    for _ in 0..(n / 2) {
        let mut m = n;
        while m > 1 {
            cont.iteracoes += 1;
            m /= 2;
            total += 1;
        }
    }
    total
}
