#!/usr/bin/env python3
"""
PDFPro site generator — the ONLY build script for pdfproapp.com.

    python build.py            # builds every generated page + sitemap.xml + robots.txt

What it generates (EN + HE):
    tool pages      /<tool>/            /he/<tool>/        (from TOOLS below)
    static pages    /about/ ... /terms/ /he/about/ ...     (from PAGES below)
    blog index      /blog/              /he/blog/
    articles        /blog/<slug>/       /he/blog/<slug>/   (meta in ARTICLES, body in content/blog/<lang>/<slug>.html)
    sitemap.xml     with real <lastmod> (tracked in .build-manifest.json)
    robots.txt

NOT generated (hand-maintained for now): /index.html and /he/index.html (homepages).
They are included in the sitemap, but this script never overwrites them.

To add a tool:     add an entry to TOOLS.
To add an article: add an entry to ARTICLES + content/blog/en/<slug>.html + content/blog/he/<slug>.html.
"""
from __future__ import annotations

import hashlib
import html
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = "https://www.pdfproapp.com"
API = "https://pdfproweb.onrender.com"
ADSENSE_CLIENT = "ca-pub-5921716820042715"
GA_ID = "G-WJ3VYWT5RY"
CONTACT_EMAIL = "support@pdfproapp.com"   # make sure this inbox actually receives mail
MAX_MB = 100                              # matches MAX_FILE_SIZE_MB in the backend
LANGS = ("en", "he")

# ════════════════════════════════════════════════════════════════════════════
# UI STRINGS
# ════════════════════════════════════════════════════════════════════════════
UI = {
    "en": {
        "home": "Home", "tools": "Tools", "blog": "Blog", "pricing": "Pricing", "cta": "All tools",
        "online": "Server online", "waking": "Starting server…", "offline": "Server offline",
        "footer_desc": "Free online PDF tools with proper Hebrew and RTL support.",
        "company": "Company", "support": "Support", "about": "About", "contact": "Contact",
        "help": "Help center", "privacy": "Privacy policy", "terms": "Terms of use",
        "copy": f"© {date.today().year} PDFPro",
        "how": "How it works", "faq": "Frequently asked questions", "related": "Related tools",
        "guides": "Guides", "read": "Read guide",
        "drop": "Drop your file here or click to choose", "drop_multi": "Drop your files here or click to choose",
        "supports": "Accepted: {accept}. Up to {max} MB.",
        "privacy_line": "Files are processed on our server and deleted automatically after one hour.",
        "js": {
            "remove": "Remove", "move_up": "Move up",
            "need_more": "Add at least one more file.",
            "bad_type": "{name} isn't a supported file type.",
            "too_big": "{name} is larger than {max} MB.",
            "uploading": "Uploading and processing…",
            "waking": "The server is starting up. The first file can take up to a minute.",
            "done": "Your file is ready", "done_parts": "{n} files are ready",
            "download": "Download", "download_txt": "Download text (.txt)",
            "no_text": "No text was found. Try a clearer scan or a different language setting.",
            "saved": "File size reduced by {p}%.",
            "deleted_note": "Download now. The file is deleted from the server after one hour.",
            "expired": "This file has expired. Process it again to get a new copy.",
            "rate_limited": "Hourly limit reached for this tool. Try again in an hour.",
            "timeout": "The server took too long to respond. Try again, or try a smaller file.",
            "network": "Couldn't reach the server. Check your connection and try again.",
            "generic_error": "Something went wrong while processing the file",
            "pw_required": "Enter a password.",
            "pw_short": "The password must be at least {n} characters.",
            "pw_mismatch": "The two passwords don't match.",
        },
        "run": "Convert", "again": "Process another file",
    },
    "he": {
        "home": "בית", "tools": "כלים", "blog": "בלוג", "pricing": "מחירים", "cta": "כל הכלים",
        "online": "השרת פעיל", "waking": "השרת עולה…", "offline": "השרת לא זמין",
        "footer_desc": "כלי PDF חינמיים אונליין, עם תמיכה אמיתית בעברית ובכיווניות RTL.",
        "company": "החברה", "support": "תמיכה", "about": "אודות", "contact": "צור קשר",
        "help": "מרכז עזרה", "privacy": "מדיניות פרטיות", "terms": "תנאי שימוש",
        "copy": f"© {date.today().year} PDFPro",
        "how": "איך זה עובד", "faq": "שאלות נפוצות", "related": "כלים נוספים",
        "guides": "מדריכים", "read": "למדריך",
        "drop": "גררו קובץ לכאן או לחצו לבחירה", "drop_multi": "גררו קבצים לכאן או לחצו לבחירה",
        "supports": "סוגי קבצים: {accept}. עד {max}MB.",
        "privacy_line": "הקבצים מעובדים בשרת שלנו ונמחקים אוטומטית אחרי שעה.",
        "js": {
            "remove": "הסר", "move_up": "הזז למעלה",
            "need_more": "הוסיפו לפחות קובץ אחד נוסף.",
            "bad_type": "סוג הקובץ {name} לא נתמך.",
            "too_big": "הקובץ {name} גדול מ-{max}MB.",
            "uploading": "מעלה ומעבד…",
            "waking": "השרת מתעורר. הקובץ הראשון יכול לקחת עד דקה.",
            "done": "הקובץ מוכן", "done_parts": "{n} קבצים מוכנים",
            "download": "הורדת", "download_txt": "הורדת הטקסט (txt.)",
            "no_text": "לא נמצא טקסט. נסו סריקה ברורה יותר או שפה אחרת.",
            "saved": "גודל הקובץ קטן ב-{p}%.",
            "deleted_note": "הורידו עכשיו. הקובץ נמחק מהשרת אחרי שעה.",
            "expired": "תוקף הקובץ פג. עבדו אותו שוב כדי לקבל עותק חדש.",
            "rate_limited": "הגעתם למגבלה השעתית של הכלי. נסו שוב בעוד שעה.",
            "timeout": "השרת לא הגיב בזמן. נסו שוב או נסו קובץ קטן יותר.",
            "network": "אין חיבור לשרת. בדקו את החיבור ונסו שוב.",
            "generic_error": "משהו השתבש בעיבוד הקובץ",
            "pw_required": "הקלידו סיסמה.",
            "pw_short": "הסיסמה צריכה להכיל לפחות {n} תווים.",
            "pw_mismatch": "שתי הסיסמאות לא תואמות.",
        },
        "run": "המר", "again": "עיבוד קובץ נוסף",
    },
}

# ════════════════════════════════════════════════════════════════════════════
# TOOLS — one entry per tool page. `api` must match the FastAPI backend.
# ════════════════════════════════════════════════════════════════════════════
TOOLS = [
    {
        "slug": "pdf-to-word", "limit": 20,
        "api": {"endpoint": "/api/convert/pdf-to-word", "field": "file", "multi": False, "accept": ".pdf", "result": "file"},
        "options": [],
        "en": {
            "name": "PDF to Word",
            "title": "PDF to Word Converter – Free, Keeps Hebrew Intact | PDFPro",
            "desc": "Convert PDF to an editable Word (.docx) file for free. Keeps layout, tables and right-to-left Hebrew text in order. No sign-up.",
            "h1": "PDF to Word converter",
            "lead": "Turn a PDF into an editable Word document. Layout, tables and images are kept, and Hebrew or Arabic text stays in the right order.",
            "run": "Convert to Word",
            "steps": [
                ("Choose your PDF", "Drop the file into the box above or click to pick it from your device."),
                ("Convert", "The file is rebuilt as a .docx document with its paragraphs, tables and images."),
                ("Download", "Save the Word file and edit it in Word, Google Docs or LibreOffice."),
            ],
            "faqs": [
                ("Is it free?", "Yes. There's no sign-up and no watermark. Each tool has an hourly limit to keep the service available for everyone."),
                ("Will the formatting be kept?", "Text, fonts, tables and images are kept as closely as possible. Very complex layouts, like magazines with overlapping elements, may need small fixes afterwards."),
                ("Does it work with Hebrew PDFs?", "Yes. Right-to-left text is detected so Hebrew words and sentences don't come out reversed. Mixed Hebrew and English paragraphs keep their order."),
                ("Can I convert a scanned PDF?", "A scanned PDF is an image of text, so there's nothing to convert directly. Use the OCR tool and choose Word as the output format instead."),
                ("What's the maximum file size?", f"Up to {MAX_MB} MB per file."),
            ],
            "related": ["ocr-pdf", "pdf-to-excel", "compress-pdf"],
        },
        "he": {
            "name": "PDF ל-Word",
            "title": "המרת PDF ל-Word בחינם – עברית בלי טקסט הפוך | PDFPro",
            "desc": "המרת PDF לקובץ Word (docx) שאפשר לערוך, בחינם ובלי הרשמה. שומר על הפריסה, הטבלאות וכיווניות העברית.",
            "h1": "המרת PDF ל-Word",
            "lead": "הופכים PDF למסמך Word שאפשר לערוך. הפריסה, הטבלאות והתמונות נשמרות, והטקסט בעברית נשאר בסדר הנכון ולא מתהפך.",
            "run": "המר ל-Word",
            "steps": [
                ("בוחרים את ה-PDF", "גוררים את הקובץ לתיבה למעלה או לוחצים ובוחרים אותו מהמחשב או מהטלפון."),
                ("ממירים", "הקובץ נבנה מחדש כמסמך docx עם הפסקאות, הטבלאות והתמונות."),
                ("מורידים", "שומרים את קובץ ה-Word ועורכים אותו ב-Word, ב-Google Docs או ב-LibreOffice."),
            ],
            "faqs": [
                ("זה באמת בחינם?", "כן. בלי הרשמה ובלי סימן מים. לכל כלי יש מגבלה שעתית כדי שהשירות יישאר זמין לכולם."),
                ("העיצוב נשמר?", "טקסט, גופנים, טבלאות ותמונות נשמרים כמה שיותר קרוב למקור. פריסות מורכבות מאוד, כמו עיתון עם אלמנטים חופפים, עשויות לדרוש תיקונים קטנים."),
                ("זה עובד עם PDF בעברית?", "כן. הכלי מזהה טקסט מימין לשמאל כך שמילים ומשפטים בעברית לא יוצאים הפוכים. פסקאות שמשלבות עברית ואנגלית שומרות על הסדר."),
                ("אפשר להמיר PDF סרוק?", "PDF סרוק הוא בעצם תמונה של טקסט, ולכן אין מה להמיר ישירות. השתמשו בכלי ה-OCR ובחרו Word כפורמט הפלט."),
                ("מה גודל הקובץ המקסימלי?", f"עד {MAX_MB}MB לקובץ."),
            ],
            "related": ["ocr-pdf", "pdf-to-excel", "compress-pdf"],
        },
    },
    {
        "slug": "pdf-to-excel", "limit": 20,
        "api": {"endpoint": "/api/convert/pdf-to-excel", "field": "file", "multi": False, "accept": ".pdf", "result": "file"},
        "options": [],
        "en": {
            "name": "PDF to Excel",
            "title": "Free PDF to Excel Converter Online – No Sign-Up | PDFPro",
            "desc": "Convert PDF to Excel free and online, with no sign-up and nothing to download. Every table becomes its own sheet in an .xlsx spreadsheet.",
            "h1": "PDF to Excel converter",
            "lead": "Pull the tables out of a PDF and into an Excel spreadsheet, ready to sort, filter and calculate.",
            "run": "Convert to Excel",
            "steps": [
                ("Choose your PDF", "Pick a PDF that contains tables, like a bank statement, price list or report."),
                ("Extract tables", "Each table is detected and placed on its own sheet, named by page number."),
                ("Download", "Open the .xlsx file in Excel, Google Sheets or LibreOffice Calc."),
            ],
            "faqs": [
                ("What if the PDF has several tables?", "Every table goes to a separate sheet, labeled with the page it came from, so nothing gets merged by mistake."),
                ("Does it work with scanned PDFs?", "Table extraction needs real text in the PDF. For a scan, run it through the OCR tool first."),
                ("Is it free?", "Yes, with an hourly limit per tool and no sign-up."),
                ("Do I need to download or install anything?", "No. The converter runs in your browser, on any computer or phone. You only download the finished Excel file."),
                ("Can I open the result in Google Sheets?", "Yes. Upload the .xlsx file to Google Drive and open it with Google Sheets, or use File, Import in an existing sheet."),
                ("What's the maximum file size?", f"Up to {MAX_MB} MB per file."),
            ],
            "related": ["pdf-to-word", "ocr-pdf", "split-pdf"],
        },
        "he": {
            "name": "PDF ל-Excel",
            "title": "המרת PDF ל-Excel בחינם – חילוץ טבלאות | PDFPro",
            "desc": "חילוץ טבלאות מקובץ PDF לגיליון Excel (xlsx). כל טבלה בגיליון נפרד. בחינם ובלי הרשמה.",
            "h1": "המרת PDF ל-Excel",
            "lead": "מוציאים את הטבלאות מתוך ה-PDF לגיליון Excel, מוכן למיון, סינון וחישובים.",
            "run": "המר ל-Excel",
            "steps": [
                ("בוחרים את ה-PDF", "קובץ שיש בו טבלאות, כמו דף חשבון בנק, מחירון או דוח."),
                ("מחלצים טבלאות", "כל טבלה מזוהה ומועברת לגיליון נפרד, עם שם לפי מספר העמוד."),
                ("מורידים", "פותחים את קובץ ה-xlsx ב-Excel, ב-Google Sheets או ב-LibreOffice."),
            ],
            "faqs": [
                ("מה אם יש כמה טבלאות?", "כל טבלה עוברת לגיליון נפרד עם שם העמוד שממנו הגיעה, כך ששום דבר לא מתערבב."),
                ("זה עובד עם PDF סרוק?", "חילוץ טבלאות דורש טקסט אמיתי בקובץ. אם זו סריקה, העבירו אותה קודם דרך כלי ה-OCR."),
                ("זה בחינם?", "כן, בלי הרשמה, עם מגבלה שעתית לכל כלי."),
                ("מה גודל הקובץ המקסימלי?", f"עד {MAX_MB}MB לקובץ."),
            ],
            "related": ["pdf-to-word", "ocr-pdf", "split-pdf"],
        },
    },
    {
        "slug": "compress-pdf", "limit": 20,
        "api": {"endpoint": "/api/organize/compress", "field": "file", "multi": False, "accept": ".pdf", "result": "file"},
        "options": [
            {"name": "level", "type": "select", "default": "medium",
             "values": ["low", "medium", "high", "extreme"],
             "en": {"label": "Compression level", "labels": ["Low (best quality)", "Medium (recommended)", "High", "Extreme (smallest file)"]},
             "he": {"label": "רמת דחיסה", "labels": ["נמוכה (איכות מקסימלית)", "בינונית (מומלץ)", "גבוהה", "מקסימלית (הקובץ הקטן ביותר)"]}},
        ],
        "en": {
            "name": "Compress PDF",
            "title": "Compress PDF – Reduce PDF File Size Free | PDFPro",
            "desc": "Make a PDF smaller for email or upload forms. Choose how much to compress, keep text sharp. Free, no sign-up.",
            "h1": "Compress PDF",
            "lead": "Shrink a PDF so it fits email attachments and upload limits on government, bank and job sites. Text stays sharp, images are optimized.",
            "run": "Compress PDF",
            "steps": [
                ("Choose your PDF", "Drop the file into the box above."),
                ("Pick a level", "Medium suits most files. Use Extreme only when you must fit a strict size limit."),
                ("Download", "Save the smaller PDF. The result shows how much space was saved."),
            ],
            "faqs": [
                ("How much smaller will my PDF get?", "It depends on what's inside. Files with lots of photos or scans shrink the most. A PDF that is mostly text is already small and won't change much."),
                ("Will compression hurt the quality?", "Text and vector graphics aren't touched. Images are re-encoded, so higher levels make photos softer. Low is close to the original."),
                ("Which level should I choose?", "Medium for everyday use. If a website still rejects the file, try High, then Extreme."),
                ("Will signatures stay readable?", "On Low and Medium, yes. Check the result before sending if you used High or Extreme on a signed document."),
            ],
            "related": ["merge-pdf", "split-pdf", "pdf-to-word"],
        },
        "he": {
            "name": "דחיסת PDF",
            "title": "דחיסת PDF – הקטנת קובץ PDF בחינם | PDFPro",
            "desc": "הקטנת קובץ PDF לשליחה במייל או להעלאה לאתרים עם מגבלת גודל. בוחרים רמת דחיסה, הטקסט נשאר חד. בחינם.",
            "h1": "דחיסת PDF",
            "lead": "מקטינים PDF כך שיעבור במייל ובמגבלות ההעלאה של אתרי ממשלה, בנקים ומשאבי אנוש. הטקסט נשאר חד והתמונות עוברות אופטימיזציה.",
            "run": "דחוס PDF",
            "steps": [
                ("בוחרים את ה-PDF", "גוררים את הקובץ לתיבה למעלה."),
                ("בוחרים רמה", "בינונית מתאימה לרוב הקבצים. מקסימלית רק כשצריך לעמוד במגבלת גודל קשוחה."),
                ("מורידים", "שומרים את הקובץ הקטן. בתוצאה מופיע כמה מקום נחסך."),
            ],
            "faqs": [
                ("בכמה הקובץ יקטן?", "תלוי בתוכן. קבצים עם הרבה תמונות או סריקות מתכווצים הכי הרבה. PDF שהוא בעיקר טקסט כבר קטן ולא ישתנה הרבה."),
                ("הדחיסה פוגעת באיכות?", "טקסט וגרפיקה וקטורית לא משתנים. התמונות מקודדות מחדש, ולכן ברמות גבוהות תמונות נראות רכות יותר. ברמה נמוכה התוצאה קרובה למקור."),
                ("איזו רמה לבחור?", "בינונית לשימוש יומיומי. אם אתר עדיין דוחה את הקובץ, נסו גבוהה ואז מקסימלית."),
                ("החתימה תישאר קריאה?", "ברמה נמוכה ובינונית כן. אם השתמשתם בגבוהה או מקסימלית על מסמך חתום, בדקו את התוצאה לפני השליחה."),
            ],
            "related": ["merge-pdf", "split-pdf", "pdf-to-word"],
        },
    },
    {
        "slug": "merge-pdf", "limit": 15,
        "api": {"endpoint": "/api/organize/merge", "field": "files", "multi": True, "minFiles": 2, "accept": ".pdf", "result": "file"},
        "options": [],
        "en": {
            "name": "Merge PDF",
            "title": "Merge PDF – Combine PDF Files into One Free | PDFPro",
            "desc": "Combine up to 20 PDF files into a single PDF, in the order you choose. Free, no sign-up, no watermark.",
            "h1": "Merge PDF files",
            "lead": "Combine several PDFs into one file. Add them, set the order, and download a single PDF.",
            "run": "Merge PDFs",
            "steps": [
                ("Add your PDFs", "Choose between 2 and 20 files. You can add more in several rounds."),
                ("Set the order", "Use Move up to reorder. The first file in the list becomes the first pages."),
                ("Download", "Save the combined PDF."),
            ],
            "faqs": [
                ("How many files can I merge?", "Between 2 and 20 PDFs at once."),
                ("Does merging reduce quality?", "No. Pages are copied as they are, nothing is re-compressed."),
                ("Can I merge password-protected PDFs?", "Not directly. Remove the password first with the Unlock PDF tool, then merge."),
                ("The merged file is too big. What now?", "Run it through Compress PDF after merging."),
            ],
            "related": ["split-pdf", "compress-pdf", "unlock-pdf"],
        },
        "he": {
            "name": "מיזוג PDF",
            "title": "מיזוג PDF – איחוד כמה קבצי PDF לקובץ אחד בחינם | PDFPro",
            "desc": "איחוד של עד 20 קבצי PDF לקובץ אחד, בסדר שתבחרו. בחינם, בלי הרשמה ובלי סימן מים.",
            "h1": "מיזוג קבצי PDF",
            "lead": "מאחדים כמה קבצי PDF לקובץ אחד. מוסיפים, קובעים סדר ומורידים PDF אחד.",
            "run": "מזג קבצים",
            "steps": [
                ("מוסיפים קבצים", "בין 2 ל-20 קבצים. אפשר להוסיף בכמה סבבים."),
                ("קובעים סדר", "משתמשים ב'הזז למעלה'. הקובץ הראשון ברשימה יהיה העמודים הראשונים."),
                ("מורידים", "שומרים את ה-PDF המאוחד."),
            ],
            "faqs": [
                ("כמה קבצים אפשר למזג?", "בין 2 ל-20 קבצי PDF בפעם אחת."),
                ("המיזוג פוגע באיכות?", "לא. העמודים מועתקים כמו שהם, בלי דחיסה מחדש."),
                ("אפשר למזג PDF מוגן בסיסמה?", "לא ישירות. מסירים קודם את הסיסמה בכלי הסרת סיסמה מ-PDF, ואז ממזגים."),
                ("הקובץ המאוחד גדול מדי, מה עושים?", "מעבירים אותו אחרי המיזוג דרך דחיסת PDF."),
            ],
            "related": ["split-pdf", "compress-pdf", "unlock-pdf"],
        },
    },
    {
        "slug": "split-pdf", "limit": 15,
        "api": {"endpoint": "/api/organize/split", "field": "file", "multi": False, "accept": ".pdf", "result": "parts"},
        "options": [
            {"name": "mode", "type": "hidden", "default": "ranges"},
            {"name": "ranges", "type": "text", "default": "1-3",
             "en": {"label": "Page ranges", "hint": "Separate ranges with commas, e.g. 1-3,4-6 or just 5 for a single page."},
             "he": {"label": "טווחי עמודים", "hint": "מפרידים בפסיקים, לדוגמה 1-3,4-6 או רק 5 לעמוד בודד."}},
        ],
        "en": {
            "name": "Split PDF",
            "title": "Split PDF – Extract Pages from a PDF Free | PDFPro",
            "desc": "Split a PDF by page ranges or pull out a single page. Each range becomes its own PDF. Free, no sign-up.",
            "h1": "Split PDF",
            "lead": "Cut a long PDF into smaller files, or pull out just the pages you need.",
            "run": "Split PDF",
            "steps": [
                ("Choose your PDF", "Drop the file into the box above."),
                ("Enter page ranges", "Write the ranges you want, like 1-3,4-6. Each range becomes a separate file."),
                ("Download", "Save each part."),
            ],
            "faqs": [
                ("How do I extract one page?", "Type just that page number, for example 5."),
                ("Can I get several separate parts?", "Yes. 1-2,3-5,6-10 gives you three PDFs."),
                ("Does splitting change the quality?", "No. Pages are copied exactly."),
                ("What's the maximum file size?", f"Up to {MAX_MB} MB per file."),
            ],
            "related": ["merge-pdf", "compress-pdf", "pdf-to-word"],
        },
        "he": {
            "name": "פיצול PDF",
            "title": "פיצול PDF – חילוץ עמודים מקובץ PDF בחינם | PDFPro",
            "desc": "פיצול PDF לפי טווחי עמודים או חילוץ עמוד בודד. כל טווח הופך ל-PDF נפרד. בחינם ובלי הרשמה.",
            "h1": "פיצול PDF",
            "lead": "חותכים PDF ארוך לקבצים קטנים, או מוציאים רק את העמודים שצריך.",
            "run": "פצל PDF",
            "steps": [
                ("בוחרים את ה-PDF", "גוררים את הקובץ לתיבה למעלה."),
                ("כותבים טווחי עמודים", "למשל 1-3,4-6. כל טווח הופך לקובץ נפרד."),
                ("מורידים", "שומרים כל חלק."),
            ],
            "faqs": [
                ("איך מוציאים עמוד אחד?", "כותבים רק את מספר העמוד, למשל 5."),
                ("אפשר לקבל כמה חלקים נפרדים?", "כן. 1-2,3-5,6-10 ייתן שלושה קבצים."),
                ("הפיצול משנה את האיכות?", "לא. העמודים מועתקים בדיוק."),
                ("מה גודל הקובץ המקסימלי?", f"עד {MAX_MB}MB לקובץ."),
            ],
            "related": ["merge-pdf", "compress-pdf", "pdf-to-word"],
        },
    },
    {
        "slug": "ocr-pdf", "limit": 10,
        "api": {"endpoint": "/api/ocr/extract", "field": "file", "multi": False, "accept": ".pdf,.jpg,.jpeg,.png", "result": "text"},
        "options": [
            {"name": "language", "type": "select", "default": "heb+eng",
             "values": ["heb+eng", "heb", "eng", "ara"],
             "en": {"label": "Document language", "labels": ["Hebrew + English", "Hebrew", "English", "Arabic"]},
             "he": {"label": "שפת המסמך", "labels": ["עברית + אנגלית", "עברית", "אנגלית", "ערבית"]}},
            {"name": "output_format", "type": "select", "default": "txt",
             "values": ["txt", "docx", "pdf"],
             "en": {"label": "Output", "labels": ["Plain text", "Word document", "Searchable PDF"]},
             "he": {"label": "פורמט פלט", "labels": ["טקסט", "מסמך Word", "PDF עם טקסט לחיפוש"]}},
        ],
        "en": {
            "name": "OCR PDF",
            "title": "OCR Hebrew & English – Extract Text from Scanned PDF | PDFPro",
            "desc": "Extract text from scanned PDFs and photos with OCR. Works with Hebrew, English and Arabic. Get text, Word or a searchable PDF.",
            "h1": "OCR: extract text from scans",
            "lead": "Turn a scanned document or a photo of a page into text you can copy, search and edit. Hebrew, English and Arabic are supported, including mixed documents.",
            "run": "Extract text",
            "steps": [
                ("Upload a scan or photo", "PDF, JPG or PNG. A straight, well-lit photo gives the best result."),
                ("Pick the language", "Choose Hebrew + English for documents that mix both."),
                ("Get the text", "Copy it, download it as text, or get a Word file or searchable PDF."),
            ],
            "faqs": [
                ("Does OCR work with Hebrew?", "Yes. Choose Hebrew or Hebrew + English. Text is returned right-to-left in the correct order."),
                ("How accurate is it?", "Clean, high-resolution scans come out very accurately. Blurry photos, handwriting and very small fonts reduce accuracy."),
                ("Which files can I upload?", "PDF, JPG and PNG."),
                ("Can I get an editable Word file?", "Yes. Set the output to Word document."),
            ],
            "related": ["pdf-to-word", "translate-pdf", "compress-pdf"],
        },
        "he": {
            "name": "OCR לעברית",
            "title": "OCR בעברית – חילוץ טקסט מ-PDF סרוק ומתמונה | PDFPro",
            "desc": "חילוץ טקסט ממסמכים סרוקים ומתמונות עם OCR. עובד עם עברית, אנגלית וערבית. מקבלים טקסט, Word או PDF עם חיפוש.",
            "h1": "OCR: חילוץ טקסט מסריקות",
            "lead": "הופכים מסמך סרוק או צילום של דף לטקסט שאפשר להעתיק, לחפש ולערוך. תומך בעברית, אנגלית וערבית, כולל מסמכים מעורבים.",
            "run": "חלץ טקסט",
            "steps": [
                ("מעלים סריקה או צילום", "PDF, JPG או PNG. צילום ישר ומואר נותן את התוצאה הטובה ביותר."),
                ("בוחרים שפה", "עברית + אנגלית למסמכים שמשלבים את שתיהן."),
                ("מקבלים את הטקסט", "מעתיקים, מורידים כטקסט, או מקבלים קובץ Word או PDF עם חיפוש."),
            ],
            "faqs": [
                ("ה-OCR עובד בעברית?", "כן. בוחרים עברית או עברית + אנגלית. הטקסט חוזר מימין לשמאל ובסדר הנכון."),
                ("כמה זה מדויק?", "סריקות נקיות וברזולוציה טובה יוצאות מדויקות מאוד. צילום מטושטש, כתב יד וגופן קטן מאוד מורידים את הדיוק."),
                ("אילו קבצים אפשר להעלות?", "PDF, JPG ו-PNG."),
                ("אפשר לקבל קובץ Word לעריכה?", "כן. בוחרים 'מסמך Word' בפורמט הפלט."),
            ],
            "related": ["pdf-to-word", "translate-pdf", "compress-pdf"],
        },
    },
    {
        "slug": "translate-pdf", "limit": 5,
        "api": {"endpoint": "/api/translate/pdf", "field": "file", "multi": False, "accept": ".pdf", "result": "file"},
        "options": [
            {"name": "target_language", "type": "select", "default": {"en": "iw", "he": "en"},
             "values": ["iw", "en", "ar", "ru", "fr", "de", "es"],
             "en": {"label": "Translate to", "labels": ["Hebrew", "English", "Arabic", "Russian", "French", "German", "Spanish"]},
             "he": {"label": "לתרגם ל", "labels": ["עברית", "אנגלית", "ערבית", "רוסית", "צרפתית", "גרמנית", "ספרדית"]}},
            {"name": "preserve_layout", "type": "select", "default": "true",
             "values": ["true", "false"],
             "en": {"label": "Keep original layout", "labels": ["Yes", "No, plain text"]},
             "he": {"label": "שמירת הפריסה המקורית", "labels": ["כן", "לא, טקסט רגיל"]}},
        ],
        "en": {
            "name": "Translate PDF",
            "title": "Translate PDF – Hebrew ↔ English and More, Free | PDFPro",
            "desc": "Translate a PDF between Hebrew, English, Arabic, Russian, French, German and Spanish, keeping the layout. Free online.",
            "h1": "Translate a PDF",
            "lead": "Translate a whole PDF into another language and get it back as a PDF, with the original layout kept where possible.",
            "run": "Translate PDF",
            "steps": [
                ("Choose your PDF", "The PDF needs real text. For scans, run OCR first."),
                ("Pick the target language", "The source language is detected automatically."),
                ("Download", "Save the translated PDF."),
            ],
            "faqs": [
                ("Which languages are supported?", "Hebrew, English, Arabic, Russian, French, German and Spanish."),
                ("Is the layout kept?", "With Keep original layout on, text is placed back where it was. Long translations can overflow small boxes."),
                ("Is the translation good enough for official use?", "It's machine translation, fine for understanding a document. For legal or official submissions, use a certified translator."),
                ("Why is there a lower limit on this tool?", "Translation is the heaviest tool to run, so it allows fewer files per hour."),
            ],
            "related": ["ocr-pdf", "pdf-to-word", "compress-pdf"],
        },
        "he": {
            "name": "תרגום PDF",
            "title": "תרגום PDF לעברית ומעברית – בחינם אונליין | PDFPro",
            "desc": "תרגום קובץ PDF בין עברית, אנגלית, ערבית, רוסית, צרפתית, גרמנית וספרדית, עם שמירה על הפריסה. בחינם.",
            "h1": "תרגום קובץ PDF",
            "lead": "מתרגמים PDF שלם לשפה אחרת ומקבלים אותו בחזרה כ-PDF, עם הפריסה המקורית ככל האפשר.",
            "run": "תרגם PDF",
            "steps": [
                ("בוחרים את ה-PDF", "הקובץ צריך להכיל טקסט אמיתי. אם זו סריקה, מעבירים קודם ב-OCR."),
                ("בוחרים שפת יעד", "שפת המקור מזוהה אוטומטית."),
                ("מורידים", "שומרים את ה-PDF המתורגם."),
            ],
            "faqs": [
                ("אילו שפות נתמכות?", "עברית, אנגלית, ערבית, רוסית, צרפתית, גרמנית וספרדית."),
                ("הפריסה נשמרת?", "כששמירת הפריסה מופעלת, הטקסט חוזר למקום שבו היה. תרגום ארוך יכול לחרוג מתיבות קטנות."),
                ("התרגום מספיק טוב לשימוש רשמי?", "זה תרגום מכונה, מתאים להבנת המסמך. למסמכים משפטיים או רשמיים עדיף מתרגם מוסמך."),
                ("למה המגבלה בכלי הזה נמוכה יותר?", "תרגום הוא הכלי הכבד ביותר להרצה, ולכן מותר בו פחות קבצים בשעה."),
            ],
            "related": ["ocr-pdf", "pdf-to-word", "compress-pdf"],
        },
    },
    {
        "slug": "unlock-pdf", "limit": 20,
        "api": {"endpoint": "/api/edit/unlock", "field": "file", "multi": False, "accept": ".pdf", "result": "file"},
        "options": [
            {"name": "password", "type": "password", "autocomplete": "current-password",
             "en": {"label": "The file's current password", "hint": "This is the password you type today to open the file."},
             "he": {"label": "הסיסמה הנוכחית של הקובץ", "hint": "הסיסמה שאתם מקלידים היום כדי לפתוח את הקובץ."}},
        ],
        "en": {
            "name": "Unlock PDF",
            "title": "Remove Password from PDF – Unlock PDF Free | PDFPro",
            "desc": "Remove the password from a PDF you can already open, so it stops asking every time. Free, no sign-up, files deleted after an hour.",
            "h1": "Remove a password from a PDF",
            "lead": "Tired of typing the same password every time you open a file? Enter it once here and download a copy that opens without it.",
            "run": "Remove password",
            "errors": {"403": "That password is incorrect. Check it and try again. Passwords are case-sensitive."},
            "steps": [
                ("Choose the locked PDF", "Drop the file into the box above."),
                ("Enter its password", "Type the password you normally use to open it."),
                ("Download the unlocked copy", "The new file opens without asking for a password."),
            ],
            "faqs": [
                ("Can you unlock a PDF if I forgot the password?", "No. The tool needs the correct password. It removes protection you can already open, it doesn't break it."),
                ("Does removing the password change the document?", "No. Pages, text, images and quality stay the same. Only the encryption is removed."),
                ("It says the password is wrong, but I'm sure it's right.", "Passwords are case-sensitive, and some keyboards switch language without you noticing. Try typing it in a text editor first and pasting it in."),
                ("Why can't other tools open my file?", "Encrypted PDFs can't be merged, compressed or converted until the password is removed. Unlock it here first, then use the other tool."),
            ],
            "related": ["protect-pdf", "merge-pdf", "compress-pdf"],
        },
        "he": {
            "name": "הסרת סיסמה מ-PDF",
            "title": "הסרת סיסמה מקובץ PDF בחינם – ביטול הגנה | PDFPro",
            "desc": "מסירים את הסיסמה מ-PDF שאתם כבר יודעים לפתוח, כמו תלוש שכר או דוח בנק, כדי שלא יבקש אותה כל פעם. בחינם ובלי הרשמה.",
            "h1": "הסרת סיסמה מקובץ PDF",
            "lead": "נמאס להקליד את אותה סיסמה בכל פעם שפותחים את הקובץ? מקלידים אותה כאן פעם אחת ומורידים עותק שנפתח בלי סיסמה.",
            "run": "הסר סיסמה",
            "errors": {"403": "הסיסמה שגויה. בדקו אותה ונסו שוב. יש הבדל בין אותיות גדולות לקטנות."},
            "steps": [
                ("בוחרים את ה-PDF הנעול", "גוררים את הקובץ לתיבה למעלה."),
                ("מקלידים את הסיסמה", "את הסיסמה שבה אתם פותחים אותו בדרך כלל, למשל מספר תעודת הזהות."),
                ("מורידים עותק פתוח", "הקובץ החדש נפתח בלי לבקש סיסמה."),
            ],
            "faqs": [
                ("אפשר לפתוח PDF אם שכחתי את הסיסמה?", "לא. הכלי צריך את הסיסמה הנכונה. הוא מסיר הגנה שאתם כבר יכולים לפתוח, ולא פורץ אותה."),
                ("הסרת הסיסמה משנה את המסמך?", "לא. העמודים, הטקסט, התמונות והאיכות נשארים אותו דבר. רק ההצפנה יורדת."),
                ("כתוב שהסיסמה שגויה, אבל אני בטוח שהיא נכונה", "יש הבדל בין אותיות גדולות לקטנות, ולפעמים המקלדת עוברת לעברית בלי ששמים לב. נסו להקליד את הסיסמה בפנקס רשימות ולהדביק אותה."),
                ("מה הסיסמה של תלוש השכר שלי?", "ברוב המקרים זה מספר תעודת הזהות, לפעמים בלי ספרת הביקורת. אם זה לא עובד, מחלקת השכר או מי ששלח את המסמך יכולים להגיד לכם."),
                ("למה כלים אחרים לא מצליחים לפתוח את הקובץ?", "אי אפשר למזג, לדחוס או להמיר PDF מוצפן לפני שמסירים את הסיסמה. מסירים אותה כאן ואז משתמשים בכלי השני."),
            ],
            "related": ["protect-pdf", "merge-pdf", "compress-pdf"],
        },
    },
    {
        "slug": "protect-pdf", "limit": 20,
        "api": {"endpoint": "/api/edit/protect", "field": "file", "multi": False, "accept": ".pdf", "result": "file"},
        "options": [
            {"name": "password", "type": "password", "autocomplete": "new-password", "minlength": 4, "confirm": True,
             "en": {"label": "New password", "confirm_label": "Repeat the password", "hint": "At least 4 characters. Share it with the recipient separately, not in the same email."},
             "he": {"label": "סיסמה חדשה", "confirm_label": "הקלידו שוב את הסיסמה", "hint": "לפחות 4 תווים. שלחו אותה לנמען בנפרד, לא באותו מייל."}},
        ],
        "en": {
            "name": "Password protect PDF",
            "title": "Password Protect PDF – Add a Password to a PDF Free | PDFPro",
            "desc": "Lock a PDF with a password using AES-256 encryption before you email or share it. Free, no sign-up.",
            "h1": "Add a password to a PDF",
            "lead": "Lock a PDF so only people with the password can open it. Useful before emailing ID scans, contracts, pay slips or medical documents.",
            "run": "Protect PDF",
            "steps": [
                ("Choose your PDF", "Drop the file into the box above."),
                ("Set a password", "Type it twice to avoid typos."),
                ("Download the protected file", "It will ask for the password every time it's opened."),
            ],
            "faqs": [
                ("What encryption is used?", "AES-256, supported by every modern PDF reader, including Adobe Acrobat, browsers and phone apps."),
                ("Can the recipient print the file?", "Yes. After opening it with the password, printing is allowed. Copying text and editing are restricted in readers that respect PDF permissions."),
                ("What if I forget the password?", "It can't be recovered, by us or anyone else. Keep your original unprotected file."),
                ("Is my password stored?", "No. It's used once to encrypt the file, and the files are deleted from the server after an hour."),
            ],
            "related": ["unlock-pdf", "compress-pdf", "merge-pdf"],
        },
        "he": {
            "name": "הוספת סיסמה ל-PDF",
            "title": "הוספת סיסמה ל-PDF – הצפנת קובץ PDF בחינם | PDFPro",
            "desc": "נועלים קובץ PDF בסיסמה עם הצפנת AES-256 לפני ששולחים אותו במייל. בחינם ובלי הרשמה.",
            "h1": "הוספת סיסמה לקובץ PDF",
            "lead": "נועלים PDF כך שרק מי שיודע את הסיסמה יוכל לפתוח אותו. שימושי לפני ששולחים צילום תעודת זהות, חוזה, תלוש שכר או מסמך רפואי.",
            "run": "נעל PDF",
            "steps": [
                ("בוחרים את ה-PDF", "גוררים את הקובץ לתיבה למעלה."),
                ("קובעים סיסמה", "מקלידים אותה פעמיים כדי למנוע טעות הקלדה."),
                ("מורידים את הקובץ המוגן", "הוא יבקש את הסיסמה בכל פתיחה."),
            ],
            "faqs": [
                ("באיזו הצפנה משתמשים?", "AES-256, שנתמכת בכל קורא PDF מודרני, כולל Adobe Acrobat, דפדפנים ואפליקציות בטלפון."),
                ("הנמען יוכל להדפיס את הקובץ?", "כן. אחרי פתיחה עם הסיסמה מותר להדפיס. העתקת טקסט ועריכה מוגבלות בקוראים שמכבדים הרשאות PDF."),
                ("מה אם אשכח את הסיסמה?", "אי אפשר לשחזר אותה, לא אנחנו ולא אף אחד אחר. שמרו את הקובץ המקורי הלא מוגן."),
                ("הסיסמה שלי נשמרת?", "לא. היא משמשת פעם אחת להצפנת הקובץ, והקבצים נמחקים מהשרת אחרי שעה."),
            ],
            "related": ["unlock-pdf", "compress-pdf", "merge-pdf"],
        },
    },
    {
        "slug": "jpg-to-pdf", "limit": 20,
        "api": {"endpoint": "/api/convert/images-to-pdf", "field": "files", "multi": True, "accept": ".jpg,.jpeg,.png,.webp,.gif,.bmp,.tif,.tiff", "result": "file"},
        "options": [
            {"name": "page_size", "type": "select", "default": "A4", "values": ["A4", "fit", "Letter"],
             "en": {"label": "Page size", "labels": ["A4 (standard document)", "Same as the image", "US Letter"]},
             "he": {"label": "גודל עמוד", "labels": ["A4 (מסמך רגיל)", "לפי גודל התמונה", "Letter (ארה\"ב)"]}},
        ],
        "en": {
            "name": "JPG to PDF",
            "title": "JPG to PDF – Convert Images to PDF Free | PDFPro",
            "desc": "Turn photos and scans (JPG, PNG and more) into a single PDF, in the order you choose. Up to 50 images. Free, no sign-up.",
            "h1": "JPG to PDF: images to one PDF",
            "lead": "Combine photos of documents, receipts or scans into one PDF file that's easy to email or upload.",
            "run": "Create PDF",
            "steps": [
                ("Add your images", "JPG, PNG, WEBP and other common formats. Up to 50 at once."),
                ("Set the order and page size", "Use Move up to reorder. A4 gives a standard document page."),
                ("Download the PDF", "Each image becomes one page."),
            ],
            "faqs": [
                ("How many images can I combine?", "Up to 50 images in one PDF."),
                ("Which page size should I pick?", "A4 if the PDF is going to an office, a bank or a government site. Same as the image keeps each photo at its own size."),
                ("Can I convert iPhone photos (HEIC)?", "When you pick photos from an iPhone in the browser, they are usually sent as JPG automatically. If a file is still rejected, change the camera format to Most Compatible in the iPhone settings."),
                ("The PDF is too big to upload. What can I do?", "Run the result through Compress PDF."),
            ],
            "related": ["compress-pdf", "merge-pdf", "ocr-pdf"],
        },
        "he": {
            "name": "תמונה ל-PDF",
            "title": "המרת תמונה ל-PDF בחינם – JPG ל-PDF | PDFPro",
            "desc": "הופכים צילומים וסריקות (JPG, PNG ועוד) לקובץ PDF אחד, בסדר שתבחרו. עד 50 תמונות. בחינם ובלי הרשמה.",
            "h1": "המרת תמונות ל-PDF",
            "lead": "מאחדים צילומי מסמכים, קבלות או סריקות לקובץ PDF אחד שקל לשלוח במייל או להעלות לאתר.",
            "run": "צור PDF",
            "steps": [
                ("מוסיפים תמונות", "JPG, PNG, WEBP ופורמטים נפוצים אחרים. עד 50 בבת אחת."),
                ("קובעים סדר וגודל עמוד", "משתמשים ב'הזז למעלה' כדי לסדר. A4 נותן עמוד מסמך רגיל."),
                ("מורידים את ה-PDF", "כל תמונה הופכת לעמוד."),
            ],
            "faqs": [
                ("כמה תמונות אפשר לאחד?", "עד 50 תמונות בקובץ PDF אחד."),
                ("איזה גודל עמוד לבחור?", "A4 אם הקובץ הולך למשרד, לבנק או לאתר ממשלתי. 'לפי גודל התמונה' משאיר כל צילום בגודל שלו."),
                ("אפשר להמיר תמונות מאייפון (HEIC)?", "כשבוחרים תמונות מהאייפון בדפדפן, הן בדרך כלל נשלחות כ-JPG אוטומטית. אם קובץ עדיין נדחה, משנים בהגדרות המצלמה את הפורמט ל'התאמה מרבית'."),
                ("ה-PDF גדול מדי להעלאה, מה עושים?", "מעבירים את התוצאה דרך דחיסת PDF."),
            ],
            "related": ["compress-pdf", "merge-pdf", "ocr-pdf"],
        },
    },
    {
        "slug": "word-to-pdf", "limit": 20,
        "api": {"endpoint": "/api/convert/office-to-pdf", "field": "file", "multi": False, "accept": ".doc,.docx,.xls,.xlsx,.ppt,.pptx", "result": "file"},
        "options": [],
        "en": {
            "name": "Word to PDF",
            "title": "Word to PDF – Convert DOCX, Excel & PowerPoint to PDF | PDFPro",
            "desc": "Convert Word, Excel and PowerPoint files to PDF online, with Hebrew and right-to-left text kept intact. Free, no sign-up.",
            "h1": "Word to PDF converter",
            "lead": "Turn a Word document, Excel sheet or PowerPoint presentation into a PDF that looks the same on every device.",
            "run": "Convert to PDF",
            "steps": [
                ("Choose your file", "DOC, DOCX, XLS, XLSX, PPT or PPTX."),
                ("Convert", "The document is laid out exactly as it would print."),
                ("Download the PDF", "Ready to email, upload or print."),
            ],
            "faqs": [
                ("Does it work with Excel and PowerPoint too?", "Yes. Excel sheets and PowerPoint slides are converted the same way as Word documents."),
                ("Will Hebrew text stay right-to-left?", "Yes. Right-to-left paragraphs and mixed Hebrew-English text are kept as they appear in the original."),
                ("Why does a font look different in the PDF?", "If the document uses a font that isn't installed on our server, a similar font is used instead. For an exact match, export to PDF from Word itself with the font embedded."),
                ("My Excel sheet is split across several pages.", "The PDF follows the sheet's print settings. Set the print area and Fit to page in Excel, save, and convert again."),
            ],
            "related": ["pdf-to-word", "compress-pdf", "merge-pdf"],
        },
        "he": {
            "name": "Word ל-PDF",
            "title": "המרת Word ל-PDF בחינם – גם Excel ו-PowerPoint | PDFPro",
            "desc": "המרת קבצי Word, Excel ו-PowerPoint ל-PDF אונליין, עם עברית וכיווניות מימין לשמאל שנשמרות. בחינם ובלי הרשמה.",
            "h1": "המרת Word ל-PDF",
            "lead": "הופכים מסמך Word, גיליון Excel או מצגת PowerPoint ל-PDF שנראה אותו דבר בכל מכשיר.",
            "run": "המר ל-PDF",
            "steps": [
                ("בוחרים קובץ", "DOC, DOCX, XLS, XLSX, PPT או PPTX."),
                ("ממירים", "המסמך נפרס בדיוק כמו שהיה מודפס."),
                ("מורידים את ה-PDF", "מוכן לשליחה במייל, להעלאה או להדפסה."),
            ],
            "faqs": [
                ("זה עובד גם עם Excel ו-PowerPoint?", "כן. גיליונות Excel ומצגות PowerPoint מומרים בדיוק כמו מסמכי Word."),
                ("העברית תישאר מימין לשמאל?", "כן. פסקאות בעברית וטקסט מעורב עברית-אנגלית נשמרים כמו במקור."),
                ("למה גופן נראה אחרת ב-PDF?", "אם המסמך משתמש בגופן שלא מותקן בשרת שלנו, מוחלף גופן דומה. להתאמה מדויקת, ייצאו ל-PDF מתוך Word עצמו עם הטמעת גופנים."),
                ("גיליון ה-Excel נחתך לכמה עמודים", "ה-PDF עוקב אחרי הגדרות ההדפסה של הגיליון. הגדירו ב-Excel אזור הדפסה והתאמה לעמוד, שמרו והמירו שוב."),
            ],
            "related": ["pdf-to-word", "compress-pdf", "merge-pdf"],
        },
    },
    {
        "slug": "pdf-to-jpg", "limit": 20,
        "api": {"endpoint": "/api/convert/pdf-to-images", "field": "file", "multi": False, "accept": ".pdf", "result": "parts"},
        "options": [
            {"name": "format", "type": "select", "default": "jpg", "values": ["jpg", "png"], "query": True,
             "en": {"label": "Image format", "labels": ["JPG (smaller files)", "PNG (sharper text)"]},
             "he": {"label": "פורמט תמונה", "labels": ["JPG (קבצים קטנים)", "PNG (טקסט חד יותר)"]}},
            {"name": "dpi", "type": "select", "default": "150", "values": ["100", "150", "300"], "query": True,
             "en": {"label": "Quality", "labels": ["Standard (screen)", "High (recommended)", "Print quality"]},
             "he": {"label": "איכות", "labels": ["רגילה (למסך)", "גבוהה (מומלץ)", "איכות הדפסה"]}},
        ],
        "en": {
            "name": "PDF to JPG",
            "title": "PDF to JPG – Convert PDF Pages to Images Free | PDFPro",
            "desc": "Save every page of a PDF as a JPG or PNG image, in the quality you need. Free, no sign-up.",
            "h1": "PDF to JPG: pages to images",
            "lead": "Turn each page of a PDF into an image you can post, send on WhatsApp, or drop into a presentation.",
            "run": "Convert to images",
            "steps": [
                ("Choose your PDF", "Drop the file into the box above."),
                ("Pick format and quality", "JPG for sharing, PNG when text needs to stay crisp."),
                ("Download the images", "One image per page."),
            ],
            "faqs": [
                ("JPG or PNG?", "JPG files are smaller and fine for photos and sharing. PNG keeps text and lines sharper, at a larger size."),
                ("Which quality should I choose?", "High works for almost everything. Print quality makes large files, so use it only when you'll print the images."),
                ("Can I convert just one page?", "Convert the whole file and keep the page you need, or first pull the page out with Split PDF."),
            ],
            "related": ["jpg-to-pdf", "split-pdf", "compress-pdf"],
        },
        "he": {
            "name": "PDF לתמונה",
            "title": "המרת PDF לתמונה (JPG) בחינם | PDFPro",
            "desc": "שומרים כל עמוד ב-PDF כתמונת JPG או PNG, באיכות שצריך. בחינם ובלי הרשמה.",
            "h1": "המרת PDF לתמונות",
            "lead": "הופכים כל עמוד ב-PDF לתמונה שאפשר לפרסם, לשלוח בוואטסאפ או להכניס למצגת.",
            "run": "המר לתמונות",
            "steps": [
                ("בוחרים את ה-PDF", "גוררים את הקובץ לתיבה למעלה."),
                ("בוחרים פורמט ואיכות", "JPG לשיתוף, PNG כשהטקסט צריך להישאר חד."),
                ("מורידים את התמונות", "תמונה אחת לכל עמוד."),
            ],
            "faqs": [
                ("JPG או PNG?", "קבצי JPG קטנים יותר ומתאימים לתמונות ולשיתוף. PNG שומר על טקסט וקווים חדים יותר, בגודל קובץ גדול יותר."),
                ("איזו איכות לבחור?", "גבוהה מתאימה כמעט לכל דבר. איכות הדפסה יוצרת קבצים גדולים, אז כדאי רק כשמדפיסים."),
                ("אפשר להמיר רק עמוד אחד?", "ממירים את כל הקובץ ושומרים את העמוד שצריך, או מוציאים קודם את העמוד בעזרת פיצול PDF."),
            ],
            "related": ["jpg-to-pdf", "split-pdf", "compress-pdf"],
        },
    },
    {
        "slug": "pdf-to-powerpoint", "limit": 10,
        "api": {"endpoint": "/api/convert/pdf-to-pptx", "field": "file", "multi": False, "accept": ".pdf", "result": "file"},
        "options": [
            {"name": "dpi", "type": "select", "default": "150", "values": ["150", "200", "300"], "query": True,
             "en": {"label": "Slide quality", "labels": ["Standard (smaller file)", "High", "Very high (large file)"]},
             "he": {"label": "איכות השקופיות", "labels": ["רגילה (קובץ קטן)", "גבוהה", "גבוהה מאוד (קובץ גדול)"]}},
        ],
        "en": {
            "name": "PDF to PowerPoint",
            "title": "PDF to PowerPoint – Convert PDF to PPTX Slides Free | PDFPro",
            "desc": "Turn each page of a PDF into a PowerPoint slide, ready to present. Free, no sign-up.",
            "h1": "PDF to PowerPoint",
            "lead": "Turn a PDF into a PowerPoint file with one slide per page, so you can present it, reorder it and add your own slides.",
            "run": "Convert to PowerPoint",
            "steps": [
                ("Choose your PDF", "Slides exported as PDF convert best."),
                ("Pick the quality", "Standard is enough for a projector or a screen share."),
                ("Download the PPTX", "Open it in PowerPoint, Google Slides or Keynote."),
            ],
            "faqs": [
                ("Can I edit the text on the slides?", "Each page is placed on its slide as a high-quality image, so the layout looks exactly like the PDF, but the text can't be edited directly. To edit the text, use PDF to Word."),
                ("Why is the file large?", "Every slide is an image. Choose Standard quality for a smaller file."),
                ("Will Hebrew slides look right?", "Yes. Because each page is copied as an image, Hebrew text and layout look exactly as in the PDF."),
            ],
            "related": ["pdf-to-word", "pdf-to-jpg", "compress-pdf"],
        },
        "he": {
            "name": "PDF ל-PowerPoint",
            "title": "המרת PDF ל-PowerPoint בחינם – PDF למצגת | PDFPro",
            "desc": "הופכים כל עמוד ב-PDF לשקופית ב-PowerPoint, מוכנה להצגה. בחינם ובלי הרשמה.",
            "h1": "המרת PDF ל-PowerPoint",
            "lead": "הופכים PDF לקובץ PowerPoint עם שקופית לכל עמוד, כדי להציג אותו, לשנות סדר ולהוסיף שקופיות משלכם.",
            "run": "המר למצגת",
            "steps": [
                ("בוחרים את ה-PDF", "מצגות שיוצאו ל-PDF מומרות הכי טוב."),
                ("בוחרים איכות", "רגילה מספיקה למקרן או לשיתוף מסך."),
                ("מורידים את ה-PPTX", "פותחים ב-PowerPoint, ב-Google Slides או ב-Keynote."),
            ],
            "faqs": [
                ("אפשר לערוך את הטקסט בשקופיות?", "כל עמוד מונח על השקופית כתמונה באיכות גבוהה, כך שהעיצוב נראה בדיוק כמו ב-PDF, אבל אי אפשר לערוך את הטקסט ישירות. כדי לערוך טקסט, השתמשו ב-PDF ל-Word."),
                ("למה הקובץ גדול?", "כל שקופית היא תמונה. בחרו איכות רגילה לקובץ קטן יותר."),
                ("שקופיות בעברית ייראו תקין?", "כן. כיוון שכל עמוד מועתק כתמונה, הטקסט והעיצוב בעברית נראים בדיוק כמו ב-PDF."),
            ],
            "related": ["pdf-to-word", "pdf-to-jpg", "compress-pdf"],
        },
    },
    {
        "slug": "rotate-pdf", "limit": 30,
        "api": {"endpoint": "/api/organize/rotate", "field": "file", "multi": False, "accept": ".pdf", "result": "file"},
        "options": [
            {"name": "angle", "type": "select", "default": "90", "values": ["90", "180", "270"],
             "en": {"label": "Rotate", "labels": ["90° clockwise", "180° (upside down)", "90° counter-clockwise"]},
             "he": {"label": "סיבוב", "labels": ["90° עם כיוון השעון", "180° (הפוך)", "90° נגד כיוון השעון"]}},
            {"name": "pages", "type": "text", "default": "",
             "en": {"label": "Pages (optional)", "placeholder": "All pages", "hint": "Leave empty for all pages, or list pages like 1,3,5."},
             "he": {"label": "עמודים (לא חובה)", "placeholder": "כל העמודים", "hint": "השאירו ריק לכל העמודים, או כתבו עמודים כמו 1,3,5."}},
        ],
        "en": {
            "name": "Rotate PDF",
            "title": "Rotate PDF – Turn PDF Pages and Save Free | PDFPro",
            "desc": "Rotate all pages or just the ones that are sideways, and save the PDF that way permanently. Free, no sign-up.",
            "h1": "Rotate PDF pages",
            "lead": "Fix a scan that came out sideways or upside down, and save it so it opens the right way for everyone.",
            "run": "Rotate PDF",
            "steps": [
                ("Choose your PDF", "Drop the file into the box above."),
                ("Pick direction and pages", "Leave pages empty to rotate the whole file, or list only the pages that are sideways."),
                ("Download", "The rotation is saved in the file."),
            ],
            "faqs": [
                ("Is the rotation saved, or only in my viewer?", "It's saved in the file, so it opens correctly on any device and for anyone you send it to."),
                ("Only some pages are sideways.", "List just those pages, for example 2,5, and the rest stay as they are."),
                ("Does rotating reduce quality?", "No. Rotation doesn't touch the content of the page."),
            ],
            "related": ["merge-pdf", "split-pdf", "compress-pdf"],
        },
        "he": {
            "name": "סיבוב PDF",
            "title": "סיבוב דפי PDF ושמירה בחינם | PDFPro",
            "desc": "מסובבים את כל העמודים או רק את אלה שעומדים על הצד, ושומרים את ה-PDF כך לתמיד. בחינם ובלי הרשמה.",
            "h1": "סיבוב עמודי PDF",
            "lead": "מתקנים סריקה שיצאה על הצד או הפוכה, ושומרים אותה כך שתיפתח נכון אצל כולם.",
            "run": "סובב PDF",
            "steps": [
                ("בוחרים את ה-PDF", "גוררים את הקובץ לתיבה למעלה."),
                ("בוחרים כיוון ועמודים", "משאירים את שדה העמודים ריק לסיבוב כל הקובץ, או כותבים רק את העמודים שעומדים על הצד."),
                ("מורידים", "הסיבוב נשמר בקובץ."),
            ],
            "faqs": [
                ("הסיבוב נשמר, או רק בתצוגה אצלי?", "הוא נשמר בקובץ, כך שייפתח נכון בכל מכשיר ואצל כל מי שתשלחו לו."),
                ("רק חלק מהעמודים על הצד", "כותבים רק אותם, למשל 2,5, ושאר העמודים נשארים כמו שהם."),
                ("הסיבוב פוגע באיכות?", "לא. סיבוב לא נוגע בתוכן העמוד."),
            ],
            "related": ["merge-pdf", "split-pdf", "compress-pdf"],
        },
    },
    {
        "slug": "watermark-pdf", "limit": 20,
        "api": {"endpoint": "/api/edit/watermark", "field": "file", "multi": False, "accept": ".pdf", "result": "file"},
        "options": [
            {"name": "type", "type": "hidden", "default": "text"},
            {"name": "text", "type": "text", "default": {"en": "CONFIDENTIAL", "he": "סודי"}, "dir": "auto",
             "en": {"label": "Watermark text", "required": "Enter the watermark text."},
             "he": {"label": "טקסט סימן המים", "required": "הקלידו את טקסט סימן המים."}},
            {"name": "opacity", "type": "select", "default": "0.25", "values": ["0.15", "0.25", "0.4"],
             "en": {"label": "Strength", "labels": ["Light", "Medium", "Strong"]},
             "he": {"label": "עוצמה", "labels": ["עדינה", "בינונית", "חזקה"]}},
        ],
        "en": {
            "name": "Watermark PDF",
            "title": "Add Watermark to PDF – Text Watermark Free | PDFPro",
            "desc": "Stamp a diagonal text watermark like CONFIDENTIAL or DRAFT across every page of a PDF. Hebrew supported. Free.",
            "h1": "Add a watermark to a PDF",
            "lead": "Stamp a diagonal line of text across every page, such as Confidential, Draft or who the copy is for.",
            "run": "Add watermark",
            "steps": [
                ("Choose your PDF", "Drop the file into the box above."),
                ("Write the text and pick the strength", "Light keeps the page easy to read. Strong is harder to ignore."),
                ("Download", "Every page now carries the watermark."),
            ],
            "faqs": [
                ("Can I write the watermark in Hebrew?", "Yes. Hebrew, English and mixed text all render correctly."),
                ("Can someone remove the watermark?", "It's drawn into the page, so it can't be switched off in a normal reader, but someone with editing software can remove it. It deters casual copying rather than preventing it."),
                ("Can I use a logo instead of text?", "Not on this page yet. Text watermarks only for now."),
            ],
            "related": ["protect-pdf", "redact-pdf", "sign-pdf"],
        },
        "he": {
            "name": "סימן מים",
            "title": "הוספת סימן מים ל-PDF בחינם – גם בעברית | PDFPro",
            "desc": "מוסיפים סימן מים באלכסון, כמו 'סודי' או 'טיוטה', על כל עמוד ב-PDF. תומך בעברית. בחינם.",
            "h1": "הוספת סימן מים ל-PDF",
            "lead": "מטביעים שורת טקסט באלכסון על כל עמוד, כמו 'סודי', 'טיוטה' או למי מיועד העותק.",
            "run": "הוסף סימן מים",
            "steps": [
                ("בוחרים את ה-PDF", "גוררים את הקובץ לתיבה למעלה."),
                ("כותבים טקסט ובוחרים עוצמה", "עדינה משאירה את העמוד קריא. חזקה קשה יותר להתעלם ממנה."),
                ("מורידים", "כל העמודים נושאים עכשיו את סימן המים."),
            ],
            "faqs": [
                ("אפשר לכתוב את סימן המים בעברית?", "כן. עברית, אנגלית וטקסט מעורב מוצגים נכון."),
                ("אפשר להסיר את סימן המים?", "הוא מצויר בתוך העמוד, כך שאי אפשר לכבות אותו בקורא PDF רגיל, אבל מי שיש לו תוכנת עריכה יכול להסיר אותו. הוא מרתיע מהעתקה, לא מונע אותה."),
                ("אפשר להשתמש בלוגו במקום טקסט?", "עדיין לא בעמוד הזה. כרגע רק סימן מים של טקסט."),
            ],
            "related": ["protect-pdf", "redact-pdf", "sign-pdf"],
        },
    },
    {
        "slug": "sign-pdf", "limit": 20,
        "api": {"endpoint": "/api/edit/sign", "field": "file", "multi": False, "accept": ".pdf", "result": "file"},
        "options": [
            {"name": "signature_text", "type": "signature",
             "en": {"label": "Your signature", "draw": "Draw", "type": "Type",
                    "pad": "Sign here with your mouse or finger", "clear": "Clear",
                    "name_label": "Your name", "placeholder": "e.g. Dana Levi",
                    "need_draw": "Draw your signature, or switch to Type.",
                    "need_text": "Enter the name to sign with."},
             "he": {"label": "החתימה שלכם", "draw": "ציור", "type": "הקלדה",
                    "pad": "חתמו כאן עם העכבר או עם האצבע", "clear": "נקה",
                    "name_label": "השם שלכם", "placeholder": "לדוגמה: דנה לוי",
                    "need_draw": "ציירו את החתימה, או עברו להקלדה.",
                    "need_text": "הקלידו את השם לחתימה."}},
            {"name": "page", "type": "select", "default": "-1", "values": ["-1", "1"],
             "en": {"label": "Page", "labels": ["Last page", "First page"]},
             "he": {"label": "עמוד", "labels": ["העמוד האחרון", "העמוד הראשון"]}},
            {"name": "position", "type": "select", "fields": "x,y", "default": {"en": "0.7|0.85", "he": "0.05|0.85"},
             "values": ["0.7|0.85", "0.05|0.85", "0.375|0.85"],
             "en": {"label": "Position", "labels": ["Bottom right", "Bottom left", "Bottom center"]},
             "he": {"label": "מיקום", "labels": ["למטה מימין", "למטה משמאל", "למטה באמצע"]}},
            {"name": "add_date", "type": "select", "default": "true", "values": ["true", "false"],
             "en": {"label": "Today's date under the signature", "labels": ["Add date", "No date"]},
             "he": {"label": "תאריך מתחת לחתימה", "labels": ["להוסיף תאריך", "בלי תאריך"]}},
        ],
        "script": "sign.js",
        "en": {
            "name": "Sign PDF",
            "title": "Sign PDF Online Free – Draw or Type Your Signature | PDFPro",
            "desc": "Draw your signature with a mouse or finger, or type your name, and add it to a PDF without printing or scanning. Free, no sign-up.",
            "h1": "Sign a PDF",
            "lead": "Draw your signature with your mouse or finger, or type your name, and place it on the page you choose. No printing, no scanning.",
            "run": "Sign PDF",
            "steps": [
                ("Choose your PDF", "Drop the file into the box above."),
                ("Draw or type your signature", "Then choose the page and where the signature goes."),
                ("Download the signed PDF", "The signature, and the date if you want it, are added to the page."),
            ],
            "faqs": [
                ("Is this a legally binding signature?", "It adds a visible signature, like ink on paper, which is accepted for many everyday documents like forms, rental paperwork and approvals. Some documents require a certified digital signature, so check with whoever asked for it."),
                ("Can I sign in Hebrew?", "Yes. Hebrew names are written right-to-left, correctly."),
                ("Can I draw my own signature?", "Yes. Draw it in the box with a mouse, a trackpad or your finger on a phone. It's added to the PDF as you drew it, without a frame."),
                ("Is my drawn signature saved anywhere?", "No. It's sent only with the file you're signing and deleted from the server with it after an hour."),
            ],
            "related": ["protect-pdf", "watermark-pdf", "compress-pdf"],
        },
        "he": {
            "name": "חתימה על PDF",
            "title": "חתימה דיגיטלית על PDF בחינם – לחתום על מסמך אונליין | PDFPro",
            "desc": "חתימה דיגיטלית על מסמך PDF אונליין: מציירים חתימה עם העכבר או עם האצבע, או מקלידים שם, בלי להדפיס ולסרוק. בחינם ובלי הרשמה.",
            "h1": "חתימה דיגיטלית על PDF",
            "lead": "חותמים על מסמך PDF אונליין, מהמחשב או מהטלפון: מציירים את החתימה עם העכבר או עם האצבע, או מקלידים שם, ובוחרים איפה היא תופיע. בלי מדפסת ובלי סורק.",
            "run": "חתום על PDF",
            "steps": [
                ("בוחרים את ה-PDF", "גוררים את הקובץ לתיבה למעלה."),
                ("מציירים או מקלידים חתימה", "ואז בוחרים עמוד ואיפה החתימה תופיע."),
                ("מורידים את ה-PDF החתום", "החתימה, ואם רוצים גם התאריך, מתווספות לעמוד."),
            ],
            "faqs": [
                ("זו חתימה דיגיטלית?", "בשפה היומיומית כן: זו חתימה על מסמך בלי נייר. היא לא 'חתימה אלקטרונית מאושרת' עם תעודה דיגיטלית, שחלק מהגופים דורשים. ההבדלים מוסברים במדריך על סוגי חתימות."),
                ("אפשר לחתום מהטלפון?", "כן. פותחים את העמוד בדפדפן בטלפון, בוחרים את ה-PDF מהקבצים או מהמייל, ומורידים את הקובץ החתום."),
                ("זו חתימה מחייבת משפטית?", "הכלי מוסיף חתימה גלויה, כמו חתימה בעט על נייר, שמתקבלת בהרבה מסמכים יומיומיים כמו טפסים, חוזי שכירות ואישורים. יש מסמכים שדורשים חתימה אלקטרונית מאושרת, אז כדאי לבדוק עם מי שביקש את המסמך."),
                ("אפשר לחתום בעברית?", "כן. שמות בעברית נכתבים מימין לשמאל, בצורה תקינה."),
                ("אפשר לצייר חתימה משלי?", "כן. מציירים בתיבה עם העכבר, עם משטח המגע או עם האצבע בטלפון. החתימה נכנסת ל-PDF בדיוק כמו שציירתם, בלי מסגרת."),
                ("החתימה שציירתי נשמרת איפשהו?", "לא. היא נשלחת רק עם הקובץ שאתם חותמים עליו, ונמחקת מהשרת יחד איתו אחרי שעה."),
            ],
            "related": ["protect-pdf", "watermark-pdf", "compress-pdf"],
        },
    },
    {
        "slug": "redact-pdf", "limit": 20,
        "api": {"endpoint": "/api/edit/redact", "field": "file", "multi": False, "accept": ".pdf", "result": "file"},
        "options": [
            {"name": "texts", "type": "text", "default": "", "dir": "auto",
             "en": {"label": "Text to hide", "placeholder": "e.g. 123456782, Dana Levi", "hint": "Separate several items with commas. Every occurrence in the file is blacked out.", "required": "Enter the text you want to hide."},
             "he": {"label": "טקסט להסתרה", "placeholder": "לדוגמה: 123456782, דנה לוי", "hint": "מפרידים כמה פריטים בפסיקים. כל מופע בקובץ מושחר.", "required": "הקלידו את הטקסט שרוצים להסתיר."}},
        ],
        "en": {
            "name": "Redact PDF",
            "title": "Redact PDF – Black Out Sensitive Text Free | PDFPro",
            "desc": "Permanently black out ID numbers, names, account numbers or any text in a PDF before sharing it. Free, no sign-up.",
            "h1": "Redact a PDF",
            "lead": "Black out ID numbers, names or account details before you share a document. The hidden text is removed from the file, not just covered.",
            "run": "Redact PDF",
            "steps": [
                ("Choose your PDF", "Drop the file into the box above."),
                ("Type what to hide", "An ID number, a name, an address. Separate items with commas."),
                ("Download", "Every occurrence is blacked out and removed."),
            ],
            "faqs": [
                ("Is the text really removed, or just covered?", "Removed. The black box replaces the text in the file itself, so it can't be copied or found by searching."),
                ("It didn't find my text.", "The text has to match exactly as it appears in the PDF, including spaces and dashes. Scanned documents contain images instead of text, so run them through OCR first."),
                ("Does it work with Hebrew?", "Yes, as long as the PDF contains real Hebrew text, which is the case for most documents created on a computer."),
            ],
            "related": ["protect-pdf", "watermark-pdf", "ocr-pdf"],
        },
        "he": {
            "name": "השחרת טקסט",
            "title": "השחרת טקסט ב-PDF – הסתרת מידע רגיש בחינם | PDFPro",
            "desc": "משחירים לצמיתות מספר תעודת זהות, שמות, מספרי חשבון או כל טקסט ב-PDF לפני ששולחים אותו. בחינם ובלי הרשמה.",
            "h1": "השחרת מידע רגיש ב-PDF",
            "lead": "משחירים מספר תעודת זהות, שמות או פרטי חשבון לפני ששולחים מסמך. הטקסט המושחר נמחק מהקובץ, לא רק מכוסה.",
            "run": "השחר טקסט",
            "steps": [
                ("בוחרים את ה-PDF", "גוררים את הקובץ לתיבה למעלה."),
                ("כותבים מה להסתיר", "מספר תעודת זהות, שם, כתובת. מפרידים כמה פריטים בפסיקים."),
                ("מורידים", "כל המופעים מושחרים ונמחקים."),
            ],
            "faqs": [
                ("הטקסט באמת נמחק, או רק מכוסה?", "נמחק. המלבן השחור מחליף את הטקסט בקובץ עצמו, כך שאי אפשר להעתיק אותו או למצוא אותו בחיפוש."),
                ("הכלי לא מצא את הטקסט שלי", "הטקסט צריך להתאים בדיוק למה שכתוב ב-PDF, כולל רווחים ומקפים. מסמכים סרוקים מכילים תמונה ולא טקסט, אז מעבירים אותם קודם ב-OCR."),
                ("זה עובד בעברית?", "כן, כל עוד ה-PDF מכיל טקסט עברי אמיתי, כמו ברוב המסמכים שנוצרו במחשב."),
            ],
            "related": ["protect-pdf", "watermark-pdf", "ocr-pdf"],
        },
    },
]
TOOL_BY_SLUG = {t["slug"]: t for t in TOOLS}

# ════════════════════════════════════════════════════════════════════════════
# ARTICLES — body lives in content/blog/<lang>/<slug>.html
# ════════════════════════════════════════════════════════════════════════════
ARTICLES = [
    {"slug": "word-to-pdf-hebrew", "published": "2026-09-26", "tool": "word-to-pdf", "also": ["pdf-to-word"],
     "en": {"title": "How to Convert Word to PDF Without the Layout Shifting",
            "desc": "Why Word documents look different on other computers, five checks before converting, and how to send a PDF that looks exactly right.",
            "tag": "Conversion", "cta": "Convert Word to PDF"},
     "he": {"title": "איך להמיר Word ל-PDF בלי שהעברית תזוז",
            "desc": "למה מסמכי Word נראים אחרת במחשבים אחרים, חמש בדיקות לפני ההמרה, ואיך שולחים PDF שנראה בדיוק כמו שצריך.",
            "tag": "המרה", "cta": "המרת Word ל-PDF"}},
    {"slug": "sign-rental-contract-online", "published": "2026-09-26", "tool": "sign-pdf",
     "en": {"title": "How to Sign a Rental Contract Without Printing It",
            "desc": "What to check before signing a lease, how to sign the PDF online, and what to keep afterwards.",
            "tag": "Signature", "cta": "Sign a PDF"},
     "he": {"title": "איך לחתום על חוזה שכירות בלי להדפיס",
            "desc": "מה לבדוק לפני שחותמים על חוזה שכירות, איך חותמים על ה-PDF אונליין, ומה לשמור אחרי החתימה.",
            "tag": "חתימה", "cta": "חתימה על PDF"}},
    {"slug": "signature-types-explained", "published": "2026-09-26", "tool": "sign-pdf",
     "en": {"title": "Scanned, Electronic or Certified Signature: What's the Difference?",
            "desc": "Three kinds of signatures on digital documents, what each one proves, and how to know which one you need.",
            "tag": "Signature", "cta": "Sign a PDF"},
     "he": {"title": "חתימה סרוקה, חתימה על PDF או חתימה מאושרת: מה ההבדל?",
            "desc": "שלושה סוגי חתימות על מסמכים דיגיטליים, מה כל אחד מוכיח, ואיך יודעים איזה סוג צריך.",
            "tag": "חתימה", "cta": "חתימה על PDF"}},
    {"slug": "rotate-scanned-pdf", "published": "2026-09-26", "tool": "rotate-pdf",
     "en": {"title": "How to Rotate a Scanned PDF and Save It That Way",
            "desc": "Why rotating in your viewer doesn't stick, and how to rotate pages in the file itself, including only some pages.",
            "tag": "Organize", "cta": "Rotate PDF"},
     "he": {"title": "איך לסובב PDF סרוק ולשמור אותו כך",
            "desc": "למה סיבוב בתוכנת הצפייה לא נשמר, ואיך מסובבים עמודים בקובץ עצמו, כולל רק חלק מהעמודים.",
            "tag": "ארגון", "cta": "סיבוב PDF"}},
    {"slug": "copy-text-from-image-hebrew", "published": "2026-09-26", "tool": "ocr-pdf",
     "en": {"title": "How to Copy Text from an Image or Scan (Including Hebrew)",
            "desc": "Extract text from photos and scans with OCR, why Hebrew is harder, and how to get an accurate result.",
            "tag": "OCR", "cta": "Extract text with OCR"},
     "he": {"title": "איך להעתיק טקסט מתמונה או מסריקה בעברית",
            "desc": "חילוץ טקסט מצילומים וסריקות עם OCR, למה עברית קשה יותר לזיהוי, ואיך מקבלים תוצאה מדויקת.",
            "tag": "OCR", "cta": "OCR בעברית"}},
    {"slug": "powerpoint-to-pdf", "published": "2026-09-26", "tool": "word-to-pdf",
     "en": {"title": "How to Send a Presentation as a PDF (and What Gets Lost)",
            "desc": "Why a PowerPoint file can look different for the recipient, how to convert it to PDF, and what happens to animations and video.",
            "tag": "Conversion", "cta": "Convert PowerPoint to PDF"},
     "he": {"title": "איך לשלוח מצגת כ-PDF, ומה הולך לאיבוד",
            "desc": "למה קובץ PowerPoint יכול להיראות אחרת אצל הנמען, איך ממירים ל-PDF, ומה קורה לאנימציות ולסרטונים.",
            "tag": "המרה", "cta": "המרת PowerPoint ל-PDF"}},
    {"slug": "bank-statement-to-excel", "published": "2026-09-26", "tool": "pdf-to-excel",
     "en": {"title": "How to Turn a Bank Statement PDF into an Excel Spreadsheet",
            "desc": "Convert a bank or credit card statement to Excel, tidy up the data, and use it to track spending.",
            "tag": "Conversion", "cta": "Convert PDF to Excel"},
     "he": {"title": "איך להפוך דף חשבון מהבנק לטבלת Excel",
            "desc": "המרה של דף חשבון או פירוט אשראי ל-Excel, סידור הנתונים, ושימוש בהם למעקב אחרי הוצאות.",
            "tag": "המרה", "cta": "המרת PDF ל-Excel"}},
    {"slug": "extract-page-from-pdf", "published": "2026-09-26", "tool": "split-pdf",
     "en": {"title": "How to Extract a Single Page from a Long PDF",
            "desc": "Pull one page, a range, or several separate pages out of a PDF into a new file, in under a minute.",
            "tag": "Organize", "cta": "Split PDF"},
     "he": {"title": "איך להוציא עמוד אחד מקובץ PDF ארוך",
            "desc": "מוציאים עמוד בודד, טווח או כמה עמודים לא רציפים מ-PDF לקובץ חדש, בפחות מדקה.",
            "tag": "ארגון", "cta": "פיצול PDF"}},
    {"slug": "translate-official-document", "published": "2026-09-26", "tool": "translate-pdf",
     "en": {"title": "Translating an Official Document: When Machine Translation Is Enough",
            "desc": "When translating a PDF automatically is fine, when you need a certified translator, and how to get the best machine translation.",
            "tag": "Translation", "cta": "Translate a PDF"},
     "he": {"title": "תרגום מסמך רשמי: מתי תרגום מכונה מספיק ומתי צריך מתרגם",
            "desc": "מתי אפשר לתרגם PDF אוטומטית, מתי צריך תרגום נוטריוני או מאושר, ואיך מקבלים תרגום מכונה טוב יותר.",
            "tag": "תרגום", "cta": "תרגום PDF"}},
    {"slug": "present-pdf-as-slides", "published": "2026-09-26", "tool": "pdf-to-powerpoint",
     "en": {"title": "How to Present a PDF as a Slideshow or Turn It into PowerPoint",
            "desc": "Present a PDF full screen, or convert it to PowerPoint to add, remove and reorder slides.",
            "tag": "Conversion", "cta": "Convert PDF to PowerPoint"},
     "he": {"title": "איך להציג PDF כמצגת או להפוך אותו ל-PowerPoint",
            "desc": "הצגת PDF במסך מלא, או המרה ל-PowerPoint כדי להוסיף, למחוק ולסדר שקופיות.",
            "tag": "המרה", "cta": "PDF ל-PowerPoint"}},
    {"slug": "combine-payslips-pdf", "published": "2026-09-26", "tool": "merge-pdf", "also": ["unlock-pdf"],
     "en": {"title": "How to Combine Password-Protected Payslips into One PDF",
            "desc": "Unlock and merge several payslips into a single PDF for a mortgage, loan or rental application, step by step.",
            "tag": "Guides", "cta": "Merge PDF files"},
     "he": {"title": "איך לאחד תלושי שכר מוגנים בסיסמה לקובץ PDF אחד",
            "desc": "מדריך צעד אחר צעד להסרת סיסמה ואיחוד כמה תלושי שכר ל-PDF אחד, לבקשת משכנתא, הלוואה או שכירות.",
            "tag": "מדריכים", "cta": "מיזוג PDF"}},
    {"slug": "scan-document-with-phone", "published": "2026-09-26", "tool": "jpg-to-pdf", "also": ["compress-pdf"],
     "en": {"title": "How to Scan a Document with Your Phone and Send It as a PDF",
            "desc": "No scanner needed: how to photograph a document so it looks like a real scan, and turn the photos into one PDF.",
            "tag": "Guides", "cta": "Convert JPG to PDF"},
     "he": {"title": "איך לסרוק מסמך עם הטלפון ולשלוח אותו כ-PDF",
            "desc": "בלי סורק: איך לצלם מסמך כך שייראה כמו סריקה אמיתית, ואיך להפוך את הצילומים לקובץ PDF אחד.",
            "tag": "מדריכים", "cta": "המרת תמונה ל-PDF"}},
    {"slug": "pdf-file-too-large", "published": "2026-09-26", "tool": "compress-pdf", "also": ["split-pdf"],
     "en": {"title": "PDF Too Large to Upload? How to Make It Fit",
            "desc": "Why PDFs get so big, and four ways to get under an upload limit, from compression to fixing the file at the source.",
            "tag": "Compression", "cta": "Compress a PDF"},
     "he": {"title": "הקובץ גדול מדי? איך להקטין PDF כשאתר לא מקבל אותו",
            "desc": "למה קבצי PDF כל כך כבדים, וארבע דרכים לעמוד במגבלת ההעלאה, מדחיסה ועד תיקון הקובץ במקור.",
            "tag": "דחיסה", "cta": "דחיסת PDF"}},
    {"slug": "hide-personal-details-pdf", "published": "2026-09-26", "tool": "redact-pdf",
     "en": {"title": "How to Hide an ID Number or Personal Details in a PDF Before Sending It",
            "desc": "Which details to hide before sharing a document, why a black box in an editor isn't enough, and how to redact properly.",
            "tag": "Privacy", "cta": "Redact a PDF"},
     "he": {"title": "איך להסתיר מספר תעודת זהות ופרטים אישיים ב-PDF לפני ששולחים",
            "desc": "אילו פרטים כדאי להסתיר לפני ששולחים מסמך, למה מלבן שחור בתוכנת עריכה לא מספיק, ואיך משחירים כמו שצריך.",
            "tag": "פרטיות", "cta": "השחרת טקסט"}},
    {"slug": "send-id-copy-safely", "published": "2026-09-26", "tool": "watermark-pdf", "also": ["protect-pdf"],
     "en": {"title": "Sending a Copy of Your ID? How to Do It Safely",
            "desc": "A landlord or employer asked for a copy of your ID. How to limit what the copy can be used for with a watermark and a password.",
            "tag": "Privacy", "cta": "Add a watermark"},
     "he": {"title": "שולחים צילום תעודת זהות? כך עושים את זה בצורה בטוחה",
            "desc": "בעל דירה או מעסיק ביקשו צילום תעודת זהות. איך להגביל את השימוש בעותק עם סימן מים וסיסמה.",
            "tag": "פרטיות", "cta": "הוספת סימן מים"}},
    {"slug": "compress-id-contract-pdf", "published": "2026-07-08", "tool": "compress-pdf",
     "en": {"title": "How to Compress an ID or Contract PDF Without Losing Signature Clarity",
            "desc": "A guide to compressing sensitive documents like ID cards and signed contracts while keeping text and signatures fully legible.",
            "tag": "Compression", "cta": "Compress a PDF"},
     "he": {"title": "איך לדחוס PDF של תעודת זהות או חוזה בלי לפגוע בקריאות החתימה",
            "desc": "מדריך לדחיסת מסמכים רגישים כמו תעודת זהות וחוזים, תוך שמירה על קריאות מלאה של הטקסט והחתימה.",
            "tag": "דחיסה", "cta": "דחיסת PDF"}},
    {"slug": "pdf-broken-mobile", "published": "2026-07-07", "tool": "compress-pdf",
     "en": {"title": "5 Mistakes That Make Your PDF Look Broken on Mobile",
            "desc": "The most common reasons PDF files look broken, cut off, or unreadable on a mobile phone.",
            "tag": "Compatibility", "cta": "Compress a PDF"},
     "he": {"title": "5 טעויות שגורמות ל-PDF להיראות שבור בפתיחה בנייד",
            "desc": "הסיבות הנפוצות ביותר לכך שקבצי PDF נראים שבורים, חתוכים או לא קריאים בטלפון הנייד.",
            "tag": "תאימות", "cta": "דחיסת PDF"}},
    {"slug": "pdf-password-protected", "published": "2026-07-05", "tool": "unlock-pdf",
     "en": {"title": "Password-Protected PDF: What to Do When You've Lost the Password",
            "desc": "What to do when you've lost the password to your own PDF file — legitimate options only.",
            "tag": "Security", "cta": "Know the password? Remove it"},
     "he": {"title": "PDF מוגן סיסמה: מה עושים כשאיבדתם את הסיסמה",
            "desc": "מה לעשות כשאיבדתם את הסיסמה לקובץ PDF שלכם - אפשרויות לגיטימיות בלבד.",
            "tag": "אבטחה", "cta": "יודעים את הסיסמה? הסירו אותה"}},
    {"slug": "electronic-signature-pdf", "published": "2026-07-03", "tool": "sign-pdf",
     "en": {"title": "How to Sign a PDF Document Without Printing It",
            "desc": "A complete guide to electronically signing PDF documents — no printer, scanner, or wasted time required.",
            "tag": "Signature", "cta": "Sign a PDF"},
     "he": {"title": "איך לחתום על מסמך PDF בעברית בלי להדפיס",
            "desc": "מדריך מלא לחתימה דיגיטלית על מסמכי PDF בעברית - בלי מדפסת, סורק או בזבוז זמן.",
            "tag": "חתימה", "cta": "חתימה על PDF"}},
    {"slug": "pdf-hebrew-rtl", "published": "2026-07-01", "tool": "pdf-to-word",
     "en": {"title": "Why Hebrew or Arabic Text Gets Scrambled After PDF Conversion (And How to Fix It)",
            "desc": "A full explanation of RTL (right-to-left) text issues in PDF conversion, why it happens, and how to pick a tool that actually handles it correctly.",
            "tag": "Conversion", "cta": "Convert PDF to Word"},
     "he": {"title": "למה הטקסט בעברית \"מתהפך\" אחרי המרת PDF? והפתרון המלא",
            "desc": "הסבר מלא לבעיית ה-RTL בהמרת PDF לעברית - למה זה קורה וכיצד לפתור את זה נכון.",
            "tag": "המרה", "cta": "המרת PDF ל-Word"}},
]

# ════════════════════════════════════════════════════════════════════════════
# STATIC PAGES — body is plain HTML inside the page container
# ════════════════════════════════════════════════════════════════════════════
def _limits_table(lang: str) -> str:
    head = ("<tr><th>Tool</th><th>Files per hour</th></tr>" if lang == "en"
            else "<tr><th>כלי</th><th>קבצים לשעה</th></tr>")
    rows = "".join(f'<tr><td><a href="{url(lang, t["slug"])}">{esc(t[lang]["name"])}</a></td><td>{t["limit"]}</td></tr>'
                   for t in TOOLS)
    return f'<table class="limits">{head}{rows}</table>'


def static_pages() -> dict:
    return {
        "about": {
            "en": {"title": "About PDFPro", "desc": "Who builds PDFPro, why it exists, and how your files are handled.",
                   "body": f"""
<p class="lead">PDFPro is a set of free online PDF tools built with one specific gap in mind: most converters mangle Hebrew and other right-to-left languages.</p>
<h2>Why it exists</h2>
<p>Convert a Hebrew PDF with a typical online tool and you often get reversed words, flipped numbers and paragraphs in the wrong order. PDFPro is built and tested on Hebrew and mixed Hebrew-English documents first, and it works just as well for English-only files.</p>
<h2>Who builds it</h2>
<p>PDFPro is an independent project, built and maintained by a software developer in Israel. It is not affiliated with any other product called PDF Pro.</p>
<h2>How your files are handled</h2>
<p>Files are uploaded over an encrypted connection, processed on our server, and deleted automatically one hour later. We don't look at, keep or share their contents. Details are in the <a href="/privacy/">privacy policy</a>.</p>
<h2>How it's funded</h2>
<p>The tools are free to use. The site shows ads to cover server costs.</p>
<p>Questions or a bug to report? <a href="/contact/">Get in touch</a>.</p>"""},
            "he": {"title": "אודות PDFPro", "desc": "מי בונה את PDFPro, למה הוא קיים ואיך הקבצים שלכם מטופלים.",
                   "body": f"""
<p class="lead">PDFPro הוא אוסף כלי PDF חינמיים אונליין, שנבנה בגלל בעיה אחת מוכרת: רוב הממירים הורסים טקסט בעברית ובשפות אחרות שנכתבות מימין לשמאל.</p>
<h2>למה הוא קיים</h2>
<p>ממירים PDF בעברית בכלי אונליין רגיל ומקבלים מילים הפוכות, מספרים שהתהפכו ופסקאות בסדר הלא נכון. PDFPro נבנה ונבדק קודם כול על מסמכים בעברית ובעברית-אנגלית, ועובד באותה רמה גם עם קבצים באנגלית בלבד.</p>
<h2>מי בונה אותו</h2>
<p>PDFPro הוא פרויקט עצמאי שנבנה ומתוחזק על ידי מפתח תוכנה בישראל. אין לו קשר למוצרים אחרים בשם PDF Pro.</p>
<h2>מה קורה לקבצים שלכם</h2>
<p>הקבצים עולים בחיבור מוצפן, מעובדים בשרת שלנו ונמחקים אוטומטית אחרי שעה. אנחנו לא מסתכלים על התוכן, לא שומרים אותו ולא משתפים אותו. הפרטים ב<a href="/he/privacy/">מדיניות הפרטיות</a>.</p>
<h2>איך האתר ממומן</h2>
<p>הכלים בחינם. באתר מוצגות פרסומות שמממנות את עלויות השרת.</p>
<p>שאלה או באג? <a href="/he/contact/">כתבו לנו</a>.</p>"""},
        },
        "contact": {
            "en": {"title": "Contact PDFPro", "desc": "Contact PDFPro for support, bug reports or feedback.",
                   "body": f"""
<p class="lead">Found a bug, got a file that didn't convert well, or have a suggestion? Email us.</p>
<div class="card"><h2 style="margin-top:0">Email</h2>
<p><a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></p>
<p>We usually reply within two business days.</p></div>
<h2>Reporting a conversion problem</h2>
<p>It helps a lot to include which tool you used, roughly when, and what went wrong (for example, "Hebrew text came out reversed on page 2"). Please don't attach documents with personal or sensitive information.</p>
<p>Before writing, the <a href="/help/">help center</a> may already have the answer.</p>"""},
            "he": {"title": "צור קשר | PDFPro", "desc": "יצירת קשר עם PDFPro לתמיכה, דיווח על באגים או משוב.",
                   "body": f"""
<p class="lead">מצאתם באג, קובץ שלא הומר טוב, או שיש לכם הצעה? שלחו לנו מייל.</p>
<div class="card"><h2 style="margin-top:0">מייל</h2>
<p><a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></p>
<p>בדרך כלל עונים תוך שני ימי עבודה.</p></div>
<h2>דיווח על בעיה בהמרה</h2>
<p>עוזר מאוד לציין באיזה כלי השתמשתם, בערך מתי, ומה השתבש (למשל: "הטקסט בעברית יצא הפוך בעמוד 2"). אנא אל תצרפו מסמכים עם מידע אישי או רגיש.</p>
<p>לפני שכותבים, ייתכן שהתשובה כבר נמצאת ב<a href="/he/help/">מרכז העזרה</a>.</p>"""},
        },
        "pricing": {
            "en": {"title": "Pricing – PDFPro Is Free", "desc": "All PDFPro tools are free, with no sign-up. See the file size and hourly limits for each tool.",
                   "body": f"""
<p class="lead">Every tool on PDFPro is free. No account, no trial, no watermark.</p>
<div class="plan"><p class="price">Free</p>
<p>All tools, files up to {MAX_MB} MB, files deleted after one hour.</p>
<a class="cta" href="/#tools">Choose a tool</a></div>
<h2>Limits</h2>
<p>To keep the service fast for everyone, each tool allows a certain number of files per hour from the same connection:</p>
{_limits_table("en")}
<h2>Will there be a paid plan?</h2>
<p>Possibly, for people who need higher limits or larger files. If that happens, the free tools will stay free.</p>"""},
            "he": {"title": "מחירים – PDFPro בחינם", "desc": "כל הכלים של PDFPro בחינם ובלי הרשמה. מגבלות גודל קובץ ומגבלות שעתיות לכל כלי.",
                   "body": f"""
<p class="lead">כל הכלים ב-PDFPro בחינם. בלי חשבון, בלי תקופת ניסיון ובלי סימן מים.</p>
<div class="plan"><p class="price">חינם</p>
<p>כל הכלים, קבצים עד {MAX_MB}MB, מחיקה אוטומטית אחרי שעה.</p>
<a class="cta" href="/he/#tools">בחירת כלי</a></div>
<h2>מגבלות</h2>
<p>כדי שהשירות יישאר מהיר לכולם, כל כלי מאפשר מספר קבצים מסוים בשעה מאותו חיבור:</p>
{_limits_table("he")}
<h2>יהיה מסלול בתשלום?</h2>
<p>אולי, למי שצריך מגבלות גבוהות יותר או קבצים גדולים יותר. אם זה יקרה, הכלים החינמיים יישארו חינמיים.</p>"""},
        },
        "help": {
            "en": {"title": "Help Center | PDFPro", "desc": "Answers to common questions about PDFPro: limits, privacy, Hebrew support and troubleshooting.",
                   "body": f"""
<p class="lead">Answers to the questions we get most often.</p>
<h2>Using the tools</h2>
<details><summary>Do I need an account?</summary><p>No. Open a tool, add your file, and download the result.</p></details>
<details><summary>What's the maximum file size?</summary><p>{MAX_MB} MB per file. Merge accepts up to 20 files at once.</p></details>
<details><summary>Is there a usage limit?</summary><p>Yes, a number of files per hour for each tool. The exact numbers are on the <a href="/pricing/">pricing page</a>.</p></details>
<details><summary>Why did the first file take so long?</summary><p>When nobody has used the site for a while, the server goes to sleep and needs up to a minute to start. After that, files are processed in seconds.</p></details>
<h2>Hebrew and RTL</h2>
<details><summary>My Hebrew text came out reversed. What happened?</summary><p>This usually happens with other converters that don't handle right-to-left text. If it happens with PDFPro, please <a href="/contact/">tell us</a> which tool you used. The <a href="/blog/pdf-hebrew-rtl/">RTL guide</a> explains the cause.</p></details>
<details><summary>Can I OCR a document that mixes Hebrew and English?</summary><p>Yes. In <a href="/ocr-pdf/">OCR</a>, choose Hebrew + English.</p></details>
<h2>Privacy</h2>
<details><summary>What happens to my files?</summary><p>They're processed on our server and deleted automatically after one hour. We don't read or keep them. See the <a href="/privacy/">privacy policy</a>.</p></details>
<h2>Troubleshooting</h2>
<details><summary>"The file has expired" when downloading</summary><p>Results are kept for one hour. Process the file again to get a new copy.</p></details>
<details><summary>"Hourly limit reached"</summary><p>Wait an hour, or use a different tool in the meantime.</p></details>
<p>Still stuck? <a href="/contact/">Contact us</a>.</p>"""},
            "he": {"title": "מרכז עזרה | PDFPro", "desc": "תשובות לשאלות נפוצות על PDFPro: מגבלות, פרטיות, תמיכה בעברית ופתרון תקלות.",
                   "body": f"""
<p class="lead">תשובות לשאלות שהכי הרבה שואלים אותנו.</p>
<h2>שימוש בכלים</h2>
<details><summary>צריך חשבון?</summary><p>לא. פותחים כלי, מוסיפים קובץ ומורידים את התוצאה.</p></details>
<details><summary>מה גודל הקובץ המקסימלי?</summary><p>{MAX_MB}MB לקובץ. במיזוג אפשר עד 20 קבצים בבת אחת.</p></details>
<details><summary>יש מגבלת שימוש?</summary><p>כן, מספר קבצים לשעה בכל כלי. המספרים המדויקים ב<a href="/he/pricing/">עמוד המחירים</a>.</p></details>
<details><summary>למה הקובץ הראשון לקח הרבה זמן?</summary><p>כשאף אחד לא השתמש באתר זמן מה, השרת נכנס למצב שינה וצריך עד דקה כדי לעלות. אחרי זה הקבצים מעובדים תוך שניות.</p></details>
<h2>עברית ו-RTL</h2>
<details><summary>הטקסט בעברית יצא הפוך. מה קרה?</summary><p>זה קורה בדרך כלל בממירים שלא יודעים לטפל בטקסט מימין לשמאל. אם זה קרה ב-PDFPro, <a href="/he/contact/">ספרו לנו</a> באיזה כלי השתמשתם. <a href="/he/blog/pdf-hebrew-rtl/">המדריך על RTL</a> מסביר את הסיבה.</p></details>
<details><summary>אפשר לעשות OCR למסמך עברית-אנגלית?</summary><p>כן. בכלי ה-<a href="/he/ocr-pdf/">OCR</a> בוחרים עברית + אנגלית.</p></details>
<h2>פרטיות</h2>
<details><summary>מה קורה לקבצים שלי?</summary><p>הם מעובדים בשרת שלנו ונמחקים אוטומטית אחרי שעה. אנחנו לא קוראים ולא שומרים אותם. ראו <a href="/he/privacy/">מדיניות פרטיות</a>.</p></details>
<h2>תקלות</h2>
<details><summary>"תוקף הקובץ פג" בזמן ההורדה</summary><p>התוצאות נשמרות שעה אחת. עבדו את הקובץ שוב כדי לקבל עותק חדש.</p></details>
<details><summary>"הגעתם למגבלה השעתית"</summary><p>חכו שעה, או השתמשו בינתיים בכלי אחר.</p></details>
<p>עדיין תקועים? <a href="/he/contact/">צרו קשר</a>.</p>"""},
        },
        "privacy": {
            "en": {"title": "Privacy Policy | PDFPro", "desc": "How PDFPro handles uploaded files, cookies, analytics and advertising.",
                   "body": f"""
<p class="meta">Last updated: {PRIVACY_UPDATED}</p>
<h2>1. Files you upload</h2>
<p>Files are sent over an encrypted (HTTPS) connection to our processing server, used only to perform the operation you asked for, and deleted automatically, together with the results, one hour after processing. We don't read, keep, sell or share the contents of your documents.</p>
<h2>2. Information collected automatically</h2>
<p>Like most websites, our server and third-party services receive technical information such as your IP address, browser type, device type and the pages you visit. We use the IP address to enforce hourly usage limits.</p>
<h2>3. Analytics</h2>
<p>We use Google Analytics to understand how the site is used (for example, which tools are popular). Google Analytics uses cookies. You can opt out with the <a href="https://tools.google.com/dlpage/gaoptout" rel="nofollow">Google Analytics opt-out add-on</a>.</p>
<h2>4. Advertising</h2>
<p>This site uses Google AdSense to show ads. Third-party vendors, including Google, use cookies to serve ads based on your previous visits to this and other websites. Google's use of advertising cookies enables it and its partners to serve ads based on your visits to this site and/or other sites on the internet.</p>
<p>You can opt out of personalized advertising in <a href="https://www.google.com/settings/ads" rel="nofollow">Google Ads Settings</a>, or opt out of some third-party vendors' use of cookies at <a href="https://www.aboutads.info/choices/" rel="nofollow">aboutads.info</a>. Learn more in <a href="https://policies.google.com/technologies/partner-sites" rel="nofollow">how Google uses information from sites that use its services</a>.</p>
<h2>5. Other cookies and storage</h2>
<p>We store your language preference in your browser. We don't use accounts, so there's no login data.</p>
<h2>6. Service providers</h2>
<p>The website is hosted on Vercel and files are processed on a server hosted by Render. Fonts are loaded from Google Fonts. Translation uses a third-party machine-translation service, which receives the text of the document being translated.</p>
<h2>7. Children</h2>
<p>The service isn't directed at children under 13, and we don't knowingly collect their information.</p>
<h2>8. Your rights and contact</h2>
<p>For any privacy question or request, email <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>.</p>
<h2>9. Changes</h2>
<p>If this policy changes, the date at the top will be updated.</p>"""},
            "he": {"title": "מדיניות פרטיות | PDFPro", "desc": "איך PDFPro מטפל בקבצים שמועלים, בעוגיות, באנליטיקס ובפרסומות.",
                   "body": f"""
<p class="meta">עודכן לאחרונה: {PRIVACY_UPDATED}</p>
<h2>1. קבצים שאתם מעלים</h2>
<p>הקבצים נשלחים בחיבור מוצפן (HTTPS) לשרת העיבוד שלנו, משמשים רק לביצוע הפעולה שביקשתם, ונמחקים אוטומטית, יחד עם התוצאות, שעה אחרי העיבוד. אנחנו לא קוראים, שומרים, מוכרים או משתפים את תוכן המסמכים.</p>
<h2>2. מידע שנאסף אוטומטית</h2>
<p>כמו ברוב האתרים, השרת שלנו ושירותי צד שלישי מקבלים מידע טכני כמו כתובת IP, סוג דפדפן, סוג מכשיר והעמודים שבהם ביקרתם. אנחנו משתמשים בכתובת ה-IP כדי לאכוף את המגבלות השעתיות.</p>
<h2>3. אנליטיקס</h2>
<p>אנחנו משתמשים ב-Google Analytics כדי להבין איך משתמשים באתר (למשל, אילו כלים פופולריים). Google Analytics משתמש בעוגיות. אפשר לבטל את המעקב עם <a href="https://tools.google.com/dlpage/gaoptout" rel="nofollow">התוסף של Google לביטול Analytics</a>.</p>
<h2>4. פרסומות</h2>
<p>באתר מוצגות פרסומות של Google AdSense. ספקי צד שלישי, כולל Google, משתמשים בעוגיות כדי להציג מודעות על סמך ביקורים קודמים שלכם באתר הזה ובאתרים אחרים. השימוש של Google בעוגיות פרסום מאפשר לה ולשותפיה להציג לכם מודעות על סמך הביקורים שלכם באתר הזה ו/או באתרים אחרים באינטרנט.</p>
<p>אפשר לבטל פרסום מותאם אישית ב<a href="https://www.google.com/settings/ads" rel="nofollow">הגדרות המודעות של Google</a>, או לבטל שימוש בעוגיות של חלק מספקי הצד השלישי ב-<a href="https://www.aboutads.info/choices/" rel="nofollow">aboutads.info</a>. מידע נוסף: <a href="https://policies.google.com/technologies/partner-sites" rel="nofollow">איך Google משתמשת במידע מאתרים שמשתמשים בשירותים שלה</a>.</p>
<h2>5. עוגיות ואחסון נוספים</h2>
<p>אנחנו שומרים בדפדפן את העדפת השפה שלכם. אין באתר חשבונות משתמש, ולכן אין נתוני התחברות.</p>
<h2>6. ספקי שירות</h2>
<p>האתר מאוחסן ב-Vercel והקבצים מעובדים בשרת שמאוחסן ב-Render. הגופנים נטענים מ-Google Fonts. התרגום נעשה באמצעות שירות תרגום מכונה חיצוני, שמקבל את טקסט המסמך המתורגם.</p>
<h2>7. ילדים</h2>
<p>השירות לא מיועד לילדים מתחת לגיל 13, ואנחנו לא אוספים ביודעין מידע עליהם.</p>
<h2>8. הזכויות שלכם ויצירת קשר</h2>
<p>לכל שאלה או בקשה בנושא פרטיות: <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>.</p>
<h2>9. שינויים</h2>
<p>אם המדיניות תשתנה, התאריך למעלה יתעדכן.</p>"""},
        },
        "terms": {
            "en": {"title": "Terms of Use | PDFPro", "desc": "Terms of use for the PDFPro online PDF tools.",
                   "body": f"""
<p class="meta">Last updated: {PRIVACY_UPDATED}</p>
<h2>1. Using the service</h2>
<p>PDFPro provides free online tools for converting and editing PDF files. By using the site you agree to these terms.</p>
<h2>2. Your files</h2>
<p>You keep full ownership of the files you upload. You give us permission to process them only to perform the operation you requested. Files are deleted automatically one hour after processing.</p>
<h2>3. Acceptable use</h2>
<p>Only upload files you have the right to use. Don't use the service for illegal content, to break the protection of documents that aren't yours, or to overload the service with automated requests.</p>
<h2>4. Limits</h2>
<p>Tools have file size and hourly usage limits, listed on the <a href="/pricing/">pricing page</a>. We may change them to keep the service available.</p>
<h2>5. No warranty</h2>
<p>The service is provided "as is". Conversions are automatic and may not be perfect, so check important documents before relying on them. Keep your own copy of the original file.</p>
<h2>6. Limitation of liability</h2>
<p>To the extent permitted by law, PDFPro is not liable for data loss, conversion errors, or damages resulting from use of the service.</p>
<h2>7. Changes</h2>
<p>We may update these terms. The date at the top shows the latest version.</p>
<h2>8. Contact</h2>
<p><a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></p>"""},
            "he": {"title": "תנאי שימוש | PDFPro", "desc": "תנאי השימוש בכלי ה-PDF של PDFPro.",
                   "body": f"""
<p class="meta">עודכן לאחרונה: {PRIVACY_UPDATED}</p>
<h2>1. שימוש בשירות</h2>
<p>PDFPro מספק כלים חינמיים אונליין להמרה ועריכה של קבצי PDF. השימוש באתר מהווה הסכמה לתנאים האלה.</p>
<h2>2. הקבצים שלכם</h2>
<p>הבעלות על הקבצים שאתם מעלים נשארת שלכם. אתם מאשרים לנו לעבד אותם רק לצורך הפעולה שביקשתם. הקבצים נמחקים אוטומטית שעה אחרי העיבוד.</p>
<h2>3. שימוש מותר</h2>
<p>העלו רק קבצים שיש לכם זכות להשתמש בהם. אין להשתמש בשירות לתוכן לא חוקי, לפריצת הגנה של מסמכים שאינם שלכם, או להעמסת השירות בבקשות אוטומטיות.</p>
<h2>4. מגבלות</h2>
<p>לכלים יש מגבלות גודל קובץ ומגבלות שימוש שעתיות, המפורטות ב<a href="/he/pricing/">עמוד המחירים</a>. אנחנו רשאים לשנות אותן כדי לשמור על זמינות השירות.</p>
<h2>5. ללא אחריות</h2>
<p>השירות ניתן כמו שהוא (AS IS). ההמרות אוטומטיות ועשויות לא להיות מושלמות, לכן בדקו מסמכים חשובים לפני שמסתמכים עליהם. שמרו עותק של הקובץ המקורי.</p>
<h2>6. הגבלת אחריות</h2>
<p>ככל שהחוק מתיר, PDFPro לא אחראי לאובדן מידע, לשגיאות המרה או לנזקים שנגרמו משימוש בשירות.</p>
<h2>7. שינויים</h2>
<p>ייתכן שנעדכן את התנאים. התאריך למעלה מציין את הגרסה האחרונה.</p>
<h2>8. יצירת קשר</h2>
<p><a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></p>"""},
        },
    }

PRIVACY_UPDATED = "September 26, 2026"
BLOG_META = {
    "en": {"title": "PDF Guides and Tips | PDFPro Blog", "h1": "Guides",
           "desc": "Practical guides for working with PDF files: compression, conversion, Hebrew and RTL text, signatures and more.",
           "lead": "Practical guides for getting PDF files to do what you need."},
    "he": {"title": "מדריכים וטיפים ל-PDF | הבלוג של PDFPro", "h1": "מדריכים",
           "desc": "מדריכים מעשיים לעבודה עם קבצי PDF: דחיסה, המרה, עברית ו-RTL, חתימות ועוד.",
           "lead": "מדריכים מעשיים שיעזרו לכם לגרום לקבצי PDF לעשות מה שצריך."},
}

# ════════════════════════════════════════════════════════════════════════════
# HELPERS
# ════════════════════════════════════════════════════════════════════════════
esc = html.escape
HE_MONTHS = ["ינואר", "פברואר", "מרץ", "אפריל", "מאי", "יוני", "יולי", "אוגוסט", "ספטמבר", "אוקטובר", "נובמבר", "דצמבר"]
EN_MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def url(lang: str, slug: str = "") -> str:
    """Site-relative URL, always with trailing slash."""
    prefix = "/he" if lang == "he" else ""
    return f"{prefix}/{slug}/" if slug else f"{prefix}/"


def abs_url(lang: str, slug: str = "") -> str:
    return SITE + url(lang, slug)


def fmt_date(iso: str, lang: str) -> str:
    y, m, d = map(int, iso.split("-"))
    return f"{d} ב{HE_MONTHS[m-1]} {y}" if lang == "he" else f"{EN_MONTHS[m-1]} {d}, {y}"


def asset(name: str) -> str:
    """Cache-busting URL for files in /assets/."""
    h = hashlib.md5((ROOT / "assets" / name).read_bytes()).hexdigest()[:8]
    return f"/assets/{name}?v={h}"


def ld(obj) -> str:
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"


def breadcrumb(lang: str, crumbs: list[tuple[str, str | None]]) -> tuple[str, dict]:
    """crumbs: [(label, site_relative_url_or_None_for_current)]"""
    items_html, items_ld = [], []
    for i, (label, href) in enumerate(crumbs, 1):
        if href:
            items_html.append(f'<li><a href="{href}">{esc(label)}</a></li>')
            items_ld.append({"@type": "ListItem", "position": i, "name": label, "item": SITE + href})
        else:
            items_html.append(f'<li aria-current="page">{esc(label)}</li>')
            items_ld.append({"@type": "ListItem", "position": i, "name": label})
    nav = f'<nav class="breadcrumb" aria-label="Breadcrumb"><ol>{"".join(items_html)}</ol></nav>'
    return nav, {"@type": "BreadcrumbList", "itemListElement": items_ld}


# ════════════════════════════════════════════════════════════════════════════
# LAYOUT
# ════════════════════════════════════════════════════════════════════════════
def header(lang: str, active: str) -> str:
    u = UI[lang]
    def link(key, href):
        cls = ' class="active"' if key == active else ""
        return f'<li><a href="{href}"{cls}>{u[key]}</a></li>'
    return f"""<header class="site-nav">
  <a href="{url(lang)}" class="logo" aria-label="PDFPro">PDF<span>Pro</span></a>
  <ul class="nav-links">
    {link("tools", url(lang) + "#tools")}
    {link("blog", url(lang, "blog"))}
    {link("pricing", url(lang, "pricing"))}
  </ul>
  <div class="nav-right">
    <span class="api-status" id="api-status" role="status" data-online="{u['online']}" data-waking="{u['waking']}" data-offline="{u['offline']}">
      <span class="api-dot"></span><span id="api-status-text">{u['waking']}</span>
    </span>
    <a class="nav-cta" href="{url(lang)}#tools">{u['cta']}</a>
  </div>
</header>"""


def footer(lang: str, slug: str) -> str:
    u = UI[lang]
    tools = "".join(f'<li><a href="{url(lang, t["slug"])}">{esc(t[lang]["name"])}</a></li>' for t in TOOLS)
    en_cur = ' aria-current="true"' if lang == "en" else ""
    he_cur = ' aria-current="true"' if lang == "he" else ""
    return f"""<footer class="site-footer">
  <div class="footer-inner">
    <div class="footer-brand">
      <a href="{url(lang)}" class="logo">PDF<span>Pro</span></a>
      <p>{u['footer_desc']}</p>
      <div class="footer-lang">
        <a href="{url('en', slug)}" hreflang="en" lang="en"{en_cur}>English</a>
        <a href="{url('he', slug)}" hreflang="he" lang="he"{he_cur}>עברית</a>
      </div>
    </div>
    <div class="footer-col"><h2>{u['tools']}</h2><ul>{tools}</ul></div>
    <div class="footer-col"><h2>{u['company']}</h2><ul>
      <li><a href="{url(lang, 'about')}">{u['about']}</a></li>
      <li><a href="{url(lang, 'blog')}">{u['blog']}</a></li>
      <li><a href="{url(lang, 'contact')}">{u['contact']}</a></li>
      <li><a href="{url(lang, 'pricing')}">{u['pricing']}</a></li>
    </ul></div>
    <div class="footer-col"><h2>{u['support']}</h2><ul>
      <li><a href="{url(lang, 'help')}">{u['help']}</a></li>
      <li><a href="{url(lang, 'privacy')}">{u['privacy']}</a></li>
      <li><a href="{url(lang, 'terms')}">{u['terms']}</a></li>
    </ul></div>
  </div>
  <div class="footer-bottom">{u['copy']}</div>
</footer>"""


ICON_LINKS = """<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png" type="image/png" sizes="96x96">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#0D1B2A">"""


def page(*, lang: str, slug: str, title: str, desc: str, body: str, active: str = "",
         schema: list | None = None, og_type: str = "website", scripts: str = "") -> str:
    """slug: path without language prefix and without slashes ('' for home, 'blog/x' for articles)."""
    canonical = abs_url(lang, slug)
    graph = {"@context": "https://schema.org", "@graph": schema or []}
    return f"""<!DOCTYPE html>
<html lang="{lang}" dir="{'rtl' if lang == 'he' else 'ltr'}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
{ICON_LINKS}
<link rel="alternate" hreflang="en" href="{abs_url('en', slug)}">
<link rel="alternate" hreflang="he" href="{abs_url('he', slug)}">
<link rel="alternate" hreflang="x-default" href="{abs_url('en', slug)}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="PDFPro">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="{'he_IL' if lang == 'he' else 'en_US'}">
<meta name="twitter:card" content="summary">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="{API}">
<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;600;700;800;900&family=Plus+Jakarta+Sans:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{asset('site.css')}">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script>
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA_ID}');</script>
{ld(graph) if schema else ''}
</head>
<body class="{'rtl' if lang == 'he' else 'ltr'}">
{header(lang, active)}
<main>
{body}
</main>
{footer(lang, slug)}
<script src="{asset('site.js')}"></script>
{scripts}
</body>
</html>
"""


# ════════════════════════════════════════════════════════════════════════════
# PAGE BUILDERS
# ════════════════════════════════════════════════════════════════════════════
def option_html(opt: dict, lang: str) -> str:
    name = opt["name"]
    default = opt.get("default", "")
    if isinstance(default, dict):
        default = default[lang]
    if opt["type"] == "hidden":
        return f'<input type="hidden" name="{name}" value="{esc(default)}">'
    o = opt[lang]
    fid = f"opt-{name}"
    hint = f'<p class="hint" id="{fid}-hint">{esc(o["hint"])}</p>' if o.get("hint") else ""
    described = f' aria-describedby="{fid}-hint"' if o.get("hint") else ""
    if opt["type"] == "signature":
        return f"""<div class="sig" id="sig" data-mode="draw" data-need-draw="{esc(o['need_draw'])}" data-need-text="{esc(o['need_text'])}">
  <div class="sig-head"><span class="sig-label" id="sig-label">{esc(o['label'])}</span>
    <div class="sig-tabs" role="group" aria-labelledby="sig-label">
      <button type="button" data-mode="draw" aria-pressed="true">{esc(o['draw'])}</button>
      <button type="button" data-mode="type" aria-pressed="false">{esc(o['type'])}</button>
    </div></div>
  <div class="sig-draw">
    <canvas id="sig-canvas" aria-label="{esc(o['pad'])}"></canvas>
    <span class="sig-hint" aria-hidden="true">{esc(o['pad'])}</span>
    <button type="button" class="link-btn sig-clear" id="sig-clear">{esc(o['clear'])}</button>
  </div>
  <div class="sig-type" hidden>
    <label for="{fid}">{esc(o['name_label'])}</label>
    <input id="{fid}" name="{name}" type="text" dir="auto" autocomplete="name" placeholder="{esc(o['placeholder'])}" disabled>
  </div>
</div>"""
    if opt["type"] == "password":
        mn = f' data-minlength="{opt["minlength"]}"' if opt.get("minlength") else ""
        ac = opt.get("autocomplete", "off")
        field = (f'<input id="{fid}" name="{name}" type="password" autocomplete="{ac}" dir="ltr" '
                 f'data-required="{esc(UI[lang]["js"]["pw_required"])}"{mn}{described}>')
        out = f'<div><label for="{fid}">{esc(o["label"])}</label>{field}{hint}</div>'
        if opt.get("confirm"):
            out += (f'<div><label for="{fid}-confirm">{esc(o["confirm_label"])}</label>'
                    f'<input id="{fid}-confirm" type="password" autocomplete="{ac}" dir="ltr" data-confirm="{fid}"></div>')
        return out
    extra = ""
    if opt.get("query"):
        extra += ' data-query="1"'
    if opt.get("fields"):
        extra += f' data-fields="{opt["fields"]}"'
    if o.get("required"):
        extra += f' data-required="{esc(o["required"])}"'
    if opt["type"] == "select":
        opts = "".join(
            f'<option value="{esc(v)}"{" selected" if v == default else ""}>{esc(lbl)}</option>'
            for v, lbl in zip(opt["values"], o["labels"]))
        field = f'<select id="{fid}" name="{name}"{described}{extra}>{opts}</select>'
    else:
        tdir = opt.get("dir", "ltr")
        ph = f' placeholder="{esc(o["placeholder"])}"' if o.get("placeholder") else ""
        field = f'<input id="{fid}" name="{name}" type="text" value="{esc(default)}" dir="{tdir}"{ph}{described}{extra}>'
    return f'<div><label for="{fid}">{esc(o["label"])}</label>{field}{hint}</div>'


def tool_intro(slug: str, lang: str, d: dict) -> str:
    f = ROOT / "content" / "tools" / lang / f"{slug}.html"
    return f.read_text(encoding="utf-8") if f.exists() else d.get("intro", "")


def build_tool(tool: dict, lang: str) -> str:
    d, u, api = tool[lang], UI[lang], tool["api"]
    slug = tool["slug"]
    crumbs_html, crumbs_ld = breadcrumb(lang, [(u["home"], url(lang)), (d["name"], None)])

    accept_label = ", ".join(a.strip().lstrip(".").upper() for a in api["accept"].split(","))
    multi_attr = " multiple" if api["multi"] else ""
    drop_text = u["drop_multi"] if api["multi"] else u["drop"]
    opts = "".join(option_html(o, lang) for o in tool["options"])
    visible_opts = [o for o in tool["options"] if o["type"] != "hidden"]
    options_block = f'<div class="tool-options" id="tool-options">{opts}</div>' if tool["options"] else '<div id="tool-options"></div>'
    if tool["options"] and not visible_opts:
        options_block = f'<div id="tool-options" hidden>{opts}</div>'

    steps = "".join(f"<li><h3>{esc(a)}</h3><p>{esc(b)}</p></li>" for a, b in d["steps"])
    faqs = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in d["faqs"])
    related = "".join(f'<li><a href="{url(lang, r)}">{esc(TOOL_BY_SLUG[r][lang]["name"])}</a></li>' for r in d["related"])
    guides = [a for a in ARTICLES if a["tool"] == slug or slug in a.get("also", [])]
    guides_html = ""
    if guides:
        cards = "".join(
            f'<a class="blog-card" href="{url(lang, "blog/" + a["slug"])}"><h3 style="margin:0 0 .3rem">{esc(a[lang]["title"])}</h3><p>{esc(a[lang]["desc"])}</p></a>'
            for a in guides)
        guides_html = f'<h2>{u["guides"]}</h2>{cards}'

    js_cfg = {"slug": slug, "endpoint": api["endpoint"], "field": api["field"], "multi": api["multi"],
              "minFiles": api.get("minFiles", 1), "accept": api["accept"], "result": api["result"],
              "maxMB": MAX_MB, "t": u["js"], "errors": d.get("errors", {})}

    body = f"""<div class="container">
  {crumbs_html}
  <h1>{esc(d['h1'])}</h1>
  <p class="lead">{esc(d['lead'])}</p>

  <section class="tool" aria-label="{esc(d['name'])}">
    <label class="dropzone" id="tool-dropzone" tabindex="0">
      <strong>{drop_text}</strong>
      <small>{u['supports'].format(accept=accept_label, max=MAX_MB)}</small>
      <input type="file" id="tool-input" class="visually-hidden" accept="{api['accept']}"{multi_attr}>
    </label>
    <ul class="file-list" id="tool-files"></ul>
    {options_block}
    <div class="tool-actions">
      <button type="button" class="cta" id="tool-run" disabled>{esc(d['run'])}</button>
      <button type="button" class="link-btn" id="tool-reset" hidden>{u['again']}</button>
    </div>
    <div class="progress" id="tool-progress" aria-hidden="true"><div></div></div>
    <p class="tool-status" id="tool-status" role="status" aria-live="polite"></p>
    <div class="tool-result" id="tool-result" aria-live="polite">
      <h2 id="tool-result-title"></h2>
      <div class="downloads" id="tool-downloads"></div>
      <pre id="tool-preview" hidden></pre>
    </div>
    <p class="tool-note">{u['privacy_line']}</p>
  </section>

  <section class="prose">
    {tool_intro(slug, lang, d)}
    <h2>{u['how']}</h2>
    <ol class="steps">{steps}</ol>
    <h2>{u['faq']}</h2>
    {faqs}
    {guides_html}
    <h2>{u['related']}</h2>
    <ul class="chip-row">{related}</ul>
  </section>
</div>"""

    schema = [
        {"@type": "WebApplication", "name": f"PDFPro {d['name']}", "url": abs_url(lang, slug),
         "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any", "inLanguage": lang,
         "description": d["desc"], "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in d["faqs"]]},
        crumbs_ld,
    ]
    extra_js = f'<script src="{asset(tool["script"])}"></script>\n' if tool.get("script") else ""
    scripts = extra_js + (f"<script>window.TOOL={json.dumps(js_cfg, ensure_ascii=False)};</script>\n"
               f'<script src="{asset("tool.js")}"></script>')
    # keyboard: Enter/Space on the dropzone opens the file picker
    scripts += "\n<script>document.getElementById('tool-dropzone').addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();document.getElementById('tool-input').click();}});</script>"
    return page(lang=lang, slug=slug, title=d["title"], desc=d["desc"], body=body,
                active="tools", schema=schema, scripts=scripts)


def build_static(key: str, data: dict, lang: str) -> str:
    u = UI[lang]
    crumbs_html, crumbs_ld = breadcrumb(lang, [(u["home"], url(lang)), (data["title"].split(" | ")[0].split(" – ")[0], None)])
    h1 = data.get("h1") or data["title"].split(" | ")[0].split(" – ")[0]
    body = f'<div class="container narrow prose">\n{crumbs_html}\n<h1>{esc(h1)}</h1>\n{data["body"]}\n</div>'
    return page(lang=lang, slug=key, title=data["title"], desc=data["desc"], body=body,
                active=key if key == "pricing" else "", schema=[crumbs_ld])


def build_blog_index(lang: str) -> str:
    u, m = UI[lang], BLOG_META[lang]
    crumbs_html, crumbs_ld = breadcrumb(lang, [(u["home"], url(lang)), (u["blog"], None)])
    cards = "".join(
        f'<a class="blog-card" href="{url(lang, "blog/" + a["slug"])}">'
        f'<time datetime="{a["published"]}">{fmt_date(a["published"], lang)}</time>'
        f'<span class="tag">{esc(a[lang]["tag"])}</span>'
        f'<h2>{esc(a[lang]["title"])}</h2><p>{esc(a[lang]["desc"])}</p></a>'
        for a in sorted(ARTICLES, key=lambda a: a["published"], reverse=True))
    body = f'<div class="container narrow">\n{crumbs_html}\n<h1>{m["h1"]}</h1>\n<p class="lead">{m["lead"]}</p>\n{cards}\n</div>'
    return page(lang=lang, slug="blog", title=m["title"], desc=m["desc"], body=body, active="blog", schema=[crumbs_ld])


def build_article(art: dict, lang: str) -> str:
    u, d = UI[lang], art[lang]
    slug = "blog/" + art["slug"]
    content = (ROOT / "content" / "blog" / lang / f"{art['slug']}.html").read_text(encoding="utf-8")
    crumbs_html, crumbs_ld = breadcrumb(lang, [(u["home"], url(lang)), (u["blog"], url(lang, "blog")), (d["title"], None)])
    cta = ""
    if art["tool"] and d.get("cta"):
        cta = f'<div class="card article-cta"><a href="{url(lang, art["tool"])}" class="cta">{esc(d["cta"])}</a></div>'
    updated = art.get("updated", art["published"])
    body = f"""<article class="container narrow prose">
{crumbs_html}
<span class="tag">{esc(d['tag'])}</span>
<h1>{esc(d['title'])}</h1>
<p class="meta"><time datetime="{art['published']}">{fmt_date(art['published'], lang)}</time></p>
{content}
{cta}
</article>"""
    schema = [
        {"@type": "Article", "headline": d["title"], "description": d["desc"], "inLanguage": lang,
         "datePublished": art["published"], "dateModified": updated,
         "author": {"@type": "Organization", "name": "PDFPro", "url": SITE},
         "publisher": {"@type": "Organization", "name": "PDFPro", "url": SITE},
         "mainEntityOfPage": abs_url(lang, slug)},
        crumbs_ld,
    ]
    return page(lang=lang, slug=slug, title=f"{d['title']} | PDFPro", desc=d["desc"], body=body,
                active="blog", schema=schema, og_type="article")


# ════════════════════════════════════════════════════════════════════════════
# OUTPUT, SITEMAP, CHECKS
# ════════════════════════════════════════════════════════════════════════════
MANIFEST = ROOT / ".build-manifest.json"


def main() -> None:
    manifest = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    today = date.today().isoformat()
    outputs: dict[str, str] = {}   # site path -> html

    for lang in LANGS:
        for tool in TOOLS:
            outputs[url(lang, tool["slug"])] = build_tool(tool, lang)
        for key, data in static_pages().items():
            outputs[url(lang, key)] = build_static(key, data[lang], lang)
        outputs[url(lang, "blog")] = build_blog_index(lang)
        for art in ARTICLES:
            outputs[url(lang, "blog/" + art["slug"])] = build_article(art, lang)

    written = 0
    for path, html_doc in outputs.items():
        f = ROOT / path.strip("/") / "index.html"
        f.parent.mkdir(parents=True, exist_ok=True)
        # lastmod only moves when the page content (ignoring asset hashes) changes
        h = hashlib.md5(re.sub(r"\?v=[0-9a-f]{8}", "", html_doc).encode()).hexdigest()
        if manifest.get(path, {}).get("hash") != h:
            manifest[path] = {"hash": h, "lastmod": today}
        if not f.exists() or f.read_text(encoding="utf-8") != html_doc:
            f.write_text(html_doc, encoding="utf-8")
            written += 1

    # homepages are hand-maintained: track their lastmod from file contents
    for path in ("/", "/he/"):
        f = ROOT / path.strip("/") / "index.html" if path != "/" else ROOT / "index.html"
        h = hashlib.md5(f.read_bytes()).hexdigest()
        if manifest.get(path, {}).get("hash") != h:
            manifest[path] = {"hash": h, "lastmod": today}

    # sitemap: every page with its hreflang pair
    def counterpart(p):  # '/x/' <-> '/he/x/'
        return p[3:] if p.startswith("/he/") else "/he" + p
    urls = sorted(set(outputs) | {"/", "/he/"}, key=lambda p: (p.startswith("/he"), p))
    entries = []
    for p in urls:
        en, he = (counterpart(p), p) if p.startswith("/he/") else (p, counterpart(p))
        entries.append(
            f"  <url>\n    <loc>{SITE}{p}</loc>\n    <lastmod>{manifest[p]['lastmod']}</lastmod>\n"
            f'    <xhtml:link rel="alternate" hreflang="en" href="{SITE}{en}"/>\n'
            f'    <xhtml:link rel="alternate" hreflang="he" href="{SITE}{he}"/>\n'
            f'    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{en}"/>\n  </url>')
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(entries) + "\n</urlset>\n", encoding="utf-8")

    (ROOT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n"
        "# API paths appear inside homepage JavaScript; they are not pages.\n"
        "Disallow: /api/\n\n"
        f"Sitemap: {SITE}/sitemap.xml\n", encoding="utf-8")

    MANIFEST.write_text(json.dumps(manifest, indent=1, sort_keys=True))

    # ── internal link check over every page, including homepages ──
    known = set(urls)
    broken = []
    for p in urls:
        f = ROOT / "index.html" if p == "/" else ROOT / p.strip("/") / "index.html"
        for href in re.findall(r'href="(/[^"#?]*)', f.read_text(encoding="utf-8")):
            if href.startswith("/assets/") or href.endswith((".xml", ".txt", ".css", ".js", ".png", ".ico", ".svg", ".webmanifest")):
                continue
            target = href if href.endswith("/") else href + "/"
            if target not in known:
                broken.append((p, href))

    print(f"Built {len(outputs)} pages ({written} changed) + sitemap.xml ({len(urls)} URLs) + robots.txt")
    if broken:
        print("\nBROKEN INTERNAL LINKS:")
        for src, href in broken:
            print(f"  {src} -> {href}")
        raise SystemExit(1)
    print("Internal links: OK")


if __name__ == "__main__":
    main()
