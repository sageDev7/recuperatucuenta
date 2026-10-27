(function () {
  "use strict";
  var body = document.body;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var WA_NUMBER = "5491126054556";

  /* ---------- header ---------- */
  var hdr = document.getElementById("hdr");
  function onScroll() { hdr.classList.toggle("sc", window.scrollY > 40); }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });


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

  /* ---------- formulario: arma un mensaje natural y lo abre en WhatsApp ---------- */
  var form = document.getElementById("contactForm");
  if (form) {
    var val = function (n) { var el = form.elements[n]; return el ? el.value.trim() : ""; };
    var valid = function (input) {
      var ok = input.value.trim() !== "";
      input.closest(".field").classList.toggle("err", !ok);
      return ok;
    };
    var buildMsg = function () {
      var user = val("usuario"), red = val("red"), emp = val("empresa"), dos = red === "Instagram y Facebook";
      if (red !== "Facebook" && user && user.charAt(0) !== "@") user = "@" + user;
      var m = "Hola, me llamo " + val("nombre") + ". Me inhabilitaron " + (dos ? "mis cuentas de Instagram y Facebook" : "mi cuenta de " + red) + " (" + user + ")";
      if (emp) m += ", " + (dos ? "que son" : "que es") + " de mi empresa, " + emp;
      m += ". " + (dos ? "Tienen" : "Tiene") + " " + val("seguidores") + " seguidores. ¿Me podrían ayudar a " + (dos ? "recuperarlas" : "recuperarla") + "?";
      return m + " Mi número es " + val("whatsapp") + ".";
    };
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var ok = true;
      form.querySelectorAll("[required]").forEach(function (i) { if (!valid(i)) ok = false; });
      if (!ok) { var f = form.querySelector(".field.err input,.field.err select"); if (f) f.focus(); return; }
      if (window.fbq) fbq("track", "Lead");
      var url = "https://wa.me/" + WA_NUMBER + "?text=" + encodeURIComponent(buildMsg());
      var w = window.open(url, "_blank");
      if (!w) window.location.href = url;
    });
    form.querySelectorAll("[required]").forEach(function (i) {
      i.addEventListener("input", function () { if (i.closest(".field").classList.contains("err")) valid(i); });
      i.addEventListener("change", function () { if (i.closest(".field").classList.contains("err")) valid(i); });
    });
  }

  document.getElementById("yr").textContent = new Date().getFullYear();
})();
