"""Render a CoverLetter to PDF, using the sender's resume for the letterhead."""

from __future__ import annotations

import datetime as dt
from pathlib import Path

from reportlab.platypus import Flowable, HRFlowable, Paragraph, Spacer

from resumate.markup import blocks, inline
from resumate.models import CoverLetter, Resume, Style
from resumate.render.common import Typography, header, make_doc


def _date_text(value: dt.date | str | None) -> str:
    if isinstance(value, str):
        return value
    day = value or dt.date.today()
    return f"{day:%B} {day.day}, {day.year}"


def render_cover_letter(letter: CoverLetter, sender: Resume, out: Path, style: Style) -> int:
    """Write the cover letter PDF to `out` and return its page count."""
    style = style.merged(sender.style).merged(letter.style)
    typo = Typography(style)
    out.parent.mkdir(parents=True, exist_ok=True)
    subject = " – ".join(p for p in ("Cover Letter", letter.role, letter.company) if p)
    doc = make_doc(
        out, style, title=f"{sender.name} – {subject}", author=sender.name, subject=subject
    )

    flow: list[Flowable] = header(sender.name, sender.headline, sender.contact, typo)
    flow += [
        Spacer(1, style.base_size * 0.4),
        HRFlowable(width="100%", thickness=0.6, color=typo.accent),
        Spacer(1, style.base_size * 1.6),
        Paragraph(_date_text(letter.date), typo.letter_body),
    ]

    recipient = [r for r in (letter.recipient, letter.company, *letter.address) if r]
    if recipient:
        flow.append(Paragraph("<br/>".join(inline(r) for r in recipient), typo.letter_body))

    for block in blocks(letter.body):
        if block.kind == "bullets":
            flow += [
                Paragraph(inline(item, typo.link_color), typo.letter_bullet, bulletText="•")
                for item in block.lines
            ]
        else:
            # Letters keep single line breaks so sign-offs ("Sincerely,\nJane") render as typed.
            text = "<br/>".join(inline(ln, typo.link_color) for ln in block.lines)
            flow.append(Paragraph(text, typo.letter_body))

    doc.build(flow)
    return doc.page
