---
name: resumate-apply
description: Tailor a resume and cover letter for a specific job using resumate. Use when the user shares a job description or posting link, says why they're interested in a role, or asks for help applying to a job. Researches the company, tailors resume.yaml from the master resume, drafts a cover letter from the user's stories, recommends supporting materials, builds PDFs, and hands everything back for review.
---

# Tailor an application

Goal: get past the resume filter honestly, so a person sets up an interview. Make the
real match visible in the posting's own words, and make the letter sound like the user.
You prepare drafts; **the user reviews, edits, and submits.**

Everything you write for the employer serves that goal.

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
never imply something false by omission that a background check would contradict.
Read the `resumate` skill first if you haven't, for file formats and commands.

## 0. Make sure the master resume is real

If `master/resume.yaml` still has the `# resumate:example` marker, stop: tailoring the
sample would be meaningless. Ask the user for their current resume and run the
`resumate-capture` first-time setup, then come back here.

## 1. Intake

You need two things from the user. Ask for whatever is missing, and don't proceed
without the first:

- **Why they're interested**, in their words. If it's thin ("seems cool"), ask one
  follow-up: what specifically about the company, product, team, or problem? Tell them
  they can be completely honest here: `job.md` is their private notes, and you'll decide
  what reaches the employer.
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

Edit the application's `resume.yaml` (already a copy of the master). The master is a
warehouse and is allowed to run long. This copy is what has to fit on the page:

- **Select**: comment out (`#`) bullets, entries, skills, and certificates that don't
  serve this role. Keep the master's order of sections unless there's a clear reason to
  change it.
- **Order**: within each entry, move the most relevant bullets to the top.
- **Reframe**: reword bullets to foreground what this role cares about, and mirror the
  posting's terminology where it's *accurate* (ATS keyword matching is literal: if they
  say "Kubernetes" and the user did Kubernetes work, say "Kubernetes").
- **Headline and summary**: adjust to speak to this role. Keep dates (graduation month,
  years) out of the summary: Workday's autofill read a dated summary as a job.
- **Parser-safe structure**: follow "Parser-safe content" in the `resumate` skill. Plain
  org names (details go in bullets), a City, ST location on every job, `degree` and
  `major` for education, phone without +1, and no en or em dashes anywhere, in the
  resume or the letter. Fix every parse warning `resumate check` prints before handing off.
- **Never** add an accomplishment, metric, tool, or title that isn't in the master, the
  stories, or the conversation. If a reframe stretches the original, or you think a
  real metric exists but you don't know it, leave `# TODO(review): ...`.

Then:

```bash
resumate check <app>     # fix errors; get to the page limit
resumate diff <app>      # sanity-check that every change is defensible
```

## 4. Draft the cover letter

Edit `cover_letter.md`. Write for a recruiter who will skim it in under a minute, likely
right after the resume. It should read like a confident person wrote it to one
company, not like a template.

**Shape**: 250–350 words, one page, three to five short paragraphs of at most four
sentences each. No headings. **One point per paragraph**: never combine two jobs or two
requirements in one paragraph, or the reader can't follow the argument. Every
paragraph's first sentence should carry its point, because that's often all that gets
read.

**Structure (ACT: Align, Connect, Tailor):**

1. **Align: who you are and why this job.** In the first two sentences, say who the
   user is in one clause (current role, or degree and school) and the specific reason
   they want *this* role at *this* company. Use their own words from `job.md` (filtered
   as in *Candor is input, not copy* above), plus at most one fact from `research.md`
   that a recruiter could verify. Name the role.
2. **Connect: why you're a great fit.** Pick the two or three requirements ranked
   highest in `research.md` (*What they're really looking for*) and give each its own
   paragraph. Open with the employer's need in their terms, then the user's evidence
   from one job, project, or story: what they did and what happened, with a number if
   there is one ("Your help desk needs someone who can resolve tickets on their own,
   and that's what I do now. As a ..."). The argument the reader should come away with:
   *given what this person has done, they'll do this job well.* One strong story, told
   briefly, beats a list of every qualification. Don't repeat the resume line by line;
   add the context a bullet can't.
3. **Close: interest and confidence.** Say plainly what they'd bring or take on in the
   role, why they expect to do well (tie it to evidence already given), and invite a
   conversation. Confident, not pleading: no "I hope", "I would be honored", or "thank
   you for considering my application".

**Tailor throughout**: mirror the company's language for its work and the posting's
words for the job. The letter should fail if sent to a different company.

**Gaps**: don't volunteer them. Show the closest real evidence plus intent ("I've built
REST APIs in Flask and want to do the same in GraphQL") rather than "I haven't used X."
Never a sentence of caveats, let alone a paragraph. Candid gap analysis goes in
`research.md` for interview prep.

**Sound human, not generated:**

- Write like the user talks. Reuse phrasing from `job.md` and `stories/`. Contractions
  are fine.
- Concrete beats impressive: a system name, a number, what broke and how they fixed it.
- Vary sentence length. Don't start most sentences with "I".
- Avoid stock phrases: "I am writing to apply/express my interest", "I am thrilled /
  excited to apply", "passionate about", "leverage", "results-driven",
  "detail-oriented", "team player", "fast-paced environment", "proven track record",
  "I believe I would be a great fit", "unique blend of skills", "make an impact".
- Avoid generated-text tells: triplets of adjectives, "not only… but also", rhetorical
  questions, em-dash asides in every paragraph, and a final sentence that just
  restates the letter.
- No claims about the company you couldn't cite.

Set `recipient` only if research found a named person confidently; otherwise leave it
unset and open with "Dear Hiring Team,". Sign off with "Sincerely," and the user's name
from the resume.

**Before handing off**, run the skim test: read only the first sentence of each
paragraph. Together they should answer *who is this, why us, why them, what next*.
Then read the whole thing aloud for anything the user wouldn't say. Check every claim
traces to the master resume, stories, or the conversation, and that the body is
250–350 words.

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
