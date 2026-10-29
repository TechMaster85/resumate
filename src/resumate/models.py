"""Data models for resumes, cover letters, and workspace settings.

Everything a user writes is plain text (YAML or Markdown). These models validate
that text and give agents precise error messages when something is malformed.
"""

from __future__ import annotations

import datetime as dt
from typing import Annotated, Literal

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, model_validator


def _to_text(value: object) -> object:
    # YAML reads `dates: 2018` as an int and `start: 2022-03-01` as a date; both mean text here.
    if isinstance(value, (int, float, dt.date)) and not isinstance(value, bool):
        return str(value)
    return value


Text = Annotated[str, BeforeValidator(_to_text)]


class _Model(BaseModel):
    # Reject unknown keys so typos ("bulets:") fail loudly instead of silently vanishing.
    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="before")
    @classmethod
    def _drop_empty(cls, data: object) -> object:
        # Commenting out every item under a key (`bullets:` with nothing left) yields None;
        # treat that as absent so tailoring by commenting out never breaks validation.
        if isinstance(data, dict):
            return {k: v for k, v in data.items() if v is not None}
        return data


class Style(_Model):
    # classic: centered serif header, underlined headings, one line per entry heading.
    # modern: left-aligned sans header in the accent color, ruled headings, org/location line.
    layout: Literal["classic", "modern"] = "classic"
    # inline: dates follow the title on the same line, so every PDF parser keeps them with
    # their entry. right: flush right, which some parsers detach from the entry.
    date_align: Literal["inline", "right"] = "inline"
    font: Literal["Helvetica", "Times-Roman", "Courier"] | None = None  # None: layout's default
    accent: str = "#1F3A5F"  # modern layout only
    page_size: Literal["letter", "a4"] = "letter"
    base_size: float = Field(10.0, ge=8, le=13)
    margin_in: float = Field(0.6, ge=0.3, le=1.5)
    max_pages: int = Field(1, ge=1, le=4)

    def merged(self, overrides: dict | None) -> Style:
        if not overrides:
            return self
        return Style(**{**self.model_dump(), **overrides})


class Link(_Model):
    label: Text
    url: Text | None = None


class Contact(_Model):
    email: Text | None = None
    phone: Text | None = None
    location: Text | None = None
    links: list[Link] = []


class Entry(_Model):
    """A job, degree, or project: a title line, an org line, dates, and bullets."""

    title: Text
    org: Text | None = None
    location: Text | None = None
    start: Text | None = None
    end: Text | None = None
    dates: Text | None = None  # free-form alternative to start/end
    url: Text | None = None  # shown after the title, e.g. a project's repo
    summary: Text | None = None
    bullets: list[Text] = []

    @property
    def date_range(self) -> str:
        # Plain hyphens: some older parsers misread en/em dashes in date ranges.
        if self.dates:
            return self.dates.replace("–", "-").replace("—", "-")
        if self.start and self.end:
            return f"{self.start} - {self.end}"
        return self.start or self.end or ""


class SkillGroup(_Model):
    category: Text
    items: Text | list[Text]

    @property
    def text(self) -> str:
        return self.items if isinstance(self.items, str) else ", ".join(self.items)


class Section(_Model):
    """A resume section with at most one of entries / skills / bullets / text.

    A section left with no content (everything commented out) is skipped when rendering.
    """

    title: Text
    entries: list[Entry] | None = None
    skills: list[SkillGroup] | None = None
    bullets: list[Text] | None = None
    text: Text | None = None

    @model_validator(mode="after")
    def _one_kind(self) -> Section:
        kinds = [k for k in ("entries", "skills", "bullets", "text") if getattr(self, k)]
        if len(kinds) > 1:
            raise ValueError(
                f"section {self.title!r} must have only one of entries, skills, bullets, "
                f"or text (found: {', '.join(kinds)})"
            )
        return self

    @property
    def is_empty(self) -> bool:
        return not (self.entries or self.skills or self.bullets or self.text)


class Resume(_Model):
    name: Text
    headline: Text | None = None
    contact: Contact = Contact()
    summary: Text | None = None
    sections: list[Section] = []
    style: dict | None = None  # per-resume overrides of workspace Style


class CoverLetter(_Model):
    """Front matter of a cover letter Markdown file. The body is kept separately."""

    company: Text | None = None
    role: Text | None = None
    recipient: Text | None = None
    address: list[Text] = []
    date: dt.date | str | None = None
    style: dict | None = None
    body: Text = ""


class Settings(_Model):
    """Contents of the workspace's resumate.yaml."""

    style: Style = Style()
