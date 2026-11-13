---
name: resumate-capture
description: Grow an existing resumate workspace's master materials by interviewing the user. Use when the user wants to add accomplishments, a new job, project, or certification to their master resume, write up a work story, describe files in supporting/, or (only when they ask) get suggestions for a public project README or a check of their LinkedIn profile against the master. For the first import of an existing resume use resumate-setup; for tailoring one application use resumate-apply.
---

# Capture career material

The master resume and stories are what every future application draws from. Your job
is to help the user get rich, specific, *true* material into them, in their voice.
Read the `resumate` skill for file formats and "Parser-safe content". If
`master/resume.yaml` still starts with `# resumate:example`, run `resumate-setup` first.

## Adding accomplishments

Interview, don't transcribe. For each role or project, ask about:

- The problem, and why it mattered to the business or to users
- What *they* did specifically (versus the team)
- Results, with numbers: scale, time saved, revenue, latency, adoption, team growth.
  If they don't know a number, ask for an honest estimate or describe the change
  qualitatively. Never make one up.

Write bullets as **action + what + measurable result**, one or two lines each, and let
the lengths vary. Add them to the right entry in `master/resume.yaml`. It's fine for the
master to hold more than fits on a page; comment out ones they consider weak rather
than deleting them. New entries follow "Parser-safe content".

When the user mentions a certification, add it under `certificates` (see the `resumate`
skill).

If the user has no resume at all, use these same questions to build the master from
scratch, one role or project at a time.

## Writing a story

Stories power cover letters and interview prep, so capture the texture a bullet can't.
Ask about one specific moment, then write `stories/<short-slug>.md` using the template
in `stories/README.md`: Situation, What I did, Result, **Why it matters to me**. Push
gently for that last section; it's what makes a cover letter sound like a person. Ask
for the messy parts too: what they tried first, what confused them, what they'd do
differently.

Keep the user's own phrasing wherever possible. Show them the draft and ask what's
wrong or missing before saving. When a story or a reason comes up during an
application, offer to save it the same day, in their words, so it isn't reconstructed
from memory later.

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

## Public profiles (only when the user asks)

Recruiters open the links on a resume and often check LinkedIn. Offer these; don't do
them unprompted, and never edit an account or post anything yourself.

- **Project READMEs.** For a public repo the user links, suggest README improvements:
  the problem it solves, the main technical decisions, how to run or test it, and
  working links or screenshots. Suggest text; the user commits it. Never invent
  features, users, or results, and never build a fake demo.
- **LinkedIn consistency.** When the user provides their profile (an export, pasted
  text, or a page they open for you), compare it with the master: titles, employers,
  dates, locations, degrees, and skills. List contradictions and claims on either side
  that the other doesn't support. The user decides what to change. Don't optimize the
  profile for its own sake; the goal is that nothing contradicts.
