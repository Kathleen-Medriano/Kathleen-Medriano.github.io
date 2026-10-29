#!/usr/bin/env python3
"""Generate a compact academic CV PDF from _data/cv.json."""

import json
from pathlib import Path

try:
    from reportlab.lib.colors import HexColor, black
    from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_RIGHT
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import inch
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import (
        HRFlowable,
        KeepTogether,
        Paragraph,
        SimpleDocTemplate,
        Spacer,
        Table,
        TableStyle,
    )

    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    print("Warning: reportlab not available. Install with: pip install reportlab")

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
if REPORTLAB_AVAILABLE:
    CONTENT_WIDTH = 7.1 * inch
    DATE_WIDTH = 2.55 * inch


def load_cv_data(json_path):
    """Load CV data from JSON file."""
    try:
        with open(json_path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError:
        print(f"Error: CV data file not found at {json_path}")
        return None
    except json.JSONDecodeError as exc:
        print(f"Error: Invalid JSON in CV data file: {exc}")
        return None


def register_fonts():
    """Use DejaVu Serif when it is installed so accents render correctly."""
    regular = FONT_DIR / "DejaVuSerif.ttf"
    bold = FONT_DIR / "DejaVuSerif-Bold.ttf"
    italic = FONT_DIR / "DejaVuSerif-Italic.ttf"
    bold_italic = FONT_DIR / "DejaVuSerif-BoldItalic.ttf"
    if not all(path.exists() for path in (regular, bold, italic, bold_italic)):
        return "Times-Roman", "Times-Bold", "Times-Italic"
    pdfmetrics.registerFont(TTFont("DejaVu", str(regular)))
    pdfmetrics.registerFont(TTFont("DejaVu-Bold", str(bold)))
    pdfmetrics.registerFont(TTFont("DejaVu-Italic", str(italic)))
    pdfmetrics.registerFont(TTFont("DejaVu-BoldItalic", str(bold_italic)))
    pdfmetrics.registerFontFamily(
        "DejaVu",
        normal="DejaVu",
        bold="DejaVu-Bold",
        italic="DejaVu-Italic",
        boldItalic="DejaVu-BoldItalic",
    )
    return "DejaVu", "DejaVu-Bold", "DejaVu-Italic"


def create_styles():
    """Styles for a compact academic CV."""
    font, font_bold, font_italic = register_fonts()
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="CVName",
        fontName=font_bold,
        fontSize=18,
        leading=22,
        alignment=TA_CENTER,
        textColor=black,
        spaceAfter=2,
    ))
    styles.add(ParagraphStyle(
        name="CVContact",
        fontName=font,
        fontSize=9,
        leading=12,
        alignment=TA_CENTER,
        textColor=HexColor("#333333"),
        spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        name="CVSection",
        fontName=font_bold,
        fontSize=11,
        leading=13,
        textColor=black,
        spaceBefore=0,
        spaceAfter=0,
    ))
    styles.add(ParagraphStyle(
        name="CVSubsection",
        fontName=font_bold,
        fontSize=10,
        leading=13,
        textColor=black,
        spaceBefore=4,
        spaceAfter=3,
    ))
    styles.add(ParagraphStyle(
        name="EntryTitle",
        fontName=font_bold,
        fontSize=10.5,
        leading=13,
        textColor=black,
    ))
    styles.add(ParagraphStyle(
        name="EntryDate",
        fontName=font,
        fontSize=10,
        leading=13,
        alignment=TA_RIGHT,
        textColor=black,
    ))
    styles.add(ParagraphStyle(
        name="EntryOrg",
        fontName=font_italic,
        fontSize=10,
        leading=12,
        textColor=HexColor("#222222"),
        spaceBefore=1,
    ))
    styles.add(ParagraphStyle(
        name="EntryDesc",
        fontName=font,
        fontSize=9.5,
        leading=12,
        alignment=TA_JUSTIFY,
        textColor=black,
        spaceBefore=1,
    ))
    styles.add(ParagraphStyle(
        name="SkillLine",
        fontName=font,
        fontSize=10,
        leading=13,
        textColor=black,
        spaceBefore=1,
        spaceAfter=1,
    ))
    return styles


def esc(text):
    """Escape text for ReportLab paragraphs."""
    if text is None:
        return ""
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def is_placeholder(*values):
    """True when a field still contains an unfilled bracket placeholder."""
    return any(value and "[" in str(value) for value in values)


def format_date_range(start_date, end_date):
    """Format a start and end date for the right-hand column."""
    if start_date and end_date:
        return f"{start_date} – {end_date}"
    if start_date:
        return f"{start_date} – Present"
    return end_date or ""


def add_section(story, styles, title):
    story.append(Spacer(1, 9))
    story.append(Paragraph(esc(title).upper(), styles["CVSection"]))
    story.append(HRFlowable(
        width="100%",
        thickness=0.6,
        color=black,
        spaceBefore=1,
        spaceAfter=5,
    ))


def add_entry(story, styles, title, date, lines=None, description=None, bullets=None):
    """One CV entry: title on the left, date on the right."""
    title_para = Paragraph(esc(title), styles["EntryTitle"])
    date_text = esc(date or "").replace(" ", "&nbsp;")
    date_para = Paragraph(date_text, styles["EntryDate"])
    table = Table(
        [[title_para, date_para]],
        colWidths=[CONTENT_WIDTH - DATE_WIDTH, DATE_WIDTH],
    )
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    block = [table]
    for line in lines or []:
        if line:
            block.append(Paragraph(esc(line), styles["EntryOrg"]))
    if description:
        block.append(Paragraph(esc(description), styles["EntryDesc"]))
    for bullet in bullets or []:
        if bullet:
            block.append(Paragraph(f"• {esc(bullet)}", styles["EntryDesc"]))
    block.append(Spacer(1, 7))
    story.append(KeepTogether(block))


def add_education(story, styles, cv_data):
    education = cv_data.get("education") or []
    if not education:
        return
    add_section(story, styles, "Education")
    for item in education:
        title_parts = [part for part in (item.get("studyType"), item.get("area")) if part]
        add_entry(
            story,
            styles,
            ", ".join(title_parts),
            format_date_range(item.get("startDate"), item.get("endDate")),
            [item.get("institution")],
            item.get("description"),
        )


def add_research(story, styles, cv_data):
    research = cv_data.get("research_experience") or []
    if not research:
        return
    add_section(story, styles, "Research Experience")
    for item in research:
        lines = [item.get("institution")]
        if item.get("supervisor"):
            lines.append(f"Supervisor: {item['supervisor']}")
        add_entry(
            story,
            styles,
            item.get("position", ""),
            format_date_range(item.get("startDate"), item.get("endDate")),
            lines,
            item.get("description"),
        )


def add_publications(story, styles, cv_data):
    publications = cv_data.get("publications") or {}
    manuscripts = publications.get("manuscripts_in_prep") or []
    peer_reviewed = publications.get("peer_reviewed") or []
    if not manuscripts and not peer_reviewed:
        return
    add_section(story, styles, "Publications")
    if manuscripts:
        story.append(Paragraph("Manuscripts in Preparation / Under Review", styles["CVSubsection"]))
        for item in manuscripts:
            lines = []
            authors = item.get("authors") or []
            if authors:
                lines.append(", ".join(authors))
            if item.get("expected_submission"):
                lines.append(f"Expected submission: {item['expected_submission']}")
            add_entry(
                story,
                styles,
                item.get("title", ""),
                item.get("status", ""),
                lines,
                item.get("description"),
            )
    if peer_reviewed:
        story.append(Paragraph("Peer-Reviewed Journal Articles", styles["CVSubsection"]))
        for item in peer_reviewed:
            lines = []
            authors = item.get("authors") or []
            if authors:
                lines.append(", ".join(authors))
            journal_bits = [item.get("journal") or ""]
            if item.get("volume"):
                journal_bits.append(str(item["volume"]))
            journal = ", ".join(bit for bit in journal_bits if bit)
            if item.get("issue"):
                journal += f"({item['issue']})"
            if item.get("pages"):
                journal += f": {item['pages']}"
            if journal:
                lines.append(journal)
            if item.get("doi"):
                lines.append(f"DOI: {item['doi']}")
            add_entry(
                story,
                styles,
                item.get("title", ""),
                str(item.get("year") or ""),
                lines,
                item.get("description"),
            )


def add_talks(story, styles, cv_data):
    talks = cv_data.get("talks_and_presentations") or []
    if not talks:
        return
    add_section(story, styles, "Talks and Presentations")
    for item in talks:
        event_bits = [bit for bit in (item.get("type"), item.get("event")) if bit]
        lines = [", ".join(event_bits)] if event_bits else []
        if item.get("location"):
            lines.append(item["location"])
        add_entry(
            story,
            styles,
            item.get("title", ""),
            item.get("date", ""),
            lines,
            item.get("description"),
        )


def add_honors(story, styles, cv_data):
    honors = cv_data.get("honors_and_awards") or []
    if not honors:
        return
    add_section(story, styles, "Honors and Awards")
    for item in honors:
        add_entry(
            story,
            styles,
            item.get("title", ""),
            item.get("date", ""),
            [item.get("organization")],
            item.get("description"),
        )


def add_professional(story, styles, cv_data):
    jobs = [
        job for job in (cv_data.get("professional_experience") or [])
        if not is_placeholder(job.get("startDate"), job.get("endDate"), job.get("position"))
    ]
    if not jobs:
        return
    add_section(story, styles, "Professional Experience")
    for job in jobs:
        org_bits = [bit for bit in (job.get("organization"), job.get("location")) if bit]
        add_entry(
            story,
            styles,
            job.get("position", ""),
            format_date_range(job.get("startDate"), job.get("endDate")),
            [", ".join(org_bits)] if org_bits else [],
            bullets=job.get("responsibilities"),
        )


def add_skills(story, styles, cv_data):
    skills = cv_data.get("skills") or []
    lines = []
    for skill in skills:
        items = skill.get("items") or skill.get("keywords") or []
        label = skill.get("category") or skill.get("name")
        if label and items:
            lines.append(f"<b>{esc(label)}:</b> {esc(', '.join(items))}")
        elif label:
            lines.append(esc(label))
    if not lines:
        return
    add_section(story, styles, "Skills")
    for line in lines:
        story.append(Paragraph(line, styles["SkillLine"]))


def generate_pdf(cv_data, output_path):
    """Generate a compact academic CV PDF."""
    if not REPORTLAB_AVAILABLE:
        print("Error: reportlab library is required for PDF generation.")
        print("Install with: pip install reportlab")
        return False
    if not cv_data:
        print("Error: No CV data provided")
        return False

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=0.7 * inch,
        leftMargin=0.7 * inch,
        topMargin=0.6 * inch,
        bottomMargin=0.6 * inch,
        title=cv_data.get("basics", {}).get("name", "CV"),
    )
    styles = create_styles()
    story = []

    basics = cv_data.get("basics") or {}
    if basics.get("name"):
        story.append(Paragraph(esc(basics["name"]), styles["CVName"]))

    contact = []
    if basics.get("email"):
        contact.append(basics["email"])
    if basics.get("website"):
        contact.append(basics["website"])
    location = basics.get("location") or {}
    location_parts = [location.get("city"), location.get("region")]
    location_text = ", ".join(part for part in location_parts if part)
    if location_text:
        contact.append(location_text)
    if contact:
        story.append(Paragraph(esc("  |  ".join(contact)), styles["CVContact"]))

    add_education(story, styles, cv_data)
    add_research(story, styles, cv_data)
    add_publications(story, styles, cv_data)
    add_talks(story, styles, cv_data)
    add_honors(story, styles, cv_data)
    add_professional(story, styles, cv_data)
    add_skills(story, styles, cv_data)

    try:
        doc.build(story)
        return True
    except Exception as exc:
        print(f"Error building PDF: {exc}")
        return False


def main():
    """Generate files/cv.pdf from _data/cv.json."""
    script_dir = Path(__file__).parent
    cv_json_path = script_dir / "_data" / "cv.json"
    output_path = script_dir / "files" / "cv.pdf"
    output_path.parent.mkdir(exist_ok=True)

    print("Loading CV data...")
    cv_data = load_cv_data(cv_json_path)
    if not cv_data:
        return 1

    print(f"Generating PDF: {output_path}")
    if not generate_pdf(cv_data, str(output_path)):
        print("✗ Failed to generate PDF")
        return 1

    print(f"✓ PDF generated successfully: {output_path}")
    print(f"File size: {output_path.stat().st_size} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
