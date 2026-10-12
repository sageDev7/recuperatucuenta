"""Landing de Recupera Tu Cuenta: genera privacidad.html y 404.html reutilizando el header, el menú y el
footer del index (los links #ancla pasan a ./index.html#ancla), y agrega a index.html las meta de
favicon/OG. Idempotente: se puede volver a correr si cambia el index."""
import os, re
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(D)
idx = open("index.html", encoding="utf8").read()

# ---------- meta favicon / OG en el index (una sola vez)
if "og:image" not in idx:
    t = re.search(r"<title>(.*?)</title>", idx).group(1)
    d = re.search(r'<meta name="description" content="(.*?)">', idx).group(1)
    meta = f'''<link rel="icon" type="image/png" href="./favicon.png">
<link rel="apple-touch-icon" href="./favicon.png">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_AR">
<meta property="og:site_name" content="Recupera Tu Cuenta">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:image" content="./og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="1200">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">'''
    idx = idx.replace('<meta name="theme-color" content="#070B16">', '<meta name="theme-color" content="#070B16">\n' + meta, 1)
if "./privacidad.html" not in idx:
    idx = idx.replace('    <p>Desarrollado por', '    <p><a href="./privacidad.html">Política de privacidad</a></p>\n    <p>Desarrollado por', 1)
open("index.html", "w", encoding="utf8", newline="\n").write(idx)

# ---------- piezas compartidas tomadas del index
head_tpl = idx[:idx.index("<title>")]
links_head = idx[idx.index('<link rel="preconnect"'):idx.index("<script type=\"application/ld+json\">")]
top = idx[idx.index("<!-- ============ HEADER ============ -->"):idx.index("<main>")]
foot = idx[idx.index("<!-- ============ FOOTER ============ -->"):idx.index('<div class="modal"')]
def interna(s):
    s = re.sub(r'href="#(?!")', 'href="./index.html#', s)
    return s.replace('href="./index.html#inicio"', 'href="./index.html"')
top, foot = interna(top), interna(foot)

def page(name, title, desc, body, robots=""):
    rb = f'<meta name="robots" content="{robots}">\n' if robots else ""
    html = (head_tpl + f"<title>{title}</title>\n<meta name=\"description\" content=\"{desc}\">\n{rb}"
            '<meta name="theme-color" content="#070B16">\n<link rel="icon" type="image/png" href="./favicon.png">\n'
            + links_head + "</head>\n<body>\n\n" + top + "<main>\n" + body + "\n</main>\n\n" + foot
            + '<script src="./main.js"></script>\n</body>\n</html>\n')
    open(name, "w", encoding="utf8", newline="\n").write(html); print("ok", name)

page("privacidad.html", "Política de privacidad | Recupera Tu Cuenta",
     "Cómo se tratan los datos personales recibidos a través de este sitio, conforme a la Ley 25.326.", '''
<section class="legal-hero">
  <div class="wrap">
    <p class="eyebrow">Información legal</p>
    <h1 class="h2">Política <em>de privacidad.</em></h1>
  </div>
</section>
<section class="legal">
  <div class="wrap legal-in">
    <p class="legal-date">Última actualización: octubre de 2026</p>
    <h2>1. Responsable</h2>
    <p>El responsable del tratamiento es el Dr. Nicolás Avots Sugimoto, abogado matriculado en el CPACF, a cargo de Recupera Tu Cuenta. Contacto: recuperatucuenta.ar@gmail.com · +54 9 11 2605-4556.</p>
    <h2>2. Qué datos se recopilan</h2>
    <p>Solo los que enviás voluntariamente: nombre, WhatsApp, email, la red y el usuario del perfil afectado y el mensaje que escribís en el formulario, o los datos que compartís al escribir por WhatsApp. El sitio no usa cookies de seguimiento ni herramientas de publicidad.</p>
    <h2>3. Para qué se usan</h2>
    <p>Para analizar tu caso, responder tu consulta y, si decidís contratar el servicio, llevar adelante la gestión. No se usan para otros fines ni se ceden a terceros con fines comerciales.</p>
    <h2>4. Secreto profesional</h2>
    <p>La información que compartís está protegida por el secreto profesional que rige el ejercicio de la abogacía.</p>
    <p>Nunca te vamos a pedir tu contraseña por chat ni por el formulario.</p>
    <h2>5. Servicios de terceros</h2>
    <p>Para funcionar, el sitio usa servicios externos que pueden procesar datos técnicos (como la dirección IP):</p>
    <ul>
      <li><b>FormSubmit</b>, que envía al email del estudio los datos del formulario.</li>
      <li><b>WhatsApp</b> (Meta Platforms), si elegís escribir por ese medio.</li>
      <li><b>Google Fonts</b> y <b>jsDelivr</b>, que sirven las tipografías y los íconos del sitio.</li>
    </ul>
    <p>Cada uno se rige por su propia política de privacidad.</p>
    <h2>6. Conservación y seguridad</h2>
    <p>Los datos se conservan el tiempo necesario para atender la consulta y cumplir obligaciones legales y profesionales, con medidas razonables de protección.</p>
    <h2>7. Tus derechos</h2>
    <p>Conforme a la Ley 25.326, podés solicitar en forma gratuita el acceso, la rectificación, la actualización o la supresión de tus datos, por los medios indicados en el punto 1. La Agencia de Acceso a la Información Pública, órgano de control de la Ley 25.326, atiende las denuncias y los reclamos por incumplimientos de las normas sobre protección de datos personales.</p>
    <h2>8. Cambios</h2>
    <p>Esta política puede actualizarse. La versión vigente es siempre la publicada en esta página.</p>
  </div>
</section>''')

page("404.html", "Página no encontrada | Recupera Tu Cuenta", "La página que buscás no existe o cambió de dirección.", '''
<section class="nf">
  <div class="wrap">
    <span class="nf-num" aria-hidden="true">404</span>
    <h1 class="h2">Esta página <em>no existe.</em></h1>
    <p class="lead">Puede que haya cambiado de dirección. Volvé al inicio o escribinos y te ayudamos.</p>
    <div class="hero-ctas">
      <a class="btn btn-gold" href="./index.html">Volver al inicio</a>
      <a class="btn btn-line js-wa" href="#" data-msg="Hola, me inhabilitaron un perfil y quisiera hacer una consulta.">Consultar por WhatsApp</a>
    </div>
  </div>
</section>''', robots="noindex")

# ---------- CSS de las páginas legales (una sola vez)
c = open("styles.css", encoding="utf8").read()
if ".legal-hero" not in c:
    css = '''
/* ---------- privacidad y 404 ---------- */
.legal-hero{padding:calc(var(--hdr) + 5rem) 0 3.6rem;background:linear-gradient(125deg,var(--ink) 0%,var(--navy-d) 50%,var(--navy) 100%);border-bottom:1px solid var(--line-l)}
.legal{padding:80px 0 120px;background:var(--navy-d)}
.legal-in>*{max-width:46rem}
.legal-date{margin-bottom:2.2rem;font-size:.85rem;font-weight:600;color:var(--gold-l)}
.legal h2{margin:2.4rem 0 .8rem;font-size:1.45rem}
.legal p,.legal li{color:var(--muted)}
.legal p+p{margin-top:.8rem}
.legal ul{display:grid;gap:.5rem;margin:.8rem 0}
.legal li{position:relative;padding-left:1.3rem}
.legal li::before{content:"";position:absolute;left:0;top:.8em;width:.55rem;height:1px;background:var(--gold)}
.legal b{color:var(--white)}
.nf{min-height:100vh;min-height:100svh;display:flex;align-items:center;padding:calc(var(--hdr) + 3rem) 0 4rem;background:linear-gradient(125deg,var(--ink) 0%,var(--navy-d) 45%,var(--navy) 100%)}
.nf-num{display:block;margin-bottom:1rem;font-family:var(--head);font-size:clamp(6rem,14vw,11rem);line-height:.85;color:var(--gold)}
.nf .lead{margin-top:1.2rem;max-width:34rem}
@media (max-width:768px){
  .legal-hero{padding:calc(var(--hdr) + 3rem) 0 2.6rem;text-align:center}
  .legal{padding:56px 0 84px}
  .nf{text-align:center}
  .nf .lead{margin-left:auto;margin-right:auto}
  .nf .hero-ctas{flex-direction:column;align-items:center}
}
'''
    open("styles.css", "a", encoding="utf8").write(css); print("css ok")
