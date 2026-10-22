"""Render a Resume to PDF."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import (
    CondPageBreak,
    Flowable,
    HRFlowable,
    KeepTogether,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from resumate.markup import inline
from resumate.models import Entry, Resume, Section, Style
from resumate.render.common import Typography, header, make_doc

_NO_PADDING = TableStyle(
    [
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
    ]
)


def _two_column(
    left: Paragraph, right: Paragraph, right_text: str, font: str, size: float
) -> Table:
    # The right column is exactly as wide as its text (plus a gap) so titles get the rest.
    right_width = stringWidth(right_text, font, size) + size * 1.5
    table = Table([[left, right]], colWidths=["*", right_width])
    table.setStyle(_NO_PADDING)
    return table


def _bullets(items: list[str], typo: Typography) -> list[Flowable]:
    return [Paragraph(inline(b, typo.link_color), typo.bullet, bulletText="•") for b in items]


def _row(left: str, right: str, right_style: ParagraphStyle) -> Table:
    """A line with `left` markup flush left and plain `right` text flush right."""
    size = right_style.fontSize
    return _two_column(
        Paragraph(left, right_style.parent),
        Paragraph(inline(right), right_style),
        right,
        right_style.fontName,
        size,
    )


def _url(entry: Entry, typo: Typography) -> str:
    if not entry.url:
        return ""
    href = entry.url if "://" in entry.url else f"https://{entry.url}"
    color = f' color="{typo.link_color}"' if typo.link_color else ""
    return f'<a href="{href}"{color}>{inline(entry.url)}</a>'


def _entry_heading(entry: Entry, typo: Typography) -> list[Flowable]:
    url = _url(entry, typo)
    if typo.classic:
        # One line: **Title – Org, Location** – url, with the date in italics on the right.
        org = ", ".join(p for p in (entry.org, entry.location) if p)
        title = " – ".join(inline(p) for p in (entry.title, org) if p)
        left = f"<b>{title}</b>" + (f" – {url}" if url else "")
        return [_row(left, entry.date_range, typo.right_italic)]

    left = f"<b>{inline(entry.title)}</b>" + (f"  {url}" if url else "")
    head: list[Flowable] = [_row(left, entry.date_range, typo.right)]
    if entry.org or entry.location:
        org = f"<i>{inline(entry.org or '')}</i>"
        head.append(_row(org, entry.location or "", typo.right_italic))
    return head


def _entry(entry: Entry, typo: Typography) -> list[Flowable]:
    head = _entry_heading(entry, typo)
    if entry.summary:
        style = typo.entry_sub if typo.classic else typo.body
        head.append(Paragraph(inline(entry.summary, typo.link_color), style))
    bullets = _bullets(entry.bullets, typo)
    # Never strand an entry's heading at the bottom of a page without its first bullet.
    flow: list[Flowable] = [KeepTogether(head + bullets[:1]), *bullets[1:]]
    return [Spacer(1, typo.style.base_size * 0.5), *flow]


def _section_heading(section: Section, typo: Typography) -> list[Flowable]:
    if typo.classic:
        return [Paragraph(f"<u>{inline(section.title)}</u>", typo.section)]
    return [
        Paragraph(inline(section.title.upper()), typo.section),
        HRFlowable(width="100%", thickness=0.6, color=typo.accent, spaceBefore=1, spaceAfter=1),
    ]


def _section(section: Section, typo: Typography) -> list[Flowable]:
    flow: list[Flowable] = [
        CondPageBreak(typo.style.base_size * 6),
        *_section_heading(section, typo),
    ]
    if section.entries:
        for i, entry in enumerate(section.entries):
            items = _entry(entry, typo)
            flow += items[1:] if i == 0 else items
    elif section.skills:
        for group in section.skills:
            text = f"<b>{inline(group.category)}:</b> {inline(group.text, typo.link_color)}"
            if typo.classic:
                flow.append(Paragraph(text, typo.bullet, bulletText="•"))
            else:
                flow.append(Paragraph(text, typo.body))
    elif section.bullets:
        flow += _bullets(section.bullets, typo)
    elif section.text:
        flow.append(Paragraph(inline(section.text, typo.link_color), typo.body))
    return flow


def render_resume(resume: Resume, out: Path, style: Style) -> int:
    """Write the resume PDF to `out` and return its page count."""
    style = style.merged(resume.style)
    typo = Typography(style)
    out.parent.mkdir(parents=True, exist_ok=True)
    doc = make_doc(
        out,
        style,
        title=f"{resume.name} – Resume",
        author=resume.name,
        subject=resume.headline or "Resume",
    )

    flow = header(resume.name, resume.headline, resume.contact, typo)
    if resume.summary:
        flow += [
            Spacer(1, style.base_size * 0.6),
            Paragraph(inline(resume.summary, typo.link_color), typo.body),
        ]
    for section in resume.sections:
        if section.is_empty:
            continue
        flow += _section(section, typo)

    doc.build(flow)
    return doc.page
