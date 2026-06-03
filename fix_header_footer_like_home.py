from __future__ import annotations

import re
from pathlib import Path

SITE_URL = "https://pdfproapp.com"

SCRIPT_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = SCRIPT_DIR if (SCRIPT_DIR / "index.html").exists() else SCRIPT_DIR / "frontend"

SUPPORTED_LANGS = ["en", "he"]
SKIP_DIRS = {
    ".git",
    "node_modules",
    "dist",
    "build",
    ".next",
    ".venv",
    "venv",
    "__pycache__",
}

TEXT = {
    "en": {
        "tools": "Tools",
        "features": "Features",
        "pricing": "Pricing",
        "get_started": "Get Started",
        "connecting": "Connecting...",
        "footer_desc": "The leading platform for PDF processing — fast, secure and professional.",
        "footer_tools": "Tools",
        "footer_company": "Company",
        "footer_support": "Support",
        "convert_pdf": "Convert PDF",
        "compress_pdf": "Compress PDF",
        "edit_pdf": "Edit PDF",
        "merge_pdf": "Merge PDF",
        "about": "About",
        "blog": "Blog",
        "contact": "Contact",
        "help": "Help Center",
        "privacy": "Privacy Policy",
        "terms": "Terms of Use",
        "language": "Language",
        "copy": "© 2026 PDFPro. All rights reserved.",
    },
    "he": {
        "tools": "כלים",
        "features": "יתרונות",
        "pricing": "מחירים",
        "get_started": "התחל עכשיו",
        "connecting": "מתחבר...",
        "footer_desc": "הפלטפורמה המובילה לעיבוד מסמכי PDF — מהירה, מאובטחת ומקצועית.",
        "footer_tools": "כלים",
        "footer_company": "חברה",
        "footer_support": "תמיכה",
        "convert_pdf": "המרת PDF",
        "compress_pdf": "דחיסת PDF",
        "edit_pdf": "עריכת PDF",
        "merge_pdf": "מיזוג PDF",
        "about": "אודות",
        "blog": "בלוג",
        "contact": "צור קשר",
        "help": "מרכז עזרה",
        "privacy": "מדיניות פרטיות",
        "terms": "תנאי שימוש",
        "language": "שפה",
        "copy": "© 2026 PDFPro. כל הזכויות שמורות.",
    },
}


SHARED_CSS = r"""
/* ===== PDFPro shared header/footer - same as homepage ===== */
nav{
  background:var(--navy);
  padding:0 3rem;
  height:68px;
  display:flex;
  align-items:center;
  justify-content:space-between;
  position:sticky;
  top:0;
  z-index:100;
  border-bottom:2px solid var(--red);
  width:100%;
  box-sizing:border-box;
}

.logo{
  font-size:1.6rem;
  font-weight:900;
  color:var(--white);
  letter-spacing:-0.5px;
  text-decoration:none;
  white-space:nowrap;
}

.logo span{
  color:var(--red-light);
}

.nav-links{
  display:flex;
  align-items:center;
  gap:2rem;
  list-style:none;
  margin:0;
  padding:0;
}

.nav-links li{
  list-style:none;
  margin:0;
  padding:0;
}

.nav-links a{
  color:rgba(255,255,255,0.75);
  text-decoration:none;
  font-size:0.95rem;
  font-weight:500;
  transition:color 0.2s;
  white-space:nowrap;
}

.nav-links a:hover{
  color:var(--white);
}

.nav-right{
  display:flex;
  align-items:center;
  gap:0.8rem;
}

.nav-cta{
  background:var(--red);
  color:var(--white);
  padding:0.55rem 1.4rem;
  border-radius:6px;
  font-weight:700;
  font-size:0.9rem;
  border:none;
  cursor:pointer;
  transition:background 0.2s;
  text-decoration:none;
  display:inline-flex;
  align-items:center;
  justify-content:center;
  white-space:nowrap;
}

.nav-cta:hover{
  background:var(--red-dark);
}

.api-status{
  display:inline-flex;
  align-items:center;
  gap:0.4rem;
  font-size:0.78rem;
  font-weight:600;
  padding:0.25rem 0.7rem;
  border-radius:20px;
  white-space:nowrap;
}

.api-status.online{
  background:rgba(34,197,94,0.15);
  color:#22c55e;
}

.api-status.offline{
  background:rgba(239,68,68,0.15);
  color:#ef4444;
}

.api-dot{
  width:6px;
  height:6px;
  border-radius:50%;
  background:currentColor;
}

footer{
  background:var(--navy);
  padding:3rem;
  border-top:2px solid rgba(255,255,255,0.06);
  width:100%;
  box-sizing:border-box;
}

.footer-inner{
  max-width:1100px;
  margin:0 auto;
  display:grid;
  grid-template-columns:2fr 1fr 1fr 1fr;
  gap:3rem;
  align-items:start;
}

.footer-brand p{
  font-size:0.85rem;
  color:rgba(255,255,255,0.4);
  line-height:1.6;
  margin-top:0.8rem;
}

.footer-col h4{
  font-size:0.85rem;
  font-weight:700;
  color:rgba(255,255,255,0.5);
  text-transform:uppercase;
  letter-spacing:1px;
  margin-bottom:1rem;
}

body.rtl .footer-col h4{
  letter-spacing:0;
}

.footer-col ul{
  list-style:none;
  margin:0;
  padding:0;
}

.footer-col ul li{
  margin-bottom:0.6rem;
}

.footer-col ul li a{
  color:rgba(255,255,255,0.6);
  text-decoration:none;
  font-size:0.88rem;
  transition:color 0.2s;
}

.footer-col ul li a:hover{
  color:var(--white);
}

.footer-language{
  margin-top:1rem;
}

.footer-language label{
  display:block;
  color:rgba(255,255,255,0.5);
  font-size:0.85rem;
  margin-bottom:0.4rem;
}

.footer-language select{
  width:190px;
  max-width:100%;
  padding:0.55rem 0.8rem;
  border-radius:8px;
  border:1px solid rgba(255,255,255,0.2);
  background:var(--navy-light);
  color:var(--white);
  font-size:0.9rem;
  cursor:pointer;
}

.footer-bottom{
  max-width:1100px;
  margin:2rem auto 0;
  padding-top:1.5rem;
  border-top:1px solid rgba(255,255,255,0.08);
  display:flex;
  justify-content:space-between;
  color:rgba(255,255,255,0.3);
  font-size:0.82rem;
  flex-wrap:wrap;
  gap:1rem;
}

@media(max-width:768px){
  nav{
    padding:0 1rem;
    height:56px;
  }

  .nav-links{
    display:none;
  }

  .logo{
    font-size:1.3rem;
  }

  .nav-cta{
    padding:0.45rem 1rem;
    font-size:0.82rem;
  }

  #api-status{
    display:none;
  }

  footer{
    padding:2rem 1rem;
  }

  .footer-inner{
    grid-template-columns:1fr;
    gap:1.5rem;
  }

  .footer-bottom{
    flex-direction:column;
    align-items:center;
    text-align:center;
  }
}
/* ===== End PDFPro shared header/footer ===== */
"""


LANG_JS = r"""
<script>
function getCurrentSiteLanguage(){
  const path = window.location.pathname;
  if(path === '/he' || path === '/he/' || path.startsWith('/he/')) return 'he';
  return 'en';
}

function removeLanguagePrefix(pathname){
  if(pathname === '/he' || pathname === '/he/') return '/';
  if(pathname.startsWith('/he/')) return pathname.replace('/he', '') || '/';
  return pathname || '/';
}

function buildLanguageUrl(targetLang){
  const cleanPath = removeLanguagePrefix(window.location.pathname);

  if(targetLang === 'en'){
    return cleanPath;
  }

  if(cleanPath === '/'){
    return '/he/';
  }

  return '/he' + cleanPath;
}

function changeSiteLanguage(targetLang){
  localStorage.setItem('pdfpro_lang', targetLang);
  window.location.href = buildLanguageUrl(targetLang);
}

function setFooterLanguageValue(){
  const select = document.getElementById('footer-lang');
  if(!select) return;
  select.value = getCurrentSiteLanguage();
}

document.addEventListener('DOMContentLoaded', setFooterLanguageValue);
</script>
"""


def detect_lang_and_slug(path: Path) -> tuple[str, str]:
    rel = path.relative_to(FRONTEND_DIR)
    parts = list(rel.parts)

    lang = "en"

    if parts and parts[0] == "he":
        lang = "he"
        parts = parts[1:]

    if parts == ["index.html"]:
        slug = ""
    elif len(parts) >= 2 and parts[-1] == "index.html":
        slug = "/".join(parts[:-1])
    else:
        slug = ""

    return lang, slug


def url_for(slug: str, lang: str) -> str:
    if lang == "he":
        if slug:
            return f"/he/{slug}/"
        return "/he/"

    if slug:
        return f"/{slug}/"
    return "/"


def build_header(lang: str) -> str:
    t = TEXT[lang]
    home = url_for("", lang)

    return f"""
<nav>
  <a href="{home}" class="logo">PDF<span>Pro</span></a>

  <ul class="nav-links">
    <li><a href="{home}#tools">{t["tools"]}</a></li>
    <li><a href="{home}#features">{t["features"]}</a></li>
    <li><a href="{url_for("pricing", lang)}">{t["pricing"]}</a></li>
  </ul>

  <div class="nav-right">
    <span class="api-status offline" id="api-status">
      <span class="api-dot"></span>
      <span id="api-status-text">{t["connecting"]}</span>
    </span>

    <a class="nav-cta" href="{home}#tools">{t["get_started"]}</a>
  </div>
</nav>
""".strip()


def build_footer(lang: str) -> str:
    t = TEXT[lang]
    home = url_for("", lang)
    selected_en = " selected" if lang == "en" else ""
    selected_he = " selected" if lang == "he" else ""

    return f"""
<footer>
  <div class="footer-inner">
    <div class="footer-brand">
      <a href="{home}" class="logo">PDF<span>Pro</span></a>
      <p>{t["footer_desc"]}</p>

      <div class="footer-language">
        <label for="footer-lang">{t["language"]}</label>
        <select id="footer-lang" onchange="changeSiteLanguage(this.value)">
          <option value="en"{selected_en}>English</option>
          <option value="he"{selected_he}>עברית</option>
        </select>
      </div>
    </div>

    <div class="footer-col">
      <h4>{t["footer_tools"]}</h4>
      <ul>
        <li><a href="{url_for("pdf-to-word", lang)}">{t["convert_pdf"]}</a></li>
        <li><a href="{url_for("compress-pdf", lang)}">{t["compress_pdf"]}</a></li>
        <li><a href="{url_for("merge-pdf", lang)}">{t["merge_pdf"]}</a></li>
        <li><a href="{url_for("ocr-pdf", lang)}">OCR</a></li>
      </ul>
    </div>

    <div class="footer-col">
      <h4>{t["footer_company"]}</h4>
      <ul>
        <li><a href="{url_for("about", lang)}">{t["about"]}</a></li>
        <li><a href="{url_for("blog", lang)}">{t["blog"]}</a></li>
        <li><a href="{url_for("contact", lang)}">{t["contact"]}</a></li>
      </ul>
    </div>

    <div class="footer-col">
      <h4>{t["footer_support"]}</h4>
      <ul>
        <li><a href="{url_for("help", lang)}">{t["help"]}</a></li>
        <li><a href="{url_for("privacy", lang)}">{t["privacy"]}</a></li>
        <li><a href="{url_for("terms", lang)}">{t["terms"]}</a></li>
      </ul>
    </div>
  </div>

  <div class="footer-bottom">
    <span>{t["copy"]}</span>
    <span>🌍 Made with ❤️</span>
  </div>
</footer>
""".strip()


def remove_old_shared_css(html: str) -> str:
    html = re.sub(
        r"/\* ===== PDFPro shared header/footer - same as homepage ===== \*/.*?/\* ===== End PDFPro shared header/footer ===== \*/",
        "",
        html,
        flags=re.S,
    )
    return html


def inject_shared_css(html: str) -> str:
    html = remove_old_shared_css(html)

    if "</style>" in html:
        return html.replace("</style>", "\n" + SHARED_CSS + "\n</style>", 1)

    return html.replace("</head>", f"<style>\n{SHARED_CSS}\n</style>\n</head>", 1)


def replace_header(html: str, lang: str) -> str:
    header = build_header(lang)

    if re.search(r"<nav\b[^>]*>.*?</nav>", html, flags=re.S | re.I):
        return re.sub(r"<nav\b[^>]*>.*?</nav>", header, html, count=1, flags=re.S | re.I)

    return re.sub(r"(<body\b[^>]*>)", r"\1\n" + header, html, count=1, flags=re.I)


def replace_footer(html: str, lang: str) -> str:
    footer = build_footer(lang)

    if re.search(r"<footer\b[^>]*>.*?</footer>", html, flags=re.S | re.I):
        return re.sub(r"<footer\b[^>]*>.*?</footer>", footer, html, count=1, flags=re.S | re.I)

    return html.replace("</body>", footer + "\n</body>", 1)


def update_html_direction(html: str, lang: str) -> str:
    direction = "rtl" if lang == "he" else "ltr"
    html_lang = "he" if lang == "he" else "en"

    html = re.sub(
        r"<html\b[^>]*>",
        f'<html id="html-root" lang="{html_lang}" dir="{direction}">',
        html,
        count=1,
        flags=re.I,
    )

    html = re.sub(
        r"<body\b[^>]*>",
        f'<body class="{direction}">',
        html,
        count=1,
        flags=re.I,
    )

    return html


def inject_language_js(html: str) -> str:
    html = re.sub(
        r"<script>\s*function getCurrentSiteLanguage\(\).*?</script>",
        "",
        html,
        flags=re.S,
    )

    return html.replace("</body>", LANG_JS + "\n</body>", 1)


def process_file(path: Path) -> bool:
    lang, slug = detect_lang_and_slug(path)

    original = path.read_text(encoding="utf-8")
    html = original

    html = update_html_direction(html, lang)
    html = inject_shared_css(html)
    html = replace_header(html, lang)
    html = replace_footer(html, lang)
    html = inject_language_js(html)

    if html != original:
        backup = path.with_suffix(path.suffix + ".bak")
        if not backup.exists():
            backup.write_text(original, encoding="utf-8")

        path.write_text(html, encoding="utf-8")
        return True

    return False


def main() -> None:
    if not FRONTEND_DIR.exists():
        raise SystemExit(f"Frontend folder not found: {FRONTEND_DIR}")

    files = []
    for path in FRONTEND_DIR.rglob("index.html"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        files.append(path)

    updated = 0

    for path in sorted(files):
        changed = process_file(path)
        rel = path.relative_to(FRONTEND_DIR)

        if changed:
            updated += 1
            print(f"UPDATED: {rel}")
        else:
            print(f"SKIPPED:  {rel}")

    print("-" * 60)
    print(f"Done. Updated {updated}/{len(files)} files.")
    print("Backup created as index.html.bak next to each changed file.")


if __name__ == "__main__":
    main()