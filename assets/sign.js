/* Signature pad for the Sign PDF page.
   Draw mode: strokes are kept as point lists (CSS px), redrawn on resize, and exported
   as a tightly-cropped transparent PNG at 3x for a crisp result in the PDF.
   Type mode: the name input is enabled and sent as signature_text. */
(function () {
  var box = document.getElementById('sig');
  if (!box) return;
  var canvas = document.getElementById('sig-canvas');
  var ctx = canvas.getContext('2d');
  var input = box.querySelector('.sig-type input');
  var PEN = '#0b1f66', WIDTH = 2.6;
  var strokes = [], current = null;

  function setMode(mode) {
    box.dataset.mode = mode;
    box.querySelector('.sig-draw').hidden = mode !== 'draw';
    box.querySelector('.sig-type').hidden = mode !== 'type';
    input.disabled = mode !== 'type';
    box.querySelectorAll('.sig-tabs button').forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.dataset.mode === mode));
    });
    if (mode === 'type') input.focus(); else resize();
  }
  box.querySelectorAll('.sig-tabs button').forEach(function (b) {
    b.addEventListener('click', function () { setMode(b.dataset.mode); });
  });

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
      for (var i = 1; i < pts.length - 1; i++) {   // smooth: curve through midpoints
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
    current = [pos(e)]; strokes.push(current); redraw();
    var st = document.getElementById('tool-status');
    if (st && st.classList.contains('error')) { st.textContent = ''; st.className = 'tool-status'; }
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
  document.getElementById('sig-clear').addEventListener('click', function () { strokes = []; redraw(); });

  function toBlob() {
    var minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    strokes.forEach(function (pts) { pts.forEach(function (p) {
      minX = Math.min(minX, p[0]); minY = Math.min(minY, p[1]);
      maxX = Math.max(maxX, p[0]); maxY = Math.max(maxY, p[1]);
    }); });
    var pad = WIDTH * 4, scale = 3;
    minX -= pad; minY -= pad; maxX += pad; maxY += pad;
    var out = document.createElement('canvas');
    out.width = Math.ceil((maxX - minX) * scale); out.height = Math.ceil((maxY - minY) * scale);
    paint(out.getContext('2d'), strokes, scale, minX, minY, 1.8);
    var bin = atob(out.toDataURL('image/png').split(',')[1]);
    var bytes = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
    return new Blob([bytes], { type: 'image/png' });
  }

  window.TOOL_HOOKS = {
    validate: function () {
      if (box.dataset.mode === 'draw' && !strokes.length) return box.dataset.needDraw;
      if (box.dataset.mode === 'type' && !input.value.trim()) { input.focus(); return box.dataset.needText; }
      return '';
    },
    append: function (fd) {
      if (box.dataset.mode === 'draw') fd.append('signature_image', toBlob(), 'signature.png');
    }
  };
  resize();
})();
