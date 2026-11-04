"""CLI do scanner da propria rede local.

Uso tipico (sua casa/lab):
    python cli.py                      # sugere sua /24 e pede confirmacao
    python cli.py --network 192.168.1.0/24 --yes
    python cli.py --ports 22,80,443 --json
    python cli.py --use-nmap           # usa nmap se instalado
"""

from __future__ import annotations

import argparse
import json
import sys

from lan_scanner import (
    COMMON_PORTS,
    UnsafeTarget,
    default_network,
    parse_ports,
    scan,
    validate_network,
)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Varre SUA rede local (privada). Recusa qualquer alvo publico."
    )
    p.add_argument("--network", default=None,
                   help="CIDR privado, ex. 192.168.1.0/24 (padrao: sua /24)")
    p.add_argument("--ports", default=",".join(map(str, COMMON_PORTS)),
                   help="'22,80,8000-8010' (max 1000 portas)")
    p.add_argument("--use-nmap", action="store_true",
                   help="usar nmap se instalado (senao, ping+TCP padrao)")
    p.add_argument("--yes", action="store_true",
                   help="pula a confirmacao interativa")
    p.add_argument("--json", action="store_true", help="saida em JSON")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    cidr = args.network or default_network()
    try:
        net = validate_network(cidr)
    except UnsafeTarget as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        print("Use apenas sua rede privada (ex.: 192.168.1.0/24).", file=sys.stderr)
        return 2
    try:
        ports = parse_ports(args.ports)
    except ValueError as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 2

    hosts_count = max(net.num_addresses - 2, 1)
    if not args.yes:
        print(f"Rede alvo: {net} (~{hosts_count} hosts) · {len(ports)} porta(s)")
        print("Confirme que esta e SUA rede ou um lab autorizado.")
        try:
            ok = input("Continuar? [s/N] ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nCancelado.", file=sys.stderr)
            return 130
        if ok not in ("s", "sim", "y", "yes"):
            print("Cancelado.")
            return 0

    try:
        results = scan(net, ports, use_nmap=args.use_nmap)
    except RuntimeError as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(
            {"network": str(net),
             "hosts": [r.to_dict() for r in results]},
            indent=2,
        ))
        return 0

    print(f"\n{len(results)} host(s) ativo(s) em {net}:")
    for r in results:
        name = f" ({r.hostname})" if r.hostname else ""
        ports_s = ", ".join(map(str, r.open_ports)) if r.open_ports else "nenhuma porta comum aberta"
        print(f"  {r.ip}{name}: {ports_s}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
