#!/usr/bin/env python3
"""
PDFPro - Generate all pages with consistent header/footer and correct routing.
Run from the root of your frontend folder.
"""
import os

# ─────────────────────────────────────────────────────────
# SHARED CSS (header + footer + base styles)
# ─────────────────────────────────────────────────────────
SHARED_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
:root{
  --red:#E02020;
  --red-dark:#C41A1A;
  --red-light:#FF4444;
  --navy:#0D1B2A;
  --navy-light:#162333;
  --cream:#F8F5F0;
  --border:#D8D0C4;
  --text:#0D1B2A;
  --muted:#5A6A7A;
  --white:#FFFFFF;
}
body{font-family:'Plus Jakarta Sans',sans-serif;background:var(--cream);color:var(--text);direction:ltr}
body.rtl{direction:rtl;font-family:'Heebo',sans-serif}

/* ── NAV ── */
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
  font-size:1.6rem;font-weight:900;color:var(--white);
  letter-spacing:-0.5px;text-decoration:none;white-space:nowrap;
}
.logo span{color:var(--red-light)}
.nav-links{display:flex;align-items:center;gap:2rem;list-style:none;margin:0;padding:0}
.nav-links li{list-style:none;margin:0;padding:0}
.nav-links a{
  color:rgba(255,255,255,0.75);text-decoration:none;
  font-size:0.95rem;font-weight:500;transition:color 0.2s;white-space:nowrap;
}
.nav-links a:hover,.nav-links a.active{color:var(--white)}
.nav-right{display:flex;align-items:center;gap:0.8rem}
.nav-cta{
  background:var(--red);color:var(--white);
  padding:0.55rem 1.4rem;border-radius:6px;
  font-weight:700;font-size:0.9rem;border:none;cursor:pointer;
  transition:background 0.2s;text-decoration:none;
  display:inline-flex;align-items:center;justify-content:center;white-space:nowrap;
}
.nav-cta:hover{background:var(--red-dark)}
.api-status{
  display:inline-flex;align-items:center;gap:0.4rem;
  font-size:0.78rem;font-weight:600;
  padding:0.25rem 0.7rem;border-radius:20px;white-space:nowrap;
}
.api-status.online{background:rgba(34,197,94,0.15);color:#22c55e}
.api-status.offline{background:rgba(239,68,68,0.15);color:#ef4444}
.api-dot{width:6px;height:6px;border-radius:50%;background:currentColor}

/* ── FOOTER ── */
footer{
  background:var(--navy);padding:3rem;
  border-top:2px solid rgba(255,255,255,0.06);
  width:100%;box-sizing:border-box;margin-top:4rem;
}
.footer-inner{
  max-width:1100px;margin:0 auto;
  display:grid;grid-template-columns:2fr 1fr 1fr 1fr;
  gap:3rem;align-items:start;
}
.footer-brand p{font-size:0.85rem;color:rgba(255,255,255,0.4);line-height:1.6;margin-top:0.8rem}
.footer-col h4{
  font-size:0.85rem;font-weight:700;color:rgba(255,255,255,0.5);
  text-transform:uppercase;letter-spacing:1px;margin-bottom:1rem;
}
body.rtl .footer-col h4{letter-spacing:0}
.footer-col ul{list-style:none;margin:0;padding:0}
.footer-col ul li{margin-bottom:0.6rem}
.footer-col ul li a{color:rgba(255,255,255,0.6);text-decoration:none;font-size:0.88rem;transition:color 0.2s}
.footer-col ul li a:hover{color:var(--white)}
.footer-language{margin-top:1rem}
.footer-language label{display:block;color:rgba(255,255,255,0.5);font-size:0.85rem;margin-bottom:0.4rem}
.footer-language select{
  width:190px;max-width:100%;padding:0.55rem 0.8rem;
  border-radius:8px;border:1px solid rgba(255,255,255,0.2);
  background:var(--navy-light);color:var(--white);font-size:0.9rem;cursor:pointer;
}
.footer-bottom{
  max-width:1100px;margin:2rem auto 0;padding-top:1.5rem;
  border-top:1px solid rgba(255,255,255,0.08);
  display:flex;justify-content:space-between;
  color:rgba(255,255,255,0.3);font-size:0.82rem;flex-wrap:wrap;gap:1rem;
}

/* ── PAGE CONTENT ── */
.container{max-width:860px;margin:0 auto;padding:3rem 1.5rem}
h1{font-size:2rem;font-weight:900;color:var(--navy);margin-bottom:1rem;letter-spacing:-0.5px}
h2{font-size:1.2rem;font-weight:700;color:var(--navy);margin:1.8rem 0 0.6rem}
h3{font-size:1rem;font-weight:700;color:var(--navy);margin-bottom:0.4rem}
p{color:var(--muted);line-height:1.8;margin-bottom:0.8rem}
.lead{font-size:1.05rem;line-height:1.8;margin-bottom:1.5rem}
.card{background:white;border-radius:12px;border:1px solid var(--border);padding:1.4rem;margin-bottom:0.8rem}
.grid-2{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:1.5rem}
.grid-3{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-bottom:1.5rem}
.cta{display:inline-block;background:var(--red);color:white;padding:0.8rem 2rem;border-radius:8px;text-decoration:none;font-weight:700;margin-top:1rem;transition:background 0.2s}
.cta:hover{background:var(--red-dark)}
details{border:1px solid var(--border);border-radius:10px;padding:1rem 1.2rem;margin-bottom:0.8rem;background:white}
summary{font-weight:700;cursor:pointer;color:var(--navy);list-style:none;display:flex;justify-content:space-between}
summary::-webkit-details-marker{display:none}
details p{margin-top:0.8rem}
input,textarea,select{
  width:100%;padding:0.75rem 1rem;border-radius:8px;
  border:1px solid var(--border);font-family:'Plus Jakarta Sans',sans-serif;
  font-size:0.95rem;margin-bottom:0.8rem;background:white;direction:ltr;
  color:var(--text);
}
.send-btn{
  background:var(--red);color:white;border:none;border-radius:8px;
  padding:0.85rem 2rem;font-size:1rem;font-weight:700;cursor:pointer;width:100%;
  transition:background 0.2s;
}
.send-btn:hover{background:var(--red-dark)}
.blog-card{background:white;border-radius:12px;border:1px solid var(--border);padding:1.5rem;margin-bottom:1rem;cursor:pointer;transition:border-color 0.2s,box-shadow 0.2s}
.blog-card:hover{border-color:var(--red);box-shadow:0 4px 16px rgba(224,32,32,0.08)}
.blog-card .blog-date{font-size:0.78rem;color:var(--muted)}
.blog-card h2{margin-top:0.4rem;font-size:1.05rem;margin-bottom:0}
.blog-card p{font-size:0.88rem}
.tag{display:inline-block;background:rgba(224,32,32,0.08);color:var(--red);font-size:0.75rem;font-weight:700;padding:0.2rem 0.6rem;border-radius:4px;margin-bottom:0.6rem}
.upload-zone{
  border:2px dashed var(--border);border-radius:12px;padding:3rem;
  text-align:center;background:white;transition:border-color 0.2s;cursor:pointer;
}
.upload-zone:hover{border-color:var(--red)}
.upload-zone p{margin:0}
.upload-icon{font-size:2.5rem;margin-bottom:1rem;display:block}
.price-card{background:white;border-radius:16px;border:1px solid var(--border);padding:2rem;text-align:center}
.price-card.featured{border-color:var(--red);box-shadow:0 8px 32px rgba(224,32,32,0.12)}
.price-card .price{font-size:2.5rem;font-weight:900;color:var(--navy)}
.price-card .period{font-size:0.9rem;color:var(--muted);font-weight:400}
.price-card ul{list-style:none;margin:1.5rem 0;padding:0;text-align:left}
.price-card ul li{padding:0.4rem 0;color:var(--muted);font-size:0.9rem;display:flex;gap:0.5rem;align-items:flex-start}
.price-card ul li::before{content:"✓";color:#22c55e;font-weight:700;flex-shrink:0}
.breadcrumb{font-size:0.85rem;color:var(--muted);margin-bottom:1.5rem}
.breadcrumb a{color:var(--muted);text-decoration:none}
.breadcrumb a:hover{color:var(--red)}
.breadcrumb span{color:var(--navy);font-weight:600}

@media(max-width:768px){
  nav{padding:0 1rem;height:56px}
  .nav-links{display:none}
  .logo{font-size:1.3rem}
  .nav-cta{padding:0.45rem 1rem;font-size:0.82rem}
  #api-status{display:none}
  footer{padding:2rem 1rem}
  .footer-inner{grid-template-columns:1fr;gap:1.5rem}
  .footer-bottom{flex-direction:column;align-items:center;text-align:center}
  .grid-2,.grid-3{grid-template-columns:1fr}
  .container{padding:2rem 1rem}
  h1{font-size:1.5rem}
  .price-card{margin-bottom:1rem}
}
"""

# ─────────────────────────────────────────────────────────
# SHARED JS
# ─────────────────────────────────────────────────────────
SHARED_JS = """
function getCurrentSiteLanguage(){
  const path=window.location.pathname;
  if(path==='/he'||path==='/he/'||path.startsWith('/he/')) return 'he';
  return 'en';
}
function removeLanguagePrefix(pathname){
  if(pathname==='/he'||pathname==='/he/') return '/';
  if(pathname.startsWith('/he/')) return pathname.replace('/he','')||'/';
  return pathname||'/';
}
function buildLanguageUrl(targetLang){
  const cleanPath=removeLanguagePrefix(window.location.pathname);
  if(targetLang==='en') return cleanPath;
  if(cleanPath==='/') return '/he/';
  return '/he'+cleanPath;
}
function changeSiteLanguage(targetLang){
  localStorage.setItem('pdfpro_lang',targetLang);
  window.location.href=buildLanguageUrl(targetLang);
}
function setFooterLanguageValue(){
  const select=document.getElementById('footer-lang');
  if(!select) return;
  select.value=getCurrentSiteLanguage();
}
document.addEventListener('DOMContentLoaded',setFooterLanguageValue);
"""

# ─────────────────────────────────────────────────────────
# HEADER template
# ─────────────────────────────────────────────────────────
def make_header(active_page=""):
    links = [
        ("/#tools",    "Tools",    "tools"),
        ("/#features", "Features", "features"),
        ("/pricing/",  "Pricing",  "pricing"),
    ]
    nav_items = "\n    ".join(
        f'<li><a href="{href}" class="{"active" if slug == active_page else ""}">{label}</a></li>'
        for href, label, slug in links
    )
    return f"""<nav>
  <a href="/" class="logo">PDF<span>Pro</span></a>
  <ul class="nav-links">
    {nav_items}
  </ul>
  <div class="nav-right">
    <span class="api-status offline" id="api-status">
      <span class="api-dot"></span>
      <span id="api-status-text">Connecting...</span>
    </span>
    <a class="nav-cta" href="/#tools">Get Started</a>
  </div>
</nav>"""

# ─────────────────────────────────────────────────────────
# FOOTER template
# ─────────────────────────────────────────────────────────
FOOTER = """<footer>
  <div class="footer-inner">
    <div class="footer-brand">
      <a href="/" class="logo">PDF<span>Pro</span></a>
      <p>The leading platform for PDF processing — fast, secure and professional.</p>
      <div class="footer-language">
        <label for="footer-lang">Language</label>
        <select id="footer-lang" onchange="changeSiteLanguage(this.value)">
          <option value="en">English</option>
          <option value="he">עברית</option>
        </select>
      </div>
    </div>
    <div class="footer-col">
      <h4>Tools</h4>
      <ul>
        <li><a href="/pdf-to-word/">PDF to Word</a></li>
        <li><a href="/pdf-to-excel/">PDF to Excel</a></li>
        <li><a href="/compress-pdf/">Compress PDF</a></li>
        <li><a href="/merge-pdf/">Merge PDF</a></li>
        <li><a href="/split-pdf/">Split PDF</a></li>
        <li><a href="/ocr-pdf/">OCR PDF</a></li>
        <li><a href="/translate-pdf/">Translate PDF</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Company</h4>
      <ul>
        <li><a href="/about/">About</a></li>
        <li><a href="/blog/">Blog</a></li>
        <li><a href="/contact/">Contact</a></li>
        <li><a href="/pricing/">Pricing</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Support</h4>
      <ul>
        <li><a href="/help/">Help Center</a></li>
        <li><a href="/privacy/">Privacy Policy</a></li>
        <li><a href="/terms/">Terms of Use</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <span>© 2026 PDFPro. All rights reserved.</span>
    <span>🌍 Made with ❤️</span>
  </div>
</footer>"""

# ─────────────────────────────────────────────────────────
# PAGE BUILDER
# ─────────────────────────────────────────────────────────
def build_page(title, description, canonical_path, active_page, body_content, lang="en"):
    base_url = "https://pdfproapp.com"
    rtl_class = "rtl" if lang == "he" else "ltr"
    direction = "rtl" if lang == "he" else "ltr"
    he_path = f"/he{canonical_path}" if not canonical_path.startswith("/he") else canonical_path
    en_path = canonical_path.replace("/he","") if canonical_path.startswith("/he") else canonical_path
    en_path = en_path or "/"

    canonical_full = base_url + canonical_path
    en_full = base_url + en_path
    he_full = base_url + he_path

    header = make_header(active_page)

    return f"""<!DOCTYPE html>
<html id="html-root" lang="{lang}" dir="{direction}">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<meta name="description" content="{description}">
<title>{title}</title>
<link rel="canonical" href="{canonical_full}">
<link rel="alternate" hreflang="en" href="{en_full}">
<link rel="alternate" hreflang="he" href="{he_full}">
<link rel="alternate" hreflang="x-default" href="{en_full}">
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;600;700;800&family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet"/>
<style>{SHARED_CSS}</style>
</head>
<body class="{rtl_class}">
{header}
{body_content}
{FOOTER}
<script>{SHARED_JS}</script>
</body>
</html>"""


# ─────────────────────────────────────────────────────────
# PAGE CONTENT DEFINITIONS
# ─────────────────────────────────────────────────────────
TOOL_UPLOAD_EN = lambda tool_name, accept, desc: f"""
<div class="container">
  <div class="breadcrumb"><a href="/">Home</a> › <span>{tool_name}</span></div>
  <h1>{tool_name}</h1>
  <p class="lead">{desc}</p>
  <div class="upload-zone" id="drop-zone" onclick="document.getElementById('file-input').click()" ondragover="event.preventDefault()" ondrop="handleDrop(event)">
    <span class="upload-icon">📄</span>
    <p style="font-size:1.1rem;font-weight:700;color:var(--navy);margin-bottom:0.5rem">Drop your PDF here</p>
    <p>or <span style="color:var(--red);font-weight:600;cursor:pointer">browse files</span></p>
    <p style="font-size:0.82rem;margin-top:0.8rem">Supports: {accept} · Max 50MB</p>
    <input type="file" id="file-input" accept="{accept}" style="display:none" onchange="handleFile(this.files[0])">
  </div>
  <div id="result" style="display:none;margin-top:2rem">
    <div class="card" style="text-align:center;padding:2rem">
      <p style="font-size:1.5rem;margin-bottom:0.5rem">✅</p>
      <p style="font-weight:700;color:var(--navy);margin-bottom:0.3rem">File ready!</p>
      <p style="margin-bottom:1rem">Your file has been processed successfully.</p>
      <a href="#" class="cta" id="download-btn">Download Result</a>
    </div>
  </div>
  <div style="margin-top:3rem">
    <h2>How it works</h2>
    <div class="grid-3" style="margin-top:1rem">
      <div class="card"><h3>1. Upload</h3><p>Select or drag your PDF file to get started.</p></div>
      <div class="card"><h3>2. Process</h3><p>Our engine handles everything automatically in seconds.</p></div>
      <div class="card"><h3>3. Download</h3><p>Get your converted file instantly — no sign-up needed.</p></div>
    </div>
  </div>
</div>
<script>
function handleDrop(e){{e.preventDefault();const f=e.dataTransfer.files[0];if(f)handleFile(f);}}
function handleFile(f){{if(!f)return;document.getElementById('result').style.display='block';document.getElementById('download-btn').download=f.name.replace('.pdf','_converted');}}
</script>"""

PAGES = {
    # ── ABOUT ──
    "about/index.html": {
        "title": "About PDFPro",
        "desc": "Learn about PDFPro's mission, story and values.",
        "path": "/about/",
        "active": "",
        "content": """<div class="container">
  <div class="breadcrumb"><a href="/">Home</a> › <span>About</span></div>
  <h1>About PDFPro</h1>
  <p class="lead">PDFPro was founded with a simple mission: make professional PDF tools accessible to everyone, without expensive software or complicated workflows.</p>
  <h2>Our Story</h2>
  <p>We started in 2024 as a small team of developers frustrated with bloated, expensive PDF software. We believed that converting a PDF should take seconds, not require a subscription to a $500/year app.</p>
  <p>Today, over 2 million professionals use PDFPro every month to edit, convert, and manage their documents.</p>
  <h2>Our Values</h2>
  <div class="grid-2">
    <div class="card"><h3>Privacy First</h3><p>Your files are never stored longer than 1 hour. We take data security seriously.</p></div>
    <div class="card"><h3>No Ads</h3><p>We will never show ads or sell your data to third parties.</p></div>
    <div class="card"><h3>Open Source</h3><p>Our core tools are MIT licensed and available on GitHub.</p></div>
    <div class="card"><h3>Fair Pricing</h3><p>Professional tools at prices that work for everyone.</p></div>
  </div>
  <h2>The Team</h2>
  <p>We're a distributed team of engineers, designers, and PDF enthusiasts. We're passionate about making document workflows simpler and faster for everyone.</p>
  <a href="/contact/" class="cta">Get in Touch</a>
</div>"""
    },

    # ── BLOG ──
    "blog/index.html": {
        "title": "Blog | PDFPro",
        "desc": "Tips, tutorials and updates from the PDFPro team.",
        "path": "/blog/",
        "active": "",
        "content": """<div class="container">
  <div class="breadcrumb"><a href="/">Home</a> › <span>Blog</span></div>
  <h1>Blog</h1>
  <p class="lead">Tips, tutorials and updates from the PDFPro team.</p>
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
  <div class="blog-card" onclick="window.location.href='/translate-pdf/'">
    <p class="blog-date">April 30, 2026</p>
    <span class="tag">Translation</span>
    <h2>Translating PDFs: best practices for 2026</h2>
    <p>How to translate complex PDF documents while preserving layout, fonts and formatting.</p>
    <p style="color:var(--red);font-size:0.85rem;font-weight:600;margin-top:0.8rem">Try the tool &rarr;</p>
  </div>
</div>"""
    },

    # ── COMPRESS PDF ──
    "compress-pdf/index.html": {
        "title": "Compress PDF Online | PDFPro",
        "desc": "Reduce PDF file size without losing quality. Fast, free and secure.",
        "path": "/compress-pdf/",
        "active": "tools",
        "content": TOOL_UPLOAD_EN("Compress PDF", ".pdf", "Reduce PDF file size without losing quality. Fast, free, and no sign-up required.")
    },

    # ── CONTACT ──
    "contact/index.html": {
        "title": "Contact Us | PDFPro",
        "desc": "Get in touch with the PDFPro team.",
        "path": "/contact/",
        "active": "",
        "content": """<div class="container">
  <div class="breadcrumb"><a href="/">Home</a> › <span>Contact</span></div>
  <h1>Contact Us</h1>
  <p class="lead">Have a question or feedback? We'd love to hear from you.</p>
  <div class="grid-2" style="margin-bottom:2rem">
    <div class="card"><h3>📧 Email</h3><p>support@pdfproapp.com</p></div>
    <div class="card"><h3>⏱ Response Time</h3><p>We reply within 24 hours on business days.</p></div>
  </div>
  <div class="card">
    <h2 style="margin-top:0">Send a Message</h2>
    <p style="margin-bottom:1.2rem">Fill out the form below and we'll get back to you shortly.</p>
    <input type="text" placeholder="Your Name" id="contact-name">
    <input type="email" placeholder="Your Email" id="contact-email">
    <select id="contact-subject">
      <option value="">Select a topic</option>
      <option>Technical support</option>
      <option>Billing question</option>
      <option>Feature request</option>
      <option>Partnership</option>
      <option>Other</option>
    </select>
    <textarea rows="5" placeholder="Your message..." id="contact-msg"></textarea>
    <button class="send-btn" onclick="submitContact()">Send Message</button>
    <p id="contact-success" style="display:none;color:#22c55e;font-weight:600;margin-top:0.8rem;text-align:center">✅ Message sent! We'll be in touch soon.</p>
  </div>
</div>
<script>
function submitContact(){
  const name=document.getElementById('contact-name').value;
  const email=document.getElementById('contact-email').value;
  if(!name||!email){alert('Please fill in your name and email.');return;}
  document.getElementById('contact-success').style.display='block';
}
</script>"""
    },

    # ── HELP ──
    "help/index.html": {
        "title": "Help Center | PDFPro",
        "desc": "Find answers to common questions about PDFPro tools.",
        "path": "/help/",
        "active": "",
        "content": """<div class="container">
  <div class="breadcrumb"><a href="/">Home</a> › <span>Help Center</span></div>
  <h1>Help Center</h1>
  <p class="lead">Find answers to the most common questions about PDFPro.</p>
  <h2>Getting Started</h2>
  <details><summary>How do I convert a PDF to Word?<span>+</span></summary>
    <p>Go to <a href="/pdf-to-word/" style="color:var(--red)">PDF to Word</a>, upload your PDF file, and click Download. The conversion happens automatically in seconds.</p>
  </details>
  <details><summary>Is PDFPro free to use?<span>+</span></summary>
    <p>Yes! All core tools are free. We offer a <a href="/pricing/" style="color:var(--red)">Pro plan</a> for unlimited usage, larger files, and priority processing.</p>
  </details>
  <details><summary>How long are my files stored?<span>+</span></summary>
    <p>Files are automatically deleted within 1 hour of upload. We never store, share, or analyse your documents.</p>
  </details>
  <h2>Tools</h2>
  <details><summary>What file formats are supported?<span>+</span></summary>
    <p>PDF is the primary input format. Outputs include DOCX, XLSX, JPG, PNG, and compressed PDF depending on the tool.</p>
  </details>
  <details><summary>Is there a file size limit?<span>+</span></summary>
    <p>Free users can process files up to 10MB. Pro users can process files up to 200MB.</p>
  </details>
  <details><summary>Does OCR work for Hebrew?<span>+</span></summary>
    <p>Yes! Our <a href="/ocr-pdf/" style="color:var(--red)">OCR tool</a> fully supports Hebrew and other RTL languages.</p>
  </details>
  <h2>Billing</h2>
  <details><summary>How do I cancel my subscription?<span>+</span></summary>
    <p>Go to your account settings and click "Cancel subscription". You'll keep Pro access until the end of the billing period.</p>
  </details>
  <details><summary>Do you offer refunds?<span>+</span></summary>
    <p>Yes, we offer a 7-day money-back guarantee. Contact us at support@pdfproapp.com.</p>
  </details>
  <div style="margin-top:2rem;padding:1.5rem;background:white;border-radius:12px;border:1px solid var(--border);text-align:center">
    <p style="font-weight:700;color:var(--navy);margin-bottom:0.3rem">Still need help?</p>
    <p style="margin-bottom:1rem">Our support team is ready to assist.</p>
    <a href="/contact/" class="cta">Contact Support</a>
  </div>
</div>"""
    },

    # ── MERGE PDF ──
    "merge-pdf/index.html": {
        "title": "Merge PDF Files Online | PDFPro",
        "desc": "Combine multiple PDF files into one. Fast, free and secure.",
        "path": "/merge-pdf/",
        "active": "tools",
        "content": """<div class="container">
  <div class="breadcrumb"><a href="/">Home</a> › <span>Merge PDF</span></div>
  <h1>Merge PDF</h1>
  <p class="lead">Combine multiple PDF files into a single document in seconds.</p>
  <div class="upload-zone" id="drop-zone" onclick="document.getElementById('file-input').click()" ondragover="event.preventDefault()" ondrop="handleDrop(event)">
    <span class="upload-icon">📎</span>
    <p style="font-size:1.1rem;font-weight:700;color:var(--navy);margin-bottom:0.5rem">Drop your PDF files here</p>
    <p>or <span style="color:var(--red);font-weight:600">browse files</span></p>
    <p style="font-size:0.82rem;margin-top:0.8rem">Select multiple PDFs · Max 50MB each</p>
    <input type="file" id="file-input" accept=".pdf" multiple style="display:none" onchange="handleFiles(this.files)">
  </div>
  <div id="file-list" style="margin-top:1rem"></div>
  <div id="merge-btn-wrapper" style="display:none;margin-top:1rem">
    <button class="send-btn" onclick="doMerge()">Merge PDFs</button>
  </div>
  <div id="result" style="display:none;margin-top:2rem">
    <div class="card" style="text-align:center;padding:2rem">
      <p style="font-size:1.5rem;margin-bottom:0.5rem">✅</p>
      <p style="font-weight:700;color:var(--navy);margin-bottom:1rem">Merged successfully!</p>
      <a href="#" class="cta" download="merged.pdf">Download Merged PDF</a>
    </div>
  </div>
  <div style="margin-top:3rem">
    <h2>How it works</h2>
    <div class="grid-3" style="margin-top:1rem">
      <div class="card"><h3>1. Upload Files</h3><p>Select two or more PDF files you want to combine.</p></div>
      <div class="card"><h3>2. Arrange Order</h3><p>Drag to reorder pages as you like.</p></div>
      <div class="card"><h3>3. Download</h3><p>Get your merged PDF instantly.</p></div>
    </div>
  </div>
</div>
<script>
let files=[];
function handleDrop(e){e.preventDefault();handleFiles(e.dataTransfer.files);}
function handleFiles(newFiles){
  files=[...files,...Array.from(newFiles)];
  renderList();
  document.getElementById('merge-btn-wrapper').style.display=files.length>1?'block':'none';
}
function renderList(){
  const list=document.getElementById('file-list');
  list.innerHTML=files.map((f,i)=>`<div class="card" style="display:flex;justify-content:space-between;align-items:center;padding:0.8rem 1rem;margin-bottom:0.5rem"><span>📄 ${f.name}</span><button onclick="removeFile(${i})" style="background:none;border:none;color:var(--red);cursor:pointer;font-size:1.2rem">×</button></div>`).join('');
}
function removeFile(i){files.splice(i,1);renderList();document.getElementById('merge-btn-wrapper').style.display=files.length>1?'block':'none';}
function doMerge(){document.getElementById('result').style.display='block';}
</script>"""
    },

    # ── OCR PDF ──
    "ocr-pdf/index.html": {
        "title": "OCR PDF Online | PDFPro",
        "desc": "Extract text from scanned PDFs and images. Supports Hebrew, Arabic, English and more.",
        "path": "/ocr-pdf/",
        "active": "tools",
        "content": TOOL_UPLOAD_EN("OCR PDF", ".pdf,.jpg,.jpeg,.png", "Extract text from scanned PDFs and images. Supports Hebrew, Arabic, English and 100+ languages.")
    },

    # ── PDF TO EXCEL ──
    "pdf-to-excel/index.html": {
        "title": "PDF to Excel Online | PDFPro",
        "desc": "Convert PDF tables to Excel spreadsheets accurately.",
        "path": "/pdf-to-excel/",
        "active": "tools",
        "content": TOOL_UPLOAD_EN("PDF to Excel", ".pdf", "Convert PDF tables and data into editable Excel spreadsheets with high accuracy.")
    },

    # ── PDF TO WORD ──
    "pdf-to-word/index.html": {
        "title": "PDF to Word Online | PDFPro",
        "desc": "Convert PDF to editable Word documents online for free.",
        "path": "/pdf-to-word/",
        "active": "tools",
        "content": TOOL_UPLOAD_EN("PDF to Word", ".pdf", "Convert PDF files to fully editable Word (.docx) documents. Preserves layout, fonts and formatting.")
    },

    # ── PRICING ──
    "pricing/index.html": {
        "title": "Pricing | PDFPro",
        "desc": "Simple, transparent pricing for PDF tools. Free, Pro and Team plans.",
        "path": "/pricing/",
        "active": "pricing",
        "content": """<div class="container">
  <div class="breadcrumb"><a href="/">Home</a> › <span>Pricing</span></div>
  <h1>Simple, Transparent Pricing</h1>
  <p class="lead" style="text-align:center;max-width:520px;margin:0 auto 2.5rem">Start free. Upgrade when you need more power. No hidden fees.</p>
  <div class="grid-3">
    <div class="price-card">
      <h3>Free</h3>
      <p class="price">$0<span class="period">/mo</span></p>
      <ul>
        <li>Up to 10MB per file</li>
        <li>5 conversions per day</li>
        <li>All core tools</li>
        <li>Files deleted in 1 hour</li>
      </ul>
      <a href="/#tools" class="cta" style="display:block;text-align:center">Get Started</a>
    </div>
    <div class="price-card featured">
      <span class="tag">Most Popular</span>
      <h3>Pro</h3>
      <p class="price">$9<span class="period">/mo</span></p>
      <ul>
        <li>Up to 200MB per file</li>
        <li>Unlimited conversions</li>
        <li>Priority processing</li>
        <li>All tools + OCR</li>
        <li>Translation (50 languages)</li>
        <li>Email support</li>
      </ul>
      <a href="/contact/" class="cta" style="display:block;text-align:center">Start Pro Trial</a>
    </div>
    <div class="price-card">
      <h3>Team</h3>
      <p class="price">$29<span class="period">/mo</span></p>
      <ul>
        <li>Everything in Pro</li>
        <li>Up to 10 team members</li>
        <li>Shared workspace</li>
        <li>API access</li>
        <li>Priority support</li>
        <li>Custom integrations</li>
      </ul>
      <a href="/contact/" class="cta" style="display:block;text-align:center;background:var(--navy)">Contact Sales</a>
    </div>
  </div>
  <h2 style="text-align:center;margin-top:3rem">Frequently Asked Questions</h2>
  <details style="margin-top:1rem"><summary>Can I cancel anytime?<span>+</span></summary><p>Yes, cancel anytime from your account settings with no penalties.</p></details>
  <details><summary>Is there a free trial for Pro?<span>+</span></summary><p>Yes, we offer a 7-day free trial for the Pro plan. No credit card required.</p></details>
  <details><summary>Do you offer refunds?<span>+</span></summary><p>Yes, 7-day money-back guarantee on all plans.</p></details>
</div>"""
    },

    # ── PRIVACY ──
    "privacy/index.html": {
        "title": "Privacy Policy | PDFPro",
        "desc": "PDFPro privacy policy — how we handle your data.",
        "path": "/privacy/",
        "active": "",
        "content": """<div class="container">
  <div class="breadcrumb"><a href="/">Home</a> › <span>Privacy Policy</span></div>
  <h1>Privacy Policy</h1>
  <p style="color:var(--muted);font-size:0.88rem;margin-bottom:2rem">Last updated: June 1, 2026</p>
  <h2>1. Information We Collect</h2>
  <p>We collect only what is necessary to provide our services. This includes files you upload for processing and basic usage analytics (pages visited, tool used) to improve our product.</p>
  <h2>2. How We Use Your Files</h2>
  <p>Files uploaded to PDFPro are processed on our secure servers and automatically deleted within 1 hour. We never read, share, or sell your document contents.</p>
  <h2>3. Cookies</h2>
  <p>We use essential cookies only (language preference, session). We do not use advertising or tracking cookies.</p>
  <h2>4. Third-Party Services</h2>
  <p>We use Google Fonts for typography. No advertising networks are used on our platform.</p>
  <h2>5. Data Retention</h2>
  <p>Uploaded files: deleted within 1 hour. Account data (if applicable): retained until account deletion. Analytics: aggregated and anonymised.</p>
  <h2>6. Your Rights</h2>
  <p>You have the right to access, correct, or delete any personal data we hold about you. Contact us at privacy@pdfproapp.com.</p>
  <h2>7. Contact</h2>
  <p>Questions about this policy? Email us at <a href="mailto:privacy@pdfproapp.com" style="color:var(--red)">privacy@pdfproapp.com</a> or <a href="/contact/" style="color:var(--red)">use our contact form</a>.</p>
</div>"""
    },

    # ── SPLIT PDF ──
    "split-pdf/index.html": {
        "title": "Split PDF Online | PDFPro",
        "desc": "Split a PDF into separate pages or page ranges easily.",
        "path": "/split-pdf/",
        "active": "tools",
        "content": """<div class="container">
  <div class="breadcrumb"><a href="/">Home</a> › <span>Split PDF</span></div>
  <h1>Split PDF</h1>
  <p class="lead">Divide a PDF into individual pages or custom page ranges.</p>
  <div class="upload-zone" onclick="document.getElementById('file-input').click()">
    <span class="upload-icon">✂️</span>
    <p style="font-size:1.1rem;font-weight:700;color:var(--navy);margin-bottom:0.5rem">Drop your PDF here</p>
    <p>or <span style="color:var(--red);font-weight:600">browse files</span></p>
    <input type="file" id="file-input" accept=".pdf" style="display:none" onchange="handleFile(this.files[0])">
  </div>
  <div id="options" style="display:none;margin-top:2rem">
    <div class="card">
      <h3>Split Options</h3>
      <p style="margin-bottom:1rem">Choose how you want to split the PDF:</p>
      <label style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.8rem;cursor:pointer"><input type="radio" name="split-mode" value="all" checked> Extract all pages as separate files</label>
      <label style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.8rem;cursor:pointer"><input type="radio" name="split-mode" value="range"> Extract specific page range</label>
      <div id="range-input" style="display:none;margin-top:0.5rem">
        <input type="text" placeholder="e.g. 1-3, 5, 7-10" style="margin-bottom:0">
      </div>
      <button class="send-btn" style="margin-top:1rem" onclick="doSplit()">Split PDF</button>
    </div>
  </div>
  <div id="result" style="display:none;margin-top:2rem">
    <div class="card" style="text-align:center;padding:2rem">
      <p style="font-size:1.5rem;margin-bottom:0.5rem">✅</p>
      <p style="font-weight:700;color:var(--navy);margin-bottom:1rem">PDF split successfully!</p>
      <a href="#" class="cta" download="split.zip">Download Files (.zip)</a>
    </div>
  </div>
</div>
<script>
document.querySelectorAll('input[name="split-mode"]').forEach(r=>r.addEventListener('change',()=>{document.getElementById('range-input').style.display=r.value==='range'?'block':'none';}));
function handleFile(f){if(f)document.getElementById('options').style.display='block';}
function doSplit(){document.getElementById('result').style.display='block';}
</script>"""
    },

    # ── TERMS ──
    "terms/index.html": {
        "title": "Terms of Use | PDFPro",
        "desc": "PDFPro terms of use and service agreement.",
        "path": "/terms/",
        "active": "",
        "content": """<div class="container">
  <div class="breadcrumb"><a href="/">Home</a> › <span>Terms of Use</span></div>
  <h1>Terms of Use</h1>
  <p style="color:var(--muted);font-size:0.88rem;margin-bottom:2rem">Last updated: June 1, 2026</p>
  <h2>1. Acceptance of Terms</h2>
  <p>By using PDFPro, you agree to these terms. If you disagree, please do not use our service.</p>
  <h2>2. Use of Service</h2>
  <p>PDFPro is provided for personal and commercial document processing. You agree not to use the service to process illegal, harmful, or copyrighted content without authorisation.</p>
  <h2>3. Uploaded Files</h2>
  <p>You retain full ownership of any files you upload. By uploading, you grant PDFPro a temporary, limited licence to process the file solely to provide the requested service. Files are deleted within 1 hour.</p>
  <h2>4. Limitation of Liability</h2>
  <p>PDFPro is provided "as is". We are not liable for any data loss, conversion errors, or damages arising from use of the service.</p>
  <h2>5. Intellectual Property</h2>
  <p>The PDFPro brand, design, and core technology are owned by PDFPro Ltd. Our open-source tools are available under the MIT licence.</p>
  <h2>6. Modifications</h2>
  <p>We may update these terms at any time. Continued use of the service constitutes acceptance of the updated terms.</p>
  <h2>7. Governing Law</h2>
  <p>These terms are governed by the laws of the State of Israel.</p>
  <h2>8. Contact</h2>
  <p>Questions? <a href="/contact/" style="color:var(--red)">Contact us</a> or email legal@pdfproapp.com.</p>
</div>"""
    },

    # ── TRANSLATE PDF ──
    "translate-pdf/index.html": {
        "title": "Translate PDF Online | PDFPro",
        "desc": "Translate PDF documents while preserving layout and formatting. Supports 50+ languages.",
        "path": "/translate-pdf/",
        "active": "tools",
        "content": """<div class="container">
  <div class="breadcrumb"><a href="/">Home</a> › <span>Translate PDF</span></div>
  <h1>Translate PDF</h1>
  <p class="lead">Translate PDF documents while preserving layout and formatting. Supports 50+ languages including Hebrew, Arabic, English and more.</p>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:1.5rem">
    <div>
      <label style="display:block;font-weight:600;color:var(--navy);margin-bottom:0.4rem">From</label>
      <select id="lang-from"><option value="auto">Detect automatically</option><option value="en">English</option><option value="he">Hebrew (עברית)</option><option value="ar">Arabic (العربية)</option><option value="fr">French</option><option value="de">German</option><option value="es">Spanish</option><option value="ru">Russian</option><option value="zh">Chinese</option></select>
    </div>
    <div>
      <label style="display:block;font-weight:600;color:var(--navy);margin-bottom:0.4rem">To</label>
      <select id="lang-to"><option value="he">Hebrew (עברית)</option><option value="en">English</option><option value="ar">Arabic (العربية)</option><option value="fr">French</option><option value="de">German</option><option value="es">Spanish</option><option value="ru">Russian</option><option value="zh">Chinese</option></select>
    </div>
  </div>
  <div class="upload-zone" onclick="document.getElementById('file-input').click()">
    <span class="upload-icon">🌐</span>
    <p style="font-size:1.1rem;font-weight:700;color:var(--navy);margin-bottom:0.5rem">Drop your PDF here</p>
    <p>or <span style="color:var(--red);font-weight:600">browse files</span></p>
    <p style="font-size:0.82rem;margin-top:0.8rem">PDF only · Max 50MB</p>
    <input type="file" id="file-input" accept=".pdf" style="display:none" onchange="handleFile(this.files[0])">
  </div>
  <div id="result" style="display:none;margin-top:2rem">
    <div class="card" style="text-align:center;padding:2rem">
      <p style="font-size:1.5rem;margin-bottom:0.5rem">✅</p>
      <p style="font-weight:700;color:var(--navy);margin-bottom:1rem">Translation complete!</p>
      <a href="#" class="cta" download="translated.pdf">Download Translated PDF</a>
    </div>
  </div>
  <div style="margin-top:3rem">
    <h2>Why use PDFPro Translate?</h2>
    <div class="grid-3" style="margin-top:1rem">
      <div class="card"><h3>Layout Preserved</h3><p>Fonts, columns, images and formatting stay intact after translation.</p></div>
      <div class="card"><h3>RTL Support</h3><p>Full support for Hebrew and Arabic right-to-left documents.</p></div>
      <div class="card"><h3>50+ Languages</h3><p>Translate between dozens of language pairs instantly.</p></div>
    </div>
  </div>
</div>
<script>
function handleFile(f){if(f)setTimeout(()=>document.getElementById('result').style.display='block',1200);}
</script>"""
    },
}

# ─────────────────────────────────────────────────────────
# HEBREW VERSIONS (simplified — mirror structure with RTL)
# ─────────────────────────────────────────────────────────
HE_PAGES = {
    "he/about/index.html": {
        "title": "אודות PDFPro",
        "desc": "למד על המשימה, הסיפור והערכים של PDFPro.",
        "path": "/he/about/",
        "active": "",
        "content": """<div class="container">
  <div class="breadcrumb"><a href="/he/">בית</a> › <span>אודות</span></div>
  <h1>אודות PDFPro</h1>
  <p class="lead">PDFPro נוסדה עם משימה פשוטה: להפוך כלי PDF מקצועיים לנגישים לכולם, ללא תוכנות יקרות.</p>
  <h2>הסיפור שלנו</h2>
  <p>התחלנו ב-2024 כצוות קטן של מפתחים שנמאס להם מתוכנות PDF מסורבלות ויקרות. האמנו שהמרת PDF צריכה לקחת שניות.</p>
  <p>היום, למעלה מ-2 מיליון אנשי מקצוע משתמשים ב-PDFPro בכל חודש לעריכה, המרה וניהול מסמכים.</p>
  <h2>הערכים שלנו</h2>
  <div class="grid-2">
    <div class="card"><h3>פרטיות קודמת</h3><p>הקבצים שלך לעולם לא נשמרים יותר מ-60 דקות.</p></div>
    <div class="card"><h3>ללא פרסומות</h3><p>לעולם לא נציג פרסומות ולא נמכור את הנתונים שלך.</p></div>
    <div class="card"><h3>קוד פתוח</h3><p>הכלים המרכזיים שלנו ברישיון MIT.</p></div>
    <div class="card"><h3>תמחור הוגן</h3><p>כלים מקצועיים במחירים נגישים.</p></div>
  </div>
  <a href="/he/contact/" class="cta">צור קשר</a>
</div>"""
    },
    "he/blog/index.html": {
        "title": "בלוג | PDFPro",
        "desc": "טיפים, מדריכים ועדכונים מצוות PDFPro.",
        "path": "/he/blog/",
        "active": "",
        "content": """<div class="container">
  <div class="breadcrumb"><a href="/he/">בית</a> › <span>בלוג</span></div>
  <h1>בלוג</h1>
  <p class="lead">טיפים, מדריכים ועדכונים מצוות PDFPro.</p>
  <div class="blog-card" onclick="window.location.href='/he/compress-pdf/'">
    <p class="blog-date">20 במאי 2026</p>
    <span class="tag">דחיסה</span>
    <h2>כיצד לצמצם גודל קובץ PDF ללא איבוד איכות</h2>
    <p>למד את האסטרטגיות הטובות ביותר לדחיסת PDF תוך שמירה על קריאות ואיכות.</p>
    <p style="color:var(--red);font-size:0.85rem;font-weight:600;margin-top:0.8rem">נסה את הכלי ←</p>
  </div>
  <div class="blog-card" onclick="window.location.href='/he/ocr-pdf/'">
    <p class="blog-date">15 במאי 2026</p>
    <span class="tag">OCR</span>
    <h2>OCR למסמכים בעברית: מדריך מלא</h2>
    <p>כל מה שצריך לדעת על חילוץ טקסט עברי ממסמכים סרוקים ותמונות.</p>
    <p style="color:var(--red);font-size:0.85rem;font-weight:600;margin-top:0.8rem">נסה את הכלי ←</p>
  </div>
  <div class="blog-card" onclick="window.location.href='/he/pdf-to-word/'">
    <p class="blog-date">8 במאי 2026</p>
    <span class="tag">המרה</span>
    <h2>PDF ל-Word: מתי זה עובד ומתי לא</h2>
    <p>הבנת מגבלות המרת PDF וכיצד לקבל את התוצאות הטובות ביותר.</p>
    <p style="color:var(--red);font-size:0.85rem;font-weight:600;margin-top:0.8rem">נסה את הכלי ←</p>
  </div>
</div>"""
    },
    "he/compress-pdf/index.html": {
        "title": "דחיסת PDF אונליין | PDFPro",
        "desc": "הפחת גודל קובץ PDF ללא איבוד איכות.",
        "path": "/he/compress-pdf/",
        "active": "tools",
        "content": """<div class="container">
  <div class="breadcrumb"><a href="/he/">בית</a> › <span>דחיסת PDF</span></div>
  <h1>דחיסת PDF</h1>
  <p class="lead">הפחת גודל קובץ PDF ללא איבוד איכות. מהיר, חינמי ומאובטח.</p>
  <div class="upload-zone" onclick="document.getElementById('file-input').click()">
    <span class="upload-icon">📄</span>
    <p style="font-size:1.1rem;font-weight:700;color:var(--navy);margin-bottom:0.5rem">גרור את ה-PDF לכאן</p>
    <p>או <span style="color:var(--red);font-weight:600;cursor:pointer">בחר קובץ</span></p>
    <input type="file" id="file-input" accept=".pdf" style="display:none" onchange="document.getElementById('result').style.display='block'">
  </div>
  <div id="result" style="display:none;margin-top:2rem">
    <div class="card" style="text-align:center;padding:2rem">
      <p style="font-size:1.5rem;margin-bottom:0.5rem">✅</p>
      <p style="font-weight:700;color:var(--navy);margin-bottom:1rem">הקובץ דוחס בהצלחה!</p>
      <a href="#" class="cta">הורד PDF מדוחס</a>
    </div>
  </div>
</div>"""
    },
    "he/contact/index.html": {
        "title": "צור קשר | PDFPro",
        "desc": "צור קשר עם צוות PDFPro.",
        "path": "/he/contact/",
        "active": "",
        "content": """<div class="container">
  <div class="breadcrumb"><a href="/he/">בית</a> › <span>צור קשר</span></div>
  <h1>צור קשר</h1>
  <p class="lead">יש לך שאלה או משוב? נשמח לשמוע ממך.</p>
  <div class="card">
    <h2 style="margin-top:0">שלח הודעה</h2>
    <input type="text" placeholder="שמך" style="direction:rtl">
    <input type="email" placeholder="כתובת דוא&quot;ל" style="direction:ltr">
    <textarea rows="5" placeholder="ההודעה שלך..." style="direction:rtl"></textarea>
    <button class="send-btn" onclick="alert('ההודעה נשלחה! נחזור אליך בקרוב.')">שלח הודעה</button>
  </div>
</div>"""
    },
    "he/help/index.html": {
        "title": "מרכז עזרה | PDFPro",
        "desc": "מצא תשובות לשאלות נפוצות על כלי PDFPro.",
        "path": "/he/help/",
        "active": "",
        "content": """<div class="container">
  <div class="breadcrumb"><a href="/he/">בית</a> › <span>מרכז עזרה</span></div>
  <h1>מרכז עזרה</h1>
  <p class="lead">מצא תשובות לשאלות הנפוצות ביותר על PDFPro.</p>
  <h2>התחלה מהירה</h2>
  <details><summary>כיצד ממירים PDF ל-Word?<span>+</span></summary><p>עבור ל-<a href="/he/pdf-to-word/" style="color:var(--red)">PDF ל-Word</a>, העלה את קובץ ה-PDF ולחץ הורד. ההמרה מתבצעת אוטומטית תוך שניות.</p></details>
  <details><summary>האם PDFPro חינמי?<span>+</span></summary><p>כן! כל הכלים המרכזיים חינמיים. קיים גם <a href="/he/pricing/" style="color:var(--red)">מסלול Pro</a> לשימוש ללא הגבלה.</p></details>
  <details><summary>כמה זמן הקבצים נשמרים?<span>+</span></summary><p>קבצים נמחקים אוטומטית תוך שעה אחת.</p></details>
  <div style="margin-top:2rem;padding:1.5rem;background:white;border-radius:12px;border:1px solid var(--border);text-align:center">
    <p style="font-weight:700;color:var(--navy);margin-bottom:0.3rem">עדיין צריך עזרה?</p>
    <a href="/he/contact/" class="cta" style="margin-top:0.5rem;display:inline-block">פנה לתמיכה</a>
  </div>
</div>"""
    },
    "he/merge-pdf/index.html": {
        "title": "מיזוג PDF אונליין | PDFPro",
        "desc": "שלב מספר קבצי PDF לאחד.",
        "path": "/he/merge-pdf/",
        "active": "tools",
        "content": """<div class="container">
  <div class="breadcrumb"><a href="/he/">בית</a> › <span>מיזוג PDF</span></div>
  <h1>מיזוג PDF</h1>
  <p class="lead">שלב מספר קבצי PDF למסמך אחד תוך שניות.</p>
  <div class="upload-zone" onclick="document.getElementById('file-input').click()">
    <span class="upload-icon">📎</span>
    <p style="font-size:1.1rem;font-weight:700;color:var(--navy);margin-bottom:0.5rem">גרור קבצי PDF לכאן</p>
    <p>או <span style="color:var(--red);font-weight:600">בחר קבצים</span></p>
    <input type="file" id="file-input" accept=".pdf" multiple style="display:none" onchange="document.getElementById('result').style.display='block'">
  </div>
  <div id="result" style="display:none;margin-top:2rem">
    <div class="card" style="text-align:center;padding:2rem">
      <p style="font-size:1.5rem;margin-bottom:0.5rem">✅</p>
      <p style="font-weight:700;color:var(--navy);margin-bottom:1rem">הקבצים מוזגו בהצלחה!</p>
      <a href="#" class="cta">הורד PDF ממוזג</a>
    </div>
  </div>
</div>"""
    },
    "he/ocr-pdf/index.html": {
        "title": "OCR PDF אונליין | PDFPro",
        "desc": "חלץ טקסט מ-PDF סרוק ותמונות. תמיכה מלאה בעברית.",
        "path": "/he/ocr-pdf/",
        "active": "tools",
        "content": """<div class="container">
  <div class="breadcrumb"><a href="/he/">בית</a> › <span>OCR PDF</span></div>
  <h1>OCR PDF</h1>
  <p class="lead">חלץ טקסט מ-PDF סרוק ותמונות. תמיכה מלאה בעברית, ערבית ועוד 100 שפות.</p>
  <div class="upload-zone" onclick="document.getElementById('file-input').click()">
    <span class="upload-icon">🔍</span>
    <p style="font-size:1.1rem;font-weight:700;color:var(--navy);margin-bottom:0.5rem">גרור את ה-PDF לכאן</p>
    <p>או <span style="color:var(--red);font-weight:600">בחר קובץ</span></p>
    <input type="file" id="file-input" accept=".pdf,.jpg,.png" style="display:none" onchange="document.getElementById('result').style.display='block'">
  </div>
  <div id="result" style="display:none;margin-top:2rem">
    <div class="card" style="text-align:center;padding:2rem">
      <p style="font-size:1.5rem;margin-bottom:0.5rem">✅</p>
      <p style="font-weight:700;color:var(--navy);margin-bottom:1rem">הטקסט חולץ בהצלחה!</p>
      <a href="#" class="cta">הורד קובץ טקסט</a>
    </div>
  </div>
</div>"""
    },
    "he/pdf-to-excel/index.html": {
        "title": "PDF ל-Excel אונליין | PDFPro",
        "desc": "המר טבלאות PDF לגיליונות Excel עם דיוק גבוה.",
        "path": "/he/pdf-to-excel/",
        "active": "tools",
        "content": """<div class="container">
  <div class="breadcrumb"><a href="/he/">בית</a> › <span>PDF ל-Excel</span></div>
  <h1>PDF ל-Excel</h1>
  <p class="lead">המר טבלאות ונתונים מ-PDF לגיליונות Excel עם דיוק גבוה.</p>
  <div class="upload-zone" onclick="document.getElementById('file-input').click()">
    <span class="upload-icon">📊</span>
    <p style="font-size:1.1rem;font-weight:700;color:var(--navy);margin-bottom:0.5rem">גרור את ה-PDF לכאן</p>
    <p>או <span style="color:var(--red);font-weight:600">בחר קובץ</span></p>
    <input type="file" id="file-input" accept=".pdf" style="display:none" onchange="document.getElementById('result').style.display='block'">
  </div>
  <div id="result" style="display:none;margin-top:2rem">
    <div class="card" style="text-align:center;padding:2rem">
      <p style="font-size:1.5rem;margin-bottom:0.5rem">✅</p>
      <p style="font-weight:700;color:var(--navy);margin-bottom:1rem">ההמרה הושלמה!</p>
      <a href="#" class="cta" download="output.xlsx">הורד קובץ Excel</a>
    </div>
  </div>
</div>"""
    },
    "he/pdf-to-word/index.html": {
        "title": "PDF ל-Word אונליין | PDFPro",
        "desc": "המר PDF למסמך Word עריך אונליין.",
        "path": "/he/pdf-to-word/",
        "active": "tools",
        "content": """<div class="container">
  <div class="breadcrumb"><a href="/he/">בית</a> › <span>PDF ל-Word</span></div>
  <h1>PDF ל-Word</h1>
  <p class="lead">המר קבצי PDF למסמכי Word עריכים לחלוטין. שומר על פריסה, גופנים ועיצוב.</p>
  <div class="upload-zone" onclick="document.getElementById('file-input').click()">
    <span class="upload-icon">📝</span>
    <p style="font-size:1.1rem;font-weight:700;color:var(--navy);margin-bottom:0.5rem">גרור את ה-PDF לכאן</p>
    <p>או <span style="color:var(--red);font-weight:600">בחר קובץ</span></p>
    <input type="file" id="file-input" accept=".pdf" style="display:none" onchange="document.getElementById('result').style.display='block'">
  </div>
  <div id="result" style="display:none;margin-top:2rem">
    <div class="card" style="text-align:center;padding:2rem">
      <p style="font-size:1.5rem;margin-bottom:0.5rem">✅</p>
      <p style="font-weight:700;color:var(--navy);margin-bottom:1rem">ההמרה הושלמה!</p>
      <a href="#" class="cta" download="output.docx">הורד קובץ Word</a>
    </div>
  </div>
</div>"""
    },
    "he/pricing/index.html": {
        "title": "תמחור | PDFPro",
        "desc": "תמחור פשוט ושקוף לכלי PDF. מסלולי חינם, Pro וצוות.",
        "path": "/he/pricing/",
        "active": "pricing",
        "content": """<div class="container">
  <div class="breadcrumb"><a href="/he/">בית</a> › <span>תמחור</span></div>
  <h1>תמחור פשוט ושקוף</h1>
  <p class="lead" style="text-align:center;max-width:520px;margin:0 auto 2.5rem">התחל בחינם. שדרג כשאתה צריך יותר כוח. ללא דמי הפתעה.</p>
  <div class="grid-3">
    <div class="price-card">
      <h3>חינם</h3>
      <p class="price">₪0<span class="period">/חודש</span></p>
      <ul>
        <li>עד 10MB לקובץ</li>
        <li>5 המרות ליום</li>
        <li>כל הכלים הבסיסיים</li>
      </ul>
      <a href="/he/#tools" class="cta" style="display:block;text-align:center">התחל עכשיו</a>
    </div>
    <div class="price-card featured">
      <span class="tag">הכי פופולרי</span>
      <h3>Pro</h3>
      <p class="price">₪33<span class="period">/חודש</span></p>
      <ul>
        <li>עד 200MB לקובץ</li>
        <li>המרות ללא הגבלה</li>
        <li>עיבוד מועדף</li>
        <li>כל הכלים + OCR</li>
        <li>תרגום (50 שפות)</li>
        <li>תמיכה במייל</li>
      </ul>
      <a href="/he/contact/" class="cta" style="display:block;text-align:center">התנסה ב-Pro</a>
    </div>
    <div class="price-card">
      <h3>צוות</h3>
      <p class="price">₪109<span class="period">/חודש</span></p>
      <ul>
        <li>הכל ב-Pro</li>
        <li>עד 10 משתמשים</li>
        <li>סביבת עבודה משותפת</li>
        <li>גישת API</li>
        <li>תמיכה מועדפת</li>
      </ul>
      <a href="/he/contact/" class="cta" style="display:block;text-align:center;background:var(--navy)">פנה למכירות</a>
    </div>
  </div>
</div>"""
    },
    "he/privacy/index.html": {
        "title": "מדיניות פרטיות | PDFPro",
        "desc": "מדיניות הפרטיות של PDFPro — כיצד אנו מטפלים בנתוניך.",
        "path": "/he/privacy/",
        "active": "",
        "content": """<div class="container">
  <div class="breadcrumb"><a href="/he/">בית</a> › <span>מדיניות פרטיות</span></div>
  <h1>מדיניות פרטיות</h1>
  <p style="color:var(--muted);font-size:0.88rem;margin-bottom:2rem">עודכן לאחרונה: 1 ביוני 2026</p>
  <h2>1. מידע שאנו אוספים</h2>
  <p>אנו אוספים רק את מה שנחוץ למתן השירותים שלנו: קבצים שאתה מעלה לעיבוד ואנליטיקס בסיסי.</p>
  <h2>2. כיצד אנו משתמשים בקבצים שלך</h2>
  <p>קבצים המועלים ל-PDFPro מעובדים בשרתים מאובטחים ונמחקים אוטומטית תוך שעה. לעולם לא נקרא, נשתף או נמכור את תכני המסמכים שלך.</p>
  <h2>3. עוגיות</h2>
  <p>אנו משתמשים בעוגיות חיוניות בלבד (העדפת שפה, סשן). אין עוגיות פרסום או מעקב.</p>
  <h2>4. יצירת קשר</h2>
  <p>שאלות? <a href="/he/contact/" style="color:var(--red)">צור קשר</a> או שלח מייל ל-privacy@pdfproapp.com.</p>
</div>"""
    },
    "he/split-pdf/index.html": {
        "title": "פיצול PDF אונליין | PDFPro",
        "desc": "פצל PDF לדפים נפרדים או טווחי עמודים.",
        "path": "/he/split-pdf/",
        "active": "tools",
        "content": """<div class="container">
  <div class="breadcrumb"><a href="/he/">בית</a> › <span>פיצול PDF</span></div>
  <h1>פיצול PDF</h1>
  <p class="lead">חלק PDF לדפים נפרדים או טווחי עמודים מותאמים אישית.</p>
  <div class="upload-zone" onclick="document.getElementById('file-input').click()">
    <span class="upload-icon">✂️</span>
    <p style="font-size:1.1rem;font-weight:700;color:var(--navy);margin-bottom:0.5rem">גרור את ה-PDF לכאן</p>
    <p>או <span style="color:var(--red);font-weight:600">בחר קובץ</span></p>
    <input type="file" id="file-input" accept=".pdf" style="display:none" onchange="document.getElementById('result').style.display='block'">
  </div>
  <div id="result" style="display:none;margin-top:2rem">
    <div class="card" style="text-align:center;padding:2rem">
      <p style="font-size:1.5rem;margin-bottom:0.5rem">✅</p>
      <p style="font-weight:700;color:var(--navy);margin-bottom:1rem">ה-PDF פוצל בהצלחה!</p>
      <a href="#" class="cta">הורד קבצים (.zip)</a>
    </div>
  </div>
</div>"""
    },
    "he/terms/index.html": {
        "title": "תנאי שימוש | PDFPro",
        "desc": "תנאי השימוש של PDFPro.",
        "path": "/he/terms/",
        "active": "",
        "content": """<div class="container">
  <div class="breadcrumb"><a href="/he/">בית</a> › <span>תנאי שימוש</span></div>
  <h1>תנאי שימוש</h1>
  <p style="color:var(--muted);font-size:0.88rem;margin-bottom:2rem">עודכן לאחרונה: 1 ביוני 2026</p>
  <h2>1. קבלת התנאים</h2>
  <p>בשימוש ב-PDFPro, אתה מסכים לתנאים אלה. אם אינך מסכים, אנא אל תשתמש בשירות.</p>
  <h2>2. שימוש בשירות</h2>
  <p>PDFPro מסופקת לעיבוד מסמכים אישי ועסקי. אתה מסכים לא להשתמש בשירות לעיבוד תכנים בלתי חוקיים.</p>
  <h2>3. קבצים מועלים</h2>
  <p>אתה שומר על בעלות מלאה על הקבצים שלך. קבצים נמחקים תוך שעה.</p>
  <h2>4. יצירת קשר</h2>
  <p>שאלות? <a href="/he/contact/" style="color:var(--red)">צור קשר</a>.</p>
</div>"""
    },
    "he/translate-pdf/index.html": {
        "title": "תרגום PDF אונליין | PDFPro",
        "desc": "תרגם מסמכי PDF תוך שמירה על פריסה ועיצוב. תמיכה ב-50+ שפות.",
        "path": "/he/translate-pdf/",
        "active": "tools",
        "content": """<div class="container">
  <div class="breadcrumb"><a href="/he/">בית</a> › <span>תרגום PDF</span></div>
  <h1>תרגום PDF</h1>
  <p class="lead">תרגם מסמכי PDF תוך שמירה על פריסה ועיצוב. תמיכה ב-50+ שפות כולל עברית, ערבית ואנגלית.</p>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:1.5rem">
    <div>
      <label style="display:block;font-weight:600;color:var(--navy);margin-bottom:0.4rem">מ</label>
      <select><option>זיהוי אוטומטי</option><option>עברית</option><option>אנגלית</option><option>ערבית</option></select>
    </div>
    <div>
      <label style="display:block;font-weight:600;color:var(--navy);margin-bottom:0.4rem">ל</label>
      <select><option>אנגלית</option><option>עברית</option><option>ערבית</option><option>צרפתית</option></select>
    </div>
  </div>
  <div class="upload-zone" onclick="document.getElementById('file-input').click()">
    <span class="upload-icon">🌐</span>
    <p style="font-size:1.1rem;font-weight:700;color:var(--navy);margin-bottom:0.5rem">גרור את ה-PDF לכאן</p>
    <p>או <span style="color:var(--red);font-weight:600">בחר קובץ</span></p>
    <input type="file" id="file-input" accept=".pdf" style="display:none" onchange="document.getElementById('result').style.display='block'">
  </div>
  <div id="result" style="display:none;margin-top:2rem">
    <div class="card" style="text-align:center;padding:2rem">
      <p style="font-size:1.5rem;margin-bottom:0.5rem">✅</p>
      <p style="font-weight:700;color:var(--navy);margin-bottom:1rem">התרגום הושלם!</p>
      <a href="#" class="cta" download="translated.pdf">הורד PDF מתורגם</a>
    </div>
  </div>
</div>"""
    },
}

# Hebrew footer with RTL nav
def make_he_header(active_page=""):
    links = [
        ("/he/#tools",    "כלים",    "tools"),
        ("/he/#features", "תכונות", "features"),
        ("/he/pricing/",  "תמחור",  "pricing"),
    ]
    nav_items = "\n    ".join(
        f'<li><a href="{href}" class="{"active" if slug == active_page else ""}">{label}</a></li>'
        for href, label, slug in links
    )
    return f"""<nav>
  <a href="/he/" class="logo">PDF<span>Pro</span></a>
  <ul class="nav-links">
    {nav_items}
  </ul>
  <div class="nav-right">
    <span class="api-status offline" id="api-status">
      <span class="api-dot"></span>
      <span id="api-status-text">מתחבר...</span>
    </span>
    <a class="nav-cta" href="/he/#tools">התחל עכשיו</a>
  </div>
</nav>"""

HE_FOOTER = """<footer>
  <div class="footer-inner">
    <div class="footer-brand">
      <a href="/he/" class="logo">PDF<span>Pro</span></a>
      <p>הפלטפורמה המובילה לעיבוד PDF — מהיר, מאובטח ומקצועי.</p>
      <div class="footer-language">
        <label for="footer-lang">שפה</label>
        <select id="footer-lang" onchange="changeSiteLanguage(this.value)">
          <option value="en">English</option>
          <option value="he">עברית</option>
        </select>
      </div>
    </div>
    <div class="footer-col">
      <h4>כלים</h4>
      <ul>
        <li><a href="/he/pdf-to-word/">PDF ל-Word</a></li>
        <li><a href="/he/pdf-to-excel/">PDF ל-Excel</a></li>
        <li><a href="/he/compress-pdf/">דחיסת PDF</a></li>
        <li><a href="/he/merge-pdf/">מיזוג PDF</a></li>
        <li><a href="/he/split-pdf/">פיצול PDF</a></li>
        <li><a href="/he/ocr-pdf/">OCR PDF</a></li>
        <li><a href="/he/translate-pdf/">תרגום PDF</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>חברה</h4>
      <ul>
        <li><a href="/he/about/">אודות</a></li>
        <li><a href="/he/blog/">בלוג</a></li>
        <li><a href="/he/contact/">צור קשר</a></li>
        <li><a href="/he/pricing/">תמחור</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>תמיכה</h4>
      <ul>
        <li><a href="/he/help/">מרכז עזרה</a></li>
        <li><a href="/he/privacy/">מדיניות פרטיות</a></li>
        <li><a href="/he/terms/">תנאי שימוש</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <span>© 2026 PDFPro. כל הזכויות שמורות.</span>
    <span>🌍 נעשה עם ❤️</span>
  </div>
</footer>"""

# ─────────────────────────────────────────────────────────
# WRITE ALL FILES
# ─────────────────────────────────────────────────────────
def write_page(rel_path, html):
    full = os.path.join(os.getcwd(), rel_path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  ✓  {rel_path}")

def main():
    print("\n🚀  Generating PDFPro pages...\n")

    # English pages
    for rel_path, cfg in PAGES.items():
        html = build_page(
            title=cfg["title"],
            description=cfg["desc"],
            canonical_path=cfg["path"],
            active_page=cfg["active"],
            body_content=cfg["content"],
            lang="en",
        )
        write_page(rel_path, html)

    # Hebrew pages (use custom header/footer)
    for rel_path, cfg in HE_PAGES.items():
        header = make_he_header(cfg["active"])
        css = SHARED_CSS
        js  = SHARED_JS
        direction = "rtl"
        lang = "he"
        en_path = cfg["path"].replace("/he","") or "/"
        canonical_full = f"https://pdfproapp.com{cfg['path']}"
        en_full = f"https://pdfproapp.com{en_path}"
        he_full = f"https://pdfproapp.com{cfg['path']}"

        html = f"""<!DOCTYPE html>
<html id="html-root" lang="he" dir="rtl">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<meta name="description" content="{cfg['desc']}">
<title>{cfg['title']}</title>
<link rel="canonical" href="{canonical_full}">
<link rel="alternate" hreflang="en" href="{en_full}">
<link rel="alternate" hreflang="he" href="{he_full}">
<link rel="alternate" hreflang="x-default" href="{en_full}">
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;600;700;800&family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet"/>
<style>{css}</style>
</head>
<body class="rtl">
{header}
{cfg['content']}
{HE_FOOTER}
<script>{js}</script>
</body>
</html>"""
        write_page(rel_path, html)

    total = len(PAGES) + len(HE_PAGES)
    print(f"\n✅  Done! {total} pages generated.\n")
    print("Pages generated:")
    for k in list(PAGES.keys()) + list(HE_PAGES.keys()):
        print(f"   • {k}")

if __name__ == "__main__":
    main()