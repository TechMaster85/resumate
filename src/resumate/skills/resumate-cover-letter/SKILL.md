---
name: resumate-cover-letter
description: Write or rewrite the cover_letter.md for one resumate application. Use during resumate-apply after research and tailoring, or when the user asks to draft, redo, shorten, or change a cover letter for a specific job. Needs the user's own reason for wanting the job in job.md. Covers the letter's shape, ACT structure, one story per letter, gaps, recipient and sign-off, and avoiding repeats of the user's other letters. Letters only; short form-box answers are resumate-questions, the shared writing rules are resumate-voice.
---

# Write the cover letter

Edit the application's `cover_letter.md`. Write for a recruiter who will skim it in
under a minute, likely right after the resume. It should read like a confident person
wrote it to one company, not like a template. A letter only earns its place when it says
something the resume can't: why this company, and one story with texture.

## Before you write

- **The user's why must be in `job.md`**, in their words. If it isn't, ask for it. If you
  have to produce a draft first, mark it `<!-- TODO(review): waiting on your reason for
  this role -->` and don't build a polished opening from old answers.
- Read `research.md` (*What they're really looking for*, *Fit*), the tailored
  `resume.yaml`, and `stories/`.
- **Read the user's other letters** in `applications/*/cover_letter.md`. Note their
  openings, closings, main stories, and paragraph shapes. This letter must not reuse an
  opening or closing line, and should not lead with the same story unless nothing else
  fits this role. A recruiter sees dozens of letters that start the same way; the user's
  own letters shouldn't look like a set.
- Load `resumate-voice`; its rules apply to every sentence.

## Shape

250 to 350 words, one page, three to five short paragraphs of at most four sentences
each. No headings. **One point per paragraph**: never combine two jobs or two
requirements in one paragraph, or the reader can't follow the argument. Every
paragraph's first sentence should carry its point, because that's often all that gets
read. Vary the shape from letter to letter: some are three paragraphs, some open on the
story and close on the reason.

## Structure (ACT: Align, Connect, Tailor)

1. **Align: who you are and why this job.** Early on, say the specific reason the user
   wants *this* role at *this* company, in their own words from `job.md` (filtered as in
   *Candor is input, not copy* in `resumate-apply`), plus at most one fact from
   `research.md` that a recruiter could verify. Name the role, and say who the user is in
   one clause (current role, or degree and school). Lead with the reason or a moment
   rather than a biography line the reader can get from the resume.
2. **Connect: why you're a great fit.** Take the requirements ranked highest in
   `research.md` and argue from evidence. Open with the employer's need in their terms,
   then the user's evidence ("Your help desk needs someone who can resolve tickets on
   their own, and that's what I do now. As a ..."). The reader should come away with:
   *given what this person has done, they'll do this job well.*
   **One story per letter**, told briefly, with a detail the resume can't show: what
   broke, what they tried first, why they did it themselves, what they'd do differently.
   Don't retell resume bullets; if a sentence repeats a bullet's metric and verbs without
   adding context, cut it or add the context. Any other requirement gets a short
   paragraph of its own, not a second retold story.
3. **Close: interest and confidence.** Say plainly what they'd take on in the role, why
   they expect to do well (tie it to evidence already given), and invite a conversation
   in words that differ from their other letters. Confident, not pleading: no "I hope",
   "I would be honored", or "thank you for considering my application".

**Tailor throughout**: mirror the company's language for its work and the posting's
words for the job. The letter should fail if sent to a different company. No claims
about the company you couldn't cite from `research.md`.

## Gaps

Don't volunteer them. Show the closest real evidence plus intent ("I've built REST APIs
in Flask and want to do the same in GraphQL") rather than "I haven't used X." Never a
sentence of caveats, let alone a paragraph. Candid gap analysis goes in `research.md`
for interview prep. Hard eligibility facts (clearance, authorization, relocation) may go
in the letter when they help and the user confirmed them; they must match `answers.md`.

## Recipient and sign-off

Set `recipient` only if research found a named person confidently; otherwise leave it
unset and open with "Dear Hiring Team,". Sign off with "Sincerely," and the user's name
from the resume. Leave notes to the user in `<!-- comments -->`.

## Finish

Run `resumate-review` on the letter (skim test, word count, banned phrases, repeats
against other letters, every claim traced). Never add a fact that isn't in the master,
the stories, or the conversation.
