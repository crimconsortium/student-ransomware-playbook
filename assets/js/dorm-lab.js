/*
 * Dorm Room Incident Lab engine.
 *
 * Reads the LAB modules from <script id="lab-data"> (JSON), then wires:
 *   - clickable SVG hotspots + tile grid (both use data-hotspot="<key>")
 *   - branching decision runner (mirrors scenarios.js shape, simpler)
 *   - after-action review checklist per module
 *   - a single overall readiness meter: % = (completed modules + checked habits)
 *     out of (total modules + total unique habits across all modules)
 *
 * No-op on pages that don't include #lab-data.
 *
 * LocalStorage keys:
 *   srp:lab:done      JSON array of completed module IDs
 *   srp:lab:habits    JSON array of checked habit strings (deduped across modules)
 */
(function () {
  var dataEl = document.getElementById('lab-data');
  if (!dataEl) return;

  var LAB;
  try { LAB = JSON.parse(dataEl.textContent); }
  catch (e) { console.warn('lab data parse failed', e); return; }
  if (!Array.isArray(LAB) || !LAB.length) return;

  // Build a flat list of every unique habit across modules — used as the
  // denominator for the readiness meter so a student who completes everything
  // and checks every habit reaches 100%.
  var ALL_HABITS = (function () {
    var seen = Object.create(null);
    var out = [];
    LAB.forEach(function (m) {
      (m.aar || []).forEach(function (h) {
        if (!seen[h]) { seen[h] = 1; out.push(h); }
      });
    });
    return out;
  })();

  var DONE_KEY = 'srp:lab:done';
  var HABITS_KEY = 'srp:lab:habits';

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
    catch (e) { /* quota / private mode */ }
  }
  function getDone() { return readSet(DONE_KEY); }
  function getHabits() { return readSet(HABITS_KEY); }
  function markDone(id) {
    var s = getDone(); s.add(id); writeSet(DONE_KEY, s);
  }
  function toggleHabit(habit, on) {
    var s = getHabits();
    if (on) s.add(habit); else s.delete(habit);
    writeSet(HABITS_KEY, s);
  }

  // ---- Readiness meter -----------------------------------------------------
  function refreshMeter() {
    var done = getDone();
    var habits = getHabits();
    var totalUnits = LAB.length + ALL_HABITS.length;
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
    if (counterEl) counterEl.textContent = done.size + ' of ' + LAB.length + ' modules complete';
    if (habitCounterEl) habitCounterEl.textContent = habits.size + ' of ' + ALL_HABITS.length + ' habits checked';

    // Per-tile "Done" badge
    LAB.forEach(function (m) {
      var badge = document.querySelector('[data-lab-status="' + cssEscape(m.id) + '"]');
      if (!badge) return;
      if (done.has(m.id)) {
        badge.textContent = '✓ Done';
        badge.classList.add('is-done');
      } else {
        badge.textContent = '';
        badge.classList.remove('is-done');
      }
    });
  }

  function cssEscape(s) {
    // Module IDs are simple kebab-case so a regex strip is enough.
    return String(s).replace(/"/g, '\\"');
  }

  // ---- Runner --------------------------------------------------------------
  var runnerEl = document.querySelector('.lab-runner');
  var titleEl = document.querySelector('[data-role="lab-title"]');
  var setupEl = document.querySelector('[data-role="lab-setup"]');
  var qEl = document.querySelector('[data-role="lab-question"]');
  var choicesEl = document.querySelector('[data-role="lab-choices"]');
  var outcomeEl = document.querySelector('[data-role="lab-outcome"]');
  var aarEl = document.querySelector('[data-role="lab-aar"]');

  var current = null; // current module being played

  function findByHotspot(key) {
    for (var i = 0; i < LAB.length; i++) if (LAB[i].hotspot === key) return LAB[i];
    return null;
  }
  function findById(id) {
    for (var i = 0; i < LAB.length; i++) if (LAB[i].id === id) return LAB[i];
    return null;
  }

  function openModule(m) {
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
    // Smooth-scroll into view
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
        btn.addEventListener('click', function () { renderNode(c.next); });
        choicesEl.appendChild(btn);
      });
      outcomeEl.hidden = true;
      aarEl.hidden = true;
    } else if (node.type === 'outcome') {
      qEl.style.display = 'none';
      choicesEl.style.display = 'none';
      var tagClass = 'lab-tag-' + (node.tag || 'ok');
      var tagLabel = ({ good: 'STRONG', ok: 'OK', risky: 'RISKY', bad: 'AVOID' })[node.tag] || 'OK';
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
            '<button type="button" class="btn btn-secondary btn-sm" data-action="lab-retry">↺ Try again</button>' +
            '<button type="button" class="btn btn-secondary btn-sm" data-action="lab-close">← Back to room</button>' +
          '</div>' +
        '</div>';
      outcomeEl.hidden = false;
      // Mark done on first outcome reached for this module
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
    return String(s).replace(/[&<>"']/g, function (c) {
      return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c];
    });
  }
  function escapeAttr(s) { return escapeHtml(s); }

  // ---- Event delegation ----------------------------------------------------
  document.addEventListener('click', function (e) {
    // Hotspot or tile click
    var hotEl = e.target.closest('[data-hotspot]');
    if (hotEl) {
      e.preventDefault();
      var key = hotEl.getAttribute('data-hotspot');
      var m = findByHotspot(key);
      if (m) openModule(m);
      return;
    }
    // Tile may also have data-lab-id (specific module)
    var tileEl = e.target.closest('[data-lab-id]');
    if (tileEl) {
      e.preventDefault();
      var id = tileEl.getAttribute('data-lab-id');
      var m2 = findById(id);
      if (m2) openModule(m2);
      return;
    }
    var action = e.target.getAttribute && e.target.getAttribute('data-action');
    if (!action) return;
    if (action === 'lab-close') {
      if (runnerEl) runnerEl.hidden = true;
      current = null;
    } else if (action === 'lab-retry') {
      if (current) openModule(current);
    } else if (action === 'lab-reset') {
      if (confirm('Reset all dorm-lab progress on this device?')) {
        try { localStorage.removeItem(DONE_KEY); localStorage.removeItem(HABITS_KEY); } catch (e) {}
        if (runnerEl) runnerEl.hidden = true;
        current = null;
        refreshMeter();
      }
    }
  });

  // Habit checkbox toggling
  document.addEventListener('change', function (e) {
    var el = e.target;
    if (!el || !el.matches || !el.matches('[data-aar-habit]')) return;
    toggleHabit(el.getAttribute('data-aar-habit'), el.checked);
    refreshMeter();
  });

  // Keyboard: pressing Enter on a focused SVG hotspot triggers it.
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Enter' && e.key !== ' ') return;
    var act = document.activeElement;
    if (!act || !act.classList || !act.classList.contains('lab-hotspot')) return;
    e.preventDefault();
    act.dispatchEvent(new MouseEvent('click', { bubbles: true }));
  });

  refreshMeter();
})();
