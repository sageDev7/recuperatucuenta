"""Cierre SEO de la landing de Recupera Tu Cuenta. CORRER RECIÉN CUANDO EL DOMINIO ESTÉ CONFIRMADO.

Uso:  python _scripts/cierre_seo.py https://recuperatucuenta.com.ar

Hace (idempotente):
  - og:image / twitter:image absolutos, og:url y canonical en index y privacidad
  - url / logo / image en el JSON-LD del index
  - 404 con rutas absolutas (se sirve en cualquier URL inexistente)
  - links internos limpios (/privacidad, /#contacto)
  - sitemap.xml, robots.txt y .htaccess (https sin www, URLs sin .html, 404, compresión, caché)
"""
import json, os, re, sys
from datetime import date

if len(sys.argv) < 2 or not sys.argv[1].startswith("https://"):
    sys.exit("Pasá el dominio confirmado, ej.: python _scripts/cierre_seo.py https://recuperatucuenta.com.ar")
DOM = sys.argv[1].rstrip("/")
HOST = re.sub(r"^https://(www\.)?", "", DOM)
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(D)
PAGES = {"index.html": ("/", "1.0"), "privacidad.html": ("/privacidad", "0.3")}

def set_meta(s, attr, key, value):
    tag = f'<meta {attr}="{key}" content="{value}">'
    pat = re.compile(r'<meta %s="%s" content="[^"]*">' % (attr, re.escape(key)))
    return pat.sub(lambda m: tag, s, count=1) if pat.search(s) else s.replace("</head>", tag + "\n</head>", 1)

def set_canonical(s, url):
    tag = f'<link rel="canonical" href="{url}">'
    pat = re.compile(r'<link rel="canonical" href="[^"]*">')
    return pat.sub(lambda m: tag, s, count=1) if pat.search(s) else s.replace("</head>", tag + "\n</head>", 1)

def clean(s):
    s = s.replace('href="./index.html#', 'href="/#').replace('href="./index.html"', 'href="/"')
    return re.sub(r'href="\./([a-z0-9-]+)\.html"', r'href="/\1"', s)

for f, (path, _) in PAGES.items():
    s = open(f, encoding="utf8").read()
    s = clean(s)
    OG = "https://i.imgur.com/cQdFTBM.jpeg"   # badge original subido por Axel
    s = set_meta(s, "property", "og:image", OG)
    s = set_meta(s, "name", "twitter:image", OG)
    s = set_meta(s, "property", "og:url", DOM + path)
    s = set_canonical(s, DOM + path)
    if f == "index.html":
        m = re.search(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', s, re.S)
        data = json.loads(m.group(1))
        data.update({"@id": DOM + "/#estudio", "url": DOM + "/", "image": "https://i.imgur.com/cQdFTBM.jpeg", "logo": DOM + "/favicon.png"})
        s = s.replace(m.group(0), '<script type="application/ld+json">\n' + json.dumps(data, ensure_ascii=False, indent=2) + "\n</script>")
    open(f, "w", encoding="utf8", newline="\n").write(s); print("ok", f)

s = open("404.html", encoding="utf8").read()
s = clean(s)
s = re.sub(r'(href|src)="\./', r'\1="/', s)
open("404.html", "w", encoding="utf8", newline="\n").write(s); print("ok 404.html")

hoy = date.today().isoformat()
urls = "\n".join(f"  <url><loc>{DOM}{p}</loc><lastmod>{hoy}</lastmod><priority>{pr}</priority></url>" for p, pr in PAGES.values())
open("sitemap.xml", "w", encoding="utf8").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')
open("robots.txt", "w", encoding="utf8").write(f"User-agent: *\nAllow: /\nDisallow: /_scripts/\n\nSitemap: {DOM}/sitemap.xml\n")
host_re = HOST.replace(".", r"\.")
open(".htaccess", "w", encoding="utf8", newline="\n").write(f'''# Recupera Tu Cuenta — {HOST}
Options -Indexes -MultiViews
DirectoryIndex index.html
ErrorDocument 404 /404.html

<IfModule mod_rewrite.c>
RewriteEngine On
# https y sin www
RewriteCond %{{HTTPS}} off [OR]
RewriteCond %{{HTTP_HOST}} ^www\\. [NC]
RewriteRule ^ https://{HOST}%{{REQUEST_URI}} [L,R=301]
# /index.html -> /
RewriteCond %{{THE_REQUEST}} \\s/+index(\\.html)?[\\s?#] [NC]
RewriteRule ^ / [L,R=301]
# /pagina.html -> /pagina
RewriteCond %{{THE_REQUEST}} \\s/+([^\\s?]+?)\\.html[\\s?] [NC]
RewriteRule ^ /%1 [L,R=301]
# /pagina sirve pagina.html
RewriteCond %{{REQUEST_FILENAME}} !-d
RewriteCond %{{REQUEST_FILENAME}}.html -f
RewriteRule ^(.+?)/?$ $1.html [L]
</IfModule>

RedirectMatch 404 ^/_scripts(/.*)?$

<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css application/javascript text/javascript image/svg+xml text/xml application/xml text/plain
</IfModule>
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType text/html "access plus 0 seconds"
  ExpiresByType text/css "access plus 1 month"
  ExpiresByType application/javascript "access plus 1 month"
  ExpiresByType image/png "access plus 6 months"
  ExpiresByType image/jpeg "access plus 6 months"
</IfModule>
<IfModule mod_headers.c>
  Header always set X-Content-Type-Options "nosniff"
  Header always set X-Frame-Options "SAMEORIGIN"
  Header always set Referrer-Policy "strict-origin-when-cross-origin"
</IfModule>
''')
print("ok sitemap.xml, robots.txt, .htaccess — con links limpios, abrir por doble clic deja de navegar: probar en el hosting")
