/* Content script: analisa a pagina atual e exibe faixa de alerta se suspeita. */
(function () {
  const H = window.PhishingHeuristics;
  if (!H) return;

  const base = H.analyzeUrl(location.href);
  const result = H.analyzePage(base, document);
  if (result.level === "segura") return;

  const bar = document.createElement("div");
  const bg = result.level === "suspeita" ? "#b00020" : "#b26a00";
  bar.setAttribute("role", "alert");
  bar.style.cssText =
    `position:fixed;top:0;left:0;right:0;z-index:2147483647;background:${bg};` +
    "color:#fff;font:14px/1.4 system-ui,sans-serif;padding:10px 48px 10px 16px;";
  const items = result.signals.map((s) => `• ${s.msg}`).join("<br>");
  bar.innerHTML =
    `<strong>Alerta de possível phishing (nível: ${result.level}, pontos: ${result.score}).</strong><br>${items}`;

  const close = document.createElement("button");
  close.textContent = "✕";
  close.setAttribute("aria-label", "Fechar alerta");
  close.style.cssText =
    "position:absolute;right:10px;top:8px;background:transparent;border:0;color:#fff;font-size:16px;cursor:pointer;";
  close.onclick = () => bar.remove();
  bar.appendChild(close);

  const push = () => { document.body.style.marginTop = bar.offsetHeight + "px"; };
  document.documentElement.prepend(bar);
  if (document.body) push();
  else new MutationObserver((_, obs) => { if (document.body) { push(); obs.disconnect(); } })
    .observe(document.documentElement, { childList: true });
})();
