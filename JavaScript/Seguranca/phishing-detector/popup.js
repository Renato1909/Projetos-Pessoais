/* Popup: mostra o veredito da aba atual e permite checar uma URL colada. */
(function () {
  const H = window.PhishingHeuristics;
  const box = document.getElementById("result");

  function render(result) {
    const sigs = result.signals.length
      ? `<ul>${result.signals.map((s) => `<li>${escapeHtml(s.msg)} (+${s.w})</li>`).join("")}</ul>`
      : "<p>Nenhum sinal suspeito encontrado.</p>";
    box.innerHTML =
      `<span class="badge ${result.level}"> ${result.level.toUpperCase()} · ${result.score} pts</span>${sigs}`;
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  }

  function show(url) {
    render(H.analyzeUrl(url));
  }

  if (chrome?.tabs?.query) {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs[0]?.url) show(tabs[0].url);
      else box.textContent = "Não foi possível ler a aba atual.";
    });
  } else {
    box.textContent = "Abra pela extensão para analisar a aba atual.";
  }

  document.getElementById("check").onclick = () => {
    const v = document.getElementById("manual").value.trim();
    if (v) show(v);
  };
})();
