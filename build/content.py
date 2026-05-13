ROLES = [
    {
        "id": "student",
        "label": "Student",
        "icon": "🎓",
        "summary": "Protect your accounts, recognize phishing, and report fast when something looks wrong.",
        "before": [
            "Turn on multi-factor authentication (MFA) for your campus account, email, and any system holding your records.",
            "Use a password manager and a unique password for your campus identity. Never reuse it on other sites.",
            "Keep your laptop, phone, and browser updated. Install updates within 7 days of release.",
            "Back up your coursework to campus cloud storage (and a second copy where allowed). Don’t rely on a single drive.",
            "Save the IT help desk and security team contact info in your phone before you need it.",
            "Complete any phishing or security training the campus offers — even short modules build real skill.",
            "Review your account recovery options (backup email, phone) so an attacker can’t reset your password.",
        ],
        "during": [
            "If a message, login page, or pop-up looks suspicious, stop. Do not click, do not enter credentials.",
            "If you already clicked or entered a password, change that password from a different device and report it now.",
            "If your device is acting strange (files renamed, ransom note, unexpected encryption), disconnect it from Wi-Fi and any cables, leave it powered on, and contact IT.",
            "Forward suspicious emails using the campus ‘Report Phishing’ button or as an attachment to the security team.",
            "Don’t try to ‘fix’ a suspected infection yourself. Don’t pay a ransom on a personal device — call IT.",
            "Follow official guidance from the campus emergency channel. Ignore unverified rumors on social media.",
        ],
        "after": [
            "Change passwords for any account that may have been exposed and review login history.",
            "Re-enable backups and confirm your important files are still recoverable.",
            "Tell classmates and roommates what you saw — phishing campaigns usually target many students at once.",
            "Attend any post-incident briefings; they teach you the exact lure that worked so you can avoid the next one.",
        ],
        "checklist_id": "student-readiness",
        "checklist_title": "Student readiness checklist",
        "checklist_items": [
            "MFA is on for my campus email and student portal.",
            "I use a password manager (or at least a unique password for school accounts).",
            "My laptop and phone install updates automatically.",
            "I have at least one backup of my coursework outside the device I use daily.",
            "I know how to report a phishing email on my campus.",
            "The IT help desk number is saved in my phone.",
            "I’ve reviewed my account recovery email and phone in the last 6 months.",
        ],
    },
]

PHASES = {
    "prepare": {
        "title": "Prepare",
        "summary": "Reduce attack surface, raise the cost of a successful intrusion, and rehearse the response.",
        "actions": [
            "Enforce MFA — phishing-resistant where you can.",
            "Maintain immutable, tested backups for tier-1 systems.",
            "Segment networks and harden remote access.",
            "Patch on a defined cadence; track third-party SaaS exposure.",
            "Run regular phishing simulations and security training.",
            "Hold annual tabletop exercises across roles.",
        ],
    },
    "detect": {
        "title": "Detect",
        "summary": "Catch ransomware activity early — before encryption, ideally during initial access.",
        "actions": [
            "Deploy EDR on all endpoints with tuned alerting.",
            "Centralize identity provider logs and hunt continuously.",
            "Monitor for impossible travel, MFA fatigue, OAuth grants, and rogue mailbox rules.",
            "Empower users to report suspicious activity in one click and reward reports.",
            "Watch for early indicators: mass file renames, shadow-copy deletion, unexpected admin tool use.",
        ],
    },
    "contain": {
        "title": "Contain",
        "summary": "Stop the spread fast, then preserve evidence.",
        "actions": [
            "Isolate affected hosts and segments; disable compromised identities.",
            "Revoke active sessions and rotate exposed credentials/secrets.",
            "Block known command-and-control infrastructure.",
            "Preserve memory and disk images before any reimaging.",
            "Avoid powering off systems unless directed by IR — volatile evidence matters.",
        ],
    },
    "communicate": {
        "title": "Communicate",
        "summary": "Coordinate honest, timely messages internally and externally.",
        "actions": [
            "Use out-of-band channels; assume primary email may be unsafe.",
            "Activate the pre-approved holding statement.",
            "Engage legal counsel, insurer, and law enforcement (e.g., FBI/CISA) early.",
            "Brief students, faculty, staff, vendors, and the board on a defined cadence.",
            "Direct everyone to a single source of truth.",
        ],
    },
    "recover": {
        "title": "Recover",
        "summary": "Restore services in priority order — into a hardened environment.",
        "actions": [
            "Rebuild from known-good images; do not reintroduce unpatched systems.",
            "Validate backups before relying on them; restore in priority order.",
            "Rotate secrets, certificates, and service-account credentials.",
            "Hunt for persistence before declaring recovery complete.",
            "Run focused communications about service restoration timelines.",
        ],
    },
    "learn": {
        "title": "Learn",
        "summary": "Treat the incident as data. Improve before the next one.",
        "actions": [
            "Hold a blameless after-action review with all involved roles.",
            "Produce a written AAR with tracked remediation actions and owners.",
            "Update detections, runbooks, and this playbook.",
            "Brief leadership, the board, and accreditors as required.",
            "Recognize and rest the responders.",
        ],
    },
}


GLOSSARY = [
    ("After-action review (AAR)", "A structured, blameless review held after an incident to capture what happened, what worked, what didn’t, and what to change. Produces a written report with tracked actions."),
    ("Backups (immutable / offline)", "Copies of data that cannot be altered or deleted by a normal admin (immutable) or are physically disconnected (offline). Critical for ransomware recovery."),
    ("CISA", "U.S. Cybersecurity and Infrastructure Security Agency. Publishes the #StopRansomware guide and maintains free resources for higher education."),
    ("Command and control (C2)", "Infrastructure attackers use to communicate with malware on compromised systems. Blocking C2 helps stop ongoing attacks."),
    ("Containment", "Steps that stop an attack from spreading further: isolating hosts, disabling accounts, revoking sessions, blocking outbound traffic."),
    ("Decryption key", "The key needed to reverse ransomware encryption. May or may not be supplied by attackers after payment; sometimes published by law enforcement."),
    ("Detection", "Identifying that an intrusion or attack is occurring or has occurred, ideally before damage is done."),
    ("Endpoint Detection and Response (EDR)", "Software that monitors laptops, desktops, and servers for malicious behavior and supports investigation and response."),
    ("FERPA", "Family Educational Rights and Privacy Act (U.S.). Governs the privacy of student education records and shapes notification obligations."),
    ("FIDO2 / WebAuthn", "Phishing-resistant authentication standards. Hardware keys and platform authenticators (Touch ID, Face ID, Windows Hello) implement them."),
    ("Incident Commander", "The single person responsible for directing the response during an incident, regardless of normal seniority."),
    ("Indicator of Compromise (IOC)", "An observable artifact (file hash, IP, domain, behavior) that suggests a system has been attacked."),
    ("MFA / Multi-factor authentication", "Requiring more than a password to sign in, typically a code or hardware key. Phishing-resistant MFA (FIDO2) defeats most credential phishing."),
    ("MFA fatigue", "Attack where an attacker repeatedly triggers MFA prompts hoping the user approves one out of frustration."),
    ("NIST", "U.S. National Institute of Standards and Technology. Publishes the Cybersecurity Framework and SP 800-61 for incident response."),
    ("Phishing", "Deceptive messages (email, SMS, voice, web) that trick users into entering credentials, running malware, or approving fraudulent transactions."),
    ("Ransomware", "Malware that encrypts files and/or steals data, then demands payment to restore access or to prevent publication."),
    ("RDP", "Remote Desktop Protocol. Frequently abused by attackers when exposed to the internet without strong controls."),
    ("Segmentation", "Dividing a network into zones so a compromise in one area can’t spread freely to others."),
    ("Tabletop exercise", "A facilitated discussion-based drill where leaders walk through their response to a hypothetical incident."),
    ("Third-party risk", "Risk introduced by vendors, SaaS providers, and contractors. Recent higher-ed ransomware impact has been driven heavily by exploited third-party software."),
]


FAQ = [
    ("What even is ransomware, in plain terms?",
     "Malicious software that locks up files (and often steals copies first) so someone can demand payment to unlock them or to not publish them. As a student, you mainly see the front door: phishing emails, fake login pages, and account takeovers that let attackers in."),
    ("Why should I care — isn’t this an IT problem?",
     "Your account is the easiest way in. Compromised student accounts have been used to attack faculty, raid scholarship funds, exfiltrate course rosters, and reset other passwords. A single careless click can affect your grades, financial aid, and roommates."),
    ("I think I clicked a phishing link. What now?",
     "Stop using the device. From a different device (your phone is fine), change the password for the affected account, then call the campus IT help desk. Keep the original message — IT may need it. Speed matters more than embarrassment."),
    ("My laptop is showing a ransom note. What should I do?",
     "Don’t pay anything. Disconnect from Wi-Fi and unplug any cables, but leave the device powered on (forensics may need volatile memory). Call campus IT immediately. Don’t try to ‘fix’ it yourself."),
    ("Is the campus going to discipline me if I report a mistake?",
     "Most campuses have a non-punitive reporting culture for honest reports — they need the data to defend everyone. Check your campus policy, but the cost of not reporting is almost always worse than the cost of reporting."),
    ("Should I use a personal device for schoolwork?",
     "Generally fine if it’s up to date, has MFA on your campus account, and you don’t pirate software on it. Some courses or programs (e.g., clinical, legal, research with sensitive data) require institution-managed devices — check your syllabus."),
    ("Is MFA actually worth the hassle?",
     "Yes. Multi-factor authentication blocks almost all bulk credential-phishing. Phishing-resistant MFA (FIDO2 / passkeys / hardware keys like YubiKey) is even stronger. Enable it wherever your campus offers it."),
    ("Is public Wi-Fi at the coffee shop dangerous?",
     "Less than it used to be — most sites and apps use HTTPS by default — but it’s still a good idea to avoid logging into your campus account from networks you don’t trust, and to use your campus VPN if your school provides one."),
    ("Can this site substitute for legal advice?",
     "No. This is a plain-language educational summary. Specific obligations under FERPA, state breach laws, or your campus policies depend on your situation — talk to your IT help desk, dean of students, or campus counsel."),
]

REFERENCES = [
    ("CISA Secure Our World", "https://www.cisa.gov/secureourworld",
     "Plain-language consumer guidance from the U.S. Cybersecurity & Infrastructure Security Agency on MFA, phishing, passwords, and updates."),
    ("CISA #StopRansomware", "https://www.cisa.gov/stopransomware",
     "U.S. CISA hub of ransomware guidance, including how to report an incident."),
    ("National Cybersecurity Alliance — StaySafeOnline", "https://staysafeonline.org/online-safety-privacy-basics/",
     "General-public cybersecurity basics, including phishing, passwords, and account safety."),
    ("EDUCAUSE: Cybersecurity Awareness for College Students", "https://library.educause.edu/resources/2020/9/cybersecurity-awareness-for-college-students-7-things-to-do-now",
     "Higher-ed-focused student safety tips from Purdue/EDUCAUSE."),
    ("Federal Trade Commission — Identity Theft and Online Security", "https://consumer.ftc.gov/identity-theft-and-online-security/online-privacy-and-security",
     "U.S. FTC guidance for individuals on online privacy, scams, and recovering from identity theft."),
    ("FBI Internet Crime Complaint Center (IC3)", "https://www.ic3.gov/",
     "Where U.S. individuals and institutions can report cyber incidents to the FBI."),
    ("Higher Ed Dive: Ransomware in Education, H1 2025", "https://www.highereddive.com/news/ransomware-attacks-education-jump-23-percent-h1-2025/754011/",
     "Reporting on the scale and trends of ransomware affecting colleges and schools."),
]


# ============================================================================
# SCENARIOS — interactive "Choose-Your-Response" branching simulations.
# ----------------------------------------------------------------------------
# Each scenario:
#   id, title, blurb, situation (short setup), start (node id), nodes {...}.
#
# Node types:
#   "decision" — q (string), choices [{label, next, score, tag}]
#                score is -2, -1, 0, +1, +2 (strong, ok, neutral, risky, catastrophic)
#                tag is "good" | "ok" | "risky" | "bad"  (drives the result CSS)
#   "outcome"  — title, body, tag ("good"|"ok"|"risky"|"bad"), score (cumulative on this path)
#                links: optional list of (label, href) to send the student to relevant
#                guidance (Protect yourself / If something goes wrong / FAQ).
#
# Authoring rules (per repo guidance):
#   - Plain, directive, student-friendly language.
#   - Distinguish general guidance from institution-specific policies.
#   - Never describe how to attack, deploy ransomware, or evade defenses.
#   - All scenarios are *plausible everyday situations*, not exploit walkthroughs.
# ============================================================================

SCENARIOS = [
    # ----------------------------------------------------------------------
    {
        "id": "phishing-it-helpdesk",
        "title": "The ‘IT Help Desk’ email",
        "blurb": "A panic-inducing email about your account.",
        "situation": (
            "At 11:47 PM, the night before a paper is due, you get an email titled "
            "‘ACTION REQUIRED: Your campus account will be deleted in 24 hours.’ "
            "It says click the link to ‘verify your identity’ or lose access to your "
            "coursework. The sender address has your school’s name in it, but the "
            "domain after the @ doesn’t quite match your school."
        ),
        "start": "n0",
        "nodes": {
            "n0": {"type": "decision", "q": "What do you do first?", "choices": [
                {"label": "Click the link to check whether it’s real.",
                 "next": "n_clicked", "score": 1, "tag": "risky"},
                {"label": "Look at the sender’s full email address and the link before doing anything.",
                 "next": "n_inspect", "score": -1, "tag": "good"},
                {"label": "Reply to the sender asking if it’s legit.",
                 "next": "n_replied", "score": 1, "tag": "risky"},
                {"label": "Enter your password on the linked page so you don’t lose access.",
                 "next": "out_creds", "score": 2, "tag": "bad"},
            ]},
            "n_inspect": {"type": "decision",
                "q": "The sender domain is ‘mail-university-support.com’ and the link goes to a Google Form. What now?", "choices": [
                {"label": "Report the message using my campus ‘Report Phishing’ button (or forward it as an attachment to the security team) and delete it.",
                 "next": "out_reported", "score": -2, "tag": "good"},
                {"label": "Forward it to a friend to warn them.",
                 "next": "out_forwarded", "score": 1, "tag": "risky"},
                {"label": "Ignore it.",
                 "next": "out_ignored", "score": 0, "tag": "ok"},
            ]},
            "n_clicked": {"type": "decision",
                "q": "The page looks exactly like your school’s login. What now?", "choices": [
                {"label": "Close the tab without entering anything and report the email.",
                 "next": "out_close_report", "score": -1, "tag": "good"},
                {"label": "Type in my username and password to ‘check.’",
                 "next": "out_creds", "score": 2, "tag": "bad"},
            ]},
            "n_replied": {"type": "outcome", "tag": "risky", "score": 1,
                "title": "Replying confirms your address is active.",
                "body": "Replying to phishing tells the attacker the address is live and monitored. Even if you don’t click anything, expect more targeted messages. Next time, don’t reply — report and delete.",
                "links": [("If something goes wrong", "response.html")]},
            "out_creds": {"type": "outcome", "tag": "bad", "score": 2,
                "title": "Catastrophic — credentials likely compromised.",
                "body": "You just typed your campus password into a page controlled by an attacker. From a different device (your phone is fine), change your campus password immediately, sign out of all sessions, and call the IT help desk. Keep the original email as evidence. Do not use the suspect device for anything sensitive until IT clears it.",
                "links": [("If something goes wrong", "response.html"), ("Sources", "references.html")]},
            "out_reported": {"type": "outcome", "tag": "good", "score": -2,
                "title": "Textbook response.",
                "body": "Inspecting the sender domain and the link before clicking is the single biggest skill students can build. Reporting through the campus tool helps your security team warn everyone else getting the same lure. Nice work.",
                "links": [("Protect yourself", "prevention.html")]},
            "out_forwarded": {"type": "outcome", "tag": "risky", "score": 1,
                "title": "Well-intentioned, but risky.",
                "body": "Forwarding the live message can lead a friend to click. Report it through your campus tool instead, and tell friends about the pattern in your own words (‘watch out for fake IT deletion emails right now’).",
                "links": [("If something goes wrong", "response.html")]},
            "out_ignored": {"type": "outcome", "tag": "ok", "score": 0,
                "title": "Safe, but you missed the upside.",
                "body": "Ignoring kept you safe. Reporting is even better — it lets the security team block the lure for everyone else and pull the page down faster.",
                "links": [("Protect yourself", "prevention.html")]},
            "out_close_report": {"type": "outcome", "tag": "good", "score": -1,
                "title": "Solid recovery.",
                "body": "Closing without entering credentials limits the damage to maybe a tracking pixel. Report the email so the security team can pull the page down. If you have any doubt at all about whether you typed something, change your password from a different device.",
                "links": [("If something goes wrong", "response.html")]},
        },
    },
    # ----------------------------------------------------------------------
    {
        "id": "fake-canvas-login",
        "title": "The Canvas link that wasn’t",
        "blurb": "A link from a TA leads to a login page.",
        "situation": (
            "Your TA shares ‘a quick poll for Friday’s class’ in the course Discord. "
            "The link opens a page that looks like your school’s Canvas login, but the "
            "URL in the address bar reads ‘canvas-myschool-edu.app/auth’."
        ),
        "start": "n0",
        "nodes": {
            "n0": {"type": "decision", "q": "What do you notice first?", "choices": [
                {"label": "The URL doesn’t end in my school’s real domain. Stop.",
                 "next": "n_stopped", "score": -1, "tag": "good"},
                {"label": "It looks like Canvas — just sign in to take the poll.",
                 "next": "out_creds_canvas", "score": 2, "tag": "bad"},
                {"label": "DM the TA on a separate channel to ask if they posted this.",
                 "next": "n_dm", "score": -1, "tag": "good"},
            ]},
            "n_stopped": {"type": "decision",
                "q": "What next?", "choices": [
                {"label": "Open Canvas by typing my school’s URL myself, and check there for the poll.",
                 "next": "out_typed_url", "score": -2, "tag": "good"},
                {"label": "Refresh the page in case it loads correctly the second time.",
                 "next": "out_refresh", "score": 1, "tag": "risky"},
            ]},
            "n_dm": {"type": "outcome", "tag": "good", "score": -2,
                "title": "Verify out of band — great instinct.",
                "body": "Asking the TA through a different channel (text, in person, official email) is one of the cleanest ways to verify a suspicious link. If their Discord was compromised, the impostor will often answer ‘yes, it’s real’ — so trust the out-of-band reply, not the in-channel one.",
                "links": [("Protect yourself", "prevention.html")]},
            "out_creds_canvas": {"type": "outcome", "tag": "bad", "score": 2,
                "title": "Your Canvas (and possibly campus) password is now exposed.",
                "body": "Many schools use the same SSO for Canvas, email, and the student portal — so this could be your master credential. From a different device, change your campus password immediately, revoke active sessions, and tell IT. Mention that the lure came from a TA’s Discord — it’s a clue the TA’s account is compromised, too.",
                "links": [("If something goes wrong", "response.html")]},
            "out_typed_url": {"type": "outcome", "tag": "good", "score": -2,
                "title": "Best practice.",
                "body": "Typing the URL yourself (or using your own bookmark) defeats almost all credential-harvesting pages, because the attacker can’t intercept what you typed into your own address bar. Report the original link so IT can take it down.",
                "links": [("Protect yourself", "prevention.html")]},
            "out_refresh": {"type": "outcome", "tag": "risky", "score": 1,
                "title": "Refreshing doesn’t fix a fake page.",
                "body": "A reload just reloads the attacker’s page. The URL is your evidence — if it doesn’t match your school’s domain, treat the page as hostile and leave. Report the link.",
                "links": [("Protect yourself", "prevention.html")]},
        },
    },
    # ----------------------------------------------------------------------
    {
        "id": "dorm-ransom-note",
        "title": "The dorm laptop ransom note",
        "blurb": "Your roommate’s gaming laptop is screaming for Bitcoin.",
        "situation": (
            "You walk into your dorm and your roommate’s laptop is open on the desk. "
            "The screen shows a red ransom note demanding $400 in Bitcoin to ‘decrypt your files.’ "
            "Your roommate isn’t home. The laptop is plugged in via Ethernet to the dorm jack."
        ),
        "start": "n0",
        "nodes": {
            "n0": {"type": "decision", "q": "What do you do first?", "choices": [
                {"label": "Unplug the Ethernet cable and turn off Wi-Fi. Leave the laptop powered on.",
                 "next": "n_disconnect", "score": -2, "tag": "good"},
                {"label": "Power the laptop off so it stops.",
                 "next": "out_powered_off", "score": 1, "tag": "risky"},
                {"label": "Try clicking the ransom note buttons to see the options.",
                 "next": "out_clicked_note", "score": 2, "tag": "bad"},
                {"label": "Take a phone photo of the screen, then walk away until I can reach my roommate.",
                 "next": "n_photo", "score": 0, "tag": "ok"},
            ]},
            "n_disconnect": {"type": "decision",
                "q": "Good — the laptop is isolated. Now what?", "choices": [
                {"label": "Take a photo of the note, write down the time, and call the campus IT help desk.",
                 "next": "out_isolated_called", "score": -2, "tag": "good"},
                {"label": "Try to recover files with a ‘free ransomware decryptor’ I just searched for.",
                 "next": "out_decryptor", "score": 2, "tag": "bad"},
                {"label": "Pay the $400 quickly so my roommate doesn’t lose their files.",
                 "next": "out_paid", "score": 2, "tag": "bad"},
            ]},
            "n_photo": {"type": "outcome", "tag": "ok", "score": 0,
                "title": "Helpful evidence, but the device is still on the network.",
                "body": "A photo is great for IT, but while the device is still on the network, the malware may be reaching out to attacker infrastructure, encrypting cloud-synced files, or attacking other devices on the dorm Wi-Fi. Disconnect first, then photograph, then call IT.",
                "links": [("If something goes wrong", "response.html")]},
            "out_powered_off": {"type": "outcome", "tag": "risky", "score": 1,
                "title": "Powering off destroys evidence.",
                "body": "Volatile memory often contains the encryption key or attacker indicators that responders use to recover files. Leave the device powered on but disconnected from networks. (This is exactly opposite to what feels intuitive.)",
                "links": [("If something goes wrong", "response.html")]},
            "out_clicked_note": {"type": "outcome", "tag": "bad", "score": 2,
                "title": "Don’t interact with the note.",
                "body": "Some ransom notes have ‘chat’ or ‘test decrypt’ buttons that escalate the attack, start a deadline timer, or send your IP to the attacker. Don’t click anything. Disconnect from the network, photograph the screen, and call IT.",
                "links": [("If something goes wrong", "response.html")]},
            "out_isolated_called": {"type": "outcome", "tag": "good", "score": -2,
                "title": "Exactly right.",
                "body": "Isolate, photograph, call. That sequence — even if it’s your roommate’s personal device — gives the responders volatile memory, the lock-screen text, and an accurate timeline. Tell your roommate as soon as you reach them.",
                "links": [("Protect yourself", "prevention.html")]},
            "out_decryptor": {"type": "outcome", "tag": "bad", "score": 2,
                "title": "‘Free decryptors’ are almost always more malware.",
                "body": "Search results for ‘ransomware decryptor’ are saturated with second-stage malware that finishes the job. Real decryption tools (when they exist) are released by law enforcement or vetted vendors like Europol’s No More Ransom — and applying them is something IT or a forensic responder should do, not a panicking student.",
                "links": [("If something goes wrong", "response.html")]},
            "out_paid": {"type": "outcome", "tag": "bad", "score": 2,
                "title": "Don’t pay.",
                "body": "Most ransomware payments don’t produce a working key, and many fund sanctioned criminal groups. Paying also marks your roommate (and your dorm) as soft targets. Call IT instead — they can advise on what backups, cloud restore, or device replacement looks like.",
                "links": [("If something goes wrong", "response.html"), ("Sources", "references.html")]},
        },
    },
    # ----------------------------------------------------------------------
    {
        "id": "mfa-fatigue",
        "title": "The 2 AM MFA prompts",
        "blurb": "Your phone is buzzing with login requests you didn’t make.",
        "situation": (
            "At 2:11 AM your phone buzzes with an MFA push notification. ‘Approve sign-in?’ "
            "You ignore it. Two minutes later, another. By 2:20 AM you’ve had nine prompts in a row. "
            "You’re not trying to sign in to anything."
        ),
        "start": "n0",
        "nodes": {
            "n0": {"type": "decision", "q": "What do you do?", "choices": [
                {"label": "Approve one so the buzzing stops.",
                 "next": "out_approved", "score": 2, "tag": "bad"},
                {"label": "Deny the prompt and change my password right now from a different device.",
                 "next": "n_denied_changed", "score": -2, "tag": "good"},
                {"label": "Turn my phone on Do Not Disturb and deal with it tomorrow.",
                 "next": "out_dnd", "score": 1, "tag": "risky"},
                {"label": "Deny the prompt and report it to IT in the morning.",
                 "next": "out_reported_morning", "score": 0, "tag": "ok"},
            ]},
            "n_denied_changed": {"type": "decision",
                "q": "Password changed. What else?", "choices": [
                {"label": "Sign out of all active sessions and review my login history.",
                 "next": "out_full_response", "score": -2, "tag": "good"},
                {"label": "Done — go back to sleep.",
                 "next": "out_partial", "score": 0, "tag": "ok"},
            ]},
            "out_approved": {"type": "outcome", "tag": "bad", "score": 2,
                "title": "Classic ‘MFA fatigue’ takeover.",
                "body": "MFA fatigue (also called ‘push bombing’) is one of the most effective attacks against student accounts. By approving one push, you almost certainly handed someone full access. From a different device, change your password, sign out of all sessions, and call IT first thing in the morning — earlier if your campus has 24/7 IT.",
                "links": [("If something goes wrong", "response.html")]},
            "out_dnd": {"type": "outcome", "tag": "risky", "score": 1,
                "title": "Quiet doesn’t mean safe.",
                "body": "DND silences the prompts but doesn’t stop the attempts. The attacker has your password — they’re trying to bypass MFA. By tomorrow morning they may have tried hundreds of logins, social engineering your helpdesk, or pivoted to your email recovery. Change the password tonight, even if it’s annoying.",
                "links": [("If something goes wrong", "response.html")]},
            "out_reported_morning": {"type": "outcome", "tag": "ok", "score": 0,
                "title": "Better than approving, but slow.",
                "body": "Denying is good. Waiting until morning is risky — the attacker has your password and is hammering MFA. Change the password now from a different device; reporting can wait until the help desk opens.",
                "links": [("If something goes wrong", "response.html")]},
            "out_full_response": {"type": "outcome", "tag": "good", "score": -2,
                "title": "Excellent.",
                "body": "Deny → change password → sign out all sessions → review login history is the gold-standard response. If your school offers phishing-resistant MFA (FIDO2, hardware key, or platform passkey), this is a great moment to enroll.",
                "links": [("Protect yourself", "prevention.html"), ("Sources", "references.html")]},
            "out_partial": {"type": "outcome", "tag": "ok", "score": 0,
                "title": "Halfway there.",
                "body": "Changing the password is critical, but active sessions stay valid until you sign them out. Also check your account’s recent login history — many providers show it in your account settings.",
                "links": [("Protect yourself", "prevention.html")]},
        },
    },
    # ----------------------------------------------------------------------
    {
        "id": "job-scam",
        "title": "The ‘paid research assistant’ DM",
        "blurb": "A professor you don’t recognize offers you $40/hr.",
        "situation": (
            "Someone DMs you on LinkedIn claiming to be a visiting professor in your department. "
            "They’re ‘urgently hiring a paid research assistant for remote work — $40/hr, 10 hrs/week.’ "
            "They ask for your personal email so they can send a contract, and request you Venmo $75 "
            "for ‘software setup’ that they’ll reimburse with your first paycheck."
        ),
        "start": "n0",
        "nodes": {
            "n0": {"type": "decision", "q": "What do you do?", "choices": [
                {"label": "Send the $75 — it’s reimbursable and the rate is amazing.",
                 "next": "out_paid_scam", "score": 2, "tag": "bad"},
                {"label": "Reply asking for their campus email and look them up in the school directory first.",
                 "next": "n_verify", "score": -1, "tag": "good"},
                {"label": "Give them your personal email but not the money.",
                 "next": "out_handed_email", "score": 1, "tag": "risky"},
                {"label": "Block and report — anyone asking a student to pay them upfront is a scam.",
                 "next": "out_blocked", "score": -2, "tag": "good"},
            ]},
            "n_verify": {"type": "decision",
                "q": "There’s no faculty member by that name in the directory. They reply with a generic Gmail address. What now?", "choices": [
                {"label": "Block and report to LinkedIn, then warn classmates.",
                 "next": "out_blocked", "score": -2, "tag": "good"},
                {"label": "Send them $75 anyway — the rate is too good to pass up.",
                 "next": "out_paid_scam", "score": 2, "tag": "bad"},
            ]},
            "out_paid_scam": {"type": "outcome", "tag": "bad", "score": 2,
                "title": "Student job scam — money is gone.",
                "body": "Real employers do not ask candidates to pay them, period. The $75 is gone, and depending on what info you shared, you may be on a list for follow-on identity theft (fake check, phony tax forms, etc.). Report the fraud to LinkedIn, your bank/Venmo, and the FBI IC3.",
                "links": [("If something goes wrong", "response.html"), ("Sources", "references.html")]},
            "out_handed_email": {"type": "outcome", "tag": "risky", "score": 1,
                "title": "You traded contact info for a relationship with a scammer.",
                "body": "They’ll now use your personal email to send convincing follow-ups, fake checks to deposit, or phishing that uses your name correctly. Stop responding, block the account, and add your personal email to extra vigilance for the next month.",
                "links": [("Protect yourself", "prevention.html")]},
            "out_blocked": {"type": "outcome", "tag": "good", "score": -2,
                "title": "Pattern matched correctly.",
                "body": "Upfront ‘software fee,’ unreal-sounding rate, off-platform contact, unverifiable identity — that’s the modern student job scam. Reporting on LinkedIn helps the platform shut the account down before it hits your classmates.",
                "links": [("Protect yourself", "prevention.html"), ("Sources", "references.html")]},
        },
    },
    # ----------------------------------------------------------------------
    {
        "id": "financial-aid",
        "title": "‘Verify your FAFSA refund’",
        "blurb": "A text says your aid disbursement is on hold.",
        "situation": (
            "You get a text: ‘[University] Financial Aid: Your refund of $1,432.18 is on hold. "
            "Verify your bank info within 12 hours to prevent reversal: hxxps://fin-aid-portal-myschool.com’."
        ),
        "start": "n0",
        "nodes": {
            "n0": {"type": "decision", "q": "What do you do?", "choices": [
                {"label": "Tap the link and enter my bank login so I don’t lose the refund.",
                 "next": "out_bank_creds", "score": 2, "tag": "bad"},
                {"label": "Open my actual student portal in a browser and check there.",
                 "next": "n_portal_check", "score": -2, "tag": "good"},
                {"label": "Call the financial aid office using the number from the school’s real website.",
                 "next": "out_called_office", "score": -2, "tag": "good"},
                {"label": "Reply ‘STOP’.",
                 "next": "out_reply_stop", "score": 1, "tag": "risky"},
            ]},
            "n_portal_check": {"type": "outcome", "tag": "good", "score": -2,
                "title": "Right channel, right answer.",
                "body": "Your student portal is the source of truth. If there’s really a hold, it’s there. ‘Verify within 12 hours’ urgency, an unfamiliar domain, and a request for bank credentials are three classic phishing signals stacked in one message.",
                "links": [("Protect yourself", "prevention.html")]},
            "out_called_office": {"type": "outcome", "tag": "good", "score": -2,
                "title": "Best of all — verify by voice.",
                "body": "Calling the office using a number you find on the school’s real website (not from the text) verifies in seconds whether anything is actually wrong. This works for ‘unpaid tuition,’ ‘scholarship deactivated,’ and similar lures too.",
                "links": [("Protect yourself", "prevention.html")]},
            "out_bank_creds": {"type": "outcome", "tag": "bad", "score": 2,
                "title": "Bank credentials compromised.",
                "body": "Call your bank immediately, freeze the account, and change online-banking credentials from a clean device. File a fraud report at ic3.gov and with your school’s financial aid office. Watch for follow-on impersonation: scammers often parlay one win into another (‘this is your bank fraud team’).",
                "links": [("If something goes wrong", "response.html"), ("Sources", "references.html")]},
            "out_reply_stop": {"type": "outcome", "tag": "risky", "score": 1,
                "title": "STOP confirms you read it.",
                "body": "Replying — even with ‘STOP’ — confirms the number is live and you opened the message. Don’t reply. Don’t click. Delete and, if you have an iPhone or Android, report as junk.",
                "links": [("Protect yourself", "prevention.html")]},
        },
    },
    # ----------------------------------------------------------------------
    {
        "id": "club-drive",
        "title": "The club Google Drive looks weird",
        "blurb": "Files renamed, weird shares, missing folders.",
        "situation": (
            "You’re the secretary of a campus club. This morning, your shared Google Drive shows "
            "two folders missing, several files renamed to ‘encrypted-by-…’ style names, and a new "
            "‘share’ to an external Gmail address you don’t recognize. The club president is in class."
        ),
        "start": "n0",
        "nodes": {
            "n0": {"type": "decision", "q": "First move?", "choices": [
                {"label": "Right away, revoke the unknown external share and lock down sharing on the affected files.",
                 "next": "n_locked", "score": -1, "tag": "good"},
                {"label": "Delete the weird files so they’re not visible.",
                 "next": "out_deleted", "score": 1, "tag": "risky"},
                {"label": "Restore older versions of the files from version history while figuring out what happened.",
                 "next": "n_restored", "score": -1, "tag": "good"},
                {"label": "Ignore it — probably a Drive glitch.",
                 "next": "out_ignored", "score": 1, "tag": "risky"},
            ]},
            "n_locked": {"type": "decision",
                "q": "Sharing is locked. Next?", "choices": [
                {"label": "Notify campus IT, then change the password and revoke active sessions on the club’s owning account.",
                 "next": "out_full_clean", "score": -2, "tag": "good"},
                {"label": "Just tell the president when you next see them.",
                 "next": "out_delayed", "score": 1, "tag": "risky"},
            ]},
            "n_restored": {"type": "decision",
                "q": "Files are restoring. What else?", "choices": [
                {"label": "Also revoke unknown shares and notify IT — restoration alone doesn’t kick the attacker out.",
                 "next": "out_full_clean", "score": -2, "tag": "good"},
                {"label": "Done — files are back.",
                 "next": "out_left_attacker", "score": 1, "tag": "risky"},
            ]},
            "out_deleted": {"type": "outcome", "tag": "risky", "score": 1,
                "title": "You destroyed the evidence.",
                "body": "Deleting the encrypted files removes the forensic trail and might also delete the only artifact that can identify the actor. Restore from version history instead, revoke the bad share, and tell IT.",
                "links": [("If something goes wrong", "response.html")]},
            "out_ignored": {"type": "outcome", "tag": "risky", "score": 1,
                "title": "It’s almost certainly not a glitch.",
                "body": "Missing folders + renamed files + an unknown external share is the signature of an account takeover or a ransomware actor targeting cloud storage. Don’t wait — revoke the share now and tell IT.",
                "links": [("If something goes wrong", "response.html")]},
            "out_full_clean": {"type": "outcome", "tag": "good", "score": -2,
                "title": "Strong, calm response.",
                "body": "Revoke the unknown share, restore from version history, change the owner account’s password, sign out all sessions, and loop in IT. That sequence cuts the attacker’s access without losing your data. Tell the president as soon as they’re free.",
                "links": [("Protect yourself", "prevention.html")]},
            "out_delayed": {"type": "outcome", "tag": "risky", "score": 1,
                "title": "Speed matters more than chain-of-command.",
                "body": "While you wait, the attacker may rename or re-share more files. Loop in campus IT now — a 5-minute conversation is fine — and message the president on the side.",
                "links": [("If something goes wrong", "response.html")]},
            "out_left_attacker": {"type": "outcome", "tag": "risky", "score": 1,
                "title": "Files back, attacker still inside.",
                "body": "Restoring fixes the file damage but the attacker still has access through the unknown external share, a session, or compromised credentials. Revoke the share, change the password on the owning account, and contact IT.",
                "links": [("If something goes wrong", "response.html")]},
        },
    },
    # ----------------------------------------------------------------------
    {
        "id": "stolen-laptop",
        "title": "Stolen laptop at the library",
        "blurb": "Your laptop is gone. Your coursework is on it.",
        "situation": (
            "You stepped away for two minutes to refill a water bottle. Your laptop is gone. "
            "It was unlocked. Your campus email, Canvas, and a draft of your thesis were open."
        ),
        "start": "n0",
        "nodes": {
            "n0": {"type": "decision", "q": "First five minutes — what do you do?", "choices": [
                {"label": "Find another device, sign in to my campus account, and sign out of all sessions everywhere.",
                 "next": "n_signed_out", "score": -2, "tag": "good"},
                {"label": "Wait at the library in case it’s a prank.",
                 "next": "out_waited", "score": 1, "tag": "risky"},
                {"label": "Call campus police / security and report the theft.",
                 "next": "n_called_police", "score": -1, "tag": "good"},
                {"label": "Use Find My / device tracking and drive to the location.",
                 "next": "out_chase", "score": 2, "tag": "bad"},
            ]},
            "n_signed_out": {"type": "decision",
                "q": "Sessions ended. What next?", "choices": [
                {"label": "Change my campus password and any other passwords stored in my browser.",
                 "next": "n_changed_pw", "score": -2, "tag": "good"},
                {"label": "Done — go home and finish my thesis tomorrow.",
                 "next": "out_thesis_lost", "score": 1, "tag": "risky"},
            ]},
            "n_called_police": {"type": "decision",
                "q": "Police have the report. What else?", "choices": [
                {"label": "Sign out of all sessions on the campus account and change my password from a safe device.",
                 "next": "n_changed_pw", "score": -2, "tag": "good"},
                {"label": "Wait for police to follow up before doing anything online.",
                 "next": "out_wait_for_police", "score": 1, "tag": "risky"},
            ]},
            "n_changed_pw": {"type": "outcome", "tag": "good", "score": -2,
                "title": "Containment done right.",
                "body": "Sign out everywhere → change password → file the police/security report → use Find My to mark the device lost (which often forces a remote lock). If you have campus device-encryption (FileVault, BitLocker), the thief is mostly facing a brick. Your thesis backup in OneDrive / Google Drive / iCloud should still be intact.",
                "links": [("Protect yourself", "prevention.html")]},
            "out_waited": {"type": "outcome", "tag": "risky", "score": 1,
                "title": "Time isn’t on your side.",
                "body": "Every minute the device is unlocked is a minute someone can read your email, copy your files, or pivot into your accounts. File the report after taking online containment steps. Don’t leave a stolen, unlocked laptop alive on your campus account.",
                "links": [("If something goes wrong", "response.html")]},
            "out_chase": {"type": "outcome", "tag": "bad", "score": 2,
                "title": "Don’t physically pursue.",
                "body": "Find My is for evidence and remote lock, not for you to confront a thief. Share the location with campus police or local police and let them act. Your safety and the data containment matter more than recovering the device.",
                "links": [("If something goes wrong", "response.html")]},
            "out_thesis_lost": {"type": "outcome", "tag": "risky", "score": 1,
                "title": "Half done.",
                "body": "Sessions ended, but the device may still have remembered passwords in the browser, an active Outlook profile, and saved cookies for other sites. Change the campus password and any reused passwords now from a different device.",
                "links": [("Protect yourself", "prevention.html")]},
            "out_wait_for_police": {"type": "outcome", "tag": "risky", "score": 1,
                "title": "Police won’t do the online steps for you.",
                "body": "Campus police handle the physical investigation, not your account containment. Don’t wait — sign out, change the password, and tell IT in parallel.",
                "links": [("If something goes wrong", "response.html")]},
        },
    },
    # ----------------------------------------------------------------------
    {
        "id": "roommate-login",
        "title": "The roommate who wants ‘just one login’",
        "blurb": "‘Can I use yours? Mine glitched out.’",
        "situation": (
            "Your roommate asks if they can borrow your campus login to access the library’s "
            "paid databases for an essay due tomorrow. They say theirs ‘glitched out’ and they "
            "don’t want to wait for the help desk to open."
        ),
        "start": "n0",
        "nodes": {
            "n0": {"type": "decision", "q": "How do you respond?", "choices": [
                {"label": "Hand them my password — they’re a friend.",
                 "next": "out_shared", "score": 2, "tag": "bad"},
                {"label": "Let them use my account on my laptop while I watch.",
                 "next": "out_supervised", "score": 1, "tag": "risky"},
                {"label": "Politely refuse and help them open a help desk ticket / use 24/7 self-service password reset.",
                 "next": "out_helped", "score": -2, "tag": "good"},
                {"label": "Tell them most universities have public-library or open-access alternatives, and help them find the article.",
                 "next": "out_helped_alt", "score": -2, "tag": "good"},
            ]},
            "out_shared": {"type": "outcome", "tag": "bad", "score": 2,
                "title": "Account sharing is almost always a policy violation — and a security disaster.",
                "body": "Your school’s acceptable-use policy almost certainly forbids password sharing. If your roommate gets compromised or commits anything questionable while signed in as you, you’re the one in the logs. Even if you trust them, change your password the moment they’re done — and don’t do it again.",
                "links": [("If something goes wrong", "response.html"), ("FAQ", "faq.html")]},
            "out_supervised": {"type": "outcome", "tag": "risky", "score": 1,
                "title": "Still risky.",
                "body": "Supervised use limits some damage, but downloads, browser cookies, and screen captures can persist. And from the library’s perspective, the database access is logged as you. Better path: help them recover their own access.",
                "links": [("FAQ", "faq.html")]},
            "out_helped": {"type": "outcome", "tag": "good", "score": -2,
                "title": "Right call.",
                "body": "Most universities offer 24/7 self-service password reset and an after-hours help desk number. Help them open a ticket — and tell them you’d expect the same back. Healthy boundaries are part of cybersecurity too.",
                "links": [("Protect yourself", "prevention.html")]},
            "out_helped_alt": {"type": "outcome", "tag": "good", "score": -2,
                "title": "Underrated answer.",
                "body": "Public libraries, Google Scholar, the Internet Archive, and many publishers’ ‘read-only’ links can unblock a single article in minutes. Often the fastest way to help a friend is the route that doesn’t involve your password at all.",
                "links": [("Protect yourself", "prevention.html")]},
        },
    },
    # ----------------------------------------------------------------------
    {
        "id": "usb-found",
        "title": "The unmarked USB stick",
        "blurb": "You find a USB drive in a study room.",
        "situation": (
            "You find a USB stick on the desk in a group study room you just booked. "
            "No label, no name, no return-address sticker. You wonder if it’s a classmate’s lost drive."
        ),
        "start": "n0",
        "nodes": {
            "n0": {"type": "decision", "q": "What do you do?", "choices": [
                {"label": "Plug it into my laptop to look for the owner’s name.",
                 "next": "out_plugged", "score": 2, "tag": "bad"},
                {"label": "Drop it off at the library lost-and-found or campus IT.",
                 "next": "out_lostfound", "score": -2, "tag": "good"},
                {"label": "Throw it away — too risky.",
                 "next": "out_threw", "score": 0, "tag": "ok"},
                {"label": "Plug it into a school computer in a public lab to ‘check.’",
                 "next": "out_lab_pc", "score": 2, "tag": "bad"},
            ]},
            "out_plugged": {"type": "outcome", "tag": "bad", "score": 2,
                "title": "USB drop attacks are a real thing.",
                "body": "A surprising fraction of found USB drives are deliberate ‘drop’ attacks. Some emulate keyboards, some auto-run malware, some install hardware-level implants. Don’t plug an unknown drive into any device you care about — yours or the school’s. If you already did, disconnect from the network and call IT.",
                "links": [("If something goes wrong", "response.html"), ("Sources", "references.html")]},
            "out_lostfound": {"type": "outcome", "tag": "good", "score": -2,
                "title": "Right answer.",
                "body": "Library or IT lost-and-found is where it belongs. They have isolated equipment to identify the owner safely if needed. You stay out of the malware loop, and the actual owner has a real chance of getting it back.",
                "links": [("Protect yourself", "prevention.html")]},
            "out_threw": {"type": "outcome", "tag": "ok", "score": 0,
                "title": "Safe, but unkind to the real owner.",
                "body": "Throwing it away is safe for you but discards what might be a classmate’s research. Lost-and-found is a better default — and means the next person doesn’t find and plug it in.",
                "links": [("Protect yourself", "prevention.html")]},
            "out_lab_pc": {"type": "outcome", "tag": "bad", "score": 2,
                "title": "The lab PC isn’t a sandbox.",
                "body": "Lab PCs are connected to the campus network and often have shared drives mapped. Plugging an unknown USB into one can compromise far more than your laptop would. If you already did, leave the PC alone, note the time, and tell IT.",
                "links": [("If something goes wrong", "response.html")]},
        },
    },
]
