---
name: resumate-setup
description: First-time setup of a resumate workspace, turning the user's existing resume into master/resume.yaml. Use when master/resume.yaml still starts with "# resumate:example", when the user says "set up resumate from my resume", or when they give you a resume file or pasted text to import. Also covers building a first master from scratch by interview when they have no resume. One-time; for adding to an existing master later, use resumate-capture.
---

# Set up the master resume

The master resume is the source of truth for every future application, so this import
has to be complete and faithful. Read the `resumate` skill first for the format and
"Parser-safe content".

If there's no workspace yet (no `resumate.yaml` here or above), create one first:
`resumate init <dir>`, or `resumate init <dir> --from <resume>` when they have a file.

1. **Get their current resume.** Look in `master/source/` first (`resumate init --from`
   and `resumate import` put it there; PDFs come with a `.txt` of their text). If it's
   empty, ask the user for it: a file path (PDF, Word, Markdown, LaTeX, plain text,
   LinkedIn export) or pasted text. Save files with `resumate import FILE`. If they have
   no resume at all, build one from scratch by interviewing them, as described in
   `resumate-capture`.
2. **Rewrite it as `master/resume.yaml`**, replacing the sample entirely and removing the
   marker line. Keep *every* bullet and every entry, including ones the source had
   commented out or hidden (keep those commented out with `#`). Preserve their wording;
   fix only obvious typos, each flagged with `# TODO(review): ...` so they can confirm.
   Don't drop details like GPA, coursework, links, certifications, or "source available
   on request" notes.
3. **Make it parser-safe without changing facts**, following "Parser-safe content" in
   the `resumate` skill: move parenthetical details out of org names into bullets, give
   every job a City, ST location, split degrees into `title` (school), `degree`, and
   `major`, keep dates out of the summary, and write the phone without +1. Flag anything
   you had to guess, like a remote job's city, with `# TODO(review): ...`.
4. **Match their look.** If the source is a PDF, compare it with
   `resumate build master --open` and pick the closer `style.layout` (`classic` or
   `modern`) in `resumate.yaml`. Keep `entry_heading: stacked` even if their old resume
   put each job on one line; it's the shape Workday parsed correctly. Set `max_pages` to
   the source's length if it's longer than one page.
5. **Check.** Run `resumate check master` until it's clean apart from review notes, then
   show the user the PDF and list everything you flagged.
6. **Clear the examples.** Delete the example stories in `stories/` and offer to write a
   few real ones together with `resumate-capture`.

Never invent anything to fill a gap in the source. Missing locations, dates, or numbers
become `TODO(review)` questions, not plausible guesses.
