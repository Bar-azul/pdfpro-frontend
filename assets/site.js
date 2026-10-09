/* PDFPro shared script.
   The backend runs on a paid Render instance that stays awake, so there is no
   server-status badge or warm-up ping any more; this only exposes the API base URL. */
(function () {
  window.PDFPro = { API: 'https://pdfproweb.onrender.com' };
})();
