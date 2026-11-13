---
name: resumate-interview-prep
description: Build an interview prep guide for one resumate application. Use when an application's status is interviewing, or when the user says they got an interview, phone screen, or onsite for a role they applied to through resumate. Turns research.md (including the gaps saved for interview prep), the tailored resume, the cover letter, answers.md, and job.md into interview-prep.md with likely questions, the user's real stories mapped to them, honest gap answers, questions to ask, and logistics. Not for application-form questions (resumate-questions).
---

# Prepare for an interview

The application got the user in the room. Now they need to sound like the person on the
page, with true stories ready. Write `interview-prep.md` in the application folder. It's
private notes for the user, not something the employer sees.

## Read first

`job.md` (the posting, their reasons, their screening answers), `research.md`
(especially *Fit*, the gaps, the candid notes saved for interview prep, and *Employer
policies*), the tailored `resume.yaml`, `cover_letter.md`, `answers.md`, and every story
in `stories/`. Ask the user what they know about the interview: the stage, the format
(phone, video, technical, panel, onsite), who they'll meet, and how long it is. Refresh
the company research if there's recent news.

## Write interview-prep.md

1. **What they'll probe.** The top requirements from `research.md`, and everything the
   resume and letter claimed: the user should be able to talk about any line for two
   minutes.
2. **Likely questions.** Behavioral questions tied to the role's requirements, technical
   or role-specific topics the posting names, and the usual openers ("Tell me about
   yourself", "Why us?", "Why this role?"). For "Tell me about yourself", a short outline
   in the user's words, consistent with the letter.
3. **Stories mapped to questions.** For each likely question, the user's best real story
   from `stories/` or the master resume, as Situation, Action, Result bullets the user
   can say aloud. Point out where one story covers several questions, and where there's
   no good story yet (offer to capture one with `resumate-capture`).
4. **Honest gap answers.** For each gap in `research.md`, a truthful answer: the closest
   real experience, what they're doing about it, and how they'd ramp up. Never coach the
   user to claim experience they don't have.
5. **Questions to ask them.** Three to five specific questions drawn from the research
   and the user's own reasons, not generic ones.
6. **Logistics.** Date, time and time zone, format, interviewers, what to bring, and
   anything from the employer's AI-use and identity-verification policy (for example, no
   AI tools during the interview, ID check, camera on). Unknowns are
   `<!-- TODO(review): ... -->` items.

Never invent facts, numbers, or stories; everything traces to the master, the stories,
or the conversation. Keep the user's voice: prep notes they would actually say beat
polished scripts. Don't change `status`; the user sets it.
