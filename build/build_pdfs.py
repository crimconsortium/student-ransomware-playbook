"""Generate the Student Ransomware Playbook PDF from content.py.

Output:
  assets/pdf/student-playbook.pdf  (full guide as a printable one-pager-ish PDF)
"""
from __future__ import annotations
import sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "build"))
from content import ROLES, GLOSSARY, FAQ, REFERENCES, DRILLS  # noqa: E402

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem, PageBreak
)
from reportlab.lib.enums import TA_LEFT

BRAND_ORANGE = colors.HexColor("#f68212")
INK = colors.HexColor("#111111")
MUTED = colors.HexColor("#555555")


def _styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle("Title", parent=base["Title"], fontSize=22, leading=27,
                                textColor=INK, spaceAfter=10, alignment=TA_LEFT),
        "h1": ParagraphStyle("H1", parent=base["Heading1"], fontSize=18, leading=22,
                             textColor=INK, spaceBefore=14, spaceAfter=6),
        "h2": ParagraphStyle("H2", parent=base["Heading2"], fontSize=14, leading=18,
                             textColor=INK, spaceBefore=12, spaceAfter=4),
        "h3": ParagraphStyle("H3", parent=base["Heading3"], fontSize=12, leading=16,
                             textColor=INK, spaceBefore=8, spaceAfter=2),
        "body": ParagraphStyle("Body", parent=base["BodyText"], fontSize=10.5, leading=14,
                               spaceAfter=4),
        "lead": ParagraphStyle("Lead", parent=base["BodyText"], fontSize=11.5, leading=16,
                               textColor=MUTED, spaceAfter=6),
        "small": ParagraphStyle("Small", parent=base["BodyText"], fontSize=9, leading=12,
                                textColor=MUTED),
    }


def _esc(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def _bullets(items, style):
    flows = [Paragraph(_esc(x), style) for x in items]
    return ListFlowable(
        [ListItem(f, leftIndent=12, bulletColor=BRAND_ORANGE) for f in flows],
        bulletType="bullet", start="•", leftIndent=14, bulletFontSize=10
    )


def _header_footer(canv, doc):
    canv.saveState()
    canv.setFont("Helvetica", 9)
    canv.setFillColor(MUTED)
    canv.drawString(inch, 0.5 * inch, "Student Ransomware Playbook · CrimRxiv Consortium")
    canv.drawRightString(LETTER[0] - inch, 0.5 * inch, f"Page {doc.page}")
    canv.setStrokeColor(BRAND_ORANGE)
    canv.setLineWidth(0.5)
    canv.line(inch, 0.7 * inch, LETTER[0] - inch, 0.7 * inch)
    canv.restoreState()


def build_pdf(out_dir: pathlib.Path) -> pathlib.Path:
    s = _styles()
    student = ROLES[0]
    path = out_dir / "student-playbook.pdf"
    doc = SimpleDocTemplate(
        str(path), pagesize=LETTER,
        leftMargin=inch, rightMargin=inch,
        topMargin=0.9 * inch, bottomMargin=0.9 * inch,
        title="Student Ransomware Playbook",
        author="Joshua Gerstenfeld and Scott Jacques (CrimRxiv Consortium)",
        subject="Student Ransomware Playbook",
    )
    story = []

    story.append(Paragraph("Student Ransomware Playbook", s["title"]))
    story.append(Paragraph(
        "A plain-language guide for college and university students. "
        "How to spot phishing, protect your accounts and coursework, and know what to do if something goes wrong.",
        s["lead"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Created by Joshua Gerstenfeld and Scott Jacques with support from the CrimRxiv Consortium. "
        "Open access. Code MIT-licensed; content CC BY 4.0. Live site: "
        "https://crimconsortium.github.io/student-ransomware-playbook/",
        s["small"]))

    story.append(Paragraph("Protect yourself (before anything goes wrong)", s["h1"]))
    story.append(_bullets(student["before"], s["body"]))

    story.append(Paragraph("Phishing red flags", s["h2"]))
    story.append(_bullets([
        "Urgency: \"Your account will be locked in 24 hours.\"",
        "A login link in the message — type your campus URL into the browser yourself.",
        "Sender domain close but not exact (e.g., support@my-college.edu.help).",
        "Unexpected attachments — zip files, OneNote files, HTML \"invoices.\"",
        "Offers too good to be true: surprise scholarships, refunds, high-paying student jobs.",
        "MFA prompts you didn't trigger. Never approve a prompt you didn't start.",
    ], s["body"]))
    story.append(Paragraph(
        "And sometimes there are no red flags. A real account from someone you actually know — a friend, "
        "a professor, your RA, the campus help desk — can be compromised and used to send phishing. Same "
        "name, same email address, normal-looking signature. If a message asks you to click a link, log in "
        "somewhere, pay something, share an MFA code, or move money, treat the request with suspicion — "
        "not just the sender. Verify out-of-band: text or call the person on a number you already had, or "
        "walk over.",
        s["body"]))

    story.append(PageBreak())

    story.append(Paragraph("If something goes wrong", s["h1"]))
    story.append(Paragraph("In the moment", s["h2"]))
    story.append(_bullets(student["during"], s["body"]))
    story.append(Paragraph("After the dust settles", s["h2"]))
    story.append(_bullets(student["after"], s["body"]))

    story.append(Paragraph("Quick checklist", s["h2"]))
    for item in student["checklist_items"]:
        story.append(Paragraph("☐ &nbsp; " + _esc(item), s["body"]))

    story.append(PageBreak())

    story.append(Paragraph("Drills", s["h1"]))
    story.append(Paragraph(
        f"{len(DRILLS)} short incident rehearsals. Some are anchored in a simulated dorm room "
        "you can click around; the rest are off-screen patterns (fake login page, MFA fatigue, "
        "job and financial-aid scams, lost or stolen devices). Each drill has branching choices "
        "and a short after-action review. Play the interactive version at "
        "crimconsortium.github.io/student-ransomware-playbook/drills.html and earn a printable "
        "Cyber-Smart Student certificate after finishing them all. The drills are listed below "
        "for quick offline reference.",
        s["body"]))
    for i, mod in enumerate(DRILLS, 1):
        story.append(Paragraph(f"{i:02d}. {_esc(mod['title'])}", s["h3"]))
        story.append(Paragraph(_esc(mod.get('setup', '')), s["body"]))
        for habit in mod.get('aar', []):
            story.append(Paragraph("☐ &nbsp; " + _esc(habit), s["body"]))

    story.append(PageBreak())

    story.append(Paragraph("FAQ", s["h1"]))
    for q, a in FAQ:
        story.append(Paragraph(_esc(q), s["h3"]))
        story.append(Paragraph(_esc(a), s["body"]))

    story.append(PageBreak())

    story.append(Paragraph("Glossary", s["h1"]))
    for term, defn in GLOSSARY:
        story.append(Paragraph(f"<b>{_esc(term)}</b> — {_esc(defn)}", s["body"]))

    story.append(Paragraph("Sources", s["h1"]))
    for title, url, blurb in REFERENCES:
        story.append(Paragraph(
            f"<b>{_esc(title)}</b> — {_esc(blurb)}<br/><font size='8'>{_esc(url)}</font>",
            s["body"]))

    doc.build(story, onFirstPage=_header_footer, onLaterPages=_header_footer)
    return path


def main() -> None:
    out_dir = ROOT / "assets" / "pdf"
    out_dir.mkdir(parents=True, exist_ok=True)
    p = build_pdf(out_dir)
    print("Wrote", p)


if __name__ == "__main__":
    main()
