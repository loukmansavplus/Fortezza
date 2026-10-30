"""Génère le site statique Fortezza dans ./public

Usage :  python build.py
Tout ce qui est à confirmer (téléphone, adresse, forme juridique…) est dans CONFIG.
"""
import shutil
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).parent
PUB = ROOT / "public"
LOGOS = ROOT.parent / "images" / "logos"

import sys
HOST = sys.argv[1] if len(sys.argv) > 1 else "hostinger"   # "hostinger" (PHP) ou "netlify"


def form_attrs(name):
    if HOST == "netlify":
        return f'name="{name}" action="/merci" method="post" data-netlify="true" netlify-honeypot="website"'
    return f'name="{name}" action="/send.php" method="post"'


def form_hidden(name):
    return f'<input type="hidden" name="form-name" value="{name}"><input type="hidden" name="form" value="{name}">' if HOST == "netlify" else f'<input type="hidden" name="form" value="{name}">'


CONFIG = {
    "domain": "https://fortezza.bj",
    "legal": "Fortezza SAS",              # à trancher : SAS ou SARL
    "phone": "+229 00 00 00 00",          # À FOURNIR
    "wa": "22900000000",                  # À FOURNIR (format international sans +)
    "email": "contact@fortezza.bj",
    "email_devis": "devis@fortezza.bj",
    "address": "Cotonou, Bénin",          # À COMPLÉTER (rue / quartier)
    "hours": [("Lundi – Vendredi", "08h – 18h"), ("Samedi", "09h – 13h")],
    "year": 2026,
}
C = CONFIG

# ------------------------------------------------------------------ données
ICONS = {
    "infra": '<path d="M4 6h16v5H4zM4 13h16v5H4z"/><path d="M7.5 8.5h.01M7.5 15.5h.01M11 8.5h6M11 15.5h6"/>',
    "mat": '<rect x="3" y="4" width="18" height="12" rx="1.5"/><path d="M8 20h8M12 16v4"/>',
    "maint": '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.6 2.6-2.4-.6-.6-2.4z"/>',
    "web": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.8 3 2.8 15 0 18M12 3c-2.8 3-2.8 15 0 18"/>',
    "form": '<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11.5V16c0 1.5 3 3 6 3s6-1.5 6-3v-4.5M22 9v6"/>',
    "user": '<circle cx="12" cy="8" r="3.5"/><path d="M5 20c0-4 3-6.5 7-6.5s7 2.5 7 6.5"/>',
    "bolt": '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
    "shield": '<path d="M12 2l8 3v6c0 5-3.4 8.7-8 11-4.6-2.3-8-6-8-11V5z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
    "chat": '<path d="M4 5h16v11H9l-5 4z"/><path d="M8 9.5h8M8 12.5h5"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    "pin": '<path d="M12 21s7-6.2 7-11.5A7 7 0 0 0 5 9.5C5 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
}


def icon(name, cls="ic"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg>'


POLES = [
    dict(slug="infrastructures", icon="infra", img="infra",
         name="Infrastructures & Systèmes d'Information",
         pagetitle="Informatique & Systèmes d'Information",
         short="Infrastructures & SI",
         accroche="Votre système nerveux numérique, on s'en occupe.",
         intro="Audit, conception, intégration et sécurisation de vos réseaux, serveurs et systèmes informatiques. Nous construisons une base solide pour votre croissance.",
         items=["Audit et conseil informatique", "Étude et conception d'architecture réseau",
                "Intégration de systèmes et infrastructures", "Infogérance et sécurisation de vos données"],
         seo="Audit, réseau, serveurs et infogérance à Cotonou : Fortezza conçoit et sécurise votre infrastructure informatique au Bénin."),
    dict(slug="materiel", icon="mat", img="mat",
         name="Fourniture de Matériels",
         pagetitle="Fourniture de Matériels & Équipements",
         short="Fourniture de matériels",
         accroche="Du matériel fiable, au bon prix.",
         intro="Ordinateurs, serveurs, imprimantes, onduleurs, accessoires réseau. Matériel d'origine, garanti, avec service de livraison et d'installation au Bénin.",
         items=["Vente de PC, serveurs, imprimantes, onduleurs, réseau",
                "Équipements et consommables informatiques & électroniques",
                "Solutions complètes pour bureaux et entreprises",
                "Importation et distribution de marques certifiées"],
         seo="Vente de matériel informatique au Bénin : PC, serveurs, imprimantes, onduleurs et réseau garantis, livrés et installés à Cotonou."),
    dict(slug="maintenance", icon="maint", img="maint",
         name="Maintenance & Support Technique",
         pagetitle="Maintenance & Assistance Technique",
         short="Maintenance & support",
         accroche="On ne vous laisse jamais en panne.",
         intro="Votre activité ne doit jamais s'arrêter. Maintenance préventive, dépannage curatif sur site et à distance, contrat de support et infogérance.",
         items=["Maintenance préventive et corrective", "Dépannage rapide sur site et à distance",
                "Support utilisateur et Helpdesk", "Contrat de maintenance annuel (SAV garanti)"],
         seo="Maintenance informatique à Cotonou : dépannage sur site et à distance, support helpdesk et contrat annuel avec SAV garanti."),
    dict(slug="developpement-web-cloud", icon="web", img="web",
         name="Développement Web & Cloud",
         pagetitle="Services Numériques & Développement",
         short="Développement Web & Cloud",
         accroche="Votre présence digitale, clé en main.",
         intro="Sites vitrines, applications web et mobiles, hébergement professionnel, messagerie pro, solutions Cloud et cybersécurité.",
         items=["Création de sites web & applications mobiles", "Hébergement web, emails pro & Cloud",
                "Cybersécurité et protection des données", "Solutions de gestion sur mesure (ERP, CRM)"],
         seo="Création de site web au Bénin, hébergement, emails pro, Cloud, cybersécurité et solutions ERP/CRM sur mesure avec Fortezza."),
    dict(slug="formation", icon="form", img="form",
         name="Formation Professionnelle",
         pagetitle="Formation & Renforcement de Capacités",
         short="Formation professionnelle",
         accroche="La technologie ne vaut que si vos équipes la maîtrisent.",
         intro="Formez vos équipes à la bureautique avancée, à la cybersécurité, aux réseaux et aux outils numériques pour gagner en autonomie.",
         items=["Formation bureautique, réseau, cybersécurité", "Ateliers pratiques pour entreprises",
                "Séminaires sur les nouvelles technologies", "Certificats de formation Fortezza"],
         seo="Formation cybersécurité, réseau et bureautique à Cotonou : ateliers pratiques pour entreprises et certificats Fortezza."),
]

WHY = [
    ("user", "Expertise complète", "Un seul interlocuteur pour tout votre IT."),
    ("bolt", "Réactivité", "Intervention rapide à Cotonou et partout au Bénin."),
    ("shield", "Qualité & Garantie", "Matériels certifiés et services garantis."),
    ("chat", "Accompagnement", "On vous conseille, on ne vous vend pas juste."),
]

# ------------------------------------------------------------------ images
IMG_SIZES = (1600, 800)


def build_images():
    out = PUB / "assets" / "img"
    for src in sorted((ROOT / "src_img").glob("*.jpg")):
        im = Image.open(src).convert("RGB")
        for w in IMG_SIZES:
            t = im.copy()
            t.thumbnail((w, w * 2))
            t.save(out / f"{src.stem}-{w}.webp", "WEBP", quality=74 if w > 800 else 72, method=6)
    # logos : fond transparent conservé, 3 variantes
    base = Image.open(LOGOS / "LOGO FULL FORTEZZA.png").convert("RGBA").crop((0, 0, 1016, 270))
    bb = base.getbbox()
    base = base.crop(bb)
    base.save(out / "logo.png", optimize=True)
    white = Image.new("RGBA", base.size)
    pb, pw = base.load(), white.load()
    for y in range(base.height):
        for x in range(base.width):
            r, g, b, a = pb[x, y]
            if a > 8:
                pw[x, y] = (0, 198, 215, a) if g > r + 60 else (255, 255, 255, a)
    white.save(out / "logo-white.png", optimize=True)
    icon_src = Image.open(LOGOS / "LOGOTYPE FORTEZZA.png").convert("RGBA")
    for s, n in ((32, "favicon-32.png"), (180, "apple-touch-icon.png"), (512, "icon-512.png")):
        t = icon_src.copy()
        t.thumbnail((s, s))
        t.save(out / n, optimize=True)
    t = icon_src.copy(); t.thumbnail((48, 48)); t.save(PUB / "favicon.ico", sizes=[(32, 32)])


def pic(name, alt, cls="", sizes="100vw", eager=False, w=1600, h=1066):
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<img class="{cls}" src="/assets/img/{name}-800.webp" '
            f'srcset="/assets/img/{name}-800.webp 800w, /assets/img/{name}-1600.webp 1600w" '
            f'sizes="{sizes}" width="{w}" height="{h}" alt="{alt}" {load}>')


# ------------------------------------------------------------------ gabarit
def nav_html(active):
    def a(href, label, key):
        cur = ' aria-current="page"' if active == key else ""
        return f'<a href="{href}"{cur}>{label}</a>'
    sub = "".join(f'<a href="/services/{p["slug"]}">{icon(p["icon"])}<span>{p["short"]}</span></a>' for p in POLES)
    svc_cur = ' aria-current="page"' if active == "services" else ""
    return f'''<nav id="nav" aria-label="Navigation principale">
      {a("/", "Accueil", "home")}
      {a("/a-propos", "À propos", "about")}
      <div class="has-sub">
        <a href="/services"{svc_cur}>Services <svg class="chev" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></a>
        <div class="sub">{sub}</div>
      </div>
      {a("/contact", "Contact", "contact")}
      <a class="btn btn-primary nav-cta" href="/devis">Demander un devis</a>
    </nav>'''


def wa_link(msg="Bonjour Fortezza, je souhaite un devis pour…"):
    from urllib.parse import quote
    return f'https://wa.me/{C["wa"]}?text={quote(msg)}'


def head(title, desc, path, active, og="cover", extra=""):
    url = C["domain"] + path
    return f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#03214A">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_BJ">
<meta property="og:site_name" content="Fortezza">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{C["domain"]}/assets/img/{og}-1600.webp">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
<script>document.documentElement.classList.add("js");setTimeout(function(){{if(!window.gsap||!window.ScrollTrigger)document.documentElement.classList.add("no-gsap")}},3500)</script>
<link rel="stylesheet" href="/assets/css/style.css">
{extra}
</head>'''


def header(active):
    return f'''<a class="skip" href="#main">Aller au contenu</a>
<header class="site-header" id="top">
  <div class="wrap bar">
    <a class="brand" href="/" aria-label="Fortezza – Accueil"><img src="/assets/img/logo.png" alt="Fortezza" width="829" height="74"></a>
    <button class="burger" aria-label="Menu" aria-expanded="false" aria-controls="nav"><span></span><span></span></button>
    {nav_html(active)}
  </div>
</header>'''


def cta_block(service=None):
    link = "/devis" + (f"?service={service}" if service else "")
    return f'''<section class="cta-final">
  <div class="wrap cta-in">
    <div class="txtblock">
      <p class="eyebrow">Parlons de votre projet</p>
      <h2>Prêt à sécuriser et <em>moderniser</em> votre entreprise&nbsp;?</h2>
      <p>Ne laissez pas un problème informatique ralentir votre business. Parlons de votre projet.</p>
    </div>
    <div class="cta-btns reveal">
      <a class="btn btn-primary btn-lg" href="{link}">{"Demander un devis pour ce service" if service else "Demander un devis"}{icon("arrow","ic-s")}</a>
      <a class="btn btn-ghost btn-lg" href="/contact">Contactez-nous maintenant</a>
    </div>
  </div>
</section>'''


def why_block():
    cards = "".join(f'<div class="why-card reveal">{icon(i)}<h3>{t}</h3><p>{d}</p></div>' for i, t, d in WHY)
    return f'''<section class="section why">
  <div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">Pourquoi nous choisir&nbsp;?</p><h2>Fortezza, la différence.</h2></div>
    <div class="why-grid">{cards}</div>
  </div>
</section>'''


def footer():
    svc = "".join(f'<li><a href="/services/{p["slug"]}">{p["name"]}</a></li>' for p in POLES)
    hrs = "".join(f"<li><span>{d}</span> {h}</li>" for d, h in C["hours"])
    schema = f'''<script type="application/ld+json">{{
"@context":"https://schema.org","@type":"LocalBusiness","name":"Fortezza","url":"{C["domain"]}",
"description":"Matériel informatique, maintenance, réseau, développement web et formation à Cotonou, Bénin.",
"image":"{C["domain"]}/assets/img/cover-1600.webp","telephone":"{C["phone"]}","email":"{C["email"]}",
"address":{{"@type":"PostalAddress","addressLocality":"Cotonou","addressCountry":"BJ"}},
"openingHoursSpecification":[{{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"08:00","closes":"18:00"}},{{"@type":"OpeningHoursSpecification","dayOfWeek":"Saturday","opens":"09:00","closes":"13:00"}}]
}}</script>'''
    return f'''<footer class="site-footer">
  <div class="wrap foot-grid">
    <div class="foot-brand">
      <img src="/assets/img/logo-white.png" alt="Fortezza" width="829" height="74" loading="lazy">
      <p class="foot-slogan">L'Excellence Technologique.</p>
      <p class="muted">Un seul partenaire pour tout votre IT, de l'idée à la maintenance.</p>
    </div>
    <div><h4>Services</h4><ul>{svc}</ul></div>
    <div><h4>Contact</h4><ul>
      <li>{icon("pin","ic-s")} {C["address"]}</li>
      <li>{icon("phone","ic-s")} <a href="tel:{C["phone"].replace(" ","")}">{C["phone"]}</a></li>
      <li>{icon("mail","ic-s")} <a href="mailto:{C["email"]}">{C["email"]}</a></li>
      <li>{icon("chat","ic-s")} <a href="{wa_link()}" rel="noopener" target="_blank">WhatsApp</a></li>
    </ul></div>
    <div><h4>Horaires</h4><ul class="hours">{hrs}</ul>
      <a class="btn btn-primary btn-sm" href="/devis">Demander un devis</a></div>
  </div>
  <div class="wrap foot-bottom">
    <span>© {C["year"]} {C["legal"]}</span>
    <span><a href="/mentions-legales">Mentions légales</a></span>
  </div>
</footer>
<a class="wa-float" href="{wa_link()}" target="_blank" rel="noopener" aria-label="Écrire sur WhatsApp">
  {icon("chat", "ic-wa")}
</a>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js" defer></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js" defer></script>
<script src="/assets/js/main.js" defer></script>
<script src="/assets/js/anim.js" defer></script>
{schema}
</body>
</html>'''


def page(path, title, desc, active, body, og="cover", extra=""):
    out = PUB / path.strip("/") / "index.html" if path != "/" else PUB / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    html = head(title, desc, path, active, og, extra) + "\n<body>\n" + header(active) + f'\n<main id="main">\n{body}\n</main>\n' + footer()
    out.write_text(html, encoding="utf-8")


def page_hero(eyebrow, h1, lead, img=None, crumbs=None):
    bc = ""
    if crumbs:
        bc = '<nav class="crumbs" aria-label="Fil d\'Ariane">' + " / ".join(
            f'<a href="{h}">{l}</a>' if h else f"<span>{l}</span>" for l, h in crumbs) + "</nav>"
    bg = f'<div class="ph-bg">{pic(img, "", sizes="100vw", eager=True)}</div>' if img else ""
    return f'''<section class="page-hero">
  {bg}<div class="shade"></div>
  <div class="wrap ph-in">{bc}<p class="eyebrow">{eyebrow}</p><h1>{h1}</h1><p class="lead">{lead}</p></div>
</section>'''


def pole_cards():
    out = ""
    for i, p in enumerate(POLES, 1):
        out += f'''<a class="pole-card reveal" href="/services/{p["slug"]}">
  <div class="pc-img">{pic(p["img"], "", sizes="(min-width:900px) 380px, 100vw", w=800, h=533)}<span class="pc-num">0{i}</span></div>
  <div class="pc-body">
    <span class="pc-ic">{icon(p["icon"])}</span>
    <h3>{p["name"]}</h3>
    <p>{p["intro"]}</p>
    <span class="more">Découvrir {icon("arrow","ic-s")}</span>
  </div>
</a>'''
    return out


# ------------------------------------------------------------------ pages
def build_pages():
    # ---------------- Accueil
    body = f'''<section class="hero">
  <div class="hero-bg">{pic("cover", "", eager=True)}</div><div class="shade"></div>
  <div class="wrap hero-in">
    <div class="hero-txt">
      <p class="eyebrow">Fortezza · L'Excellence Technologique</p>
      <h1>Votre Partenaire Technologique pour une <em>Performance Durable.</em></h1>
      <p class="lead">Fortezza accompagne les entreprises au Bénin et en Afrique dans leur transformation numérique : de la fourniture de matériel à la sécurisation de vos systèmes.</p>
      <div class="hero-btns">
        <a class="btn btn-primary btn-lg" href="/devis">Demander un Devis {icon("arrow","ic-s")}</a>
        <a class="btn btn-ghost btn-lg" href="#services">Nos Services</a>
      </div>
    </div>
  </div>
  <div class="wrap"><ul class="hero-proof">
    <li>{icon("user","ic-s")} Un seul interlocuteur</li>
    <li>{icon("bolt","ic-s")} Réactivité à Cotonou</li>
    <li>{icon("shield","ic-s")} Matériel certifié &amp; garanti</li>
    <li>{icon("chat","ic-s")} Conseil avant la vente</li>
  </ul></div>
</section>

<section class="section about-home">
  <div class="wrap split">
    <div class="split-img reveal">{pic("about", "Collaborateurs travaillant sur un ordinateur portable", sizes="(min-width:900px) 560px, 100vw", w=1600, h=1066)}
      <div class="float-card">{icon("shield")}<div><strong>Vision</strong><span>Devenir la référence de l'excellence IT en Afrique de l'Ouest.</span></div></div>
    </div>
    <div class="split-txt reveal">
      <p class="eyebrow">À propos</p>
      <h2>Qui est Fortezza&nbsp;?</h2>
      <p>Fortezza SAS est une société béninoise spécialisée en informatique, systèmes d'information et services numériques. Notre mission est simple : <strong>rendre la technologie accessible, fiable et performante pour toutes les entreprises, quelle que soit leur taille.</strong></p>
      <p>Nous ne vendons pas juste du matériel ou des logiciels. Nous apportons des solutions qui résolvent de vrais problèmes : sécuriser vos données, fluidifier votre travail, et vous faire gagner du temps.</p>
      <a class="link-arrow" href="/a-propos">En savoir plus {icon("arrow","ic-s")}</a>
    </div>
  </div>
</section>

<section class="section expertises" id="services">
  <div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">Nos expertises</p><h2>Nos Expertises</h2>
      <p class="sub">Cinq pôles complémentaires pour couvrir tout votre IT.</p></div>
    <div class="pole-grid">{pole_cards()}</div>
  </div>
</section>

{why_block()}
{cta_block()}'''
    page("/", "Fortezza SAS | Vente Matériel Informatique, Maintenance & Services IT au Bénin",
         "Fortezza est votre fournisseur de matériel informatique, maintenance, réseau et développement web au Bénin. Devis gratuit à Cotonou.",
         "home", body)

    # ---------------- À propos
    body = page_hero("À propos", "Plus qu'un prestataire, <em>votre partenaire technologique.</em>",
                     "Fortezza accompagne entreprises, administrations et particuliers de l'idée à la maintenance.",
                     img="team", crumbs=[("Accueil", "/"), ("À propos", None)]) + f'''
<section class="section">
  <div class="wrap split">
    <div class="split-txt reveal">
      <p class="eyebrow">Qui est Fortezza&nbsp;?</p>
      <h2>Une société béninoise, une exigence d'excellence.</h2>
      <p>Fortezza SAS est une société béninoise spécialisée en informatique, systèmes d'information et services numériques, basée à Cotonou. Notre mission est simple : rendre la technologie accessible, fiable et performante pour toutes les entreprises, quelle que soit leur taille.</p>
      <p>Nous ne vendons pas juste du matériel ou des logiciels. Nous apportons des solutions qui résolvent de vrais problèmes : sécuriser vos données, fluidifier votre travail, et vous faire gagner du temps.</p>
      <blockquote>Fortezza, c'est plus qu'un prestataire, c'est votre partenaire technologique.</blockquote>
    </div>
    <div class="split-img reveal">{pic("about2", "Deux collaborateurs échangeant autour d'un ordinateur", sizes="(min-width:900px) 560px, 100vw")}</div>
  </div>
</section>
<section class="section vm">
  <div class="wrap vm-grid">
    <div class="vm-card dark reveal"><p class="eyebrow">Notre vision</p><p class="big">Devenir la référence de l'excellence IT en Afrique de l'Ouest.</p></div>
    <div class="vm-card reveal"><p class="eyebrow alt">Notre mission</p><p class="big">Rendre la technologie accessible, fiable et performante pour toutes les entreprises, quelle que soit leur taille.</p></div>
  </div>
</section>
{why_block()}
{cta_block()}'''
    page("/a-propos", "À propos de Fortezza | Société informatique à Cotonou, Bénin",
         "Fortezza SAS, société béninoise de services informatiques et numériques à Cotonou : notre vision, notre mission et nos engagements.",
         "about", body, og="team")

    # ---------------- Services (vue d'ensemble)
    body = page_hero("Nos services", "Cinq pôles, <em>un seul interlocuteur.</em>",
                     "Infrastructures, matériel, maintenance, développement web et formation : Fortezza couvre tout votre IT, de l'idée à la maintenance.",
                     img="infra", crumbs=[("Accueil", "/"), ("Services", None)]) + f'''
<section class="section expertises"><div class="wrap"><div class="pole-grid">{pole_cards()}</div></div></section>
{why_block()}
{cta_block()}'''
    page("/services", "Nos services informatiques à Cotonou | Fortezza",
         "Matériel informatique, réseau, maintenance, développement web & Cloud et formation : découvrez les 5 pôles d'expertise de Fortezza au Bénin.",
         "services", body, og="infra")

    # ---------------- Pages pôle
    for i, p in enumerate(POLES):
        items = "".join(f'<li class="reveal"><span class="n">{icon("check","ic-s")}</span><span>{t}</span></li>' for t in p["items"])
        others = "".join(f'<a class="reveal" href="/services/{o["slug"]}">{icon(o["icon"])}<span>{o["short"]}</span></a>' for o in POLES if o is not p)
        body = page_hero(f"Pôle 0{i+1}", p["pagetitle"], f'<strong>{p["accroche"]}</strong>', img=p["img"],
                         crumbs=[("Accueil", "/"), ("Services", "/services"), (p["short"], None)]) + f'''
<section class="section">
  <div class="wrap split">
    <div class="split-txt reveal">
      <p class="eyebrow">{p["short"]}</p>
      <h2>{p["accroche"]}</h2>
      <p class="intro">{p["intro"]}</p>
      <a class="btn btn-primary" href="/devis?service={p["slug"]}">Demander un devis pour ce service {icon("arrow","ic-s")}</a>
    </div>
    <div class="presta reveal"><h3>Nos prestations</h3><ul>{items}</ul></div>
  </div>
</section>
<section class="section other-poles"><div class="wrap">
  <h3 class="reveal">Découvrez aussi nos autres pôles</h3>
  <div class="other-grid">{others}</div>
</div></section>
{why_block()}
{cta_block(p["slug"])}'''
        page(f"/services/{p['slug']}", f"{p['pagetitle']} à Cotonou | Fortezza", p["seo"], "services", body, og=p["img"])

    # ---------------- Devis
    opts = "".join(f'<option value="{p["slug"]}">{p["name"]}</option>' for p in POLES) + '<option value="autre">Autre</option>'
    body = page_hero("Devis gratuit", "Demandez votre <em>devis</em>.",
                     "Décrivez-nous votre besoin : nous revenons vers vous rapidement avec une proposition adaptée.",
                     img="contact", crumbs=[("Accueil", "/"), ("Demande de devis", None)]) + f'''
<section class="section">
  <div class="wrap form-layout">
    <form class="card-form reveal" id="quote-form" {form_attrs("devis")} enctype="multipart/form-data" novalidate>
      {form_hidden("devis")}
      <div class="hp" aria-hidden="true"><label>Ne pas remplir <input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
      <div class="row2">
        <label>Nom et prénom *<input name="nom" required autocomplete="name"></label>
        <label>Entreprise / Organisation<input name="entreprise" autocomplete="organization"></label>
      </div>
      <div class="row2">
        <label>Type de client *<select name="type" required><option value="">Choisir…</option><option>Entreprise</option><option>Administration</option><option>Particulier</option></select></label>
        <label>Téléphone (WhatsApp) *<input name="tel" type="tel" required value="+229 " autocomplete="tel"></label>
      </div>
      <div class="row2">
        <label>Email *<input name="email" type="email" required autocomplete="email"></label>
        <label>Service concerné *<select name="service" id="service" required><option value="">Choisir…</option>{opts}</select></label>
      </div>
      <label>Description du besoin *<textarea name="besoin" rows="5" required placeholder="Décrivez votre projet ou votre problème…"></textarea></label>
      <div class="row2">
        <label>Budget indicatif (FCFA)<select name="budget"><option value="">Je préfère en discuter</option><option>Moins de 500 000</option><option>500 000 – 2 000 000</option><option>2 000 000 – 10 000 000</option><option>Plus de 10 000 000</option></select></label>
        <label>Délai souhaité<select name="delai"><option value="">Pas de délai</option><option>Urgent</option><option>Sous 1 mois</option><option>Sous 3 mois</option></select></label>
      </div>
      <label>Pièce jointe (PDF ou image, 5 Mo max)<input name="fichier" type="file" accept=".pdf,image/*"></label>
      <label class="check"><input type="checkbox" name="consent" required> <span>J'accepte que mes données soient utilisées pour traiter ma demande. *</span></label>
      <button class="btn btn-primary btn-lg" type="submit">Envoyer ma demande {icon("arrow","ic-s")}</button>
      <p class="form-msg" role="status" aria-live="polite"></p>
    </form>
    <aside class="side reveal">
      <div class="side-card dark"><h3>Besoin d'une réponse rapide&nbsp;?</h3>
        <p>Écrivez-nous directement sur WhatsApp.</p>
        <a class="btn btn-wa" href="{wa_link()}" target="_blank" rel="noopener">{icon("chat","ic-s")} Discuter sur WhatsApp</a></div>
      <ul class="side-list">
        <li>{icon("check","ic-s")} Devis gratuit, sans engagement</li>
        <li>{icon("check","ic-s")} Un seul interlocuteur pour tout votre IT</li>
        <li>{icon("check","ic-s")} Accusé de réception immédiat par email</li>
        <li>{icon("clock","ic-s")} {C["hours"][0][0]} : {C["hours"][0][1]}</li>
      </ul>
    </aside>
  </div>
</section>'''
    page("/devis", "Demande de devis gratuit | Fortezza, société informatique à Cotonou",
         "Demandez un devis gratuit à Fortezza : matériel informatique, maintenance, réseau, développement web ou formation au Bénin.",
         "devis", body, og="contact")

    # ---------------- Contact
    hrs = "".join(f"<li><span>{d}</span><strong>{h}</strong></li>" for d, h in C["hours"])
    body = page_hero("Contact", "Parlons de <em>votre projet.</em>", "Une question, un besoin, une urgence ? Notre équipe vous répond.",
                     img="about", crumbs=[("Accueil", "/"), ("Contact", None)]) + f'''
<section class="section">
  <div class="wrap contact-grid">
    <div class="contact-info reveal">
      <ul class="ci">
        <li>{icon("pin")}<div><strong>Adresse</strong><span>{C["address"]}</span></div></li>
        <li>{icon("phone")}<div><strong>Téléphone</strong><a href="tel:{C["phone"].replace(" ","")}">{C["phone"]}</a></div></li>
        <li>{icon("chat")}<div><strong>WhatsApp</strong><a href="{wa_link()}" target="_blank" rel="noopener">Écrire sur WhatsApp</a></div></li>
        <li>{icon("mail")}<div><strong>Email</strong><a href="mailto:{C["email"]}">{C["email"]}</a></div></li>
      </ul>
      <div class="hours-card"><h3>{icon("clock","ic-s")} Horaires d'ouverture</h3><ul>{hrs}</ul></div>
      <div class="map"><iframe title="Carte de Cotonou" loading="lazy" referrerpolicy="no-referrer-when-downgrade"
        src="https://www.google.com/maps?q=Cotonou,+B%C3%A9nin&output=embed"></iframe></div>
    </div>
    <form class="card-form reveal" id="contact-form" {form_attrs("contact")} novalidate>
      <h2>Écrivez-nous</h2>
      {form_hidden("contact")}
      <div class="hp" aria-hidden="true"><label>Ne pas remplir <input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
      <label>Nom *<input name="nom" required autocomplete="name"></label>
      <div class="row2">
        <label>Email *<input name="email" type="email" required autocomplete="email"></label>
        <label>Téléphone<input name="tel" type="tel" autocomplete="tel"></label>
      </div>
      <label>Message *<textarea name="besoin" rows="6" required></textarea></label>
      <label class="check"><input type="checkbox" name="consent" required> <span>J'accepte que mes données soient utilisées pour répondre à ma demande. *</span></label>
      <button class="btn btn-primary btn-lg" type="submit">Envoyer {icon("arrow","ic-s")}</button>
      <p class="form-msg" role="status" aria-live="polite"></p>
    </form>
  </div>
</section>'''
    page("/contact", "Contact Fortezza | Société informatique à Cotonou, Bénin",
         "Contactez Fortezza à Cotonou : téléphone, WhatsApp, email et horaires. Devis gratuit pour votre matériel, réseau ou maintenance informatique.",
         "contact", body, og="about")

    # ---------------- Mentions légales
    body = page_hero("Informations", "Mentions légales", "Informations légales relatives au site fortezza.bj.",
                     crumbs=[("Accueil", "/"), ("Mentions légales", None)]) + f'''
<section class="section"><div class="wrap prose">
  <h2>Éditeur du site</h2>
  <p>{C["legal"]} — {C["address"]}<br>Email : {C["email"]} · Téléphone : {C["phone"]}</p>
  <p>RCCM : <em>à fournir</em> · IFU : <em>à fournir</em> · Directeur de la publication : <em>à fournir</em></p>
  <h2>Hébergement</h2><p><em>Hébergeur à fournir.</em></p>
  <h2>Données personnelles</h2>
  <p>Les informations transmises via les formulaires (devis, contact) sont utilisées uniquement pour traiter votre demande et ne sont jamais cédées à des tiers.</p>
  <h2>Crédits</h2>
  <p>Photographies : Pexels (licence libre de droits). Conception : Fortezza.</p>
</div></section>'''
    page("/mentions-legales", "Mentions légales | Fortezza", "Mentions légales du site fortezza.bj.", "legal", body,
         extra='<meta name="robots" content="noindex">')

    # ---------------- Merci + 404
    body = page_hero("Merci", "Votre demande a bien été <em>envoyée.</em>", "Nous revenons vers vous très rapidement. Un accusé de réception vous a été envoyé par email.") + \
        '<section class="section"><div class="wrap center"><a class="btn btn-primary" href="/">Retour à l\'accueil</a></div></section>'
    page("/merci", "Merci | Fortezza", "Votre demande a bien été envoyée.", "", body, extra='<meta name="robots" content="noindex">')
    body = page_hero("Erreur 404", "Page <em>introuvable.</em>", "La page que vous cherchez n'existe pas ou a été déplacée.") + \
        '<section class="section"><div class="wrap center"><a class="btn btn-primary" href="/">Retour à l\'accueil</a></div></section>'
    page("/404", "Page introuvable | Fortezza", "Page introuvable.", "", body, extra='<meta name="robots" content="noindex">')
    (PUB / "404.html").write_text((PUB / "404" / "index.html").read_text(encoding="utf-8"), encoding="utf-8")
    shutil.rmtree(PUB / "404")

    # ---------------- sitemap / robots
    urls = ["/", "/a-propos", "/services"] + [f"/services/{p['slug']}" for p in POLES] + ["/devis", "/contact"]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + \
        "".join(f"  <url><loc>{C['domain']}{u}</loc></url>\n" for u in urls) + "</urlset>\n"
    (PUB / "sitemap.xml").write_text(sm, encoding="utf-8")
    (PUB / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /send.php\nSitemap: {C['domain']}/sitemap.xml\n", encoding="utf-8")


if __name__ == "__main__":
    (PUB / "assets" / "img").mkdir(parents=True, exist_ok=True)
    build_images()
    build_pages()
    for f in ("send.php", ".htaccess"):
        (PUB / f).unlink(missing_ok=True)
    (PUB / "_headers").unlink(missing_ok=True)
    if HOST == "netlify":
        (PUB / "_headers").write_text(
            "/assets/*\n  Cache-Control: public, max-age=31536000, immutable\n", encoding="utf-8")
    else:
        for f in ("send.php", ".htaccess"):
            shutil.copy(ROOT / "archive-php" / f, PUB / f)
        (PUB / "robots.txt").write_text(
            f"User-agent: *\nAllow: /\nDisallow: /send.php\nSitemap: {C['domain']}/sitemap.xml\n", encoding="utf-8")
    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    zp = shutil.make_archive(str(dist / f"fortezza-{HOST}"), "zip", PUB)
    print("OK ->", PUB, "|", HOST, "| zip:", zp)
