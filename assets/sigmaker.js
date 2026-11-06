/* Signature maker: draw or type a signature and download it as a transparent PNG.
   Runs entirely in the browser; nothing is uploaded. */
(function () {
  var box = document.getElementById('sm');
  if (!box) return;
  var canvas = document.getElementById('sm-canvas');
  var ctx = canvas.getContext('2d');
  var input = document.getElementById('sm-name');
  var status = document.getElementById('sm-status');
  var styles = box.querySelectorAll('.sm-style');
  var colors = box.querySelectorAll('.sm-color');
  var WIDTH = 2.6, PEN = '#0b1f66';
  var strokes = [], current = null, style = 'SigA';
  var RTL = /[֐-׿؀-ۿ]/;

  function setMode(mode) {
    box.dataset.mode = mode;
    box.querySelector('.sig-draw').hidden = mode !== 'draw';
    box.querySelector('.sm-type').hidden = mode !== 'type';
    box.querySelectorAll('.sig-tabs button').forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.dataset.mode === mode));
    });
    status.textContent = '';
    if (mode === 'type') input.focus(); else resize();
  }
  box.querySelectorAll('.sig-tabs button').forEach(function (b) {
    b.addEventListener('click', function () { setMode(b.dataset.mode); });
  });

  colors.forEach(function (c) {
    c.addEventListener('click', function () {
      PEN = c.dataset.color;
      colors.forEach(function (x) { x.setAttribute('aria-pressed', String(x === c)); });
      box.style.setProperty('--ink', PEN);
      redraw();
    });
  });
  styles.forEach(function (s) {
    s.addEventListener('click', function () {
      style = s.dataset.font;
      styles.forEach(function (x) { x.setAttribute('aria-pressed', String(x === s)); });
    });
  });
  function updatePreviews() {
    var t = input.value.trim() || input.placeholder.replace(/^[^:]*:\s*/, '');
    styles.forEach(function (s) { s.querySelector('span').textContent = t; });
  }
  input.addEventListener('input', function () { updatePreviews(); status.textContent = ''; });

  function paint(c, list, scale, dx, dy, weight) {
    c.lineCap = 'round'; c.lineJoin = 'round'; c.strokeStyle = PEN; c.fillStyle = PEN;
    c.lineWidth = WIDTH * scale * (weight || 1);
    list.forEach(function (pts) {
      var P = function (p) { return [(p[0] - dx) * scale, (p[1] - dy) * scale]; };
      if (pts.length === 1) {
        var q = P(pts[0]); c.beginPath(); c.arc(q[0], q[1], c.lineWidth / 2, 0, Math.PI * 2); c.fill(); return;
      }
      c.beginPath();
      var a = P(pts[0]); c.moveTo(a[0], a[1]);
      for (var i = 1; i < pts.length - 1; i++) {
        var p = P(pts[i]), n = P(pts[i + 1]);
        c.quadraticCurveTo(p[0], p[1], (p[0] + n[0]) / 2, (p[1] + n[1]) / 2);
      }
      var z = P(pts[pts.length - 1]); c.lineTo(z[0], z[1]);
      c.stroke();
    });
  }
  function redraw() {
    var dpr = window.devicePixelRatio || 1;
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    paint(ctx, strokes, dpr, 0, 0);
    box.classList.toggle('has-ink', strokes.length > 0);
  }
  function resize() {
    var r = canvas.getBoundingClientRect(); if (!r.width) return;
    var dpr = window.devicePixelRatio || 1;
    canvas.width = Math.round(r.width * dpr); canvas.height = Math.round(r.height * dpr);
    redraw();
  }
  window.addEventListener('resize', resize);
  function pos(e) { var r = canvas.getBoundingClientRect(); return [e.clientX - r.left, e.clientY - r.top]; }
  canvas.addEventListener('pointerdown', function (e) {
    e.preventDefault(); canvas.setPointerCapture(e.pointerId);
    current = [pos(e)]; strokes.push(current); redraw(); status.textContent = '';
  });
  canvas.addEventListener('pointermove', function (e) {
    if (!current) return;
    var p = pos(e), last = current[current.length - 1];
    if (Math.abs(p[0] - last[0]) + Math.abs(p[1] - last[1]) < 1.5) return;
    current.push(p); redraw();
  });
  ['pointerup', 'pointercancel', 'lostpointercapture'].forEach(function (ev) {
    canvas.addEventListener(ev, function () { current = null; });
  });
  document.getElementById('sm-clear').addEventListener('click', function () { strokes = []; redraw(); });

  function drawnPng() {
    var minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    strokes.forEach(function (pts) { pts.forEach(function (p) {
      minX = Math.min(minX, p[0]); minY = Math.min(minY, p[1]);
      maxX = Math.max(maxX, p[0]); maxY = Math.max(maxY, p[1]);
    }); });
    var pad = WIDTH * 4, scale = 3;
    minX -= pad; minY -= pad; maxX += pad; maxY += pad;
    var out = document.createElement('canvas');
    out.width = Math.ceil((maxX - minX) * scale); out.height = Math.ceil((maxY - minY) * scale);
    paint(out.getContext('2d'), strokes, scale, minX, minY, 1.4);
    return Promise.resolve(out);
  }
  function typedPng(text) {
    var size = 150, font = size + 'px ' + style;
    return document.fonts.load(font, text).then(function () {
      var dir = RTL.test(text) ? 'rtl' : 'ltr';
      var m = document.createElement('canvas').getContext('2d');
      m.font = font; m.direction = dir; m.textAlign = 'left'; m.textBaseline = 'alphabetic';
      var t = m.measureText(text), pad = Math.round(size * 0.12);
      var left = t.actualBoundingBoxLeft || 0, right = t.actualBoundingBoxRight || t.width;
      var up = t.actualBoundingBoxAscent || size * 0.8, down = t.actualBoundingBoxDescent || size * 0.2;
      var out = document.createElement('canvas');
      out.width = Math.ceil(left + right + pad * 2); out.height = Math.ceil(up + down + pad * 2);
      var c = out.getContext('2d');
      c.font = font; c.fillStyle = PEN; c.direction = dir; c.textAlign = 'left'; c.textBaseline = 'alphabetic';
      c.fillText(text, pad + left, pad + up);
      return out;
    });
  }

  document.getElementById('sm-download').addEventListener('click', function () {
    var job;
    if (box.dataset.mode === 'draw') {
      if (!strokes.length) { status.textContent = box.dataset.needDraw; return; }
      job = drawnPng();
    } else {
      var text = input.value.trim();
      if (!text) { status.textContent = box.dataset.needText; input.focus(); return; }
      job = typedPng(text);
    }
    job.then(function (out) {
      var a = document.createElement('a');
      a.href = out.toDataURL('image/png');
      a.download = box.dataset.filename;
      document.body.appendChild(a); a.click(); a.remove();
      status.textContent = box.dataset.done;
      if (window.gtag) {
        gtag('event', 'tool_run', { tool: 'create-signature' });
        gtag('event', 'file_download', { tool: 'create-signature' });
      }
    });
  });

  updatePreviews();
  resize();
})();
