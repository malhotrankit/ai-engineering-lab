#!/usr/bin/env python3
"""Generate the job-readiness plan and master revision PDFs from Markdown sources."""

from __future__ import annotations

import html
import os
import re
import tempfile
from dataclasses import dataclass
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
    XPreformatted,
)


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class PdfSpec:
    source: Path
    output: Path
    short_title: str


SPECS = (
    PdfSpec(
        ROOT / "docs/AI_Application_Engineering_16_Week_Plan.md",
        ROOT / "docs/AI_Application_Engineering_16_Week_Plan.pdf",
        "16-Week AI Application Engineering Plan",
    ),
    PdfSpec(
        ROOT / "coursera_notes/course_1_master_revision.md",
        ROOT / "coursera_notes/course_1_master_revision.pdf",
        "Course 1 Master Revision",
    ),
    PdfSpec(
        ROOT / "coursera_notes/course_2_master_revision.md",
        ROOT / "coursera_notes/course_2_master_revision.pdf",
        "Course 2 Master Revision",
    ),
    PdfSpec(
        ROOT / "coursera_notes/interview_questions.md",
        ROOT / "coursera_notes/interview_questions_master.pdf",
        "AI Application Engineer Interview Bank",
    ),
)


INK = colors.HexColor("#172033")
NAVY = colors.HexColor("#12355B")
BLUE = colors.HexColor("#1E5AA8")
SKY = colors.HexColor("#EAF2FB")
PALE = colors.HexColor("#F5F7FA")
MUTED = colors.HexColor("#5E6A7D")
LINE = colors.HexColor("#CFD8E6")
GREEN = colors.HexColor("#26734D")


def normalize_text(value: str) -> str:
    """Use characters supported reliably by the standard PDF fonts."""
    replacements = {
        "\u2013": "-",
        "\u2014": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2192": "->",
        "\u2794": "->",
        "\u2026": "...",
        "\u00a0": " ",
        "\u20ac": "EUR ",
    }
    for old, new in replacements.items():
        value = value.replace(old, new)
    return value.encode("latin-1", errors="replace").decode("latin-1")


def inline_markup(value: str) -> str:
    """Convert a small safe Markdown subset into ReportLab paragraph markup."""
    value = normalize_text(value.strip())
    escaped = html.escape(value, quote=True)
    escaped = re.sub(
        r"\[([^\]]+)\]\((https?://[^)]+)\)",
        r'<link href="\2" color="#1E5AA8"><u>\1</u></link>',
        escaped,
    )
    escaped = re.sub(
        r"(?<!\*)\*\*([^*]+)\*\*(?!\*)",
        r"<b>\1</b>",
        escaped,
    )
    escaped = re.sub(
        r"`([^`]+)`",
        r'<font name="Courier" color="#12355B">\1</font>',
        escaped,
    )
    return escaped


def build_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "TitleCustom",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=23,
            leading=27,
            textColor=NAVY,
            alignment=TA_LEFT,
            spaceAfter=9 * mm,
        ),
        "h2": ParagraphStyle(
            "H2Custom",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=14.5,
            leading=17,
            textColor=NAVY,
            spaceBefore=4.7 * mm,
            spaceAfter=2.2 * mm,
            keepWithNext=True,
        ),
        "h3": ParagraphStyle(
            "H3Custom",
            parent=base["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=11.2,
            leading=13.5,
            textColor=BLUE,
            spaceBefore=3.5 * mm,
            spaceAfter=1.5 * mm,
            keepWithNext=True,
        ),
        "h4": ParagraphStyle(
            "H4Custom",
            parent=base["Heading4"],
            fontName="Helvetica-Bold",
            fontSize=9.8,
            leading=11.8,
            textColor=GREEN,
            spaceBefore=3 * mm,
            spaceAfter=1.2 * mm,
            keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "BodyCustom",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.9,
            leading=12.25,
            textColor=INK,
            spaceAfter=1.9 * mm,
        ),
        "bullet": ParagraphStyle(
            "BulletCustom",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.8,
            leading=12.1,
            leftIndent=5 * mm,
            firstLineIndent=-3.5 * mm,
            bulletIndent=1.2 * mm,
            textColor=INK,
            spaceAfter=1.0 * mm,
        ),
        "number": ParagraphStyle(
            "NumberCustom",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.8,
            leading=12.1,
            leftIndent=6 * mm,
            firstLineIndent=-4.5 * mm,
            textColor=INK,
            spaceAfter=1.0 * mm,
        ),
        "code": ParagraphStyle(
            "CodeCustom",
            parent=base["Code"],
            fontName="Courier",
            fontSize=7.5,
            leading=10,
            textColor=NAVY,
            leftIndent=3 * mm,
            rightIndent=3 * mm,
            spaceBefore=1 * mm,
            spaceAfter=2.5 * mm,
        ),
        "table": ParagraphStyle(
            "TableCustom",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=7.5,
            leading=9.5,
            textColor=INK,
        ),
        "table_header": ParagraphStyle(
            "TableHeaderCustom",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=7.6,
            leading=9.5,
            textColor=colors.white,
            alignment=TA_CENTER,
        ),
    }


def is_table_separator(line: str) -> bool:
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def parse_table(lines: list[str], styles: dict[str, ParagraphStyle], width: float) -> Table:
    raw_rows = [
        [cell.strip() for cell in line.strip().strip("|").split("|")]
        for line in lines
        if not is_table_separator(line)
    ]
    column_count = max(len(row) for row in raw_rows)
    for row in raw_rows:
        row.extend([""] * (column_count - len(row)))

    weights = []
    for column in range(column_count):
        max_length = max(len(row[column]) for row in raw_rows)
        weights.append(max(12, min(max_length, 42)))
    total_weight = sum(weights)
    col_widths = [width * weight / total_weight for weight in weights]

    rows = []
    for row_index, row in enumerate(raw_rows):
        style = styles["table_header"] if row_index == 0 else styles["table"]
        rows.append([Paragraph(inline_markup(cell), style) for cell in row])

    table = Table(rows, colWidths=col_widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE]),
                ("GRID", (0, 0), (-1, -1), 0.45, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return table


def markdown_story(markdown: str, styles: dict[str, ParagraphStyle], width: float) -> list:
    lines = markdown.splitlines()
    story: list = []
    index = 0
    in_code = False
    code_lines: list[str] = []

    while index < len(lines):
        raw = lines[index].rstrip()

        if raw.startswith("```"):
            if in_code:
                code = normalize_text("\n".join(code_lines))
                story.append(
                    Table(
                        [[XPreformatted(html.escape(code), styles["code"]) ]],
                        colWidths=[width],
                        style=TableStyle(
                            [
                                ("BACKGROUND", (0, 0), (-1, -1), SKY),
                                ("BOX", (0, 0), (-1, -1), 0.5, LINE),
                                ("LEFTPADDING", (0, 0), (-1, -1), 2),
                                ("RIGHTPADDING", (0, 0), (-1, -1), 2),
                            ]
                        ),
                    )
                )
                code_lines = []
                in_code = False
            else:
                in_code = True
            index += 1
            continue

        if in_code:
            code_lines.append(raw)
            index += 1
            continue

        if raw.startswith("|") and "|" in raw[1:]:
            table_lines = []
            while index < len(lines):
                candidate = lines[index].rstrip()
                if not (candidate.startswith("|") and "|" in candidate[1:]):
                    break
                table_lines.append(candidate)
                index += 1
            story.append(parse_table(table_lines, styles, width))
            story.append(Spacer(1, 2.5 * mm))
            continue

        stripped = raw.strip()
        if not stripped:
            index += 1
            continue
        if stripped in {"---", "***"}:
            story.append(Spacer(1, 1.5 * mm))
            story.append(HRFlowable(width="100%", thickness=0.6, color=LINE))
            story.append(Spacer(1, 1.5 * mm))
            index += 1
            continue
        if stripped == "<!-- pagebreak -->":
            story.append(PageBreak())
            index += 1
            continue

        heading = re.match(r"^(#{1,4})\s+(.+)$", stripped)
        if heading:
            level = len(heading.group(1))
            key = "title" if level == 1 else f"h{level}"
            story.append(Paragraph(inline_markup(heading.group(2)), styles[key]))
            if level == 1:
                story.append(HRFlowable(width="100%", thickness=2, color=BLUE))
                story.append(Spacer(1, 3 * mm))
            index += 1
            continue

        bullet = re.match(r"^\s*[-*]\s+(.+)$", raw)
        if bullet:
            story.append(
                Paragraph(inline_markup(bullet.group(1)), styles["bullet"], bulletText="-")
            )
            index += 1
            continue

        number = re.match(r"^\s*(\d+)\.\s+(.+)$", raw)
        if number:
            story.append(
                Paragraph(
                    inline_markup(number.group(2)),
                    styles["number"],
                    bulletText=f"{number.group(1)}.",
                )
            )
            index += 1
            continue

        paragraph_lines = [stripped]
        index += 1
        while index < len(lines):
            candidate = lines[index].rstrip()
            candidate_stripped = candidate.strip()
            if not candidate_stripped:
                break
            if (
                candidate_stripped.startswith("#")
                or candidate_stripped.startswith("```")
                or candidate_stripped in {"---", "***", "<!-- pagebreak -->"}
                or re.match(r"^\s*[-*]\s+", candidate)
                or re.match(r"^\s*\d+\.\s+", candidate)
                or (candidate.startswith("|") and "|" in candidate[1:])
            ):
                break
            paragraph_lines.append(candidate_stripped)
            index += 1
        story.append(Paragraph(inline_markup(" ".join(paragraph_lines)), styles["body"]))

    if in_code and code_lines:
        story.append(XPreformatted(html.escape(normalize_text("\n".join(code_lines))), styles["code"]))
    return story


def page_decorator(short_title: str):
    def decorate(canvas, doc) -> None:
        canvas.saveState()
        page_width, page_height = A4
        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.5)
        canvas.line(18 * mm, page_height - 13 * mm, page_width - 18 * mm, page_height - 13 * mm)
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(MUTED)
        canvas.drawString(18 * mm, page_height - 10 * mm, short_title)
        canvas.drawRightString(page_width - 18 * mm, 10 * mm, f"Page {doc.page}")
        canvas.drawString(18 * mm, 10 * mm, "Updated 8 August 2026")
        canvas.restoreState()

    return decorate


def generate(spec: PdfSpec) -> None:
    markdown = spec.source.read_text(encoding="utf-8")
    spec.output.parent.mkdir(parents=True, exist_ok=True)
    styles = build_styles()
    page_width, _ = A4
    usable_width = page_width - 36 * mm

    fd, temp_name = tempfile.mkstemp(
        suffix=".pdf", prefix=f".{spec.output.stem}.", dir=spec.output.parent
    )
    os.close(fd)
    temp_path = Path(temp_name)
    try:
        document = SimpleDocTemplate(
            str(temp_path),
            pagesize=A4,
            rightMargin=18 * mm,
            leftMargin=18 * mm,
            topMargin=18 * mm,
            bottomMargin=16 * mm,
            title=spec.short_title,
            author="Ankit Malhotra",
            subject="AI application engineering job-readiness material",
        )
        story = markdown_story(markdown, styles, usable_width)
        decorator = page_decorator(spec.short_title)
        document.build(story, onFirstPage=decorator, onLaterPages=decorator)
        os.replace(temp_path, spec.output)
        print(f"generated {spec.output.relative_to(ROOT)}")
    finally:
        temp_path.unlink(missing_ok=True)


def main() -> None:
    for spec in SPECS:
        generate(spec)


if __name__ == "__main__":
    main()
