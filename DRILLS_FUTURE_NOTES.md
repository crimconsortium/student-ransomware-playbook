# Drills — deferred review notes

**Status:** Drills section is being **unlinked** (option #2 from the May 27 2026 review with Joshua and Scott). Source content stays in the repo. These notes apply **only if/when drills come back online**. Do not act on these until that decision is made.

**Source:** Joshua Gerstenfeld review, relayed by Scott Jacques, May 27 2026.

---

## Items to address before drills are republished

### 1. Remove the post-drill After-Action Review checklist and the "If something goes wrong" link
Both appear after a student finishes a drill. Joshua finds them annoying and notes they repeat / link out to material already covered elsewhere on the site. When drills come back, strip both from the drill completion view. Touchpoints (as of the May 2026 build):
- `assets/js/drills.js` — AAR rendering and the "If something goes wrong" link
- `drills.html` — any related markup
- The AAR-print button noted in the earlier print-button cleanup should be removed at the same time (it was kept then because it had a real after-action use; that use is being retired)

### 2. Remove the visual dorm-room SVG
Joshua finds it confusing rather than helpful. When drills come back, drop the dorm SVG from `drills.html`. Keep the tile grid of drills — that's the navigation that matters. Source asset and any related CSS can be removed at the same time.

### 3. Tighten the drill answer model

Direction from Joshua (Scott concurs):

- **No "risky" or "avoid" categories.** Every terminal answer (one that doesn't branch into a new question) is either **Correct** or **Incorrect**.
- **Correct answers highlighted green; incorrect answers highlighted red.** Reuse the scoped quiz palette already added in May 2026 (`#1f8a3a` / `#c0392b`, with dark-mode variants) — same approach, applied to drill outcomes.
- **Remove ambiguous or neutral options.** Every answer offered must clearly harm or clearly help security. No "it depends" terminal outcomes.
- **Add a "Step back" button** on multi-part drills so the student can undo a choice and try the previous step again.

Implementation notes for future me:
- Audit every drill in `build/content.py` for outcomes currently tagged as anything other than a clean "correct" / "incorrect." Either promote them to one of those buckets or rewrite the option so the framing is unambiguous.
- The decision tree on the Response page is separate and is **not** in scope for this change — Joshua's note is about drills only.

### 4. Verify the "based on something that actually happened" claim
The drills page (or intro copy) states that each scenario is built around a real event. Before drills are republished:
- Re-read every drill and confirm whether that framing is actually true for each one.
- For each drill where it is true, attach a public source (same bar as the validity audit: CISA, FBI/IC3, named ISO, named journalism, peer-reviewed work).
- For any drill where it is **not** true, either (a) rewrite the framing so it isn't claimed, or (b) cut the drill.
- This work fits naturally into the `/verify/` subtree build — each drill becomes either a sourced scenario or an `[authoring choice]` scenario, with no middle ground.

### 5. Delete the first drill (the "should I pay the ransom?" one)
Reasoning from Joshua: the drill assumes "do not pay" is unambiguously correct. In some real student situations paying may actually be the least-bad option. Because the scenario is structured around that single decision, you can't fix it by rewriting one option — the whole drill is built on a contestable premise. Cleaner to remove than to modify.

Action when drills return: remove this drill from `build/content.py`, remove its tile from `drills.html`, and add a redirect from its old `/drills/<slug>/` path to `/drills/` so any external link doesn't 404.

---

## Cross-cutting note

If drills come back, they should ship into the `/verify/` subtree the same way the rest of the site does, with each drill declared as either a **sourced scenario** (real event, public source attached) or an **`[authoring choice]` scenario** (instructional, not claimed as real). That framing also resolves item #4 above — there is no "based on a real event" claim without a source behind it.
