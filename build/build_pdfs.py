"""Generate PDFs from content.py using ReportLab.

Outputs:
  assets/pdf/role-<id>.pdf            (one per role)
  assets/pdf/playbook-summary.pdf     (overall summary)
"""
from __future__ import annotations
import sys, pathlib
from html import unescape

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "build"))
from content import ROLES, PHASES, GLOSSARY, FAQ, REFERENCES  # noqa: E402

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT
from svglib.svglib import svg2rlg
import re, tempfile

IMG_DIR = ROOT / "assets" / "img"

# Emoji codepoint ranges that the default PDF font can't render.
# Strip them before handing the SVG to svglib so they don't show as missing-glyph boxes.
_EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001F6FF"  # symbols & pictographs / transport
    "\U0001F900-\U0001F9FF"  # supplemental symbols
    "\u2600-\u27BF"           # misc symbols / dingbats
    "\uFE0F"                  # variation selector-16
    "]"
)


def _svg(name: str, target_width: float):
    """Load an SVG as a ReportLab Drawing (a Flowable) scaled to target_width points."""
    raw = (IMG_DIR / name).read_text(encoding="utf-8")
    cleaned = _EMOJI_RE.sub("", raw)
    # tighten leftover spacing inside <text>...</text>, e.g. "> Students" -> ">Students"
    cleaned = re.sub(r">\s+([A-Za-z])", r">\1", cleaned)
    # ASCII-only fallbacks for chars the default PDF font lacks
    cleaned = cleaned.replace("→", "->").replace("←", "<-")
    with tempfile.NamedTemporaryFile("w", suffix=".svg", delete=False, encoding="utf-8") as tf:
        tf.write(cleaned)
        tmp_path = tf.name
    drawing = svg2rlg(tmp_path)
    if drawing is None:
        return None
    if drawing.width and drawing.width > 0:
        scale = target_width / drawing.width
        drawing.width = drawing.width * scale
        drawing.height = drawing.height * scale
        drawing.scale(scale, scale)
    drawing.hAlign = "CENTER"
    return drawing


BRAND_BROWN = colors.HexColor("#583b2a")
BRAND_RED = colors.HexColor("#791a0b")


def _styles():
    base = getSampleStyleSheet()
    s = {
        "title": ParagraphStyle("Title", parent=base["Title"], fontSize=22, leading=27,
                                textColor=BRAND_BROWN, spaceAfter=10, alignment=TA_LEFT),
        "h1": ParagraphStyle("H1", parent=base["Heading1"], fontSize=18, leading=22,
                             textColor=BRAND_BROWN, spaceBefore=14, spaceAfter=6),
        "h2": ParagraphStyle("H2", parent=base["Heading2"], fontSize=14, leading=18,
                             textColor=BRAND_BROWN, spaceBefore=12, spaceAfter=4),
        "h3": ParagraphStyle("H3", parent=base["Heading3"], fontSize=12, leading=16,
                             textColor=BRAND_BROWN, spaceBefore=8, spaceAfter=2),
        "body": ParagraphStyle("Body", parent=base["BodyText"], fontSize=10.5, leading=14,
                               spaceAfter=4),
        "lead": ParagraphStyle("Lead", parent=base["BodyText"], fontSize=11.5, leading=16,
                               textColor=colors.HexColor("#5a4f47"), spaceAfter=6),
        "small": ParagraphStyle("Small", parent=base["BodyText"], fontSize=9, leading=12,
                                textColor=colors.HexColor("#5a4f47")),
        "tag_before": ParagraphStyle("TagB", parent=base["BodyText"], fontSize=9, leading=12,
                                     textColor=colors.HexColor("#1f6f3f")),
        "tag_during": ParagraphStyle("TagD", parent=base["BodyText"], fontSize=9, leading=12,
                                     textColor=BRAND_RED),
        "tag_after":  ParagraphStyle("TagA", parent=base["BodyText"], fontSize=9, leading=12,
                                     textColor=colors.HexColor("#8a5a00")),
    }
    return s


def _bullets(items, style):
    flows = [Paragraph(_esc(x), style) for x in items]
    return ListFlowable(
        [ListItem(f, leftIndent=12, bulletColor=BRAND_BROWN) for f in flows],
        bulletType="bullet", start="•", leftIndent=14, bulletFontSize=10
    )


def _esc(s: str) -> str:
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;"))


def _header_footer(canv, doc):
    canv.saveState()
    canv.setFont("Helvetica", 9)
    canv.setFillColor(colors.HexColor("#5a4f47"))
    canv.drawString(inch, 0.5 * inch, "Campus Ransomware Playbook · CrimRxiv Consortium")
    canv.drawRightString(LETTER[0] - inch, 0.5 * inch, f"Page {doc.page}")
    canv.setStrokeColor(BRAND_BROWN)
    canv.setLineWidth(0.5)
    canv.line(inch, 0.7 * inch, LETTER[0] - inch, 0.7 * inch)
    canv.restoreState()


def _doc(path: pathlib.Path, title: str):
    return SimpleDocTemplate(
        str(path), pagesize=LETTER,
        leftMargin=inch, rightMargin=inch,
        topMargin=0.9 * inch, bottomMargin=0.9 * inch,
        title=title, author="Joshua Gerstenfeld and Scott Jacques (CrimRxiv Consortium)",
        subject="Campus Ransomware Playbook",
    )


def role_pdf(role: dict, out_dir: pathlib.Path) -> pathlib.Path:
    s = _styles()
    path = out_dir / f"role-{role['id']}.pdf"
    doc = _doc(path, f"Campus Ransomware Playbook — {role['label']}")
    story = []
    story.append(Paragraph("Campus Ransomware Playbook", s["small"]))
    story.append(Paragraph(_esc(role["label"]), s["title"]))
    story.append(Paragraph(_esc(role["summary"]), s["lead"]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Before — prepare", s["h2"]))
    story.append(_bullets(role["before"], s["body"]))

    story.append(Paragraph("During — respond", s["h2"]))
    story.append(_bullets(role["during"], s["body"]))

    story.append(Paragraph("After — recover &amp; learn", s["h2"]))
    story.append(_bullets(role["after"], s["body"]))

    story.append(Paragraph("Self-audit checklist", s["h2"]))
    chk = []
    for item in role["checklist_items"]:
        chk.append(Paragraph("☐ &nbsp; " + _esc(item), s["body"]))
    story.extend(chk)

    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "Created by Joshua Gerstenfeld and Scott Jacques with support from the CrimRxiv Consortium. "
        "Code MIT-licensed; content licensed CC BY 4.0. Sources: NIST SP 800-61r3, NIST IR 8374, "
        "CISA #StopRansomware, EDUCAUSE. See: "
        "https://github.com/crimconsortium/campus-ransomware-playbook",
        s["small"]
    ))

    doc.build(story, onFirstPage=_header_footer, onLaterPages=_header_footer)
    return path


def summary_pdf(out_dir: pathlib.Path) -> pathlib.Path:
    s = _styles()
    path = out_dir / "playbook-summary.pdf"
    doc = _doc(path, "Campus Ransomware Playbook — Summary")
    story = []

    # Cover
    story.append(Paragraph("Campus Ransomware Playbook", s["title"]))
    story.append(Paragraph("A role-based, evidence-based guide for higher education", s["lead"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "Created by Joshua Gerstenfeld and Scott Jacques with support from the CrimRxiv Consortium. "
        "Open access. Code MIT-licensed; content CC BY 4.0.", s["body"]
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Why this playbook", s["h2"]))
    story.append(Paragraph(
        "Higher-education institutions remain prime ransomware targets, with valuable research and "
        "student data spread across decentralized environments. Recent reporting (2024–2025) shows "
        "continued attack volume and a sharp rise in records exposed via third-party software exploits. "
        "Resilience is a campus-wide responsibility — every role contributes.", s["body"]))

    # Phases
    story.append(Paragraph("Phases of a ransomware incident", s["h2"]))
    lc = _svg("lifecycle.svg", 6.5 * inch)
    if lc is not None:
        story.append(lc)
        story.append(Paragraph(
            "The six-phase ransomware lifecycle. Diagram CC BY 4.0.", s["small"]))
        story.append(Spacer(1, 6))
    for pid, p in PHASES.items():
        story.append(Paragraph(p["title"], s["h3"]))
        story.append(Paragraph(_esc(p["summary"]), s["body"]))
        story.append(_bullets(p["actions"], s["body"]))

    story.append(PageBreak())

    # Role summaries
    story.append(Paragraph("Role responsibilities at a glance", s["h1"]))
    for r in ROLES:
        story.append(KeepTogether([
            Paragraph(_esc(r["label"]), s["h2"]),
            Paragraph(_esc(r["summary"]), s["body"]),
            Paragraph("Top before-actions", s["h3"]),
            _bullets(r["before"][:4], s["body"]),
            Paragraph("Top during-actions", s["h3"]),
            _bullets(r["during"][:4], s["body"]),
            Paragraph("Top after-actions", s["h3"]),
            _bullets(r["after"][:3], s["body"]),
            Spacer(1, 6),
        ]))

    story.append(PageBreak())

    # Emergency one-pager
    story.append(Paragraph("Emergency: what to do right now", s["h1"]))
    ew = _svg("early-warnings.svg", 6.5 * inch)
    if ew is not None:
        story.append(ew)
        story.append(Paragraph(
            "Early-warning signals — two or more at once should be treated as a likely incident. "
            "Diagram CC BY 4.0.",
            s["small"]))
        story.append(Spacer(1, 8))
    story.append(Paragraph("If you see a ransom note or files renamed", s["h3"]))
    story.append(_bullets([
        "Disconnect from the network (Wi-Fi off, cables out). Don’t power off.",
        "Don’t delete the note, files, or emails — they are evidence.",
        "Call IT/Security from a different device.",
        "Don’t pay or download ‘decryption’ tools.",
    ], s["body"]))
    story.append(Paragraph("If you may have entered a password into a fake site", s["h3"]))
    story.append(_bullets([
        "Move to a different device.",
        "Change the affected password and review recovery info.",
        "Report the message to IT/security and keep it as evidence.",
    ], s["body"]))
    story.append(Paragraph("Incident-response team", s["h3"]))
    story.append(_bullets([
        "Trigger the IR plan; appoint an Incident Commander.",
        "Isolate segments, disable compromised identities, revoke sessions and tokens.",
        "Preserve memory and disk images before reimaging.",
        "Engage legal, insurer, and law enforcement (FBI / CISA in the U.S.) early.",
        "Coordinate communications cadence with comms and legal.",
    ], s["body"]))

    story.append(Spacer(1, 12))
    story.append(Paragraph("Sources", s["h2"]))
    for title, url, blurb in REFERENCES:
        story.append(Paragraph(f"<b>{_esc(title)}</b> — {_esc(blurb)}<br/><font size='8'>{_esc(url)}</font>", s["body"]))

    doc.build(story, onFirstPage=_header_footer, onLaterPages=_header_footer)
    return path


def main() -> None:
    out_dir = ROOT / "assets" / "pdf"
    out_dir.mkdir(parents=True, exist_ok=True)
    for r in ROLES:
        p = role_pdf(r, out_dir)
        print("Wrote", p)
    p = summary_pdf(out_dir)
    print("Wrote", p)


if __name__ == "__main__":
    main()
