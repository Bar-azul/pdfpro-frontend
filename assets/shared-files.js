/* Reads files that were shared to the installed app (stored by /sw.js).
   window.PDFProShared.load() -> Promise<File[]> (empty when nothing fresh is stored). */
(function () {
  var CACHE = 'pdfpro-share-v1', MAX_AGE = 60 * 60 * 1000;
  function load() {
    if (!('caches' in window)) return Promise.resolve([]);
    return caches.open(CACHE).then(function (cache) {
      return cache.match('/__shared/meta').then(function (r) { return r ? r.json() : null; }).then(function (meta) {
        if (!meta || !meta.files || !meta.files.length) return [];
        if (Date.now() - meta.at > MAX_AGE) { caches.delete(CACHE); return []; }
        return Promise.all(meta.files.map(function (m) {
          return cache.match(m.key).then(function (r) { return r ? r.blob() : null; }).then(function (b) {
            return b ? new File([b], m.name, { type: m.type || b.type }) : null;
          });
        })).then(function (list) { return list.filter(Boolean); });
      });
    }).catch(function () { return []; });
  }
  window.PDFProShared = { load: load };
})();
