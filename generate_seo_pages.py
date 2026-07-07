"""
generate_seo_pages.py
=====================
מייצר דפי נחיתה SEO לכל כלי — אנגלית + עברית.

הרץ: python generate_seo_pages.py
יוצר תיקיית output/ עם כל הדפים.
"""

import os
import json

BASE_URL = "https://www.pdfproapp.com"

# ── Tool definitions ───────────────────────────────────────────────────────────
TOOLS = [
    {
        "slug": "pdf-to-word",
        "en": {
            "title": "PDF to Word Converter — Free Online | PDFPro",
            "desc": "Convert PDF to Word (DOCX) online for free. Preserve formatting, fonts and layout. No installation needed.",
            "h1": "PDF to Word Converter",
            "subtitle": "Convert any PDF to an editable Word document in seconds. Free, fast, and accurate.",
            "keywords": "pdf to word, convert pdf to word, pdf to docx, pdf converter",
            "steps": [
                ("Upload your PDF", "Click the upload button or drag and drop your PDF file."),
                ("Convert automatically", "Our engine converts your PDF while preserving all formatting."),
                ("Download your Word file", "Get your editable .docx file instantly."),
            ],
            "faqs": [
                ("Is it free to convert PDF to Word?", "Yes, PDFPro offers free PDF to Word conversion. Free users get 5 conversions per day."),
                ("Will my formatting be preserved?", "Yes, our converter preserves fonts, tables, images and layout as accurately as possible."),
                ("What is the maximum file size?", "Free users can convert files up to 100MB. Pro users up to 500MB."),
                ("Can I convert scanned PDFs?", "Yes, our OCR engine can extract text from scanned documents before converting to Word."),
            ],
            "related": ["pdf-to-excel", "pdf-to-pptx", "compress-pdf"],
        },
        "he": {
            "title": "המרת PDF ל-Word בחינם | PDFPro",
            "desc": "המר PDF לקובץ Word הניתן לעריכה בחינם. שמירה על עיצוב, גופנים ופריסה. ללא התקנה.",
            "h1": "המרת PDF ל-Word",
            "subtitle": "המר כל קובץ PDF למסמך Word הניתן לעריכה תוך שניות. חינם, מהיר ומדויק.",
            "keywords": "המרת pdf לוורד, pdf לוורד, pdf ל word, המרת pdf",
            "steps": [
                ("העלה את ה-PDF שלך", "לחץ על כפתור ההעלאה או גרור את קובץ ה-PDF."),
                ("המרה אוטומטית", "המנוע שלנו ממיר את ה-PDF תוך שמירה על העיצוב."),
                ("הורד את קובץ ה-Word", "קבל את קובץ ה-.docx הניתן לעריכה מיידית."),
            ],
            "faqs": [
                ("האם ההמרה מ-PDF ל-Word חינמית?", "כן, PDFPro מציע המרת PDF ל-Word בחינם. משתמשים חינמיים מקבלים 5 המרות ביום."),
                ("האם העיצוב ישמר?", "כן, הממיר שלנו שומר על גופנים, טבלאות, תמונות ופריסה בדיוק מרבי."),
                ("מה גודל הקובץ המקסימלי?", "משתמשים חינמיים יכולים להמיר קבצים עד 100MB. משתמשי Pro עד 500MB."),
                ("אפשר להמיר PDF סרוק?", "כן, מנוע ה-OCR שלנו יכול לחלץ טקסט ממסמכים סרוקים לפני ההמרה ל-Word."),
            ],
            "related": ["pdf-to-excel", "pdf-to-pptx", "compress-pdf"],
        },
    },
    {
        "slug": "pdf-to-excel",
        "en": {
            "title": "PDF to Excel Converter — Free Online | PDFPro",
            "desc": "Convert PDF tables to Excel spreadsheets online. Extract data accurately. Free, no signup required.",
            "h1": "PDF to Excel Converter",
            "subtitle": "Extract tables and data from PDF files directly into Excel spreadsheets. Fast and accurate.",
            "keywords": "pdf to excel, convert pdf to excel, pdf to xlsx, extract tables from pdf",
            "steps": [
                ("Upload your PDF", "Select a PDF file containing tables or data."),
                ("Extract tables", "Our engine automatically detects and extracts all tables."),
                ("Download Excel file", "Get your .xlsx file with all data perfectly organized."),
            ],
            "faqs": [
                ("Can it extract tables from PDF?", "Yes, PDFPro automatically detects and extracts tables from PDFs into Excel sheets."),
                ("What if my PDF has multiple tables?", "Each table is placed on a separate Excel sheet, clearly labeled by page number."),
                ("Does it work with scanned PDFs?", "For scanned PDFs, use our OCR tool first to make them searchable, then convert to Excel."),
                ("Is the Excel conversion free?", "Yes, free users get 5 conversions per day. Upgrade to Pro for unlimited conversions."),
            ],
            "related": ["pdf-to-word", "pdf-to-pptx", "compress-pdf"],
        },
        "he": {
            "title": "המרת PDF ל-Excel בחינם | PDFPro",
            "desc": "המר טבלאות PDF לגיליון Excel אונליין. חילוץ נתונים מדויק. חינם, ללא הרשמה.",
            "h1": "המרת PDF ל-Excel",
            "subtitle": "חלץ טבלאות ונתונים מקבצי PDF ישירות לגיליונות Excel. מהיר ומדויק.",
            "keywords": "המרת pdf לאקסל, pdf לאקסל, חילוץ טבלאות מ-pdf, pdf ל excel",
            "steps": [
                ("העלה את ה-PDF שלך", "בחר קובץ PDF המכיל טבלאות או נתונים."),
                ("חילוץ טבלאות", "המנוע שלנו מזהה ומחלץ אוטומטית את כל הטבלאות."),
                ("הורד קובץ Excel", "קבל את קובץ ה-.xlsx עם כל הנתונים מאורגנים בצורה מושלמת."),
            ],
            "faqs": [
                ("האם הוא מחלץ טבלאות מ-PDF?", "כן, PDFPro מזהה ומחלץ אוטומטית טבלאות מ-PDFs לגיליונות Excel."),
                ("מה אם יש מספר טבלאות?", "כל טבלה מוכנסת לגיליון Excel נפרד, מסומן לפי מספר עמוד."),
                ("עובד עם PDF סרוק?", "לPDF סרוקים, השתמש קודם בכלי ה-OCR שלנו ואז המר ל-Excel."),
                ("ההמרה חינמית?", "כן, משתמשים חינמיים מקבלים 5 המרות ביום. שדרג ל-Pro להמרות ללא הגבלה."),
            ],
            "related": ["pdf-to-word", "pdf-to-pptx", "compress-pdf"],
        },
    },
    {
        "slug": "compress-pdf",
        "en": {
            "title": "Compress PDF Online — Reduce PDF Size Free | PDFPro",
            "desc": "Compress PDF files online for free. Reduce PDF size by up to 80% without losing quality. Fast and easy.",
            "h1": "Compress PDF Online",
            "subtitle": "Reduce your PDF file size by up to 80% while maintaining quality. Perfect for email and sharing.",
            "keywords": "compress pdf, reduce pdf size, pdf compressor, shrink pdf, pdf file size reducer",
            "steps": [
                ("Upload your PDF", "Select the PDF file you want to compress."),
                ("Choose compression level", "Select from Low (lossless), Medium, High, or Extreme compression."),
                ("Download compressed file", "Get your smaller PDF file instantly."),
            ],
            "faqs": [
                ("How much can I reduce my PDF size?", "Depending on content, you can reduce file size by 10-80%. Image-heavy PDFs compress the most."),
                ("Will compression affect quality?", "Low compression is near-lossless. Higher levels reduce image quality slightly but dramatically shrink file size."),
                ("What is the best compression level?", "Medium is recommended for most use cases — great size reduction with minimal quality loss."),
                ("Is PDF compression free?", "Yes, compressing PDFs is free. Free users can compress up to 5 files per day."),
            ],
            "related": ["merge-pdf", "split-pdf", "pdf-to-word"],
        },
        "he": {
            "title": "דחיסת PDF אונליין — הקטן PDF חינם | PDFPro",
            "desc": "דחוס קבצי PDF אונליין בחינם. הקטן גודל PDF עד 80% ללא אובדן איכות. מהיר וקל.",
            "h1": "דחיסת PDF אונליין",
            "subtitle": "הקטן את גודל קובץ ה-PDF שלך עד 80% תוך שמירה על איכות. מושלם לשליחה במייל.",
            "keywords": "דחיסת pdf, הקטנת pdf, דחיסת קבצי pdf, להקטין pdf",
            "steps": [
                ("העלה את ה-PDF שלך", "בחר את קובץ ה-PDF שברצונך לדחוס."),
                ("בחר רמת דחיסה", "בחר מבין נמוכה, בינונית, גבוהה או מקסימלית."),
                ("הורד קובץ דחוס", "קבל את קובץ ה-PDF הקטן יותר מיידית."),
            ],
            "faqs": [
                ("כמה אפשר להקטין PDF?", "תלוי בתוכן, ניתן להקטין 10-80%. PDFs עם הרבה תמונות נדחסים הכי הרבה."),
                ("האם הדחיסה תפגע באיכות?", "דחיסה נמוכה כמעט ללא אובדן. רמות גבוהות יותר מקטינות קצת את איכות התמונות."),
                ("מה רמת הדחיסה הטובה ביותר?", "בינונית מומלצת לרוב המקרים — הקטנה טובה עם אובדן מינימלי."),
                ("דחיסת PDF חינמית?", "כן, דחיסת PDFs חינמית. משתמשים חינמיים יכולים לדחוס עד 5 קבצים ביום."),
            ],
            "related": ["merge-pdf", "split-pdf", "pdf-to-word"],
        },
    },
    {
        "slug": "merge-pdf",
        "en": {
            "title": "Merge PDF Files Online — Combine PDFs Free | PDFPro",
            "desc": "Merge multiple PDF files into one online. Combine PDFs in any order. Free, fast, secure.",
            "h1": "Merge PDF Files",
            "subtitle": "Combine multiple PDF documents into a single file. Drag, drop, and merge in seconds.",
            "keywords": "merge pdf, combine pdf, join pdf files, pdf merger, merge pdf online",
            "steps": [
                ("Upload your PDFs", "Select 2 or more PDF files to merge. Up to 20 files at once."),
                ("Arrange the order", "Files are merged in the order you upload them."),
                ("Download merged PDF", "Get your combined PDF file instantly."),
            ],
            "faqs": [
                ("How many PDFs can I merge at once?", "You can merge up to 20 PDF files in a single operation."),
                ("Will the quality be affected?", "No, merging PDFs does not affect the quality of any content."),
                ("Can I merge password-protected PDFs?", "You'll need to unlock them first using our PDF Unlock tool."),
                ("Is merging PDFs free?", "Yes, merging PDFs is free for up to 5 operations per day."),
            ],
            "related": ["split-pdf", "compress-pdf", "pdf-to-word"],
        },
        "he": {
            "title": "מיזוג PDF אונליין — חבר PDFs בחינם | PDFPro",
            "desc": "מזג מספר קבצי PDF לקובץ אחד אונליין. חבר PDFs בכל סדר. חינם, מהיר, מאובטח.",
            "h1": "מיזוג קבצי PDF",
            "subtitle": "חבר מספר מסמכי PDF לקובץ אחד. גרור, שחרר ומזג תוך שניות.",
            "keywords": "מיזוג pdf, חיבור pdf, לאחד קבצי pdf, מיזוג קבצים",
            "steps": [
                ("העלה את ה-PDFs שלך", "בחר 2 קבצי PDF או יותר למיזוג. עד 20 קבצים בבת אחת."),
                ("סדר את הקבצים", "הקבצים ממוזגים בסדר ההעלאה שלהם."),
                ("הורד PDF ממוזג", "קבל את קובץ ה-PDF המשולב מיידית."),
            ],
            "faqs": [
                ("כמה PDFs אפשר למזג?", "ניתן למזג עד 20 קבצי PDF בפעולה אחת."),
                ("האם האיכות תיפגע?", "לא, מיזוג PDFs לא משפיע על איכות התוכן."),
                ("אפשר למזג PDF מוגן סיסמה?", "צריך לבטל את הנעילה קודם עם כלי שחרור הסיסמה שלנו."),
                ("המיזוג חינמי?", "כן, מיזוג PDFs חינמי עד 5 פעולות ביום."),
            ],
            "related": ["split-pdf", "compress-pdf", "pdf-to-word"],
        },
    },
    {
        "slug": "split-pdf",
        "en": {
            "title": "Split PDF Online — Extract Pages Free | PDFPro",
            "desc": "Split PDF files by page range online. Extract specific pages or split into equal parts. Free and easy.",
            "h1": "Split PDF Online",
            "subtitle": "Divide large PDF documents into smaller files. Split by page range, every N pages, or extract specific pages.",
            "keywords": "split pdf, pdf splitter, extract pages from pdf, divide pdf, pdf page extractor",
            "steps": [
                ("Upload your PDF", "Select the large PDF file you want to split."),
                ("Set split options", "Choose page ranges (e.g. 1-3, 4-6) or split every N pages."),
                ("Download split files", "Download all parts as separate PDF files."),
            ],
            "faqs": [
                ("How do I split a PDF by page range?", "Enter page ranges like '1-3,4-6' and we'll create separate PDFs for each range."),
                ("Can I extract a single page?", "Yes, enter a single page number (e.g. '5') to extract just that page."),
                ("Is there a limit on PDF size?", "Free users can split PDFs up to 100MB. Pro users up to 500MB."),
                ("Is splitting PDFs free?", "Yes, free for up to 5 operations per day."),
            ],
            "related": ["merge-pdf", "compress-pdf", "pdf-to-word"],
        },
        "he": {
            "title": "פיצול PDF אונליין — חלץ עמודים בחינם | PDFPro",
            "desc": "פצל קבצי PDF לפי טווח עמודים אונליין. חלץ עמודים ספציפיים. חינם וקל.",
            "h1": "פיצול PDF אונליין",
            "subtitle": "חלק מסמכי PDF גדולים לקבצים קטנים יותר. פצל לפי טווח עמודים או חלץ עמודים ספציפיים.",
            "keywords": "פיצול pdf, חילוץ עמודים מ-pdf, לפצל pdf, פיצול קובץ pdf",
            "steps": [
                ("העלה את ה-PDF שלך", "בחר את קובץ ה-PDF הגדול שברצונך לפצל."),
                ("הגדר אפשרויות פיצול", "בחר טווחי עמודים (לדוגמה 1-3,4-6) או פצל כל N עמודים."),
                ("הורד קבצים מפוצלים", "הורד את כל החלקים כקבצי PDF נפרדים."),
            ],
            "faqs": [
                ("איך מפצלים PDF לפי טווח עמודים?", "הכנס טווחים כמו '1-3,4-6' ואנחנו ניצור PDFs נפרדים לכל טווח."),
                ("אפשר לחלץ עמוד בודד?", "כן, הכנס מספר עמוד בודד (לדוגמה '5') כדי לחלץ רק אותו."),
                ("יש הגבלה על גודל PDF?", "משתמשים חינמיים יכולים לפצל PDFs עד 100MB. Pro עד 500MB."),
                ("הפיצול חינמי?", "כן, חינמי עד 5 פעולות ביום."),
            ],
            "related": ["merge-pdf", "compress-pdf", "pdf-to-word"],
        },
    },
    {
        "slug": "ocr-pdf",
        "en": {
            "title": "OCR PDF — Extract Text from Scanned PDF Free | PDFPro",
            "desc": "Extract text from scanned PDFs and images using OCR. Supports Hebrew, Arabic, English and 40+ languages. Free.",
            "h1": "OCR — Extract Text from PDF",
            "subtitle": "Convert scanned documents and images to searchable, editable text using our powerful OCR engine.",
            "keywords": "ocr pdf, extract text from pdf, pdf ocr, scanned pdf to text, image to text, hebrew ocr",
            "steps": [
                ("Upload scanned PDF or image", "Upload your scanned document, image, or photo of text."),
                ("Select language", "Choose the language(s) in your document (Hebrew, English, Arabic, etc.)."),
                ("Extract and download text", "Get your extracted text as TXT, searchable PDF, or Word document."),
            ],
            "faqs": [
                ("Does OCR support Hebrew?", "Yes! Our OCR engine supports Hebrew, Arabic, English and 40+ languages simultaneously."),
                ("What image formats are supported?", "We support PDF, JPG, PNG, TIFF, BMP and other common image formats."),
                ("How accurate is the OCR?", "Accuracy depends on document quality. Clear, high-resolution scans typically achieve 95%+ accuracy."),
                ("Can it handle mixed Hebrew-English documents?", "Yes, select 'heb+eng' language mode to handle documents with both languages."),
            ],
            "related": ["pdf-to-word", "translate-pdf", "compress-pdf"],
        },
        "he": {
            "title": "OCR — חילוץ טקסט מ-PDF סרוק בחינם | PDFPro",
            "desc": "חלץ טקסט מ-PDFs סרוקים ותמונות באמצעות OCR. תמיכה בעברית, ערבית, אנגלית ו-40+ שפות.",
            "h1": "OCR — זיהוי טקסט ב-PDF",
            "subtitle": "המר מסמכים סרוקים ותמונות לטקסט חיפוש ועריכה באמצעות מנוע ה-OCR החזק שלנו.",
            "keywords": "ocr עברית, זיהוי טקסט מ-pdf, pdf סרוק לטקסט, חילוץ טקסט מתמונה",
            "steps": [
                ("העלה PDF סרוק או תמונה", "העלה את המסמך הסרוק, התמונה או הצילום של הטקסט."),
                ("בחר שפה", "בחר את השפה/ות במסמך שלך (עברית, אנגלית, ערבית וכו')."),
                ("חלץ והורד טקסט", "קבל את הטקסט המחולץ כ-TXT, PDF חיפוש, או מסמך Word."),
            ],
            "faqs": [
                ("האם OCR תומך בעברית?", "כן! מנוע ה-OCR שלנו תומך בעברית, ערבית, אנגלית ו-40+ שפות בו-זמנית."),
                ("אילו פורמטי תמונה נתמכים?", "אנחנו תומכים ב-PDF, JPG, PNG, TIFF, BMP ופורמטים נפוצים אחרים."),
                ("כמה מדויק ה-OCR?", "הדיוק תלוי באיכות המסמך. סריקות ברורות בדרך כלל מגיעות ל-95%+ דיוק."),
                ("אפשר לטפל במסמכים עברית-אנגלית?", "כן, בחר מצב שפה 'heb+eng' לטיפול במסמכים עם שתי השפות."),
            ],
            "related": ["pdf-to-word", "translate-pdf", "compress-pdf"],
        },
    },
    {
        "slug": "translate-pdf",
        "en": {
            "title": "Translate PDF Online — Free PDF Translation | PDFPro",
            "desc": "Translate PDF documents to 40+ languages online. Supports Hebrew, Arabic, English, Russian and more. Free.",
            "h1": "Translate PDF Online",
            "subtitle": "Translate your PDF documents into any language while preserving the original layout. Powered by AI.",
            "keywords": "translate pdf, pdf translation, translate pdf to english, translate pdf to hebrew, pdf translator",
            "steps": [
                ("Upload your PDF", "Select the PDF document you want to translate."),
                ("Choose target language", "Select from 40+ supported languages including Hebrew, Arabic, Russian."),
                ("Download translated PDF", "Get your translated document as a PDF."),
            ],
            "faqs": [
                ("How many languages are supported?", "We support 40+ languages including Hebrew, Arabic, English, Russian, French, German, Spanish and more."),
                ("Will the layout be preserved?", "We offer layout-preserving mode that tries to maintain the original document structure."),
                ("Is PDF translation accurate?", "Translation quality is powered by Google Translate and is generally excellent for common languages."),
                ("Can I translate Hebrew PDFs to English?", "Yes, simply upload your Hebrew PDF and select English as the target language."),
            ],
            "related": ["ocr-pdf", "pdf-to-word", "compress-pdf"],
        },
        "he": {
            "title": "תרגום PDF אונליין — תרגום PDF חינמי | PDFPro",
            "desc": "תרגם מסמכי PDF ל-40+ שפות אונליין. תמיכה בעברית, ערבית, אנגלית, רוסית ועוד. חינם.",
            "h1": "תרגום PDF אונליין",
            "subtitle": "תרגם את מסמכי ה-PDF שלך לכל שפה תוך שמירה על הפריסה המקורית. מונע בבינה מלאכותית.",
            "keywords": "תרגום pdf, לתרגם pdf, תרגום מסמך pdf, pdf לעברית",
            "steps": [
                ("העלה את ה-PDF שלך", "בחר את מסמך ה-PDF שברצונך לתרגם."),
                ("בחר שפת יעד", "בחר מ-40+ שפות נתמכות כולל עברית, ערבית, רוסית."),
                ("הורד PDF מתורגם", "קבל את המסמך המתורגם כ-PDF."),
            ],
            "faqs": [
                ("כמה שפות נתמכות?", "אנחנו תומכים ב-40+ שפות כולל עברית, ערבית, אנגלית, רוסית, צרפתית, גרמנית, ספרדית ועוד."),
                ("האם הפריסה תישמר?", "אנחנו מציעים מצב שמירת פריסה שמנסה לשמור על מבנה המסמך המקורי."),
                ("האם התרגום מדויק?", "איכות התרגום מונעת על ידי Google Translate ובדרך כלל מצוינת לשפות נפוצות."),
                ("אפשר לתרגם PDF אנגלי לעברית?", "כן, פשוט העלה את ה-PDF האנגלי ובחר עברית כשפת יעד."),
            ],
            "related": ["ocr-pdf", "pdf-to-word", "compress-pdf"],
        },
    },
]

# ── HTML Template ─────────────────────────────────────────────────────────────
def build_page(tool, lang, base_url):
    data = tool[lang]
    slug = tool["slug"]
    is_he = lang == "he"
    dir_attr = 'dir="rtl"' if is_he else 'dir="ltr"'
    lang_attr = 'he' if is_he else 'en'
    font = "'Heebo', sans-serif" if is_he else "'Plus Jakarta Sans', sans-serif"
    canonical = f"{base_url}/{'he/' if is_he else ''}{slug}"
    alt_lang = "en" if is_he else "he"
    alt_url = f"{base_url}/{'he/' if not is_he else ''}{slug}"
    main_url = f"{base_url}/{'he' if is_he else ''}"

    # Related tools links
    related_html = ""
    for r_slug in data["related"]:
        r_url = f"{base_url}/{'he/' if is_he else ''}{r_slug}"
        related_html += f'<a href="{r_url}" style="display:inline-block;padding:0.5rem 1rem;background:#f0f4ff;border-radius:6px;text-decoration:none;color:#0D1B2A;font-size:0.88rem;font-weight:600">{r_slug.replace("-"," ").title()}</a>\n'

    # Steps
    steps_html = ""
    schema_steps = []
    for i, (step_name, step_desc) in enumerate(data["steps"], 1):
        steps_html += f"""
        <div style="display:flex;gap:1.5rem;align-items:flex-start;margin-bottom:1.5rem">
          <div style="width:40px;height:40px;border-radius:50%;background:#E02020;color:white;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:1.1rem;flex-shrink:0">{i}</div>
          <div>
            <h3 style="font-size:1rem;font-weight:700;margin-bottom:0.3rem;color:#0D1B2A">{step_name}</h3>
            <p style="color:#5A6A7A;line-height:1.6">{step_desc}</p>
          </div>
        </div>"""
        schema_steps.append({"@type":"HowToStep","name":step_name,"text":step_desc,"position":i})

    # FAQs
    faq_html = ""
    schema_faqs = []
    for q, a in data["faqs"]:
        faq_html += f"""
        <details style="border:1px solid #D8D0C4;border-radius:10px;padding:1rem 1.2rem;margin-bottom:0.8rem;background:white">
          <summary style="font-weight:700;cursor:pointer;color:#0D1B2A;list-style:none;display:flex;justify-content:space-between;align-items:center">
            {q} <span style="color:#E02020;font-size:1.2rem">+</span>
          </summary>
          <p style="margin-top:0.8rem;color:#5A6A7A;line-height:1.7">{a}</p>
        </details>"""
        schema_faqs.append({"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}})

    # Schema.org
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "name": data["title"],
                "description": data["desc"],
                "url": canonical,
                "inLanguage": lang_attr,
                "isPartOf": {"@type":"WebSite","name":"PDFPro","url":base_url},
            },
            {
                "@type": "HowTo",
                "name": data["h1"],
                "description": data["subtitle"],
                "step": schema_steps,
            },
            {
                "@type": "FAQPage",
                "mainEntity": schema_faqs,
            }
        ]
    }

    cta_text = "המר עכשיו — חינם" if is_he else "Convert Now — Free"
    steps_title = "איך זה עובד?" if is_he else "How It Works"
    faq_title = "שאלות נפוצות" if is_he else "Frequently Asked Questions"
    related_title = "כלים קשורים" if is_he else "Related Tools"
    nav_tools = "כלים" if is_he else "Tools"
    nav_back = "← חזרה לכל הכלים" if is_he else "← All Tools"

    return f"""<!DOCTYPE html>
<html lang="{lang_attr}" {dir_attr}>
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{data['title']}</title>
<meta name="description" content="{data['desc']}"/>
<meta name="keywords" content="{data['keywords']}"/>
<link rel="canonical" href="{canonical}"/>
<link rel="alternate" hreflang="{alt_lang}" href="{alt_url}"/>
<link rel="alternate" hreflang="{lang_attr}" href="{canonical}"/>
<link rel="alternate" hreflang="x-default" href="{base_url}/{slug}"/>
<meta property="og:title" content="{data['title']}"/>
<meta property="og:description" content="{data['desc']}"/>
<meta property="og:url" content="{canonical}"/>
<meta property="og:type" content="website"/>
<meta property="og:site_name" content="PDFPro"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="{data['title']}"/>
<meta name="twitter:description" content="{data['desc']}"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;600;700;800;900&family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet"/>
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False, indent=2)}</script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:{font};background:#F8F5F0;color:#0D1B2A;direction:{'rtl' if is_he else 'ltr'}}}
nav{{background:#0D1B2A;padding:0 2rem;height:64px;display:flex;align-items:center;justify-content:space-between;border-bottom:2px solid #E02020;position:sticky;top:0;z-index:100}}
.logo{{font-size:1.5rem;font-weight:900;color:white;text-decoration:none}}.logo span{{color:#FF4444}}
.nav-link{{color:rgba(255,255,255,0.7);text-decoration:none;font-size:0.9rem;font-weight:500}}
.nav-link:hover{{color:white}}
.hero{{background:#0D1B2A;padding:4rem 2rem;text-align:center}}
.hero h1{{font-size:2.5rem;font-weight:900;color:white;margin-bottom:1rem;letter-spacing:-0.5px}}
.hero p{{font-size:1.1rem;color:rgba(255,255,255,0.7);max-width:600px;margin:0 auto 2rem;line-height:1.7}}
.cta-btn{{display:inline-block;background:#E02020;color:white;padding:1rem 2.5rem;border-radius:8px;text-decoration:none;font-weight:700;font-size:1.05rem;transition:background 0.2s;box-shadow:0 4px 20px rgba(224,32,32,0.4)}}
.cta-btn:hover{{background:#B31515}}
.container{{max-width:800px;margin:0 auto;padding:3rem 2rem}}
.card{{background:white;border-radius:12px;padding:2rem;border:1px solid #D8D0C4;margin-bottom:2rem}}
.section-title{{font-size:1.5rem;font-weight:800;color:#0D1B2A;margin-bottom:1.5rem}}
footer{{background:#0D1B2A;padding:2rem;text-align:center;color:rgba(255,255,255,0.4);font-size:0.85rem;margin-top:3rem}}
footer a{{color:rgba(255,255,255,0.6);text-decoration:none}}
details summary::-webkit-details-marker{{display:none}}
@media(max-width:600px){{.hero h1{{font-size:1.8rem}}.container{{padding:1.5rem 1rem}}}}
</style>
</head>
<body>
<nav>
  <a href="{main_url}" class="logo">PDF<span>Pro</span></a>
  <div style="display:flex;gap:1.5rem;align-items:center">
    <a href="{alt_url}" class="nav-link">{'EN' if is_he else 'עב'}</a>
    <a href="{main_url}" class="nav-link">{nav_tools}</a>
  </div>
</nav>

<div class="hero">
  <a href="{main_url}" style="display:inline-block;color:rgba(255,255,255,0.5);text-decoration:none;font-size:0.85rem;margin-bottom:1.5rem">{nav_back}</a>
  <h1>{data['h1']}</h1>
  <p>{data['subtitle']}</p>
  <a href="{main_url}#{slug}" class="cta-btn">{cta_text}</a>
</div>

<div class="container">
  <div class="card">
    <h2 class="section-title">{steps_title}</h2>
    {steps_html}
    <div style="text-align:center;margin-top:1.5rem">
      <a href="{main_url}#{slug}" class="cta-btn">{cta_text}</a>
    </div>
  </div>

  <div class="card">
    <h2 class="section-title">{faq_title}</h2>
    {faq_html}
  </div>

  <div class="card">
    <h2 class="section-title">{related_title}</h2>
    <div style="display:flex;gap:0.8rem;flex-wrap:wrap">
      {related_html}
    </div>
  </div>
</div>

<footer>
  <a href="{main_url}" class="logo" style="font-size:1.2rem;display:block;margin-bottom:0.8rem">PDF<span>Pro</span></a>
  <p>© 2026 PDFPro. {'כל הזכויות שמורות.' if is_he else 'All rights reserved.'}</p>
</footer>
</body>
</html>"""


# ── Generate all pages ────────────────────────────────────────────────────────
def generate_all():
    out_dir = "seo_pages"
    os.makedirs(out_dir, exist_ok=True)

    total = 0
    for tool in TOOLS:
        slug = tool["slug"]

        # English page
        en_dir = os.path.join(out_dir, slug)
        os.makedirs(en_dir, exist_ok=True)
        with open(os.path.join(en_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(build_page(tool, "en", BASE_URL))
        print(f"✅ EN: /{slug}/")

        # Hebrew page
        he_dir = os.path.join(out_dir, "he", slug)
        os.makedirs(he_dir, exist_ok=True)
        with open(os.path.join(he_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(build_page(tool, "he", BASE_URL))
        print(f"✅ HE: /he/{slug}/")

        total += 2

    print(f"\n🎉 Generated {total} pages in ./{out_dir}/")
    print(f"📁 Copy contents of ./{out_dir}/ to your frontend repo root")


if __name__ == "__main__":
    generate_all()