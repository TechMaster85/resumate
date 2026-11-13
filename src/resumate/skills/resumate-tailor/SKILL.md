---
name: resumate-tailor
description: Tailor one application's resume.yaml in resumate from the master resume for a specific job. Use during resumate-apply after research, or when the user asks to retailor, shorten, refocus, or fit a specific application's resume to the page. Selects, orders, and reframes real master content in the posting's accurate terms, puts each must-have skill in a bullet where it was used, opens the summary with the most relevant accomplishment, and checks the diff. Edits only the application's resume.yaml; to add new facts to the master use resumate-capture.
---

# Tailor the resume

Edit the application's `resume.yaml` (already a copy of the master). The master is a
warehouse and is allowed to run long. This copy is what has to fit on the page and
survive two readers: an AI ranker or keyword search, then a recruiter skimming for
seconds. Read `research.md` first; its ranked *What they're really looking for* list
decides what goes up front. Read the `resumate` skill for the format, "Parser-safe
content", and "Fitting on the page".

## Select, order, reframe

- **Select**: comment out (`#`) bullets, entries, skills, and certificates that don't
  serve this role. Keep the master's order of sections unless there's a clear reason to
  change it. Prefer commenting out to deleting, so `resumate diff` stays readable.
- **Order**: within each entry, move the most relevant bullets to the top.
- **Reframe**: reword bullets to foreground what this role cares about, and mirror the
  posting's terminology where it's *accurate* (keyword matching is literal: if they say
  "Kubernetes" and the user did Kubernetes work, say "Kubernetes"). Never stuff keywords,
  never add hidden text, and never list a tool the user can't discuss in a screen.

## Put must-haves where the work happened

For each requirement in `research.md` that the user really meets, make sure it appears
in a sentence: a bullet where they used it, or the summary. The skills list is an honest
index, not the only place a word occurs. AI rankers now grade each qualification
against the parsed resume and point to the experience, summary, and skills that support
it (for example Workday HiredScore's Fit and Gap view); a skill shown in context is
easier for that grader and for a recruiter to find. If the user doesn't have it, leave
it out: no reframe makes a missing skill real.

## Headline and summary

Adjust both to speak to this role. **Open the summary with the user's most relevant real
accomplishment for this job**, not a stock opener like "Recent graduate who..." or
"Results-driven engineer with...". Keep their level and school visible later in the
summary if they matter. Keep dates (graduation month, years) out of the summary
(see "Parser-safe content"). Summaries follow `resumate-voice`.

## Make it read like a person

- **Vary bullet length on purpose.** Some bullets one line, some two. Near-identical
  bullet lengths, and every bullet opening with the same kind of power verb, are now a
  common sign of generated text.
- Don't polish away specifics: a system name and a number beat "improved efficiency."
- No en or em dashes; follow every other rule in "Parser-safe content".

## Never add facts

**Never** add an accomplishment, metric, tool, or title that isn't in the master, the
stories, or the conversation. If a reframe stretches the original, or you think a real
metric exists but you don't know it, leave `# TODO(review): ...`. Don't change the
user's real job titles to match the posting.

## Check

```bash
resumate check <app>     # fix errors and parse warnings; get to the page limit
resumate diff <app>      # sanity-check that every change is defensible
```

If it runs long, follow "Fitting on the page" in the `resumate` skill.
