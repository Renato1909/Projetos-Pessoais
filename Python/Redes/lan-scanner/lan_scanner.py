"""Scanner defensivo da PROPRIA rede local (uso autorizado/lab).

Travas de seguranca (nao removiveis via CLI):
  * so aceita IPv4 privado: 10/8, 172.16/12, 192.168/16, 127/8, 169.254/16
  * recusa 0.0.0.0/0, faixas publicas, multicast, reservadas e /prefixo < 16
  * pede confirmacao interativa, salvo --yes

Descoberta de hosts: `nmap -sn` se disponivel (--use-nmap), senao ping do
sistema em paralelo. Portas: TCP connect nas portas informadas.
"""

from __future__ import annotations

import ipaddress
import platform
import shutil
import socket
import subprocess
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field

COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445,
                993, 995, 1723, 3306, 3389, 5900, 8080, 8443]

MAX_HOSTS = 65534  # recusa redes maiores que uma /16


class UnsafeTarget(ValueError):
    """Alvo fora da propria rede privada."""


def validate_network(cidr: str) -> ipaddress.IPv4Network:
    """Valida e retorna a rede; levanta UnsafeTarget se nao for rede privada."""
    try:
        net = ipaddress.ip_network(cidr, strict=False)
    except ValueError as exc:
        raise UnsafeTarget(f"rede invalida: {cidr}") from exc
    if not isinstance(net, ipaddress.IPv4Network):
        raise UnsafeTarget("apenas IPv4 e suportado")
    if (
        net.is_multicast
        or net.is_unspecified
        or net.is_reserved
        or net.is_global
        or not (net.is_private or net.is_loopback or net.is_link_local)
    ):
        raise UnsafeTarget(
            f"recusado: {net} nao e rede privada local "
            "(permitido: 10/8, 172.16/12, 192.168/16, 127/8, 169.254/16)"
        )
    if net.prefixlen < 16:
        raise UnsafeTarget(f"recusado: {net} e grande demais (minimo /16)")
    if net.num_addresses - 2 > MAX_HOSTS:
        raise UnsafeTarget(f"recusado: {net} tem hosts demais")
    return net


def parse_ports(spec: str) -> list[int]:
    """'22,80,8000-8010' -> lista ordenada sem duplicatas (1..65535)."""
    ports: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            lo_s, hi_s = part.split("-", 1)
            lo, hi = int(lo_s), int(hi_s)
            if not (1 <= lo <= hi <= 65535):
                raise ValueError(f"faixa invalida: {part}")
            ports.update(range(lo, hi + 1))
        else:
            p = int(part)
            if not 1 <= p <= 65535:
                raise ValueError(f"porta invalida: {part}")
            ports.add(p)
        if len(ports) > 1000:
            raise ValueError("maximo de 1000 portas por varredura")
    if not ports:
        raise ValueError("informe ao menos uma porta")
    return sorted(ports)


def local_outbound_ip() -> str:
    """IP local usado para sair (connect UDP nao envia pacotes)."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]


def default_network() -> str:
    """Sugere a /24 do IP local, se privada; senao, loopback."""
    try:
        ip = local_outbound_ip()
        if ipaddress.ip_address(ip).is_private:
            return str(ipaddress.ip_network(f"{ip}/24", strict=False))
    except OSError:
        pass
    return "127.0.0.0/24"


def _ping(ip: str, timeout_ms: int = 600) -> bool:
    if platform.system() == "Windows":
        cmd = ["ping", "-n", "1", "-w", str(timeout_ms), ip]
    else:
        cmd = ["ping", "-c", "1", "-W", str(max(timeout_ms // 1000, 1)), ip]
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=(timeout_ms / 1000) + 5)
        return r.returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def _nmap_available() -> bool:
    return shutil.which("nmap") is not None


def discover_nmap(net: ipaddress.IPv4Network) -> list[str]:
    out = subprocess.run(
        ["nmap", "-sn", "-oG", "-", str(net)],
        capture_output=True, text=True, timeout=300,
    )
    if out.returncode != 0:
        raise RuntimeError(f"nmap -sn falhou: {out.stderr.strip()[:200]}")
    live = []
    for line in out.stdout.splitlines():
        # "Host: 192.168.1.1 (...)	Status: Up"
        if line.startswith("Host:") and "Status: Up" in line:
            live.append(line.split()[1])
    return sorted(live, key=ipaddress.ip_address)


def discover_ping(net: ipaddress.IPv4Network, workers: int = 64) -> list[str]:
    ips = [str(h) for h in net.hosts()]
    if net.is_loopback and not ips:
        ips = ["127.0.0.1"]
    with ThreadPoolExecutor(max_workers=workers) as pool:
        alive = pool.map(_ping, ips)
    return sorted(
        (ip for ip, ok in zip(ips, alive) if ok), key=ipaddress.ip_address
    )


def scan_ports_nmap(hosts: list[str], ports: list[int]) -> dict[str, list[int]]:
    if not hosts:
        return {}
    out = subprocess.run(
        ["nmap", "-p", ",".join(map(str, ports)), "--open", "-oG", "-", *hosts],
        capture_output=True, text=True, timeout=600,
    )
    if out.returncode != 0:
        raise RuntimeError(f"nmap falhou: {out.stderr.strip()[:200]}")
    result: dict[str, list[int]] = {h: [] for h in hosts}
    cur = None
    for line in out.stdout.splitlines():
        if line.startswith("Host:"):
            cur = line.split()[1]
        elif line.startswith("Ports:") and cur:
            for field in line[len("Ports:"):].split(","):
                parts = field.strip().split("/")
                if len(parts) >= 2 and parts[1] == "open":
                    try:
                        result[cur].append(int(parts[0]))
                    except ValueError:
                        pass
    return {h: sorted(p) for h, p in result.items()}


def _tcp_open(ip: str, port: int, timeout: float) -> bool:
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except OSError:
        return False


def scan_ports_tcp(hosts: list[str], ports: list[int],
                   timeout: float = 0.7, workers: int = 100) -> dict[str, list[int]]:
    result: dict[str, list[int]] = {h: [] for h in hosts}

    def probe(host: str, port: int) -> tuple[str, int, bool]:
        return host, port, _tcp_open(host, port, timeout)

    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(probe, h, p) for h in hosts for p in ports]
        for f in futures:
            host, port, is_open = f.result()
            if is_open:
                result[host].append(port)
    return {h: sorted(p) for h, p in result.items()}


def reverse_dns(ip: str) -> str:
    try:
        return socket.gethostbyaddr(ip)[0]
    except (OSError, socket.herror):
        return ""


@dataclass
class HostResult:
    ip: str
    hostname: str = ""
    open_ports: list[int] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {"ip": self.ip, "hostname": self.hostname, "open_ports": self.open_ports}


def scan(net: ipaddress.IPv4Network, ports: list[int],
         use_nmap: bool = False) -> list[HostResult]:
    """Executa descoberta + varredura e retorna resultados ordenados por IP."""
    if use_nmap:
        if not _nmap_available():
            raise RuntimeError("nmap nao encontrado no PATH; instale ou omita --use-nmap")
        live = discover_nmap(net)
        portmap = scan_ports_nmap(live, ports) if live else {}
    else:
        live = discover_ping(net)
        portmap = scan_ports_tcp(live, ports) if live else {}

    results = [
        HostResult(ip=ip, hostname=reverse_dns(ip), open_ports=portmap.get(ip, []))
        for ip in live
    ]
    return results
