# Career workspace (resumate)

This folder holds one person's career materials as plain text. **The goal is to get past
resume filters honestly, so the user gets an interview.** Use real experience and the
posting's own words when they are true. Do not invent facts. You don't run their job
search and you never submit anything: the user reviews and edits every file before it
goes anywhere.

## Workflow

1. **No workspace yet.** If this directory has no `resumate.yaml`, create one before
   anything else: `resumate init <dir>`, or `resumate init <dir> --from <resume>` when
   they already have a file. Then work inside that directory.

2. **Master resume.** Encourage them to provide an existing resume (PDF, Word, Markdown,
   or pasted text) and as much other detail as they will give. Rewrite it as
   `master/resume.yaml` with the `resumate-capture` skill. Check `master/source/` first.
   If `master/resume.yaml` still starts with `# resumate:example`, it is sample content:
   do not tailor from it.

3. **Stories and supporting files.** Save interview-worthy stories as `stories/*.md`,
   including ones that may not go on a resume yet. Encourage portfolio pieces and other
   proof in `supporting/`. The user can be completely honest, including things a
   recruiter should not read. Keep that candor in the stories, `job.md`, and
   `research.md`. The resume and cover letter that a filter and a recruiter will read
   stay true, and they include the real matches that earn the interview.

4. **A job description.** Ask why the job appeals to them, in their words. Ask the story
   prompts from `resumate-capture` so anything new gets saved before you draft. Then
   follow `resumate-apply`: tailor that application's `resume.yaml` from the master so
   the filter sees the real match, and write `cover_letter.md` in their voice so a
   person wants to interview them. Not a generated letter. Both files are plain text they can edit with or without you. `resumate build`
   writes the PDFs into that application's `out/` folder. The posting, the sources, and
   the PDFs all live in that one application folder.

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

- **resumate**: file formats and CLI reference. Read before editing any resumate file.
- **resumate-apply**: tailor a resume and cover letter for a specific job.
- **resumate-capture**: add accomplishments and stories to the master materials.

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
5. **Write for the parser, then the person.** Follow "Parser-safe content" in the
   `resumate` skill (plain org names, City, ST locations, no dates in the summary,
   `degree`/`major` for education, no en or em dashes) and clear the parse warnings
   from `resumate check`.
6. **Candor is input, not copy.** The user can tell you anything, including what they
   don't know or don't enjoy. Use it to decide what gets past the filter. What the
   employer reads must be true, and it should be the part that earns the interview:
   keep what helps, reframe what has a strength inside it, and leave the rest for
   interview prep in `research.md`.
