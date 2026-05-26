// One Long Impersonation -- Shared Pyramid Mark
// Renders the I.M. Pei Rock Hall building as a small decorative SVG.
// Usage: include this script, add <div class="pyramid-mark"></div> anywhere.
// Options: set data-size="small" on the div for a compact version.

(function() {
  'use strict';

  var els = document.querySelectorAll('.pyramid-mark');
  if (!els.length) return;

  els.forEach(function(el) { renderPyramid(el); });

  function renderPyramid(el) {

  var small = el.getAttribute('data-size') === 'small';
  var W = small ? 120 : 460;
  var H = small ? 80 : 320;
  var accent = '#d4a017', ink = '#efe8d6';
  var apex = { x: W * 0.50, y: small ? 8 : 30 };
  var baseL = { x: W * 0.03, y: H - (small ? 16 : 60) };
  var baseR = { x: W * 0.97, y: H - (small ? 16 : 60) };
  var bands = small ? 3 : 6;

  function lerp(a, b, t) { return { x: a.x + (b.x - a.x) * t, y: a.y + (b.y - a.y) * t }; }

  var bandLines = [];
  for (var i = 1; i <= bands; i++) {
    bandLines.push({ a: lerp(apex, baseL, i / bands), b: lerp(apex, baseR, i / bands) });
  }

  // Trusses
  var trussPaths = '';
  if (!small) {
    for (var i = 1; i <= bands; i++) {
      var top = i === 1 ? { a: apex, b: apex } : { a: bandLines[i - 2].a, b: bandLines[i - 2].b };
      var bottom = bandLines[i - 1];
      var segs = i + 1, segsT = i;
      var ptsTop = [], ptsBot = [];
      for (var k = 0; k <= segsT; k++) {
        var tt = segsT === 0 ? 0 : k / segsT;
        ptsTop.push({ x: top.a.x + (top.b.x - top.a.x) * tt, y: top.a.y + (top.b.y - top.a.y) * tt });
      }
      for (var k = 0; k <= segs; k++) {
        var tt = k / segs;
        ptsBot.push({ x: bottom.a.x + (bottom.b.x - bottom.a.x) * tt, y: bottom.a.y + (bottom.b.y - bottom.a.y) * tt });
      }
      for (var k = 0; k < ptsBot.length; k++) {
        var bp = ptsBot[k];
        var leftIdx = Math.max(0, Math.floor(k * segsT / segs));
        var rightIdx = Math.min(segsT, leftIdx + 1);
        if (ptsTop[leftIdx]) trussPaths += '<line x1="'+bp.x+'" y1="'+bp.y+'" x2="'+ptsTop[leftIdx].x+'" y2="'+ptsTop[leftIdx].y+'"/>';
        if (ptsTop[rightIdx] && rightIdx !== leftIdx) trussPaths += '<line x1="'+bp.x+'" y1="'+bp.y+'" x2="'+ptsTop[rightIdx].x+'" y2="'+ptsTop[rightIdx].y+'"/>';
      }
    }
  }

  // Tower (full size only)
  var towerSvg = '';
  if (!small) {
    var tW = 56, tH = 170, tX = W * 0.72, tY = H - 60 - tH;
    var tLines = '';
    for (var i = 1; i <= 12; i++) tLines += '<line x1="'+tX+'" x2="'+(tX+tW)+'" y1="'+(tY+i*tH/13)+'" y2="'+(tY+i*tH/13)+'" stroke="'+ink+'" stroke-opacity="0.18" stroke-width="0.5"/>';
    for (var i = 1; i <= 3; i++) tLines += '<line x1="'+(tX+i*tW/4)+'" x2="'+(tX+i*tW/4)+'" y1="'+tY+'" y2="'+(tY+tH)+'" stroke="'+ink+'" stroke-opacity="0.18" stroke-width="0.5"/>';
    towerSvg = '<g opacity="0.85"><rect x="'+tX+'" y="'+tY+'" width="'+tW+'" height="'+tH+'" fill="none" stroke="'+ink+'" stroke-opacity="0.55" stroke-width="0.8"/>'+tLines+'</g>';
  }

  // Band lines
  var bandPaths = '';
  for (var i = 0; i < bandLines.length; i++) {
    var b = bandLines[i];
    bandPaths += '<line x1="'+b.a.x+'" y1="'+b.a.y+'" x2="'+b.b.x+'" y2="'+b.b.y+'"/>';
  }

  var groundY = small ? H - 14 : H - 58;
  var uid = 'pyr' + Math.random().toString(36).substr(2, 6);

  var svg = '<svg viewBox="0 0 '+W+' '+H+'" width="100%" style="display:block;max-width:'+W+'px" role="img" aria-label="I.M. Pei Rock and Roll Hall of Fame building">' +
    '<defs>' +
      '<linearGradient id="'+uid+'g" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="'+accent+'" stop-opacity="0.22"/><stop offset="55%" stop-color="'+accent+'" stop-opacity="0.10"/><stop offset="100%" stop-color="'+accent+'" stop-opacity="0.04"/></linearGradient>' +
      '<filter id="'+uid+'s" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="'+(small?1:3)+'"/></filter>' +
    '</defs>' +
    '<line x1="0" y1="'+groundY+'" x2="'+W+'" y2="'+groundY+'" stroke="'+ink+'" stroke-opacity="0.35" stroke-width="0.5"/>' +
    '<ellipse cx="'+(W/2)+'" cy="'+groundY+'" rx="'+(W*0.46)+'" ry="'+(small?3:10)+'" fill="'+accent+'" fill-opacity="0.18" filter="url(#'+uid+'s)"/>' +
    towerSvg +
    '<polygon points="'+apex.x+','+apex.y+' '+baseL.x+','+baseL.y+' '+baseR.x+','+baseR.y+'" fill="url(#'+uid+'g)"/>' +
    (trussPaths ? '<g stroke="'+accent+'" stroke-opacity="0.55" stroke-width="0.7">'+trussPaths+'</g>' : '') +
    '<g stroke="'+accent+'" stroke-opacity="0.85" stroke-width="'+(small?0.6:0.9)+'">'+bandPaths+'</g>' +
    '<polygon points="'+apex.x+','+apex.y+' '+baseL.x+','+baseL.y+' '+baseR.x+','+baseR.y+'" fill="none" stroke="'+accent+'" stroke-width="'+(small?1:1.6)+'"/>' +
    '<circle cx="'+apex.x+'" cy="'+apex.y+'" r="'+(small?1.5:2.4)+'" fill="'+accent+'"/>' +
  '</svg>';

  el.innerHTML = svg;
  }
})();
