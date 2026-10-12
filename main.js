(function () {
  "use strict";
  var body = document.body;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- WhatsApp: un solo número para todos los botones ---------- */
  var WA_NUMBER = "5491126054556";
  document.querySelectorAll(".js-wa").forEach(function (a) {
    var msg = a.getAttribute("data-msg") || "Hola, me inhabilitaron una cuenta y quisiera hacer una consulta.";
    a.href = "https://wa.me/" + WA_NUMBER + "?text=" + encodeURIComponent(msg);
    a.target = "_blank";
    a.rel = "noopener";
  });

  /* ---------- header ---------- */
  var hdr = document.getElementById("hdr");
  function onScroll() { hdr.classList.toggle("sc", window.scrollY > 40); }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  /* ---------- menú mobile (la hamburguesa se transforma en cruz) ---------- */
  var burger = document.getElementById("burger");
  function setNav(open) {
    body.classList.toggle("nav-open", open);
    burger.setAttribute("aria-expanded", open ? "true" : "false");
    burger.setAttribute("aria-label", open ? "Cerrar menú" : "Abrir menú");
  }
  burger.addEventListener("click", function () { setNav(!body.classList.contains("nav-open")); });
  document.getElementById("mnavOv").addEventListener("click", function () { setNav(false); });
  document.querySelectorAll(".mnav a").forEach(function (a) { a.addEventListener("click", function () { setNav(false); }); });

  /* ---------- título: entra palabra por palabra (el &nbsp; mantiene palabras juntas) ---------- */
  var wordIdx = 0;
  function splitWords(node) {
    Array.prototype.slice.call(node.childNodes).forEach(function (n) {
      if (n.nodeType === 3) {
        var frag = document.createDocumentFragment();
        n.textContent.split(/([ \t\n\r]+)/).forEach(function (part) {
          if (!part) return;
          if (/^[ \t\n\r]+$/.test(part)) { frag.appendChild(document.createTextNode(" ")); return; }
          var w = document.createElement("span");
          w.className = "w";
          w.textContent = part;
          w.style.animationDelay = (0.2 + wordIdx++ * 0.08) + "s";
          frag.appendChild(w);
        });
        node.replaceChild(frag, n);
      } else if (n.nodeType === 1 && n.tagName !== "BR") {
        splitWords(n);
      }
    });
  }
  if (!reduce) document.querySelectorAll(".split-words").forEach(splitWords);

  /* ---------- contadores ---------- */
  function runCount(el) {
    var to = parseFloat(el.getAttribute("data-to")), pre = el.getAttribute("data-prefix") || "";
    var dur = 1800, t0 = null;
    function step(t) {
      if (!t0) t0 = t;
      var k = Math.min((t - t0) / dur, 1), e = 1 - Math.pow(1 - k, 4);
      el.textContent = pre + Math.round(to * e);
      if (k < 1) requestAnimationFrame(step);
    }
    el.textContent = pre + "0";
    requestAnimationFrame(step);
  }
  if (!reduce && "IntersectionObserver" in window) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { runCount(en.target); cio.unobserve(en.target); } });
    }, { threshold: 0.6 });
    document.querySelectorAll(".count").forEach(function (el) { cio.observe(el); });
  }

  /* ---------- preguntas: acordeón con apertura suave (una abierta a la vez por lista) ---------- */
  function animateTo(a, from, to, done) {
    a.style.height = from + "px";
    requestAnimationFrame(function () {
      a.style.transition = "height .45s cubic-bezier(.2,.7,.2,1)";
      a.style.height = to + "px";
    });
    a.addEventListener("transitionend", function te() { a.removeEventListener("transitionend", te); a.style.cssText = ""; if (done) done(); });
  }
  function closeFaq(d) {
    if (reduce) { d.open = false; return; }
    var a = d.querySelector(".faq-a");
    animateTo(a, a.scrollHeight, 0, function () { d.open = false; });
  }
  document.querySelectorAll(".faq-list details").forEach(function (d) {
    d.querySelector("summary").addEventListener("click", function (e) {
      e.preventDefault();
      if (d.open) { closeFaq(d); return; }
      d.closest(".faq-list").querySelectorAll("details").forEach(function (o) { if (o !== d && o.open) closeFaq(o); });
      d.open = true;
      if (reduce) return;
      var a = d.querySelector(".faq-a");
      animateTo(a, 0, a.scrollHeight);
    });
  });

  /* ---------- hero: la cuenta pasa de inhabilitada a gestión legal y a recuperada ---------- */
  var phone = document.getElementById("phone");
  if (phone) {
    var steps = document.querySelectorAll(".ph-steps li"), step = 0;
    var show = function (n) {
      phone.setAttribute("data-step", n);
      steps.forEach(function (li, i) { li.classList.toggle("on", i === n); });
    };
    if (reduce) { show(2); }
    else { setInterval(function () { step = (step + 1) % 3; show(step); }, 2000); }
  }

  /* ---------- reveals ---------- */
  var items = document.querySelectorAll(".reveal, .pasos");
  if (reduce || !("IntersectionObserver" in window)) {
    items.forEach(function (el) { el.classList.add("in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    items.forEach(function (el) { io.observe(el); });
  }

  /* ---------- parallax del hero ---------- */
  var heroBg = null, ticking = false;
  if (heroBg && !reduce) {
    window.addEventListener("scroll", function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        ticking = false;
        if (window.scrollY < window.innerHeight * 1.2) heroBg.style.transform = "translate3d(0," + (window.scrollY * 0.25) + "px,0)";
      });
    }, { passive: true });
  }

  /* ---------- WhatsApp flotante: se oculta en el hero, el contacto y el footer ---------- */
  var fab = document.getElementById("waFloat");
  if (fab && "IntersectionObserver" in window) {
    var hidden = new Set();
    var fio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) hidden.add(en.target); else hidden.delete(en.target); });
      fab.classList.toggle("hide", hidden.size > 0);
    });
    document.querySelectorAll(".hero, #contacto, #ftr").forEach(function (el) { fio.observe(el); });
  }

  /* ---------- formulario (FormSubmit + modal) ---------- */
  var form = document.getElementById("contactForm"), btn = document.getElementById("formSubmitBtn");
  var iframe = document.getElementById("formsubmit-iframe"), modal = document.getElementById("okModal"), sending = false;
  if (form) {
    var valid = function (input) {
      var v = input.value.trim();
      var ok = v !== "" && (input.type !== "email" || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v));
      input.closest(".field").classList.toggle("err", !ok);
      return ok;
    };
    form.addEventListener("submit", function (e) {
      var ok = true;
      form.querySelectorAll("[required]").forEach(function (i) { if (!valid(i)) ok = false; });
      if (!ok) { e.preventDefault(); var f = form.querySelector(".field.err input,.field.err select,.field.err textarea"); if (f) f.focus(); return; }
      sending = true; btn.disabled = true; btn.textContent = "Enviando...";
    });
    form.querySelectorAll("[required]").forEach(function (i) {
      i.addEventListener("input", function () { if (i.closest(".field").classList.contains("err")) valid(i); });
      i.addEventListener("change", function () { if (i.closest(".field").classList.contains("err")) valid(i); });
    });
    iframe.addEventListener("load", function () {
      if (!sending) return;
      sending = false; form.reset(); btn.disabled = false; btn.textContent = "Enviar consulta";
      modal.classList.add("show");
    });
    modal.addEventListener("click", function (e) { if (e.target === modal || e.target.hasAttribute("data-close")) modal.classList.remove("show"); });
  }
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") { setNav(false); if (modal) modal.classList.remove("show"); }
  });

  document.getElementById("yr").textContent = new Date().getFullYear();
})();
