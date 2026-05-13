# Campus Ransomware Playbook

An open-access, evidence-based playbook helping every role on campus prevent and respond to ransomware. Created by **Joshua Gerstenfeld** and **Scott Jacques** with support from the **CrimRxiv Consortium**.

🌐 **Live site:** https://crimconsortium.github.io/campus-ransomware-playbook/

## What this is

A self-contained static website with role-based guidance for higher-education institutions — public and private universities, community colleges, and other colleges. It covers prevention and response across the full lifecycle: prepare, detect, contain, communicate, recover, and learn.

Every role on campus is treated as equally important:

- **Students**
- **Faculty** (including adjuncts and researchers)
- **Staff and department personnel**
- **Campus IT and security teams**
- **Senior leadership and administrators**
- **Communications, public affairs, and legal**

## Features

- Role-based navigation with persistent (browser-only) role memory.
- Per-role checklists with progress saved on-device — no accounts, no servers.
- "What should I do right now?" decision trees for common situations.
- Mini-scenarios and quizzes with immediate feedback.
- A campus-wide self-audit checklist.
- A concise **Emergency** page for active incidents.
- Glossary and FAQ for non-technical readers.
- Light/dark mode honoring system preferences.
- WCAG-aware semantic HTML, keyboard navigation, and accessible contrast.
- Print-friendly CSS and downloadable PDFs of every role guide plus an overall summary.

The site is fully static — works on GitHub Pages out of the box. No backend, no database, no third-party JavaScript.

## Repository layout

```
.
├── index.html              # Home / role selector
├── prevention.html         # Prepare + detect
├── response.html           # Contain, communicate, recover, learn
├── emergency.html          # Action-oriented "right now" page
├── readiness.html          # Campus-wide and per-role self-audit
├── glossary.html
├── faq.html
├── references.html
├── 404.html
├── roles/                  # Per-role guides (built)
│   ├── index.html
│   ├── student.html
│   ├── faculty.html
│   ├── staff.html
│   ├── it.html
│   ├── leadership.html
│   └── comms.html
├── assets/
│   ├── css/styles.css
│   ├── js/app.js
│   └── pdf/                # Generated role PDFs + summary PDF
├── build/
│   ├── content.py          # Source-of-truth content for pages and PDFs
│   ├── build_pages.py      # Generates HTML pages
│   └── build_pdfs.py       # Generates PDFs (ReportLab)
├── LICENSE                 # MIT (code)
└── LICENSE-content         # CC BY 4.0 (content)
```

## Build locally

Requires Python 3.10+ and `reportlab` (only for PDF builds).

```bash
# Pages
python build/build_pages.py

# PDFs (requires reportlab)
pip install reportlab
python build/build_pdfs.py

# Preview
python -m http.server 5000
# then open http://localhost:5000/
```

GitHub Pages is configured to serve from the `main` branch root.

## Maintenance cadence

The playbook is reviewed and updated **quarterly**. Each cycle:

1. Re-checks credible sources (EDUCAUSE, NIST, CISA, peer-reviewed reporting).
2. Updates content where new or clearer guidance justifies it.
3. Keeps URLs and major headings stable to avoid breaking external references.
4. Regenerates HTML and PDFs.
5. Commits to `main` with a meaningful message and produces a short change summary.

## Licensing

- **Code** (HTML, CSS, JS, build scripts, configuration): [MIT License](LICENSE).
- **Content** (text, checklists, decision trees, quizzes, glossary, illustrations, PDFs): [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE-content).

When reusing or adapting content, please credit:

> *Campus Ransomware Playbook* by Joshua Gerstenfeld and Scott Jacques (CrimRxiv Consortium), CC BY 4.0, https://github.com/crimconsortium/campus-ransomware-playbook

## Safety and scope

This playbook is **strictly defensive and educational**. It does not include exploit code, offensive techniques, or anything that meaningfully lowers the barrier to committing ransomware or related crimes. It distinguishes general guidance from institution-specific legal or regulatory obligations and does not constitute legal advice; coordinate with counsel for jurisdiction- and contract-specific decisions.

## Contributing

Improvements, corrections, and additional examples are welcome via GitHub Issues and Pull Requests. Please keep:

- Language plain and directive.
- Roles equally represented.
- Content vendor-neutral.
- Sources reputable and recent.

## Acknowledgements

Guidance synthesized from publicly available material, including:

- NIST SP 800-61r3 (Incident Response, 2025) and NIST IR 8374 (Ransomware Risk Management).
- CISA #StopRansomware and the CISA/MS-ISAC Ransomware Guide.
- EDUCAUSE cybersecurity articles and benchmarks.
- Reporting on higher-ed ransomware (Higher Ed Dive, GovTech, Comparitech).

See the [References page](https://crimconsortium.github.io/campus-ransomware-playbook/references.html) for the full list.
