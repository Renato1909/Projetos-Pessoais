import socket
import threading

import pytest

from lan_scanner import (
    UnsafeTarget,
    parse_ports,
    scan_ports_tcp,
    validate_network,
)


def test_private_ranges_accepted():
    for cidr in ("192.168.1.0/24", "10.0.0.0/16", "172.16.0.0/20",
                 "127.0.0.0/24", "169.254.0.0/16"):
        assert str(validate_network(cidr)) == cidr.split("/")[0] + "/" + cidr.split("/")[1]


def test_public_and_special_refused():
    for cidr in ("8.8.8.0/24", "1.1.1.1/32", "0.0.0.0/0", "224.0.0.0/4",
                 "2001:db8::/32", "999.1.1.0/24"):
        with pytest.raises(UnsafeTarget):
            validate_network(cidr)


def test_too_large_refused():
    with pytest.raises(UnsafeTarget):
        validate_network("10.0.0.0/8")  # /8 < /16


def test_parse_ports():
    assert parse_ports("22,80,8000-8002") == [22, 80, 8000, 8001, 8002]
    assert parse_ports("443,443, 80") == [80, 443]
    with pytest.raises(ValueError):
        parse_ports("0")
    with pytest.raises(ValueError):
        parse_ports("22-70000")
    with pytest.raises(ValueError):
        parse_ports("")


def test_tcp_scan_finds_local_listener():
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", 0))
    srv.listen(1)
    port = srv.getsockname()[1]

    def serve():
        try:
            conn, _ = srv.accept()
            conn.close()
        except OSError:
            pass

    t = threading.Thread(target=serve, daemon=True)
    t.start()
    try:
        found = scan_ports_tcp(["127.0.0.1"], [port, 9], timeout=1.0)
        assert port in found["127.0.0.1"]
        assert 9 not in found["127.0.0.1"]
    finally:
        srv.close()
