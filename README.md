# resumate

Your career materials as plain text, tailored per job by an AI agent, compiled into
clean, ATS-friendly PDFs that you review before anything gets sent.

resumate doesn't run your job search. The goal is to get past resume filters honestly
so you get an interview:

1. You keep a **master resume** (everything you've done, at whatever length it takes)
   and a few **work stories** in plain text. Each application copies the master, then
   comments out positions and bullets until that one application fits the page limit.
2. For a job you care about, you tell your agent **why you're interested** and paste
   the **job description**.
3. The agent researches the company, **tailors a resume** (by commenting out and
   reframing master content, never inventing it), **drafts a cover letter** from your
   stories, and **recommends supporting materials**.
4. You review and edit the plain-text files, then compile them with
   `resumate build`.

## Install

From a checkout of this repo:

```bash
uv tool install -e .
```

Or `uv sync` and prefix commands with `uv run`.

## Quick start

```bash
resumate init ~/career --from ~/Downloads/My_Resume.pdf   # PDF, Word, Markdown, or text
cd ~/career
```

Then open an agent in `~/career` and say **"Set up resumate from my resume."** It
rewrites your resume as plain text in `master/resume.yaml`, matching your existing
layout, and flags anything it wants you to confirm. Check the result with
`resumate build master --open`.

No resume file handy? Run `resumate init ~/career` and give the agent your resume
later (a path or pasted text). Until you do, `master/resume.yaml` is sample content,
and `resumate check` and `resumate new` remind you.

For each job, in an agent session (Claude Code, Codex, Gemini CLI, Copilot, Cursor, ...)
opened in `~/career`:

> I'm applying to the Staff Engineer role at Acme. I've used their product for years and
> want to work on their reliability problems. Here's the posting: …

The agent follows the bundled `resumate-apply` skill and leaves everything in
`applications/2026-10-22-acme-staff-engineer/`. Review it:

```bash
resumate check acme          # page limits, text extraction, open TODO(review) notes
resumate diff acme           # how the tailored resume differs from master
resumate build acme --open   # compile resume + cover letter PDFs to out/
resumate status acme applied
```

## Workspace layout

```
career/
  resumate.yaml              style and page-limit settings
  AGENTS.md                  orientation for agents (CLAUDE.md, GEMINI.md import it)
  .agents/skills/            resumate, resumate-apply, resumate-capture
  .claude/skills/            the same skills, for Claude Code
  master/resume.yaml         the master resume
  stories/*.md               work anecdotes for cover letters
  supporting/                portfolio pieces, writing samples, ... (+ optional notes)
  applications/<date>-<company>-<role>/
    job.md                   why you're interested + job description + status
    research.md              agent's research, with sources
    resume.yaml              tailored resume
    cover_letter.md          tailored cover letter
    materials.md             supporting-material recommendations
    out/                     PDFs to submit
```

Put the workspace under git: every tailoring change becomes a reviewable diff.

## File formats

**Resume** (`resume.yaml`): YAML. It's structured enough to validate and for agents to
edit precisely, and unlike JSON, `#` comments out any line, which is how tailoring works. See the example
master resume created by `resumate init` for every field.

```yaml
name: Your Name
headline: Senior Software Engineer
contact: { email: you@example.com, location: "Ann Arbor, MI" }
sections:
  - title: Experience
    entries:
      - title: Senior Software Engineer
        org: Company
        start: Mar 2022
        end: Present
        bullets:
          - Cut event latency from **15 min to 4 s** for 2M daily shipments
          # - A bullet that doesn't fit this job
  - title: Skills
    skills:
      - { category: Languages, items: "Python, Go, SQL" }
```

**Cover letter** (`cover_letter.md`): Markdown with front matter (`company`, `role`,
optional `recipient`, `address`, and `date`). The letterhead (name, email, and phone)
comes from the resume beside it; an inside address prints only for a named recipient
or address. `<!-- comments -->` never render.

**Review markers**: agents flag anything you should confirm with `TODO(review)` in a
comment; `resumate check` lists them all.

## The PDFs

Single column, standard PDF fonts, real selectable text in reading order, and no
multi-column layouts, images, text boxes, or headers/footers: the things applicant
tracking systems parse reliably. `resumate text out/Your_Name_Resume.pdf` shows exactly what an ATS
extracts. Style (font, accent color, size, margins, page size, page limit) is set in
`resumate.yaml` and can be overridden per resume with a `style:` block.

Two layouts:

- **classic** (default): centered serif header with your name in capitals, bold
  underlined section headings, one bold line per entry with the date in italics after
  it. The traditional CS resume format.
- **modern**: left-aligned sans-serif header in an accent color, ruled section headings,
  and a separate italic line for organization and location.

Dates go on the same line as the entry heading (`Senior Engineer | Mar 2022 - Present`),
because some ATS parsers detach flush-right dates from their entry and lose your
timeline. Set `date_align: right` in `style:` for the traditional flush-right look.
Date ranges use plain hyphens, which older parsers read more reliably than en dashes.

## Agent skills

resumate works with any coding agent. It uses two open standards:

- **[AGENTS.md](https://agents.md)** orients the agent to the workspace. `CLAUDE.md` and
  `GEMINI.md` just import it, for agents that look for their own filename.
- **[Agent Skills](https://agentskills.io)** (`SKILL.md` folders) teach the procedures.
  `resumate init` installs them into `.agents/skills/`, the shared location read by
  Codex, Gemini CLI, GitHub Copilot, Cursor and others, and mirrors them into
  `.claude/skills/` for Claude Code. Agents without skill support are pointed to the
  files by `AGENTS.md`.

| Skill | Use |
|---|---|
| `resumate` | File formats and CLI reference |
| `resumate-apply` | Research a role, tailor resume and cover letter, recommend materials, hand off for review |
| `resumate-capture` | Interview you to grow the master resume and stories; first-time setup |

After upgrading resumate, refresh both copies with `resumate install-skills`.

## Library use

```python
from pathlib import Path
from resumate import Style, load_resume, render_resume

resume = load_resume(Path("master/resume.yaml"))
pages = render_resume(resume, Path("out/resume.pdf"), Style(accent="#7A1F1F"))
```

## Development

```bash
uv sync
uv run pytest
uv run ruff check .
```
