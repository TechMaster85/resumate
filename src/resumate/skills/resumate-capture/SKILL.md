---
name: resumate-capture
description: Grow a resumate workspace's master materials by interviewing the user. Use when the user wants to add accomplishments, update their master resume, write up a work story, import an existing resume, or set up resumate for the first time.
---

# Capture career material

The master resume and stories are what every future application draws from. Your job
is to help the user get rich, specific, *true* material into them, in their voice.
Read the `resumate` skill for file formats.

## First-time setup

If `master/resume.yaml` starts with `# resumate:example`, the user hasn't set up yet.

1. **Get their current resume.** Look in `master/source/` first (`resumate init --from`
   and `resumate import` put it there; PDFs come with a `.txt` of their text). If it's
   empty, ask the user for it: a file path (PDF, Word, Markdown, LaTeX, plain text,
   LinkedIn export) or pasted text. Save files with `resumate import FILE`. If they have
   no resume at all, build one from scratch by interviewing them (below).
2. **Rewrite it as `master/resume.yaml`**, replacing the sample entirely and removing the
   marker line. Keep *every* bullet and every entry, including ones the source had
   commented out or hidden (keep those commented out with `#`). Preserve their wording;
   fix only obvious typos, each flagged with `# TODO(review): ...` so they can confirm.
   Don't drop details like GPA, coursework, links, or "source available on request" notes.
3. **Match their look.** If the source is a PDF, compare it with
   `resumate build master --open` and pick the closer `style.layout` (`classic` or
   `modern`) in `resumate.yaml`. Set `max_pages` to the source's length if it's longer
   than one page.
4. Run `resumate check master` until it's clean apart from review notes, then show the
   user the PDF and list anything you flagged.
5. Delete the example stories in `stories/` and offer to write a few real ones together.

## Adding accomplishments

Interview, don't transcribe. For each role or project, ask about:

- The problem, and why it mattered to the business or to users
- What *they* did specifically (versus the team)
- Results, with numbers: scale, time saved, revenue, latency, adoption, team growth.
  If they don't know a number, ask for an honest estimate or describe the change
  qualitatively. Never make one up.

Write bullets as **action + what + measurable result**, one or two lines each. Add them
to the right entry in `master/resume.yaml`. It's fine for the master to hold more than
fits on a page; comment out ones they consider weak rather than deleting them.

When the user mentions a certification, add it under `certificates` (see the resumate skill).

## Writing a story

Stories power cover letters, so capture the texture a bullet can't. Ask about one
specific moment, then write `stories/<short-slug>.md` using the template in
`stories/README.md`: Situation, What I did, Result, **Why it matters to me**. Push
gently for that last section; it's what makes a cover letter sound like a person.

Keep the user's own phrasing wherever possible. Show them the draft and ask what's
wrong or missing before saving.

Prompts that surface good stories:
- A time you changed someone's mind
- Something you built that people actually used
- A failure and what you did next
- When you took on something nobody owned
- The work you're proudest of, and why

## Supporting materials

When the user adds files to `supporting/`, offer to write each file's sidecar note
(`<file>.md`): title, what it shows, and whether it's shareable (`yes`, `ask-first`,
`no`). Ask; don't assume something is shareable.
