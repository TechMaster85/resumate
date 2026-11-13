"""The career workspace: a folder of plain-text career materials and per-job applications.

my-career/
  resumate.yaml          workspace settings (style, page limits)
  AGENTS.md              orientation for AI agents (CLAUDE.md, GEMINI.md import it)
  .agents/skills/        Agent Skills that teach agents to operate resumate
  .claude/skills/        the same skills, where Claude Code looks for them
  master/resume.yaml     everything you've done; tailored copies comment things out
  stories/*.md           work anecdotes for cover letters and interviews
  supporting/            portfolio pieces, writing samples, transcripts, ...
  applications/<date>-<company>-<role>/
    job.md               why you're interested + screening questions + the job description
    research.md          the agent's notes on the company and role
    resume.yaml          tailored resume
    cover_letter.md      tailored cover letter
    answers.md           drafted answers for the application form's questions
    materials.md         which supporting materials to include, and why
    interview-prep.md    prep guide, written by an agent once there's an interview
    out/                 compiled PDFs
"""

from __future__ import annotations

import datetime as dt
import re
import shutil
from dataclasses import dataclass
from importlib import resources
from importlib.resources.abc import Traversable
from pathlib import Path

from resumate.check import EXAMPLE_MARKER, pdf_text
from resumate.loader import ResumateError, read_meta

MARKER = "resumate.yaml"
STATUSES = ("drafting", "ready", "applied", "interviewing", "offer", "rejected", "withdrawn")
# Where agents discover skills (agentskills.io format). `.agents/skills` is the shared
# location (Codex, Gemini CLI, Copilot, Cursor, ...); Claude Code only reads its own.
SKILL_DIRS = (".agents/skills", ".claude/skills")


def _templates() -> Traversable:
    return resources.files("resumate") / "templates"


def _skills() -> Traversable:
    return resources.files("resumate") / "skills"


def _copy_tree(src: Traversable, dest: Path, *, overwrite: bool) -> list[Path]:
    written: list[Path] = []
    dest.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        target = dest / item.name
        if item.is_dir():
            written += _copy_tree(item, target, overwrite=overwrite)
        elif overwrite or not target.exists():
            target.write_bytes(item.read_bytes())
            written.append(target)
    return written


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def find_root(start: Path | None = None) -> Path | None:
    """Walk up from `start` to the nearest directory containing resumate.yaml."""
    here = (start or Path.cwd()).resolve()
    for candidate in (here, *here.parents):
        if (candidate / MARKER).is_file():
            return candidate
    return None


def require_root(start: Path | None = None) -> Path:
    root = find_root(start)
    if root is None:
        raise ResumateError(
            "not inside a resumate workspace (no resumate.yaml found in this directory or any "
            "parent). Run `resumate init <dir>` to create one."
        )
    return root


def init_workspace(
    path: Path, *, name: str | None = None, existing_resume: Path | None = None
) -> list[Path]:
    """Create a workspace with example content. Never overwrites existing files."""
    if (path / MARKER).exists():
        raise ResumateError(f"{path} is already a resumate workspace")
    if existing_resume and not existing_resume.is_file():
        raise ResumateError(f"{existing_resume} not found")
    written = _copy_tree(_templates() / "workspace", path, overwrite=False)
    for skill_dir in SKILL_DIRS:
        written += install_skills(path / skill_dir)
    if name:
        resume = path / "master" / "resume.yaml"
        resume.write_text(resume.read_text().replace("Jordan Rivera", name, 1))
    if existing_resume:
        written += import_source(path, existing_resume)
    return written


def import_source(root: Path, resume: Path) -> list[Path]:
    """Store an existing resume in master/source/ for an agent to rewrite as resume.yaml.

    PDFs also get a .txt of their extracted text, since that's what the agent will read.
    """
    dest_dir = root / "master" / "source"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / resume.name
    shutil.copy2(resume, dest)
    written = [dest]
    if resume.suffix.lower() == ".pdf":
        text = dest.with_name(dest.name + ".txt")
        text.write_text(pdf_text(dest), encoding="utf-8")
        written.append(text)
    return written


def is_example(resume: Path) -> bool:
    """Whether a resume file still contains the sample content from `resumate init`."""
    try:
        return EXAMPLE_MARKER in resume.read_text(encoding="utf-8")
    except OSError:
        return False


def install_skills(dest: Path, *, overwrite: bool = True) -> list[Path]:
    """Copy the bundled agent skills into `dest` (e.g. <workspace>/.agents/skills)."""
    return _copy_tree(_skills(), dest, overwrite=overwrite)


@dataclass
class Application:
    path: Path
    company: str
    role: str
    status: str
    created: str

    @property
    def name(self) -> str:
        return self.path.name


def new_application(
    root: Path, company: str, role: str, *, url: str = "", today: dt.date | None = None
) -> Path:
    today = today or dt.date.today()
    app = root / "applications" / f"{today.isoformat()}-{slugify(company)}-{slugify(role)}"
    if app.exists():
        raise ResumateError(f"{app} already exists")
    master = root / "master" / "resume.yaml"
    if not master.exists():
        raise ResumateError(f"{master} not found; the master resume is the starting point")

    values = {"company": company, "role": role, "url": url, "date": today.isoformat()}

    def fill(text: str) -> str:
        for key, value in values.items():
            text = text.replace("{{" + key + "}}", value)
        return text

    app.mkdir(parents=True)
    for item in (_templates() / "application").iterdir():
        (app / item.name).write_text(fill(item.read_text(encoding="utf-8")), encoding="utf-8")

    # Start from the master resume verbatim, comments included, so the diff stays reviewable.
    banner = (
        f"# Tailored resume for {role} at {company}.\n"
        f"# Started from master/resume.yaml on {today.isoformat()}. Comment out (#) or delete\n"
        f"# what doesn't serve this role; `resumate diff` shows changes vs. the master.\n\n"
    )
    (app / "resume.yaml").write_text(banner + master.read_text(encoding="utf-8"), encoding="utf-8")
    (app / "out").mkdir()
    return app


def list_applications(root: Path) -> list[Application]:
    apps: list[Application] = []
    for job in sorted((root / "applications").glob("*/job.md")):
        meta = read_meta(job)
        apps.append(
            Application(
                path=job.parent,
                company=str(meta.get("company", "?")),
                role=str(meta.get("role", "?")),
                status=str(meta.get("status", "?")),
                created=str(meta.get("created", "")),
            )
        )
    return apps


def resolve_application(root: Path, ref: str | None) -> Path:
    """Find an application by path, exact folder name, or unique substring."""
    if ref is None:
        here = Path.cwd().resolve()
        for candidate in (here, *here.parents):
            if (candidate / "job.md").is_file():
                return candidate
        raise ResumateError("no application given and the current directory isn't inside one")
    direct = Path(ref)
    if (direct / "job.md").is_file():
        return direct.resolve()
    matches = [a.path for a in list_applications(root) if ref.lower() in a.name.lower()]
    if len(matches) == 1:
        return matches[0]
    if not matches:
        raise ResumateError(f"no application matches {ref!r}; see `resumate list`")
    names = "\n  ".join(m.name for m in matches)
    raise ResumateError(f"{ref!r} matches several applications:\n  {names}")


def set_status(app: Path, status: str) -> None:
    if status not in STATUSES:
        raise ResumateError(f"unknown status {status!r}; choose from {', '.join(STATUSES)}")
    job = app / "job.md"
    text = job.read_text(encoding="utf-8")
    updated, count = re.subn(r"(?m)^status:.*$", f"status: {status}", text, count=1)
    if count == 0:
        raise ResumateError(f"{job} has no `status:` line in its front matter")
    job.write_text(updated, encoding="utf-8")


def output_name(person: str, kind: str) -> str:
    """Recruiter-friendly filename, e.g. Jordan_Rivera_Resume.pdf."""
    return f"{re.sub(r'[^A-Za-z0-9]+', '_', person).strip('_')}_{kind}.pdf"


def copy_supporting(root: Path, app: Path, names: list[str]) -> list[Path]:
    """Copy chosen supporting materials into the application's out/ folder."""
    copied = []
    for name in names:
        src = root / "supporting" / name
        if not src.is_file():
            raise ResumateError(f"{src} not found")
        dest = app / "out" / src.name
        shutil.copy2(src, dest)
        copied.append(dest)
    return copied
