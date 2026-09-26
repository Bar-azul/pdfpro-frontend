/* PDFPro shared script — server status + cold-start warm-up.
   The backend runs on Render's free tier and sleeps when idle, so the first
   request can take up to ~60s. We ping /api/health as soon as any page loads,
   so the server is usually awake by the time the visitor picks a file. */
(function () {
  var API = 'https://pdfproweb.onrender.com';
  var el = document.getElementById('api-status');
  var txt = document.getElementById('api-status-text');

  function setState(state) {
    if (!el || !txt) return;
    el.className = 'api-status ' + state;
    txt.textContent = el.getAttribute('data-' + state) || state;
  }

  function ping(timeoutMs) {
    var ctrl = new AbortController();
    var timer = setTimeout(function () { ctrl.abort(); }, timeoutMs);
    return fetch(API + '/api/health', { signal: ctrl.signal, cache: 'no-store' })
      .then(function (r) { clearTimeout(timer); return r.ok; })
      .catch(function () { clearTimeout(timer); return false; });
  }

  // Quick ping first; if it doesn't answer fast, the server is probably waking up.
  var wakingTimer = setTimeout(function () { setState('waking'); }, 2500);
  var ready = ping(75000).then(function (ok) {
    clearTimeout(wakingTimer);
    setState(ok ? 'online' : 'offline');
    return ok;
  });

  window.PDFPro = { API: API, apiReady: ready, ping: ping, setState: setState };
})();
