(function () {
  "use strict";

  var cfg = window.CONECTA_CONFIG || { whatsappGeral: "", clinicas: {} };
  var body = document.body;

  /* ---------- WhatsApp: monta os links a partir do config.js ---------- */
  function waLink(numero, texto) {
    var url = "https://wa.me/" + String(numero).replace(/\D/g, "");
    return texto ? url + "?text=" + encodeURIComponent(texto) : url;
  }

  document.querySelectorAll("a[data-clinic]").forEach(function (a) {
    var c = cfg.clinicas[a.getAttribute("data-clinic")];
    if (!c) return;
    var numero = c.whatsapp || cfg.whatsappGeral;
    if (!numero) return;
    a.href = waLink(numero, "Olá! Gostaria de agendar um atendimento na clínica de " + c.nome + ".");
  });

  document.querySelectorAll("a[data-wa-general]").forEach(function (a) {
    if (cfg.whatsappGeral) a.href = waLink(cfg.whatsappGeral, a.classList.contains("fab") ? "Olá! Vim pelo site do CONecta Saúde." : "");
  });

  /* ---------- Menu mobile ---------- */
  var btn = document.querySelector(".menu-btn");
  var nav = document.getElementById("menu");
  var mq = window.matchMedia("(max-width: 900px)");

  function setMenu(open) {
    body.classList.toggle("menu-open", open);
    btn.setAttribute("aria-expanded", String(open));
    btn.setAttribute("aria-label", open ? "Fechar menu" : "Abrir menu");
  }

  btn.addEventListener("click", function () {
    setMenu(!body.classList.contains("menu-open"));
  });
  nav.addEventListener("click", function (e) {
    if (e.target.closest("a")) setMenu(false);
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && body.classList.contains("menu-open")) {
      setMenu(false);
      btn.focus();
    }
  });
  (mq.addEventListener ? mq.addEventListener.bind(mq, "change") : mq.addListener.bind(mq))(function (e) {
    if (!e.matches) setMenu(false);
  });

  /* ---------- Item de menu ativo conforme a rolagem ---------- */
  var links = Array.prototype.slice.call(nav.querySelectorAll("a[href^='#']"));
  var map = {};
  links.forEach(function (a) { map[a.getAttribute("href").slice(1)] = a; });

  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        links.forEach(function (a) { a.classList.remove("is-active"); a.removeAttribute("aria-current"); });
        var a = map[en.target.id];
        if (a) { a.classList.add("is-active"); a.setAttribute("aria-current", "true"); }
      });
    }, { rootMargin: "-45% 0px -50% 0px" });

    Object.keys(map).forEach(function (id) {
      var s = document.getElementById(id);
      if (s && id !== "contato") io.observe(s);
    });
  }
})();
