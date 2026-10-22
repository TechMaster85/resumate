"""Shared page setup, typography, and header used by both the resume and cover letter.

ATS notes: everything is real, selectable text in standard PDF fonts, laid out in a
single column in reading order. No images, text boxes, or multi-column layouts.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from reportlab.lib.colors import HexColor, black
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4, LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Flowable, Paragraph, SimpleDocTemplate, Spacer

from resumate.markup import inline
from resumate.models import Contact, Style

_FONT_VARIANTS = {
    "Helvetica": ("Helvetica", "Helvetica-Bold", "Helvetica-Oblique"),
    "Times-Roman": ("Times-Roman", "Times-Bold", "Times-Italic"),
    "Courier": ("Courier", "Courier-Bold", "Courier-Oblique"),
}


@dataclass
class Typography:
    style: Style

    def __post_init__(self) -> None:
        s = self.style
        self.classic = s.layout == "classic"
        font = s.font or ("Times-Roman" if self.classic else "Helvetica")
        regular, bold, italic = _FONT_VARIANTS[font]
        self.regular, self.bold, self.italic = regular, bold, italic
        # Classic is all black, like a printed page; modern uses the accent color.
        self.accent = black if self.classic else HexColor(s.accent)
        size = s.base_size
        lead = size * 1.2 if self.classic else size * 1.25

        def ps(name: str, **kw) -> ParagraphStyle:
            base = dict(
                fontName=regular, fontSize=size, leading=lead, textColor=black, alignment=TA_LEFT
            )
            return ParagraphStyle(name, **{**base, **kw})

        if self.classic:
            self.name = ps(
                "name", fontName=bold, fontSize=size * 1.75, leading=size * 2.1, alignment=TA_CENTER
            )
            self.headline = ps("headline", alignment=TA_CENTER)
            self.contact = ps("contact", alignment=TA_CENTER, spaceBefore=size * 0.2)
            self.section = ps(
                "section", fontName=bold, spaceBefore=size * 1.1, spaceAfter=size * 0.15
            )
        else:
            self.name = ps(
                "name",
                fontName=bold,
                fontSize=size * 2.2,
                leading=size * 2.6,
                textColor=self.accent,
            )
            self.headline = ps("headline", fontSize=size * 1.15, leading=size * 1.5)
            self.contact = ps("contact", fontSize=size * 0.92, leading=size * 1.2)
            self.section = ps(
                "section",
                fontName=bold,
                fontSize=size * 1.1,
                leading=size * 1.3,
                textColor=self.accent,
                spaceBefore=size * 0.9,
                spaceAfter=size * 0.15,
            )
        self.body = ps("body")
        self.entry_title = ps("entry_title", fontName=bold)
        self.entry_sub = ps("entry_sub", fontName=italic)
        # Right-aligned date/location cells; `parent` is the style for the left cell.
        self.right = ps("right", parent=self.body, alignment=TA_RIGHT)
        self.right_italic = ps(
            "right_italic", parent=self.body, fontName=italic, alignment=TA_RIGHT
        )
        # Symbol's bullet has an unambiguous character code; the standard fonts' bullet is
        # encoded in a way some PDF parsers (pypdf, possibly some ATS) misread.
        self.bullet = ps(
            "bullet",
            leftIndent=size * 1.4,
            bulletIndent=size * 0.4,
            spaceBefore=size * 0.1,
            bulletFontName="Symbol",
        )
        self.letter_body = ps(
            "letter_body", fontSize=size * 1.08, leading=size * 1.5, spaceAfter=size * 0.8
        )
        self.letter_bullet = ps(
            "letter_bullet",
            parent=self.letter_body,
            leftIndent=size * 1.6,
            bulletIndent=size * 0.5,
            spaceAfter=size * 0.3,
            bulletFontName="Symbol",
        )

    @property
    def link_color(self) -> str | None:
        return None if self.classic else self.style.accent


def page_size(style: Style):
    return LETTER if style.page_size == "letter" else A4


def make_doc(out: Path, style: Style, *, title: str, author: str, subject: str = ""):
    margin = style.margin_in * inch
    return SimpleDocTemplate(
        str(out),
        pagesize=page_size(style),
        leftMargin=margin,
        rightMargin=margin,
        topMargin=margin,
        bottomMargin=margin,
        title=title,
        author=author,
        subject=subject,
        creator="resumate",
    )


def _contact_parts(values: list[str | None]) -> list[str]:
    return [inline(v) for v in values if v]


def _link_parts(contact: Contact, typo: Typography) -> list[str]:
    color = f' color="{typo.link_color}"' if typo.link_color else ""
    parts = []
    for link in contact.links:
        label = inline(link.label)
        parts.append(f'<a href="{link.url}"{color}>{label}</a>' if link.url else label)
    return parts


def header(name: str, headline: str | None, contact: Contact, typo: Typography) -> list[Flowable]:
    if typo.classic:
        # Centered name in capitals; location/email/phone on one line, links on the next.
        flow: list[Flowable] = [Paragraph(inline(name.upper()), typo.name)]
        if headline:
            flow.append(Paragraph(inline(headline), typo.headline))
        lines = [
            _contact_parts([contact.location, contact.email, contact.phone]),
            _link_parts(contact, typo),
        ]
        flow += [Paragraph(" | ".join(line), typo.contact) for line in lines if line]
        return flow

    flow = [Paragraph(inline(name), typo.name)]
    if headline:
        flow.append(Paragraph(inline(headline), typo.headline))
    parts = _contact_parts([contact.email, contact.phone, contact.location])
    parts += _link_parts(contact, typo)
    if parts:
        flow += [Spacer(1, 2), Paragraph("  |  ".join(parts), typo.contact)]
    return flow
