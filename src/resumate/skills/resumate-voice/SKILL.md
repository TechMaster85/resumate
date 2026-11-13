---
name: resumate-voice
description: Shared writing rules for anything an employer reads in resumate, including cover letters, resume summaries and bullets, and application-form answers. Use whenever drafting or editing that text, alongside resumate-cover-letter, resumate-tailor, or resumate-questions, or when the user asks to make something sound more like them or less generated. Covers writing in the user's voice, concrete detail, sentence variety, banned stock phrases and AI tells, and no en or em dashes. Writing style only; it doesn't decide what content goes in.
---

# Write like the user

Recruiters don't object to AI help as such. Surveys and interviews from 2025 and 2026
agree that they object to generic writing: text that could have been sent by anyone,
polished but vague, in the same shape as every other application. Their common tells
are an unnatural or overly smooth tone, repeated generic phrasing, vague or inflated
claims, buzzwords, perfect grammar with no variation, and formatting habits such as em
dashes. The fix is the user's own words and specific detail, not a detector score.

## Sound like the user

- **Write like the user talks.** Read their reasons in this and other applications'
  `job.md` files and the *Why it matters to me* sections in `stories/` to pick up how
  they say things: word choice, sentence length, how formal they are. Reuse their tone,
  and their exact phrasing for *this* job's reasons. Don't recycle a memorable line
  from another application; the same sentence in every letter becomes its own tell.
- Put their spoken phrasing on the page with almost no cleanup. Don't "elevate" plain
  words. Contractions are fine.
- **Concrete beats impressive:** a system name, a number, what broke and how they fixed
  it. "Cut processing time by two days by moving requests into one shared queue" beats
  "improved departmental efficiency through strategic process improvements."
- **Vary sentence length.** Let some sentences be short and a little uneven. Don't
  start most sentences with "I".
- Keep the register consistent with how the user will sound in an interview. An
  eloquent letter followed by a plain-spoken call is a mismatch recruiters notice.

## Avoid

- **Stock phrases:** "I am writing to apply/express my interest", "I am thrilled /
  excited to apply", "passionate about", "leverage", "results-driven",
  "detail-oriented", "team player", "fast-paced environment", "proven track record",
  "proven ability to", "I believe I would be a great fit", "unique blend of skills",
  "make an impact", "the opportunity to contribute", "I am confident in my ability to
  contribute", "thank you for considering my application".
- **Words now strongly associated with generated text:** foster, streamline, seamless,
  spearheaded, honed, delve, robust, comprehensive, adept, cultivate, meticulous,
  showcase, orchestrated, dynamic, innovative, synergy, cross-functional (unless the
  posting uses it and the user's work fits), "accelerated time-to-market", "exceeding
  stakeholder expectations".
- **House formulas that creep in across letters:** "I'd bring that same...", "I'd
  welcome a conversation" in every closing, "I'm applying for the [role]" as the first
  words of every letter. Any opening or closing used in the user's other letters.
- **Generated-text structure:** triplets of adjectives, "not only... but also",
  rhetorical questions, paragraphs opening with "Furthermore", "Additionally", or
  "Moreover", bolded themes in a list of "key strengths", every bullet or paragraph the
  same length, and a final sentence that just restates the letter.
- **No en or em dashes**, anywhere. Use a comma, colon, period, parentheses, or a plain
  hyphen. They're both a parse risk (see "Parser-safe content" in the `resumate` skill)
  and one of the most recognized AI tells.
- Claims about the company you couldn't cite, and anything not in the master resume,
  stories, or conversation.

## Don't

- Don't run AI-detector tools or chase a detector score; they're unreliable and flag
  edited human writing too. The test is: read it aloud. Would the user say this?
- Don't add a disclaimer that AI helped. If an employer asks directly, the user answers
  honestly; that's their call.
