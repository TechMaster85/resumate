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
summary: >                      # optional paragraph, printed under a "Summary" heading
  ...                           # no dates in it (Workday read a dated summary as a job)
summary_title: Summary          # optional; the summary's heading ("" for none, not advised)
sections:                       # rendered in this order
  - title: Experience
    entries:                    # jobs, degrees, projects
      - title: Senior Engineer
        org: Company            # plain name: no commas or parentheses
        location: Detroit, MI   # City, ST on every job; see "Parser-safe content" for remote
        start: Mar 2022         # free text
        end: Present            # or use `dates: 2018 - 2022` instead of start/end
        url: https://github.com/user/repo   # optional, shown after the title
        summary: optional one-line context under the heading (e.g. "Source available on request")
        bullets:
          - Did X, achieving **Y**
          # - Commented-out bullet: excluded from the PDF, kept for reference
  - title: Education
    entries:
      - title: University of Michigan          # the school
        degree: Bachelor of Science in Engineering   # instead of org
        major: Computer Science                 # printed as `Major: Computer Science`
        minor: Mathematics                      # optional
        location: Ann Arbor, MI
        dates: May 2026
  - title: Skills
    skills:
      - category: Languages
        items: Python, Go       # string or list
  - title: Certifications
    certificates:               # name required; every other field optional
      - name: AWS Certified Solutions Architect - Associate
        issuer: Amazon Web Services
        issued: Jun 2024        # free text
        expires: Jun 2027       # omit when it doesn't expire
        credential_id: SAA-EXAMPLE
        url: https://example.com/certs/saa   # verification link
  - title: Awards
    bullets: [Dean's List, team MVP]
  - title: Interests
    text: A single paragraph.
style:                          # optional per-file overrides of resumate.yaml style
  max_pages: 2
```

Layouts (`style.layout`): **modern** (default) is a left-aligned sans header in the
accent color and ruled section headings. **classic** is a centered serif header with the
name in capitals, bold underlined section headings, all-black text, and skills as bullets.

Entry headings (`style.entry_heading`): **stacked** (default) prints `Title | dates` on
one line and `Org | Location` on the next. That is the shape a real Workday resume
autofill parsed correctly (title, company, location, dates, bullets). **one_line** prints
`Title | Org | Location | dates` on one line; it is more compact but untested against
Workday. Both layouts support both headings. For a degree, the org line holds `degree`
and a labeled `Major: ...` line follows.
Dates follow the heading after a `|` (`style.date_align: inline`, the default) so every
PDF parser keeps them with their entry; `date_align: right` puts them flush right, which
looks traditional but some ATS parsers detach right-aligned dates from the entry. Date
ranges are written with a plain hyphen (`Mar 2022 - Present`); en and em dashes in
`dates`, `issued`, and `expires` are converted. Resumate's own separators are pipes,
never en or em dashes, in the text and in the PDF metadata.
A certificate keeps the date on the name's line. The issuer, credential id, and url
follow on the next line, in italics, separated by `|`. With `expires` set, the date
reads `Jun 2024 (expires Jun 2027)`.

## Parser-safe content

Workday's resume autofill was tested against resumate PDFs. These habits came out of
those tests, and `resumate check` warns about each one:

- **Org names are plain.** `Sky Systems`, not `Sky Systems (Microsoft contractor,
  on-call)`. A comma or parentheses split one job into two. Put the detail in a bullet.
- **Every job has a `location: City, ST`.** Without one, Workday split the entry and lost
  the company.
- **Remote work:** a bare `location: Remote` made Workday drop the company and bullets.
  Use the City, ST the person worked from (or the employer's city) and say it was remote
  in a bullet. This workaround is a best guess and hasn't been re-tested in Workday.
- **No dates in the summary.** `May 2026 Computer Science graduate ...` became a fake job.
  Keep dates in Experience and Education. The summary always gets a heading.
- **Degrees use `degree` and `major`.** "Bachelor of Science in Engineering in Computer
  Science" was read as the field "Engineering Physics". School in `title`, degree name in
  `degree`, field in `major`.
- **Phone without +1**: `(586) 555-0100`. Workday's phone field rejected `+1 (586) ...`.
- **No en or em dashes** in any text. Use a hyphen, comma, colon, or pipe.

Rules:
- Each section has one of `entries`, `skills`, `certificates`, `bullets`, `text`. A section
  whose content is all commented out is skipped.
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
recipient: Jane Doe            # optional: a named person, if known
address: ["optional", "lines"]
date: 2026-01-15                # optional; defaults to build date
---

Dear Hiring Team,

Paragraphs separated by blank lines. Single line breaks are kept.

- Bullet lists work too

Sincerely,
Full Name
```

- The letterhead (name, email, phone) comes from `resume.yaml` beside the letter,
  falling back to `master/resume.yaml`. The resume's headline, location, and links are
  left off.
- An inside address (recipient, company, address lines) prints only when `recipient` or
  `address` is set. Leave both out for a generic "Dear Hiring Team," letter.
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
| `resumate check [TARGET]` | Validate, test an application's page count and text extraction, warn about ATS parse risks (see "Parser-safe content"), list review markers; exit 1 on errors. The master resume is not held to the page limit. |
| `resumate diff [APP]` | Unified diff of an application's resume vs. master |
| `resumate text FILE.pdf` | Print the text an ATS would extract |
| `resumate status APP STATUS` | drafting, ready, applied, interviewing, offer, rejected, withdrawn |
| `resumate attach APP FILE...` | Copy files from `supporting/` into the application's `out/` |
| `resumate install-skills [--dest DIR]` | Refresh these skills in `.agents/skills/` and `.claude/skills/` from the installed package |

`APP` accepts a path, the folder name, or any unique substring of it (e.g. `acme`).

## Fitting on the page

The master resume holds every position and bullet and can run as long as it needs.
Trim when tailoring an application, not in the master. `check` enforces `max_pages`
on application resumes only.

When `check` reports too many pages, in order of preference: comment out the least
relevant bullets, drop older or less relevant entries, tighten long bullets (most
should fit on one or two lines), then adjust `style` (`base_size` down to 9.5,
`margin_in` down to 0.5). Don't shrink type below 9.5pt.
