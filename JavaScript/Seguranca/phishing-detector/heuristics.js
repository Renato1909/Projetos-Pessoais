/* Heuristicas 100% locais de deteccao de phishing.
 * Sem rede, sem telemetria, sem listas externas: so analise da URL.
 * Exporta `analyzeUrl` (tambem funciona como script classico no browser).
 */
(function (root, factory) {
  const api = factory();
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.PhishingHeuristics = api;
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  const SUSPICIOUS_TLDS = new Set([
    "tk", "ml", "ga", "cf", "gq", "top", "xyz", "click", "link",
    "zip", "mov", "quest", "sbs", "cyou", "buzz", "info",
  ]);

  // marca -> dominios oficiais (terminacoes validas)
  const BRANDS = {
    paypal: ["paypal.com"],
    apple: ["apple.com", "icloud.com"],
    google: ["google.com", "gmail.com", "youtube.com"],
    microsoft: ["microsoft.com", "live.com", "outlook.com", "office.com"],
    instagram: ["instagram.com"],
    whatsapp: ["whatsapp.com"],
    facebook: ["facebook.com"],
    nubank: ["nubank.com.br"],
    itau: ["itau.com.br"],
    bradesco: ["bradesco.com.br"],
    caixa: ["caixa.gov.br"],
    bancodobrasil: ["bb.com.br"],
    santander: ["santander.com.br"],
    mercadolivre: ["mercadolivre.com.br"],
    amazon: ["amazon.com", "amazon.com.br"],
    netflix: ["netflix.com"],
    correios: ["correios.com.br"],
  };

  const IPV4 = /^\d{1,3}(\.\d{1,3}){3}$/;

  function isIp(host) {
    if (IPV4.test(host)) return true;
    return host.includes(":"); // IPv6 contem ':'
  }

  function brandImpersonation(host) {
    const h = host.toLowerCase();
    const findings = [];
    for (const [brand, official] of Object.entries(BRANDS)) {
      if (!h.includes(brand)) continue;
      const legit = official.some((d) => h === d || h.endsWith("." + d));
      if (!legit) findings.push(brand);
    }
    return findings;
  }

  function analyzeUrl(raw) {
    const signals = [];
    let url;
    try {
      url = new URL(raw);
    } catch {
      return { score: 0, level: "invalida", signals: [{ id: "url-invalida", w: 0, msg: "URL invalida" }] };
    }
    const host = url.hostname.toLowerCase();
    const add = (id, w, msg) => signals.push({ id, w, msg });

    if (host.includes("xn--")) add("punycode", 3, "domínio com punycode (xn--): possível homógrafo");
    if (isIp(host)) add("ip-no-host", 3, "endereço IP no lugar de domínio");
    if (raw.includes("@")) add("arroba", 2, "'@' na URL (tudo antes dele é ignorado pelo navegador)");
    const brands = brandImpersonation(host);
    if (brands.length) add("marca-suspeita", 3, `cita marca conhecida (${brands.join(", ")}) fora do domínio oficial`);
    if (brands.length && host.includes("-")) add("hifen-marca", 1, "hífen junto a nome de marca");
    const tld = host.split(".").pop() || "";
    if (SUSPICIOUS_TLDS.has(tld)) add("tld-suspeito", 2, `TLD .${tld} muito usado em golpes`);
    const labels = host.split(".").filter(Boolean);
    if (labels.length > 4) add("subdominios", 1, `${labels.length} níveis de subdomínio`);
    if (host.length > 30) add("host-longo", 1, "nome de host muito longo");
    if (url.protocol === "http:") add("sem-https", 1, "página sem HTTPS");
    if (raw.length > 120) add("url-longa", 1, "URL com mais de 120 caracteres");
    if ((raw.match(/%[0-9a-fA-F]{2}/g) || []).length > 3) add("encoding", 1, "muitos trechos %-codificados");
    if (url.port && !["80", "443", ""].includes(url.port)) add("porta", 1, `porta não padrão (:${url.port})`);

    const score = signals.reduce((s, x) => s + x.w, 0);
    const level = score >= 4 ? "suspeita" : score >= 2 ? "atencao" : "segura";
    return { score, level, signals };
  }

  /** Checagens que dependem do DOM da pagina (só no content script). */
  function analyzePage(urlResult, doc) {
    const signals = urlResult.signals.slice();
    let score = urlResult.score;
    const hasPassword = !!doc.querySelector('input[type="password"]');
    if (hasPassword && doc.location.protocol === "http:") {
      signals.push({ id: "senha-sem-https", w: 2, msg: "campo de senha em página sem HTTPS" });
      score += 2;
    }
    const forms = Array.from(doc.querySelectorAll("form[action]"));
    const pageHost = doc.location.hostname.toLowerCase();
    const crossDomain = forms.some((f) => {
      try {
        return new URL(f.action, doc.baseURI).hostname.toLowerCase() !== pageHost;
      } catch {
        return false;
      }
    });
    if (crossDomain && hasPassword) {
      signals.push({ id: "form-externo", w: 2, msg: "formulário envia dados para outro domínio" });
      score += 2;
    }
    const level = score >= 4 ? "suspeita" : score >= 2 ? "atencao" : "segura";
    return { score, level, signals };
  }

  return { analyzeUrl, analyzePage, SUSPICIOUS_TLDS, BRANDS };
});
