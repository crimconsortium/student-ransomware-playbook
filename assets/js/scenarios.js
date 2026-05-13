/* Student Ransomware Playbook — Choose-Your-Response engine.
 * Runs entirely in the browser. No analytics, no network calls.
 * Persists per-scenario outcomes under localStorage key "srp:scn:<id>" and
 * a roll-up set under "srp:scn:done". MIT-licensed.
 */
(function () {
  'use strict';

  var dataEl = document.getElementById('scn-data');
  if (!dataEl) return; // not on the scenarios page

  var SCENARIOS;
  try { SCENARIOS = JSON.parse(dataEl.textContent); }
  catch (e) { console.error('Bad scenarios JSON', e); return; }

  var DONE_KEY = 'srp:scn:done';
  var BEST_KEY = 'srp:scn:best'; // best (lowest = strongest) cumulative score per scenario

  /* ----------------------------- storage helpers ----------------------------- */
  function getDoneSet() {
    try { return new Set(JSON.parse(localStorage.getItem(DONE_KEY) || '[]')); }
    catch (e) { return new Set(); }
  }
  function setDoneSet(set) {
    localStorage.setItem(DONE_KEY, JSON.stringify(Array.from(set)));
  }
  function getBestMap() {
    try { return JSON.parse(localStorage.getItem(BEST_KEY) || '{}'); }
    catch (e) { return {}; }
  }
  function setBestMap(m) {
    localStorage.setItem(BEST_KEY, JSON.stringify(m));
  }

  /* ----------------------------- DOM refs ----------------------------- */
  var runner   = document.querySelector('.scn-runner');
  var titleEl  = runner && runner.querySelector('[data-role="scn-title"]');
  var sitEl    = runner && runner.querySelector('[data-role="scn-situation"]');
  var qEl      = runner && runner.querySelector('[data-role="scn-question"]');
  var choicesEl= runner && runner.querySelector('[data-role="scn-choices"]');
  var outcomeEl= runner && runner.querySelector('[data-role="scn-outcome"]');
  var counter  = document.querySelector('[data-role="scn-counter"]');
  var certBtn  = document.querySelector('[data-action="scn-certificate"]');
  var resetBtn = document.querySelector('[data-action="scn-reset"]');
  var closeBtn = runner && runner.querySelector('[data-action="scn-close"]');

  /* ----------------------------- progress display ----------------------------- */
  function refreshProgress() {
    var done = getDoneSet();
    var total = SCENARIOS.length;
    if (counter) counter.textContent = done.size + ' of ' + total + ' complete';
    if (certBtn) {
      var unlocked = done.size >= total;
      certBtn.disabled = !unlocked;
      certBtn.setAttribute('aria-disabled', String(!unlocked));
      certBtn.classList.toggle('btn-secondary', !unlocked);
      if (unlocked) {
        certBtn.textContent = '🎓 Download certificate';
        certBtn.title = '';
      } else {
        certBtn.textContent = '🔒 Certificate locked — finish ' + (total - done.size) + ' more';
        certBtn.title = 'Complete all ' + total + ' scenarios to unlock your certificate.';
      }
    }
    // tile status badges
    SCENARIOS.forEach(function (s) {
      var b = document.querySelector('[data-scn-status="' + s.id + '"]');
      if (!b) return;
      if (done.has(s.id)) {
        b.textContent = '✓ Done';
        b.className = 'scn-status done';
      } else {
        b.textContent = '';
        b.className = 'scn-status';
      }
    });
  }

  /* ----------------------------- scenario runner ----------------------------- */
  var current = null;        // scenario object
  var cumScore = 0;          // sum of scores along the current path
  var pathLabels = [];       // for breadcrumb

  function openScenario(id) {
    var s = SCENARIOS.find(function (x) { return x.id === id; });
    if (!s) return;
    current = s;
    cumScore = 0;
    pathLabels = [];
    runner.hidden = false;
    titleEl.textContent = s.title;
    sitEl.innerHTML = '<p><strong>Situation.</strong> ' + escapeHtml(s.situation) + '</p>';
    outcomeEl.hidden = true; outcomeEl.innerHTML = '';
    renderNode(s.start);
    // bring into view
    runner.scrollIntoView({behavior: 'smooth', block: 'start'});
  }

  function closeScenario() {
    if (!runner) return;
    runner.hidden = true;
    current = null;
    // scroll back to the grid
    var grid = document.querySelector('.scn-grid');
    if (grid) grid.scrollIntoView({behavior: 'smooth', block: 'start'});
  }

  function renderNode(nodeId) {
    if (!current) return;
    var node = current.nodes[nodeId];
    if (!node) return;
    if (node.type === 'outcome') return renderOutcome(node);
    // decision
    outcomeEl.hidden = true; outcomeEl.innerHTML = '';
    qEl.innerHTML = '<strong>' + escapeHtml(node.q) + '</strong>' +
      (pathLabels.length ? '<br><span class="scn-crumbs">' + escapeHtml(pathLabels.join(' → ')) + '</span>' : '');
    choicesEl.innerHTML = '';
    (node.choices || []).forEach(function (c) {
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'scn-choice';
      btn.textContent = c.label;
      btn.addEventListener('click', function () {
        cumScore += (c.score || 0);
        pathLabels.push(c.label);
        renderNode(c.next);
      });
      choicesEl.appendChild(btn);
    });
  }

  function renderOutcome(node) {
    qEl.innerHTML = '';
    choicesEl.innerHTML = '';
    var tag = node.tag || 'ok';
    var score = (typeof node.score === 'number') ? node.score : cumScore;
    // record best (lowest = strongest)
    var best = getBestMap();
    if (best[current.id] === undefined || score < best[current.id]) {
      best[current.id] = score;
      setBestMap(best);
    }
    // mark scenario as attempted/done
    var done = getDoneSet();
    done.add(current.id);
    setDoneSet(done);
    refreshProgress();

    var linksHtml = (node.links && node.links.length)
      ? '<p class="scn-outcome-links">Related: ' + node.links.map(function (l) {
          return '<a href="' + escapeAttr(l[1]) + '">' + escapeHtml(l[0]) + '</a>';
        }).join(' &middot; ') + '</p>'
      : '';

    outcomeEl.innerHTML =
      '<div class="scn-outcome-card scn-tag-' + escapeAttr(tag) + '">' +
        '<h3>' + escapeHtml(node.title || 'Outcome') + '</h3>' +
        '<p>' + escapeHtml(node.body || '') + '</p>' +
        linksHtml +
        '<div class="scn-outcome-actions">' +
          '<button type="button" class="btn btn-secondary btn-sm" data-action="scn-retry">↺ Try this scenario again</button> ' +
          '<button type="button" class="btn btn-sm" data-action="scn-next">Next scenario →</button> ' +
          '<button type="button" class="btn btn-secondary btn-sm" data-action="scn-close-inline">Back to list</button>' +
        '</div>' +
      '</div>';
    outcomeEl.hidden = false;
  }

  function nextScenario() {
    if (!current) return;
    var idx = SCENARIOS.findIndex(function (s) { return s.id === current.id; });
    var next = SCENARIOS[idx + 1];
    if (next) {
      openScenario(next.id);
    } else {
      // finished the last one — go back to list and surface certificate if eligible
      closeScenario();
      var done = getDoneSet();
      if (done.size >= SCENARIOS.length && certBtn) {
        certBtn.focus({preventScroll: true});
      }
    }
  }

  /* ----------------------------- certificate ----------------------------- */
  function buildCertificateHtml() {
    var best = getBestMap();
    var totalBest = SCENARIOS.reduce(function (acc, s) {
      var v = best[s.id];
      return acc + (typeof v === 'number' ? v : 0);
    }, 0);
    // Lower is stronger. -2 per scenario = perfect. We translate to a star rating.
    var stars;
    if (totalBest <= -16) stars = '★★★★★';
    else if (totalBest <= -10) stars = '★★★★☆';
    else if (totalBest <= -4)  stars = '★★★☆☆';
    else if (totalBest <= 4)   stars = '★★☆☆☆';
    else                       stars = '★☆☆☆☆';

    var today = new Date();
    var dateStr = today.toLocaleDateString(undefined, {year:'numeric', month:'long', day:'numeric'});
    return [
      '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">',
      '<title>Cyber-Smart Student Certificate</title>',
      '<style>',
      'body{margin:0;padding:0;background:#fff;color:#0d0d0d;font-family:Georgia,"Times New Roman",serif;}',
      '.cert{box-sizing:border-box;width:100%;max-width:1000px;margin:2rem auto;padding:3rem 3rem;border:14px solid #f68212;position:relative;}',
      '.cert::after{content:"";position:absolute;inset:10px;border:2px solid #f68212;pointer-events:none;}',
      '.eyebrow{font-family:system-ui,sans-serif;text-transform:uppercase;letter-spacing:.2em;font-size:.85rem;color:#555;margin:0 0 .8rem;}',
      'h1{font-size:2.6rem;margin:0 0 1.4rem;line-height:1.1;}',
      'p{font-size:1.15rem;line-height:1.5;margin:.6rem 0;}',
      '.name{font-size:2rem;margin:1.4rem 0;border-bottom:2px dashed #888;padding-bottom:.4rem;display:inline-block;min-width:60%;}',
      '.stars{font-size:1.6rem;color:#f68212;letter-spacing:.3rem;margin:.5rem 0 1.2rem;}',
      '.meta{display:flex;justify-content:space-between;gap:2rem;margin-top:2.4rem;font-size:.95rem;color:#444;font-family:system-ui,sans-serif;}',
      '.meta strong{display:block;color:#0d0d0d;font-size:1.05rem;font-family:Georgia,serif;}',
      '.muted{color:#666;font-size:.85rem;font-family:system-ui,sans-serif;}',
      '@media print{body{background:#fff;}.cert{border-color:#f68212;margin:0;max-width:none;}}',
      '.actions{font-family:system-ui,sans-serif;text-align:center;margin:1rem 0 2rem;}',
      '.actions button{font-size:1rem;padding:.6rem 1.2rem;background:#f68212;color:#fff;border:0;border-radius:6px;cursor:pointer;}',
      '@media print{.actions{display:none;}}',
      '</style>',
      '</head><body>',
      '<div class="actions"><button onclick="window.print()">Print or save as PDF</button></div>',
      '<div class="cert">',
        '<p class="eyebrow">Student Ransomware Playbook · Choose-Your-Response</p>',
        '<h1>Cyber-Smart Student</h1>',
        '<p>This certifies that</p>',
        '<div class="name" contenteditable="true" spellcheck="false">Your name</div>',
        '<p>has completed all ' + SCENARIOS.length + ' scenarios of the Student Ransomware Playbook ',
        'and demonstrated awareness of phishing, account safety, ransomware response, ',
        'and common cyber scams that target college and university students.</p>',
        '<div class="stars" aria-label="Path rating">' + stars + '</div>',
        '<div class="meta">',
          '<div><strong>Issued</strong>' + dateStr + '</div>',
          '<div><strong>Issued by</strong>Joshua Gerstenfeld &amp; Scott Jacques<br><span class="muted">with support from the CrimRxiv Consortium</span></div>',
          '<div><strong>Verify</strong><span class="muted">crimconsortium.github.io/student-ransomware-playbook</span></div>',
        '</div>',
      '</div>',
      '</body></html>'
    ].join('');
  }

  function downloadCertificate() {
    var win = window.open('', '_blank');
    if (!win) {
      alert('Pop-up blocked. Please allow pop-ups for this site to view your certificate.');
      return;
    }
    win.document.open();
    win.document.write(buildCertificateHtml());
    win.document.close();
    win.focus();
  }

  /* ----------------------------- event wiring ----------------------------- */
  document.addEventListener('click', function (e) {
    var tile = e.target.closest('.scn-tile');
    if (tile && tile.dataset.scnId) {
      e.preventDefault();
      openScenario(tile.dataset.scnId);
      return;
    }
    var action = e.target.closest('[data-action]');
    if (!action) return;
    var a = action.dataset.action;
    if (a === 'scn-reset') {
      if (confirm('Reset progress on all scenarios on this device?')) {
        localStorage.removeItem(DONE_KEY);
        localStorage.removeItem(BEST_KEY);
        refreshProgress();
        closeScenario();
      }
    } else if (a === 'scn-certificate') {
      // Hard guard: never generate a certificate unless every scenario is done.
      var doneNow = getDoneSet();
      if (doneNow.size < SCENARIOS.length) {
        alert('Finish all ' + SCENARIOS.length + ' scenarios to unlock your certificate. '
          + 'You have ' + doneNow.size + ' of ' + SCENARIOS.length + ' complete.');
        return;
      }
      downloadCertificate();
    } else if (a === 'scn-close' || a === 'scn-close-inline') {
      closeScenario();
    } else if (a === 'scn-retry') {
      if (current) openScenario(current.id);
    } else if (a === 'scn-next') {
      nextScenario();
    }
  });

  /* ----------------------------- utility ----------------------------- */
  function escapeHtml(s) {
    return String(s == null ? '' : s)
      .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
      .replace(/"/g,'&quot;').replace(/'/g,'&#39;');
  }
  function escapeAttr(s) {
    return escapeHtml(s);
  }

  /* ----------------------------- init ----------------------------- */
  refreshProgress();
})();
