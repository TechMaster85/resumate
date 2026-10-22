"""resumate: plain-text career materials, tailored by AI agents, compiled into ATS-friendly PDFs.

The CLI (`resumate --help`) covers everyday use. The same operations are available as a library:

    from resumate import load_resume, render_resume, Style
    render_resume(load_resume(Path("resume.yaml")), Path("out/resume.pdf"), Style())
"""

from resumate.loader import ResumateError, load_cover_letter, load_resume
from resumate.models import CoverLetter, Resume, Style
from resumate.render import render_cover_letter, render_resume

__version__ = "0.1.0"

__all__ = [
    "CoverLetter",
    "Resume",
    "ResumateError",
    "Style",
    "load_cover_letter",
    "load_resume",
    "render_cover_letter",
    "render_resume",
]
