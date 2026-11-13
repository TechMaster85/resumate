---
name: resumate-questions
description: Draft answers.md for one resumate application, the answers to the application form's own questions. Use during resumate-apply after the cover letter, or when the user is filling out an application form and asks how to answer screening or knockout questions (work authorization, sponsorship, relocation, degree, clearance, start date, salary) or free-text boxes like "Why this company?" or "Additional information". Prepares answers only from facts the user confirmed and marks unknowns for review. Not for the cover letter (resumate-cover-letter) or interview questions (resumate-interview-prep).
---

# Draft application answers

Two kinds of questions decide a lot before a person reads anything else:

- **Screening (knockout) questions** are the one well-documented automatic rejection
  path in applicant tracking systems. A wrong click on sponsorship or a required
  license can't be fixed by a good letter.
- **Free-text boxes** ("Why do you want to work here?", "Anything else we should
  know?") are often what a recruiter reads first, and many application sites never show
  the cover letter at all.

Write both into the application's `answers.md`. The user copies them into the form
themselves; you never fill in or submit a form.

## Screening answers

Start from *Screening questions* in `job.md`, the posting's stated requirements, and
`research.md`'s must-haves. For each likely question, write the question as worded (or
the likely wording) and the answer.

Answer **only from facts the user confirmed**, in this conversation or in earlier
applications' `answers.md` they reviewed: work authorization, need for sponsorship now
or later, current location and willingness to relocate (where), degree and graduation
date, clearance held versus willing and able to obtain, earliest start date, and on-site
or remote preference. Salary only if the user gave a number or range.

**Never guess an eligibility fact.** If you don't know, write
`<!-- TODO(review): ... -->` with the exact question to ask the user. Watch for questions
that sound alike but aren't: "Do you hold a clearance?" versus "Are you able to obtain
one?"; "Are you authorized to work?" versus "Will you now or in the future require
sponsorship?". Answers must agree with the resume and the letter.

## Free-text answers

Draft short answers for the boxes this application has or likely has:

- **Why this company / this role**: the user's own reason from `job.md`, plus one
  specific, citable fact from `research.md`. Roughly 50 to 150 words, or within the
  posted character limit. Not a paste of the letter: the same reason, said more briefly.
- **Additional information**: the one useful thing the resume doesn't carry, such as a
  relocation plan, availability, or the letter's story in two sentences. Leave it out if
  there's nothing worth adding.
- Any other prompt shown on the form, answered the same way.

If the user hasn't given their why yet, leave the box as a `TODO(review)` rather than
writing a generic reason.

Every answer follows `resumate-voice`: their words, concrete, no stock phrases, no en or
em dashes. Never add a fact that isn't in the master, the stories, or the conversation.

## Format

```markdown
# Application answers: Role at Company

## Screening
**Are you legally authorized to work in the United States?** Yes
**Will you now or in the future require sponsorship?** <!-- TODO(review): confirm -->

## Why this company? (limit: 1000 characters)
...

## Additional information
...
```
