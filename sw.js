/* PDFPro service worker.
   Its only job is the Web Share Target: when a file is shared to the installed app
   (e.g. a PDF from WhatsApp), the OS POSTs it to /share/ or /he/share/. We keep the
   file(s) in a local cache and redirect to the share page, which offers the tools.
   Every other request goes straight to the network untouched — no page, script,
   ad or analytics request is cached or intercepted. */
var SHARE_CACHE = 'pdfpro-share-v1';
var EXT_BY_TYPE = {
  'application/pdf': 'pdf', 'image/jpeg': 'jpg', 'image/png': 'png', 'image/webp': 'webp',
  'audio/ogg': 'ogg', 'audio/opus': 'opus', 'audio/mpeg': 'mp3', 'audio/mp4': 'm4a',
  'audio/aac': 'aac', 'audio/amr': 'amr', 'audio/wav': 'wav', 'audio/x-wav': 'wav',
  'video/mp4': 'mp4',
  'application/msword': 'doc',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
  'application/vnd.ms-excel': 'xls',
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'xlsx',
  'application/vnd.ms-powerpoint': 'ppt',
  'application/vnd.openxmlformats-officedocument.presentationml.presentation': 'pptx'
};

self.addEventListener('install', function () { self.skipWaiting(); });
self.addEventListener('activate', function (e) { e.waitUntil(self.clients.claim()); });

self.addEventListener('fetch', function (e) {
  var req = e.request;
  if (req.method !== 'POST') return;
  var u = new URL(req.url);
  if (u.origin !== self.location.origin || !/^\/(he\/)?share\/?$/.test(u.pathname)) return;
  e.respondWith(receiveShare(req, u.pathname.replace(/\/?$/, '/')));
});

function fileName(f, i) {
  var name = (f.name || '').trim() || 'shared-file-' + (i + 1);
  if (!/\.[a-z0-9]{2,5}$/i.test(name)) {
    var ext = EXT_BY_TYPE[(f.type || '').split(';')[0]];
    if (ext) name += '.' + ext;
  }
  return name;
}

function receiveShare(req, page) {
  return req.formData().then(function (form) {
    var files = form.getAll('files').filter(function (f) { return f && typeof f !== 'string' && f.size; });
    return caches.delete(SHARE_CACHE).then(function () { return caches.open(SHARE_CACHE); }).then(function (cache) {
      var meta = [];
      return Promise.all(files.map(function (f, i) {
        var key = '/__shared/' + i;
        meta.push({ key: key, name: fileName(f, i), type: f.type || '', size: f.size });
        return cache.put(key, new Response(f, { headers: { 'Content-Type': f.type || 'application/octet-stream' } }));
      })).then(function () {
        return cache.put('/__shared/meta', new Response(JSON.stringify({ at: Date.now(), files: meta }),
          { headers: { 'Content-Type': 'application/json' } }));
      });
    });
  }).catch(function () { /* fall through to the page, which says nothing was received */ })
    .then(function () { return Response.redirect(page, 303); });
}
