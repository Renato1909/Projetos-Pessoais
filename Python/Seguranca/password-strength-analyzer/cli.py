"""CLI do analisador de forca de senhas.

A senha e lida com getpass (sem eco) e nunca e impressa, registrada ou
salva. Use --json para saida legivel por maquina (ainda sem a senha).
"""

from __future__ import annotations

import argparse
import getpass
import json
import sys

from password_analyzer import analyze, check_breach_count


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Analisa forca de senha (entropia + vazamentos, sem enviar a senha)."
    )
    p.add_argument(
        "--no-breach",
        action="store_true",
        help="pula a consulta de vazamentos (modo totalmente offline)",
    )
    p.add_argument(
        "--json", action="store_true", help="imprime o resultado em JSON"
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        password = getpass.getpass("Digite a senha a analisar (nao sera exibida): ")
    except (EOFError, KeyboardInterrupt):
        print("\nCancelado.", file=sys.stderr)
        return 130
    if not password:
        print("Senha vazia.", file=sys.stderr)
        return 2

    result = analyze(password)

    breach: int | None | str = "nao verificado (offline)"
    if not args.no_breach:
        count = check_breach_count(password)
        breach = "indisponivel (sem internet?)" if count is None else count
        if isinstance(breach, int) and breach > 0:
            result.warnings.append(
                f"aparece em {breach:,} vazamentos conhecidos: troque-a em todo lugar onde foi usada"
            )
            result.score = 0
            result.label = "muito fraca"
        # Remove a senha da memoria asim que possivel (melhor esforco).
        password = "*" * len(password)
        del password

    if args.json:
        print(
            json.dumps(
                {
                    "length": result.length,
                    "entropy_bits": result.entropy_bits,
                    "score": result.score,
                    "label": result.label,
                    "crack_time_offline": result.crack_time_offline,
                    "crack_time_online": result.crack_time_online,
                    "breach_count": breach,
                    "warnings": result.warnings,
                    "suggestions": result.suggestions,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    bar = "#" * (result.score + 1) + "-" * (4 - result.score)
    print(f"\nForca: {result.label} [{bar}] ({result.entropy_bits} bits, {result.length} caracteres)")
    print(f"Quebra estimada offline (GPU): {result.crack_time_offline}")
    print(f"Quebra estimada online (com limite): {result.crack_time_online}")
    print(f"Vazamentos conhecidos: {breach if isinstance(breach, str) else f'{breach:,} ocorrência(s)'}")
    for w in result.warnings:
        print(f"  ! {w}")
    for s in dict.fromkeys(result.suggestions):
        print(f"  > {s}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
