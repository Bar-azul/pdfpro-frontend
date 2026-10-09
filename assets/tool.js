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
        n.textContent = data.saved_percentage > 0
          ? t.saved.replace('{p}', data.saved_percentage)
          : t.saved_none;
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
      if (j && j.code && t.err && t.err[j.code]) return t.err[j.code];
      if (Array.isArray(d)) d = d.map(function (x) { return x.msg; }).join(', ');
      return d || (t.generic_error + ' (' + resp.status + ')');
    }).catch(function () { return t.generic_error + ' (' + resp.status + ')'; });
  }

  function validateOptions() {
    var hooks = window.TOOL_HOOKS || {};
    if (hooks.validate) { var h = hooks.validate(); if (h) return h; }
    var fields = document.querySelectorAll('#tool-options input:not([disabled])');
    for (var i = 0; i < fields.length; i++) {
      var el = fields[i];
      if (el.dataset.required && !el.value.trim()) { el.focus(); return el.dataset.required; }
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
    setProgress(0, t.p_upload.replace('{p}', 0));

    // If the server is still waking up, tell the user instead of looking stuck.
    var slowTimer = setTimeout(function () { setStatus(t.waking, 'busy'); }, 6000);

    var fd = new FormData();
    files.forEach(function (f) { fd.append(cfg.field, f); });
    var query = new URLSearchParams();
    document.querySelectorAll('#tool-options [name]').forEach(function (el) {
      if (el.value === '' || el.disabled) return;
      // one select can fill several API fields, e.g. position "0.6|0.85" -> x, y
      var names = el.dataset.fields ? el.dataset.fields.split(',') : [el.name];
      var values = el.dataset.fields ? el.value.split('|') : [el.value];
      names.forEach(function (n, k) {
        if (el.dataset.query) query.append(n, values[k]); else fd.append(n, values[k]);
      });
    });
    var qs = query.toString();
    if (window.TOOL_HOOKS && window.TOOL_HOOKS.append) window.TOOL_HOOKS.append(fd);

    if (window.gtag) gtag('event', 'tool_run', { tool: cfg.slug });

    // Real progress: upload bytes from the browser, then the server's own count
    // (pages read, images compressed, files merged...) polled by job id.
    var job = newJobId();
    var url = API + cfg.endpoint + '?' + (qs ? qs + '&' : '') + 'job_id=' + job;
    var xhr = new XMLHttpRequest();
    var poller = null, finished = false;
    xhr.open('POST', url);
    xhr.timeout = (cfg.timeoutSec || 180) * 1000;
    xhr.responseType = 'text';

    xhr.upload.onprogress = function (e) {
      if (!e.lengthComputable) return;
      var p = Math.round(100 * e.loaded / e.total);
      clearTimeout(slowTimer);
      setProgress(p, t.p_upload.replace('{p}', p));
    };
    xhr.upload.onload = function () {
      setProgress(null, t.p_processing);
      pollProgress(job);
      poller = setInterval(function () { pollProgress(job); }, 700);
    };

    function done(err, data) {
      if (finished) return;
      finished = true;
      clearInterval(poller); clearTimeout(slowTimer);
      if (err) { setStatus(err, 'error'); hideProgress(); busy = false; render(); return; }
      setProgress(100, t.p_finishing);
      setTimeout(function () {
        hideProgress(); setStatus('');
        busy = false; render();
        try { showResult(data); } catch (e) { setStatus(e.message, 'error'); }
      }, 300);
    }
    function respObj() {
      return { status: xhr.status, json: function () {
        return new Promise(function (res, rej) { try { res(JSON.parse(xhr.responseText)); } catch (e) { rej(e); } });
      } };
    }
    xhr.onload = function () {
      if (xhr.status >= 200 && xhr.status < 300) {
        var data; try { data = JSON.parse(xhr.responseText); } catch (e) { return done(t.generic_error); }
        done(null, data);
      } else {
        errorFrom(respObj()).then(function (m) { done(m); });
      }
    };
    xhr.onerror = function () { done(t.network); };
    xhr.ontimeout = function () { done(t.timeout); };
    xhr.send(fd);
  });

  function newJobId() {
    if (window.crypto && crypto.randomUUID) return crypto.randomUUID().replace(/-/g, '');
    return Date.now().toString(36) + Math.random().toString(36).slice(2, 12);
  }
  function setProgress(percent, label) {
    bar.classList.add('show');
    var fill = bar.firstElementChild;
    if (percent === null) {
      bar.classList.add('indeterminate'); fill.style.width = '';
      bar.removeAttribute('aria-valuenow');
    } else {
      bar.classList.remove('indeterminate'); fill.style.width = percent + '%';
      bar.setAttribute('aria-valuenow', percent);
    }
    if (label) setStatus(label, 'busy');
  }
  function hideProgress() {
    bar.classList.remove('show', 'indeterminate');
    bar.firstElementChild.style.width = '0';
  }
  function pollProgress(job) {
    fetch(API + '/api/progress/' + job).then(function (r) { return r.ok ? r.json() : null; })
      .then(function (p) {
        if (!p || !busy) return;
        var key = 'p_' + p.stage;
        var label = t[key] || t.p_processing;
        if (p.total > 0) {
          var n = Math.min(p.total, Math.floor(p.done) + 1);
          label = label.replace('{n}', n).replace('{total}', p.total);
          setProgress(Math.max(2, Math.min(99, p.percent)), label);
        } else {
          setProgress(null, label.replace('{n}', '').replace('{total}', ''));
        }
      }).catch(function () { /* polling is best-effort */ });
  }

  resetBtn.addEventListener('click', function () {
    files = []; result.classList.remove('show'); resetBtn.hidden = true; setStatus(''); render();
    document.querySelectorAll('#tool-options input[type=password]').forEach(function (el) { el.value = ''; });
    zone.focus();
  });

  render();
})();
