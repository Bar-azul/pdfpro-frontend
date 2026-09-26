# PDFPro frontend

Static site for https://www.pdfproapp.com, deployed on Vercel. Backend: `Bar-azul/PdfPro` (FastAPI on Render).

## How the site is built

**`build.py` is the only build script.** Edit content there and run:

    python build.py

It regenerates every tool page, static page, blog page (EN + HE), `sitemap.xml` and `robots.txt`,
then checks every internal link. Never edit generated `index.html` files by hand — the next build overwrites them.

| What | Where |
|---|---|
| Tool pages (title, steps, FAQ, API config) | `TOOLS` in `build.py` |
| Tool page long content | `content/tools/<en|he>/<slug>.html` (optional) |
| About / Contact / Pricing / Help / Privacy / Terms | `static_pages()` in `build.py` |
| Article metadata | `ARTICLES` in `build.py` |
| Article body | `content/blog/<en|he>/<slug>.html` |
| Styles / shared JS / tool uploader | `assets/site.css`, `assets/site.js`, `assets/tool.js` |
| Homepages | `index.html`, `he/index.html` — **hand-maintained**, not generated (yet) |

## Adding an article
1. Add an entry to `ARTICLES` (slug, date, related tool, EN/HE title + description).
2. Create `content/blog/en/<slug>.html` and `content/blog/he/<slug>.html` (body only, starting with `<p class="lead">`).
3. `python build.py`, commit, push.

`.vercelignore` keeps `build.py`, `content/` and the manifest off the public site.
