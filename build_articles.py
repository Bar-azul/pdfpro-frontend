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
body{font-family:'Heebo',sans-serif;background:var(--cream);color:var(--text);direction:rtl}
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
.footer-col h4{font-size:0.85rem;font-weight:700;color:rgba(255,255,255,0.5);text-transform:uppercase;letter-spacing:0;margin-bottom:1rem}
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
ul.article-list{margin:0 0 1rem 0;padding-right:1.3rem;color:var(--muted);line-height:1.9}
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
  <a href="/he/" class="logo">PDF<span>Pro</span></a>
  <ul class="nav-links">
    <li><a href="/he/#tools">כלים</a></li>
    <li><a href="/he/#features">יתרונות</a></li>
    <li><a href="/he/pricing/">מחירים</a></li>
  </ul>
  <div class="nav-right">
    <span class="api-status offline" id="api-status"><span class="api-dot"></span><span id="api-status-text">מתחבר...</span></span>
    <a class="nav-cta" href="/he/#tools">התחל עכשיו</a>
  </div>
</nav>"""

FOOTER = """<footer>
  <div class="footer-inner">
    <div class="footer-brand">
      <a href="/he/" class="logo">PDF<span>Pro</span></a>
      <p>הפלטפורמה המובילה לעיבוד מסמכי PDF — מהירה, מאובטחת ומקצועית.</p>
      <div class="footer-language">
        <label for="footer-lang">שפה</label>
        <select id="footer-lang" onchange="changeSiteLanguage(this.value)">
          <option value="en">English</option>
          <option value="he" selected>עברית</option>
        </select>
      </div>
    </div>
    <div class="footer-col"><h4>כלים</h4><ul>
      <li><a href="/he/pdf-to-word/">המרת PDF</a></li>
      <li><a href="/he/merge-pdf/">מיזוג PDF</a></li>
      <li><a href="/he/compress-pdf/">דחיסת PDF</a></li>
      <li><a href="/he/ocr-pdf/">OCR</a></li>
    </ul></div>
    <div class="footer-col"><h4>חברה</h4><ul>
      <li><a href="/he/about/">אודות</a></li>
      <li><a href="/he/blog/">בלוג</a></li>
      <li><a href="/he/contact/">צור קשר</a></li>
    </ul></div>
    <div class="footer-col"><h4>תמיכה</h4><ul>
      <li><a href="/he/help/">מרכז עזרה</a></li>
      <li><a href="/he/privacy/">מדיניות פרטיות</a></li>
      <li><a href="/he/terms/">תנאי שימוש</a></li>
    </ul></div>
  </div>
  <div class="footer-bottom"><span>© 2026 PDFPro. כל הזכויות שמורות.</span><span>🌍 Made with ❤️</span></div>
</footer>"""


def build_article(slug, title, description, date, tag, tool_link, tool_label, body_html):
    canonical = f"https://www.pdfproapp.com/he/blog/{slug}/"
    en_canonical = f"https://www.pdfproapp.com/blog/{slug}/"
    return f"""<!DOCTYPE html>
<html id="html-root" lang="he" dir="rtl">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<meta name="description" content="{description}">
<title>{title} | PDFPro</title>
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="he" href="{canonical}">
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
  <div class="breadcrumb"><a href="/he/">בית</a> › <a href="/he/blog/">בלוג</a> › <span>{title}</span></div>
  <span class="tag">{tag}</span>
  <h1>{title}</h1>
  <p class="meta">{date}</p>
  {body_html}
  <div class="card" style="text-align:center;margin-top:2rem">
    <p style="color:var(--navy);font-weight:700;margin-bottom:0.6rem">רוצה לנסות בעצמך?</p>
    <a href="{tool_link}" class="cta">{tool_label}</a>
  </div>
</div>
{FOOTER}
<script>{LANG_JS}</script>
</body>
</html>
"""


ARTICLES = []

# ── 1. RTL Hebrew PDF ──────────────────────────────────────────
ARTICLES.append(dict(
    slug="pdf-hebrew-rtl",
    title='למה הטקסט בעברית "מתהפך" אחרי המרת PDF? והפתרון המלא',
    description="הסבר מלא לבעיית ה-RTL בהמרת PDF לעברית - למה זה קורה וכיצד לפתור את זה נכון.",
    date="1 ביולי 2026", sort_date="2026-07-01",
    tag="המרה",
    tool_link="/he/pdf-to-word/",
    tool_label="המר PDF ל-Word עכשיו",
    body_html="""
<p class="lead">אם אי פעם המרת PDF בעברית ל-Word וקיבלת בחזרה טקסט הפוך, מבולגן, או עם סדר מילים משובש — אתה לא לבד. זו אחת התקלות הנפוצות ביותר בהמרת מסמכים בעברית, והיא כמעט תמיד קשורה לאותה סיבה טכנית אחת.</p>

<h2>מה גורם לבעיה?</h2>
<p>עברית היא שפת <strong>RTL</strong> (מימין לשמאל), בזמן שרוב מנועי ההמרה בעולם נבנו במקור סביב אנגלית, שפת <strong>LTR</strong> (משמאל לימין). כשמנוע המרה לא בנוי נכון לטפל בכיווניות מעורבת, קורים כמה דברים אופייניים:</p>
<ul class="article-list">
  <li>הפיכת סדר תווים - מילים שלמות מופיעות "מגובבות" בסדר הפוך</li>
  <li>בעיות במספרים ותאריכים בתוך משפט עברי</li>
  <li>פירוק פסקאות מעורבות עברית-אנגלית</li>
  <li>יישור טקסט הפוך - נדבק לשמאל במקום לימין</li>
</ul>

<h2>למה זה קורה בעיקר בהמרת PDF?</h2>
<p>PDF, בניגוד ל-Word, לא שומר את הטקסט כ"טקסט הגיוני" עם כיווניות מוגדרת - הוא שומר בעיקר את המיקום הוויזואלי של כל תו על הדף. מנוע המרה חייב לשחזר את הכיווניות הנכונה מתוך המיקום החזותי בלבד. אם הוא לא בנוי במיוחד לזהות RTL - מתקבל בלגן.</p>

<h2>איך פותרים את זה בפועל?</h2>
<p><strong>1. תבדוק שהמנוע תומך רשמית ב-RTL</strong>, לא רק "תומך בעברית". יש הבדל בין הצגת גופן עברי לבין הבנת כיווניות טקסט אמיתית.</p>
<p><strong>2. אם המסמך סרוק</strong> - תעבור קודם דרך OCR שתומך בעברית (heb או heb+eng), לא רק אנגלית.</p>
<p><strong>3. אחרי ההמרה</strong>, תבדוק פסקה עם מספרים או מונחים באנגלית בתוכה - זו הבדיקה הכי אמינה לתקינות ה-RTL.</p>

<h2>מה עושים אם ההמרה כבר יצאה הפוכה?</h2>
<p>ברוב המקרים אין טעם "לתקן ידנית" - עדיף להמיר מחדש דרך כלי שתומך נכון ב-RTL, כי תיקון ידני של כיווניות בטקסט ארוך הוא עבודה איטית ומועדת לטעויות.</p>
"""
))

# ── 2. Electronic signature ───────────────────────────────────
ARTICLES.append(dict(
    slug="electronic-signature-pdf",
    title="איך לחתום על מסמך PDF בעברית בלי להדפיס",
    description="מדריך מלא לחתימה דיגיטלית על מסמכי PDF בעברית - בלי מדפסת, סורק או בזבוז זמן.",
    date="3 ביולי 2026", sort_date="2026-07-03",
    tag="חתימה",
    tool_link="/he/pdf-to-word/",
    tool_label="נסה כלי חתימה דיגיטלית",
    body_html="""
<p class="lead">"תדפיס, תחתום, תסרוק, תשלח בחזרה" - התהליך המסורתי לחתימה על מסמך לוקח בממוצע כמה עשרות דקות ודורש גישה למדפסת וסורק. חתימה דיגיטלית עושה את זה תוך שניות, ישירות מהמחשב או מהנייד.</p>

<h2>מה ההבדל בין "חתימה דיגיטלית" ל"חתימה אלקטרונית"?</h2>
<p><strong>חתימה אלקטרונית</strong> היא בפועל הוספת ייצוג ויזואלי של חתימה (כתב יד סרוק, טקסט מעוצב, או ציור עכבר/אצבע) לתוך המסמך. זה מספיק לרוב המסמכים היומיומיים - הסכמי שכירות, טפסים, אישורים פנימיים.</p>
<p><strong>חתימה דיגיטלית מאובטחת</strong> (עם תעודה דיגיטלית) מוסיפה גם שכבת הצפנה שמוכיחה מבחינה משפטית שהחותם הוא אכן מי שהוא טוען שהוא, ושהמסמך לא שונה אחרי החתימה. זו נדרשת בעיקר לחוזים מחייבים מבחינה משפטית, מסמכים מול רשויות, או עסקאות בעלות ערך גבוה.</p>

<h2>איך זה עובד בפועל עם מסמך בעברית?</h2>
<p>נקודה חשובה: כלי חתימה שלא תומך נכון ב-RTL עלול "לזרוק" את החתימה במקום הלא נכון על העמוד, במיוחד במסמכים שהטקסט בהם מיושר לימין. חשוב לוודא שהכלי שבו משתמשים מציג תצוגה מקדימה (preview) לפני השמירה הסופית, כדי לוודא שהחתימה יושבת בדיוק במקום הנכון.</p>

<h2>שלבי התהליך</h2>
<p><strong>1. העלאת המסמך</strong> - PDF קיים שצריך חתימה.</p>
<p><strong>2. הוספת החתימה</strong> - כתיבת שם מלא כטקסט מעוצב, או ציור חתימה ידנית עם העכבר/מסך מגע.</p>
<p><strong>3. מיקום מדויק</strong> - גרירת החתימה למקום הנכון בעמוד, תוך שימת לב במיוחד למסמכים בעברית שבהם השדות לרוב מיושרים לימין ולא לשמאל כמו במסמכים אנגליים.</p>
<p><strong>4. הורדה או שליחה</strong> - שמירת המסמך החתום ושליחתו ישירות מהדפדפן.</p>

<h2>מתי כדאי חתימה מאובטחת ולא רק חזותית?</h2>
<p>אם המסמך הוא חוזה בעל השלכות משפטיות משמעותיות, מומלץ לבדוק מול איש מקצוע (עורך דין) האם נדרשת חתימה דיגיטלית מאובטחת עם תעודה דיגיטלית מוכרת, ולא להסתפק בחתימה חזותית בלבד.</p>
"""
))

# ── 3. Password protected PDF (educational only) ──────────────
ARTICLES.append(dict(
    slug="pdf-password-protected",
    title="PDF מוגן סיסמה: מה עושים כשאיבדתם את הסיסמה",
    description="מה לעשות כשאיבדתם את הסיסמה לקובץ PDF שלכם - אפשרויות לגיטימיות בלבד.",
    date="5 ביולי 2026", sort_date="2026-07-05",
    tag="אבטחה",
    tool_link="/he/contact/",
    tool_label="פנה אלינו לייעוץ",
    body_html="""
<p class="lead">איבוד סיסמה לקובץ PDF חשוב - חוזה, תלוש שכר, מסמך רשמי - הוא תרחיש מתסכל ונפוץ. חשוב להבהיר מראש: המאמר הזה עוסק אך ורק במצבים שבהם אתם הבעלים הלגיטימיים של המסמך, ולא בעקיפת הגנות של קבצים שאינם שייכים לכם.</p>

<h2>קודם כל - האם אתה באמת חייב לפתוח את זה בעצמך?</h2>
<p>לפני שמנסים כל פתרון טכני, כדאי לבדוק את האפשרות הפשוטה ביותר: <strong>לפנות למי ששלח לך את הקובץ</strong> ולבקש את הסיסמה מחדש, או בקשה לקובץ חדש ללא הגנה. במקרים רבים זה הפתרון המהיר והבטוח ביותר, ולא כרוך בשום סיכון.</p>

<h2>מה אם המסמך שלך ואיבדת את הסיסמה בעצמך?</h2>
<p>אם זה מסמך שאתה יצרת או הגנת עליו בעצמך (למשל דוח שהגנת עליו בסיסמה ושכחת אותה):</p>
<p><strong>1. תבדוק מנהל סיסמאות</strong> - אם המסמך נשמר לאחרונה, ייתכן שהסיסמה נשמרה אוטומטית בדפדפן או במנהל סיסמאות שאתה משתמש בו.</p>
<p><strong>2. תבדוק גרסאות קודמות</strong> - אם המסמך נוצר מתוך Word או תוכנה אחרת, ייתכן שיש עותק לא-מוגן בגרסה ישנה יותר בגיבויים או ב-Google Drive/OneDrive.</p>
<p><strong>3. פנייה לתמיכה של התוכנה שיצרה את הקובץ</strong> - אם המסמך נוצר על ידי מערכת ארגונית (כמו מערכת שכר, מערכת בנקאית), לרוב יש למערכת עצמה יכולת להנפיק מחדש את המסמך ללא הגנה, בפניה ישירה לגורם שהנפיק אותו.</p>

<h2>למה לא ננסה "לפצח" את הסיסמה?</h2>
<p>כלים שמבטיחים "לפרוץ" סיסמת PDF עלולים להיות לא אמינים (לעיתים מכילים תוכנות זדוניות), ובנוסף - אם מדובר במסמך שאינו שלך, ניסיון לעקוף הגנה עליו עלול להיות גם בעייתי מבחינה משפטית. הדרך הבטוחה והנכונה תמיד עוברת דרך פנייה לבעל הזכויות החוקי על המסמך.</p>

<h2>מה עושים אחרי שפתחת את המסמך בהצלחה?</h2>
<p>אם ברצונך להסיר את ההגנה כדי שתוכל לגשת למסמך שלך בקלות בעתיד, יש לוודא שאתה עושה זאת רק במסמכים ששייכים לך, ולשמור את הגרסה החדשה במקום מאובטח (מנהל סיסמאות, אחסון מוצפן).</p>
"""
))

# ── 4. Broken PDF on mobile ────────────────────────────────────
ARTICLES.append(dict(
    slug="pdf-broken-mobile",
    title="5 טעויות שגורמות ל-PDF להיראות שבור בפתיחה בנייד",
    description="הסיבות הנפוצות ביותר לכך שקבצי PDF נראים שבורים, חתוכים או לא קריאים בטלפון הנייד.",
    date="7 ביולי 2026", sort_date="2026-07-07",
    tag="תאימות",
    tool_link="/he/compress-pdf/",
    tool_label="דחוס PDF לנייד עכשיו",
    body_html="""
<p class="lead">שלחתם PDF שנראה מושלם במחשב, אבל כשהלקוח או הבוס פתחו אותו בנייד - הטקסט חתוך, התמונות לא נטענות, או הכל נראה מיושר לא נכון. הנה חמש הסיבות הנפוצות ביותר, ואיך למנוע כל אחת מהן.</p>

<h2>1. גודל עמוד לא מותאם</h2>
<p>מסמכים שנוצרו לדפוס (כמו A3 או פוסטרים) לרוב לא נטענים כמו שצריך באפליקציות PDF בנייד שמצפות ליחס גובה-רוחב סטנדרטי. הפתרון: לפני שליחה, לוודא שהמסמך נוצר בגודל A4 או Letter רגיל, אלא אם יש סיבה ספציפית אחרת.</p>

<h2>2. גופנים לא מוטבעים (Embedded Fonts)</h2>
<p>אם הגופן שבו נוצר המסמך לא "מוטבע" בתוך קובץ ה-PDF עצמו, מכשירים אחרים (כולל טלפונים) מחליפים אותו בגופן ברירת מחדל - מה שגורם לפריסה כולה "לזוז" ולהיראות שבורה. רוב תוכנות היצירה (Word, Google Docs) מטביעות גופנים אוטומטית בעת ייצוא ל-PDF, אבל שווה לוודא זאת בהגדרות הייצוא.</p>

<h2>3. קובץ כבד מדי</h2>
<p>PDF עם תמונות ברזולוציה גבוהה מדי (למשל תמונות סריקה ב-600 DPI כשמספיק 150) עלול לקחת זמן רב להיטען בנייד, ובחיבור אינטרנט חלש - להיתקע באמצע או להיראות חלקי. דחיסת הקובץ פותרת את זה כמעט תמיד, בלי לפגוע משמעותית באיכות הקריאה.</p>

<h2>4. שכבות OCR שבורות</h2>
<p>אם המסמך עבר OCR (זיהוי טקסט אוטומטי) בצורה לא מוצלחת, לפעמים נוצרת "שכבת טקסט" מתחת לתמונה שמסתדרת לא נכון - וכשמנסים להעתיק טקסט או לחפש במסמך בנייד, מקבלים תוצאות מוזרות או המסמך "קופץ". הפתרון הוא לעבור על המסמך מחדש עם מנוע OCR איכותי, ולא רק "לחיות עם זה".</p>

<h2>5. כיווניות RTL שגויה במסמכים בעברית</h2>
<p>מסמך שנוצר בתוכנה שלא תומכת נכון בעברית עלול להיראות תקין במחשב (בעזרת תיקונים אוטומטיים של מערכת ההפעלה) אבל להתפרק בנייד, במיוחד באפליקציות PDF פשוטות יותר. פירוט מלא על הבעיה הזו ואיך לפתור אותה נמצא במדריך שלנו על <a href="/he/blog/pdf-hebrew-rtl/" style="color:var(--red)">RTL בהמרת PDF לעברית</a>.</p>

<h2>איך למנוע את כל זה מראש?</h2>
<p>הכלל הכי אמין: אחרי יצירת/המרת כל PDF חשוב, לפתוח אותו פעם אחת בטלפון (לא רק במחשב) לפני שליחה סופית. זה לוקח 10 שניות וחוסך הרבה מבוכה.</p>
"""
))

# ── 5. Compress ID/contract without hurting signature readability ──
ARTICLES.append(dict(
    slug="compress-id-contract-pdf",
    title="איך לדחוס PDF של תעודת זהות או חוזה בלי לפגוע בקריאות החתימה",
    description="מדריך לדחיסת מסמכים רגישים כמו תעודת זהות וחוזים, תוך שמירה על קריאות מלאה של הטקסט והחתימה.",
    date="8 ביולי 2026", sort_date="2026-07-08",
    tag="דחיסה",
    tool_link="/he/compress-pdf/",
    tool_label="דחוס PDF עכשיו",
    body_html="""
<p class="lead">כשמדובר במסמכים רגישים כמו תעודת זהות, חוזה חתום, או אישור בנקאי - יש איזון עדין: הקובץ צריך להיות קטן מספיק לשליחה במייל או העלאה למערכת, אבל בו זמנית ברור מספיק שאפשר לקרוא כל ספרה ולזהות את החתימה בבירור.</p>

<h2>למה דחיסה "רגילה" מסוכנת למסמכים כאלה</h2>
<p>דחיסה אגרסיבית מדי (כמו הגדרת "Extreme" בכלי דחיסה כלליים) מקטינה בעיקר את איכות התמונות - מה שיכול להפוך מספרי תעודת זהות למטושטשים או קווי חתימה לבלתי ברורים. במסמך רגיל זה פחות קריטי; במסמך שצריך זיהוי מדויק - זו בעיה של ממש.</p>

<h2>מה רמת הדחיסה הנכונה למסמכים רגישים?</h2>
<p><strong>רמה נמוכה-בינונית היא הבחירה הבטוחה.</strong> ברוב כלי הדחיסה יש כמה רמות (נמוכה, בינונית, גבוהה, מקסימלית) - רמה נמוכה שומרת כמעט את כל האיכות המקורית תוך הקטנת גודל הקובץ ב-10-30% בלבד, מה שברוב המקרים מספיק כדי לעבור מגבלות העלאה נפוצות (כמו 5MB או 10MB), בלי לפגוע בקריאות.</p>

<h2>בדיקה אחרי דחיסה - שלב שאסור לדלג עליו</h2>
<p>אחרי כל דחיסה של מסמך רגיש, מומלץ תמיד:</p>
<p><strong>1. להגדיל (זום) על מספרי תעודת הזהות</strong> - לוודא שכל ספרה ברורה וללא טשטוש.</p>
<p><strong>2. להגדיל על אזור החתימה</strong> - לוודא שקווי החתימה עדיין חדים ואפשר לזהות אותה בבירור אם יידרש אימות בעתיד.</p>
<p><strong>3. להשוות גודל קובץ לפני ואחרי</strong> - אם הקובץ ירד בהרבה אבל האיכות עדיין נראית תקינה בזום, זו סימן טוב שהדחיסה עבדה כמו שצריך.</p>

<h2>מה אם המסמך עדיין גדול מדי אחרי דחיסה קלה?</h2>
<p>אם אחרי דחיסה ברמה נמוכה הקובץ עדיין חורג ממגבלת ההעלאה, לפני שעוברים לרמת דחיסה גבוהה יותר (שעלולה לפגוע באיכות), כדאי לבדוק: האם המסמך כולל עמודים מיותרים שאפשר להסיר? האם אפשר לפצל למספר קבצים קטנים יותר במקום קובץ אחד גדול? אלה פתרונות ששומרים על איכות מלאה בלי לוותר על שום דבר.</p>
"""
))

LEGACY_CARDS_HE = """
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
"""

BLOG_INDEX_TEMPLATE_HE = """<!DOCTYPE html>
<html id="html-root" lang="he" dir="rtl">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<meta name="description" content="כלי PDF מקצועיים להמרה, מיזוג, פיצול, דחיסה, עריכה ותרגום קבצים אונליין.">
<title>בלוג PDFPro</title>
<link rel="canonical" href="https://www.pdfproapp.com/he/blog/">
<link rel="alternate" hreflang="en" href="https://www.pdfproapp.com/blog/">
<link rel="alternate" hreflang="he" href="https://www.pdfproapp.com/he/blog/">
<link rel="alternate" hreflang="x-default" href="https://www.pdfproapp.com/blog/">
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;600;700;800&family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet"/>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5792951933667466" crossorigin="anonymous"></script>
{GTAG_SNIPPET}
<style>{css}</style>
</head>
<body class="rtl">
{nav}
<div class="container">
  <div class="breadcrumb"><a href="/he/">בית</a> › <span>בלוג</span></div>
  <h1>בלוג</h1>
  <p class="lead">טיפים, מדריכים ועדכונים מצוות PDFPro.</p>
{cards}
</div>
{footer}
<script>{js}</script>
</body>
</html>
"""

BLOG_NAV_HE = """<nav>
  <a href="/he/" class="logo">PDF<span>Pro</span></a>
  <ul class="nav-links">
    <li><a href="/he/#tools">כלים</a></li>
    <li><a href="/he/#features">יתרונות</a></li>
    <li><a href="/he/pricing/">מחירים</a></li>
  </ul>
  <div class="nav-right">
    <span class="api-status offline" id="api-status"><span class="api-dot"></span><span id="api-status-text">מתחבר...</span></span>
    <button class="nav-cta" onclick="document.getElementById('tools')?.scrollIntoView({behavior:'smooth'})">התחל עכשיו</button>
  </div>
</nav>"""

BLOG_CARD_CSS_EXTRA = """
.container{max-width:860px;margin:0 auto;padding:3rem 1.5rem}
h1{font-size:2rem;font-weight:900;color:var(--navy);margin-bottom:1rem;letter-spacing:-0.5px}
.lead{font-size:1.05rem;line-height:1.8;margin-bottom:1.5rem}
.blog-card{background:white;border-radius:12px;border:1px solid var(--border);padding:1.5rem;margin-bottom:1rem;cursor:pointer;transition:border-color 0.2s,box-shadow 0.2s}
.blog-card:hover{border-color:var(--red);box-shadow:0 4px 16px rgba(224,32,32,0.08)}
.blog-card .blog-date{font-size:0.78rem;color:var(--muted)}
.blog-card h2{margin-top:0.4rem;font-size:1.05rem;margin-bottom:0}
.blog-card p{font-size:0.88rem}
"""


def build_blog_index_he(articles):
    sorted_articles = sorted(articles, key=lambda a: a["sort_date"], reverse=True)
    cards = ""
    for art in sorted_articles:
        cards += f"""
  <div class="blog-card" onclick="window.location.href='/he/blog/{art['slug']}/'">
    <p class="blog-date">{art['date']}</p>
    <span class="tag">{art['tag']}</span>
    <h2>{art['title']}</h2>
    <p>{art['description']}</p>
    <p style="color:var(--red);font-size:0.85rem;font-weight:600;margin-top:0.8rem">קרא עוד ←</p>
  </div>"""
    cards += LEGACY_CARDS_HE
    return BLOG_INDEX_TEMPLATE_HE.format(
        css=SHARED_CSS + BLOG_CARD_CSS_EXTRA,
        nav=BLOG_NAV_HE,
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
    out_dir = f"he/blog/{art['slug']}"
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✓ he/blog/{art['slug']}/index.html")

# Auto-build the blog listing page
os.makedirs("he/blog", exist_ok=True)
with open("he/blog/index.html", "w", encoding="utf-8") as f:
    f.write(build_blog_index_he(ARTICLES))
print("✓ he/blog/index.html (auto-generated listing)")

# Print sitemap lines to copy into sitemap.xml
print("\n--- Add these lines to sitemap.xml (Hebrew articles) ---")
for art in sorted(ARTICLES, key=lambda a: a["sort_date"], reverse=True):
    print(f'  <url><loc>https://www.pdfproapp.com/he/blog/{art["slug"]}/</loc><priority>0.6</priority></url>')

print("\nDone.")