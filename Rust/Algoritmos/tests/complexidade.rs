//! Testes do tema 01 em Rust: a contagem exata bate com a forma fechada.

use algoritmos::complexidade::{
    Contador, pares_sobre_metades, pares_sobre_metades_contado, quantas_metades,
    quantas_metades_contado, soma_ate, soma_ate_contado, tem_repetido, tem_repetido_contado,
};

const TAMANHOS: [i64; 10] = [0, 1, 2, 3, 4, 7, 8, 100, 1024, 10_000];
// O ciclo duplo a 10^4 custa 5*10^7 comparacoes; a escala grande nao e necessaria
// para provar uma forma fechada.
const TAMANHOS_QUADRATICOS: [i64; 9] = [0, 1, 2, 3, 4, 7, 8, 100, 250];

fn distintos(n: i64) -> Vec<i64> {
    (0..n).collect()
}

#[test]
fn soma_ate_roda_n_iteracoes() {
    for n in TAMANHOS {
        let mut cont = Contador::default();
        assert_eq!(soma_ate_contado(n, &mut cont), n * (n - 1) / 2);
        assert_eq!(cont.iteracoes, n);
        assert_eq!(soma_ate(n), soma_ate_contado(n, &mut Contador::default()));
    }
}

#[test]
fn quantas_metades_conta_divisoes_reais() {
    let casos = [
        (1, 0),
        (2, 1),
        (3, 1),
        (4, 2),
        (7, 2),
        (8, 3),
        (9, 3),
        (1024, 10),
        (1_000_000, 19),
    ];
    for (n, queria) in casos {
        let mut cont = Contador::default();
        assert_eq!(quantas_metades_contado(n, &mut cont), queria);
        assert_eq!(cont.iteracoes, queria);
        assert_eq!(quantas_metades(n), queria);
    }
}

#[test]
fn tem_repetido_varre_pares_inteiros_quando_nao_ha_repeticao() {
    for n in TAMANHOS_QUADRATICOS {
        let valores = distintos(n);
        let mut cont = Contador::default();
        assert!(!tem_repetido_contado(&valores, &mut cont));
        assert_eq!(cont.comparacoes, n * (n - 1) / 2);
        assert!(!tem_repetido(&valores));
    }
}

#[test]
fn tem_repetido_para_na_comparacao_que_decide() {
    let valores = [0, 1, 2, 3, 4, 5, 0];
    let mut cont = Contador::default();
    assert!(tem_repetido_contado(&valores, &mut cont));
    assert_eq!(cont.comparacoes, valores.len() as i64 - 1);
}

#[test]
fn pares_sobre_metades_eh_n_log_n_em_contagem_exata() {
    for n in TAMANHOS {
        let esperado = (n / 2) * quantas_metades(n);
        let mut cont = Contador::default();
        assert_eq!(pares_sobre_metades_contado(n, &mut cont), esperado);
        assert_eq!(cont.iteracoes, esperado);
        assert_eq!(pares_sobre_metades(n), esperado);
    }
}
