/* One Long Impersonation -- Chapter 06: The Other Side -- Engine */
/* Minimal JS: renders improvement metrics and correct-decision list from inline data */

(function () {
  'use strict';

  var data = window.OTHER_SIDE_DATA;
  if (!data) return;

  /* ------------------------------------------------
     IMPROVEMENT METRIC CARDS
     ------------------------------------------------ */
  var metricsEl = document.getElementById('improvement-metrics');
  if (metricsEl && data.improvement) {
    var html = '';
    data.improvement.forEach(function (m) {
      html += '<div class="metric-card">'
        + '<div class="metric-card__label">' + m.label + '</div>'
        + '<div class="metric-card__before">' + m.before_label + ': ' + m.before + '</div>'
        + '<div class="metric-card__arrow">&darr;</div>'
        + '<div class="metric-card__after">' + m.after + '</div>'
        + '<div class="metric-card__note">' + m.after_label + '</div>'
        + '</div>';
    });
    metricsEl.innerHTML = html;
  }

  /* ------------------------------------------------
     CORRECT DECISIONS LIST
     ------------------------------------------------ */
  var listEl = document.getElementById('correct-decisions-list');
  if (listEl && data.correct_decisions) {
    var listHtml = '';
    data.correct_decisions.forEach(function (d) {
      listHtml += '<li>'
        + '<span class="correct-list__check">&check;</span>'
        + '<span class="correct-list__artist">' + d.artist + '</span>'
        + '<span class="correct-list__detail">' + d.detail + '</span>'
        + '</li>';
    });
    listEl.innerHTML = listHtml;
  }

})();
