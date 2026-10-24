# lan-scanner

![CI](https://github.com/Renato1909/lan-scanner/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.11%2B-blue)

Scanner **defensivo** da **própria rede local**: descobre hosts ativos e lista
portas TCP comuns abertas. Usa `nmap` quando disponível (`--use-nmap`),
senão ping do sistema + TCP connect (só biblioteca padrão).

> **Uso autorizado apenas.** Varra somente redes que são suas ou labs com
> permissão explícita. Escanear redes de terceiros sem autorização é crime
> (Lei 12.737/2012 no Brasil).

## Travas de segurança (sempre ativas)

- Só aceita IPv4 **privado**: `10/8`, `172.16/12`, `192.168/16`, `127/8`, `169.254/16`.
- **Recusa**: IPs/faixas públicas, `0.0.0.0/0`, multicast, redes maiores que `/16`.
- Máximo de 1000 portas por varredura.
- **Confirmação interativa** mostrando rede + nº de hosts (pule com `--yes`).

## Como rodar

```powershell
python cli.py                                # sugere sua /24 e pede confirmação
python cli.py --network 192.168.1.0/24 --yes
python cli.py --ports 22,80,443 --json
python cli.py --use-nmap                     # requer nmap instalado
```

Exemplo de saída:

```
3 host(s) ativo(s) em 192.168.1.0/24:
  192.168.1.1 (router.lan): 80, 443
  192.168.1.10: 22, 8080
  192.168.1.15: nenhuma porta comum aberta
```

## Instalando o nmap (opcional)

- Windows: `winget install Insecure.Nmap`
- Ubuntu: `sudo apt install nmap`

Sem ele, o scanner usa ping + sockets — mais lento, mas sem dependências.

## Como testar

```powershell
pip install pytest
pytest -v
```

Os testes são herméticos (validação de alvos + listener local em `127.0.0.1`),
não tocam em rede real.

## Licença

[MIT](LICENSE)
