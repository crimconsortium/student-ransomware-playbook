/* Campus Ransomware Playbook — client-side logic
 * MIT-licensed. Runs entirely in the browser. No analytics, no network calls.
 * State is kept in localStorage under "crp:*" keys.
 */
(function () {
  'use strict';

  /* ------------------------------ Theme ------------------------------ */
  const THEME_KEY = 'crp:theme';
  function applyTheme(t) {
    if (t === 'light' || t === 'dark') {
      document.documentElement.setAttribute('data-theme', t);
    } else {
      document.documentElement.removeAttribute('data-theme');
    }
  }
  function initTheme() {
    const saved = localStorage.getItem(THEME_KEY);
    if (saved) applyTheme(saved);
  }
  function toggleTheme() {
    const cur = document.documentElement.getAttribute('data-theme');
    const sysDark = matchMedia('(prefers-color-scheme: dark)').matches;
    let next;
    if (!cur) next = sysDark ? 'light' : 'dark';
    else next = cur === 'dark' ? 'light' : 'dark';
    applyTheme(next);
    localStorage.setItem(THEME_KEY, next);
    updateThemeButton();
  }
  function updateThemeButton() {
    const btn = document.querySelector('.theme-toggle');
    if (!btn) return;
    const cur = document.documentElement.getAttribute('data-theme') ||
                (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    btn.setAttribute('aria-label', 'Switch to ' + (cur === 'dark' ? 'light' : 'dark') + ' mode');
    btn.textContent = cur === 'dark' ? '☀ Light' : '☾ Dark';
  }
  initTheme();

  /* ------------------------------ Mobile nav ------------------------------ */
  document.addEventListener('click', function (e) {
    const t = e.target.closest('.menu-toggle');
    if (!t) return;
    const nav = document.querySelector('nav.primary');
    if (!nav) return;
    const open = nav.getAttribute('data-open') === 'true';
    nav.setAttribute('data-open', open ? 'false' : 'true');
    t.setAttribute('aria-expanded', String(!open));
  });

  /* ------------------------------ Theme toggle wiring ------------------------------ */
  document.addEventListener('click', function (e) {
    if (e.target.closest('.theme-toggle')) toggleTheme();
  });

  /* ------------------------------ Role memory ------------------------------ */
  const ROLE_KEY = 'crp:role';
  function setRole(role) {
    if (!role) return;
    localStorage.setItem(ROLE_KEY, role);
    document.querySelectorAll('.role-tile').forEach(t => {
      t.classList.toggle('selected', t.dataset.role === role);
    });
    const banner = document.getElementById('role-banner');
    if (banner) banner.textContent = 'Your role: ' + roleLabel(role);
  }
  function getRole() { return localStorage.getItem(ROLE_KEY); }
  function roleLabel(r) {
    return ({
      student: 'Student',
      faculty: 'Faculty',
      staff: 'Staff',
      it: 'IT / Security',
      leadership: 'Leadership',
      comms: 'Communications / Legal'
    })[r] || r;
  }
  document.addEventListener('click', function (e) {
    const tile = e.target.closest('.role-tile');
    if (!tile) return;
    setRole(tile.dataset.role);
  });

  /* ------------------------------ Checklists ------------------------------ */
  // Persists per-checklist by [data-checklist-id]; each item by its index.
  function ckKey(id) { return 'crp:ck:' + id; }
  function loadCk(id) {
    try { return JSON.parse(localStorage.getItem(ckKey(id)) || '[]'); }
    catch (e) { return []; }
  }
  function saveCk(id, arr) { localStorage.setItem(ckKey(id), JSON.stringify(arr)); }
  function initChecklists() {
    document.querySelectorAll('.checklist[data-checklist-id]').forEach(cl => {
      const id = cl.dataset.checklistId;
      const state = loadCk(id);
      const items = cl.querySelectorAll('li');
      items.forEach((li, i) => {
        const cb = li.querySelector('input[type="checkbox"]');
        if (!cb) return;
        const cbid = 'ck-' + id + '-' + i;
        cb.id = cbid;
        const lab = li.querySelector('label');
        if (lab) lab.setAttribute('for', cbid);
        cb.checked = !!state[i];
        if (cb.checked) li.classList.add('done');
        cb.addEventListener('change', function () {
          state[i] = cb.checked;
          saveCk(id, state);
          li.classList.toggle('done', cb.checked);
          updateCkProgress(cl);
        });
      });
      // Reset
      const resetBtn = cl.querySelector('[data-action="reset"]');
      if (resetBtn) resetBtn.addEventListener('click', function () {
        items.forEach((li, i) => {
          const cb = li.querySelector('input[type="checkbox"]');
          if (cb) { cb.checked = false; li.classList.remove('done'); }
        });
        saveCk(id, []);
        updateCkProgress(cl);
      });
      updateCkProgress(cl);
    });
  }
  function updateCkProgress(cl) {
    const items = cl.querySelectorAll('li');
    const done = cl.querySelectorAll('li.done').length;
    const bar = cl.querySelector('.progress > span');
    const counter = cl.querySelector('[data-role="counter"]');
    const badge = cl.querySelector('[data-role="badge"]');
    const pct = items.length ? Math.round((done / items.length) * 100) : 0;
    if (bar) bar.style.width = pct + '%';
    if (counter) counter.textContent = done + ' of ' + items.length + ' complete (' + pct + '%)';
    if (badge) {
      if (done === items.length && items.length > 0) {
        badge.hidden = false;
        // Track earned badges
        const earnedKey = 'crp:badges';
        let earned = [];
        try { earned = JSON.parse(localStorage.getItem(earnedKey) || '[]'); } catch (e) {}
        const id = cl.dataset.checklistId;
        if (id && !earned.includes(id)) {
          earned.push(id);
          localStorage.setItem(earnedKey, JSON.stringify(earned));
        }
      } else {
        badge.hidden = true;
      }
    }
  }

  /* ------------------------------ Decision trees ------------------------------ */
  // Tree structure embedded in [data-decision] script tag (JSON).
  function initDecisionTrees() {
    document.querySelectorAll('.decision[data-decision-id]').forEach(d => {
      const dataEl = d.querySelector('script[type="application/json"]');
      if (!dataEl) return;
      let tree;
      try { tree = JSON.parse(dataEl.textContent); }
      catch (e) { return; }
      const path = [];
      function render(nodeId) {
        const node = tree.nodes[nodeId];
        if (!node) return;
        const q = d.querySelector('.question');
        const choices = d.querySelector('.choices');
        const result = d.querySelector('.result');
        const crumbs = d.querySelector('.breadcrumbs');
        if (crumbs) crumbs.textContent = path.length ? 'Path: ' + path.join(' → ') : '';
        if (node.type === 'result') {
          if (q) q.textContent = '';
          if (choices) choices.innerHTML = '';
          if (result) {
            result.innerHTML = '<strong>' + (node.title || 'Recommended action') + '</strong><br>' + node.body;
            result.hidden = false;
            const restartBtn = document.createElement('button');
            restartBtn.className = 'btn btn-secondary btn-sm';
            restartBtn.style.marginTop = '0.6rem';
            restartBtn.textContent = '↺ Start over';
            restartBtn.addEventListener('click', function () {
              path.length = 0;
              if (result) { result.hidden = true; result.innerHTML = ''; }
              render(tree.start);
            });
            result.appendChild(document.createElement('br'));
            result.appendChild(restartBtn);
          }
          return;
        }
        if (q) q.textContent = node.q;
        if (result) { result.hidden = true; result.innerHTML = ''; }
        if (choices) {
          choices.innerHTML = '';
          (node.choices || []).forEach(c => {
            const b = document.createElement('button');
            b.type = 'button';
            b.textContent = c.label;
            b.addEventListener('click', function () {
              path.push(c.label);
              render(c.next);
            });
            choices.appendChild(b);
          });
        }
      }
      render(tree.start);
    });
  }

  /* ------------------------------ Quizzes ------------------------------ */
  function initQuizzes() {
    document.querySelectorAll('.quiz[data-quiz-id]').forEach(q => {
      const dataEl = q.querySelector('script[type="application/json"]');
      if (!dataEl) return;
      let questions;
      try { questions = JSON.parse(dataEl.textContent); }
      catch (e) { return; }
      const id = q.dataset.quizId;
      let i = 0, score = 0;
      const stateKey = 'crp:quiz:' + id;

      function render() {
        const cur = questions[i];
        const qEl = q.querySelector('.question');
        const oEl = q.querySelector('.options');
        const fEl = q.querySelector('.feedback');
        const mEl = q.querySelector('.meta');
        if (mEl) {
          if (cur) {
            mEl.textContent = 'Question ' + (i + 1) + ' of ' + questions.length + ' · Score: ' + score;
          } else {
            mEl.textContent = 'Results · Score: ' + score + ' of ' + questions.length;
          }
        }
        if (!cur) {
          // Done
          if (qEl) qEl.textContent = 'Quiz complete';
          if (oEl) oEl.innerHTML = '';
          if (fEl) {
            fEl.innerHTML = '<strong>Final score: ' + score + ' / ' + questions.length + '</strong><br>' +
              (score === questions.length ? 'Perfect — well done.' :
               score >= Math.ceil(questions.length * 0.7) ? 'Strong result. Review missed items above.' :
               'Worth reviewing the role guidance and trying again.');
          }
          // Save best score
          let best = 0;
          try { best = parseInt(localStorage.getItem(stateKey) || '0', 10) || 0; } catch (e) {}
          if (score > best) localStorage.setItem(stateKey, String(score));
          // Restart
          if (oEl) {
            const r = document.createElement('button');
            r.className = 'btn btn-secondary btn-sm';
            r.textContent = '↺ Try again';
            r.addEventListener('click', function () { i = 0; score = 0; render(); });
            oEl.appendChild(r);
          }
          return;
        }
        if (qEl) qEl.textContent = cur.q;
        if (fEl) { fEl.hidden = true; fEl.textContent = ''; }
        if (oEl) {
          oEl.innerHTML = '';
          cur.options.forEach((opt, idx) => {
            const b = document.createElement('button');
            b.type = 'button';
            b.textContent = opt;
            b.addEventListener('click', function () {
              const correct = idx === cur.correct;
              if (correct) {
                score++;
                b.classList.add('correct');
              } else {
                b.classList.add('incorrect');
                const right = oEl.children[cur.correct];
                if (right) right.classList.add('correct');
              }
              // Disable
              [...oEl.querySelectorAll('button')].forEach(x => x.disabled = true);
              if (fEl) {
                fEl.hidden = false;
                fEl.innerHTML = '<strong>' + (correct ? 'Correct.' : 'Not quite.') + '</strong> ' + (cur.explanation || '');
                const next = document.createElement('button');
                next.className = 'btn btn-sm';
                next.style.marginTop = '0.6rem';
                next.textContent = (i + 1 < questions.length) ? 'Next question →' : 'See results';
                next.addEventListener('click', function () { i++; render(); });
                fEl.appendChild(document.createElement('br'));
                fEl.appendChild(next);
              }
            });
            oEl.appendChild(b);
          });
        }
      }
      render();
    });
  }

  /* ------------------------------ Active nav ------------------------------ */
  function markCurrentNav() {
    const here = location.pathname.replace(/\/+$/, '') || '/';
    document.querySelectorAll('nav.primary a').forEach(a => {
      try {
        const u = new URL(a.href, location.href);
        const path = u.pathname.replace(/\/+$/, '') || '/';
        if (path === here) a.setAttribute('aria-current', 'page');
      } catch (e) {}
    });
  }

  /* ------------------------------ Init ------------------------------ */
  document.addEventListener('DOMContentLoaded', function () {
    updateThemeButton();
    markCurrentNav();
    initChecklists();
    initDecisionTrees();
    initQuizzes();
    // Restore saved role highlight
    const r = getRole();
    if (r) setRole(r);
    // Year in footer
    document.querySelectorAll('[data-year]').forEach(el => {
      el.textContent = String(new Date().getFullYear());
    });
  });
})();
