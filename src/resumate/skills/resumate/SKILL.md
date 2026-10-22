---
name: resumate
description: Reference for operating resumate, the plain-text resume and cover letter toolkit. Covers the workspace layout, the resume.yaml and cover_letter.md formats, and every CLI command (init, new, build, check, diff, list, status, attach, text). Use whenever reading, editing, building, or checking files in a resumate workspace (a folder containing resumate.yaml).
---

# resumate reference

resumate keeps a person's career materials as plain text and compiles them into clean,
single-column, ATS-friendly PDFs. The workspace root is the nearest folder containing
`resumate.yaml`. Run CLI commands from anywhere inside it.

## Workspace layout

```
resumate.yaml                 style + page limits
master/resume.yaml            master resume: source of truth for all facts
stories/*.md                  work anecdotes (front matter: title, when, where, tags)
supporting/                   portfolio files; optional `<file>.md` sidecar notes
applications/<date>-<company>-<role>/
  job.md                      front matter (company, role, url, status) + why interested + JD
  research.md                 agent research notes, with sources
  resume.yaml                 tailored resume (starts as a copy of master)
  cover_letter.md             tailored cover letter
  materials.md                supporting-material recommendations
  out/                        compiled PDFs and attached materials
```

## resume.yaml format

```yaml
name: Full Name                 # required
headline: Role · Specialty      # optional, under the name
contact:
  email: a@b.com
  phone: (555) 123-4567
  location: City, ST
  links:
    - label: github.com/user    # shown text; keep it readable, ATS reads the label
      url: https://github.com/user
summary: >                      # optional paragraph under the header
  ...
sections:                       # rendered in this order
  - title: Experience
    entries:                    # jobs, degrees, projects
      - title: Senior Engineer
        org: Company
        location: Remote
        start: Mar 2022         # free text
        end: Present            # or use `dates: 2018 – 2022` instead of start/end
        url: https://github.com/user/repo   # optional, shown after the title
        summary: optional one-line context under the heading (e.g. "Source available on request")
        bullets:
          - Did X, achieving **Y**
          # - Commented-out bullet: excluded from the PDF, kept for reference
  - title: Skills
    skills:
      - category: Languages
        items: Python, Go       # string or list
  - title: Certifications
    bullets: [AWS Solutions Architect, ...]
  - title: Interests
    text: A single paragraph.
style:                          # optional per-file overrides of resumate.yaml style
  max_pages: 2
```

Layouts (`style.layout`): **classic** (default) is a centered serif header, bold
underlined section headings, one bold line per entry (`Title – Org, Location – url`) with
the date in italics on the right, and skills as bullets. **modern** is a left-aligned sans
header in the accent color, ruled headings, and a second italic line for org/location.
In classic, `title` can hold the whole heading (e.g. `University of Michigan, Ann Arbor, MI
– B.S.E. Computer Science`) when a source resume orders it differently.

Rules:
- Each section has one of `entries`, `skills`, `bullets`, `text`. A section whose
  content is all commented out is skipped.
- Unknown keys are errors (catches typos). Run `resumate check` after editing.
- Inline Markdown in any text field: `**bold**`, `*italic*`, `[label](url)`.
- `#` comments are how content is excluded. Preserve the master's structure when
  tailoring so `resumate diff` stays readable.
- YAML gotcha: quote strings that start with `*`, `[`, `{`, `&`, `!`, `%`, `@`, or
  contain `: ` (e.g. `- "Led: the thing"`).
- The PDF fonts cover Western European characters only (Windows-1252). `check` warns
  about anything else (emoji, CJK, some symbols).

## cover_letter.md format

```markdown
---
company: Acme
role: Staff Engineer
recipient: Hiring Team          # or a named person, if known
address: ["optional", "lines"]
date: 2026-01-15                # optional; defaults to build date
---

Dear Hiring Team,

Paragraphs separated by blank lines. Single line breaks are kept.

- Bullet lists work too

Sincerely,
Full Name
```

- The letterhead (name, headline, contact) comes from `resume.yaml` beside the letter,
  falling back to `master/resume.yaml`.
- `<!-- comments -->` never render. Use them for notes to the user.

## Sample content

`resumate init` creates a sample master resume whose first line is `# resumate:example`.
`check` and `new` warn while it's there. Replace the content with the user's real resume
(see `resumate-capture`) and delete the marker line.

## Review markers

Any line containing `TODO`, `FIXME`, or `REVIEW` is reported by `resumate check`. Agents
flag things the user must confirm as `# TODO(review): ...` (YAML) or
`<!-- TODO(review): ... -->` (Markdown). The user deletes the marker once resolved.

## CLI

| Command | Purpose |
|---|---|
| `resumate init DIR [--from RESUME] [--name "Full Name"]` | Create a workspace with examples and skills; `--from` saves an existing resume to `master/source/` |
| `resumate import FILE` | Save an existing resume to `master/source/` (PDFs also get extracted `.txt`) |
| `resumate new COMPANY ROLE [--url URL]` | Create an application folder; prints its path |
| `resumate list` | Applications with status |
| `resumate build [TARGET] [--open] [-o DIR]` | Compile an application folder, `master/`, or one `.yaml`/`.md` file to `out/` |
| `resumate check [TARGET]` | Validate, test page count and text extraction, list review markers; exit 1 on errors |
| `resumate diff [APP]` | Unified diff of an application's resume vs. master |
| `resumate text FILE.pdf` | Print the text an ATS would extract |
| `resumate status APP STATUS` | drafting, ready, applied, interviewing, offer, rejected, withdrawn |
| `resumate attach APP FILE...` | Copy files from `supporting/` into the application's `out/` |
| `resumate install-skills` | Refresh these skills from the installed package |

`APP` accepts a path, the folder name, or any unique substring of it (e.g. `acme`).

## Fitting on the page

When `check` reports too many pages, in order of preference: comment out the least
relevant bullets, drop older or less relevant entries, tighten long bullets (most
should fit on one or two lines), then adjust `style` (`base_size` down to 9.5,
`margin_in` down to 0.5). Don't shrink type below 9.5pt.
