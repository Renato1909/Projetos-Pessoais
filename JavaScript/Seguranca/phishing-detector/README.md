# phishing-detector

![CI](https://github.com/Renato1909/Projetos-Pessoais/actions/workflows/projetos-consolidados.yml/badge.svg)

Extensão de navegador (Manifest V3) **defensiva** que analisa a URL da página
com heurísticas **100% locais** e exibe um alerta quando há sinais de phishing.
Nada é enviado para lugar nenhum: sem telemetria, sem listas externas.

## Sinais detectados

| Sinal | Peso |
|---|---|
| Punycode (`xn--`, homógrafo) | +3 |
| IP no lugar do domínio | +3 |
| Marca conhecida fora do domínio oficial | +3 |
| `@` na URL | +2 |
| TLD muito usado em golpes (`.tk`, `.xyz`, `.click`…) | +2 |
| Campo de senha em página sem HTTPS | +2 |
| Formulário que envia para outro domínio | +2 |
| Hífen junto a marca, subdomínios demais, host longo, URL longa, encoding excessivo, porta estranha, sem HTTPS | +1 cada |

Níveis: **segura** (0–1) · **atenção** (2–3) · **suspeita** (4+).

## Instalar (modo desenvolvedor)

1. Abra `chrome://extensions` (ou `edge://extensions` / `about:debugging` no Firefox*).
2. Ative o **modo do desenvolvedor**.
3. **Carregar sem compactação** → selecione esta pasta.
4. Abra qualquer site: o ícone mostra o veredito; páginas suspeitas ganham faixa de alerta.

\* O manifest é MV3 (Chrome/Edge). No Firefox use `about:debugging` → mesmo fluxo.

## Testar as heurísticas

```powershell
node --test tests/heuristics.test.js
```

## Limitações (por design)

- Heurísticas não provam golpe nem inocência: é um **alerta educativo**, não antivírus.
- Marcas oficiais cobertas são uma lista curta de exemplo.
- Golpistas evoluem; listas locais nunca substituem bom senso + 2FA.

## Localização neste repositório

Este projeto está em `JavaScript/Seguranca/phishing-detector/`. A partir da raiz de `Projetos-Pessoais`, execute `cd JavaScript/Seguranca/phishing-detector` antes de utilizar os comandos acima.

A integração contínua é definida no [workflow compartilhado](../../../.github/workflows/projetos-consolidados.yml), com execução no diretório deste projeto. O [repositório de origem](https://github.com/Renato1909/phishing-detector) permanece preservado. Consulte o [registro de consolidação](../../../docs/CONSOLIDACAO.md) para conhecer o escopo desta organização.

## Licença

[MIT](LICENSE)

