import math

import pytest

from password_analyzer import (
    _has_repeated_run,
    _has_sequential_run,
    _pool_size,
    analyze,
    sha1_prefix,
)


def test_pool_counts_character_classes():
    assert _pool_size("abc") == 26
    assert _pool_size("abcABC") == 52
    assert _pool_size("abcABC123") == 62
    assert _pool_size("abcABC123!") == 94


def test_entropy_math():
    a = analyze("abcdefgh")  # 8 minusculas
    assert a.entropy_bits == pytest.approx(8 * math.log2(26), abs=0.1)


def test_common_password_scores_zero():
    a = analyze("password")
    assert a.score == 0
    assert any("mais usadas" in w for w in a.warnings)


def test_long_random_scores_high():
    a = analyze("Tr7$kQ9!mZ2@pL4#vX8&")
    assert a.score == 4


def test_short_password_warns():
    a = analyze("Ab1!")
    assert a.score <= 1
    assert any("curta" in w for w in a.warnings)


def test_repeated_and_sequential_detected():
    assert _has_repeated_run("aaabbb")
    assert not _has_repeated_run("abcdef")
    assert _has_sequential_run("abcd9!")
    assert not _has_sequential_run("a9Z$kQ")


def test_empty_raises():
    with pytest.raises(ValueError):
        analyze("")


def test_sha1_prefix_kanonymity_shape():
    # SHA-1("password") = 5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8
    prefix, suffix = sha1_prefix("password")
    assert prefix == "5BAA6"
    assert prefix + suffix == "5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8"
