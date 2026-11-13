---
name: resumate-review
description: Final check of one resumate application before the user submits it. Use as the last step of resumate-apply, after the user edits an application's files by hand, or when the user asks whether an application is ready. Checks that every claim traces to the master resume, stories, or conversation, runs the skim test and word count, scans for banned phrases and dashes, compares against the user's other letters and answers for repeats, confirms eligibility facts agree across resume, letter, and answers, and gets resumate check clean apart from review notes. Reports findings; fixes only mechanical problems.
---

# Review an application

You are the last reader before the user. Check the files the employer will see:
`resume.yaml`, `cover_letter.md`, and `answers.md`. Fix only **mechanical** problems
yourself (a stray en or em dash, a banned word with an obvious plain swap, a parse
warning, a typo, a broken page limit). Everything that changes meaning goes back to the
user as a finding. If the user edited a file by hand, their wording wins: flag, don't
revert.

## Checks

1. **Every claim traces.** Each accomplishment, metric, tool, title, and date in the
   resume, letter, and answers comes from `master/resume.yaml`, `stories/`, or something
   the user said. Untraceable claims get `TODO(review)` or are removed.
2. **Eligibility facts agree** across resume, letter, and `answers.md`: degree and
   graduation date, location and relocation, work authorization and sponsorship,
   clearance (held versus willing to obtain), start date. Nothing implies something false
   by omission.
3. **Skim test.** Read only the first sentence of each letter paragraph. Together they
   should answer *who is this, why us, why them, what next*.
4. **Word count.** The letter body is 250 to 350 words; free-text answers fit their
   stated limits.
5. **Voice.** Scan for `resumate-voice`'s banned phrases, AI-associated words, and house
   formulas, and for en or em dashes anywhere. Read the letter aloud for anything the
   user wouldn't say.
6. **Repeats.** Compare the letter's opening, closing, and main story, and the "Why this
   company?" answer, with the user's other `applications/*/cover_letter.md` and
   `answers.md`. Flag reused sentences and near-identical shapes.
7. **Resume shape.** Must-have skills from `research.md` appear in bullets or the
   summary where the user really has them; the summary opens with a relevant
   accomplishment, not a stock opener; bullet lengths vary; no dates in the summary.
8. **The user's why.** The letter and "Why this company?" answer use the user's own
   reason from `job.md`. If it's missing, the letter is still a draft; say so.
9. **`resumate check <app>`** is clean apart from review notes: no errors, no parse
   warnings (see "Parser-safe content" in the `resumate` skill), within the page limit.

## Report

List findings grouped as *fixed* (mechanical, what you changed) and *needs you* (each
with the file and line), then every open `TODO(review)` from `resumate check`. Don't
change `status`.
