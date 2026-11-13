---
name: resumate-apply
description: Coordinate one job application in resumate from posting to handoff. Use when the user shares a job description or posting link, says why they're interested in a role, or asks for help applying to a job. Handles intake (posting, the user's reasons, screening questions), then runs resumate-research, resumate-tailor, resumate-cover-letter, resumate-questions, and resumate-review in order, recommends supporting materials, builds the PDFs, and hands everything back. Use a sibling skill directly when the user wants only one piece redone (for example just the letter). Not for finding job openings; resumate starts once the user has a posting.
---

# Coordinate an application

Goal: get past the resume filter honestly, so a person sets up an interview. Make the
real match visible in the posting's own words, and make everything the employer reads
sound like the user. You prepare drafts; **the user reviews, edits, and submits.** You
never submit an application, and you never change `status` past `drafting`.

**Quality over volume.** A few strong, tailored applications beat many weak ones. Never
mass-apply, never pad a week with weak-fit roles to "get more out," and never offer to
fill in or submit forms in bulk. The user sets their own weekly number; help them make
each one count. When a company's own career site and a one-click board both carry the
posting, suggest the company site.

**Candor is input, not copy.** Encourage the user to be blunt with you: what they don't
know, what they'd rather not do, what they like more than what the job asks for. You need
that to tailor well. But not everything true belongs in the application. Every sentence
the employer reads must be true; not every truth needs a sentence. For each candid thing
the user says, decide whether it helps this employer say yes:

- **Use it** if it's a reason to hire them. Keep their meaning and voice.
- **Reframe it** if there's a strength inside it. "I like AI because I care more about
  what the customer wants than solving technical problems" becomes "AI tools let me spend
  more of my time on what the customer actually needs," not a confession that they find
  technical problems less interesting.
- **Leave it out** if it only gives a reader a reason to say no (a gap, a preference, a
  doubt, an unflattering comparison). Note it in `research.md` for interview prep instead.

Never misstate hard eligibility facts (degree status, dates, work authorization), and
never imply something false by omission that a background check would contradict. Never
invent facts: every claim traces to `master/resume.yaml`, `stories/`, or this
conversation. Read the `resumate` skill first if you haven't, for file formats, commands,
and "Parser-safe content".

## 0. Make sure the master resume is real

If `master/resume.yaml` still has the `# resumate:example` marker, stop: tailoring the
sample would be meaningless. Ask for the user's current resume and run `resumate-setup`,
then come back here.

## 1. Intake

You need two things from the user:

- **The job description** (pasted text, or a link you can fetch). Don't proceed without it.
- **Why they're interested**, in their words. If it's thin ("seems cool"), ask one
  follow-up: what specifically about the company, product, team, or problem? Tell them
  they can be completely honest here: `job.md` is their private notes, and you'll decide
  what reaches the employer.

The resume can be drafted before the reasons arrive. **The cover letter and the "Why
this company?" answers wait for the user's why in their own words.** Don't invent a
polished substitute from old answers. If you must hand off before they answer, leave
the letter as a marked draft with `<!-- TODO(review): waiting on your reason for this
role -->` at the top.

Then create the folder and record everything:

```bash
resumate new "Company" "Role Title" --url "https://..."
```

Fill in `job.md`:

- `posted:` in the front matter: the posting date if the page shows one, else the date
  the user first saw it, else leave it blank. Freshness matters: many recruiters review
  in arrival order and stop once they have a strong shortlist.
- *Why I'm interested*: their reasons, their words, lightly cleaned up at most.
- *Screening questions*: the knockout questions the posting or application form asks or
  is likely to ask (work authorization, sponsorship, location or relocation, degree,
  clearance, start date, salary), copied as worded when you can see them. These are
  the main automatic rejection path, so they get answered in `resumate-questions`.
- *Job description*: the full posting.

## 2. Run the steps in order

1. **`resumate-research`** writes `research.md`: the company, the ranked requirements,
   fit and honest gaps, the employer's AI and identity-verification policy, possible
   referrals, and posting freshness.
2. **`resumate-tailor`** edits the application's `resume.yaml`.
3. **`resumate-cover-letter`** writes `cover_letter.md` (only once the user's why is in
   `job.md`).
4. **`resumate-questions`** drafts `answers.md`: screening answers and short answers for
   the "Why this company?" and additional-information boxes.
5. **Supporting materials** (below).
6. **`resumate-review`** checks everything the employer will read, fixes mechanical
   problems, and lists what needs the user.

Every piece the employer reads follows `resumate-voice`.

## 3. Supporting materials

Review `supporting/` against this role and write `materials.md`: what to include and
why, what you considered and rejected, and anything worth creating. Respect
`shareable:` in sidecar notes (`ask-first`: flag it; `no`: never recommend). Fewer is
better: only recommend what clearly strengthens the application. Don't attach anything;
the user decides and runs `resumate attach`.

## 4. Build and hand off

```bash
resumate check <app>
resumate build <app>
```

Then give the user a short summary:

- Paths to the PDFs (`out/`), `answers.md`, and the source files to edit
- How old the posting is (from `posted:`), and if it's a strong match and fresh, that
  applying soon is worth it
- The 3 to 5 requirements you optimized for, and the main tailoring choices
- **Every `TODO(review)` item** they need to resolve (from `resumate check`), including
  any screening answer you couldn't confirm
- Anything from the employer's AI or identity-verification policy they should know
  before applying or interviewing, and any possible referral `research.md` found (they
  decide whether to reach out; you never contact anyone)
- Your supporting-materials recommendation in one line
- **One ask:** rewrite at least one sentence of the letter in their own words, or swap in
  a phrase they'd actually say, before submitting
- How to iterate: edit the files directly, or tell you what to change, then
  `resumate build <app> --open`. After hand edits, `resumate-review` can check again.

Leave `status: drafting`. The user submits the application and sets `ready`, `applied`,
and later statuses themselves (`resumate status <app> applied`).

## When you learn something new

If the user mentions an accomplishment or story during this process that isn't in the
master materials, offer to add it there too (see `resumate-capture`), so future
applications benefit. When the status becomes `interviewing`, use
`resumate-interview-prep`.
