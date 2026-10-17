"""
Share cards (og:image) for PDFPro pages: 1200x630 JPEGs in assets/og/.

    python3 tools/make_og.py            # all cards
    python3 tools/make_og.py --only he  # one language

One card per tool page, per blog article and for the home page, in English
and Hebrew, plus <lang>-default.jpg for every other page. build.py points
og:image at the page's card when the file exists, else at the default.

Needs Playwright for Python and a Chromium (PLAYWRIGHT_CHROMIUM or
/opt/pw-browsers/chromium). Fonts come from tools/og-fonts (Heebo and
Plus Jakarta Sans, SIL Open Font License), so cards look the same on any
machine. Re-run after adding a tool or an article; existing cards are
overwritten only when their text changed.
"""

import hashlib
import html
import importlib.util
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "og"
FONTS = ROOT / "tools" / "og-fonts"
STAMP = ROOT / "tools" / "og-cards.json"  # text hash per card, so unchanged cards are not re-rendered

TAGLINE = {"he": "חינם · בלי הרשמה · עברית מימין לשמאל", "en": "Free · No sign-up · Hebrew & RTL ready"}
GUIDE = {"he": "מדריך", "en": "Guide"}
HOME = {
    "he": ("כלי PDF בעברית, בחינם", "המרה, דחיסה, חתימה, OCR ותרגום, ישר מהדפדפן"),
    "en": ("Free PDF tools", "Convert, compress, sign, OCR and translate, right in your browser"),
}


def load_build():
    spec = importlib.util.spec_from_file_location("build", ROOT / "build.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def first_sentence(text: str, limit: int = 110) -> str:
    s = text.split(". ")[0].rstrip(".")
    if len(s) <= limit:
        return s
    for mark in (":", ";", ","):  # a whole clause reads better than a cut sentence
        head = s.split(mark)[0]
        if 25 <= len(head) <= limit:
            return head
    return s[: limit - 1].rsplit(" ", 1)[0] + "…"


def cards(b, langs):
    for lang in langs:
        yield f"{lang}-home", lang, "", *HOME[lang]
        yield f"{lang}-default", lang, "", *HOME[lang]
        for t in b.TOOLS:
            d = t[lang]
            yield f"{lang}-{t['slug']}", lang, "", d["h1"], first_sentence(d["lead"])
        for a in b.ARTICLES:
            d = a[lang]
            yield f"{lang}-blog-{a['slug']}", lang, f"{GUIDE[lang]} · {d['tag']}", d["title"], ""


def font_face(family: str, file: str, weight: int, rng: str) -> str:
    return (f"@font-face{{font-family:'{family}';font-weight:{weight};"
            f"src:url('file://{FONTS / file}') format('woff2');unicode-range:{rng}}}")


HEB = "U+0590-05FF,U+200C-2010,U+20AA,U+25CC,U+FB1D-FB4F"
LAT = "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD"
CSS_FONTS = "".join([
    font_face("Heebo", "heebo-hebrew-500-normal.woff2", 500, HEB),
    font_face("Heebo", "heebo-hebrew-800-normal.woff2", 800, HEB),
    font_face("Heebo", "heebo-hebrew-900-normal.woff2", 900, HEB),
    font_face("Heebo", "heebo-latin-500-normal.woff2", 500, LAT),
    font_face("Heebo", "heebo-latin-800-normal.woff2", 800, LAT),
    font_face("Heebo", "heebo-latin-900-normal.woff2", 900, LAT),
    font_face("Jakarta", "plus-jakarta-sans-latin-500-normal.woff2", 500, LAT),
    font_face("Jakarta", "plus-jakarta-sans-latin-800-normal.woff2", 800, LAT),
])


def card_html(lang: str, kicker: str, title: str, sub: str) -> str:
    rtl = lang == "he"
    font = "'Heebo'" if rtl else "'Jakarta','Heebo'"
    size = 76 if len(title) <= 28 else 64 if len(title) <= 46 else 54
    e = html.escape
    return f"""<!doctype html><html lang="{lang}" dir="{'rtl' if rtl else 'ltr'}"><head><meta charset="utf-8"><style>
{CSS_FONTS}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{overflow:hidden}}
body{{width:1200px;height:630px;background:#0D1B2A;color:#fff;font-family:{font},sans-serif;overflow:hidden;position:relative}}
.bg{{position:absolute;inset:0;overflow:hidden}}
.glow{{position:absolute;width:760px;height:760px;border-radius:50%;background:radial-gradient(circle,rgba(224,32,32,.28),rgba(224,32,32,0) 65%);
  top:-260px;{'left' if rtl else 'right'}:-240px}}
.bar{{position:absolute;bottom:0;left:0;right:0;height:10px;background:#E02020}}
.wrap{{position:absolute;inset:70px 80px 80px 80px;display:flex;flex-direction:column}}
.logo{{font-family:'Jakarta','Heebo',sans-serif;font-weight:800;font-size:44px;letter-spacing:-1px;direction:ltr;align-self:flex-start}}
.logo span{{color:#FF4444}}
.mid{{margin-top:auto;margin-bottom:auto}}
.kicker{{display:inline-block;font-weight:800;font-size:26px;color:#FF6B6B;letter-spacing:.5px;margin-bottom:18px}}
h1{{font-weight:900;font-size:{size}px;line-height:1.12;letter-spacing:-.5px;max-width:1000px}}
.sub{{margin-top:22px;font-weight:500;font-size:32px;line-height:1.35;color:rgba(255,255,255,.78);max-width:980px}}
.tag{{font-weight:500;font-size:26px;color:rgba(255,255,255,.62)}}
.url{{font-family:'Jakarta','Heebo',sans-serif;font-weight:800;color:#fff;direction:ltr;unicode-bidi:isolate}}
.foot{{display:flex;justify-content:space-between;align-items:center}}
</style></head><body><div class="bg"><div class="glow"></div></div><div class="wrap">
<div class="logo">PDF<span>Pro</span></div>
<div class="mid">{f'<div class="kicker">{e(kicker)}</div>' if kicker else ''}<h1>{e(title)}</h1>{f'<div class="sub">{e(sub)}</div>' if sub else ''}</div>
<div class="foot"><div class="tag">{e(TAGLINE[lang])}</div><div class="tag url">pdfproapp.com</div></div>
</div><div class="bar"></div></body></html>"""


def main():
    langs = [sys.argv[sys.argv.index("--only") + 1]] if "--only" in sys.argv else ["en", "he"]
    b = load_build()
    OUT.mkdir(parents=True, exist_ok=True)
    stamps = json.loads(STAMP.read_text()) if STAMP.exists() else {}
    todo = []
    for name, lang, kicker, title, sub in cards(b, langs):
        doc = card_html(lang, kicker, title, sub)
        h = hashlib.md5(doc.encode()).hexdigest()
        if stamps.get(name) != h or not (OUT / f"{name}.jpg").exists():
            todo.append((name, doc, h))
    if not todo:
        print("Share cards up to date")
        return

    from playwright.sync_api import sync_playwright
    exe = os.environ.get("PLAYWRIGHT_CHROMIUM", "/opt/pw-browsers/chromium")
    tmp = OUT / ".card.html"
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=exe if Path(exe).exists() else None)
        page = browser.new_page(viewport={"width": 1200, "height": 630})
        for name, doc, h in todo:
            tmp.write_text(doc, encoding="utf-8")
            page.goto(tmp.as_uri())
            page.evaluate("document.fonts.ready")
            page.screenshot(path=str(OUT / f"{name}.jpg"), type="jpeg", quality=88)
            stamps[name] = h
        browser.close()
    tmp.unlink(missing_ok=True)
    STAMP.write_text(json.dumps(stamps, indent=0, sort_keys=True))
    print(f"Rendered {len(todo)} share cards into {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
