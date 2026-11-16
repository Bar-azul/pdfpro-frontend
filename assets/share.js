/* Share page: lists the shared file(s) and the tools that accept them.
   Page provides window.SHARE = {tools:[{slug,name,url,accept,multi}], t:{...}} (tools in priority order). */
(function () {
  var cfg = window.SHARE;
  if (!cfg || !window.PDFProShared) return;
  var t = cfg.t;
  var $ = function (id) { return document.getElementById(id); };

  function ext(f) { var m = /\.([a-z0-9]+)$/i.exec(f.name); return m ? '.' + m[1].toLowerCase() : ''; }
  function accepts(tool, f) {
    return tool.accept.split(',').some(function (a) {
      a = a.trim().toLowerCase();
      if (a.charAt(0) === '.') return ext(f) === a;
      if (/\/\*$/.test(a)) return (f.type || '').toLowerCase().indexOf(a.slice(0, -1)) === 0;
      return (f.type || '').toLowerCase() === a;
    });
  }
  function fmtSize(b) { return b < 1048576 ? Math.max(1, Math.round(b / 1024)) + ' KB' : (b / 1048576).toFixed(1) + ' MB'; }
  function track(name, p) { if (window.gtag) gtag('event', name, p || {}); }

  window.PDFProShared.load().then(function (files) {
    var status = $('share-status'), list = $('share-files'), grid = $('share-tools');
    if (!files.length) { status.textContent = t.empty; $('share-all').hidden = false; return; }

    list.innerHTML = '';
    files.forEach(function (f) {
      var li = document.createElement('li');
      li.textContent = f.name + ' · ' + fmtSize(f.size);
      list.appendChild(li);
    });

    var fit = cfg.tools.filter(function (tool) { return files.every(function (f) { return accepts(tool, f); }); });
    if (files.length > 1) fit.sort(function (a, b) { return (b.multi ? 1 : 0) - (a.multi ? 1 : 0); });
    track('share_received', { file_type: ext(files[0]).slice(1) || 'unknown', files: files.length, matches: fit.length });

    if (!fit.length) { status.textContent = t.unsupported; $('share-all').hidden = false; return; }
    status.textContent = files.length > 1 ? t.pick_multi : t.pick;
    fit.forEach(function (tool) {
      var a = document.createElement('a');
      a.className = 'share-tool';
      a.href = tool.url + '?shared=1';
      a.textContent = tool.name;
      a.addEventListener('click', function () { track('share_tool', { tool: tool.slug }); });
      grid.appendChild(a);
    });
  });
})();
