"""Command-line interface: `resumate --help`."""

from __future__ import annotations

import difflib
from pathlib import Path

import click

from resumate import __version__
from resumate.check import (
    EXAMPLE_WARNING,
    Finding,
    check_cover_letter,
    check_resume,
    page_limit_applies,
    pdf_text,
    review_markers,
)
from resumate.loader import ResumateError, load_cover_letter, load_resume, load_settings
from resumate.models import Resume
from resumate.render import render_cover_letter, render_resume
from resumate.workspace import (
    SKILL_DIRS,
    STATUSES,
    copy_supporting,
    find_root,
    import_source,
    init_workspace,
    install_skills,
    is_example,
    list_applications,
    new_application,
    output_name,
    require_root,
    resolve_application,
    set_status,
)

RESUME_FILE = "resume.yaml"
LETTER_FILE = "cover_letter.md"


class _Group(click.Group):
    """Turn ResumateError into a clean message instead of a traceback."""

    def invoke(self, ctx: click.Context):
        try:
            return super().invoke(ctx)
        except ResumateError as e:
            raise click.ClickException(str(e)) from None


@click.group(cls=_Group)
@click.version_option(__version__, prog_name="resumate")
def main() -> None:
    """Plain-text career materials, tailored by AI agents, compiled into ATS-friendly PDFs."""


# --- workspace -------------------------------------------------------------------------


_SETUP_PROMPT = (
    'Open an agent in this folder and say: "Set up resumate from my resume."\n'
    "It will rewrite your resume as master/resume.yaml and help you write a few stories."
)


@main.command()
@click.argument("directory", type=click.Path(file_okay=False, path_type=Path), default=".")
@click.option("--name", help="Your name, filled into the example master resume.")
@click.option(
    "--from",
    "existing",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="Your current resume (PDF, Word, Markdown, text) to convert into the master resume.",
)
def init(directory: Path, name: str | None, existing: Path | None) -> None:
    """Create a career workspace in DIRECTORY with examples and agent skills."""
    written = init_workspace(directory, name=name, existing_resume=existing)
    click.echo(f"Created resumate workspace in {directory.resolve()} ({len(written)} files).\n")
    if existing:
        click.echo(f"Saved {existing.name} to master/source/.")
    else:
        click.secho(
            "Next: have your current resume handy (PDF, Word, Markdown, or text). "
            "master/resume.yaml is sample content until it's replaced with yours.",
            fg="yellow",
        )
    click.echo(_SETUP_PROMPT)


@main.command(name="import")
@click.argument("file", type=click.Path(exists=True, dir_okay=False, path_type=Path))
def import_cmd(file: Path) -> None:
    """Save an existing resume to master/source/ for your agent to convert."""
    for path in import_source(require_root(), file):
        click.echo(f"Wrote {path}")
    click.echo(_SETUP_PROMPT)


@main.command()
@click.argument("company")
@click.argument("role")
@click.option("--url", default="", help="Link to the job posting.")
def new(company: str, role: str, url: str) -> None:
    """Start an application folder for ROLE at COMPANY."""
    root = require_root()
    if is_example(root / "master" / RESUME_FILE):
        click.secho(f"warning: master/resume.yaml is {EXAMPLE_WARNING}", fg="yellow")
    app = new_application(root, company, role, url=url)
    click.echo(f"Created {app}")
    click.echo("Paste the job description and why you're interested into job.md.")


@main.command(name="list")
def list_cmd() -> None:
    """List applications and their status."""
    apps = list_applications(require_root())
    if not apps:
        click.echo("No applications yet. Start one with `resumate new COMPANY ROLE`.")
        return
    width = max(len(a.name) for a in apps)
    for a in apps:
        click.echo(f"{a.name:<{width}}  {a.status:<12}  {a.role} @ {a.company}")


@main.command()
@click.argument("application")
@click.argument("new_status", type=click.Choice(STATUSES))
def status(application: str, new_status: str) -> None:
    """Set an application's status (drafting, ready, applied, ...)."""
    app = resolve_application(require_root(), application)
    set_status(app, new_status)
    click.echo(f"{app.name}: {new_status}")


@main.command()
@click.argument("application")
@click.argument("files", nargs=-1, required=True)
def attach(application: str, files: tuple[str, ...]) -> None:
    """Copy supporting materials (paths relative to supporting/) into APPLICATION/out/."""
    root = require_root()
    for dest in copy_supporting(root, resolve_application(root, application), list(files)):
        click.echo(f"Copied {dest}")


@main.command(name="install-skills")
@click.option(
    "--dest",
    type=click.Path(file_okay=False, path_type=Path),
    help="Target directory (default: <workspace>/.agents/skills and <workspace>/.claude/skills).",
)
def install_skills_cmd(dest: Path | None) -> None:
    """Install or update the bundled agent skills."""
    dests = [dest] if dest else [require_root() / skill_dir for skill_dir in SKILL_DIRS]
    for target in dests:
        for path in install_skills(target):
            click.echo(f"Wrote {path}")


# --- building --------------------------------------------------------------------------


def _sender_for(letter_path: Path, root: Path | None) -> Resume:
    """The letterhead comes from the resume beside the letter, else the master resume."""
    for candidate in (
        letter_path.parent / RESUME_FILE,
        root / "master" / RESUME_FILE if root else None,
    ):
        if candidate and candidate.exists():
            return load_resume(candidate)
    raise ResumateError(f"no {RESUME_FILE} next to {letter_path} or in master/ for the letterhead")


def _resolve_target(ref: str) -> Path:
    """A path, a workspace-relative path like `master`, or an application name like `acme`."""
    if Path(ref).exists():
        return Path(ref).resolve()
    root = find_root()
    if root and (root / ref).exists():
        return root / ref
    if root:
        return resolve_application(root, ref)
    raise ResumateError(f"{ref} not found")


def _targets(target: Path) -> tuple[Path | None, Path | None]:
    if target.is_dir():
        resume, letter = target / RESUME_FILE, target / LETTER_FILE
        found = (resume if resume.exists() else None, letter if letter.exists() else None)
        if found == (None, None):
            raise ResumateError(f"{target} has no {RESUME_FILE} or {LETTER_FILE}")
        return found
    if target.suffix in (".yaml", ".yml"):
        return target, None
    if target.suffix == ".md":
        return None, target
    raise ResumateError(f"don't know how to build {target}; expected a folder, .yaml, or .md")


@main.command()
@click.argument("target", default=".")
@click.option(
    "-o",
    "--out-dir",
    type=click.Path(file_okay=False, path_type=Path),
    help="Where to write PDFs (default: an out/ folder beside the source).",
)
@click.option("--open", "open_after", is_flag=True, help="Open the PDFs when done.")
def build(target: str, out_dir: Path | None, open_after: bool) -> None:
    """Compile TARGET to PDF.

    TARGET is an application (folder or name, e.g. `acme`), `master`, or a single .yaml
    resume or .md cover letter. Defaults to the current directory.
    """
    path = _resolve_target(target)
    root = find_root(path)
    style = load_settings(root).style
    resume_path, letter_path = _targets(path)
    built: list[Path] = []

    if resume_path:
        resume = load_resume(resume_path)
        out = (out_dir or resume_path.parent / "out") / output_name(resume.name, "Resume")
        pages = render_resume(resume, out, style)
        limit = style.merged(resume.style).max_pages
        click.echo(f"Built {out} ({pages} page{'s' * (pages != 1)})")
        if page_limit_applies(resume_path) and pages > limit:
            click.secho(
                f"  warning: over the {limit}-page limit; trim or comment out content", fg="yellow"
            )
        built.append(out)

    if letter_path:
        letter = load_cover_letter(letter_path)
        sender = _sender_for(letter_path, root)
        out = (out_dir or letter_path.parent / "out") / output_name(sender.name, "Cover_Letter")
        pages = render_cover_letter(letter, sender, out, style)
        click.echo(f"Built {out} ({pages} page{'s' * (pages != 1)})")
        built.append(out)

    if open_after:
        for path in built:
            click.launch(str(path))


# --- review ----------------------------------------------------------------------------


_COLORS = {"error": "red", "warning": "yellow", "note": "cyan"}


@main.command()
@click.argument("target", default=".")
def check(target: str) -> None:
    """Check TARGET before submitting: validity, page count, text extraction, open TODOs.

    Lines containing TODO, FIXME, or REVIEW are listed as notes: agents use them to flag
    anything the user should confirm. Exits non-zero if there are errors.
    """
    path = _resolve_target(target)
    root = find_root(path)
    resume_path, letter_path = _targets(path)
    findings: list[Finding] = []
    sender = None
    if resume_path:
        found, sender = check_resume(resume_path, root)
        findings += found
    if letter_path:
        if sender is None:
            try:
                sender = _sender_for(letter_path, root)
            except ResumateError:
                pass
        findings += check_cover_letter(letter_path, sender, root)
    if path.is_dir():
        for notes in ("materials.md", "answers.md"):
            if (path / notes).exists():
                findings += review_markers(path / notes)

    for f in findings:
        click.secho(f"{f.level:>7}  {f.file}: {f.message}", fg=_COLORS[f.level])
    errors = sum(f.level == "error" for f in findings)
    notes = sum(f.level == "note" for f in findings)
    if errors:
        raise SystemExit(1)
    click.secho(f"OK{f' ({notes} review note(s) to resolve)' if notes else ''}", fg="green")


@main.command()
@click.argument("application", required=False)
def diff(application: str | None) -> None:
    """Show how an application's resume differs from the master resume."""
    root = require_root()
    app = resolve_application(root, application)
    master = (root / "master" / RESUME_FILE).read_text(encoding="utf-8").splitlines()
    tailored = (app / RESUME_FILE).read_text(encoding="utf-8").splitlines()
    lines = difflib.unified_diff(
        master, tailored, "master/resume.yaml", f"{app.name}/resume.yaml", lineterm=""
    )
    colors = {"+": "green", "-": "red", "@": "cyan"}
    for line in lines:
        click.secho(line, fg=colors.get(line[:1]))


@main.command()
@click.argument("pdf", type=click.Path(exists=True, dir_okay=False, path_type=Path))
def text(pdf: Path) -> None:
    """Print the text an ATS would extract from PDF."""
    click.echo(pdf_text(pdf))
