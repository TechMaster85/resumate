"""Pre-submission checks: does it parse, fit, read cleanly as text, and is review done?"""

from __future__ import annotations

import re
import tempfile
from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader

from resumate.loader import ResumateError, load_cover_letter, load_resume, load_settings
from resumate.models import Resume
from resumate.render import render_cover_letter, render_resume

REVIEW_MARKER = re.compile(r"\b(TODO|FIXME|REVIEW)\b.*")
LONG_BULLET = 240  # characters; roughly three lines at default size
LONG_LETTER = 400  # words
EXAMPLE_MARKER = "resumate:example"  # first line of the sample master resume
EXAMPLE_WARNING = (
    "still the sample resume from `resumate init`: give your agent your current resume "
    "(or run `resumate import FILE`) to rewrite it in plain text"
)


@dataclass
class Finding:
    level: str  # "error" | "warning" | "note"
    file: str
    message: str


def pdf_text(path: Path) -> str:
    """The text an ATS would extract from the PDF."""
    return "\n".join(page.extract_text() or "" for page in PdfReader(path).pages)


def _unencodable(text: str) -> set[str]:
    # The standard PDF fonts cover Windows-1252; other characters render as blanks or boxes.
    bad = set()
    for ch in set(text):
        try:
            ch.encode("cp1252")
        except UnicodeEncodeError:
            bad.add(ch)
    return bad


def review_markers(path: Path) -> list[Finding]:
    found = []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if m := REVIEW_MARKER.search(line):
            found.append(Finding("note", f"{path.name}:{n}", m.group(0).strip(" ->#")))
    return found


def _check_text(path: Path, raw: str) -> list[Finding]:
    bad = _unencodable(raw)
    if not bad:
        return []
    chars = " ".join(sorted(repr(c) for c in bad))
    return [Finding("warning", path.name, f"characters the PDF fonts can't render: {chars}")]


def page_limit_applies(path: Path) -> bool:
    """Application resumes must fit max_pages. The master is a warehouse and can run long."""
    return not (path.parent.name == "master" and path.name == "resume.yaml")


def check_resume(path: Path, root: Path | None) -> tuple[list[Finding], Resume | None]:
    raw = path.read_text(encoding="utf-8")
    findings = review_markers(path) + _check_text(path, raw)
    if EXAMPLE_MARKER in raw:
        findings.append(Finding("warning", path.name, EXAMPLE_WARNING))
    try:
        resume = load_resume(path)
    except ResumateError as e:
        return findings + [Finding("error", path.name, str(e))], None

    for section in resume.sections:
        for entry in section.entries or []:
            for bullet in entry.bullets:
                if len(bullet) > LONG_BULLET:
                    findings.append(
                        Finding(
                            "warning",
                            path.name,
                            f"long bullet under {entry.title!r}: {bullet[:60]}…",
                        )
                    )
    if not (resume.contact.email or resume.contact.phone):
        findings.append(Finding("warning", path.name, "no email or phone in contact"))

    style = load_settings(root).style.merged(resume.style)
    with tempfile.TemporaryDirectory() as tmp:
        pdf = Path(tmp) / "resume.pdf"
        pages = render_resume(resume, pdf, load_settings(root).style)
        text = pdf_text(pdf)
    if page_limit_applies(path) and pages > style.max_pages:
        findings.append(
            Finding(
                "error",
                path.name,
                f"{pages} pages; the limit is {style.max_pages} (style.max_pages)",
            )
        )
    if resume.name.split()[0].lower() not in text.lower():
        findings.append(Finding("error", path.name, "name not found in extracted PDF text"))
    return findings, resume


def check_cover_letter(path: Path, sender: Resume | None, root: Path | None) -> list[Finding]:
    raw = path.read_text(encoding="utf-8")
    findings = review_markers(path) + _check_text(path, raw)
    try:
        letter = load_cover_letter(path)
    except ResumateError as e:
        return findings + [Finding("error", path.name, str(e))]
    words = len(letter.body.split())
    if words == 0:
        findings.append(Finding("error", path.name, "cover letter body is empty"))
    elif words > LONG_LETTER:
        findings.append(
            Finding(
                "warning",
                path.name,
                f"{words} words; most strong cover letters are under {LONG_LETTER}",
            )
        )
    if sender is not None and words:
        with tempfile.TemporaryDirectory() as tmp:
            pdf = Path(tmp) / "letter.pdf"
            pages = render_cover_letter(letter, sender, pdf, load_settings(root).style)
        if pages > 1:
            findings.append(Finding("warning", path.name, f"cover letter runs {pages} pages"))
    return findings
