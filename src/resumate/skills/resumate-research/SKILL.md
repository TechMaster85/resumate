---
name: resumate-research
description: Research a company and role for one resumate application and write the application's research.md with cited sources. Use after resumate-apply intake (job.md has the posting), or when the user asks to research or re-research a specific employer or role they're applying to. Ranks what the employer is really looking for, maps it to the user's evidence and honest gaps, records the employer's AI-use and identity-verification policy, lists possible referrals by name only, and notes posting freshness. Writes notes only; tailoring is resumate-tailor, the letter is resumate-cover-letter.
---

# Research the company and role

`research.md` is the user's private briefing. Every later step reads it: the tailored
resume and letter argue from its ranked requirements, and interview prep reuses its
gaps. Cite a source link for every fact so the user can check it. Read the `resumate`
skill for the workspace layout.

## Read the workspace first

`job.md` (the posting, the user's reasons, any screening questions),
`master/resume.yaml`, every file in `stories/`, and `supporting/` including sidecar
`.md` notes. You can't judge fit without knowing what the user has done.

## Research

Use whatever web tools you have:

- What the company does, for whom, its stage, and recent news (launches, funding, layoffs)
- Engineering blog posts, talks, or open source from this team; the product itself
- The values and language the company uses about itself
- **Posting freshness:** the posting date if shown (the page, the careers site, or the
  board listing). Record it in `job.md`'s `posted:` if it's blank, and note whether the
  role looks newly opened or reposted.
- **AI and integrity policy:** search the careers site, the posting, and any
  candidate-facing FAQ for the employer's rules on AI use in applications, online
  assessments, and interviews, and for identity verification (government ID, a
  verification service, camera-on interviews). Quote the policy and link it. If you
  find nothing, write "No published policy found" rather than guessing. These rules are
  binding on the user; flag them clearly.
- **Possible referrals:** people who might give a warm introduction, such as alumni of
  the user's school or former colleagues (from the master resume) who work there now,
  or a named recruiter or hiring manager for the team. List each by name, role, and the
  public source where you saw them. These are suggestions only: **never contact anyone,
  and never draft outreach unless the user asks.** If you can't search for people, say so.

If you can't browse at all, say so, research from the posting alone, and note that in
`research.md`.

## Write research.md

Use the template's sections:

- **The company**, **The team and role**: what you found, cited.
- **What they're really looking for**: the most important section. The 3 to 5
  requirements that matter most, ranked, reading between the lines of the posting.
  Separate hard must-haves (likely knockout or screening criteria) from preferences.
- **Fit**: for each top requirement, the user's strongest real evidence from the master
  resume and stories, and the posting's exact term for it when the user's work matches.
  Be honest about gaps: what's missing, how close the nearest real evidence is, and
  whether it's worth addressing. Candid things the user told you that shouldn't reach
  the employer go here too, for interview prep.
- **Posting**: date posted or first seen, and how fresh it is.
- **Employer policies**: AI use and identity verification, as above.
- **Possible referrals**: names, roles, sources; or "none found".
- **Sources**: every link.

No claim about the company goes in `research.md` unless you can cite it, and nothing
else the user sends can rely on an uncited claim.
