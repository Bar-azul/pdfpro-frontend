/* PDFPro shared script.
   The backend runs on a paid Render instance that stays awake, so there is no
   server-status badge or warm-up ping any more; this exposes the API base URL and
   registers the service worker that makes the site installable (share target only,
   it caches nothing). */
(function () {
  window.PDFPro = { API: 'https://pdfproweb.onrender.com' };

  if ('serviceWorker' in navigator) {
    window.addEventListener('load', function () { navigator.serviceWorker.register('/sw.js').catch(function () {}); });
  }
  function track(name, p) { if (window.gtag) gtag('event', name, p || {}); }
  window.addEventListener('appinstalled', function () { track('app_installed'); });
  try {
    var standalone = window.matchMedia('(display-mode: standalone)').matches || navigator.standalone;
    if (standalone && !sessionStorage.getItem('pdfpro_app_open')) {
      sessionStorage.setItem('pdfpro_app_open', '1');
      track('app_open');
    }
  } catch (e) {}
})();
