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
from resumate.models import Certificate, Entry, Resume, Section, Style
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


def _link(url: str, typo: Typography) -> str:
    if not url:
        return ""
    href = url if "://" in url else f"https://{url}"
    color = f' color="{typo.link_color}"' if typo.link_color else ""
    return f'<a href="{href}"{color}>{inline(url)}</a>'


def _url(entry: Entry, typo: Typography) -> str:
    return _link(entry.url or "", typo)


def _inline_row(left: str, right: str, right_style: ParagraphStyle, italic: bool) -> Paragraph:
    """`left | right` on one line, so the right text stays next to its entry when parsed."""
    if right:
        right = f"<i>{inline(right)}</i>" if italic else inline(right)
        left = f"{left} | {right}" if left else right
    return Paragraph(left, right_style.parent)


def _degree_lines(entry: Entry, typo: Typography) -> list[Flowable]:
    # Labeled lines so a parser can't mistake part of the degree name for the major.
    # (Workday read "Bachelor of Science in Engineering in Computer Science" as Engineering
    # Physics.)
    labeled = [("Major", entry.major), ("Minor", entry.minor)]
    return [Paragraph(f"{label}: {inline(value)}", typo.body) for label, value in labeled if value]


def _entry_heading(entry: Entry, typo: Typography) -> list[Flowable]:
    url = _url(entry, typo)
    inline_dates = typo.style.date_align == "inline"
    org_text = entry.org_text
    date_style = typo.right_italic if typo.classic else typo.right

    if typo.style.entry_heading == "one_line":
        # **Title** | Org | Location  url | dates. Pipes, never dashes, between the parts.
        parts = [f"<b>{inline(entry.title)}</b>"]
        parts += [inline(p) for p in (org_text, entry.location) if p]
        left = " | ".join(parts) + (f"  {url}" if url else "")
        if inline_dates:
            head = [_inline_row(left, entry.date_range, date_style, italic=typo.classic)]
        else:
            head = [_row(left, entry.date_range, date_style)]
        return head + _degree_lines(entry, typo)

    # Stacked: `Title | dates`, then `Org | Location`. This is the shape Workday's resume
    # autofill parsed correctly (title, company, location, and dates).
    left = f"<b>{inline(entry.title)}</b>" + (f"  {url}" if url else "")
    if inline_dates:
        head: list[Flowable] = [_inline_row(left, entry.date_range, date_style, typo.classic)]
    else:
        head = [_row(left, entry.date_range, date_style)]
    if org_text or entry.location:
        org = f"<i>{inline(org_text)}</i>" if org_text else ""
        if inline_dates:
            head.append(_inline_row(org, entry.location or "", typo.right_italic, italic=True))
        else:
            head.append(_row(org, entry.location or "", typo.right_italic))
    return head + _degree_lines(entry, typo)


def _certificate_detail(cert: Certificate, typo: Typography) -> str:
    """Issuer, credential id, and verification link. The date stays on the name line."""
    parts: list[str] = []
    if cert.issuer:
        parts.append(inline(cert.issuer))
    if cert.credential_id:
        parts.append(f"Credential ID {inline(cert.credential_id)}")
    if link := _link(cert.url or "", typo):
        parts.append(link)
    return " | ".join(parts)


def _certificate(cert: Certificate, typo: Typography) -> list[Flowable]:
    # Dates share the name's line, as they do for jobs, so a parser keeps them together.
    # Issuer and credential go underneath: verification URLs are too long for that line.
    left = f"<b>{inline(cert.name)}</b>"
    date_style = typo.right_italic if typo.classic else typo.right
    if typo.style.date_align == "inline":
        row: Flowable = _inline_row(left, cert.date_text, date_style, italic=typo.classic)
    else:
        row = _row(left, cert.date_text, date_style)
    block = [row]
    if detail := _certificate_detail(cert, typo):
        block.append(Paragraph(detail, typo.entry_sub))
    return [Spacer(1, typo.style.base_size * 0.5), KeepTogether(block)]


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
    elif section.certificates:
        for i, cert in enumerate(section.certificates):
            items = _certificate(cert, typo)
            flow += items[1:] if i == 0 else items
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
        title=f"{resume.name} Resume",
        author=resume.name,
        subject=resume.headline or "Resume",
    )

    flow = header(resume.name, resume.headline, resume.contact, typo)
    if resume.summary:
        # A real heading: without one, Workday's autofill read the summary as a job entry.
        if resume.summary_title:
            flow += _section_heading(Section(title=resume.summary_title), typo)
        else:
            flow.append(Spacer(1, style.base_size * 0.6))
        flow.append(Paragraph(inline(resume.summary, typo.link_color), typo.body))
    for section in resume.sections:
        if section.is_empty:
            continue
        flow += _section(section, typo)

    doc.build(flow)
    return doc.page
