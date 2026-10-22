"""Reading resume YAML and cover letter Markdown from disk."""

from __future__ import annotations

import re
from pathlib import Path

import yaml
from pydantic import ValidationError

from resumate.models import CoverLetter, Resume, Settings

FRONT_MATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.DOTALL)
HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)


class ResumateError(Exception):
    """An error caused by user content, with a message meant to be shown as-is."""


def split_front_matter(text: str) -> tuple[dict, str]:
    match = FRONT_MATTER.match(text)
    if not match:
        return {}, text
    meta = yaml.safe_load(match.group(1)) or {}
    if not isinstance(meta, dict):
        raise ResumateError("front matter must be a YAML mapping")
    return meta, text[match.end() :]


def strip_comments(markdown: str) -> str:
    """Remove <!-- --> comments, which are notes for the author and never rendered."""
    return HTML_COMMENT.sub("", markdown)


def _format_validation(path: Path, err: ValidationError) -> str:
    lines = [f"{path}: invalid content"]
    for e in err.errors():
        loc = ".".join(str(p) for p in e["loc"]) or "(top level)"
        lines.append(f"  - {loc}: {e['msg']}")
    return "\n".join(lines)


def _read_yaml(path: Path) -> dict:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ResumateError(f"{path}: file not found") from None
    except yaml.YAMLError as e:
        raise ResumateError(f"{path}: YAML syntax error\n{e}") from None
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ResumateError(f"{path}: expected a YAML mapping at the top level")
    return data


def load_resume(path: Path) -> Resume:
    try:
        return Resume.model_validate(_read_yaml(path))
    except ValidationError as e:
        raise ResumateError(_format_validation(path, e)) from None


def load_cover_letter(path: Path) -> CoverLetter:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise ResumateError(f"{path}: file not found") from None
    try:
        meta, body = split_front_matter(text)
    except yaml.YAMLError as e:
        raise ResumateError(f"{path}: front matter YAML syntax error\n{e}") from None
    try:
        return CoverLetter.model_validate({**meta, "body": strip_comments(body).strip()})
    except ValidationError as e:
        raise ResumateError(_format_validation(path, e)) from None


def load_settings(root: Path | None) -> Settings:
    if root is None or not (root / "resumate.yaml").exists():
        return Settings()
    path = root / "resumate.yaml"
    try:
        return Settings.model_validate(_read_yaml(path))
    except ValidationError as e:
        raise ResumateError(_format_validation(path, e)) from None


def read_meta(path: Path) -> dict:
    """Front matter of a Markdown file, or {} if it has none or can't be parsed."""
    try:
        return split_front_matter(path.read_text(encoding="utf-8"))[0]
    except (OSError, yaml.YAMLError, ResumateError):
        return {}
