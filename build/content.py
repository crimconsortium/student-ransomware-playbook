ROLES = [
    {
        "id": "student",
        "label": "Student",
        "icon": "🎓",
        "summary": "Protect your accounts, recognize phishing, and report fast when something looks wrong.",
        "before": [
            "Turn on multi-factor authentication (MFA) for your campus account, email, and any system holding your records.",
            "Use a password manager and a unique password for your campus identity. Don't reuse it on other sites.",
            "Keep your laptop, phone, and browser updated. Install updates within 7 days of release.",
            "Back up your coursework to campus cloud storage (and a second copy where allowed). Don't rely on a single drive.",
            "Save the IT help desk and security team contact info in your phone before you need it.",
            "Complete any phishing or security training the campus offers. Even short modules build real skill.",
            "Review your account recovery options (backup email, phone) so an attacker can't reset your password.",
        ],
        "during": [
            "If a message, login page, or pop-up looks suspicious, stop. Don't click, don't enter credentials.",
            "If you already clicked or entered a password, change that password from a different device and report it now.",
            "If your device is acting strange (files renamed, ransom note, unexpected encryption), disconnect it from Wi-Fi and any cables, leave it powered on, and contact IT.",
            "Forward suspicious emails using the campus 'Report Phishing' button or as an attachment to the security team.",
            "Don't try to 'fix' a suspected infection yourself. Don't pay a ransom on a personal device. Call IT.",
            "Follow official guidance from the campus emergency channel. Ignore unverified rumors on social media.",
        ],
        "after": [
            "Change passwords for any account that may have been exposed and review login history.",
            "Re-enable backups and confirm your important files are still recoverable.",
            "Tell classmates and roommates what you saw. Phishing campaigns usually target many students at once.",
            "Attend any post-incident briefings. They teach you the exact lure that worked so you can spot the next one.",
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
            "I've reviewed my account recovery email and phone in the last 6 months.",
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
    ("After-action review (AAR)", "A structured, blameless review held after an incident to capture what happened, what worked, what didn't, and what to change. Produces a written report with tracked actions."),
    ("Backups (immutable / offline)", "Copies of data that can't be altered or deleted by a normal admin (immutable) or are physically disconnected (offline). Critical for ransomware recovery."),
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
    ("MFA / Multi-factor authentication", "Requiring more than a password to sign in, typically a code or hardware key. Phishing-resistant MFA (FIDO2/WebAuthn) binds the credential to the real site, so it cannot be replayed on a fake login page."),
    ("MFA fatigue", "Attack where an attacker repeatedly triggers MFA prompts hoping the user approves one out of frustration."),
    ("NIST", "U.S. National Institute of Standards and Technology. Publishes the Cybersecurity Framework and SP 800-61 for incident response."),
    ("Phishing", "Deceptive messages (email, SMS, voice, web) that trick users into entering credentials, running malware, or approving fraudulent transactions."),
    ("Ransomware", "Malware that encrypts files and/or steals data, then demands payment to restore access or to prevent publication."),
    ("RDP", "Remote Desktop Protocol. Frequently abused by attackers when exposed to the internet without strong controls."),
    ("Segmentation", "Dividing a network into zones so a compromise in one area can't spread freely to others."),
    ("Tabletop exercise", "A facilitated discussion-based drill where leaders walk through their response to a hypothetical incident."),
    ("Third-party risk", "Risk introduced by vendors, SaaS providers, and contractors. Recent higher-ed ransomware impact has been driven heavily by exploited third-party software."),
]


FAQ = [
    ("What even is ransomware, in plain terms?",
     "Software that locks up your files (and usually steals copies first) so someone can charge you to unlock them, or to not leak them. As a student you mostly see the way in: phishing emails, fake login pages, and account takeovers."),
    ("Why should I care? Isn't this an IT problem?",
     # Every clause in the answer below is anchored to a named higher-ed institution
     # documenting compromised STUDENT (not faculty/staff) accounts, on the record:
     #
     #   - "taken over by phishing, used to send more phishing to classmates":
     #     Morehouse College ITS, reported by The Maroon Tiger (2 Aug 2025).
     #     Morehouse ITS confirmed student accounts were compromised and used to send
     #     phishing to other students (fake job, work-study, and direct-funding lures).
     #     https://maroontigermedia.com/2025/08/phishing-morehouse-emails-student-hacking/
     #
     #   - "reset passwords or change account-recovery settings to keep access":
     #     University of Utah Information Security Office (Nov 2021).
     #     "recent attackers have used a combination of phished and socially-engineered
     #     information to reset user passwords, allowing the attackers to keep using
     #     compromised accounts even after the password has been changed."
     #     https://attheu.utah.edu/announcements/students-face-increasing-phishing-and-other-cyberattacks/
     #
     # Claims removed during 2026-05 review for lack of clean public-source support
     # for the *compromised-student-account* pathway specifically:
     #   - "attack faculty" (cited cases like Sac State 2020, Oregon State 2019, Duke 2014
     #     are all compromised FACULTY/STAFF accounts, not students)
     #   - "raid scholarship funds" (documented federal aid fraud is overwhelmingly
     #     synthetic-identity / bot fraud, not real student account takeover)
     #   - "exfiltrate course rosters" (no clean documented case of a compromised
     #     student account being used to exfiltrate rosters)
     "Your account is the easiest way in. Universities have documented student accounts being taken over by phishing, then used to send more phishing to classmates from a trusted address, and to reset passwords or change account-recovery settings so attackers keep access even after the original password is changed. A single careless click can affect your grades, financial aid, and the people around you."),
    ("I think I clicked a phishing link. What now?",
     "Stop using the device. From a different device (your phone is fine), change the password for the affected account, then call the campus IT help desk. Keep the original message. IT may need it. Speed matters more than embarrassment."),
    ("My laptop is showing a ransom note. What should I do?",
     "Don't pay anything. Disconnect from Wi-Fi and unplug any cables, but leave the device powered on (forensics may need volatile memory). Call campus IT right now. Don't try to 'fix' it yourself."),
    ("Is the campus going to discipline me if I report a mistake?",
     # "Most campuses have a non-punitive reporting culture" was an unsourced empirical
     # claim about institutional behavior; reframed to "Check your campus policy" with
     # a directional argument that doesn't require quantifying campus policies.
     "Many campuses encourage honest reporting and treat accidental clicks differently from intentional misconduct. They need the data to defend everyone. Check your campus policy, but in general the cost of not reporting is worse than the cost of reporting."),
    ("Should I use a personal device for schoolwork?",
     "Generally fine if it's up to date, has MFA on your campus account, and you don't pirate software on it. Some courses or programs (e.g., clinical, legal, research with sensitive data) require institution-managed devices. Check your syllabus."),
    ("Is MFA actually worth the hassle?",
     # MFA effectiveness framing anchored to CISA's public position; specific quantitative
     # claims (e.g., the older Microsoft "99.9%") have been eroded by adversary-in-the-middle
     # and Duo-OTP-theft campaigns documented in 2024-2025, so we describe it directionally.
     # See: https://www.cisa.gov/MFA
     "Yes. Multi-factor authentication is one of the most important things you can do to protect an account, and CISA recommends it for everyone. Phishing-resistant MFA (FIDO2 / passkeys / hardware keys like YubiKey) is the strongest form because the credential is bound to the legitimate site. Enable it wherever your campus offers it."),
    ("Is public Wi-Fi at the coffee shop dangerous?",
     "Less than it used to be. Most sites and apps use HTTPS by default. Still a good idea to avoid logging into your campus account from networks you don't trust, and to use your campus VPN if your school provides one."),
    ("Can this site substitute for legal advice?",
     "No. This is a plain-language educational summary. Specific obligations under FERPA, state breach laws, or your campus policies depend on your situation. Talk to your IT help desk, dean of students, or campus counsel."),
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
    ("University of Utah ISO: Students Face Increasing Phishing and Other Cyberattacks (2021)", "https://attheu.utah.edu/announcements/students-face-increasing-phishing-and-other-cyberattacks/",
     "University of Utah Information Security Office advisory documenting compromised student accounts and attackers using socially-engineered information to reset passwords and maintain access."),
    ("The Maroon Tiger: Several Morehouse students fall victim to phishing emails (2025)", "https://maroontigermedia.com/2025/08/phishing-morehouse-emails-student-hacking/",
     "Student newspaper reporting, with Morehouse College ITS confirmation, of compromised student accounts being used to send phishing to other students (fake job, work-study, and direct-funding lures)."),
    ("Tischer et al., 'Users Really Do Plug in USB Drives They Find' (IEEE Security & Privacy, 2016)", "https://research.google/pubs/users-really-do-plug-in-usb-drives-they-find/",
     "University of Illinois / Google research demonstrating that 45-98% of dropped USB drives were plugged in by finders, with first drives connected in under six minutes."),
    ("No More Ransom Project", "https://www.nomoreransom.org/",
     "Europol-backed clearinghouse of legitimate, free ransomware decryption tools. Use only at the direction of IT or law enforcement, never as a first response."),
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
        "title": "The 'IT Help Desk' email",
        "blurb": "A panic-inducing email about your account.",
        "situation": (
            "It's 11:47 PM. Your paper's due tomorrow. An email shows up: "
            "'ACTION REQUIRED: Your campus account will be deleted in 24 hours.' "
            "It tells you to click a link and 'verify your identity' or you'll lose your coursework. "
            "The sender has your school's name in it, but the part after the @ isn't quite right."
        ),
        "start": "n0",
        "nodes": {
            "n0": {"type": "decision", "q": "What do you do first?", "choices": [
                {"label": "Click the link to check whether it's real.",
                 "next": "n_clicked", "score": 1, "tag": "risky"},
                {"label": "Look at the sender's full email address and the link before doing anything.",
                 "next": "n_inspect", "score": -1, "tag": "good"},
                {"label": "Reply to the sender asking if it's legit.",
                 "next": "n_replied", "score": 1, "tag": "risky"},
                {"label": "Enter your password on the linked page so you don't lose access.",
                 "next": "out_creds", "score": 2, "tag": "bad"},
            ]},
            "n_inspect": {"type": "decision",
                "q": "The sender domain is 'mail-university-support.com' and the link goes to a Google Form. What now?", "choices": [
                {"label": "Report the message using my campus 'Report Phishing' button (or forward it as an attachment to the security team) and delete it.",
                 "next": "out_reported", "score": -2, "tag": "good"},
                {"label": "Forward it to a friend to warn them.",
                 "next": "out_forwarded", "score": 1, "tag": "risky"},
                {"label": "Ignore it.",
                 "next": "out_ignored", "score": 0, "tag": "ok"},
            ]},
            "n_clicked": {"type": "decision",
                "q": "The page looks exactly like your school's login. What now?", "choices": [
                {"label": "Close the tab without entering anything and report the email.",
                 "next": "out_close_report", "score": -1, "tag": "good"},
                {"label": "Type in my username and password to 'check.'",
                 "next": "out_creds", "score": 2, "tag": "bad"},
            ]},
            "n_replied": {"type": "outcome", "tag": "risky", "score": 1,
                "title": "Replying confirms your address is active.",
                "body": "Replying tells the attacker someone's reading the inbox. You'll get more targeted messages now. Don't reply to phishing. Report it and delete it.",
                "links": [("If something goes wrong", "response.html")]},
            "out_creds": {"type": "outcome", "tag": "bad", "score": 2,
                "title": "Your campus password is probably stolen.",
                "body": "You just typed your campus password into a page controlled by an attacker. From a different device (your phone is fine), change your campus password right now, sign out of all sessions, and call the IT help desk. Keep the original email as evidence. Don't use the suspect device for anything sensitive until IT clears it.",
                "links": [("If something goes wrong", "response.html"), ("Sources", "references.html")]},
            "out_reported": {"type": "outcome", "tag": "good", "score": -2,
                "title": "That's what to do.",
                "body": "Checking the sender and the link before you click is the habit that catches most of these. Reporting through the campus tool also helps IT block the lure for everyone else.",
                "links": [("Protect yourself", "prevention.html")]},
            "out_forwarded": {"type": "outcome", "tag": "risky", "score": 1,
                "title": "Well-intentioned, but risky.",
                "body": "Forwarding the live message can lead a friend to click. Report it through your campus tool instead, and tell friends about the pattern in your own words ('watch out for fake IT deletion emails right now').",
                "links": [("If something goes wrong", "response.html")]},
            "out_ignored": {"type": "outcome", "tag": "ok", "score": 0,
                "title": "Safe, but you missed the upside.",
                "body": "Ignoring kept you safe. Reporting is better. It lets the security team block the lure for everyone else and pull the page down faster.",
                "links": [("Protect yourself", "prevention.html")]},
            "out_close_report": {"type": "outcome", "tag": "good", "score": -1,
                "title": "Solid recovery.",
                "body": "Closing without entering credentials limits the damage to maybe a tracking pixel. Report the email so the security team can pull the page down. If you have any doubt about whether you typed something, change your password from a different device.",
                "links": [("If something goes wrong", "response.html")]},
        },
    },
    # ----------------------------------------------------------------------
    {
        "id": "fake-canvas-login",
        "title": "The Canvas link that wasn't",
        "blurb": "A link from a TA leads to a login page.",
        "situation": (
            "Your TA shares 'a quick poll for Friday's class' in the course Discord. "
            "The link opens a page that looks like your school's Canvas login, but the "
            "URL in the address bar reads 'canvas-myschool-edu.app/auth'."
        ),
        "start": "n0",
        "nodes": {
            "n0": {"type": "decision", "q": "What do you notice first?", "choices": [
                {"label": "The URL doesn't end in my school's real domain. Stop.",
                 "next": "n_stopped", "score": -1, "tag": "good"},
                {"label": "It looks like Canvas, so just sign in to take the poll.",
                 "next": "out_creds_canvas", "score": 2, "tag": "bad"},
                {"label": "DM the TA on a separate channel to ask if they posted this.",
                 "next": "n_dm", "score": -1, "tag": "good"},
            ]},
            "n_stopped": {"type": "decision",
                "q": "What next?", "choices": [
                {"label": "Open Canvas by typing my school's URL myself, and check there for the poll.",
                 "next": "out_typed_url", "score": -2, "tag": "good"},
                {"label": "Refresh the page in case it loads correctly the second time.",
                 "next": "out_refresh", "score": 1, "tag": "risky"},
            ]},
            "n_dm": {"type": "outcome", "tag": "good", "score": -2,
                "title": "Verify out of band. Good instinct.",
                "body": "Asking the TA through a different channel (text, in person, official email) is one of the cleanest ways to verify a suspicious link. If their Discord was compromised, the impostor will often answer 'yes, it's real.' Trust the out-of-band reply, not the in-channel one.",
                "links": [("Protect yourself", "prevention.html")]},
            "out_creds_canvas": {"type": "outcome", "tag": "bad", "score": 2,
                "title": "Your Canvas (and possibly campus) password is now exposed.",
                "body": "Many schools use the same SSO for Canvas, email, and the student portal, so this could be your master credential. From a different device, change your campus password right now, revoke active sessions, and tell IT. Mention that the lure came from a TA's Discord. It's a clue the TA's account is compromised, too.",
                "links": [("If something goes wrong", "response.html")]},
            "out_typed_url": {"type": "outcome", "tag": "good", "score": -2,
                "title": "Good habit.",
                "body": "Typing the URL yourself (or using your own bookmark) defeats almost all credential-harvesting pages, because the attacker can't intercept what you typed into your own address bar. Report the original link so IT can take it down.",
                "links": [("Protect yourself", "prevention.html")]},
            "out_refresh": {"type": "outcome", "tag": "risky", "score": 1,
                "title": "Refreshing doesn't fix a fake page.",
                "body": "A reload just reloads the attacker's page. The URL is your evidence. If it doesn't match your school's domain, treat the page as hostile and leave. Report the link.",
                "links": [("Protect yourself", "prevention.html")]},
        },
    },
    # ----------------------------------------------------------------------
    {
        "id": "dorm-ransom-note",
        "title": "The dorm laptop ransom note",
        "blurb": "Your roommate's gaming laptop is screaming for Bitcoin.",
        "situation": (
            "You walk into your dorm and your roommate's laptop is open on the desk. "
            "The screen shows a red ransom note demanding $400 in Bitcoin to 'decrypt your files.' "
            "Your roommate isn't home. The laptop is plugged in via Ethernet to the dorm jack."
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
                "q": "Good. The laptop is isolated. Now what?", "choices": [
                {"label": "Take a photo of the note, write down the time, and call the campus IT help desk.",
                 "next": "out_isolated_called", "score": -2, "tag": "good"},
                {"label": "Try to recover files with a 'free ransomware decryptor' I just searched for.",
                 "next": "out_decryptor", "score": 2, "tag": "bad"},
                {"label": "Pay the $400 quickly so my roommate doesn't lose their files.",
                 "next": "out_paid", "score": 2, "tag": "bad"},
            ]},
            "n_photo": {"type": "outcome", "tag": "ok", "score": 0,
                "title": "Helpful evidence, but the device is still on the network.",
                "body": "A photo is great for IT, but while the device is still on the network, the malware may be reaching out to attacker infrastructure, encrypting cloud-synced files, or attacking other devices on the dorm Wi-Fi. Disconnect first, then photograph, then call IT.",
                "links": [("If something goes wrong", "response.html")]},
            "out_powered_off": {"type": "outcome", "tag": "risky", "score": 1,
                "title": "Powering off destroys evidence.",
                "body": "Volatile memory often contains the encryption key or attacker indicators that responders use to recover files. Leave the device powered on but disconnected from networks. This is exactly opposite to what feels intuitive.",
                "links": [("If something goes wrong", "response.html")]},
            "out_clicked_note": {"type": "outcome", "tag": "bad", "score": 2,
                "title": "Don't interact with the note.",
                "body": "Some ransom notes have 'chat' or 'test decrypt' buttons that escalate the attack, start a deadline timer, or send your IP to the attacker. Don't click anything. Disconnect from the network, photograph the screen, and call IT.",
                "links": [("If something goes wrong", "response.html")]},
            "out_isolated_called": {"type": "outcome", "tag": "good", "score": -2,
                "title": "Exactly right.",
                "body": "Isolate, photograph, call. That sequence, even if it's your roommate's personal device, gives the responders volatile memory, the lock-screen text, and an accurate timeline. Tell your roommate as soon as you reach them.",
                "links": [("Protect yourself", "prevention.html")]},
            "out_decryptor": {"type": "outcome", "tag": "bad", "score": 2,
                # Original draft said "almost always more malware" — that's too strong.
                # Legitimate free decryptors do exist (NoMoreRansom.org, Emsisoft, Kaspersky
                # No Ransom). The actionable point is: do NOT download decryptors from
                # random search/YouTube results without IT's go-ahead.
                "title": "Search-result 'decryptors' are a common scam.",
                "body": "Search results for 'ransomware decryptor' are saturated with second-stage malware that finishes the job. Real decryption tools (when they exist) are released by law enforcement or vetted vendors like Europol's No More Ransom. Applying them is something IT or a forensic responder should do, not a panicking student.",
                "links": [("If something goes wrong", "response.html")]},
            "out_paid": {"type": "outcome", "tag": "bad", "score": 2,
                "title": "Don't pay.",
                "body": "Most ransomware payments don't produce a working key, and many fund sanctioned criminal groups. Paying also marks your roommate (and your dorm) as soft targets. Call IT instead. They can advise on what backups, cloud restore, or device replacement looks like.",
                "links": [("If something goes wrong", "response.html"), ("Sources", "references.html")]},
        },
    },
    # ----------------------------------------------------------------------
    {
        "id": "mfa-fatigue",
        "title": "The 2 AM MFA prompts",
        "blurb": "Your phone is buzzing with login requests you didn't make.",
        "situation": (
            "At 2:11 AM your phone buzzes with an MFA push notification. 'Approve sign-in?' "
            "You ignore it. Two minutes later, another. By 2:20 AM you've had nine prompts in a row. "
            "You're not trying to sign in to anything."
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
                {"label": "Done. Go back to sleep.",
                 "next": "out_partial", "score": 0, "tag": "ok"},
            ]},
            "out_approved": {"type": "outcome", "tag": "bad", "score": 2,
                "title": "MFA fatigue attack succeeded.",
                # "Most effective against student accounts" was a stronger claim than the
                # public evidence supports. MFA fatigue / push bombing is a well-documented
                # tactic generally (e.g., CISA AA22-074A) but I don't have a clean source
                # specifically ranking it for student-account compromise.
                "body": "MFA fatigue (also called 'push bombing') is a documented attack tactic — attackers spam you with prompts hoping you'll tap 'approve' just to make them stop. By approving one push, you likely handed someone access. From a different device, change your password, sign out of all sessions, and call IT first thing in the morning. Earlier if your campus has 24/7 IT.",
                "links": [("If something goes wrong", "response.html")]},
            "out_dnd": {"type": "outcome", "tag": "risky", "score": 1,
                "title": "Quiet doesn't mean safe.",
                "body": "DND silences the prompts but doesn't stop the attempts. The attacker has your password and is trying to bypass MFA. By tomorrow morning they may have tried hundreds of logins, social engineered your helpdesk, or pivoted to your email recovery. Change the password tonight, even if it's annoying.",
                "links": [("If something goes wrong", "response.html")]},
            "out_reported_morning": {"type": "outcome", "tag": "ok", "score": 0,
                "title": "Better than approving, but slow.",
                "body": "Denying is good. Waiting until morning is risky. The attacker has your password and is hammering MFA. Change the password now from a different device. Reporting can wait until the help desk opens.",
                "links": [("If something goes wrong", "response.html")]},
            "out_full_response": {"type": "outcome", "tag": "good", "score": -2,
                "title": "That's the full response.",
                "body": "Deny the prompt, change your password, sign out all sessions, review login history. If your school offers phishing-resistant MFA (FIDO2, hardware key, or platform passkey), this is a good moment to enroll.",
                "links": [("Protect yourself", "prevention.html"), ("Sources", "references.html")]},
            "out_partial": {"type": "outcome", "tag": "ok", "score": 0,
                "title": "Halfway there.",
                "body": "Changing the password is critical, but active sessions stay valid until you sign them out. Also check your account's recent login history. Most providers show it in your account settings.",
                "links": [("Protect yourself", "prevention.html")]},
        },
    },
    # ----------------------------------------------------------------------
    {
        "id": "job-scam",
        "title": "The 'paid research assistant' DM",
        "blurb": "A professor you don't recognize offers you $40/hr.",
        "situation": (
            "Someone DMs you on LinkedIn claiming to be a visiting professor in your department. "
            "They're 'urgently hiring a paid research assistant for remote work: $40/hr, 10 hrs/week.' "
            "They ask for your personal email so they can send a contract, and request you Venmo $75 "
            "for 'software setup' that they'll reimburse with your first paycheck."
        ),
        "start": "n0",
        "nodes": {
            "n0": {"type": "decision", "q": "What do you do?", "choices": [
                {"label": "Send the $75. It's reimbursable and the rate is amazing.",
                 "next": "out_paid_scam", "score": 2, "tag": "bad"},
                {"label": "Reply asking for their campus email and look them up in the school directory first.",
                 "next": "n_verify", "score": -1, "tag": "good"},
                {"label": "Give them your personal email but not the money.",
                 "next": "out_handed_email", "score": 1, "tag": "risky"},
                {"label": "Block and report. Anyone asking a student to pay upfront is a scam.",
                 "next": "out_blocked", "score": -2, "tag": "good"},
            ]},
            "n_verify": {"type": "decision",
                "q": "There's no faculty member by that name in the directory. They reply with a generic Gmail address. What now?", "choices": [
                {"label": "Block and report to LinkedIn, then warn classmates.",
                 "next": "out_blocked", "score": -2, "tag": "good"},
                {"label": "Send them $75 anyway. The rate is too good to pass up.",
                 "next": "out_paid_scam", "score": 2, "tag": "bad"},
            ]},
            "out_paid_scam": {"type": "outcome", "tag": "bad", "score": 2,
                "title": "Student job scam. Money is gone.",
                "body": "Real employers don't ask candidates to pay them, period. The $75 is gone, and depending on what info you shared, you may be on a list for follow-on identity theft (fake check, phony tax forms, etc.). Report the fraud to LinkedIn, your bank/Venmo, and the FBI IC3.",
                "links": [("If something goes wrong", "response.html"), ("Sources", "references.html")]},
            "out_handed_email": {"type": "outcome", "tag": "risky", "score": 1,
                "title": "You traded contact info for a relationship with a scammer.",
                "body": "They'll use your personal email to send convincing follow-ups, fake checks to deposit, or phishing that uses your name correctly. Stop responding, block the account, and watch your personal email closely for the next month.",
                "links": [("Protect yourself", "prevention.html")]},
            "out_blocked": {"type": "outcome", "tag": "good", "score": -2,
                "title": "Pattern matched correctly.",
                "body": "Upfront 'software fee,' unreal-sounding rate, off-platform contact, unverifiable identity. That's the modern student job scam. Reporting on LinkedIn helps the platform shut the account down before it hits your classmates.",
                "links": [("Protect yourself", "prevention.html"), ("Sources", "references.html")]},
        },
    },
    # ----------------------------------------------------------------------
    {
        "id": "financial-aid",
        "title": "'Verify your FAFSA refund'",
        "blurb": "A text says your aid disbursement is on hold.",
        "situation": (
            "You get a text: '[University] Financial Aid: Your refund of $1,432.18 is on hold. "
            "Verify your bank info within 12 hours to prevent reversal: hxxps://fin-aid-portal-myschool.com'."
        ),
        "start": "n0",
        "nodes": {
            "n0": {"type": "decision", "q": "What do you do?", "choices": [
                {"label": "Tap the link and enter my bank login so I don't lose the refund.",
                 "next": "out_bank_creds", "score": 2, "tag": "bad"},
                {"label": "Open my actual student portal in a browser and check there.",
                 "next": "n_portal_check", "score": -2, "tag": "good"},
                {"label": "Call the financial aid office using the number from the school's real website.",
                 "next": "out_called_office", "score": -2, "tag": "good"},
                {"label": "Reply 'STOP'.",
                 "next": "out_reply_stop", "score": 1, "tag": "risky"},
            ]},
            "n_portal_check": {"type": "outcome", "tag": "good", "score": -2,
                "title": "Right channel.",
                "body": "Your student portal is the source of truth. If there's really a hold, it's there. 'Verify within 12 hours' urgency, an unfamiliar domain, and a request for bank credentials are three classic phishing signals stacked in one message.",
                "links": [("Protect yourself", "prevention.html")]},
            "out_called_office": {"type": "outcome", "tag": "good", "score": -2,
                "title": "Best move. Verify by voice.",
                "body": "Calling the office using a number you find on the school's real website (not from the text) confirms in seconds whether anything is actually wrong. This works for 'unpaid tuition,' 'scholarship deactivated,' and similar lures too.",
                "links": [("Protect yourself", "prevention.html")]},
            "out_bank_creds": {"type": "outcome", "tag": "bad", "score": 2,
                "title": "Bank credentials compromised.",
                "body": "Call your bank right now, freeze the account, and change online-banking credentials from a clean device. File a fraud report at ic3.gov and with your school's financial aid office. Watch for follow-on impersonation. Scammers often parlay one win into another ('this is your bank fraud team').",
                "links": [("If something goes wrong", "response.html"), ("Sources", "references.html")]},
            "out_reply_stop": {"type": "outcome", "tag": "risky", "score": 1,
                "title": "STOP confirms you read it.",
                "body": "Replying, even with 'STOP,' confirms the number is live and you opened the message. Don't reply. Don't click. Delete and, if you have an iPhone or Android, report as junk.",
                "links": [("Protect yourself", "prevention.html")]},
        },
    },
    # ----------------------------------------------------------------------
    {
        "id": "club-drive",
        "title": "The club Google Drive looks weird",
        "blurb": "Files renamed, weird shares, missing folders.",
        "situation": (
            "You're the secretary of a campus club. This morning, your shared Google Drive shows "
            "two folders missing, several files renamed to 'encrypted-by-…' style names, and a new "
            "'share' to an external Gmail address you don't recognize. The club president is in class."
        ),
        "start": "n0",
        "nodes": {
            "n0": {"type": "decision", "q": "First move?", "choices": [
                {"label": "Right away, revoke the unknown external share and lock down sharing on the affected files.",
                 "next": "n_locked", "score": -1, "tag": "good"},
                {"label": "Delete the weird files so they're not visible.",
                 "next": "out_deleted", "score": 1, "tag": "risky"},
                {"label": "Restore older versions of the files from version history while figuring out what happened.",
                 "next": "n_restored", "score": -1, "tag": "good"},
                {"label": "Ignore it. Probably a Drive glitch.",
                 "next": "out_ignored", "score": 1, "tag": "risky"},
            ]},
            "n_locked": {"type": "decision",
                "q": "Sharing is locked. Next?", "choices": [
                {"label": "Notify campus IT, then change the password and revoke active sessions on the club's owning account.",
                 "next": "out_full_clean", "score": -2, "tag": "good"},
                {"label": "Just tell the president when you next see them.",
                 "next": "out_delayed", "score": 1, "tag": "risky"},
            ]},
            "n_restored": {"type": "decision",
                "q": "Files are restoring. What else?", "choices": [
                {"label": "Also revoke unknown shares and notify IT. Restoration alone doesn't kick the attacker out.",
                 "next": "out_full_clean", "score": -2, "tag": "good"},
                {"label": "Done. Files are back.",
                 "next": "out_left_attacker", "score": 1, "tag": "risky"},
            ]},
            "out_deleted": {"type": "outcome", "tag": "risky", "score": 1,
                "title": "You destroyed the evidence.",
                "body": "Deleting the encrypted files removes the forensic trail and might also delete the only artifact that can identify the actor. Restore from version history instead, revoke the bad share, and tell IT.",
                "links": [("If something goes wrong", "response.html")]},
            "out_ignored": {"type": "outcome", "tag": "risky", "score": 1,
                "title": "It's almost certainly not a glitch.",
                "body": "Missing folders, renamed files, and an unknown external share is the signature of an account takeover or a ransomware actor targeting cloud storage. Don't wait. Revoke the share now and tell IT.",
                "links": [("If something goes wrong", "response.html")]},
            "out_full_clean": {"type": "outcome", "tag": "good", "score": -2,
                "title": "Good, clean response.",
                "body": "Revoke the unknown share, restore from version history, change the owner account's password, sign out all sessions, and loop in IT. That sequence cuts the attacker's access without losing your data. Tell the president as soon as they're free.",
                "links": [("Protect yourself", "prevention.html")]},
            "out_delayed": {"type": "outcome", "tag": "risky", "score": 1,
                "title": "Speed matters more than chain-of-command.",
                "body": "While you wait, the attacker may rename or re-share more files. Loop in campus IT now. A 5-minute conversation is fine. Message the president on the side.",
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
            "n0": {"type": "decision", "q": "First five minutes: what do you do?", "choices": [
                {"label": "Find another device, sign in to my campus account, and sign out of all sessions everywhere.",
                 "next": "n_signed_out", "score": -2, "tag": "good"},
                {"label": "Wait at the library in case it's a prank.",
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
                {"label": "Done. Go home and finish my thesis tomorrow.",
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
                "body": "Sign out everywhere, change your password, file the police/security report, then use Find My to mark the device lost (which often forces a remote lock). If you have campus device-encryption (FileVault, BitLocker), the thief is mostly facing a brick. Your thesis backup in OneDrive / Google Drive / iCloud should still be intact.",
                "links": [("Protect yourself", "prevention.html")]},
            "out_waited": {"type": "outcome", "tag": "risky", "score": 1,
                "title": "Time isn't on your side.",
                "body": "Every minute the device is unlocked is a minute someone can read your email, copy your files, or pivot into your accounts. File the report after taking online containment steps. Don't leave a stolen, unlocked laptop alive on your campus account.",
                "links": [("If something goes wrong", "response.html")]},
            "out_chase": {"type": "outcome", "tag": "bad", "score": 2,
                "title": "Don't physically pursue.",
                "body": "Find My is for evidence and remote lock, not for you to confront a thief. Share the location with campus police or local police and let them act. Your safety and the data containment matter more than recovering the device.",
                "links": [("If something goes wrong", "response.html")]},
            "out_thesis_lost": {"type": "outcome", "tag": "risky", "score": 1,
                "title": "Half done.",
                "body": "Sessions ended, but the device may still have remembered passwords in the browser, an active Outlook profile, and saved cookies for other sites. Change the campus password and any reused passwords now from a different device.",
                "links": [("Protect yourself", "prevention.html")]},
            "out_wait_for_police": {"type": "outcome", "tag": "risky", "score": 1,
                "title": "Police won't do the online steps for you.",
                "body": "Campus police handle the physical investigation, not your account containment. Don't wait. Sign out, change the password, and tell IT in parallel.",
                "links": [("If something goes wrong", "response.html")]},
        },
    },
    # ----------------------------------------------------------------------
    {
        "id": "roommate-login",
        "title": "The roommate who wants 'just one login'",
        "blurb": "'Can I use yours? Mine glitched out.'",
        "situation": (
            "Your roommate asks if they can borrow your campus login to access the library's "
            "paid databases for an essay due tomorrow. They say theirs 'glitched out' and they "
            "don't want to wait for the help desk to open."
        ),
        "start": "n0",
        "nodes": {
            "n0": {"type": "decision", "q": "How do you respond?", "choices": [
                {"label": "Hand them my password. They're a friend.",
                 "next": "out_shared", "score": 2, "tag": "bad"},
                {"label": "Let them use my account on my laptop while I watch.",
                 "next": "out_supervised", "score": 1, "tag": "risky"},
                {"label": "Politely refuse and help them open a help desk ticket / use 24/7 self-service password reset.",
                 "next": "out_helped", "score": -2, "tag": "good"},
                {"label": "Tell them most universities have public-library or open-access alternatives, and help them find the article.",
                 "next": "out_helped_alt", "score": -2, "tag": "good"},
            ]},
            "out_shared": {"type": "outcome", "tag": "bad", "score": 2,
                "title": "Account sharing is a policy violation and a security problem.",
                "body": "Your school's acceptable-use policy almost certainly forbids password sharing. If your roommate gets compromised or does something questionable while signed in as you, you're the one in the logs. Even if you trust them, change your password the moment they're done. Don't do it again.",
                "links": [("If something goes wrong", "response.html"), ("FAQ", "faq.html")]},
            "out_supervised": {"type": "outcome", "tag": "risky", "score": 1,
                "title": "Still risky.",
                "body": "Supervised use limits some damage, but downloads, browser cookies, and screen captures can persist. And from the library's perspective, the database access is logged as you. Better path: help them recover their own access.",
                "links": [("FAQ", "faq.html")]},
            "out_helped": {"type": "outcome", "tag": "good", "score": -2,
                "title": "Good call.",
                "body": "Most universities offer 24/7 self-service password reset and an after-hours help desk number. Help them open a ticket and tell them you'd expect the same back.",
                "links": [("Protect yourself", "prevention.html")]},
            "out_helped_alt": {"type": "outcome", "tag": "good", "score": -2,
                "title": "Underrated answer.",
                "body": "Public libraries, Google Scholar, the Internet Archive, and many publishers' 'read-only' links can unblock a single article in minutes. Often the fastest way to help a friend is the route that doesn't involve your password at all.",
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
            "No label, no name, no return-address sticker. You wonder if it's a classmate's lost drive."
        ),
        "start": "n0",
        "nodes": {
            "n0": {"type": "decision", "q": "What do you do?", "choices": [
                {"label": "Plug it into my laptop to look for the owner's name.",
                 "next": "out_plugged", "score": 2, "tag": "bad"},
                {"label": "Drop it off at the library lost-and-found or campus IT.",
                 "next": "out_lostfound", "score": -2, "tag": "good"},
                {"label": "Throw it away. Too risky.",
                 "next": "out_threw", "score": 0, "tag": "ok"},
                {"label": "Plug it into a school computer in a public lab to 'check.'",
                 "next": "out_lab_pc", "score": 2, "tag": "bad"},
            ]},
            "out_plugged": {"type": "outcome", "tag": "bad", "score": 2,
                "title": "USB drop attacks are real.",
                # Original draft claimed "a surprising fraction of found USB drives are
                # deliberate drop attacks." The actual citable research finding is the
                # ATTACK SUCCESS RATE (Tischer et al., 2016, UIUC/Google: 45-98% of dropped
                # drives get plugged in), not the share of found drives that are malicious.
                # Rewrote to match what the research actually says.
                # Source: https://research.google/pubs/users-really-do-plug-in-usb-drives-they-find/
                "body": "Researchers have shown USB drop attacks work: in a 2016 University of Illinois study, 45-98% of dropped drives got plugged in. Some emulate keyboards, some auto-run malware, some install hardware-level implants. Don't plug an unknown drive into any device you care about. If you already did, disconnect from the network and call IT.",
                "links": [("If something goes wrong", "response.html"), ("Sources", "references.html")]},
            "out_lostfound": {"type": "outcome", "tag": "good", "score": -2,
                "title": "Right answer.",
                "body": "Library or IT lost-and-found is where it belongs. They have isolated equipment to identify the owner safely if needed. You stay out of the malware loop, and the actual owner has a real chance of getting it back.",
                "links": [("Protect yourself", "prevention.html")]},
            "out_threw": {"type": "outcome", "tag": "ok", "score": 0,
                "title": "Safe, but unkind to the real owner.",
                "body": "Throwing it away is safe for you but discards what might be a classmate's research. Lost-and-found is a better default. It also means the next person doesn't find and plug it in.",
                "links": [("Protect yourself", "prevention.html")]},
            "out_lab_pc": {"type": "outcome", "tag": "bad", "score": 2,
                "title": "The lab PC isn't a sandbox.",
                "body": "Lab PCs are connected to the campus network and often have shared drives mapped. Plugging an unknown USB into one can compromise far more than your laptop would. If you already did, leave the PC alone, note the time, and tell IT.",
                "links": [("If something goes wrong", "response.html")]},
        },
    },
]


# ============================================================================
# DORM ROOM INCIDENT LAB — 10 short room-anchored incident modules.
# ----------------------------------------------------------------------------
# Each module:
#   id, hotspot, title, blurb, setup, start (node id), nodes {...}, aar [list].
#
# hotspot       short label tied to a fixture in the dorm scene
#                ("laptop","phone","router","printer","roommate",
#                 "clouddrive","campusemail","clubaccount","usbstick")
# nodes         same shape as SCENARIOS but shorter — 2 decisions max + outcome
# aar           after-action review checklist (4–6 items, each a 1-line habit)
#                shown after the outcome; checking items raises overall
#                readiness. AAR items are unique habits, not module-specific.
#
# Authoring rules (per repo guidance):
#   - Plain, directive, student-friendly language.
#   - Distinguish general guidance from institution-specific policies.
#   - Never describe how to attack, deploy ransomware, or evade defenses.
#   - All modules are everyday situations a student could encounter at home,
#     in the dorm, in a shared kitchen, at a club meeting, or in the library.
# ============================================================================

LAB = [
    {
        "id": "laptop-encrypted",
        "hotspot": "laptop",
        "title": "Your laptop is encrypted before finals",
        "blurb": "It's 11 PM the night before your final. Your laptop screen shows a ransom note.",
        "setup": (
            "You sit down to finish your paper. Instead of your desktop you see a black screen "
            "with red text: 'All your files are encrypted. Pay 0.05 BTC within 48 hours or lose them.' "
            "Your draft, your notes, and your reference manager library all appear gone."
        ),
        "start": "n0",
        "nodes": {
            "n0": {"type": "decision", "q": "What's your first move?", "choices": [
                {"label": "Pull the Wi-Fi switch / unplug the Ethernet cable so nothing else gets reached.",
                 "next": "n1", "score": -2, "tag": "good"},
                {"label": "Power the laptop off so it 'stops' the encryption.",
                 "next": "out_power", "score": 1, "tag": "risky"},
                {"label": "Pay the 0.05 BTC. The paper is worth it.",
                 "next": "out_pay", "score": 2, "tag": "bad"},
                {"label": "Open a browser on the same laptop and search for a decryptor.",
                 "next": "out_browse", "score": 1, "tag": "risky"},
            ]},
            "n1": {"type": "decision",
                "q": "You're offline. Now what?", "choices": [
                {"label": "Call the campus IT help desk from my phone, describe what I saw, leave the laptop on, and don't touch keys.",
                 "next": "out_call", "score": -2, "tag": "good"},
                {"label": "Try to copy any visible files to a USB drive to 'save what I can.'",
                 "next": "out_copy", "score": 2, "tag": "bad"},
                {"label": "Reinstall the operating system to clean it up.",
                 "next": "out_reinstall", "score": 1, "tag": "risky"},
            ]},
            "out_power": {"type": "outcome", "tag": "risky", "score": 1,
                "title": "Powering off may destroy evidence.",
                "body": "Modern ransomware sometimes leaves keys or decryption clues in memory that vanish on shutdown. Disconnect from the network instead, leave the device on, and call IT. They'll tell you when (and how) to power down.",
                "links": [("If something goes wrong", "response.html")]},
            "out_pay": {"type": "outcome", "tag": "bad", "score": 2,
                "title": "Don't pay.",
                "body": "Paying funds the next attack and rarely returns your files reliably. Talk to your professor about a deadline extension. Most schools have a process for 'device emergency' situations. Then work with IT on recovery.",
                "links": [("If something goes wrong", "response.html")]},
            "out_browse": {"type": "outcome", "tag": "risky", "score": 1,
                "title": "Don't browse from the infected machine.",
                "body": "If your account is compromised, browsing logs you in to other services and can spread the problem. Use your phone or another device.",
                "links": [("If something goes wrong", "response.html")]},
            "out_call": {"type": "outcome", "tag": "good", "score": -2,
                "title": "That's the right call.",
                "body": "Disconnect, don't power down, don't poke at it, get a human expert on the line. Bring the device to the IT help desk the next morning with your student ID. If you had cloud backup turned on, your paper is almost certainly fine.",
                "links": [("Protect yourself", "prevention.html"), ("If something goes wrong", "response.html")]},
            "out_copy": {"type": "outcome", "tag": "bad", "score": 2,
                "title": "You may have spread the infection.",
                "body": "Plugging a fresh USB into an infected machine can encrypt the USB too, and then any other computer you plug it into. Stop, label that USB 'DO NOT USE,' and tell IT what you connected and where.",
                "links": [("If something goes wrong", "response.html")]},
            "out_reinstall": {"type": "outcome", "tag": "risky", "score": 1,
                "title": "Reinstalling is premature.",
                "body": "Wiping the system before IT looks at it destroys evidence of how it happened. Call IT first. They'll tell you when a wipe is the right step.",
                "links": [("If something goes wrong", "response.html")]},
        },
        "aar": [
            "Keep cloud backup turned on for school work (OneDrive, Google Drive, iCloud, or Dropbox).",
            "Know my campus IT help desk number. Save it in my phone now.",
            "Don't plug anything into a suspect device.",
            "If a device is acting weird, disconnect from Wi-Fi first; don't power off.",
        ],
    },
    {
        "id": "roommate-clicked",
        "hotspot": "roommate",
        "title": "Your roommate clicked a sketchy link",
        "blurb": "They show you a popup demanding 'Microsoft support' on their screen.",
        "setup": (
            "Your roommate calls you over. Their laptop has a full-screen alert with a phone number "
            "and a loud voice telling them to 'call Microsoft to remove the virus.' They want to call it."
        ),
        "start": "n0",
        "nodes": {
            "n0": {"type": "decision", "q": "What do you tell them?", "choices": [
                {"label": "Don't call. Force-quit the browser (or hold the power button) and close the page; real OS alerts never demand a phone call.",
                 "next": "n1", "score": -2, "tag": "good"},
                {"label": "Call the number. At least you'll find out what they want.",
                 "next": "out_called", "score": 2, "tag": "bad"},
                {"label": "Give the screen remote access so they can 'clean it up.'",
                 "next": "out_remote", "score": 2, "tag": "bad"},
            ]},
            "n1": {"type": "decision", "q": "The popup is gone. What next?", "choices": [
                {"label": "Have them change passwords on accounts they used today (from a different device) and turn on MFA where it isn't already.",
                 "next": "out_good", "score": -2, "tag": "good"},
                {"label": "Move on. It was just a popup.",
                 "next": "out_moveon", "score": 1, "tag": "risky"},
            ]},
            "out_called": {"type": "outcome", "tag": "bad", "score": 2,
                "title": "Tech-support scam.",
                "body": "Whoever picks up will ask for remote access, gift cards, or a card number. If your roommate already called, they should hang up, not pay anything, and watch their bank account closely. If they granted remote access, treat the machine as compromised.",
                "links": [("If something goes wrong", "response.html")]},
            "out_remote": {"type": "outcome", "tag": "bad", "score": 2,
                "title": "Treat the laptop as compromised.",
                "body": "Once an attacker has remote access, they've seen everything on the screen and may have installed persistence. Disconnect from Wi-Fi, change passwords from a different device starting with email, and bring the laptop to IT.",
                "links": [("If something goes wrong", "response.html")]},
            "out_good": {"type": "outcome", "tag": "good", "score": -2,
                "title": "Good assist.",
                "body": "Killing the browser kills the lure. Rotating passwords and turning on MFA closes the most common follow-on attacks. Report the URL to IT so they can block it for everyone else.",
                "links": [("Protect yourself", "prevention.html")]},
            "out_moveon": {"type": "outcome", "tag": "risky", "score": 1,
                "title": "Probably fine, but missed an easy upgrade.",
                "body": "Most browser popups don't install anything. But the same lure usually pushes a fake download, too. Help them turn on MFA and a password manager while you're there.",
                "links": [("Protect yourself", "prevention.html")]},
        },
        "aar": [
            "Help one friend turn on MFA this week.",
            "Know how to force-quit a browser on the OS I use.",
            "Treat any phone-number popup as a scam.",
        ],
    },
    {
        "id": "club-treasurer-compromised",
        "hotspot": "clubaccount",
        "title": "Your club treasurer account was compromised",
        "blurb": "Members are getting Venmo requests from 'the club account.' It isn't you.",
        "setup": (
            "You're the treasurer of a student club. Members are screenshotting Venmo and Zelle "
            "requests from your account name asking for 'final dues this week only.' You didn't send them. "
            "When you check your phone, you're logged out."
        ),
        "start": "n0",
        "nodes": {
            "n0": {"type": "decision", "q": "What first?", "choices": [
                {"label": "From a trusted device, change my password on the payment app, then on email, then on the school account, and turn on MFA everywhere it isn't already.",
                 "next": "n1", "score": -2, "tag": "good"},
                {"label": "DM the club groupchat and tell people not to pay.",
                 "next": "out_chatonly", "score": 0, "tag": "ok"},
                {"label": "Try to log back in and message the attacker through the app.",
                 "next": "out_engage", "score": 2, "tag": "bad"},
            ]},
            "n1": {"type": "decision", "q": "Passwords are rotated. What now?", "choices": [
                {"label": "Tell the club in writing (groupchat + email): 'the account was taken over; do not send money; here's the official channel.' Report the scam to the payment app and to my campus IT.",
                 "next": "out_good", "score": -2, "tag": "good"},
                {"label": "Refund anyone who already paid out of my own pocket.",
                 "next": "out_refund", "score": 1, "tag": "risky"},
            ]},
            "out_chatonly": {"type": "outcome", "tag": "ok", "score": 0,
                "title": "Warning members helps, but the attacker still has the account.",
                "body": "Warning members is necessary but not enough. If you don't rotate passwords and turn on MFA, the attacker keeps the account. Do the password reset first, then the warning.",
                "links": [("If something goes wrong", "response.html")]},
            "out_engage": {"type": "outcome", "tag": "bad", "score": 2,
                "title": "Don't talk to the attacker.",
                "body": "Engaging signals the account is live and you're paying attention. It also tempts you to 'negotiate.' Lock them out via password reset and MFA, then report. Don't reply.",
                "links": [("If something goes wrong", "response.html")]},
            "out_good": {"type": "outcome", "tag": "good", "score": -2,
                "title": "You handled it.",
                "body": "Rotate credentials, tell people in writing, report. Keep a short timeline of what happened so the next treasurer can learn from it. Consider moving club funds to a school-managed account where IT can help.",
                "links": [("Protect yourself", "prevention.html")]},
            "out_refund": {"type": "outcome", "tag": "risky", "score": 1,
                "title": "Don't pay victims out of your own pocket yet.",
                "body": "Report to the payment app and (if applicable) to police before you spend anything. Most apps have a fraud process. Document who paid and how much, and hand it to your club's advisor.",
                "links": [("If something goes wrong", "response.html")]},
        },
        "aar": [
            "Use a password manager for any shared club account.",
            "Turn on MFA on every payment app I use.",
            "Make sure the club has at least two officers who can lock an account out.",
            "Keep a written incident timeline if something goes wrong.",
        ],
    },
    {
        "id": "wifi-spoof",
        "hotspot": "router",
        "title": "A new Wi-Fi network appears in the dorm",
        "blurb": "'DormWiFi-Free-Faster' shows up next to your usual campus SSID.",
        "setup": (
            "You're studying in your room and your laptop says the campus Wi-Fi is slow. You scan the "
            "available networks and see a new one: 'DormWiFi-Free-Faster,' with full signal and no password."
        ),
        "start": "n0",
        "nodes": {
            "n0": {"type": "decision", "q": "Do you connect to it?", "choices": [
                {"label": "No. Open networks with names like that are usually a trap. I'll stay on the campus SSID even if it's slower.",
                 "next": "out_skip", "score": -2, "tag": "good"},
                {"label": "Yes, but I'll just use it for streaming, not for school stuff.",
                 "next": "n1", "score": 1, "tag": "risky"},
                {"label": "Yes, and I'll sign in to my email so I can check on the faster network.",
                 "next": "out_signed_in", "score": 2, "tag": "bad"},
            ]},
            "n1": {"type": "decision",
                "q": "You're on it. A browser pop-up asks you to 'sign in with your campus account' to 'unlock full speed.'", "choices": [
                {"label": "Disconnect immediately and report the SSID to IT.",
                 "next": "out_skip", "score": -2, "tag": "good"},
                {"label": "Type in my campus credentials. It's probably a campus portal.",
                 "next": "out_signed_in", "score": 2, "tag": "bad"},
            ]},
            "out_skip": {"type": "outcome", "tag": "good", "score": -2,
                "title": "Good call.",
                # "Almost always" was too strong — base rates for malicious-vs-misconfigured
                # open Wi-Fi aren't established in public research. Reframed to describe
                # the two real possibilities without quantifying them.
                "body": "An unexpected open Wi-Fi network in a dorm is either a neighbor's open router or, in some cases, a rogue 'evil twin' access point set up to intercept traffic. Either way, it's not what you want to send your credentials over. Stay on the campus SSID. If campus Wi-Fi is consistently slow, file a ticket rather than working around it.",
                "links": [("Protect yourself", "prevention.html")]},
            "out_signed_in": {"type": "outcome", "tag": "bad", "score": 2,
                "title": "Credentials may be captured.",
                "body": "From your phone's cellular connection (not the laptop on that Wi-Fi), change your campus password right now, sign out of all sessions, and tell IT what SSID you joined and when. Don't reconnect to that network.",
                "links": [("If something goes wrong", "response.html")]},
        },
        "aar": [
            "Only join Wi-Fi networks whose names I recognize.",
            "Never type credentials into a captive portal that looks unfamiliar.",
            "Report rogue SSIDs to campus IT.",
        ],
    },
    {
        "id": "shared-printer",
        "hotspot": "printer",
        "title": "The shared printer asks for a code",
        "blurb": "'Update firmware to print. Enter your campus login.'",
        "setup": (
            "You walk to the floor printer to grab your paper. The screen says, 'Firmware update required. "
            "Sign in with your campus account to authorize.' Other students are waiting in line."
        ),
        "start": "n0",
        "nodes": {
            "n0": {"type": "decision", "q": "What do you do?", "choices": [
                {"label": "Decline. Printers don't need student logins to update. I'll print from a different printer and tell housing/IT.",
                 "next": "out_decline", "score": -2, "tag": "good"},
                {"label": "Sign in so I can get my paper.",
                 "next": "out_signed_in", "score": 2, "tag": "bad"},
                {"label": "Cancel my job and walk away. Not my problem.",
                 "next": "out_walk", "score": 0, "tag": "ok"},
            ]},
            "out_decline": {"type": "outcome", "tag": "good", "score": -2,
                "title": "Good instinct.",
                "body": "A printer asking for a campus login is either misconfigured or hostile. Either way, don't type credentials into a public device. Report the printer ID so housing/IT can check it.",
                "links": [("Protect yourself", "prevention.html")]},
            "out_signed_in": {"type": "outcome", "tag": "bad", "score": 2,
                "title": "Treat your account as exposed.",
                "body": "From your phone, change your campus password, sign out of all sessions, and report to IT with the printer location and time. Don't use the printer again until housing confirms it's clean.",
                "links": [("If something goes wrong", "response.html")]},
            "out_walk": {"type": "outcome", "tag": "ok", "score": 0,
                "title": "Safe for you, but not for the next person.",
                "body": "Walking away kept you safe but left the trap up for the next student in line. Send a quick note to housing or IT so they can take the printer offline.",
                "links": [("Protect yourself", "prevention.html")]},
        },
        "aar": [
            "Never type my campus password into a printer, kiosk, or vending machine.",
            "Report odd-looking prompts on shared hardware to housing or IT.",
        ],
    },
    # NOTE: removed gaming-takeover (was hotspot="console") when the
    # console/TV-stand was dropped from the dorm scene. Password reuse
    # and MFA are still covered in other modules and on prevention.html.
    {
        "id": "clouddrive-massshare",
        "hotspot": "clouddrive",
        "title": "Your cloud drive shared everything publicly",
        "blurb": "A folder full of school work suddenly has a 'Public on the web' badge.",
        "setup": (
            "You open Google Drive (or OneDrive) and see that a top-level folder named 'Schoolwork' now "
            "has a sharing badge: 'Anyone with the link can view.' You did not change that."
        ),
        "start": "n0",
        "nodes": {
            "n0": {"type": "decision", "q": "What first?", "choices": [
                {"label": "Open the folder, revoke public sharing on the folder and every file inside, then check 'recent activity' for what changed and when.",
                 "next": "n1", "score": -2, "tag": "good"},
                {"label": "Move the folder to my computer and delete it from the cloud.",
                 "next": "out_delete", "score": 1, "tag": "risky"},
                {"label": "Leave it. Only people with the link can see it.",
                 "next": "out_leave", "score": 2, "tag": "bad"},
            ]},
            "n1": {"type": "decision", "q": "Sharing is off. What now?", "choices": [
                {"label": "Sign out all sessions, change my password from a different device, turn on MFA if it wasn't, and report the change to my campus IT if it's a school account.",
                 "next": "out_good", "score": -2, "tag": "good"},
                {"label": "Assume a friend opened my laptop and pranked me.",
                 "next": "out_assume", "score": 1, "tag": "risky"},
            ]},
            "out_delete": {"type": "outcome", "tag": "risky", "score": 1,
                "title": "Deleting doesn't un-share.",
                "body": "If someone grabbed the public link before you deleted, the data is already out. Revoke sharing first, then keep the files (you'll need them for evidence). Then chase down what changed.",
                "links": [("If something goes wrong", "response.html")]},
            "out_leave": {"type": "outcome", "tag": "bad", "score": 2,
                "title": "Public is public.",
                "body": "'Anyone with the link' folders get found by search engines, bots, and scrapers all the time. Revoke sharing now. If you don't recognize the change, treat the account as compromised.",
                "links": [("If something goes wrong", "response.html")]},
            "out_good": {"type": "outcome", "tag": "good", "score": -2,
                "title": "Right order.",
                "body": "Revoke sharing first to stop the bleeding, then rotate credentials and sessions, then report. If this is a school account, IT can check sign-in logs and tell you whether to worry.",
                "links": [("Protect yourself", "prevention.html")]},
            "out_assume": {"type": "outcome", "tag": "risky", "score": 1,
                "title": "Maybe. Verify anyway.",
                "body": "Even if a friend did it as a joke, your password and lock-screen matter. Change the password, turn on MFA, and tell them not to do it again.",
                "links": [("Protect yourself", "prevention.html")]},
        },
        "aar": [
            "Lock my laptop whenever I walk away from it.",
            "Audit my cloud drive sharing once a semester.",
            "Use MFA on the account my school work lives in.",
        ],
    },
    {
        "id": "lost-phone-mfa",
        "hotspot": "phone",
        "title": "You lost your phone, and it has all your MFA",
        "blurb": "Bus seat, gym locker, taco truck. It's gone, and it's your second factor.",
        "setup": (
            "You realize you don't have your phone. Last time you saw it was an hour ago. Your phone has "
            "the authenticator app for your campus account, your bank, your email, and your password manager."
        ),
        "start": "n0",
        "nodes": {
            "n0": {"type": "decision", "q": "First action?", "choices": [
                {"label": "From a laptop, sign in to Find My iPhone / Find My Device, mark the phone as lost, and remotely lock it. Then call my carrier to pause the SIM.",
                 "next": "n1", "score": -2, "tag": "good"},
                {"label": "Walk back over the route and look for it before doing anything else.",
                 "next": "out_walk", "score": 0, "tag": "ok"},
                {"label": "Tweet that I lost it so people return it.",
                 "next": "out_tweet", "score": 1, "tag": "risky"},
            ]},
            "n1": {"type": "decision", "q": "Phone is locked remotely. What now?", "choices": [
                {"label": "From a trusted device, change my email password first, then bank, then campus, using my password manager backup. Set up MFA backup codes on a fresh device.",
                 "next": "out_good", "score": -2, "tag": "good"},
                {"label": "Wait until I get a replacement phone. Accounts are fine for now.",
                 "next": "out_wait", "score": 1, "tag": "risky"},
            ]},
            "out_walk": {"type": "outcome", "tag": "ok", "score": 0,
                "title": "Fine, but lock it remotely first.",
                "body": "Looking for the phone is reasonable. Locking it remotely first costs nothing and protects your accounts while you spend 30 minutes looking.",
                "links": [("Protect yourself", "prevention.html")]},
            "out_tweet": {"type": "outcome", "tag": "risky", "score": 1,
                "title": "Public 'help me' posts attract scammers.",
                "body": "Some thieves browse social media for 'lost phone' posts to send fake 'we found it, click here to verify' links. Report to campus public safety and the carrier instead.",
                "links": [("If something goes wrong", "response.html")]},
            "out_good": {"type": "outcome", "tag": "good", "score": -2,
                "title": "Crisis averted.",
                "body": "Lock the phone, pause the SIM, rotate the important passwords. A lost phone becomes an annoyance instead of a disaster. Save your MFA backup codes somewhere offline (a paper envelope at home works) for next time.",
                "links": [("Protect yourself", "prevention.html")]},
            "out_wait": {"type": "outcome", "tag": "risky", "score": 1,
                "title": "Don't wait.",
                "body": "Even with a phone lock, a determined thief can sometimes get into accounts via SIM swap or social engineering. Rotate critical passwords now.",
                "links": [("If something goes wrong", "response.html")]},
        },
        "aar": [
            "Save MFA backup codes somewhere offline.",
            "Know how to use Find My Device / Find My iPhone before I need it.",
            "Have my carrier's number saved in two places (phone + paper).",
        ],
    },
    {
        "id": "usb-from-meeting",
        "hotspot": "usbstick",
        "title": "Someone hands you a USB stick at a meeting",
        "blurb": "'Just the slides from the talk. Plug it in!'",
        "setup": (
            "At a student-org meeting, a visiting speaker offers their slides on a USB stick. 'Just plug it in, "
            "we're running short on time.' The stick has no label."
        ),
        "start": "n0",
        "nodes": {
            "n0": {"type": "decision", "q": "What do you do?", "choices": [
                {"label": "Politely decline the stick and ask them to email the file or share it via a cloud link instead.",
                 "next": "out_decline", "score": -2, "tag": "good"},
                {"label": "Plug it into the club projector laptop 'because that one's not mine.'",
                 "next": "out_projector", "score": 2, "tag": "bad"},
                {"label": "Plug it into my own laptop quickly to 'just check.'",
                 "next": "out_mylaptop", "score": 2, "tag": "bad"},
            ]},
            "out_decline": {"type": "outcome", "tag": "good", "score": -2,
                "title": "Good call.",
                "body": "USB sticks from outside the org are a classic delivery method for malware and harvesting tools. A 30-second cloud upload solves the same problem with none of the risk. Just say you don't plug in unknown USBs.",
                "links": [("Protect yourself", "prevention.html")]},
            "out_projector": {"type": "outcome", "tag": "bad", "score": 2,
                "title": "Shared club laptops are still a target.",
                "body": "Shared laptops often have club credentials saved, mapped drives, or campus accounts signed in. Unplug it, leave the laptop alone, and tell whoever administers it.",
                "links": [("If something goes wrong", "response.html")]},
            "out_mylaptop": {"type": "outcome", "tag": "bad", "score": 2,
                "title": "Treat your laptop as suspect.",
                "body": "Eject the stick, disconnect from Wi-Fi, and run a full scan with your built-in antivirus. If the stick auto-opened anything, treat the laptop as compromised and call IT.",
                "links": [("If something goes wrong", "response.html")]},
        },
        "aar": [
            "Never plug in a USB stick I didn't buy myself.",
            "Ask for files via email or a cloud link instead.",
            "Disable USB auto-run on my laptop.",
        ],
    },
    {
        "id": "fake-ra-email",
        "hotspot": "campusemail",
        "title": "A 'fire safety inspection' email from your RA",
        "blurb": "Click here within 1 hour to confirm your room, or face a fine.",
        "setup": (
            "Your inbox has a message: 'Mandatory fire safety inspection. Confirm your room number within "
            "1 hour to avoid a $100 fine.' The sender looks like your RA's name, but the address is a Gmail "
            "you've never seen, not the campus one."
        ),
        "start": "n0",
        "nodes": {
            "n0": {"type": "decision", "q": "What do you do?", "choices": [
                {"label": "Don't click the link. Open a new tab, go to my campus housing portal directly, and check there. Message my RA via the official channel I already have.",
                 "next": "out_good", "score": -2, "tag": "good"},
                {"label": "Click the link to 'confirm.' It's probably real.",
                 "next": "out_click", "score": 2, "tag": "bad"},
                {"label": "Reply to the Gmail asking if it's really my RA.",
                 "next": "out_reply", "score": 1, "tag": "risky"},
            ]},
            "out_good": {"type": "outcome", "tag": "good", "score": -2,
                "title": "You caught it.",
                "body": "'Urgency + a fine + a link + the wrong sender domain' is the classic phishing template. Verify out-of-band, never via the message in front of you. Report the message to your campus phishing inbox.",
                "links": [("Protect yourself", "prevention.html")]},
            "out_click": {"type": "outcome", "tag": "bad", "score": 2,
                "title": "Probably credential theft.",
                "body": "If you typed your campus login, change your password and sign out of all sessions from a different device, then tell IT. Keep the original email as evidence.",
                "links": [("If something goes wrong", "response.html")]},
            "out_reply": {"type": "outcome", "tag": "risky", "score": 1,
                "title": "Replying confirms your address.",
                "body": "Don't reply to the suspect address. Contact the real RA via the channel you've already used (the dorm group chat, an in-person knock, the official campus phone or email).",
                "links": [("If something goes wrong", "response.html")]},
        },
        "aar": [
            "Always check the full sender domain, not just the display name.",
            "When in doubt, verify out-of-band.",
            "Report suspicious emails to my campus phishing inbox.",
        ],
    },
]


# ============================================================================
# DRILLS = merged + deduped SCENARIOS + LAB.
# ----------------------------------------------------------------------------
# We collapsed the old "Scenarios" and "Dorm lab" pages into one. Both were
# decision-tree drills, just at different angles. Now they all live in one
# DRILLS list and one page (drills.html). The dorm SVG is one entry point (for
# the items that have a hotspot in the scene). The tile grid is the other and
# is the complete list.
#
# Build rules:
#   - Scenarios use "situation"; the unified engine expects "setup". Normalize.
#   - Scenarios had no AAR; add a short, voice-matched checklist per scenario
#     mined from the "good" outcome bodies.
#   - Lab modules have a hotspot key. Scenarios without one get hotspot = "".
#   - One genuine dup is dropped: dorm-ransom-note (kept laptop-encrypted, which
#     is tighter, has an AAR, and is already anchored to the dorm laptop).
#
# Order: lab modules first (dorm-anchored, the showpiece), then the remaining
# scenarios (off-screen drills). Within each group, original order preserved.
# ============================================================================

# Per-scenario AAR checklists, written to match the "I will..." voice of the
# lab AARs and grounded in each scenario's "good" outcome.
_SCENARIO_AARS: dict = {
    "phishing-it-helpdesk": [
        "Hover the sender and the link before I click.",
        "Report suspicious emails through my campus phishing button or inbox.",
        "If I might have typed credentials, change my password from a different device.",
    ],
    "fake-canvas-login": [
        "Verify suspicious links out-of-band (text, in-person, official email).",
        "Type campus URLs myself or use my own bookmark; don't trust links sent to me.",
        "Report the original link so IT can take it down for everyone else.",
    ],
    "mfa-fatigue": [
        "Deny any MFA prompt I didn't start.",
        "After a push-bomb, change my password and sign out all sessions.",
        "Enroll in phishing-resistant MFA (passkey or hardware key) if my school offers it.",
    ],
    "job-scam": [
        "Treat any 'upfront fee,' off-platform contact, or too-good-to-be-true rate as a job scam.",
        "Verify a recruiter's identity through the company's real website, not their DM.",
        "Report fake job posts to the platform and to my campus career center.",
    ],
    "financial-aid": [
        "Check my student portal directly; never trust a financial-aid link in a text.",
        "Call the financial-aid office using a number from the school's real website.",
        "Treat 'verify within X hours' urgency as a phishing signal.",
    ],
    "club-drive": [
        "Revoke unknown shares immediately, then restore from version history.",
        "Change the owner account's password and sign out all sessions after any club-account weirdness.",
        "Loop in campus IT and the club's faculty advisor on shared-account incidents.",
    ],
    "stolen-laptop": [
        "Sign out of campus accounts everywhere and change my password the moment a device is missing.",
        "File a police or campus-security report; use Find My to mark the device lost.",
        "Keep full-disk encryption (FileVault or BitLocker) on so a thief is mostly facing a brick.",
    ],
    "roommate-login": [
        "Never share my campus password, even with a roommate, even \"just this once.\"",
        "Help friends use 24/7 self-service password reset or the after-hours help desk instead.",
        "Reach paywalled articles through the library, Google Scholar, or publisher 'read-only' links.",
    ],
    "usb-found": [
        "Never plug an unknown USB stick into any device I care about.",
        "Drop found USB sticks at the library lost-and-found or campus IT.",
        "Don't use lab PCs as a 'sandbox' for unknown drives; they're on the campus network.",
    ],
}

# IDs of scenarios to drop in the merge (genuine duplicates of lab modules).
_DROP_SCENARIO_IDS: set = {
    # Same situation as LAB's laptop-encrypted, weaker copy. Keep the lab one.
    "dorm-ransom-note",
}


def _scenario_to_drill(s: dict) -> dict:
    """Normalize a SCENARIOS-shaped dict into the unified DRILLS shape."""
    drill = dict(s)
    # situation -> setup
    if "situation" in drill and "setup" not in drill:
        drill["setup"] = drill.pop("situation")
    # no hotspot in the dorm SVG for off-screen scenarios
    drill.setdefault("hotspot", "")
    # voice-matched AAR
    drill.setdefault("aar", _SCENARIO_AARS.get(s["id"], []))
    return drill


def _build_drills() -> list:
    # Lab modules first (dorm-anchored), then the surviving scenarios.
    out = []
    seen = set()
    for m in LAB:
        out.append(m)
        seen.add(m["id"])
    for s in SCENARIOS:
        if s["id"] in _DROP_SCENARIO_IDS or s["id"] in seen:
            continue
        out.append(_scenario_to_drill(s))
        seen.add(s["id"])
    return out


DRILLS = _build_drills()
