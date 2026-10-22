---
name: resumate-apply
description: Tailor a resume and cover letter for a specific job using resumate. Use when the user shares a job description or posting link, says why they're interested in a role, or asks for help applying to a job. Researches the company, tailors resume.yaml from the master resume, drafts a cover letter from the user's stories, recommends supporting materials, builds PDFs, and hands everything back for review.
---

# Tailor an application

Goal: help the user show real interest in this role and make an honest, specific case
that they're a great fit. You prepare drafts; **the user reviews, edits, and submits.**
Read the `resumate` skill first if you haven't, for file formats and commands.

## 0. Make sure the master resume is real

If `master/resume.yaml` still has the `# resumate:example` marker, stop: tailoring the
sample would be meaningless. Ask the user for their current resume and run the
`resumate-capture` first-time setup, then come back here.

## 1. Intake

You need two things from the user. Ask for whatever is missing, and don't proceed
without the first:

- **Why they're interested**, in their words. If it's thin ("seems cool"), ask one
  follow-up: what specifically about the company, product, team, or problem?
- **The job description** (pasted text, or a link you can fetch).

Then create the folder and record both verbatim:

```bash
resumate new "Company" "Role Title" --url "https://..."
```

Fill in `job.md`: their reasons under *Why I'm interested* (their words, lightly
cleaned up at most), the full posting under *Job description*.

## 2. Research

Read everything in the workspace first: `master/resume.yaml`, every file in `stories/`,
and `supporting/` (including sidecar `.md` notes). Then research the company and role
using whatever web tools you have:

- What the company does, for whom, its stage, and recent news (launches, funding, layoffs)
- Engineering blog posts, talks, or open source from this team; the product itself
- The values and language the company uses about itself

Write `research.md`: cite a source for every fact. The most important section is
**What they're really looking for**: the 3–5 requirements that matter most, ranked,
reading between the lines of the posting. Then map each to the user's strongest
evidence under **Fit**, and be honest about gaps.

If you can't browse, say so, research from the posting alone, and note that in
`research.md`.

## 3. Tailor the resume

Edit the application's `resume.yaml` (already a copy of the master):

- **Select**: comment out (`#`) bullets, entries, and skills that don't serve this
  role. Keep the master's order of sections unless there's a clear reason to change it.
- **Order**: within each entry, move the most relevant bullets to the top.
- **Reframe**: reword bullets to foreground what this role cares about, and mirror the
  posting's terminology where it's *accurate* (ATS keyword matching is literal: if they
  say "Kubernetes" and the user did Kubernetes work, say "Kubernetes").
- **Headline and summary**: adjust to speak to this role.
- **Never** add an accomplishment, metric, tool, or title that isn't in the master, the
  stories, or the conversation. If a reframe stretches the original, or you think a
  real metric exists but you don't know it, leave `# TODO(review): ...`.

Then:

```bash
resumate check <app>     # fix errors; get to the page limit
resumate diff <app>      # sanity-check that every change is defensible
```

## 4. Draft the cover letter

Edit `cover_letter.md`. Aim for 250–350 words, three or four paragraphs:

1. **Opening**: the specific reason they want *this* job, built from their own words in
   `job.md` and your research. No "I am writing to apply for...".
2. **Proof**: one or two stories from `stories/` that map to the top requirements.
   Concrete details and results, told briefly. Connect each explicitly to what the
   company needs.
3. **Close**: what they'd bring and a plain invitation to talk.

Voice: write like the user writes. Reuse their phrasing from stories and `job.md`.
Avoid stock phrases ("I am thrilled", "passionate about leveraging", "fast-paced
environment", "I believe I would be a great fit"). No claims about the company you
couldn't cite. Use a named recipient only if research found one confidently;
otherwise "Hiring Team". Sign off with the user's name from the resume.

## 5. Supporting materials

Review `supporting/` against this role and write `materials.md`: what to include and
why, what you considered and rejected, and anything worth creating. Respect
`shareable:` in sidecar notes (`ask-first` → flag it; `no` → never recommend). Fewer is
better: only recommend what clearly strengthens the application. Don't attach anything;
the user decides.

## 6. Build and hand off

```bash
resumate check <app>
resumate build <app>
```

Then give the user a short summary:

- Paths to the PDFs (`out/`) and the source files to edit
- The 3–5 requirements you optimized for, and the main tailoring choices
- **Every `TODO(review)` item** they need to resolve (from `resumate check`)
- Your supporting-materials recommendation in one line
- How to iterate: edit the files directly, or tell you what to change, then
  `resumate build <app> --open`

Leave `status: drafting`. The user sets `ready`/`applied` themselves
(`resumate status <app> applied`).

## When you learn something new

If the user mentions an accomplishment or story during this process that isn't in the
master materials, offer to add it there too (see `resumate-capture`), so future
applications benefit.
