// One Long Impersonation -- Next Chapter Navigation
// Renders a "next chapter" handoff block before the footer.
// Usage: add <div id="next-chapter" data-current="00"></div> before </footer>
// The data-current attribute should match the chapter number (00-07).

(function() {
  'use strict';

  var el = document.getElementById('next-chapter');
  if (!el) return;

  var current = el.getAttribute('data-current');

  fetch('../../chapters.json')
    .then(function(r) { return r.json(); })
    .then(function(data) {
      if (!data.chapters) return;

      var chapters = data.chapters;
      var currentIdx = -1;
      for (var i = 0; i < chapters.length; i++) {
        if (chapters[i].number === current) {
          currentIdx = i;
          break;
        }
      }

      if (currentIdx === -1 || currentIdx >= chapters.length - 1) return;

      var next = chapters[currentIdx + 1];
      if (next.status !== 'live') return;

      el.innerHTML =
        '<div style="border-top:1px solid rgba(212,160,23,0.2); padding:64px 0 0; margin-top:80px; text-align:center">' +
          '<span style="font-family:var(--mono);font-size:10px;letter-spacing:0.2em;text-transform:uppercase;color:var(--mute);display:block;margin-bottom:16px">Next Chapter</span>' +
          '<a href="../../chapters/' + next.url.split('/chapters/')[1] + '" style="text-decoration:none;display:block">' +
            '<span style="font-family:var(--mono);font-size:11px;letter-spacing:0.15em;color:var(--gold);text-transform:uppercase;display:block;margin-bottom:8px">Chapter ' + next.number + '</span>' +
            '<span style="font-family:var(--serif);font-size:clamp(28px,4vw,42px);font-weight:500;color:var(--cream);display:block;margin-bottom:12px;line-height:1.1">' + next.title + '</span>' +
            '<span style="font-family:var(--sans);font-size:14px;color:var(--cream-2);display:block;max-width:480px;margin:0 auto;line-height:1.5">' + next.description + '</span>' +
            '<span style="display:inline-block;margin-top:24px;font-family:var(--mono);font-size:11px;letter-spacing:0.15em;color:var(--gold);border:1px solid var(--gold);padding:10px 28px;text-transform:uppercase;transition:background 0.15s">Continue &rarr;</span>' +
          '</a>' +
        '</div>';
    });
})();
