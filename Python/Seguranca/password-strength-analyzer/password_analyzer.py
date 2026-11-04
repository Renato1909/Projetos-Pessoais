"""Analisador defensivo de forca de senhas.

Nao armazena, registra em log nem transmite a senha. A verificacao de
vazamentos usa k-anonimato (HaveIBeenPwned range API): apenas os 5
primeiros caracteres hex do SHA-1 saem da maquina.
"""

from __future__ import annotations

import hashlib
import math
import unicodedata
from dataclasses import dataclass, field

COMMON_PASSWORDS = frozenset(
    """
    123456 123456789 qwerty password 12345678 111111 123123 12345 1234567
    qwerty123 1q2w3e4r admin letmein welcome monkey dragon football
    senha senha123 brasil123 123mudar qwertyuiop abc123 password1
    """.split()
)

SEQUENTIAL_RUNS = (
    "abcdefghijklmnopqrstuvwxyz",
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "0123456789",
    "qwertyuiopasdfghjklzxcvbnm",
)

GUESSES_PER_SECOND_OFFLINE = 10_000_000_000  # GPU moderna (estimativa)
GUESSES_PER_SECOND_ONLINE = 10  # login online com throttle


@dataclass
class Analysis:
    length: int
    pool_size: int
    entropy_bits: float
    score: int  # 0..4
    label: str
    crack_time_offline: str
    crack_time_online: str
    warnings: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)


def _pool_size(password: str) -> int:
    pool = 0
    if any(c.islower() for c in password):
        pool += 26
    if any(c.isupper() for c in password):
        pool += 26
    if any(c.isdigit() for c in password):
        pool += 10
    if any(not c.isalnum() and not c.isspace() and ord(c) < 128 for c in password):
        pool += 32
    if any(c.isspace() for c in password):
        pool += 1  # espaco conta pouco; o ganho real vem do comprimento
    if any(ord(c) > 127 for c in password):
        pool += 100  # unicode amplia muito o alfabeto
    return pool


def _has_repeated_run(password: str, run: int = 3) -> bool:
    lowered = password.lower()
    return any(
        lowered[i] * run == lowered[i : i + run]
        for i in range(len(lowered) - run + 1)
    )


def _has_sequential_run(password: str, run: int = 4) -> bool:
    lowered = password.lower()
    for i in range(len(lowered) - run + 1):
        window = lowered[i : i + run]
        if any(window in seq or window in seq[::-1] for seq in SEQUENTIAL_RUNS):
            return True
    return False


def _is_keyboard_walk(password: str) -> bool:
    return _has_sequential_run(password)


def _human_duration(seconds: float) -> str:
    if seconds < 1:
        return "menos de 1 segundo"
    minute, hour, day, year = 60, 3600, 86400, 365.25 * 86400
    if seconds < minute:
        return f"{seconds:.0f} segundos"
    if seconds < hour:
        return f"{seconds / minute:.0f} minutos"
    if seconds < day:
        return f"{seconds / hour:.1f} horas"
    if seconds < year:
        return f"{seconds / day:.1f} dias"
    if seconds < year * 100:
        return f"{seconds / year:.1f} anos"
    if seconds < year * 1_000_000:
        return f"{seconds / year / 1_000:.1f} mil anos"
    return "praticamente impossivel (tempo astronomico)"


def analyze(password: str) -> Analysis:
    if not isinstance(password, str) or not password:
        raise ValueError("informe uma senha nao vazia")

    length = len(password)
    pool = _pool_size(password)
    entropy = length * math.log2(pool) if pool > 1 else 0.0

    warnings: list[str] = []
    suggestions: list[str] = []

    if length < 12:
        warnings.append(f"curta ({length} caracteres); prefira 14 ou mais")
        suggestions.append("use uma frase-senha longa em vez de palavra curta")
    if password.lower() in COMMON_PASSWORDS:
        warnings.append("esta entre as senhas mais usadas do mundo")
        suggestions.append("nunca reuse senhas populares; use gerador aleatorio")
    if password.strip().lower() in COMMON_PASSWORDS or password.lower().rstrip("123!@#") in COMMON_PASSWORDS:
        if "esta entre as senhas mais usadas do mundo" not in warnings:
            warnings.append("variacao obvia de senha muito usada")
    if _has_repeated_run(password):
        warnings.append("contem repeticao (ex.: 'aaa', '111')")
    if _has_sequential_run(password):
        warnings.append("contem sequencia (ex.: 'abcd', '1234')")
    if _is_keyboard_walk(password):
        suggestions.append("evite sequencias de teclado como 'qwerty'")
    classes = sum(
        [
            any(c.islower() for c in password),
            any(c.isupper() for c in password),
            any(c.isdigit() for c in password),
            any(ord(c) < 128 and not c.isalnum() for c in password),
        ]
    )
    if classes < 3 and length < 16:
        suggestions.append("misture maiusculas, minusculas, numeros e simbolos")

    # Pontuacao 0..4 baseada em entropia, com penalidades.
    if entropy < 28:
        score = 0
    elif entropy < 40:
        score = 1
    elif entropy < 60:
        score = 2
    elif entropy < 90:
        score = 3
    else:
        score = 4
    if password.lower() in COMMON_PASSWORDS:
        score = 0
    elif warnings:
        score = max(0, score - 1)

    labels = ["muito fraca", "fraca", "razoavel", "forte", "muito forte"]
    guesses = 2 ** max(entropy - 1, 0)  # media: metade do espaco

    return Analysis(
        length=length,
        pool_size=pool,
        entropy_bits=round(entropy, 1),
        score=score,
        label=labels[score],
        crack_time_offline=_human_duration(guesses / GUESSES_PER_SECOND_OFFLINE),
        crack_time_online=_human_duration(guesses / GUESSES_PER_SECOND_ONLINE),
        warnings=warnings,
        suggestions=suggestions,
    )


def sha1_prefix(password: str) -> tuple[str, str]:
    """Retorna (prefixo5, resto) do SHA-1 em maiusculas (modelo k-anonimato)."""
    digest = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    return digest[:5], digest[5:]


def check_breach_count(password: str, timeout: float = 10.0) -> int | None:
    """Consulta vazamentos sem enviar a senha (k-anonimato HIBP).

    Retorna o numero de ocorrencias, 0 se nao vazou, ou None se offline/erro.
    """
    import urllib.request

    prefix, suffix = sha1_prefix(password)
    req = urllib.request.Request(
        f"https://api.pwnedpasswords.com/range/{prefix}",
        headers={"User-Agent": "password-strength-analyzer (estudo defensivo)"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", errors="replace")
    except Exception:
        return None
    for line in body.splitlines():
        if ":" not in line:
            continue
        suf, count = line.split(":", 1)
        if suf.strip().upper() == suffix:
            try:
                return int(count.strip())
            except ValueError:
                return None
    return 0


def _normalized_ascii(password: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFKD", password) if not unicodedata.combining(c)
    )
