# -*- coding: utf-8 -*-
import os

GTAG_SNIPPET = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-WJ3VYWT5RY"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag("js", new Date());
  gtag("config", "G-WJ3VYWT5RY");
</script>"""


SHARED_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
:root{
  --red:#E02020;--red-dark:#C41A1A;--red-light:#FF4444;
  --navy:#0D1B2A;--navy-light:#162333;--cream:#F8F5F0;
  --border:#D8D0C4;--text:#0D1B2A;--muted:#5A6A7A;--white:#FFFFFF;
}
body{font-family:'Plus Jakarta Sans',sans-serif;background:var(--cream);color:var(--text);direction:ltr}
nav{background:var(--navy);padding:0 3rem;height:68px;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:100;border-bottom:2px solid var(--red);width:100%;box-sizing:border-box}
.logo{font-size:1.6rem;font-weight:900;color:var(--white);letter-spacing:-0.5px;text-decoration:none;white-space:nowrap}
.logo span{color:var(--red-light)}
.nav-links{display:flex;align-items:center;gap:2rem;list-style:none;margin:0;padding:0}
.nav-links li{list-style:none;margin:0;padding:0}
.nav-links a{color:rgba(255,255,255,0.75);text-decoration:none;font-size:0.95rem;font-weight:500;transition:color 0.2s;white-space:nowrap}
.nav-links a:hover{color:var(--white)}
.nav-right{display:flex;align-items:center;gap:0.8rem}
.nav-cta{background:var(--red);color:var(--white);padding:0.55rem 1.4rem;border-radius:6px;font-weight:700;font-size:0.9rem;border:none;cursor:pointer;transition:background 0.2s;text-decoration:none;display:inline-flex;align-items:center;justify-content:center;white-space:nowrap}
.nav-cta:hover{background:var(--red-dark)}
.api-status{display:inline-flex;align-items:center;gap:0.4rem;font-size:0.78rem;font-weight:600;padding:0.25rem 0.7rem;border-radius:20px;white-space:nowrap}
.api-status.offline{background:rgba(239,68,68,0.15);color:#ef4444}
.api-dot{width:6px;height:6px;border-radius:50%;background:currentColor}
footer{background:var(--navy);padding:3rem;border-top:2px solid rgba(255,255,255,0.06);width:100%;box-sizing:border-box;margin-top:4rem}
.footer-inner{max-width:1100px;margin:0 auto;display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:3rem;align-items:start}
.footer-brand p{font-size:0.85rem;color:rgba(255,255,255,0.4);line-height:1.6;margin-top:0.8rem}
.footer-col h4{font-size:0.85rem;font-weight:700;color:rgba(255,255,255,0.5);text-transform:uppercase;letter-spacing:1px;margin-bottom:1rem}
.footer-col ul{list-style:none;margin:0;padding:0}
.footer-col ul li{margin-bottom:0.6rem}
.footer-col ul li a{color:rgba(255,255,255,0.6);text-decoration:none;font-size:0.88rem;transition:color 0.2s}
.footer-col ul li a:hover{color:var(--white)}
.footer-language{margin-top:1rem}
.footer-language label{display:block;color:rgba(255,255,255,0.5);font-size:0.85rem;margin-bottom:0.4rem}
.footer-language select{width:190px;max-width:100%;padding:0.55rem 0.8rem;border-radius:8px;border:1px solid rgba(255,255,255,0.2);background:var(--navy-light);color:var(--white);font-size:0.9rem;cursor:pointer}
.footer-bottom{max-width:1100px;margin:2rem auto 0;padding-top:1.5rem;border-top:1px solid rgba(255,255,255,0.08);display:flex;justify-content:space-between;color:rgba(255,255,255,0.3);font-size:0.82rem;flex-wrap:wrap;gap:1rem}
.container{max-width:760px;margin:0 auto;padding:3rem 1.5rem}
h1{font-size:1.9rem;font-weight:900;color:var(--navy);margin-bottom:1rem;letter-spacing:-0.5px;line-height:1.3}
h2{font-size:1.2rem;font-weight:700;color:var(--navy);margin:1.8rem 0 0.6rem}
h3{font-size:1rem;font-weight:700;color:var(--navy);margin-bottom:0.4rem}
p{color:var(--muted);line-height:1.85;margin-bottom:0.9rem}
.lead{font-size:1.05rem;line-height:1.85;margin-bottom:1.5rem;color:var(--text)}
ul.article-list{margin:0 0 1rem 1.3rem;padding:0;color:var(--muted);line-height:1.9}
ul.article-list li{margin-bottom:0.4rem}
.card{background:white;border-radius:12px;border:1px solid var(--border);padding:1.4rem;margin-bottom:1rem}
.cta{display:inline-block;background:var(--red);color:white;padding:0.8rem 2rem;border-radius:8px;text-decoration:none;font-weight:700;margin-top:1rem;transition:background 0.2s}
.cta:hover{background:var(--red-dark)}
.breadcrumb{font-size:0.85rem;color:var(--muted);margin-bottom:1.5rem}
.breadcrumb a{color:var(--muted);text-decoration:none}
.breadcrumb a:hover{color:var(--red)}
.breadcrumb span{color:var(--navy);font-weight:600}
.meta{font-size:0.82rem;color:var(--muted);margin-bottom:1.5rem}
.tag{display:inline-block;background:rgba(224,32,32,0.08);color:var(--red);font-size:0.75rem;font-weight:700;padding:0.2rem 0.6rem;border-radius:4px;margin-bottom:0.8rem}
@media(max-width:768px){
  nav{padding:0 1rem;height:56px}
  .nav-links{display:none}
  .logo{font-size:1.3rem}
  .nav-cta{padding:0.45rem 1rem;font-size:0.82rem}
  #api-status{display:none}
  footer{padding:2rem 1rem}
  .footer-inner{grid-template-columns:1fr;gap:1.5rem}
  .footer-bottom{flex-direction:column;align-items:center;text-align:center}
  .container{padding:2rem 1rem}
  h1{font-size:1.5rem}
}
"""

LANG_JS = """
const LANGUAGE_PREFIXES = ['he'];
function getCurrentLanguageFromPath(){const p=window.location.pathname;if(p==='/he'||p==='/he/'||p.startsWith('/he/'))return 'he';return 'en';}
function getPathWithoutLanguagePrefix(p){for(const pre of LANGUAGE_PREFIXES){if(p===`/${pre}`||p===`/${pre}/`)return '/';if(p.startsWith(`/${pre}/`))return p.replace(`/${pre}`,'')||'/';}return p||'/';}
function buildLocalizedPath(t){const c=getPathWithoutLanguagePrefix(window.location.pathname);if(t==='en')return c;if(c==='/')return `/${t}/`;return `/${t}${c}`;}
function changeSiteLanguage(t){localStorage.setItem('pdfpro_lang',t);window.location.href=buildLocalizedPath(t);}
function setCurrentFooterLanguage(){const s=document.getElementById('footer-lang');if(!s)return;s.value=getCurrentLanguageFromPath();}
document.addEventListener('DOMContentLoaded',setCurrentFooterLanguage);
"""

NAV = """<nav>
  <a href="/" class="logo">PDF<span>Pro</span></a>
  <ul class="nav-links">
    <li><a href="/#tools">Tools</a></li>
    <li><a href="/#features">Features</a></li>
    <li><a href="/pricing/">Pricing</a></li>
  </ul>
  <div class="nav-right">
    <span class="api-status offline" id="api-status"><span class="api-dot"></span><span id="api-status-text">Connecting...</span></span>
    <a class="nav-cta" href="/#tools">Get Started</a>
  </div>
</nav>"""

FOOTER = """<footer>
  <div class="footer-inner">
    <div class="footer-brand">
      <a href="/" class="logo">PDF<span>Pro</span></a>
      <p>The leading platform for PDF processing — fast, secure and professional.</p>
      <div class="footer-language">
        <label for="footer-lang">Language</label>
        <select id="footer-lang" onchange="changeSiteLanguage(this.value)">
          <option value="en" selected>English</option>
          <option value="he">עברית</option>
        </select>
      </div>
    </div>
    <div class="footer-col"><h4>Tools</h4><ul>
      <li><a href="/pdf-to-word/">PDF to Word</a></li>
      <li><a href="/merge-pdf/">Merge PDF</a></li>
      <li><a href="/compress-pdf/">Compress PDF</a></li>
      <li><a href="/ocr-pdf/">OCR</a></li>
    </ul></div>
    <div class="footer-col"><h4>Company</h4><ul>
      <li><a href="/about/">About</a></li>
      <li><a href="/blog/">Blog</a></li>
      <li><a href="/contact/">Contact</a></li>
    </ul></div>
    <div class="footer-col"><h4>Support</h4><ul>
      <li><a href="/help/">Help Center</a></li>
      <li><a href="/privacy/">Privacy Policy</a></li>
      <li><a href="/terms/">Terms of Use</a></li>
    </ul></div>
  </div>
  <div class="footer-bottom"><span>© 2026 PDFPro. All rights reserved.</span><span>🌍 Made with ❤️</span></div>
</footer>"""


def build_article(slug, title, description, date, tag, tool_link, tool_label, body_html):
    en_canonical = f"https://www.pdfproapp.com/blog/{slug}/"
    he_canonical = f"https://www.pdfproapp.com/he/blog/{slug}/"
    return f"""<!DOCTYPE html>
<html id="html-root" lang="en" dir="ltr">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<meta name="description" content="{description}">
<title>{title} | PDFPro</title>
<link rel="canonical" href="{en_canonical}">
<link rel="alternate" hreflang="en" href="{en_canonical}">
<link rel="alternate" hreflang="he" href="{he_canonical}">
<link rel="alternate" hreflang="x-default" href="{en_canonical}">
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;600;700;800&family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet"/>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5792951933667466" crossorigin="anonymous"></script>
{GTAG_SNIPPET}
<style>{SHARED_CSS}</style>
</head>
<body>
{NAV}
<div class="container">
  <div class="breadcrumb"><a href="/">Home</a> › <a href="/blog/">Blog</a> › <span>{title}</span></div>
  <span class="tag">{tag}</span>
  <h1>{title}</h1>
  <p class="meta">{date}</p>
  {body_html}
  <div class="card" style="text-align:center;margin-top:2rem">
    <p style="color:var(--navy);font-weight:700;margin-bottom:0.6rem">Want to try it yourself?</p>
    <a href="{tool_link}" class="cta">{tool_label}</a>
  </div>
</div>
{FOOTER}
<script>{LANG_JS}</script>
</body>
</html>
"""


ARTICLES = []

# ── 1. RTL text issues ──────────────────────────────────────────
ARTICLES.append(dict(
    slug="pdf-hebrew-rtl",
    title="Why Hebrew or Arabic Text Gets Scrambled After PDF Conversion (And How to Fix It)",
    description="A full explanation of RTL (right-to-left) text issues in PDF conversion, why it happens, and how to pick a tool that actually handles it correctly.",
    date="July 1, 2026", sort_date="2026-07-01",
    tag="Conversion",
    tool_link="/pdf-to-word/",
    tool_label="Convert PDF to Word Now",
    body_html="""
<p class="lead">If you've ever converted a PDF containing Hebrew or Arabic text and gotten back scrambled, reversed, or nonsensically ordered text — you're not alone. This is one of the most common issues in document conversion, and it almost always comes down to one technical cause.</p>

<h2>What causes the problem?</h2>
<p>Hebrew and Arabic are <strong>RTL</strong> (right-to-left) languages, while most conversion engines were originally built around English, an <strong>LTR</strong> (left-to-right) language. When a conversion engine isn't properly built to handle mixed directionality, a few typical things happen:</p>
<ul class="article-list">
  <li>Character order gets reversed — whole words appear "scrambled" backwards</li>
  <li>Numbers and dates inside RTL sentences get flipped incorrectly</li>
  <li>Mixed Hebrew/Arabic-English paragraphs lose their correct order</li>
  <li>Text alignment ends up reversed — stuck to the left instead of the right</li>
</ul>

<h2>Why does this happen mainly with PDF conversion?</h2>
<p>Unlike Word, PDF doesn't store text as "logical text" with defined directionality — it mainly stores the <strong>visual position</strong> of each character on the page. When converting back to an editable format, the engine has to reconstruct the correct directionality purely from visual position. If it isn't specifically built to detect and correct RTL, it simply copies character order as it appears on the page, and you get a mess.</p>

<h2>How to actually fix this</h2>
<p><strong>1. Check that the engine officially supports RTL</strong>, not just "supports Hebrew fonts." There's a big difference between a tool that can display Hebrew characters and one that truly understands text directionality — real RTL support includes automatic paragraph direction detection, correct handling of numbers inside RTL sentences, and proper handling of mixed paragraphs.</p>
<p><strong>2. If the document is scanned</strong> (not digital text), run it through OCR that explicitly supports Hebrew or Arabic first (look for "heb" or "ara" language options, not just "eng").</p>
<p><strong>3. After conversion, always check a paragraph containing numbers or English terms.</strong> This is the most reliable test — if a sentence like "The payment is 250 shekels per month via PayPal" comes out correctly, the engine likely handled RTL properly.</p>

<h2>What if the conversion already came out reversed?</h2>
<p>In most cases, manually fixing reversed text isn't worth it — it's slow and error-prone for long documents. It's almost always faster to reconvert using a tool built with proper RTL support from the start.</p>
"""
))

# ── 2. Electronic signature ───────────────────────────────────
ARTICLES.append(dict(
    slug="electronic-signature-pdf",
    title="How to Sign a PDF Document Without Printing It",
    description="A complete guide to electronically signing PDF documents — no printer, scanner, or wasted time required.",
    date="July 3, 2026", sort_date="2026-07-03",
    tag="Signature",
    tool_link="/pdf-to-word/",
    tool_label="Try Signing a Document",
    body_html="""
<p class="lead">"Print it, sign it, scan it, send it back" — the traditional signing process takes anywhere from several minutes to half an hour and requires access to a printer and scanner. Electronic signing does the same thing in seconds, directly from your computer or phone.</p>

<h2>What's the difference between an "electronic signature" and a "digital signature"?</h2>
<p>An <strong>electronic signature</strong> is essentially adding a visual representation of a signature (a scanned handwritten signature, styled text, or a mouse/finger-drawn signature) into the document. This is sufficient for most everyday documents — lease agreements, forms, internal approvals.</p>
<p>A <strong>secure digital signature</strong> (with a digital certificate) also adds an encryption layer that legally proves the signer is who they claim to be, and that the document wasn't altered after signing. This is typically required for legally binding contracts, government filings, or high-value transactions.</p>

<h2>What to watch for with RTL documents</h2>
<p>An important note if you work with Hebrew or Arabic documents: a signing tool that doesn't properly support RTL can place the signature in the wrong spot on the page, especially in documents where text is right-aligned. Always make sure the tool shows a live preview before final saving, so you can confirm the signature sits exactly where it should.</p>

<h2>The process, step by step</h2>
<p><strong>1. Upload the document</strong> — the existing PDF that needs a signature.</p>
<p><strong>2. Add the signature</strong> — type your full name as styled text, or draw it manually with a mouse or touchscreen.</p>
<p><strong>3. Precise placement</strong> — drag the signature to the correct spot on the page.</p>
<p><strong>4. Download or send</strong> — save the signed document and send it directly from the browser.</p>

<h2>When do you need a secure digital signature instead of just a visual one?</h2>
<p>If the document is a contract with significant legal consequences, it's worth checking with a legal professional whether a secure digital signature with a recognized certificate is required, rather than relying on a visual signature alone.</p>
"""
))

# ── 3. Password protected PDF (educational only) ──────────────
ARTICLES.append(dict(
    slug="pdf-password-protected",
    title="Password-Protected PDF: What to Do When You've Lost the Password",
    description="What to do when you've lost the password to your own PDF file — legitimate options only.",
    date="July 5, 2026", sort_date="2026-07-05",
    tag="Security",
    tool_link="/contact/",
    tool_label="Contact Us for Help",
    body_html="""
<p class="lead">Losing the password to an important PDF — a contract, a payslip, an official document — is a frustrating and common situation. Important note up front: this article covers only situations where you are the legitimate owner of the document, not bypassing protection on files that aren't yours.</p>

<h2>First — do you actually need to open it yourself?</h2>
<p>Before trying any technical solution, check the simplest option first: <strong>contact whoever sent you the file</strong> and ask for the password again, or request a fresh copy without protection. In many cases this is the fastest and safest solution, with zero risk involved.</p>

<h2>What if it's your own document and you lost your own password?</h2>
<p>If it's a document you created or protected yourself (for example, a report you password-protected and then forgot the password):</p>
<p><strong>1. Check your password manager</strong> — if the document is recent, the password may have been saved automatically in your browser or password manager.</p>
<p><strong>2. Check for earlier versions</strong> — if the document was created from Word or another program, an unprotected copy may still exist in an earlier version in your backups or in Google Drive/OneDrive.</p>
<p><strong>3. Contact support for the software that created the file</strong> — if the document was generated by an organizational system (like a payroll or banking system), that system can usually reissue the document unprotected if you contact them directly.</p>

<h2>Why not just try to "crack" the password?</h2>
<p>Tools that promise to "break" PDF passwords are often unreliable (and sometimes contain malware). Beyond that, if the document isn't yours, attempting to bypass its protection can be legally problematic. The safe and correct path always runs through contacting the document's legal owner.</p>

<h2>After you've successfully opened the document</h2>
<p>If you want to remove the protection so you can access your document more easily going forward, make sure you only do this with documents that actually belong to you, and store the new unprotected version somewhere secure (a password manager, encrypted storage).</p>
"""
))

# ── 4. Broken PDF on mobile ────────────────────────────────────
ARTICLES.append(dict(
    slug="pdf-broken-mobile",
    title="5 Mistakes That Make Your PDF Look Broken on Mobile",
    description="The most common reasons PDF files look broken, cut off, or unreadable on a mobile phone.",
    date="July 7, 2026", sort_date="2026-07-07",
    tag="Compatibility",
    tool_link="/compress-pdf/",
    tool_label="Compress a PDF Now",
    body_html="""
<p class="lead">You sent a PDF that looked perfect on your computer, but when a client or your boss opened it on their phone — the text was cut off, images wouldn't load, or everything looked misaligned. Here are the five most common causes, and how to avoid each one.</p>

<h2>1. Non-standard page size</h2>
<p>Documents created for print (like A3 or poster formats) often don't load correctly in mobile PDF apps that expect a standard aspect ratio. Fix: before sending, make sure the document uses standard A4 or Letter size unless there's a specific reason not to.</p>

<h2>2. Fonts that aren't embedded</h2>
<p>If the font used in the document isn't "embedded" inside the PDF file itself, other devices (including phones) substitute a default font — which shifts the entire layout and makes it look broken. Most creation tools (Word, Google Docs) embed fonts automatically on export to PDF, but it's worth double-checking in the export settings.</p>

<h2>3. Files that are too heavy</h2>
<p>A PDF with overly high-resolution images (for example, scans at 600 DPI when 150 would be enough) can take a long time to load on mobile, and on a weak connection may get stuck loading or appear only partially. Compressing the file almost always fixes this without meaningfully hurting readability.</p>

<h2>4. Broken OCR text layers</h2>
<p>If a document went through poor-quality OCR (automatic text recognition), it can create a "text layer" underneath the image that's misaligned — so when you try to copy text or search within the document on mobile, you get strange results or the view "jumps." The fix is to reprocess the document with a high-quality OCR engine rather than living with it.</p>

<h2>5. Incorrect RTL directionality in bilingual documents</h2>
<p>A document created in software that doesn't properly support RTL languages like Hebrew or Arabic can look fine on desktop (thanks to OS-level auto-correction) but fall apart on mobile, especially in simpler PDF apps. For a full breakdown of this issue and how to fix it, see our guide on <a href="/blog/pdf-hebrew-rtl/" style="color:var(--red)">RTL text in PDF conversion</a>.</p>

<h2>How to prevent all of this in advance</h2>
<p>The most reliable rule: after creating or converting any important PDF, open it once on your phone (not just your computer) before sending it. It takes ten seconds and saves a lot of embarrassment.</p>
"""
))

# ── 5. Compress ID/contract without hurting signature readability ──
ARTICLES.append(dict(
    slug="compress-id-contract-pdf",
    title="How to Compress an ID or Contract PDF Without Losing Signature Clarity",
    description="A guide to compressing sensitive documents like ID cards and signed contracts while keeping text and signatures fully legible.",
    date="July 8, 2026", sort_date="2026-07-08",
    tag="Compression",
    tool_link="/compress-pdf/",
    tool_label="Compress a PDF Now",
    body_html="""
<p class="lead">When it comes to sensitive documents like an ID card, a signed contract, or a bank statement, there's a delicate balance: the file needs to be small enough to email or upload, but still clear enough that every digit is readable and the signature is clearly identifiable.</p>

<h2>Why "regular" compression is risky for these documents</h2>
<p>Overly aggressive compression (like "Extreme" settings in general-purpose compression tools) mainly reduces image quality — which can turn ID numbers blurry or make signature lines unclear. In a regular document that's less critical; in a document that needs precise identification, it's a real problem.</p>

<h2>What's the right compression level for sensitive documents?</h2>
<p><strong>Low-to-medium compression is the safe choice.</strong> Most compression tools offer several levels (low, medium, high, extreme) — low compression keeps nearly all of the original quality while reducing file size by only 10-30%, which in most cases is enough to get under common upload limits (like 5MB or 10MB) without hurting readability.</p>

<h2>A check you shouldn't skip after compressing</h2>
<p>After compressing any sensitive document, it's always worth:</p>
<p><strong>1. Zooming in on ID numbers</strong> — confirm every digit is sharp and unblurred.</p>
<p><strong>2. Zooming in on the signature area</strong> — confirm the signature lines are still crisp and clearly identifiable if verification is ever needed.</p>
<p><strong>3. Comparing file size before and after</strong> — if the file dropped significantly but still looks correct when zoomed in, that's a good sign the compression worked well.</p>

<h2>What if the file is still too large after light compression?</h2>
<p>If the file still exceeds an upload limit after low-level compression, before jumping to a higher compression level that might hurt quality, check whether there are unnecessary pages you can remove, or whether splitting into multiple smaller files instead of one large one makes more sense. Both preserve full quality without compromise.</p>
"""
))

LEGACY_CARDS_EN = """
  <div class="blog-card" onclick="window.location.href='/compress-pdf/'">
    <p class="blog-date">May 20, 2026</p>
    <span class="tag">Compression</span>
    <h2>How to reduce PDF file size without losing quality</h2>
    <p>Learn the best strategies for compressing PDFs while maintaining readability and visual quality.</p>
    <p style="color:var(--red);font-size:0.85rem;font-weight:600;margin-top:0.8rem">Try the tool &rarr;</p>
  </div>
  <div class="blog-card" onclick="window.location.href='/ocr-pdf/'">
    <p class="blog-date">May 15, 2026</p>
    <span class="tag">OCR</span>
    <h2>OCR for Hebrew documents: a complete guide</h2>
    <p>Everything you need to know about extracting Hebrew text from scanned documents and images.</p>
    <p style="color:var(--red);font-size:0.85rem;font-weight:600;margin-top:0.8rem">Try the tool &rarr;</p>
  </div>
  <div class="blog-card" onclick="window.location.href='/pdf-to-word/'">
    <p class="blog-date">May 8, 2026</p>
    <span class="tag">Conversion</span>
    <h2>PDF to Word: when it works and when it doesn't</h2>
    <p>Understanding the limitations of PDF conversion and how to get the best results every time.</p>
    <p style="color:var(--red);font-size:0.85rem;font-weight:600;margin-top:0.8rem">Try the tool &rarr;</p>
  </div>
"""

BLOG_INDEX_TEMPLATE_EN = """<!DOCTYPE html>
<html id="html-root" lang="en" dir="ltr">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<meta name="description" content="Tips, tutorials and updates from the PDFPro team.">
<title>Blog | PDFPro</title>
<link rel="canonical" href="https://www.pdfproapp.com/blog/">
<link rel="alternate" hreflang="en" href="https://www.pdfproapp.com/blog/">
<link rel="alternate" hreflang="he" href="https://www.pdfproapp.com/he/blog/">
<link rel="alternate" hreflang="x-default" href="https://www.pdfproapp.com/blog/">
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;600;700;800&family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet"/>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5792951933667466" crossorigin="anonymous"></script>
{GTAG_SNIPPET}
<style>{css}</style>
</head>
<body>
{nav}
<div class="container">
  <div class="breadcrumb"><a href="/">Home</a> › <span>Blog</span></div>
  <h1>Blog</h1>
  <p class="lead">Tips, tutorials and updates from the PDFPro team.</p>
{cards}
</div>
{footer}
<script>{js}</script>
</body>
</html>
"""

BLOG_NAV_EN = """<nav>
  <a href="/" class="logo">PDF<span>Pro</span></a>
  <ul class="nav-links">
    <li><a href="/#tools">Tools</a></li>
    <li><a href="/#features">Features</a></li>
    <li><a href="/pricing/">Pricing</a></li>
  </ul>
  <div class="nav-right">
    <span class="api-status offline" id="api-status"><span class="api-dot"></span><span id="api-status-text">Connecting...</span></span>
    <a class="nav-cta" href="/#tools">Get Started</a>
  </div>
</nav>"""

BLOG_CARD_CSS_EXTRA = """
.container{max-width:860px;margin:0 auto;padding:3rem 1.5rem}
h1{font-size:2rem;font-weight:900;color:var(--navy);margin-bottom:1rem;letter-spacing:-0.5px}
.lead{font-size:1.05rem;line-height:1.8;margin-bottom:1.5rem}
.blog-card{background:white;border-radius:12px;border:1px solid var(--border);padding:1.5rem;margin-bottom:1rem;cursor:pointer;transition:border-color 0.2s,box-shadow 0.2s}
.blog-card:hover{border-color:var(--red);box-shadow:0 4px 16px rgba(224,32,32,0.08)}
.blog-card .blog-date{font-size:0.78rem;color:var(--muted)}
.blog-card h2{margin-top:0.4rem;font-size:1.05rem;margin-bottom:0;color:var(--navy);font-weight:700}
.blog-card p{font-size:0.88rem}
"""


def build_blog_index_en(articles):
    sorted_articles = sorted(articles, key=lambda a: a["sort_date"], reverse=True)
    cards = ""
    for art in sorted_articles:
        cards += f"""
  <div class="blog-card" onclick="window.location.href='/blog/{art['slug']}/'">
    <p class="blog-date">{art['date']}</p>
    <span class="tag">{art['tag']}</span>
    <h2>{art['title']}</h2>
    <p>{art['description']}</p>
    <p style="color:var(--red);font-size:0.85rem;font-weight:600;margin-top:0.8rem">Read more &rarr;</p>
  </div>"""
    cards += LEGACY_CARDS_EN
    return BLOG_INDEX_TEMPLATE_EN.format(
        css=SHARED_CSS + BLOG_CARD_CSS_EXTRA,
        nav=BLOG_NAV_EN,
        cards=cards,
        footer=FOOTER,
        js=LANG_JS,
        GTAG_SNIPPET=GTAG_SNIPPET,
    )


for art in ARTICLES:
    html = build_article(
        slug=art["slug"], title=art["title"], description=art["description"],
        date=art["date"], tag=art["tag"], tool_link=art["tool_link"],
        tool_label=art["tool_label"], body_html=art["body_html"]
    )
    out_dir = f"blog/{art['slug']}"
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✓ blog/{art['slug']}/index.html (EN)")

# Auto-build the blog listing page
os.makedirs("blog", exist_ok=True)
with open("blog/index.html", "w", encoding="utf-8") as f:
    f.write(build_blog_index_en(ARTICLES))
print("✓ blog/index.html (auto-generated listing, EN)")

# Print sitemap lines to copy into sitemap.xml
print("\n--- Add these lines to sitemap.xml (English articles) ---")
for art in sorted(ARTICLES, key=lambda a: a["sort_date"], reverse=True):
    print(f'  <url><loc>https://www.pdfproapp.com/blog/{art["slug"]}/</loc><priority>0.6</priority></url>')

print("\nDone.")