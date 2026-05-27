/*
 * Drills engine (formerly dorm-lab.js + scenarios.js, merged).
 *
 * One page (drills.html) for everything that used to live in the separate
 * "Scenarios" and "Dorm lab" pages. Drills come in two flavors:
 *   - Dorm-anchored drills have a non-empty .hotspot. The SVG room places
 *     a clickable dot on the matching item. The tile grid also lists them.
 *   - Off-screen drills have an empty .hotspot and only appear in the tile
 *     grid below the room.
 *
 * Behavior:
 *   - Branching decision runner with retry.
 *   - After-action review (AAR) checklist per drill, with persistent checks.
 *   - Overall readiness meter = (completed drills + checked habits) / totals.
 *   - Printable certificate once every drill is complete.
 *
 * Reads JSON from <script id="drills-data">. No-op if missing.
 *
 * CSS classes (.lab-*, .lab-tile, etc.) are unchanged from the old dorm-lab
 * page so the existing stylesheet keeps working. Only the storage keys and
 * a couple of data-attributes changed.
 *
 * LocalStorage keys:
 *   srp:drills:done      JSON array of completed drill IDs
 *   srp:drills:habits    JSON array of checked AAR-habit strings (deduped)
 *   srp:drills:best      JSON map of drill-id -> best (lowest) outcome score
 *
 * Old keys are migrated on first read so users don't lose progress:
 *   srp:lab:done / srp:lab:habits / srp:scn:done / srp:scn:best
 */
(function () {
  var dataEl = document.getElementById('drills-data');
  if (!dataEl) return;

  var DRILLS;
  try { DRILLS = JSON.parse(dataEl.textContent); }
  catch (e) { console.warn('drills data parse failed', e); return; }
  if (!Array.isArray(DRILLS) || !DRILLS.length) return;

  var DONE_KEY = 'srp:drills:done';
  var HABITS_KEY = 'srp:drills:habits';
  var BEST_KEY = 'srp:drills:best';

  function migrateOnce() {
    try {
      if (!localStorage.getItem(DONE_KEY)) {
        var done = new Set();
        ['srp:lab:done', 'srp:scn:done'].forEach(function (k) {
          try {
            var raw = localStorage.getItem(k);
            if (!raw) return;
            var arr = JSON.parse(raw);
            if (Array.isArray(arr)) arr.forEach(function (id) { done.add(id); });
          } catch (e) {}
        });
        if (done.size) localStorage.setItem(DONE_KEY, JSON.stringify(Array.from(done)));
      }
      if (!localStorage.getItem(HABITS_KEY)) {
        try {
          var raw = localStorage.getItem('srp:lab:habits');
          if (raw) localStorage.setItem(HABITS_KEY, raw);
        } catch (e) {}
      }
      if (!localStorage.getItem(BEST_KEY)) {
        try {
          var rawB = localStorage.getItem('srp:scn:best');
          if (rawB) localStorage.setItem(BEST_KEY, rawB);
        } catch (e) {}
      }
    } catch (e) {}
  }
  migrateOnce();

  var ALL_HABITS = (function () {
    var seen = Object.create(null);
    var out = [];
    DRILLS.forEach(function (m) {
      (m.aar || []).forEach(function (h) {
        if (!seen[h]) { seen[h] = 1; out.push(h); }
      });
    });
    return out;
  })();

  function readSet(key) {
    try {
      var raw = localStorage.getItem(key);
      if (!raw) return new Set();
      var arr = JSON.parse(raw);
      return new Set(Array.isArray(arr) ? arr : []);
    } catch (e) { return new Set(); }
  }
  function writeSet(key, set) {
    try { localStorage.setItem(key, JSON.stringify(Array.from(set))); }
    catch (e) {}
  }
  function readMap(key) {
    try {
      var raw = localStorage.getItem(key);
      if (!raw) return {};
      var obj = JSON.parse(raw);
      return obj && typeof obj === 'object' ? obj : {};
    } catch (e) { return {}; }
  }
  function writeMap(key, obj) {
    try { localStorage.setItem(key, JSON.stringify(obj)); }
    catch (e) {}
  }
  function getDone() { return readSet(DONE_KEY); }
  function getHabits() { return readSet(HABITS_KEY); }
  function getBest() { return readMap(BEST_KEY); }
  function markDone(id) { var s = getDone(); s.add(id); writeSet(DONE_KEY, s); }
  function recordBest(id, score) {
    if (typeof score !== 'number') return;
    var m = getBest();
    if (!(id in m) || score < m[id]) { m[id] = score; writeMap(BEST_KEY, m); }
  }
  function toggleHabit(habit, on) {
    var s = getHabits();
    if (on) s.add(habit); else s.delete(habit);
    writeSet(HABITS_KEY, s);
  }

  // ---- Readiness meter + cert button --------------------------------------
  function refreshMeter() {
    var done = getDone();
    var habits = getHabits();
    var totalUnits = DRILLS.length + ALL_HABITS.length;
    var doneUnits = done.size + habits.size;
    var pct = totalUnits ? Math.round((doneUnits / totalUnits) * 100) : 0;
    if (pct > 100) pct = 100;

    var pctEl = document.querySelector('[data-role="lab-readiness-pct"]');
    var fillEl = document.querySelector('[data-role="lab-readiness-fill"]');
    var outerEl = document.querySelector('[data-role="lab-readiness-bar-outer"]');
    var counterEl = document.querySelector('[data-role="lab-counter"]');
    var habitCounterEl = document.querySelector('[data-role="lab-habit-counter"]');
    if (pctEl) pctEl.textContent = pct + '%';
    if (fillEl) fillEl.style.width = pct + '%';
    if (outerEl) outerEl.setAttribute('aria-valuenow', String(pct));
    if (counterEl) counterEl.textContent = done.size + ' of ' + DRILLS.length + ' drills complete';
    if (habitCounterEl) habitCounterEl.textContent = habits.size + ' of ' + ALL_HABITS.length + ' habits checked';

    DRILLS.forEach(function (m) {
      var badge = document.querySelector('[data-lab-status="' + cssEscape(m.id) + '"]');
      if (!badge) return;
      if (done.has(m.id)) {
        badge.textContent = '\u2713 Done';
        badge.classList.add('is-done');
      } else {
        badge.textContent = '';
        badge.classList.remove('is-done');
      }
    });

    var certBtn = document.querySelector('[data-action="drills-certificate"]');
    if (certBtn) {
      var unlocked = done.size >= DRILLS.length;
      certBtn.disabled = !unlocked;
      certBtn.setAttribute('aria-disabled', String(!unlocked));
      certBtn.classList.toggle('btn-secondary', !unlocked);
      if (unlocked) {
        certBtn.textContent = '\ud83c\udf93 Download certificate';
        certBtn.title = '';
      } else {
        certBtn.textContent = '\ud83d\udd12 Certificate locked. Finish ' + (DRILLS.length - done.size) + ' more';
        certBtn.title = 'Complete all ' + DRILLS.length + ' drills to unlock your certificate.';
      }
    }
  }

  function cssEscape(s) { return String(s).replace(/"/g, '\\"'); }

  // ---- Runner -------------------------------------------------------------
  var runnerEl = document.querySelector('.lab-runner');
  var titleEl = document.querySelector('[data-role="lab-title"]');
  var setupEl = document.querySelector('[data-role="lab-setup"]');
  var qEl = document.querySelector('[data-role="lab-question"]');
  var choicesEl = document.querySelector('[data-role="lab-choices"]');
  var outcomeEl = document.querySelector('[data-role="lab-outcome"]');
  var aarEl = document.querySelector('[data-role="lab-aar"]');

  var current = null;

  function findByHotspot(key) {
    for (var i = 0; i < DRILLS.length; i++) if (DRILLS[i].hotspot === key) return DRILLS[i];
    return null;
  }
  function findById(id) {
    for (var i = 0; i < DRILLS.length; i++) if (DRILLS[i].id === id) return DRILLS[i];
    return null;
  }

  function openDrill(m) {
    if (!m || !runnerEl) return;
    current = m;
    runnerEl.hidden = false;
    titleEl.textContent = m.title;
    setupEl.textContent = m.setup;
    outcomeEl.hidden = true;
    outcomeEl.innerHTML = '';
    aarEl.hidden = true;
    aarEl.innerHTML = '';
    renderNode(m.start);
    var anchor = document.getElementById('lab');
    if (anchor && anchor.scrollIntoView) anchor.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function renderNode(nodeId) {
    if (!current) return;
    var node = current.nodes[nodeId];
    if (!node) return;
    if (node.type === 'decision') {
      qEl.style.display = '';
      qEl.textContent = node.q;
      choicesEl.style.display = '';
      choicesEl.innerHTML = '';
      node.choices.forEach(function (c) {
        var btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'lab-choice';
        btn.textContent = c.label;
        btn.addEventListener('click', function () {
          if (typeof c.score === 'number') recordBest(current.id, c.score);
          renderNode(c.next);
        });
        choicesEl.appendChild(btn);
      });
      outcomeEl.hidden = true;
      aarEl.hidden = true;
    } else if (node.type === 'outcome') {
      qEl.style.display = 'none';
      choicesEl.style.display = 'none';
      var tagClass = 'lab-tag-' + (node.tag || 'ok');
      var tagLabel = ({ good: 'STRONG', ok: 'OK', risky: 'RISKY', bad: 'AVOID' })[node.tag] || 'OK';
      if (typeof node.score === 'number') recordBest(current.id, node.score);
      var links = (node.links || []).map(function (pair) {
        return '<li><a href="' + escapeAttr(pair[1]) + '">' + escapeHtml(pair[0]) + '</a></li>';
      }).join('');
      outcomeEl.innerHTML =
        '<div class="lab-outcome-card ' + tagClass + '">' +
          '<span class="lab-tag-pill ' + tagClass + '">' + tagLabel + '</span>' +
          '<h3>' + escapeHtml(node.title || '') + '</h3>' +
          '<p>' + escapeHtml(node.body || '') + '</p>' +
          (links ? '<ul class="lab-outcome-links">' + links + '</ul>' : '') +
          '<div class="lab-outcome-actions">' +
            '<button type="button" class="btn btn-secondary btn-sm" data-action="drill-retry">\u21ba Try again</button>' +
            '<button type="button" class="btn btn-secondary btn-sm" data-action="drill-close">\u2190 Back to drills</button>' +
          '</div>' +
        '</div>';
      outcomeEl.hidden = false;
      markDone(current.id);
      renderAAR();
      refreshMeter();
    }
  }

  function renderAAR() {
    if (!current || !aarEl) return;
    var items = current.aar || [];
    if (!items.length) { aarEl.hidden = true; return; }
    var checked = getHabits();
    aarEl.innerHTML =
      '<h3>After-action review</h3>' +
      '<p class="muted">Check the habits you already do. Each new check raises your overall readiness.</p>' +
      '<ul class="lab-aar-list">' +
        items.map(function (h, i) {
          var on = checked.has(h);
          var id = 'aar-' + current.id + '-' + i;
          return '<li>' +
            '<input type="checkbox" id="' + id + '" data-aar-habit="' + escapeAttr(h) + '"' + (on ? ' checked' : '') + '>' +
            '<label for="' + id + '">' + escapeHtml(h) + '</label>' +
          '</li>';
        }).join('') +
      '</ul>';
    aarEl.hidden = false;
  }

  function escapeHtml(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c];
    });
  }
  function escapeAttr(s) { return escapeHtml(s); }

  // ---- Certificate --------------------------------------------------------
  function buildCertificateHtml() {
    var best = getBest();
    var totalBest = DRILLS.reduce(function (acc, s) {
      var v = best[s.id];
      return acc + (typeof v === 'number' ? v : 0);
    }, 0);
    // Lower (more negative) is stronger. -2 per drill = perfect.
    var perfect = -2 * DRILLS.length;
    var ratio = perfect ? totalBest / perfect : 0;
    var stars;
    if (ratio >= 0.9) stars = '\u2605\u2605\u2605\u2605\u2605';
    else if (ratio >= 0.7) stars = '\u2605\u2605\u2605\u2605\u2606';
    else if (ratio >= 0.5) stars = '\u2605\u2605\u2605\u2606\u2606';
    else if (ratio >= 0.2) stars = '\u2605\u2605\u2606\u2606\u2606';
    else stars = '\u2605\u2606\u2606\u2606\u2606';

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
        '<p class="eyebrow">Student Ransomware Playbook \u00b7 Drills</p>',
        '<h1>Cyber-Smart Student</h1>',
        '<p>This certifies that</p>',
        '<div class="name" contenteditable="true" spellcheck="false">Your name</div>',
        '<p>has completed all ' + DRILLS.length + ' drills of the Student Ransomware Playbook ',
        'and demonstrated awareness of phishing, account safety, ransomware response, ',
        'and common cyber scams that target college students.</p>',
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

  // ---- Event delegation ---------------------------------------------------
  document.addEventListener('click', function (e) {
    var hotEl = e.target.closest('[data-hotspot]');
    if (hotEl) {
      e.preventDefault();
      var key = hotEl.getAttribute('data-hotspot');
      var m = findByHotspot(key);
      if (m) openDrill(m);
      return;
    }
    var tileEl = e.target.closest('[data-drill-id]');
    if (tileEl) {
      e.preventDefault();
      var id = tileEl.getAttribute('data-drill-id');
      var m2 = findById(id);
      if (m2) openDrill(m2);
      return;
    }
    var actionEl = e.target.closest('[data-action]');
    if (!actionEl) return;
    var action = actionEl.getAttribute('data-action');
    if (action === 'drill-close') {
      if (runnerEl) runnerEl.hidden = true;
      current = null;
    } else if (action === 'drill-retry') {
      if (current) openDrill(current);
    } else if (action === 'drills-reset') {
      if (confirm('Reset all drill progress on this device?')) {
        try {
          localStorage.removeItem(DONE_KEY);
          localStorage.removeItem(HABITS_KEY);
          localStorage.removeItem(BEST_KEY);
        } catch (e) {}
        if (runnerEl) runnerEl.hidden = true;
        current = null;
        refreshMeter();
      }
    } else if (action === 'drills-certificate') {
      var doneNow = getDone();
      if (doneNow.size < DRILLS.length) {
        alert('Finish all ' + DRILLS.length + ' drills to unlock your certificate. '
          + 'You have ' + doneNow.size + ' of ' + DRILLS.length + ' complete.');
        return;
      }
      downloadCertificate();
    }
  });

  document.addEventListener('change', function (e) {
    var el = e.target;
    if (!el || !el.matches || !el.matches('[data-aar-habit]')) return;
    toggleHabit(el.getAttribute('data-aar-habit'), el.checked);
    refreshMeter();
  });

  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Enter' && e.key !== ' ') return;
    var act = document.activeElement;
    if (!act || !act.classList || !act.classList.contains('lab-hotspot')) return;
    e.preventDefault();
    act.dispatchEvent(new MouseEvent('click', { bubbles: true }));
  });

  refreshMeter();
})();
