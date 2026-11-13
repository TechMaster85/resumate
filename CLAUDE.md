# resumate (library development)

Python package (`src/resumate/`) + CLI that compiles plain-text resumes/cover letters to
ATS-friendly PDFs, plus agent skills that ship inside the package.

- `uv sync`, `uv run pytest`, `uv run ruff check . && uv run ruff format .`
- `models.py` (pydantic schema) → `loader.py` (YAML/Markdown parsing) → `render/` (ReportLab)
- `workspace.py`: workspace/application folders; `check.py`: pre-submission checks; `cli.py`: click
- `templates/workspace/` is copied by `resumate init`; `templates/application/` by `resumate new`
  (`{{company}}`-style placeholders). `skills/*/SKILL.md` are installed into workspaces.
- When changing the file format or CLI, update `skills/resumate/SKILL.md` and README to match:
  agents rely on the skill as their reference.
- Skills: one job per skill, a description that says when to use it (and which sibling
  to use instead). `skills/resumate/SKILL.md` is the single home for parser-safe rules
  and `skills/resumate-voice/SKILL.md` for writing rules; other skills point to them.
  Keep skills generic (no one user's facts), list new ones in the README and the
  reference's skills table, and use no en or em dashes in skill text.
- PDFs must stay ATS-safe: standard PDF fonts, single column, real text in reading order.
  Tests assert on `pdf_text()` extraction; verify visual changes by rendering a PDF.
- Defaults follow real Workday autofill tests (see CHANGES.md): modern layout, stacked
  entry headings (`Title | dates` / `Org | Location`), inline dates, a "Summary" heading.
  Don't change these without new parse evidence.
- Never emit en or em dashes from resumate's own code (separators, metadata): use a plain
  hyphen, comma, or pipe. `check.py` warns about them in user text.
