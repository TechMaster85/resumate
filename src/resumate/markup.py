"""A deliberately small Markdown subset, converted to ReportLab paragraph markup.

Supported inline: **bold**, *italic* / _italic_, `code`, [text](url).
Supported blocks: paragraphs (blank-line separated) and "- " / "* " bullet lists.
Anything fancier doesn't belong on a resume or cover letter anyway.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from html import escape

_LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
_BOLD = re.compile(r"\*\*(.+?)\*\*")
_ITALIC = re.compile(r"(?<![\w*])[*_](?!\s)(.+?)(?<!\s)[*_](?![\w*])")
_CODE = re.compile(r"`([^`]+)`")
_BULLET = re.compile(r"^\s*[-*•]\s+")


def inline(text: str, link_color: str | None = None) -> str:
    """Convert inline Markdown to ReportLab markup, escaping everything else."""
    out = escape(" ".join(text.split()), quote=False)
    color = f' color="{link_color}"' if link_color else ""
    out = _LINK.sub(lambda m: f'<a href="{m.group(2)}"{color}>{m.group(1)}</a>', out)
    out = _BOLD.sub(r"<b>\1</b>", out)
    out = _ITALIC.sub(r"<i>\1</i>", out)
    out = _CODE.sub(r'<font face="Courier">\1</font>', out)
    return out


@dataclass
class Block:
    kind: str  # "paragraph" | "bullets"
    lines: list[str]  # source lines of a paragraph, or one item per bullet


def blocks(markdown: str) -> list[Block]:
    """Split Markdown into paragraphs and bullet lists."""
    result: list[Block] = []
    for chunk in re.split(r"\n\s*\n", markdown.strip()):
        lines = [ln for ln in chunk.splitlines() if ln.strip()]
        if not lines:
            continue
        if all(_BULLET.match(ln) or ln.startswith((" ", "\t")) for ln in lines) and _BULLET.match(
            lines[0]
        ):
            items: list[str] = []
            for ln in lines:
                if _BULLET.match(ln):
                    items.append(_BULLET.sub("", ln))
                else:  # continuation line of the previous bullet
                    items[-1] += " " + ln.strip()
            result.append(Block("bullets", items))
        else:
            result.append(Block("paragraph", [ln.strip() for ln in lines]))
    return result
