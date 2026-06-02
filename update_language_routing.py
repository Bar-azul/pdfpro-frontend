from __future__ import annotations

import re
from pathlib import Path

# =========================================================
# PDFPro language routing updater
# =========================================================
# What this script does:
# 1. Removes the language buttons from the header.
# 2. Makes language selection available only in the footer.
# 3. Uses real language URLs:
#       English: /merge-pdf/
#       Hebrew:  /he/merge-pdf/
# 4. Adds canonical + hreflang tags.
# 5. Updates all existing index.html files under frontend/.
# 6. Keeps your existing tool logic, modal logic and API calls.
# =========================================================

SITE_URL = "https://pdfproapp.com"
DEFAULT_LANG = "en"
SUPPORTED_LANGS = ["en", "he"]
LANG_PREFIXES = {"en": "", "he": "he"}
LANG_LABELS = {"en": "English", "he": "עברית"}
LANG_DIR = {"en": "ltr", "he": "rtl"}
HTML_LANG = {"en": "en", "he": "he"}

# Run this script from the project root or from frontend/.
SCRIPT_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = SCRIPT_DIR if (SCRIPT_DIR / "index.html").exists() else SCRIPT_DIR / "frontend"

SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".next", "venv", ".venv", "__pycache__"}

HOME_TEXT = {
    "en": {
        "tools": "Tools",
        "features": "Features",
        "pricing": "Pricing",
        "cta": "Get Started",
        "company": "Company",
        "support": "Support",
        "footer_desc": "The leading platform for PDF processing — fast, secure and professional.",
        "footer_tools": "Tools",
        "footer_company": "Company",
        "footer_support": "Support",
        "convert_pdf": "Convert PDF",
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
        "api_connecting": "Connecting...",
    },
    "he": {
        "tools": "כלים",
        "features": "יתרונות",
        "pricing": "מחירים",
        "cta": "התחל עכשיו",
        "company": "חברה",
        "support": "תמיכה",
        "footer_desc": "הפלטפורמה המובילה לעיבוד מסמכי PDF — מהירה, מאובטחת ומקצועית.",
        "footer_tools": "כלים",
        "footer_company": "חברה",
        "footer_support": "תמיכה",
        "convert_pdf": "המרת PDF",
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
        "api_connecting": "מתחבר...",
    },
}

PAGE_TITLES = {
    "": {
        "en": "PDFPro | Professional PDF Tools",
        "he": "PDFPro | כלי PDF מקצועיים",
    },
    "compress-pdf": {
        "en": "Compress PDF Online | PDFPro",
        "he": "דחיסת PDF אונליין | PDFPro",
    },
    "merge-pdf": {
        "en": "Merge PDF Online | PDFPro",
        "he": "מיזוג PDF אונליין | PDFPro",
    },
    "split-pdf": {
        "en": "Split PDF Online | PDFPro",
        "he": "פיצול PDF אונליין | PDFPro",
    },
    "ocr-pdf": {
        "en": "OCR PDF Online | PDFPro",
        "he": "OCR ל־PDF אונליין | PDFPro",
    },
    "translate-pdf": {
        "en": "Translate PDF Online | PDFPro",
        "he": "תרגום PDF אונליין | PDFPro",
    },
    "pdf-to-word": {
        "en": "PDF to Word Online | PDFPro",
        "he": "המרת PDF ל־Word אונליין | PDFPro",
    },
    "pdf-to-excel": {
        "en": "PDF to Excel Online | PDFPro",
        "he": "המרת PDF ל־Excel אונליין | PDFPro",
    },
    "pricing": {
        "en": "Pricing | PDFPro",
        "he": "מחירים | PDFPro",
    },
    "about": {
        "en": "About PDFPro",
        "he": "אודות PDFPro",
    },
    "blog": {
        "en": "PDFPro Blog",
        "he": "בלוג PDFPro",
    },
    "contact": {
        "en": "Contact PDFPro",
        "he": "צור קשר | PDFPro",
    },
    "help": {
        "en": "Help Center | PDFPro",
        "he": "מרכז עזרה | PDFPro",
    },
    "privacy": {
        "en": "Privacy Policy | PDFPro",
        "he": "מדיניות פרטיות | PDFPro",
    },
    "terms": {
        "en": "Terms of Use | PDFPro",
        "he": "תנאי שימוש | PDFPro",
    },
}

PAGE_DESCRIPTIONS = {
    "": {
        "en": "Professional PDF tools to convert, merge, split, compress, edit and translate files online.",
        "he": "כלי PDF מקצועיים להמרה, מיזוג, פיצול, דחיסה, עריכה ותרגום קבצים אונליין.",
    },
    "compress-pdf": {
        "en": "Compress PDF files online and reduce file size quickly and securely.",
        "he": "דחסו קבצי PDF אונליין והקטינו את גודל הקובץ במהירות ובצורה מאובטחת.",
    },
    "merge-pdf": {
        "en": "Merge multiple PDF files into one PDF document online.",
        "he": "מזגו כמה קבצי PDF למסמך PDF אחד אונליין.",
    },
    "split-pdf": {
        "en": "Split PDF files into separate pages or page ranges online.",
        "he": "פצלו קבצי PDF לעמודים נפרדים או לטווחי עמודים אונליין.",
    },
    "ocr-pdf": {
        "en": "Extract text from scanned PDFs and images using OCR online.",
        "he": "חלצו טקסט מקבצי PDF סרוקים ומתמונות באמצעות OCR אונליין.",
    },
    "translate-pdf": {
        "en": "Translate PDF files online while keeping the process fast and simple.",
        "he": "תרגמו קבצי PDF אונליין בצורה פשוטה, מהירה ונוחה.",
    },
}


def html_attr_escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace('"', "&quot;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def detect_lang_and_slug(file_path: Path) -> tuple[str, str]:
    rel = file_path.relative_to(FRONTEND_DIR)
    parts = list(rel.parts)

    lang = DEFAULT_LANG
    if parts and parts[0] in LANG_PREFIXES.values() and parts[0]:
        lang = next(k for k, v in LANG_PREFIXES.items() if v == parts[0])
        parts = parts[1:]

    # index.html at root or /he/index.html => home slug ""
    if parts == ["index.html"]:
        return lang, ""

    # compress-pdf/index.html => compress-pdf
    if len(parts) >= 2 and parts[-1] == "index.html":
        return lang, "/".join(parts[:-1])

    return lang, ""


def localized_path(slug: str, lang: str) -> str:
    prefix = LANG_PREFIXES[lang]
    if slug == "":
        return f"/{prefix}/" if prefix else "/"
    return f"/{prefix}/{slug}/" if prefix else f"/{slug}/"


def absolute_url(slug: str, lang: str) -> str:
    return SITE_URL.rstrip("/") + localized_path(slug, lang)


def build_hreflang(slug: str, current_lang: str) -> str:
    canonical = absolute_url(slug, current_lang)
    lines = [f'<link rel="canonical" href="{canonical}">']
    for lang in SUPPORTED_LANGS:
        lines.append(f'<link rel="alternate" hreflang="{HTML_LANG[lang]}" href="{absolute_url(slug, lang)}">')
    lines.append(f'<link rel="alternate" hreflang="x-default" href="{absolute_url(slug, DEFAULT_LANG)}">')
    return "\n".join(lines)


def build_nav(lang: str) -> str:
    tx = HOME_TEXT[lang]
    home = localized_path("", lang)
    pricing = localized_path("pricing", lang)
    return f'''<nav>
  <a href="{home}" class="logo">PDF<span>Pro</span></a>
  <ul class="nav-links">
    <li><a href="{home}#tools">{tx["tools"]}</a></li>
    <li><a href="{home}#features">{tx["features"]}</a></li>
    <li><a href="{pricing}">{tx["pricing"]}</a></li>
  </ul>
  <div class="nav-right">
    <span class="api-status offline" id="api-status"><span class="api-dot"></span><span id="api-status-text">{tx["api_connecting"]}</span></span>
    <button class="nav-cta" onclick="document.getElementById('tools')?.scrollIntoView({{behavior:'smooth'}})">{tx["cta"]}</button>
  </div>
</nav>'''


def build_footer(lang: str) -> str:
    tx = HOME_TEXT[lang]
    home = localized_path("", lang)
    selected = {k: " selected" if k == lang else "" for k in SUPPORTED_LANGS}
    return f'''<footer>
  <div class="footer-inner">
    <div class="footer-brand">
      <a href="{home}" class="logo">PDF<span>Pro</span></a>
      <p>{tx["footer_desc"]}</p>

      <div class="footer-language">
        <label for="footer-lang">{tx["language"]}</label>
        <select id="footer-lang" onchange="changeSiteLanguage(this.value)">
          <option value="en"{selected["en"]}>English</option>
          <option value="he"{selected["he"]}>עברית</option>
        </select>
      </div>
    </div>

    <div class="footer-col"><h4>{tx["footer_tools"]}</h4><ul>
      <li><a href="{localized_path('pdf-to-word', lang)}">{tx["convert_pdf"]}</a></li>
      <li><a href="#" onclick="openModal('watermark');return false">{tx["edit_pdf"]}</a></li>
      <li><a href="{localized_path('merge-pdf', lang)}">{tx["merge_pdf"]}</a></li>
      <li><a href="{localized_path('ocr-pdf', lang)}">OCR</a></li>
    </ul></div>

    <div class="footer-col"><h4>{tx["footer_company"]}</h4><ul>
      <li><a href="{localized_path('about', lang)}">{tx["about"]}</a></li>
      <li><a href="{localized_path('blog', lang)}">{tx["blog"]}</a></li>
      <li><a href="{localized_path('contact', lang)}">{tx["contact"]}</a></li>
    </ul></div>

    <div class="footer-col"><h4>{tx["footer_support"]}</h4><ul>
      <li><a href="{localized_path('help', lang)}">{tx["help"]}</a></li>
      <li><a href="{localized_path('privacy', lang)}">{tx["privacy"]}</a></li>
      <li><a href="{localized_path('terms', lang)}">{tx["terms"]}</a></li>
    </ul></div>
  </div>

  <div class="footer-bottom"><span>{tx["copy"]}</span><span>🌍 Made with ❤️</span></div>
</footer>'''


FOOTER_LANGUAGE_CSS = r'''
.footer-language{margin-top:1.2rem}
.footer-language label{display:block;color:rgba(255,255,255,0.5);font-size:0.85rem;margin-bottom:0.45rem}
.footer-language select{width:190px;max-width:100%;padding:0.55rem 0.8rem;border-radius:8px;border:1px solid rgba(255,255,255,0.2);background:var(--navy-light);color:var(--white);font-size:0.9rem;cursor:pointer}
.footer-language select:focus{outline:2px solid rgba(255,68,68,0.45);outline-offset:2px}
'''


LANGUAGE_ROUTING_JS = r'''
// =========================================================
// SEO language routing
// English pages: /
// Hebrew pages: /he/
// =========================================================
const LANGUAGE_PREFIXES = ['he'];

function getCurrentLanguageFromPath() {
  const path = window.location.pathname;
  if (path === '/he' || path === '/he/' || path.startsWith('/he/')) return 'he';
  return 'en';
}

function getPathWithoutLanguagePrefix(pathname) {
  for (const prefix of LANGUAGE_PREFIXES) {
    if (pathname === `/${prefix}` || pathname === `/${prefix}/`) return '/';
    if (pathname.startsWith(`/${prefix}/`)) return pathname.replace(`/${prefix}`, '') || '/';
  }
  return pathname || '/';
}

function buildLocalizedPath(targetLang) {
  const cleanPath = getPathWithoutLanguagePrefix(window.location.pathname);
  if (targetLang === 'en') return cleanPath;
  if (cleanPath === '/') return `/${targetLang}/`;
  return `/${targetLang}${cleanPath}`;
}

function changeSiteLanguage(targetLang) {
  localStorage.setItem('pdfpro_lang', targetLang);
  window.location.href = buildLocalizedPath(targetLang);
}

function setCurrentFooterLanguage() {
  const select = document.getElementById('footer-lang');
  if (!select) return;
  select.value = getCurrentLanguageFromPath();
}
'''


def replace_or_add_head_seo(html: str, lang: str, slug: str) -> str:
    title = PAGE_TITLES.get(slug, {}).get(lang) or PAGE_TITLES.get(slug, {}).get("en") or PAGE_TITLES[""].get(lang)
    desc = PAGE_DESCRIPTIONS.get(slug, {}).get(lang) or PAGE_DESCRIPTIONS.get(slug, {}).get("en") or PAGE_DESCRIPTIONS[""].get(lang)

    html = re.sub(r"<title>.*?</title>", f"<title>{html_attr_escape(title)}</title>", html, flags=re.I | re.S)

    if re.search(r'<meta\s+name=["\']description["\']', html, flags=re.I):
        html = re.sub(
            r'<meta\s+name=["\']description["\']\s+content=["\'].*?["\']\s*/?>',
            f'<meta name="description" content="{html_attr_escape(desc)}">',
            html,
            flags=re.I | re.S,
        )
    else:
        html = html.replace('<meta name="viewport" content="width=device-width, initial-scale=1.0"/>',
                            '<meta name="viewport" content="width=device-width, initial-scale=1.0"/>\n'
                            f'<meta name="description" content="{html_attr_escape(desc)}">')

    # Remove old canonical / alternates and add the new complete hreflang block.
    html = re.sub(r'\n?<link\s+rel=["\']canonical["\'][^>]*>', '', html, flags=re.I)
    html = re.sub(r'\n?<link\s+rel=["\']alternate["\'][^>]*hreflang=["\'][^"\']+["\'][^>]*>', '', html, flags=re.I)

    hreflang_block = build_hreflang(slug, lang)
    if '</title>' in html:
        html = html.replace('</title>', f'</title>\n{hreflang_block}', 1)
    return html


def update_html_language_attrs(html: str, lang: str) -> str:
    html_lang = HTML_LANG[lang]
    direction = LANG_DIR[lang]

    html = re.sub(r'<html\b[^>]*>', f'<html id="html-root" lang="{html_lang}" dir="{direction}">', html, count=1, flags=re.I)
    html = re.sub(r'<body\b[^>]*>', f'<body class="{direction}">', html, count=1, flags=re.I)
    return html


def update_css(html: str) -> str:
    # Remove unused header language button CSS.
    html = re.sub(r'\n?\.lang-switcher\{[^}]*\}', '', html)
    html = re.sub(r'\n?\.lang-btn[^\{]*\{[^}]*\}', '', html)
    html = re.sub(r'\n?\.lang-btn\.active,\.lang-btn:hover\{[^}]*\}', '', html)

    if '.footer-language{' not in html:
        html = html.replace('@media(max-width:768px){', FOOTER_LANGUAGE_CSS + '\n@media(max-width:768px){', 1)
    return html


def replace_nav_and_footer(html: str, lang: str) -> str:
    html = re.sub(r'<nav>.*?</nav>', build_nav(lang), html, count=1, flags=re.I | re.S)
    html = re.sub(r'<footer>.*?</footer>', build_footer(lang), html, count=1, flags=re.I | re.S)
    return html


def update_javascript(html: str) -> str:
    # Replace the initial lang variable so language comes from URL, not from a header button.
    html = html.replace(
        "let lang='en',currentTool=null,selectedFiles=[];",
        "let lang=getCurrentLanguageFromPath(),currentTool=null,selectedFiles=[];",
    )

    # Remove the old IP-based auto detection + switchLang + applyLang block and replace it with URL-based applyLang.
    old_block_pattern = re.compile(
        r"async function detectAndRedirect\(\)\{.*?\n\}\s*\n\s*function switchLang\(nl\)\{.*?\n\}\s*\n\s*function applyLang\(nl\)\{.*?\n\}\s*\n\s*const TAB_CATS=",
        flags=re.S,
    )

    new_block = r'''function applyLang(nl){
  lang=nl;
  const isRTL=nl==='he';
  document.getElementById('html-root').lang=nl==='he'?'he':'en';
  document.getElementById('html-root').dir=isRTL?'rtl':'ltr';
  document.body.className=isRTL?'rtl':'ltr';
  document.querySelectorAll('select,input,button').forEach(el=>{
    el.style.fontFamily=isRTL?"'Heebo',sans-serif":"'Plus Jakarta Sans',sans-serif";
  });

  // Keep this because your existing homepage still uses data-t attributes.
  // The important SEO change is that every language also has a real URL: / and /he/.
  document.querySelectorAll('[data-t]').forEach(el=>{
    const v=T[lang][el.dataset.t];
    if(v!==undefined) el.innerHTML=v;
  });

  buildToolsUI();
  buildHeroSelect();

  const status=document.getElementById('api-status');
  const statusText=document.getElementById('api-status-text');
  if(status&&statusText){
    statusText.textContent=status.classList.contains('online')?t('api_online'):t('api_offline');
  }

  setCurrentFooterLanguage();
}

const TAB_CATS='''

    html = old_block_pattern.sub(new_block, html)

    # Fix accidental duplicate line if it exists.
    html = html.replace("  const isMobile=window.innerWidth<=768;\n  const isMobile=window.innerWidth<=768;", "  const isMobile=window.innerWidth<=768;")

    # Replace old final initialization.
    html = html.replace("detectAndRedirect();", "applyLang(getCurrentLanguageFromPath());\nsetCurrentFooterLanguage();")

    # Inject language routing functions after <script> only once.
    if "function getCurrentLanguageFromPath()" not in html:
        html = html.replace("<script>\n", "<script>\n" + LANGUAGE_ROUTING_JS + "\n", 1)

    return html


def process_file(path: Path) -> bool:
    lang, slug = detect_lang_and_slug(path)
    original = path.read_text(encoding="utf-8")
    html = original

    html = update_html_language_attrs(html, lang)
    html = replace_or_add_head_seo(html, lang, slug)
    html = update_css(html)
    html = replace_nav_and_footer(html, lang)
    html = update_javascript(html)

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

    html_files = []
    for p in FRONTEND_DIR.rglob("index.html"):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        html_files.append(p)

    updated = 0
    for file_path in sorted(html_files):
        if process_file(file_path):
            updated += 1
            print(f"UPDATED: {file_path.relative_to(FRONTEND_DIR)}")
        else:
            print(f"SKIPPED:  {file_path.relative_to(FRONTEND_DIR)}")

    print("-" * 60)
    print(f"Done. Updated {updated}/{len(html_files)} files.")
    print("Backup files were created as *.html.bak next to changed files.")


if __name__ == "__main__":
    main()
