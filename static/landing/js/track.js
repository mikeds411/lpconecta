/* Conta os cliques em "Falar no WhatsApp" (aparecem no painel em /painel/).
   Não interfere no link: o WhatsApp abre normalmente, e o envio é em segundo plano. */
(function () {
  "use strict";
  var URL = "/api/clique/";

  function enviar(dados) {
    var fd = new FormData();
    Object.keys(dados).forEach(function (k) { fd.append(k, dados[k]); });
    try {
      if (navigator.sendBeacon && navigator.sendBeacon(URL, fd)) return;
      fetch(URL, { method: "POST", body: fd, keepalive: true, credentials: "omit" });
    } catch (e) { /* contagem é opcional: nunca atrapalha a pessoa */ }
  }

  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a[data-clinic], a[data-wa-general]");
    if (!a) return;
    var geral = a.hasAttribute("data-wa-general");
    enviar({
      clinica: geral ? "geral" : a.getAttribute("data-clinic"),
      local: geral ? (a.classList.contains("fab") ? "flutuante" : "rodape") : "cartao",
      origem: document.referrer || ""
    });
  });
})();
