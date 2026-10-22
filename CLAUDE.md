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
- PDFs must stay ATS-safe: standard PDF fonts, single column, real text in reading order.
  Tests assert on `pdf_text()` extraction; verify visual changes by rendering a PDF.
