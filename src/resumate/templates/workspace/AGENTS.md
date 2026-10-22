# Career workspace (resumate)

This folder holds one person's career materials as plain text. You're here to help them
**show genuine interest in a role and make the case that they're a great fit**. You don't
run their job search and you never submit anything: the user reviews and edits every file
before it goes anywhere.

## First run: get the user's real resume

If `master/resume.yaml` starts with the `resumate:example` marker, it is still sample
content. Before anything else, **ask the user for their current resume** (PDF, Word,
Markdown, or plain text; a file path or pasted text both work) and rewrite it as plain
text in `master/resume.yaml` using the `resumate-capture` skill. Check `master/source/`
first: `resumate init --from` and `resumate import` leave it there (PDFs with a `.txt`
of their extracted text). Don't tailor applications from the sample content.

## Layout

| Path | What it is |
|---|---|
| `master/resume.yaml` | Everything the user has done. Source of truth for facts. |
| `stories/*.md` | Work anecdotes in the user's voice, for cover letters. |
| `supporting/` | Portfolio pieces, writing samples, etc., with optional `<file>.md` notes. |
| `applications/<date>-<company>-<role>/` | One folder per job: `job.md`, `research.md`, `resume.yaml`, `cover_letter.md`, `materials.md`, `out/`. |
| `resumate.yaml` | Style and page-limit settings. |

## Skills

Load the matching skill before acting. They're [Agent Skills](https://agentskills.io) in
`.agents/skills/` (mirrored in `.claude/skills/` for Claude Code):

- **resumate** — file formats and CLI reference. Read before editing any resumate file.
- **resumate-apply** — tailor a resume and cover letter for a specific job.
- **resumate-capture** — add accomplishments and stories to the master materials.

If your agent doesn't load skills automatically, read `.agents/skills/<name>/SKILL.md`
directly and follow it.

## Ground rules

1. **Never invent facts.** Every claim, number, title, and date must trace back to
   `master/resume.yaml`, `stories/`, or something the user told you in this conversation.
   Rewording and reframing are fine; new accomplishments are not.
2. **Flag, don't guess.** When something needs the user's confirmation, leave a
   `TODO(review): ...` comment (`#` in YAML, `<!-- -->` in Markdown). `resumate check`
   lists every one.
3. **Keep it reviewable.** Prefer commenting out master content over deleting it, so
   `resumate diff` shows the user exactly what changed.
4. **Sound like the user.** Borrow phrasing from their stories and from what they said
   about why they want the job. Avoid generic AI cover-letter language.
