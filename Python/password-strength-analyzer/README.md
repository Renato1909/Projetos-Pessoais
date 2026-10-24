# password-strength-analyzer

![CI](https://github.com/Renato1909/password-strength-analyzer/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.11%2B-blue)

Analisador **defensivo** de força de senhas: entropia, tempo estimado de quebra,
alertas de padrão fraco e consulta de vazamentos **sem enviar a senha**
(k-anonimato da API HaveIBeenPwned: só os 5 primeiros caracteres do SHA-1
saem da máquina).

## Como rodar

Requisitos: Python 3.11+ (só biblioteca padrão).

```powershell
python cli.py                # lê a senha sem eco (getpass)
python cli.py --no-breach    # modo totalmente offline
python cli.py --json         # saída em JSON (sem a senha)
```

## O que ele verifica

| Checagem | Como |
|---|---|
| Entropia | `tamanho × log2(alfabeto detectado)` |
| Tempo de quebra | metade do espaço de busca ÷ 10¹⁰ tent/s (GPU) e ÷ 10 tent/s (online com limite) |
| Senhas comuns | lista local das mais usadas (+ variações óbvias) |
| Padrões fracos | repetição (`aaa`), sequência (`abcd`, `1234`), teclado (`qwerty`) |
| Vazamentos | `GET https://api.pwnedpasswords.com/range/{5 chars}` e compara o sufixo localmente |

## Como testar

```powershell
pip install pytest
pytest -v
```

## Privacidade

- A senha **nunca** é impressa, registrada em log ou salva.
- A consulta de vazamentos envia apenas o prefixo do hash (modelo k-anonimato).
- Sem internet, o programa avisa e continua só com a análise local.

## Limitações (por design)

- Entropia por "tamanho × alfabeto" é um limite superior otimista; senhas
  com palavras reais têm entropia efetiva menor.
- Tempos de quebra são ordens de grandeza, não garantias.

## Licença

[MIT](LICENSE)
