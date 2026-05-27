"""Generate all HTML pages from content.py.

Run from repo root:  python build/build_pages.py
"""
from __future__ import annotations
import os, html, json, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent


def _read_svg(name: str) -> str:
    """Read an SVG file and strip the XML prolog so it can be embedded inline in HTML."""
    raw = (ROOT / "assets" / "img" / name).read_text(encoding="utf-8")
    # remove '<?xml ... ?>' if present
    if raw.startswith("<?xml"):
        raw = raw.split("?>", 1)[1].lstrip()
    return raw


def lifecycle_figure(emphasize: str, caption: str) -> str:
    """Inline the lifecycle SVG inside a figure that emphasizes 'prevention' or 'response'.
    The SVG itself contains <g class="prev-band"> and <g class="resp-band"> wrappers; the
    emphasize-* class on the figure dims the non-emphasized band via stylesheet rules."""
    cls = {
        "prevention": "emphasize-prev",
        "response":   "emphasize-resp",
    }.get(emphasize, "")
    svg = _read_svg("lifecycle.svg")
    return f'''    <figure class="diagram {cls}" role="img" aria-label="Six-phase ransomware lifecycle. Prevention spans Prepare and Detect; response spans Contain, Communicate, Recover, and Learn. Lessons from Learn feed back into Prepare.">
{svg}
      <figcaption>{caption}</figcaption>
    </figure>'''
sys.path.insert(0, str(ROOT / "build"))
from content import ROLES, PHASES, GLOSSARY, FAQ, REFERENCES, DRILLS, CITATIONS, CITATION_SOURCES  # noqa: E402


def page(title: str, body: str, *, depth: int = 0, description: str = "") -> str:
    """Return a full HTML page. depth = directory depth from repo root."""
    rel = "../" * depth
    desc = description or "Student Ransomware Playbook. A plain-language educational guide for college and university students."
    desc = html.escape(desc)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} · Student Ransomware Playbook</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Serif+4:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600&display=swap">
<link rel="stylesheet" href="{rel}assets/css/styles.css">
<meta name="theme-color" content="#f68212">
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>

<header class="site-header">
  <div class="container">
    <a class="brand" href="{rel}index.html">
      <span class="title">Student Ransomware Playbook</span>
    </a>
    <button class="menu-toggle" aria-expanded="false" aria-controls="primary-nav" aria-label="Toggle menu">☰ Menu</button>
    <nav class="primary" id="primary-nav" aria-label="Primary">
      <ul>
        <li><a href="{rel}index.html">Home</a></li>
        <li><a href="{rel}prevention.html">Protect yourself</a></li>
        <li><a href="{rel}response.html">If something goes wrong</a></li>
        <li><a href="{rel}readiness.html">Checklist</a></li>
        <li><a href="{rel}glossary.html">Glossary</a></li>
        <li><a href="{rel}faq.html">FAQ</a></li>
        <li><button class="theme-toggle" aria-label="Toggle dark mode">☾ Dark</button></li>
      </ul>
    </nav>
  </div>
</header>

<main id="main">
{body}
</main>

<footer class="site-footer">
  <div class="container grid">
    <div>
      <h4>Student Ransomware Playbook</h4>
      <p>Created by Joshua Gerstenfeld and Scott Jacques with support from the CrimRxiv Consortium.</p>
      <p><a href="https://github.com/crimconsortium/student-ransomware-playbook">View source on GitHub</a></p>
    </div>
    <div>
      <h4>Sections</h4>
      <ul>
        <li><a href="{rel}prevention.html">Protect yourself</a></li>
        <li><a href="{rel}response.html">If something goes wrong</a></li>
        <li><a href="{rel}readiness.html">Checklist</a></li>
      </ul>
    </div>
    <div>
      <h4>References</h4>
      <ul>
        <li><a href="{rel}glossary.html">Glossary</a></li>
        <li><a href="{rel}faq.html">FAQ</a></li>
        <li><a href="{rel}references.html">Sources &amp; further reading</a></li>
      </ul>
    </div>
    <div>
      <h4>Licensing</h4>
      <ul>
        <li>Code: <a href="{rel}LICENSE">MIT</a></li>
        <li>Content: <a href="{rel}LICENSE-content">CC BY 4.0</a></li>
        <li><a href="{rel}verify/index.html">Citation view</a></li>
      </ul>
      <p class="muted">© <span data-year></span> Joshua Gerstenfeld &amp; Scott Jacques.</p>
    </div>
  </div>
</footer>

<script src="{rel}assets/js/app.js"></script>
</body>
</html>
"""


# ---------------- Decision trees & quizzes per role -------------------
DECISION_TREES = {
    "student": {
        "start": "n0",
        "nodes": {
            "n0": {"type": "q", "q": "What just happened?", "choices": [
                {"label": "I got a suspicious email or text.", "next": "n_phish_1"},
                {"label": "My device is acting strange or shows a ransom note.", "next": "n_device_1"},
                {"label": "I think I already entered my password into a fake site.", "next": "n_creds_1"},
            ]},
            "n_phish_1": {"type": "q", "q": "Did you click a link or open an attachment?", "choices": [
                {"label": "No.", "next": "n_phish_no"},
                {"label": "Yes.", "next": "n_creds_1"},
            ]},
            "n_phish_no": {"type": "result", "title": "Report it and move on.",
                "body": "Use the campus ‘Report Phishing’ button or forward as an attachment to your security team. Do not reply to the sender. Delete after reporting."},
            "n_creds_1": {"type": "q", "q": "Are you on the same device that may have been compromised right now?", "choices": [
                {"label": "Yes.", "next": "n_creds_same"},
                {"label": "No.", "next": "n_creds_other"},
            ]},
            "n_creds_same": {"type": "result", "title": "Switch devices, then act.",
                "body": "Move to a different device (your phone is fine) and: (1) change the affected password, (2) review your account recovery info, (3) report to IT immediately. Don’t use the suspect device until IT has reviewed it."},
            "n_creds_other": {"type": "result", "title": "Change the password and report.",
                "body": "Change the affected password right now from this safe device. Then call or email IT to report what happened. Keep the original phishing message as evidence."},
            "n_device_1": {"type": "q", "q": "Can you safely disconnect from Wi-Fi and unplug any cables?", "choices": [
                {"label": "Yes, doing it now.", "next": "n_device_disc"},
                {"label": "No.", "next": "n_device_call"},
            ]},
            "n_device_disc": {"type": "result", "title": "Leave it on, stay off the network, call IT.",
                "body": "Don't power off the device. IT may need volatile memory. Don't try to recover files yourself. Call the help desk and describe exactly what you saw."},
            "n_device_call": {"type": "result", "title": "Call IT now.",
                "body": "Call the help desk immediately and describe what you’re seeing. They’ll guide containment from there."},
        }
    },
    "faculty": {
        "start": "n0",
        "nodes": {
            "n0": {"type": "q", "q": "What are you seeing?", "choices": [
                {"label": "Suspicious email about a paper, grant, or co-authorship.", "next": "n_lure"},
                {"label": "Files renamed, unreadable, or a ransom note.", "next": "n_enc"},
                {"label": "A grad student or TA reports something off.", "next": "n_team"},
            ]},
            "n_lure": {"type": "result", "title": "Verify, then report.",
                "body": "Don’t click. Check the sender domain carefully and verify via a known channel (their public page, a previous email thread, a phone call). Report the message to IT/security regardless of outcome — these targeted lures often hit many faculty at once."},
            "n_enc": {"type": "q", "q": "Is this on a campus-managed device or your personal device?", "choices": [
                {"label": "Campus-managed.", "next": "n_enc_campus"},
                {"label": "Personal but used for work.", "next": "n_enc_personal"},
            ]},
            "n_enc_campus": {"type": "result", "title": "Disconnect and call IT immediately.",
                "body": "Turn off Wi-Fi, unplug Ethernet, leave the device powered on. Notify co-authors and lab members so they can check their access. Pause major data movements until IT clears the environment."},
            "n_enc_personal": {"type": "result", "title": "Disconnect, isolate, and call IT.",
                "body": "Disconnect from the network immediately. Do not connect external drives. Call IT — even on a personal device, work data and your campus identity may be at risk."},
            "n_team": {"type": "result", "title": "Treat it as real until proven otherwise.",
                "body": "Have them stop using the suspect account/device, change credentials from a different device, and report to IT. One shared compromised account can expose a whole lab."},
        }
    },
    "staff": {
        "start": "n0",
        "nodes": {
            "n0": {"type": "q", "q": "What kind of issue?", "choices": [
                {"label": "Vendor or executive emailed an urgent payment/banking change.", "next": "n_bec"},
                {"label": "Tool or shared drive isn’t responding the way it should.", "next": "n_tool"},
                {"label": "Ransom note or files renamed on a shared drive.", "next": "n_ransom"},
            ]},
            "n_bec": {"type": "result", "title": "Pause. Verify by phone.",
                "body": "Do not act on the email. Call the vendor or executive at a number you already have on file (not one in the email). Loop in finance leadership and IT/security before sending or approving anything."},
            "n_tool": {"type": "q", "q": "Is more than one person affected?", "choices": [
                {"label": "Yes.", "next": "n_tool_many"},
                {"label": "Just me.", "next": "n_tool_one"},
            ]},
            "n_tool_many": {"type": "result", "title": "Report as a possible incident.",
                "body": "Multiple users affected at once is a red flag. Stop sending payments or moving sensitive data; contact IT and use an out-of-band channel (phone or signed-in chat) until cleared."},
            "n_tool_one": {"type": "result", "title": "Report and switch to a backup workflow.",
                "body": "Open a help desk ticket with screenshots. Don’t reinstall or ‘fix’ unfamiliar software yourself. Use offline contact lists if you need to keep operating."},
            "n_ransom": {"type": "result", "title": "Disconnect and call IT now.",
                "body": "Disconnect the affected device from the network. Do not delete files or close the ransom note. Pause approvals and payments until IT clears the environment."},
        }
    },
    "it": {
        "start": "n0",
        "nodes": {
            "n0": {"type": "q", "q": "Where are you in the lifecycle?", "choices": [
                {"label": "Suspicion only — alerts but no confirmed compromise.", "next": "n_susp"},
                {"label": "Confirmed compromise, encryption may be active.", "next": "n_active"},
                {"label": "Post-event recovery / hardening.", "next": "n_post"},
            ]},
            "n_susp": {"type": "result", "title": "Hunt and validate before disrupting.",
                "body": "Pivot from the alert in EDR and identity logs. Look for impossible travel, OAuth grants, mailbox rules, scheduled tasks, and unusual admin tool use. Document a timeline as you go. Decide containment thresholds with the IC."},
            "n_active": {"type": "q", "q": "Is encryption confirmed on multiple hosts?", "choices": [
                {"label": "Yes.", "next": "n_active_yes"},
                {"label": "No, isolated.", "next": "n_active_no"},
            ]},
            "n_active_yes": {"type": "result", "title": "Declare the incident; isolate, preserve, communicate.",
                "body": "Trigger the IR plan, name the IC, isolate affected segments, disable compromised identities, revoke sessions and tokens, capture memory and disk images. Engage legal, insurer, and FBI/CISA early. Coordinate with comms on cadence."},
            "n_active_no": {"type": "result", "title": "Contain narrowly and accelerate hunting.",
                "body": "Isolate the affected host(s), preserve evidence, and assume lateral movement until proven otherwise. Hunt across identity, endpoint, and network telemetry. Brief the IC; expand containment if scope grows."},
            "n_post": {"type": "result", "title": "Validate eradication, then run the AAR.",
                "body": "Hunt for persistence (accounts, scheduled tasks, OAuth, mailbox rules). Rebuild from known-good images. Rotate secrets and certificates. Run a blameless AAR; track remediation actions with owners and dates."},
        }
    },
    "leadership": {
        "start": "n0",
        "nodes": {
            "n0": {"type": "q", "q": "Where are you?", "choices": [
                {"label": "Pre-incident planning.", "next": "n_pre"},
                {"label": "Active incident.", "next": "n_active"},
                {"label": "Post-incident.", "next": "n_post"},
            ]},
            "n_pre": {"type": "result", "title": "Fund the baseline and decide who decides.",
                "body": "Document risk appetite and IR authorities. Fund MFA, immutable backups, EDR, segmentation, and security staffing. Approve an annual tabletop with cabinet participation."},
            "n_active": {"type": "result", "title": "Defer technical sequencing to the IC; own the business decisions.",
                "body": "Convene the crisis team. Make the calls IT cannot: which services to suspend, what to communicate, how to coordinate with insurer/counsel/law enforcement. Communicate calmly and frequently."},
            "n_post": {"type": "result", "title": "Receive the AAR; fund the fixes.",
                "body": "Approve the remediation plan with timelines and budget. Report to the board, regulators, and accreditors as required. Re-baseline cyber investment based on observed gaps."},
        }
    },
    "comms": {
        "start": "n0",
        "nodes": {
            "n0": {"type": "q", "q": "What stage?", "choices": [
                {"label": "We need to send our first message.", "next": "n_first"},
                {"label": "We’re mid-incident and questions are mounting.", "next": "n_mid"},
                {"label": "We’re closing out.", "next": "n_close"},
            ]},
            "n_first": {"type": "result", "title": "Use the holding statement.",
                "body": "Acknowledge there is a cybersecurity event, that you are investigating, that protecting people and data is the priority, and where to go for updates. Coordinate with legal, IT, leadership, and (where relevant) counsel/insurer/law enforcement before sending."},
            "n_mid": {"type": "result", "title": "Cadence over speculation.",
                "body": "Maintain a defined update rhythm. Be transparent about what you know, what you don’t, and what you are doing. Avoid attribution. Keep one source of truth."},
            "n_close": {"type": "result", "title": "Close honestly; file what you owe.",
                "body": "Issue a closing communication: what happened (at the right level of detail), what was affected, what changed, and what people should do. File required regulatory notifications within statutory deadlines and document the analysis behind notification decisions."},
        }
    },
}


QUIZZES = {
    "student": [
        {"q": "You receive an email from ‘IT Help Desk’ saying your account will be deleted in 24 hours unless you click a link to verify. The link goes to a page that looks like your campus login. What do you do?",
         "options": [
             "Enter my password. I don't want my account deleted.",
             "Click the link but only check it; don’t log in.",
             "Don’t click. Report the message via the campus phishing report tool.",
             "Reply asking if it’s real."],
         "correct": 2,
         "explanation": "Urgency + login prompt + unfamiliar link is a classic phishing pattern. Clicking can run scripts; replying confirms your address. Report it instead."},
        {"q": "You realize you typed your campus password into a fake login page yesterday. What should you do first?",
         "options": [
             "Wait to see if anything bad happens.",
             "Change the password now from a different device, then report it to IT.",
             "Email IT from the affected device.",
             "Delete the phishing email so no one knows."],
         "correct": 1,
         "explanation": "Speed beats embarrassment. Change the password from a clean device, then report. Keep the email as evidence."},
        {"q": "Your laptop suddenly shows files renamed with weird extensions and a ransom note. What’s the first move?",
         "options": [
             "Power it off immediately.",
             "Disconnect from Wi-Fi/Ethernet, leave it on, and contact IT.",
             "Run a free decryption tool you find online.",
             "Pay the ransom in crypto."],
         "correct": 1,
         "explanation": "Power-off can destroy volatile evidence. Disconnect from the network and call IT. Never pay or download unknown 'decryption' tools."},
        {"q": "Which of these is the strongest defense against credential phishing?",
         "options": [
             "A long password.",
             "Phishing-resistant MFA (a hardware key or platform authenticator).",
             "Antivirus software.",
             "Avoiding sketchy websites."],
         "correct": 1,
         "explanation": "Long passwords help, but phishing-resistant MFA (FIDO2/WebAuthn) binds the credential to the legitimate site, so it cannot be replayed on a fake login page."},
    ],
    "faculty": [
        {"q": "A ‘publisher’ emails inviting you to co-author or peer-review and asks you to log in via a link to access the manuscript. Best move?",
         "options": [
             "Log in to see the offer.",
             "Verify via the publisher’s known site or your existing editor contact, and report the message regardless.",
             "Forward to your TAs to handle.",
             "Click the link in a private window — that’s safe."],
         "correct": 1,
         "explanation": "Targeted lures often impersonate publishers. Verify out-of-band, never via the email’s link. Report to IT — colleagues are likely getting it too."},
        {"q": "Your only copy of a year’s research data is on your laptop. What’s the right answer?",
         "options": [
             "Encrypt the laptop and trust that.",
             "Move it to approved campus storage with versioned backups, and keep encryption.",
             "Email it to yourself for safety.",
             "Save it to a USB drive in your desk."],
         "correct": 1,
         "explanation": "Encryption protects confidentiality, not availability. Versioned campus storage protects against ransomware and hardware loss; the local copy stays encrypted."},
        {"q": "A grad student tells you their account is acting strange. Best response?",
         "options": [
             "Tell them to change their password later when they have time.",
             "Have them stop using the account, change credentials from a different device, and report to IT now.",
             "Try to log in yourself and see.",
             "Ignore it; they probably forgot a password."],
         "correct": 1,
         "explanation": "One compromised lab account can expose a whole project. Treat reports as real until proven otherwise."},
    ],
    "staff": [
        {"q": "A vendor emails to update their bank account for an upcoming payment. What do you do?",
         "options": [
             "Update the record and process the payment.",
             "Reply to the email asking for confirmation.",
             "Call the vendor at a number you already have on file to verify.",
             "Forward to a coworker for a second opinion."],
         "correct": 2,
         "explanation": "Business email compromise (BEC) is a top-impact attack. Always verify banking changes by phone using a previously known number — not anything in the email."},
        {"q": "You see a coworker step away from their desk without locking their screen on a system with student records. Best move?",
         "options": [
             "Lock it for them and tell them why next time you see them.",
             "Use their login to check your own email quickly.",
             "Leave it; it’s not your problem.",
             "Take a screenshot for your records."],
         "correct": 0,
         "explanation": "Lock the screen and remind them. Unattended sessions on regulated systems are a real risk and a FERPA concern."},
        {"q": "A ‘cloud storage upgrade’ tool is available online and would help your team share files. Right next step?",
         "options": [
             "Install it on your work computer.",
             "Ask your team to all install it.",
             "Ask IT/security to review it before introducing it.",
             "Email the vendor to negotiate."],
         "correct": 2,
         "explanation": "Shadow IT is a major source of breaches, including via third-party software exploits. Always route new tools through security review."},
    ],
    "it": [
        {"q": "You see one user account with logins from two countries within an hour. What’s the priority?",
         "options": [
             "Email the user politely.",
             "Disable the session and account, revoke tokens, and pivot to hunt for further activity.",
             "Reset the password and let them re-authenticate.",
             "Open a help-desk ticket for tomorrow."],
         "correct": 1,
         "explanation": "Impossible travel is high-confidence. Cut the session, revoke tokens, then hunt across identity and endpoint for follow-on activity."},
        {"q": "Backups exist for tier-1 systems but haven’t been restored end-to-end in 18 months. How should you treat them?",
         "options": [
             "As reliable — backups are backups.",
             "As untested. Schedule and run a real restoration test.",
             "Encrypt them again.",
             "Delete the oldest copies."],
         "correct": 1,
         "explanation": "Untested backups are not backups. Real restoration tests catch corruption, missing dependencies, and process gaps before you need them."},
        {"q": "Encryption is confirmed across multiple servers. What should you do first?",
         "options": [
             "Power off all affected servers.",
             "Trigger the IR plan, name the IC, isolate segments, disable identities, and preserve evidence.",
             "Restore from backups immediately.",
             "Pay the ransom to save time."],
         "correct": 1,
         "explanation": "Power-off destroys volatile evidence; restoring into a still-compromised environment reinfects. Activate the plan, contain, preserve, then recover into a hardened environment."},
    ],
    "leadership": [
        {"q": "A major incident is unfolding. Who should be making technical sequencing decisions?",
         "options": [
             "The president.",
             "The Incident Commander.",
             "The board.",
             "Whoever speaks loudest in the room."],
         "correct": 1,
         "explanation": "An IC, named in advance, directs the response regardless of seniority. Leadership owns business decisions; IC owns sequencing."},
        {"q": "An attacker is demanding ransom. What is the right framing?",
         "options": [
             "A purely technical decision for IT.",
             "A purely financial decision for the CFO.",
             "A strategic, legal, and ethical decision made with counsel, insurer, and law enforcement.",
             "Whatever the loudest stakeholder wants."],
         "correct": 2,
         "explanation": "Many incidents resolve without payment. Coordinate with counsel, your cyber-insurance carrier, and law enforcement (in the U.S., FBI/CISA)."},
    ],
    "comms": [
        {"q": "Reporters are asking pointed questions before you have facts. Best stance?",
         "options": [
             "Say ‘no comment.’",
             "Speculate to seem in control.",
             "Acknowledge the situation, share what you’ve confirmed, say what you don’t yet know, and commit to a cadence.",
             "Blame the attacker by name."],
         "correct": 2,
         "explanation": "Vague statements erode trust faster than honest uncertainty. Cadence and clarity beat speculation; avoid attribution."},
        {"q": "Where should the campus get authoritative updates during the incident?",
         "options": [
             "Wherever rumors are loudest.",
             "Different leaders’ personal social media.",
             "A single, pre-tested source of truth (status page, mass notification).",
             "The attackers’ leak site."],
         "correct": 2,
         "explanation": "One source of truth — pre-tested and ideally hosted off your main domain — keeps the campus aligned when normal channels are degraded."},
    ],
}


def render_phase_pills(include: list[str] | None = None) -> str:
    items = PHASES.items() if include is None else [(pid, PHASES[pid]) for pid in include if pid in PHASES]
    return (
        '<div class="phases">'
        + "".join(f'<a href="#{pid}">{html.escape(p["title"])}</a>' for pid, p in items)
        + "</div>"
    )


def render_role_page(role: dict) -> str:
    rid = role["id"]
    label = role["label"]
    items_html = lambda lst: "".join(f"<li>{html.escape(x)}</li>" for x in lst)
    chk_html = "".join(
        f'<li><input type="checkbox"><label>{html.escape(x)}</label></li>'
        for x in role["checklist_items"]
    )
    tree_json = html.escape(json.dumps(DECISION_TREES[rid]), quote=False)
    quiz_json = html.escape(json.dumps(QUIZZES[rid]), quote=False)
    pdf_link = f"../assets/pdf/role-{rid}.pdf"
    body = f"""
  <section class="container">
    <p class="muted"><a href="./">← All roles</a></p>
    <h1><span aria-hidden="true">{role['icon']}</span> {html.escape(label)}</h1>
    <p class="lead">{html.escape(role['summary'])}</p>
    <p>
      <a class="btn btn-secondary btn-sm" href="{pdf_link}">📄 Download PDF</a>
      <a class="btn btn-secondary btn-sm" href="../emergency.html">If an incident occurs</a>
    </p>
  </section>

  <section class="container">
    <div class="alert danger" role="note">
      <h4>Read this in advance, not during a live incident</h4>
      <p>The items below paraphrase public guidance from sources like CISA, NIST, and the FBI. It's for advance reading, not a substitute for your school's policies or trained responders. If something's happening right now, call campus IT. In the U.S. you can also report to <a href="https://www.cisa.gov/stopransomware/report-ransomware">CISA</a> and the <a href="https://www.ic3.gov/">FBI IC3</a>.</p>
    </div>
  </section>

  <section class="container read">
    <h2 id="before"><span class="tag before">Before</span> Prepare</h2>
    <ul>{items_html(role['before'])}</ul>

    <h2 id="during"><span class="tag during">During</span> Respond</h2>
    <ul>{items_html(role['during'])}</ul>

    <h2 id="after"><span class="tag after">After</span> Recover &amp; learn</h2>
    <ul>{items_html(role['after'])}</ul>
  </section>

  <section class="container">
    <h2>Self-audit checklist</h2>
    <p class="muted">Your progress is saved on this device only.</p>
    <div class="checklist" data-checklist-id="{rid}-readiness">
      <h3>{role['checklist_title']} <span class="badge-earned" data-role="badge" hidden>Complete</span></h3>
      <p class="muted" data-role="counter">0 of {len(role['checklist_items'])} complete</p>
      <div class="progress" aria-hidden="true"><span></span></div>
      <ul>
        {chk_html}
      </ul>
      <div class="actions">
        <button class="btn btn-secondary btn-sm" data-action="reset" type="button">Reset</button>
      </div>
    </div>
  </section>

  <section class="container">
    <h2>What should I do right now?</h2>
    <p>A short decision tree for the most common situations in this role.</p>
    <div class="decision" data-decision-id="{rid}-decision">
      <p class="breadcrumbs"></p>
      <p class="question"></p>
      <div class="choices"></div>
      <div class="result" hidden></div>
      <script type="application/json">{tree_json}</script>
    </div>
  </section>

  <section class="container">
    <h2>Practice scenario</h2>
    <p>Quick scenarios to turn this guidance into reflexes.</p>
    <div class="quiz" data-quiz-id="{rid}-quiz">
      <p class="meta"></p>
      <p class="question"></p>
      <div class="options"></div>
      <div class="feedback" hidden></div>
      <script type="application/json">{quiz_json}</script>
    </div>
  </section>

  <section class="container">
    <h2>Related</h2>
    <ul>
      <li><a href="../prevention.html">Prevention overview</a></li>
      <li><a href="../response.html">Response phases</a></li>
      <li><a href="../emergency.html">If an incident occurs (background reading)</a></li>
      <li><a href="../glossary.html">Glossary</a></li>
    </ul>
  </section>
"""
    return page(label, body, depth=1, description=f"Role guide for {label}: prepare, respond, recover.")


def render_role_index_redirect() -> str:
    """Stub at /roles/ that redirects to the home page (where the role picker now lives).
    Kept so external references to /roles/ don't 404."""
    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Roles · Student Ransomware Playbook</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="0; url=../#choose-role">
<link rel="canonical" href="../">
</head>
<body>
<p>The roles page has moved. <a href="../#choose-role">Choose your role on the home page</a>.</p>
<script>location.replace('../#choose-role');</script>
</body>
</html>
"""


def render_phase_section(pid: str) -> str:
    p = PHASES[pid]
    items = "".join(f"<li>{html.escape(a)}</li>" for a in p["actions"])
    return f"""
  <section class="container read" id="{pid}">
    <h2>{html.escape(p['title'])}</h2>
    <p class="lead">{html.escape(p['summary'])}</p>
    <ul>{items}</ul>
  </section>"""


def render_prevention() -> str:
    student = ROLES[0]
    items = "".join(f"<li>{html.escape(x)}</li>" for x in student['before'])
    body = f"""
  <section class="hero">
    <div class="container">
      <span class="eyebrow">Student Ransomware Playbook · Prevention</span>
      <h1>Protect <span class="accent">yourself</span></h1>
      <p class="lead">A handful of habits that make your accounts, devices, and coursework a lot harder to ransom or steal. You don't need to be technical to do any of this.</p>
    </div>
  </section>

  <section class="container">
    <div class="alert danger" role="note">
      <h4>Read this in advance, not during a live incident</h4>
      <p>This page paraphrases public guidance from <a href="https://www.cisa.gov/secureourworld">CISA Secure Our World</a>, the <a href="https://staysafeonline.org/">National Cybersecurity Alliance</a>, and <a href="https://library.educause.edu/topics/cybersecurity">EDUCAUSE</a>. It's general advice for advance reading. If something's happening right now, call campus IT from a phone or another device you trust.</p>
    </div>
  </section>

  <section class="container read">
    <h2>Do these before anything goes wrong</h2>
    <ul>{items}</ul>
  </section>

  <section class="container read">
    <h2>Phishing red flags</h2>
    <p>Most attacks on students start with a phish. An email, text, DM, or fake login page that looks real. Slow down if you see any of this:</p>
    <ul>
      <li><strong>Urgency.</strong> “Your account will be locked in 24 hours.” “Your aid will be canceled.”</li>
      <li><strong>A login link in the message.</strong> Don't click it. Type your campus URL into the browser yourself.</li>
      <li><strong>A sender domain that's close but not exact</strong> (like <code>support@my-college.edu.help</code> instead of <code>support@my-college.edu</code>).</li>
      <li><strong>Unexpected attachments.</strong> Especially zip files, OneNote files, or HTML “invoices.”</li>
      <li><strong>An offer that's too good to be true.</strong> High-paying remote job for a student, scholarship you never applied for, free laptop, surprise refund.</li>
      <li><strong>MFA prompts you didn't trigger.</strong> Never approve a prompt you didn't start. Repeated prompts are <a href="glossary.html#mfa-fatigue">MFA fatigue</a>. It's a known attack.</li>
    </ul>
    <div class="alert">
      <h4>And sometimes there are no red flags.</h4>
      <p>A real account from someone you actually know — a friend, a professor, your RA, the campus help desk — can be compromised and used to send phishing. Same name, same email address, normal-looking signature. The message will <em>look</em> legitimate because, technically, it is. If a message asks you to click a link, log in somewhere, pay something, share an MFA code, or move money, treat the <em>request</em> with suspicion — not just the sender. Verify out-of-band: text or call the person on a number you already had, or walk over.</p>
    </div>
  </section>
"""
    return page("Protect yourself", body, depth=0, description="Plain-language steps students can take to prevent ransomware and account takeover.")


def render_response() -> str:
    student = ROLES[0]
    during_items = "".join(f"<li>{html.escape(x)}</li>" for x in student['during'])
    after_items = "".join(f"<li>{html.escape(x)}</li>" for x in student['after'])
    tree_json = html.escape(json.dumps(DECISION_TREES['student']), quote=False)
    body = f"""
  <section class="hero">
    <div class="container">
      <span class="eyebrow">Student Ransomware Playbook · Response</span>
      <h1>If something <span class="accent">goes wrong</span></h1>
      <p class="lead">What to do if you think you've been hit with ransomware, phishing, or an account takeover. Read it before you need it.</p>
    </div>
  </section>

  <section class="container">
    <div class="alert danger" role="note">
      <h4>Read this in advance, not during a live incident</h4>
      <p>If something's happening right now, <strong>call your campus IT help desk</strong> from a phone or another device you trust, and do what they say. In the U.S. you can also report to <a href="https://www.cisa.gov/stopransomware/report-ransomware">CISA</a> and the <a href="https://www.ic3.gov/">FBI IC3</a>. This page is general educational material, not professional incident-response advice.</p>
    </div>
  </section>

  <section class="container read">
    <h2>In the moment</h2>
    <ul>{during_items}</ul>
  </section>

  <section class="container">
    <h2>What should I do right now?</h2>
    <p>A short decision tree for the situations students actually run into.</p>
    <div class="decision" data-decision-id="student-decision">
      <p class="breadcrumbs"></p>
      <p class="question"></p>
      <div class="choices"></div>
      <div class="result" hidden></div>
      <script type="application/json">{tree_json}</script>
    </div>
  </section>

  <section class="container read">
    <h2>After the dust settles</h2>
    <ul>{after_items}</ul>
  </section>
"""
    return page("If something goes wrong", body, depth=0, description="Student-focused guidance on what to do during and after a ransomware or phishing incident.")


def render_emergency() -> str:
    body = """
  <section class="hero">
    <div class="container">
      <span class="eyebrow">Student Ransomware Playbook · Response</span>
      <h1>If an incident <span class="accent">occurs</span></h1>
      <p class="lead">A summary of what public guidance says people on a college campus should do if they face a ransomware incident. Read it before you need it. It's not for use during a live incident.</p>
    </div>
  </section>

  <section class="container read">
    <div class="alert danger" role="note">
      <h4>This is not a real-time incident-response service</h4>
      <p>If you believe an incident is happening right now, <strong>contact your campus IT or information-security team immediately</strong> using a phone or a known-good device. In the United States, public reporting and assistance are also available from the U.S. Cybersecurity &amp; Infrastructure Security Agency at <a href="https://www.cisa.gov/stopransomware/report-ransomware">cisa.gov/stopransomware/report-ransomware</a> and the FBI Internet Crime Complaint Center at <a href="https://www.ic3.gov/">ic3.gov</a>.</p>
      <p>This page summarizes published guidance from sources such as <a href="https://www.nist.gov/news-events/news/2025/04/nist-revises-sp-800-61-incident-response-recommendations-and-considerations">NIST SP 800-61r3</a>, <a href="https://www.cisa.gov/stopransomware">CISA #StopRansomware</a>, and <a href="https://www.ic3.gov/">FBI IC3</a>. It is not professional incident-response advice and is not a substitute for trained responders, qualified counsel, or your institution’s policies and contracts.</p>
    </div>

    <h2>What public guidance generally recommends</h2>
    <p class="muted">The items below paraphrase guidance from CISA, NIST, and the FBI. Your institution’s policies, contracts, insurance terms, and applicable law take precedence.</p>

    <div class="alert">
      <h4>If a ransom note, mass file renames, or unavailable files are reported</h4>
      <ol>
        <li>CISA and the FBI generally recommend disconnecting affected devices from the network (Wi-Fi off, Ethernet unplugged) rather than powering them off, to preserve evidence in memory.</li>
        <li>Public guidance recommends not deleting the ransom note, files, or related emails, since they may be needed for investigation and potential decryption.</li>
        <li>Authoritative sources advise contacting your IT or security team using a separate phone or device, not the affected one.</li>
        <li>CISA and the FBI recommend against paying or negotiating with attackers on your own, and against downloading “decryption” tools from web search results.</li>
      </ol>
    </div>

    <div class="alert">
      <h4>If a person reports clicking a phishing link or entering credentials</h4>
      <ol>
        <li>Most published guidance recommends moving to a different, known-good device.</li>
        <li>It generally recommends changing the affected password, reviewing account recovery information, and reporting the message to IT/security.</li>
        <li>Sources advise preserving the original message as evidence rather than deleting it.</li>
      </ol>
    </div>

    <div class="alert">
      <h4>If a department leader sees a system become unavailable</h4>
      <ol>
        <li>Public guidance commonly recommends pausing sensitive workflows (payments, banking changes, sensitive data exports) until IT/security confirms it is safe to resume.</li>
        <li>Sources recommend using pre-arranged out-of-band contact lists (printed or phone-stored) rather than potentially affected systems.</li>
        <li>They also recommend waiting for official guidance before making public statements and ignoring unverified rumors.</li>
      </ol>
    </div>

    <div class="alert">
      <h4>What incident-response teams typically do (background reading only)</h4>
      <p class="muted">For pre-incident familiarity. Actual response should be led by trained personnel and qualified counsel, following your institution's plan.</p>
      <ol>
        <li>NIST SP 800-61r3 describes triggering the documented IR plan and coordinating through an out-of-band channel.</li>
        <li>CISA #StopRansomware describes isolating affected network segments, disabling compromised identities, and revoking sessions and tokens.</li>
        <li>Both sources describe preserving evidence (e.g., memory and disk images) before reimaging where feasible.</li>
        <li>Most guidance describes engaging legal counsel, the cyber-insurance hotline, and law enforcement. In the U.S., that's <a href="https://www.cisa.gov/stopransomware/report-ransomware">CISA</a> and <a href="https://www.ic3.gov/">FBI IC3</a>.</li>
        <li>It also describes coordinating with communications on cadence and channels and keeping a written timeline of decisions.</li>
      </ol>
    </div>

    <h2>By role: background reading</h2>
    <p>Each role page summarizes what published guidance says that role might do before, during, and after an incident. These are educational summaries for planning, not live-incident instructions.</p>
    <ul>
""" + "".join(f'      <li><a href="roles/{r["id"]}.html#during"><strong>{html.escape(r["label"])}</strong></a>: during-incident background reading</li>\n' for r in ROLES) + """    </ul>
  </section>
"""
    return page("If an incident occurs", body, depth=0, description="Educational summary of public guidance from CISA, NIST, and the FBI on what to do during a ransomware incident on campus. Not for live-incident use.")


def render_readiness() -> str:
    student = ROLES[0]
    chk_html = "".join(
        f'<li><input type="checkbox"><label>{html.escape(x)}</label></li>'
        for x in student["checklist_items"]
    )
    body = f"""
  <section class="hero">
    <div class="container">
      <span class="eyebrow">Student Ransomware Playbook · Readiness</span>
      <h1>Quick <span class="accent">checklist</span></h1>
      <p class="lead">A short self-audit. Check things off as you go. Progress saves on this device only. No accounts, no servers.</p>
    </div>
  </section>

  <section class="container">
    <div class="checklist" data-checklist-id="student-readiness">
      <h3>{html.escape(student['checklist_title'])} <span class="badge-earned" data-role="badge" hidden>Complete</span></h3>
      <p class="muted" data-role="counter">0 of {len(student['checklist_items'])} complete</p>
      <div class="progress" aria-hidden="true"><span></span></div>
      <ul>
        {chk_html}
      </ul>
      <div class="actions">
        <button class="btn btn-secondary btn-sm" data-action="reset" type="button">Reset</button>
      </div>
    </div>
  </section>

"""
    return page("Checklist", body, depth=0, description="A short self-audit checklist for college and university students.")


def render_glossary() -> str:
    items = "".join(
        f"<dt><strong>{html.escape(term)}</strong></dt><dd>{html.escape(defn)}</dd>"
        for term, defn in GLOSSARY
    )
    body = f"""
  <section class="container read">
    <span class="eyebrow">Student Ransomware Playbook · Reference</span>
    <h1><span class="accent">Glossary</span></h1>
    <p class="lead">Plain-language definitions for the terms in this playbook.</p>
    <dl>{items}</dl>
  </section>
"""
    return page("Glossary", body, depth=0, description="Glossary of ransomware and incident-response terms used in the playbook.")


def render_faq() -> str:
    items = "".join(
        f"<details><summary><strong>{html.escape(q)}</strong></summary><p>{html.escape(a)}</p></details>"
        for q, a in FAQ
    )
    body = f"""
  <section class="container read">
    <span class="eyebrow">Student Ransomware Playbook · Reference</span>
    <h1>Frequently asked <span class="accent">questions</span></h1>
    <p class="lead">Short answers to the questions students actually ask about ransomware, phishing, and account safety.</p>
    {items}
  </section>
"""
    return page("FAQ", body, depth=0, description="Frequently asked questions for college and university students about ransomware, phishing, and account safety.")


def render_references() -> str:
    items = "".join(
        f'<li><a href="{url}">{html.escape(title)}</a>. {html.escape(blurb)}</li>'
        for title, url, blurb in REFERENCES
    )
    body = f"""
  <section class="container read">
    <span class="eyebrow">Student Ransomware Playbook · Reference</span>
    <h1>Sources &amp; <span class="accent">further reading</span></h1>
    <p class="lead">The sources we use to keep this playbook current.</p>
    <ul>{items}</ul>
    <p class="muted">We review this list every quarter. If something's missing, suggest it on <a href="https://github.com/crimconsortium/student-ransomware-playbook/issues">GitHub Issues</a>.</p>
  </section>
"""
    return page("References", body, depth=0, description="Curated sources and further reading.")


def render_404() -> str:
    body = """
  <section class="container read">
    <h1>Page not found</h1>
    <p>That page isn't here. Try one of these:</p>
    <ul>
      <li><a href="/student-ransomware-playbook/">Home</a></li>
      <li><a href="/student-ransomware-playbook/prevention.html">Protect yourself</a></li>
      <li><a href="/student-ransomware-playbook/response.html">If something goes wrong</a></li>
      <li><a href="/student-ransomware-playbook/glossary.html">Glossary</a></li>
    </ul>
  </section>
"""
    return page("Not found", body, depth=0)


# ---------- Drills (merged Dorm Lab + Scenarios) ------------------------
# Each hotspot in the SVG and in the tile grid has data-hotspot="<key>" matching
# the LAB module's "hotspot" field. Coordinates here are tuned to the 1000x600
# viewBox below; the dorm scene is drawn flat using the strict orange/black/gray
# palette only.
HOTSPOT_GEOMETRY = {
    # key:        (cx, cy, label)
    # Coordinates are tuned to the 1000x600 viewBox of _dorm_svg().
    # roommate's desk on the left, student's desk on the right, with a
    # small stand between them holding the Wi-Fi router on top and the
    # printer on a lower shelf. Posters are on the back wall above.
    "campusemail":(565, 120, "Campus email"),
    "clubaccount":(860, 130, "Club account"),
    "clouddrive": (707, 120, "Cloud drive"),
    "roommate":   (205, 325, "Roommate's PC"),
    "router":     (510, 415, "Wi-Fi router"),
    "printer":    (510, 478, "Printer"),
    "laptop":     (735, 355, "Laptop"),
    "usbstick":   (658, 423, "USB stick"),
    "phone":      (831, 427, "Phone"),
}


def _dorm_svg() -> str:
    """Return inline SVG of a richer dorm-room scene with clickable hotspots.

    Uses the strict palette (orange #f68212, black, white, grays) plus
    light-mode shading via explicit grays. Dark-mode treatment is handled
    in CSS via the .lab-svg.dark filter scope. Each hotspot is an <a> with
    data-hotspot="<key>" so the JS engine treats clicks the same as the
    tile grid below.
    """
    # Hotspots are drawn last, on top of everything.
    dots = []
    for key, (cx, cy, label) in HOTSPOT_GEOMETRY.items():
        dots.append(
            f'<a class="lab-hotspot" href="#lab" data-hotspot="{key}" role="button" '
            f'aria-label="Open module: {html.escape(label)}" tabindex="0">'
            f'<circle cx="{cx}" cy="{cy}" r="24" class="lab-hotspot-ring"/>'
            f'<circle cx="{cx}" cy="{cy}" r="10" class="lab-hotspot-dot"/>'
            f'<text x="{cx}" y="{cy + 46}" text-anchor="middle" class="lab-hotspot-label">{html.escape(label)}</text>'
            f'</a>'
        )
    hotspots = "".join(dots)
    # The scene is drawn in layers:
    #   1. back wall + floor (with perspective-y baseboard)
    #   2. wall fixtures (window with daylight, posters, whiteboard, shelf w/ router)
    #   3. left wall furniture (roommate's desk + PC + monitor + chair)
    #   4. center desk (with laptop, USB stick, phone, mug, books, lamp w/ glow)
    #   5. bed along the right wall with pillows + blanket
    #   6. right-side TV stand with console + screen + dresser w/ printer
    #   7. rug on the floor
    #   8. hotspots (on top of everything)
    return f'''<svg class="lab-svg" viewBox="0 0 1000 600" role="img" aria-label="Illustrated dorm room with clickable items" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="lab-wall-grad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#f7f4ef"/>
      <stop offset="100%" stop-color="#ece6dc"/>
    </linearGradient>
    <linearGradient id="lab-floor-grad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#cfc4b3"/>
      <stop offset="100%" stop-color="#b8ac98"/>
    </linearGradient>
    <linearGradient id="lab-window-grad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffe5b8"/>
      <stop offset="100%" stop-color="#ffd08a"/>
    </linearGradient>
    <radialGradient id="lab-sunbeam" cx="0.5" cy="0" r="0.9">
      <stop offset="0%" stop-color="#ffe5b8" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#ffe5b8" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="lab-lamp-glow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0%" stop-color="#ffd99a" stop-opacity="0.9"/>
      <stop offset="60%" stop-color="#ffd99a" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#ffd99a" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="lab-rug-grad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#f68212" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="#d96c08" stop-opacity="0.85"/>
    </linearGradient>
    <linearGradient id="lab-blanket-grad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#f68212"/>
      <stop offset="100%" stop-color="#c45a00"/>
    </linearGradient>
  </defs>

  <!-- 1. WALL + FLOOR -->
  <rect x="0" y="0" width="1000" height="440" fill="url(#lab-wall-grad)"/>
  <rect x="0" y="440" width="1000" height="160" fill="url(#lab-floor-grad)"/>
  <!-- baseboard -->
  <rect x="0" y="430" width="1000" height="12" fill="#9b8f7c"/>
  <line x1="0" y1="442" x2="1000" y2="442" stroke="#7a6d59" stroke-width="1.2"/>
  <!-- floor planks (subtle) -->
  <g stroke="#a3957f" stroke-width="0.8" opacity="0.55">
    <line x1="0" y1="475" x2="1000" y2="475"/>
    <line x1="0" y1="510" x2="1000" y2="510"/>
    <line x1="0" y1="545" x2="1000" y2="545"/>
    <line x1="0" y1="580" x2="1000" y2="580"/>
  </g>

  <!-- 2. WINDOW with daylight + sunbeam on floor -->
  <rect x="260" y="40" width="220" height="160" fill="#3a3a3a"/>
  <rect x="268" y="48" width="204" height="144" fill="url(#lab-window-grad)"/>
  <line x1="370" y1="48" x2="370" y2="192" stroke="#3a3a3a" stroke-width="4"/>
  <line x1="268" y1="120" x2="472" y2="120" stroke="#3a3a3a" stroke-width="4"/>
  <!-- sill -->
  <rect x="252" y="196" width="236" height="12" fill="#7a6d59"/>
  <line x1="252" y1="208" x2="488" y2="208" stroke="#5a4f3e" stroke-width="1"/>
  <!-- sunbeam falling across the room -->
  <polygon points="285,200 455,200 600,470 220,470" fill="url(#lab-sunbeam)"/>

  <!-- (Router moved to the center stand between the desks; back wall stays clean.) -->

  <!-- Posters on back wall -->
  <!-- EMAIL poster (right of window, above main desk) -->
  <g>
    <rect x="490" y="60" width="150" height="115" fill="#fff" stroke="#3a3a3a" stroke-width="2"/>
    <rect x="490" y="60" width="150" height="22" fill="#f68212"/>
    <text x="565" y="77" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="700" fill="#fff" letter-spacing="0.1em">CAMPUS EMAIL</text>
    <!-- envelope motif -->
    <rect x="515" y="100" width="100" height="55" fill="#f3ede2" stroke="#3a3a3a" stroke-width="1.5"/>
    <polyline points="515,100 565,138 615,100" fill="none" stroke="#3a3a3a" stroke-width="1.5"/>
  </g>
  <!-- Cloud drive poster (between email poster and whiteboard) -->
  <g>
    <rect x="655" y="65" width="105" height="110" fill="#fff" stroke="#3a3a3a" stroke-width="2" transform="rotate(-3 707 120)"/>
    <g transform="rotate(-3 707 120)">
      <text x="707" y="100" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="700" fill="#3a3a3a" letter-spacing="0.08em">CLOUD DRIVE</text>
      <!-- cloud shape -->
      <path d="M 668,140 q 0,-22 22,-22 q 4,-13 18,-13 q 14,0 18,13 q 22,0 22,22 q 0,13 -22,13 l -40,0 q -18,0 -18,-13 z" fill="#f3ede2" stroke="#3a3a3a" stroke-width="1.5"/>
    </g>
  </g>
  <!-- Club account whiteboard (top right) -->
  <g>
    <rect x="770" y="60" width="180" height="140" fill="#fff" stroke="#3a3a3a" stroke-width="3"/>
    <rect x="770" y="60" width="180" height="6" fill="#7a6d59"/>
    <rect x="770" y="194" width="180" height="6" fill="#7a6d59"/>
    <text x="860" y="95" text-anchor="middle" font-family="sans-serif" font-size="15" font-weight="700" fill="#f68212" letter-spacing="0.08em">CLUB ACCOUNT</text>
    <line x1="790" y1="115" x2="930" y2="115" stroke="#3a3a3a" stroke-width="1.2"/>
    <text x="800" y="135" font-family="sans-serif" font-size="11" fill="#3a3a3a">Treasurer: Sam</text>
    <text x="800" y="152" font-family="sans-serif" font-size="11" fill="#3a3a3a">Pres: Alex</text>
    <text x="800" y="169" font-family="sans-serif" font-size="11" fill="#3a3a3a">Drive: shared</text>
    <text x="800" y="186" font-family="sans-serif" font-size="11" fill="#3a3a3a">Meet: Thu 7pm</text>
  </g>

  <!-- 3. ROOMMATE'S DESK (left) -->
  <!-- desk top -->
  <rect x="30" y="380" width="410" height="16" fill="#7a6d59"/>
  <rect x="30" y="396" width="410" height="4" fill="#5a4f3e"/>
  <!-- legs -->
  <rect x="40" y="396" width="12" height="100" fill="#5a4f3e"/>
  <rect x="418" y="396" width="12" height="100" fill="#5a4f3e"/>
  <!-- monitor (off, shows a small label) -->
  <rect x="130" y="275" width="150" height="100" rx="5" fill="#1a1a1a"/>
  <rect x="138" y="283" width="134" height="84" fill="#222"/>
  <text x="205" y="330" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#f68212" font-weight="700">ROOMMATE</text>
  <!-- monitor stand -->
  <rect x="195" y="375" width="22" height="8" fill="#222"/>
  <!-- tower beside the desk -->
  <rect x="55" y="395" width="42" height="105" rx="3" fill="#2b2b2b"/>
  <circle cx="76" cy="410" r="4" fill="#f68212"/>
  <rect x="65" y="420" width="22" height="3" fill="#444"/>
  <rect x="65" y="427" width="22" height="3" fill="#444"/>
  <!-- keyboard on the desk -->
  <rect x="155" y="384" width="130" height="10" rx="2" fill="#444"/>
  <!-- mouse -->
  <ellipse cx="305" cy="388" rx="8" ry="5" fill="#444"/>
  <!-- chair (tucked under) -->
  <rect x="180" y="445" width="80" height="55" rx="6" fill="#3a3a3a"/>
  <rect x="212" y="500" width="16" height="40" fill="#222"/>
  <rect x="185" y="540" width="70" height="6" fill="#222"/>

  <!-- 4. CENTER STAND between the two desks (Wi-Fi router on top, printer on lower shelf) -->
  <!-- back panel -->
  <rect x="462" y="360" width="96" height="180" fill="#7a6d59"/>
  <!-- top edge highlight -->
  <rect x="462" y="360" width="96" height="4" fill="#5a4f3e"/>
  <!-- side shadows -->
  <rect x="462" y="360" width="4" height="180" fill="#5a4f3e"/>
  <rect x="554" y="360" width="4" height="180" fill="#5a4f3e"/>
  <!-- middle shelf line -->
  <rect x="462" y="445" width="96" height="4" fill="#5a4f3e"/>
  <!-- bottom edge -->
  <rect x="462" y="536" width="96" height="4" fill="#3a3a3a"/>
  <!-- ROUTER on top shelf -->
  <rect x="472" y="395" width="76" height="40" rx="5" fill="#222"/>
  <rect x="477" y="400" width="66" height="3" fill="#f68212"/>
  <circle cx="487" cy="425" r="3" fill="#f68212"/>
  <circle cx="499" cy="425" r="3" fill="#f68212" opacity="0.7"/>
  <circle cx="511" cy="425" r="3" fill="#f68212" opacity="0.4"/>
  <!-- router antennas -->
  <line x1="482" y1="395" x2="472" y2="362" stroke="#222" stroke-width="3"/>
  <line x1="538" y1="395" x2="548" y2="362" stroke="#222" stroke-width="3"/>
  <circle cx="472" cy="362" r="3" fill="#222"/>
  <circle cx="548" cy="362" r="3" fill="#222"/>
  <!-- PRINTER on lower shelf -->
  <rect x="472" y="460" width="76" height="38" rx="4" fill="#cfc4b3" stroke="#3a3a3a" stroke-width="1.5"/>
  <rect x="478" y="472" width="64" height="6" fill="#fff" stroke="#3a3a3a" stroke-width="1"/>
  <rect x="478" y="464" width="22" height="3" fill="#222"/>
  <circle cx="540" cy="466" r="2.5" fill="#f68212"/>

  <!-- 5. STUDENT'S DESK (right) -->
  <rect x="580" y="395" width="380" height="16" fill="#7a6d59"/>
  <rect x="580" y="411" width="380" height="4" fill="#5a4f3e"/>
  <!-- drawer -->
  <rect x="590" y="415" width="360" height="22" fill="#6a5e4a"/>
  <circle cx="770" cy="426" r="3" fill="#3a3a3a"/>
  <!-- legs -->
  <rect x="590" y="415" width="12" height="85" fill="#5a4f3e"/>
  <rect x="938" y="415" width="12" height="85" fill="#5a4f3e"/>
  <!-- lamp on left side of student's desk -->
  <line x1="610" y1="395" x2="610" y2="330" stroke="#3a3a3a" stroke-width="4"/>
  <line x1="610" y1="330" x2="642" y2="310" stroke="#3a3a3a" stroke-width="4"/>
  <polygon points="632,305 664,305 668,330 628,330" fill="#3a3a3a"/>
  <!-- lamp glow -->
  <ellipse cx="650" cy="345" rx="75" ry="55" fill="url(#lab-lamp-glow)"/>
  <!-- mug -->
  <rect x="618" y="370" width="22" height="26" rx="3" fill="#f68212"/>
  <path d="M 640,375 q 8,0 8,8 q 0,8 -8,8" fill="none" stroke="#f68212" stroke-width="3"/>
  <!-- stack of books on right side -->
  <rect x="890" y="378" width="50" height="7" fill="#3a3a3a"/>
  <rect x="887" y="385" width="55" height="6" fill="#7a6d59"/>
  <rect x="893" y="391" width="48" height="4" fill="#f68212"/>
  <!-- LAPTOP (open, glowing screen) -->
  <polygon points="690,322 780,322 790,388 680,388" fill="#1a1a1a"/>
  <polygon points="698,328 772,328 780,382 690,382" fill="#2a2a2a"/>
  <!-- screen browser bar -->
  <rect x="695" y="332" width="82" height="9" fill="#0d0d0d"/>
  <rect x="698" y="335" width="3" height="3" fill="#f68212"/>
  <rect x="704" y="335" width="3" height="3" fill="#f68212" opacity="0.6"/>
  <rect x="710" y="335" width="3" height="3" fill="#f68212" opacity="0.3"/>
  <rect x="720" y="335" width="55" height="3" fill="#444"/>
  <!-- screen text lines -->
  <rect x="698" y="346" width="68" height="3" fill="#f68212"/>
  <rect x="698" y="353" width="55" height="3" fill="#888"/>
  <rect x="698" y="360" width="60" height="3" fill="#888"/>
  <rect x="698" y="367" width="45" height="3" fill="#888"/>
  <rect x="698" y="374" width="40" height="3" fill="#f68212"/>
  <!-- base (keyboard) -->
  <polygon points="665,388 795,388 810,400 650,400" fill="#2b2b2b"/>
  <polygon points="665,388 795,388 792,391 668,391" fill="#444"/>
  <!-- USB stick on the desk to the left of laptop -->
  <rect x="640" y="418" width="30" height="10" rx="1" fill="#f68212"/>
  <rect x="668" y="419" width="8" height="8" fill="#cfc4b3"/>
  <!-- PHONE on the desk, right of laptop, charging -->
  <rect x="810" y="415" width="42" height="24" rx="4" fill="#1a1a1a"/>
  <rect x="814" y="419" width="34" height="16" rx="1" fill="#2a2a2a"/>
  <circle cx="831" cy="427" r="4" fill="#f68212"/>
  <!-- charging cable hint -->
  <path d="M 852,427 q 30,0 30,15 q 0,15 -10,15" stroke="#444" stroke-width="2" fill="none"/>

  <!-- 6. (Console/TV stand removed; right side is just the desk.) -->

  <!-- 7. (Rug removed) -->

  <!-- 8. HOTSPOTS on top -->
  {hotspots}
</svg>'''


def render_drills() -> str:
    """Drills — temporarily unlinked stub.

    The full interactive drills page is preserved in version control but is
    not currently linked from the site while the section is under editorial
    review. This stub keeps /drills/ (and the dorm-lab.html / scenarios.html
    redirect targets pointing at it) returning a useful page instead of a 404,
    and steers visitors to the live reference material in the meantime.
    """
    body = """
  <section class="container read">
    <h1>Drills</h1>
    <p class="lead">Drills are temporarily offline while under review. We expect to bring them back after another editorial pass.</p>
    <p>In the meantime, the rest of the playbook is the reference material the drills were practising against:</p>
    <ul>
      <li><a href="response.html">If something goes wrong</a> — what to do in the first minutes if a device is locked or an account is compromised, with the response decision tree.</li>
      <li><a href="readiness.html">Checklist</a> — the short self-audit of habits worth having before anything goes wrong.</li>
      <li><a href="prevention.html">Protect yourself</a> — the day-to-day prevention guidance.</li>
      <li><a href="faq.html">FAQ</a> and <a href="glossary.html">Glossary</a> — for the questions and terms that come up most often.</li>
    </ul>
    <p class="muted">If your campus IT help desk gives you different instructions than anything you read here, follow your campus IT.</p>
  </section>
"""
    return page(
        "Drills (under review)",
        body,
        depth=0,
        description="The Student Ransomware Playbook drills section is temporarily offline while under editorial review. Use the response checklist and decision tree for guidance in the meantime.",
    )


def _render_drills_full_archived() -> str:
    """Archived full drills page renderer.

    Kept in source for easy revival when drills come back online. Not wired
    into main(). See DRILLS_FUTURE_NOTES.md for the list of changes to apply
    before republishing.
    """
    tiles = []
    for i, m in enumerate(DRILLS):
        hotspot = m.get("hotspot", "") or ""
        hotspot_attr = f' data-hotspot="{html.escape(hotspot)}"' if hotspot else ""
        tiles.append(
            f'<a class="lab-tile" href="#drill"{hotspot_attr} data-drill-id="{html.escape(m["id"])}">'
            f'<span class="lab-num" aria-hidden="true">{i+1:02d}</span>'
            f'<h3>{html.escape(m["title"])}</h3>'
            f'<p>{html.escape(m["blurb"])}</p>'
            f'<span class="lab-status" data-lab-status="{html.escape(m["id"])}" aria-hidden="true"></span>'
            f'</a>'
        )
    grid = "".join(tiles)
    payload = json.dumps(DRILLS, ensure_ascii=False)
    svg = _dorm_svg()
    n = len(DRILLS)
    body = f"""
  <section class="container read">
    <h1>Drills</h1>
    <p class="lead">Short incident rehearsals. Some are anchored in a simulated dorm room you can click around. Others are off-screen patterns — a fake login page, a too-good job offer, an MFA prompt at 2 a.m. Each one takes about a minute and ends with a short after-action review. Progress saves on this device only. No accounts, no servers.</p>
    <div class="alert">
      <h4>How this works</h4>
      <p>Click a hotspot in the dorm scene, or pick a drill from the list below. Read the setup, choose what you'd do, then go through the after-action checklist. Your overall readiness meter goes up as you finish drills and check off habits you've already built. Finish them all to unlock a printable completion certificate.</p>
    </div>
  </section>

  <section class="container">
    <div class="lab-readiness">
      <div class="lab-readiness-head">
        <strong>Overall readiness</strong>
        <span data-role="lab-readiness-pct">0%</span>
      </div>
      <div class="lab-readiness-bar" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0" data-role="lab-readiness-bar-outer">
        <span class="lab-readiness-fill" data-role="lab-readiness-fill" style="width:0%"></span>
      </div>
      <p class="muted lab-readiness-meta">
        <span data-role="lab-counter">0 of {n} drills complete</span>
        &nbsp;·&nbsp; <span data-role="lab-habit-counter">0 habits checked</span>
        &nbsp;·&nbsp; <button type="button" class="btn btn-secondary btn-sm" data-action="drills-reset">↺ Reset progress</button>
        &nbsp;<button type="button" class="btn btn-sm" data-action="drills-certificate" data-role="drills-cert-btn" aria-disabled="true" disabled>🔒 Certificate locked. Finish all {n}</button>
      </p>
    </div>
  </section>

  <section class="container">
    <h2>Click anything in the room</h2>
    <div class="lab-scene">
      {svg}
    </div>
    <p class="muted lab-scene-help">The dorm scene covers nine drills. The rest are in the list below. If the scene is hard to read on your screen, the list does the same thing.</p>
  </section>

  <section class="container">
    <h2>Or pick from the list</h2>
    <div class="lab-grid">
      {grid}
    </div>
  </section>

  <section class="container" id="drill">
    <div class="lab-runner" hidden>
      <div class="lab-runner-head">
        <button type="button" class="btn btn-secondary btn-sm" data-action="drill-close">← Back to drills</button>
        <span class="lab-runner-title" data-role="lab-title"></span>
      </div>
      <div class="lab-setup" data-role="lab-setup"></div>
      <div class="lab-question" data-role="lab-question"></div>
      <div class="lab-choices" data-role="lab-choices"></div>
      <div class="lab-outcome" data-role="lab-outcome" hidden></div>
      <div class="lab-aar" data-role="lab-aar" hidden></div>
    </div>
    <script type="application/json" id="drills-data">{payload}</script>
  </section>

  <section class="container read">
    <h2>What these drills are, and what they aren't</h2>
    <p>Every drill is built around something that's actually happened to students: a roommate clicks a sketchy link, a laptop gets encrypted before finals, a club's cloud drive starts hitting up members for money, a recruiter offers $40/hr to "process payments," an MFA prompt shows up at 2 a.m. when you didn't try to log in. The choices and the after-action checklists come from plain-language guidance: <a href="https://www.cisa.gov/stopransomware">CISA #StopRansomware</a>, <a href="https://www.cisa.gov/secureourworld">CISA Secure Our World</a>, the <a href="https://staysafeonline.org/">National Cybersecurity Alliance</a>, <a href="https://library.educause.edu/">EDUCAUSE</a>, and the <a href="https://www.ic3.gov/">FBI Internet Crime Complaint Center</a>. Nothing here tells you how to attack anything. It tells you how to recognize and respond.</p>
    <p>This is a simulation. Whatever your campus IT help desk says, that wins.</p>
  </section>
"""
    return page(
        "Drills",
        body,
        depth=0,
        description="Short incident drills for college and university students. Practice phishing, MFA fatigue, ransomware on a personal laptop, fake job offers, financial-aid scams, account takeover of a club's cloud drive, lost devices, and more — with feedback on every choice.",
    )


# ============================================================================
# /verify/ subtree -- per-claim citation view of the live site.
# ----------------------------------------------------------------------------
# Renders the same content as the main site, but with an inline citation
# marker after every sentence: a numbered superscript for sourced factual
# claims, or a small [guidance] / [authority: NAME] tag for directive or
# attributed sentences. Footnotes are listed at the bottom of each page.
# ============================================================================
import re as _re

_SENT_SPLIT = _re.compile(r'(?<=[.!?])(?:"|\u201d)?\s+(?=[A-Z“"—])')


def _split_sentences(text: str) -> list[str]:
    """Split prose into sentences for citation pairing.

    Conservative: splits on '.', '!', or '?' followed by whitespace and a
    capital letter (or opening quote/em-dash). Acronyms, abbreviations, and
    "e.g."-style cases are largely preserved because they aren't followed by
    a capitalized word.
    """
    text = text.strip()
    if not text:
        return []
    parts = _SENT_SPLIT.split(text)
    return [p.strip() for p in parts if p.strip()]


class _Footnotes:
    """Per-page footnote accumulator. Returns inline markers and the list."""

    def __init__(self) -> None:
        self._by_url: dict[str, int] = {}
        self._items: list[tuple[str, str]] = []  # (title, url) in citation order

    def cite(self, ref_key: str) -> str:
        """Return inline marker HTML for a source ref_key."""
        src = CITATION_SOURCES.get(ref_key)
        if not src:
            return f'<sup class="verify-tag verify-tag-missing" title="missing source: {html.escape(ref_key)}">[?]</sup>'
        title, url = src
        if url not in self._by_url:
            self._items.append((title, url))
            self._by_url[url] = len(self._items)
        n = self._by_url[url]
        return (
            f'<sup class="verify-cite"><a href="#fn-{n}" id="fnref-{n}-{len(self._by_url)}" '
            f'title="{html.escape(title)}">[{n}]</a></sup>'
        )

    def render(self) -> str:
        if not self._items:
            return ''
        rows = ''.join(
            f'<li id="fn-{i+1}"><a href="{html.escape(url)}">{html.escape(title)}</a></li>'
            for i, (title, url) in enumerate(self._items)
        )
        return (
            '<section class="container read verify-footnotes">\n'
            '<h2>Sources</h2>\n'
            '<ol>' + rows + '</ol>\n'
            '<p class="muted">Every numbered citation above resolves to a public source. '
            'Sentences marked <span class="verify-tag verify-tag-guidance">[guidance]</span> '
            'are general directive advice. Sentences marked '
            '<span class="verify-tag verify-tag-authority">[authority]</span> are '
            'recommendations attributed to a named authority.</p>\n'
            '</section>\n'
        )


def _tag(kind: str, name: str = '') -> str:
    if kind == 'guidance':
        return '<sup class="verify-tag verify-tag-guidance">[guidance]</sup>'
    if kind == 'authority':
        return f'<sup class="verify-tag verify-tag-authority">[authority: {html.escape(name)}]</sup>'
    return ''


def _annotate(text: str, key: str, fn: _Footnotes) -> str:
    """Return text with an inline citation marker after each sentence.

    The marker comes from CITATIONS[key] (positional). Missing entries default
    to [guidance]. The original text is preserved verbatim; markers are
    appended after each sentence boundary.
    """
    sentences = _split_sentences(text)
    if not sentences:
        return ''
    cite_list = CITATIONS.get(key, [])
    out_parts = []
    for i, sent in enumerate(sentences):
        entry = cite_list[i] if i < len(cite_list) else {'kind': 'guidance'}
        if 'src' in entry:
            marker = fn.cite(entry['src'])
        else:
            marker = _tag(entry.get('kind', 'guidance'), entry.get('name', ''))
        out_parts.append(html.escape(sent) + ' ' + marker)
    return ' '.join(out_parts)


def _verify_page(title: str, body: str, *, description: str = '') -> str:
    """Wrap a verify-view body in the standard site chrome at depth=1."""
    return page(title, body, depth=1, description=description)


# ---- Verify renderers (one per live-site page that has prose to cite) ------

def render_verify_index() -> str:
    body = '''
  <section class="hero">
    <div class="container">
      <span class="eyebrow">Student Ransomware Playbook · Verify</span>
      <h1>Citation <span class="accent">view</span></h1>
      <p class="lead">A side-by-side of the playbook with every claim tagged. Numbered superscripts link to public sources; sentences marked <span class="verify-tag verify-tag-guidance">[guidance]</span> are directive advice; sentences marked <span class="verify-tag verify-tag-authority">[authority: …]</span> are recommendations attributed to a named authority.</p>
    </div>
  </section>

  <section class="container read">
    <h2>Pages</h2>
    <ul>
      <li><a href="prevention.html">Protect yourself</a></li>
      <li><a href="response.html">If something goes wrong</a></li>
      <li><a href="readiness.html">Quick checklist</a></li>
      <li><a href="faq.html">FAQ</a></li>
      <li><a href="glossary.html">Glossary</a></li>
      <li><a href="references.html">Sources &amp; further reading</a></li>
    </ul>
  </section>

  <section class="container read">
    <h2>What this is</h2>
    <p>The citation view exists so anyone can verify the claims on the main site against public sources. It is generated from the same content as the live playbook, so the two cannot drift. The source bar is: CISA, FBI/IC3, NIST, EDUCAUSE, the National Cybersecurity Alliance, named university Information Security Offices, peer-reviewed research, and named journalism. No vendor marketing unless it is the original source of a specific data point.</p>
    <p>If you find a claim you think is wrong, file an issue on <a href="https://github.com/crimconsortium/student-ransomware-playbook/issues">GitHub</a>.</p>
  </section>
'''
    return _verify_page(
        'Citation view',
        body,
        description='Citation view of the Student Ransomware Playbook — every factual sentence linked to a public source.',
    )


def render_verify_prevention() -> str:
    fn = _Footnotes()
    student = ROLES[0]

    # Annotate the BEFORE list (one citation key per item).
    items_html = ''
    for i, item in enumerate(student['before']):
        items_html += '<li>' + _annotate(item, f'role.student.before.{i}', fn) + '</li>'

    # Reusable bits from the live page, with the same prose and inline annotations.
    lead_html = _annotate(
        'A handful of habits that make your accounts, devices, and coursework a lot harder to ransom or steal. You don\'t need to be technical to do any of this.',
        'page.prevention.lead', fn,
    )
    alert_html = _annotate(
        "This page paraphrases public guidance from CISA Secure Our World, the National Cybersecurity Alliance, and EDUCAUSE. It's general advice for advance reading. If something's happening right now, call campus IT from a phone or another device you trust.",
        'page.prevention.alert', fn,
    )

    redflag_intro = _annotate(
        "Most attacks on students start with a phish. An email, text, DM, or fake login page that looks real. Slow down if you see any of this:",
        'page.prevention.redflags.intro', fn,
    )
    redflag_items = ''
    for key, text in [
        ('page.prevention.redflag.urgency',     '"Your account will be locked in 24 hours." "Your aid will be canceled."'),
        ('page.prevention.redflag.link',        "A login link in the message. Don't click it. Type your campus URL into the browser yourself."),
        ('page.prevention.redflag.domain',      "A sender domain that's close but not exact (like support@my-college.edu.help instead of support@my-college.edu)."),
        ('page.prevention.redflag.attachments', 'Unexpected attachments. Especially zip files, OneNote files, or HTML "invoices."'),
        ('page.prevention.redflag.toogood',     "An offer that's too good to be true. High-paying remote job for a student, scholarship you never applied for, free laptop, surprise refund."),
        ('page.prevention.redflag.mfa',         "MFA prompts you didn't trigger. Never approve a prompt you didn't start. Repeated prompts are MFA fatigue. It's a known attack."),
    ]:
        redflag_items += '<li>' + _annotate(text, key, fn) + '</li>'

    noflag_html = _annotate(
        "A real account from someone you actually know — a friend, a professor, your RA, the campus help desk — can be compromised and used to send phishing. Same name, same email address, normal-looking signature. The message will look legitimate because, technically, it is. If a message asks you to click a link, log in somewhere, pay something, share an MFA code, or move money, treat the request with suspicion — not just the sender. Verify out-of-band: text or call the person on a number you already had, or walk over.",
        'page.prevention.noflag.0', fn,
    )

    body = f'''
  <section class="hero">
    <div class="container">
      <span class="eyebrow">Student Ransomware Playbook · Verify · Prevention</span>
      <h1>Protect yourself — <span class="accent">citation view</span></h1>
      <p class="lead">{lead_html}</p>
      <p class="muted"><a href="../prevention.html">Plain view →</a></p>
    </div>
  </section>

  <section class="container read">
    <div class="alert"><p>{alert_html}</p></div>
  </section>

  <section class="container read">
    <h2>Do these before anything goes wrong</h2>
    <ul>{items_html}</ul>
  </section>

  <section class="container read">
    <h2>Phishing red flags</h2>
    <p>{redflag_intro}</p>
    <ul>{redflag_items}</ul>
    <div class="alert"><h4>And sometimes there are no red flags.</h4><p>{noflag_html}</p></div>
  </section>

  {fn.render()}
'''
    return _verify_page('Protect yourself (citation view)', body)


def render_verify_response() -> str:
    fn = _Footnotes()
    student = ROLES[0]

    during_html = ''
    for i, item in enumerate(student['during']):
        during_html += '<li>' + _annotate(item, f'role.student.during.{i}', fn) + '</li>'
    after_html = ''
    for i, item in enumerate(student['after']):
        after_html += '<li>' + _annotate(item, f'role.student.after.{i}', fn) + '</li>'

    lead_html = _annotate(
        "What to do if you think you've been hit with ransomware, phishing, or an account takeover. Read it before you need it.",
        'page.response.lead', fn,
    )
    alert_html = _annotate(
        "If something's happening right now, call your campus IT help desk from a phone or another device you trust, and do what they say. In the U.S. you can also report to CISA and the FBI IC3. This page is general educational material, not professional incident-response advice.",
        'page.response.alert', fn,
    )
    tree_intro = _annotate(
        'A short decision tree for the situations students actually run into.',
        'page.response.decisiontree.intro', fn,
    )

    body = f'''
  <section class="hero">
    <div class="container">
      <span class="eyebrow">Student Ransomware Playbook · Verify · Response</span>
      <h1>If something goes wrong — <span class="accent">citation view</span></h1>
      <p class="lead">{lead_html}</p>
      <p class="muted"><a href="../response.html">Plain view →</a></p>
    </div>
  </section>

  <section class="container read">
    <div class="alert"><p>{alert_html}</p></div>
  </section>

  <section class="container read">
    <h2>In the moment</h2>
    <ul>{during_html}</ul>
  </section>

  <section class="container read">
    <h2>What should I do right now?</h2>
    <p>{tree_intro}</p>
    <p class="muted">The interactive decision tree on the plain view paraphrases the disconnect-but-leave-powered-on guidance from the CISA #StopRansomware guide.</p>
  </section>

  <section class="container read">
    <h2>After the dust settles</h2>
    <ul>{after_html}</ul>
  </section>

  {fn.render()}
'''
    return _verify_page('If something goes wrong (citation view)', body)


def render_verify_readiness() -> str:
    fn = _Footnotes()
    student = ROLES[0]
    lead_html = _annotate(
        'A short self-audit. Check things off as you go. Progress saves on this device only. No accounts, no servers.',
        'page.readiness.lead', fn,
    )
    items_html = ''
    for i, item in enumerate(student['checklist_items']):
        items_html += '<li>' + _annotate(item, f'role.student.checklist.{i}', fn) + '</li>'

    body = f'''
  <section class="hero">
    <div class="container">
      <span class="eyebrow">Student Ransomware Playbook · Verify · Readiness</span>
      <h1>Quick checklist — <span class="accent">citation view</span></h1>
      <p class="lead">{lead_html}</p>
      <p class="muted"><a href="../readiness.html">Plain view →</a></p>
    </div>
  </section>

  <section class="container read">
    <h2>{html.escape(student["checklist_title"])}</h2>
    <ul>{items_html}</ul>
  </section>

  {fn.render()}
'''
    return _verify_page('Quick checklist (citation view)', body)


def render_verify_faq() -> str:
    fn = _Footnotes()
    lead_html = _annotate(
        'Short answers to the questions students actually ask about ransomware, phishing, and account safety.',
        'page.faq.lead', fn,
    )
    # FAQ-key mapping mirrors the order in content.FAQ.
    keys = [
        'faq.what_is_ransomware',
        'faq.why_care',
        'faq.faq_clicked',
        'faq.ransom_note',
        'faq.discipline',
        'faq.personal_device',
        'faq.mfa_worth_it',
        'faq.public_wifi',
        'faq.legal_advice',
    ]
    items = ''
    for (q, a), k in zip(FAQ, keys):
        items += (
            '<details open><summary><strong>' + html.escape(q) + '</strong></summary>'
            '<p>' + _annotate(a, k, fn) + '</p></details>'
        )

    body = f'''
  <section class="container read">
    <span class="eyebrow">Student Ransomware Playbook · Verify · FAQ</span>
    <h1>FAQ — <span class="accent">citation view</span></h1>
    <p class="lead">{lead_html}</p>
    <p class="muted"><a href="../faq.html">Plain view →</a></p>
    {items}
  </section>

  {fn.render()}
'''
    return _verify_page('FAQ (citation view)', body)


def render_verify_glossary() -> str:
    fn = _Footnotes()
    lead_html = _annotate(
        'Plain-language definitions for the terms in this playbook.',
        'page.glossary.lead', fn,
    )
    # Glossary key mapping (only entries with anything other than guidance are keyed).
    key_for_term = {
        'CISA': 'glossary.cisa',
        'FERPA': 'glossary.ferpa',
        'FIDO2 / WebAuthn': 'glossary.fido2',
        'MFA / Multi-factor authentication': 'glossary.mfa',
        'MFA fatigue': 'glossary.mfa_fatigue',
        'NIST': 'glossary.nist',
        'Third-party risk': 'glossary.thirdparty',
    }
    items = ''
    for term, defn in GLOSSARY:
        k = key_for_term.get(term, f'glossary.{term.lower()}')
        items += (
            '<dt><strong>' + html.escape(term) + '</strong></dt>'
            '<dd>' + _annotate(defn, k, fn) + '</dd>'
        )

    body = f'''
  <section class="container read">
    <span class="eyebrow">Student Ransomware Playbook · Verify · Glossary</span>
    <h1>Glossary — <span class="accent">citation view</span></h1>
    <p class="lead">{lead_html}</p>
    <p class="muted"><a href="../glossary.html">Plain view →</a></p>
    <dl>{items}</dl>
  </section>

  {fn.render()}
'''
    return _verify_page('Glossary (citation view)', body)


def render_verify_references() -> str:
    fn = _Footnotes()
    lead_html = _annotate(
        'The sources we use to keep this playbook current.',
        'page.references.lead', fn,
    )
    items = ''
    for title, url, blurb in REFERENCES:
        items += (
            '<li><a href="' + html.escape(url) + '">' + html.escape(title) + '</a>. '
            + html.escape(blurb) + ' <sup class="verify-tag verify-tag-source">[source]</sup></li>'
        )

    body = f'''
  <section class="container read">
    <span class="eyebrow">Student Ransomware Playbook · Verify · References</span>
    <h1>Sources &amp; further reading — <span class="accent">citation view</span></h1>
    <p class="lead">{lead_html}</p>
    <p class="muted"><a href="../references.html">Plain view →</a></p>
    <ul>{items}</ul>
    <p class="muted">Every entry on this page is itself a source. The other pages in the citation view link back into this list via numbered footnotes.</p>
  </section>
'''
    return _verify_page('References (citation view)', body)


def main() -> None:
    out = ROOT
    # Top-level student-focused pages only
    (out / "prevention.html").write_text(render_prevention(), encoding="utf-8")
    (out / "response.html").write_text(render_response(), encoding="utf-8")
    (out / "readiness.html").write_text(render_readiness(), encoding="utf-8")
    (out / "drills.html").write_text(render_drills(), encoding="utf-8")
    # Redirect stubs so old external links to scenarios.html / dorm-lab.html keep working.
    _redirect = (
        '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
        '<meta http-equiv="refresh" content="0; url=drills.html">'
        '<link rel="canonical" href="https://crimconsortium.github.io/student-ransomware-playbook/drills.html">'
        '<title>Moved to Drills · Student Ransomware Playbook</title>'
        '<meta name="robots" content="noindex"></head>'
        '<body><p>This page moved to <a href="drills.html">Drills</a>.</p></body></html>\n'
    )
    (out / "scenarios.html").write_text(_redirect, encoding="utf-8")
    (out / "dorm-lab.html").write_text(_redirect, encoding="utf-8")
    (out / "glossary.html").write_text(render_glossary(), encoding="utf-8")
    (out / "faq.html").write_text(render_faq(), encoding="utf-8")
    (out / "references.html").write_text(render_references(), encoding="utf-8")
    (out / "404.html").write_text(render_404(), encoding="utf-8")

    # /verify/ subtree -- per-claim citation view of every page on the live site.
    verify_dir = out / "verify"
    verify_dir.mkdir(exist_ok=True)
    (verify_dir / "index.html").write_text(render_verify_index(), encoding="utf-8")
    (verify_dir / "prevention.html").write_text(render_verify_prevention(), encoding="utf-8")
    (verify_dir / "response.html").write_text(render_verify_response(), encoding="utf-8")
    (verify_dir / "readiness.html").write_text(render_verify_readiness(), encoding="utf-8")
    (verify_dir / "faq.html").write_text(render_verify_faq(), encoding="utf-8")
    (verify_dir / "glossary.html").write_text(render_verify_glossary(), encoding="utf-8")
    (verify_dir / "references.html").write_text(render_verify_references(), encoding="utf-8")

    print("Pages built.")


if __name__ == "__main__":
    main()
