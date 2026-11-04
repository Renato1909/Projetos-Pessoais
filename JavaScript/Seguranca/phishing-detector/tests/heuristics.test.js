import { describe, it } from "node:test";
import assert from "node:assert/strict";
import pkg from "../heuristics.js";

const { analyzeUrl } = pkg;

describe("analyzeUrl", () => {
  it("site oficial e pontuacao baixa", () => {
    const r = analyzeUrl("https://www.paypal.com/signin");
    assert.equal(r.level, "segura");
  });

  it("marca fora do dominio oficial e suspeita", () => {
    const r = analyzeUrl("http://paypal-seguro-login.tk/entrar");
    assert.equal(r.level, "suspeita");
    assert.ok(r.signals.some((s) => s.id === "marca-suspeita"));
  });

  it("IP no host e punycode somam pontos", () => {
    const ip = analyzeUrl("http://192.168.0.1/login");
    assert.ok(ip.signals.some((s) => s.id === "ip-no-host"));
    const puny = analyzeUrl("https://xn--pypal-4ve.com/");
    assert.ok(puny.signals.some((s) => s.id === "punycode"));
  });

  it("@ na URL e detectado", () => {
    const r = analyzeUrl("https://banco.com@evil.xyz/login");
    assert.ok(r.signals.some((s) => s.id === "arroba"));
  });

  it("http sem https gera apenas atencao leve", () => {
    const r = analyzeUrl("http://exemplo.com/");
    assert.ok(["segura", "atencao"].includes(r.level));
    assert.ok(r.signals.some((s) => s.id === "sem-https"));
  });

  it("URL invalida retorna nivel invalida", () => {
    assert.equal(analyzeUrl("::://").level, "invalida");
  });

  it("whatsapp falso e pego", () => {
    const r = analyzeUrl("https://whatsapp-web-verificacao.click/login");
    assert.equal(r.level, "suspeita");
  });
});
