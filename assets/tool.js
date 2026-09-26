/* PDFPro tool runner — shared by every tool page.
   Page provides window.TOOL = {endpoint, field, multi, accept, result, maxMB, minFiles, t:{...strings}}
   API contract (Bar-azul/PdfPro):
     single file result  -> {filename, download_url, size_bytes, ...}
     split               -> {parts:[{filename, download_url}], total_parts}
     ocr (txt)           -> {text, avg_confidence, ...}; ocr (pdf/docx) -> {filename, download_url}
     errors              -> {detail: "..."} with 4xx/5xx, 429 when rate-limited */
(function () {
  var cfg = window.TOOL;
  if (!cfg) return;
  var t = cfg.t;
  var API = (window.PDFPro && window.PDFPro.API) || 'https://pdfproweb.onrender.com';
  var $ = function (id) { return document.getElementById(id); };

  var input = $('tool-input'), zone = $('tool-dropzone'), list = $('tool-files'),
      runBtn = $('tool-run'), resetBtn = $('tool-reset'), status = $('tool-status'),
      bar = $('tool-progress'), result = $('tool-result'), downloads = $('tool-downloads'),
      preview = $('tool-preview'), resultTitle = $('tool-result-title');

  var files = [];
  var busy = false;

  function fmtSize(b) {
    if (b < 1024 * 1024) return Math.max(1, Math.round(b / 1024)) + ' KB';
    return (b / 1024 / 1024).toFixed(1) + ' MB';
  }
  function extOk(f) {
    if (!cfg.accept) return true;
    var name = f.name.toLowerCase();
    return cfg.accept.split(',').some(function (a) {
      a = a.trim().toLowerCase();
      if (a === 'image/*') return /^image\//.test(f.type);
      return name.endsWith(a);
    });
  }
  function setStatus(msg, kind) {
    status.textContent = msg || '';
    status.className = 'tool-status' + (kind ? ' ' + kind : '');
  }

  function render() {
    list.innerHTML = '';
    files.forEach(function (f, i) {
      var li = document.createElement('li');
      var name = document.createElement('span'); name.className = 'fname'; name.textContent = f.name;
      var size = document.createElement('span'); size.className = 'fsize'; size.textContent = fmtSize(f.size);
      li.appendChild(name); li.appendChild(size);
      if (cfg.multi && i > 0) {
        var up = document.createElement('button'); up.type = 'button'; up.textContent = t.move_up;
        up.setAttribute('aria-label', t.move_up + ': ' + f.name);
        up.onclick = function () { var x = files[i - 1]; files[i - 1] = files[i]; files[i] = x; render(); };
        li.appendChild(up);
      }
      var rm = document.createElement('button'); rm.type = 'button'; rm.textContent = t.remove;
      rm.setAttribute('aria-label', t.remove + ': ' + f.name);
      rm.onclick = function () { files.splice(i, 1); render(); };
      li.appendChild(rm);
      list.appendChild(li);
    });
    var need = cfg.minFiles || 1;
    runBtn.disabled = busy || files.length < need;
    if (!busy && files.length > 0 && files.length < need) setStatus(t.need_more);
    else if (!busy && !status.classList.contains('error')) setStatus('');
  }

  function addFiles(fileList) {
    setStatus('');
    var incoming = Array.prototype.slice.call(fileList);
    for (var i = 0; i < incoming.length; i++) {
      var f = incoming[i];
      if (!extOk(f)) { setStatus(t.bad_type.replace('{name}', f.name), 'error'); continue; }
      if (f.size > cfg.maxMB * 1024 * 1024) { setStatus(t.too_big.replace('{name}', f.name).replace('{max}', cfg.maxMB), 'error'); continue; }
      if (cfg.multi) files.push(f); else files = [f];
    }
    result.classList.remove('show');
    render();
  }

  input.addEventListener('change', function () { addFiles(input.files); input.value = ''; });
  ['dragenter', 'dragover'].forEach(function (ev) {
    zone.addEventListener(ev, function (e) { e.preventDefault(); zone.classList.add('drag'); });
  });
  ['dragleave', 'drop'].forEach(function (ev) {
    zone.addEventListener(ev, function (e) { e.preventDefault(); zone.classList.remove('drag'); });
  });
  zone.addEventListener('drop', function (e) { if (e.dataTransfer && e.dataTransfer.files) addFiles(e.dataTransfer.files); });

  function saveBlob(blob, filename) {
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob); a.download = filename;
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function () { URL.revokeObjectURL(a.href); }, 30000);
  }
  function downloadButton(url, filename, label) {
    var b = document.createElement('button');
    b.type = 'button'; b.className = 'cta'; b.textContent = label || (t.download + ' ' + filename);
    b.onclick = function () {
      b.disabled = true;
      fetch(API + url).then(function (r) {
        if (!r.ok) throw new Error(t.expired);
        return r.blob();
      }).then(function (blob) {
        saveBlob(blob, filename);
        if (window.gtag) gtag('event', 'file_download', { tool: cfg.slug });
      }).catch(function (e) { setStatus(e.message, 'error'); })
        .then(function () { b.disabled = false; });
    };
    return b;
  }

  function showResult(data) {
    downloads.innerHTML = ''; preview.hidden = true; preview.textContent = '';
    resultTitle.textContent = t.done;
    if (cfg.result === 'text' && typeof data.text === 'string') {
      var txt = data.text;
      var b = document.createElement('button'); b.type = 'button'; b.className = 'cta'; b.textContent = t.download_txt;
      b.onclick = function () { saveBlob(new Blob([txt], { type: 'text/plain;charset=utf-8' }), 'ocr_result.txt'); };
      downloads.appendChild(b);
      if (txt.trim()) { preview.hidden = false; preview.textContent = txt.slice(0, 1500) + (txt.length > 1500 ? '…' : ''); }
      else { resultTitle.textContent = t.no_text; }
    } else if (data.parts || data.files) {
      var items = data.parts || data.files;
      resultTitle.textContent = t.done_parts.replace('{n}', items.length);
      items.forEach(function (it) { downloads.appendChild(downloadButton(it.download_url, it.filename)); });
    } else if (data.download_url) {
      downloads.appendChild(downloadButton(data.download_url, data.filename || 'result'));
      if (data.saved_percentage !== undefined) {
        var n = document.createElement('p'); n.className = 'tool-note';
        n.textContent = t.saved.replace('{p}', data.saved_percentage);
        downloads.appendChild(n);
      }
    } else {
      throw new Error(t.generic_error);
    }
    var note = document.createElement('p'); note.className = 'tool-note'; note.textContent = t.deleted_note;
    downloads.appendChild(note);
    result.classList.add('show');
    resetBtn.hidden = false;
  }

  function errorFrom(resp) {
    if (cfg.errors && cfg.errors[resp.status]) return Promise.resolve(cfg.errors[resp.status]);
    if (resp.status === 429) return Promise.resolve(t.rate_limited);
    return resp.json().then(function (j) {
      var d = j && j.detail;
      if (Array.isArray(d)) d = d.map(function (x) { return x.msg; }).join(', ');
      return d || (t.generic_error + ' (' + resp.status + ')');
    }).catch(function () { return t.generic_error + ' (' + resp.status + ')'; });
  }

  function validateOptions() {
    var fields = document.querySelectorAll('#tool-options input');
    for (var i = 0; i < fields.length; i++) {
      var el = fields[i];
      if (el.dataset.required && !el.value) { el.focus(); return t.pw_required; }
      if (el.dataset.minlength && el.value.length < +el.dataset.minlength) { el.focus(); return t.pw_short.replace('{n}', el.dataset.minlength); }
      if (el.dataset.confirm && el.value !== $(el.dataset.confirm).value) { el.focus(); return t.pw_mismatch; }
    }
    return '';
  }

  runBtn.addEventListener('click', function () {
    if (busy || !files.length) return;
    var invalid = validateOptions();
    if (invalid) { setStatus(invalid, 'error'); return; }
    busy = true; render();
    result.classList.remove('show');
    bar.classList.add('show');
    setStatus(t.uploading, 'busy');

    // If the server is still waking up, tell the user instead of looking stuck.
    var slowTimer = setTimeout(function () { setStatus(t.waking, 'busy'); }, 6000);

    var fd = new FormData();
    files.forEach(function (f) { fd.append(cfg.field, f); });
    document.querySelectorAll('#tool-options [name]').forEach(function (el) {
      if (el.value !== '') fd.append(el.name, el.value);
    });

    if (window.gtag) gtag('event', 'tool_run', { tool: cfg.slug });
    var ctrl = new AbortController();
    var hardTimeout = setTimeout(function () { ctrl.abort(); }, 180000);

    fetch(API + cfg.endpoint, { method: 'POST', body: fd, signal: ctrl.signal })
      .then(function (resp) {
        if (!resp.ok) return errorFrom(resp).then(function (m) { throw new Error(m); });
        return resp.json();
      })
      .then(function (data) { setStatus(''); showResult(data); if (window.PDFPro) PDFPro.setState('online'); })
      .catch(function (e) {
        var msg = e.name === 'AbortError' ? t.timeout : (e.message === 'Failed to fetch' ? t.network : e.message);
        setStatus(msg, 'error');
      })
      .then(function () {
        clearTimeout(slowTimer); clearTimeout(hardTimeout);
        bar.classList.remove('show');
        busy = false; render();
      });
  });

  resetBtn.addEventListener('click', function () {
    files = []; result.classList.remove('show'); resetBtn.hidden = true; setStatus(''); render();
    document.querySelectorAll('#tool-options input[type=password]').forEach(function (el) { el.value = ''; });
    zone.focus();
  });

  render();
})();
