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
from content import ROLES, PHASES, GLOSSARY, FAQ, REFERENCES, SCENARIOS, LAB  # noqa: E402


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
        <li><a href="{rel}scenarios.html">Scenarios</a></li>
        <li><a href="{rel}dorm-lab.html">Dorm lab</a></li>
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
        <li><a href="{rel}scenarios.html">Scenarios</a></li>
        <li><a href="{rel}dorm-lab.html">Dorm lab</a></li>
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
      </ul>
      <p class="muted">© <span data-year></span> Joshua Gerstenfeld &amp; Scott Jacques.</p>
    </div>
  </div>
</footer>

<script src="{rel}assets/js/app.js"></script>
<script src="{rel}assets/js/scenarios.js" defer></script>
<script src="{rel}assets/js/dorm-lab.js" defer></script>
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
            "n_device_disc": {"type": "result", "title": "Stay disconnected, leave it on, call IT.",
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
         "explanation": "Long passwords help, but phishing-resistant MFA (FIDO2/WebAuthn) defeats most credential phishing because the credential is bound to the legitimate site."},
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
        <button class="btn btn-secondary btn-sm" data-action="print" type="button">Print</button>
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
<title>Roles · Campus Ransomware Playbook</title>
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
      <h1>Protect yourself</h1>
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
      <h1>If something goes wrong</h1>
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
      <h1>If an incident occurs</h1>
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
        <li>CISA, FBI, and most insurers recommend against unilaterally paying or negotiating, and against downloading “decryption” tools from web search results.</li>
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
    quiz_json = html.escape(json.dumps(QUIZZES['student']), quote=False)
    body = f"""
  <section class="hero">
    <div class="container">
      <h1>Quick checklist</h1>
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
        <button class="btn btn-secondary btn-sm" data-action="print" type="button">Print</button>
      </div>
    </div>
  </section>

  <section class="container">
    <h2>Practice scenario</h2>
    <p>One quick scenario to turn this into a reflex.</p>
    <div class="quiz" data-quiz-id="student-quiz">
      <p class="meta"></p>
      <p class="question"></p>
      <div class="options"></div>
      <div class="feedback" hidden></div>
      <script type="application/json">{quiz_json}</script>
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
    <h1>Glossary</h1>
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
    <h1>Frequently asked questions</h1>
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
    <h1>Sources &amp; further reading</h1>
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


def render_scenarios() -> str:
    """Choose-Your-Response — interactive branching scenarios for students.

    Renders a single page with an index card per scenario plus a card-shaped
    interactive ‘runner’ that mounts when the student opens a scenario.
    Engine + scoring + certificate logic lives in assets/js/scenarios.js.
    The full SCENARIOS data is embedded as JSON inside a single <script type=\"application/json\">
    tag so the page works fully offline and the build remains static.
    """
    cards = "".join(
        f'<a class="scn-tile" href="#scn" data-scn-id="{html.escape(s["id"])}">'
        f'<span class="scn-num" aria-hidden="true">{i+1:02d}</span>'
        f'<h3>{html.escape(s["title"])}</h3>'
        f'<p>{html.escape(s["blurb"])}</p>'
        f'<span class="scn-status" data-scn-status="{html.escape(s["id"])}" aria-hidden="true"></span>'
        f'</a>'
        for i, s in enumerate(SCENARIOS)
    )
    payload = json.dumps(SCENARIOS, ensure_ascii=False)
    body = f"""
  <section class="container read">
    <h1>Choose-Your-Response</h1>
    <p class="lead">Ten short, real situations students actually run into. Pick what you'd do, see what would happen, and find out why. Progress saves on this device only. No accounts, no servers.</p>
    <div class="alert">
      <h4>How this works</h4>
      <p>Each scenario takes a minute or two. Pick an option, read the outcome, retry or move on. Finish all ten and you can download a printable completion certificate.</p>
    </div>
  </section>

  <section class="container">
    <h2>Pick a scenario</h2>
    <div class="scn-grid">
      {cards}
    </div>
    <p class="scn-progress-bar" aria-live="polite">
      <span data-role="scn-counter">0 of {len(SCENARIOS)} complete</span>
      &nbsp;·&nbsp; <button type="button" class="btn btn-secondary btn-sm" data-action="scn-reset">↺ Reset progress</button>
      &nbsp;<button type="button" class="btn btn-sm" data-action="scn-certificate" data-role="scn-cert-btn" aria-disabled="true" disabled>🔒 Certificate locked. Finish all {len(SCENARIOS)}</button>
    </p>
  </section>

  <section class="container" id="scn">
    <div class="scn-runner" hidden>
      <div class="scn-runner-head">
        <button type="button" class="btn btn-secondary btn-sm" data-action="scn-close">← Back to list</button>
        <span class="scn-runner-title" data-role="scn-title"></span>
      </div>
      <div class="scn-situation" data-role="scn-situation"></div>
      <div class="scn-question" data-role="scn-question"></div>
      <div class="scn-choices" data-role="scn-choices"></div>
      <div class="scn-outcome" data-role="scn-outcome" hidden></div>
    </div>
    <script type="application/json" id="scn-data">{payload}</script>
  </section>

  <section class="container read">
    <h2>Why these ten?</h2>
    <p>Each scenario is built around a pattern that's actually hit students recently. Phishing, MFA fatigue, fake job offers, financial-aid scams, ransomware on a personal laptop, account takeover of a club's cloud drive, lost or stolen devices, social pressure to share credentials, and physical-media tricks. The choices and explanations come from public guidance: <a href="https://www.cisa.gov/stopransomware">CISA #StopRansomware</a>, <a href="https://www.cisa.gov/secureourworld">CISA Secure Our World</a>, the <a href="https://staysafeonline.org/">National Cybersecurity Alliance</a>, <a href="https://library.educause.edu/">EDUCAUSE</a>, and the <a href="https://www.ic3.gov/">FBI Internet Crime Complaint Center</a>. None of it tells you how to attack anything. It tells you how to recognize and respond.</p>
    <p>This is a simulation. Whatever your campus IT help desk says, that wins.</p>
  </section>
"""
    return page(
        "Scenarios",
        body,
        depth=0,
        description="Ten interactive branching scenarios that let college and university students practice spotting phishing, account takeover, ransomware, and common campus cyber scams, with feedback on every choice.",
    )


# ---------- Dorm Room Incident Lab --------------------------------------
# Each hotspot in the SVG and in the tile grid has data-hotspot="<key>" matching
# the LAB module's "hotspot" field. Coordinates here are tuned to the 1000x600
# viewBox below; the dorm scene is drawn flat using the strict orange/black/gray
# palette only.
HOTSPOT_GEOMETRY = {
    # key:        (cx, cy, label)
    # Coordinates are tuned to the 1000x600 viewBox of _dorm_svg().
    # New positions match the richer scene: laptop on the center desk,
    # phone next to it, console near the TV stand bottom-right, router
    # on the high shelf top-left, printer on the dresser bottom-right,
    # roommate's PC at the left wall desk, cloud drive poster above the
    # bed (right), campus email poster above the main desk (center),
    # club account whiteboard top-right, USB stick on the center desk.
    "router":     (118, 100, "Wi-Fi router"),
    "campusemail":(565, 120, "Campus email"),
    "clubaccount":(860, 130, "Club account"),
    "clouddrive": (707, 120, "Cloud drive"),
    "roommate":   (165, 320, "Roommate's PC"),
    "laptop":     (460, 360, "Laptop"),
    "usbstick":   (385, 405, "USB stick"),
    "phone":      (560, 405, "Phone"),
    "printer":    (820, 425, "Printer"),
    "console":    (855, 510, "Console"),
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

  <!-- Wi-Fi router on a shelf, top-left -->
  <!-- shelf -->
  <rect x="40" y="140" width="170" height="8" fill="#5a4f3e"/>
  <rect x="42" y="148" width="6" height="14" fill="#5a4f3e"/>
  <rect x="202" y="148" width="6" height="14" fill="#5a4f3e"/>
  <!-- router body -->
  <rect x="85" y="95" width="80" height="38" rx="5" fill="#222"/>
  <rect x="90" y="100" width="70" height="3" fill="#f68212"/>
  <circle cx="100" cy="122" r="3" fill="#f68212"/>
  <circle cx="112" cy="122" r="3" fill="#f68212" opacity="0.7"/>
  <circle cx="124" cy="122" r="3" fill="#f68212" opacity="0.4"/>
  <!-- antennas -->
  <line x1="95" y1="95" x2="75" y2="60" stroke="#222" stroke-width="3"/>
  <line x1="155" y1="95" x2="175" y2="60" stroke="#222" stroke-width="3"/>
  <circle cx="75" cy="60" r="4" fill="#222"/>
  <circle cx="175" cy="60" r="4" fill="#222"/>
  <!-- a couple of small books on the shelf -->
  <rect x="170" y="118" width="10" height="22" fill="#3a3a3a"/>
  <rect x="180" y="114" width="10" height="26" fill="#7a6d59"/>
  <rect x="190" y="120" width="10" height="20" fill="#f68212"/>

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

  <!-- 3. LEFT-WALL: Roommate's desk + monitor + tower + chair -->
  <!-- desk -->
  <rect x="30" y="340" width="230" height="14" fill="#7a6d59"/>
  <rect x="40" y="354" width="10" height="110" fill="#5a4f3e"/>
  <rect x="240" y="354" width="10" height="110" fill="#5a4f3e"/>
  <!-- monitor (off, shows a small label) -->
  <rect x="105" y="245" width="130" height="90" rx="4" fill="#1a1a1a"/>
  <rect x="112" y="252" width="116" height="76" fill="#222"/>
  <text x="170" y="295" text-anchor="middle" font-family="sans-serif" font-size="11" fill="#f68212" font-weight="700">ROOMMATE</text>
  <!-- monitor stand -->
  <rect x="160" y="335" width="20" height="8" fill="#222"/>
  <!-- tower beside the desk -->
  <rect x="40" y="360" width="40" height="95" rx="3" fill="#2b2b2b"/>
  <circle cx="60" cy="375" r="4" fill="#f68212"/>
  <rect x="50" y="385" width="20" height="3" fill="#444"/>
  <rect x="50" y="392" width="20" height="3" fill="#444"/>
  <!-- chair -->
  <rect x="125" y="395" width="70" height="60" rx="6" fill="#3a3a3a"/>
  <rect x="130" y="455" width="60" height="10" fill="#222"/>
  <rect x="155" y="465" width="10" height="30" fill="#222"/>
  <!-- keyboard on the desk -->
  <rect x="108" y="344" width="120" height="10" rx="2" fill="#444"/>

  <!-- 4. MAIN DESK (center) -->
  <rect x="310" y="395" width="410" height="18" fill="#7a6d59"/>
  <rect x="315" y="413" width="12" height="95" fill="#5a4f3e"/>
  <rect x="703" y="413" width="12" height="95" fill="#5a4f3e"/>
  <!-- desk drawer hint -->
  <rect x="335" y="413" width="360" height="22" fill="#6a5e4a"/>
  <circle cx="515" cy="424" r="3" fill="#3a3a3a"/>
  <!-- lamp on left side of desk -->
  <rect x="335" y="380" width="6" height="-50" fill="#3a3a3a"/>
  <line x1="338" y1="395" x2="338" y2="330" stroke="#3a3a3a" stroke-width="4"/>
  <line x1="338" y1="330" x2="370" y2="310" stroke="#3a3a3a" stroke-width="4"/>
  <polygon points="360,305 392,305 396,330 356,330" fill="#3a3a3a"/>
  <!-- lamp glow -->
  <ellipse cx="378" cy="345" rx="75" ry="55" fill="url(#lab-lamp-glow)"/>
  <!-- mug -->
  <rect x="345" y="370" width="22" height="26" rx="3" fill="#f68212"/>
  <path d="M 367,375 q 8,0 8,8 q 0,8 -8,8" fill="none" stroke="#f68212" stroke-width="3"/>
  <!-- stack of books -->
  <rect x="665" y="378" width="50" height="7" fill="#3a3a3a"/>
  <rect x="662" y="385" width="55" height="6" fill="#7a6d59"/>
  <rect x="668" y="391" width="48" height="4" fill="#f68212"/>
  <!-- LAPTOP (open, glowing screen) -->
  <!-- screen -->
  <polygon points="420,322 510,322 520,388 410,388" fill="#1a1a1a"/>
  <polygon points="428,328 502,328 510,382 420,382" fill="#2a2a2a"/>
  <!-- screen content: a fake browser bar in orange -->
  <rect x="425" y="332" width="82" height="9" fill="#0d0d0d"/>
  <rect x="428" y="335" width="3" height="3" fill="#f68212"/>
  <rect x="434" y="335" width="3" height="3" fill="#f68212" opacity="0.6"/>
  <rect x="440" y="335" width="3" height="3" fill="#f68212" opacity="0.3"/>
  <rect x="450" y="335" width="55" height="3" fill="#444"/>
  <!-- screen text lines -->
  <rect x="428" y="346" width="68" height="3" fill="#f68212"/>
  <rect x="428" y="353" width="55" height="3" fill="#888"/>
  <rect x="428" y="360" width="60" height="3" fill="#888"/>
  <rect x="428" y="367" width="45" height="3" fill="#888"/>
  <rect x="428" y="374" width="40" height="3" fill="#f68212"/>
  <!-- base (keyboard) -->
  <polygon points="395,388 525,388 540,400 380,400" fill="#2b2b2b"/>
  <polygon points="395,388 525,388 522,391 398,391" fill="#444"/>
  <!-- USB stick on the desk to the left of laptop -->
  <rect x="370" y="398" width="30" height="10" rx="1" fill="#f68212"/>
  <rect x="398" y="399" width="8" height="8" fill="#cfc4b3"/>
  <!-- PHONE on the desk, right of laptop, charging -->
  <rect x="540" y="395" width="42" height="24" rx="4" fill="#1a1a1a"/>
  <rect x="544" y="399" width="34" height="16" rx="1" fill="#2a2a2a"/>
  <circle cx="561" cy="407" r="4" fill="#f68212"/>
  <!-- charging cable hint -->
  <path d="M 582,407 q 30,0 30,15 q 0,15 -10,15" stroke="#444" stroke-width="2" fill="none"/>

  <!-- 5. (Bed removed; right wall is open) -->

  <!-- 6. DRESSER / PRINTER (bottom right) and TV STAND / CONSOLE -->
  <!-- Dresser/printer combo, far right -->
  <rect x="760" y="440" width="165" height="55" fill="#7a6d59"/>
  <rect x="760" y="440" width="165" height="4" fill="#5a4f3e"/>
  <!-- printer body -->
  <rect x="785" y="402" width="80" height="38" rx="4" fill="#cfc4b3" stroke="#3a3a3a" stroke-width="1.5"/>
  <rect x="790" y="414" width="70" height="6" fill="#fff" stroke="#3a3a3a" stroke-width="1"/>
  <rect x="790" y="406" width="24" height="3" fill="#222"/>
  <circle cx="855" cy="408" r="2.5" fill="#f68212"/>
  <!-- TV stand under the dresser line, left of dresser -->
  <rect x="775" y="495" width="180" height="40" fill="#5a4f3e"/>
  <rect x="775" y="495" width="180" height="4" fill="#3a3a3a"/>
  <!-- console (slim, slotted) -->
  <rect x="815" y="500" width="90" height="22" rx="3" fill="#1a1a1a"/>
  <rect x="825" y="510" width="30" height="3" fill="#3a3a3a"/>
  <circle cx="890" cy="511" r="2.5" fill="#f68212"/>

  <!-- 7. (Rug removed) -->

  <!-- 8. HOTSPOTS on top -->
  {hotspots}
</svg>'''


def render_dorm_lab() -> str:
    """Dorm Room Incident Lab — 10 short room-anchored modules.

    Single static page. SVG dorm scene shows clickable hotspots; below it,
    an accessible tile grid lists every module (used as the small-screen and
    reduced-motion fallback, and for keyboard users who prefer text targets).
    Engine, scoring, readiness meter, and per-module AAR live in
    assets/js/dorm-lab.js. Module data is embedded as JSON in a single
    <script type="application/json"> so the page is fully static.
    """
    tiles = []
    for i, m in enumerate(LAB):
        tiles.append(
            f'<a class="lab-tile" href="#lab" data-hotspot="{html.escape(m["hotspot"])}" data-lab-id="{html.escape(m["id"])}">'
            f'<span class="lab-num" aria-hidden="true">{i+1:02d}</span>'
            f'<h3>{html.escape(m["title"])}</h3>'
            f'<p>{html.escape(m["blurb"])}</p>'
            f'<span class="lab-status" data-lab-status="{html.escape(m["id"])}" aria-hidden="true"></span>'
            f'</a>'
        )
    grid = "".join(tiles)
    payload = json.dumps(LAB, ensure_ascii=False)
    svg = _dorm_svg()
    body = f"""
  <section class="container read">
    <h1>Dorm Room Incident Lab</h1>
    <p class="lead">A simulated dorm room. Click anything in the room to run a quick incident drill. Each one takes about a minute and ends with a short after-action review. Progress saves on this device only. No accounts, no servers.</p>
    <div class="alert">
      <h4>How this works</h4>
      <p>Click a hotspot in the room, or pick a tile from the list below. Read the situation, choose what you'd do, then go through the after-action checklist. Your overall readiness meter goes up as you finish modules and check off habits you've already built.</p>
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
        <span data-role="lab-counter">0 of {len(LAB)} modules complete</span>
        &nbsp;·&nbsp; <span data-role="lab-habit-counter">0 habits checked</span>
        &nbsp;·&nbsp; <button type="button" class="btn btn-secondary btn-sm" data-action="lab-reset">↺ Reset progress</button>
      </p>
    </div>
  </section>

  <section class="container">
    <h2>Click anything in the room</h2>
    <div class="lab-scene">
      {svg}
    </div>
    <p class="muted lab-scene-help">If the scene is hard to read on your screen, use the labeled list below. It does the same thing.</p>
  </section>

  <section class="container">
    <h2>Or pick from the list</h2>
    <div class="lab-grid">
      {grid}
    </div>
  </section>

  <section class="container" id="lab">
    <div class="lab-runner" hidden>
      <div class="lab-runner-head">
        <button type="button" class="btn btn-secondary btn-sm" data-action="lab-close">← Back to room</button>
        <span class="lab-runner-title" data-role="lab-title"></span>
      </div>
      <div class="lab-setup" data-role="lab-setup"></div>
      <div class="lab-question" data-role="lab-question"></div>
      <div class="lab-choices" data-role="lab-choices"></div>
      <div class="lab-outcome" data-role="lab-outcome" hidden></div>
      <div class="lab-aar" data-role="lab-aar" hidden></div>
    </div>
    <script type="application/json" id="lab-data">{payload}</script>
  </section>

  <section class="container read">
    <h2>What this lab is, and what it isn't</h2>
    <p>This lab is built around things that actually happen in dorms. A roommate clicks a sketchy link. A laptop gets encrypted before finals. A club account starts hitting up members for money. The choices and the after-action checklists come from plain-language guidance: <a href="https://www.cisa.gov/stopransomware">CISA #StopRansomware</a>, <a href="https://www.cisa.gov/secureourworld">CISA Secure Our World</a>, the <a href="https://staysafeonline.org/">National Cybersecurity Alliance</a>, <a href="https://library.educause.edu/">EDUCAUSE</a>, and the <a href="https://www.ic3.gov/">FBI Internet Crime Complaint Center</a>. Nothing here tells you how to attack anything. It tells you how to recognize and respond.</p>
    <p>Whatever your campus IT help desk says, that wins.</p>
  </section>
"""
    return page(
        "Dorm lab",
        body,
        depth=0,
        description="A simulated dorm room with ten clickable incident modules. Practice what to do when a roommate clicks a sketchy link, your laptop gets encrypted before finals, or your club account is taken over.",
    )


def main() -> None:
    out = ROOT
    # Top-level student-focused pages only
    (out / "prevention.html").write_text(render_prevention(), encoding="utf-8")
    (out / "response.html").write_text(render_response(), encoding="utf-8")
    (out / "readiness.html").write_text(render_readiness(), encoding="utf-8")
    (out / "scenarios.html").write_text(render_scenarios(), encoding="utf-8")
    (out / "dorm-lab.html").write_text(render_dorm_lab(), encoding="utf-8")
    (out / "glossary.html").write_text(render_glossary(), encoding="utf-8")
    (out / "faq.html").write_text(render_faq(), encoding="utf-8")
    (out / "references.html").write_text(render_references(), encoding="utf-8")
    (out / "404.html").write_text(render_404(), encoding="utf-8")
    print("Pages built.")


if __name__ == "__main__":
    main()
