# Changes

## Unreleased: one skill per job

The three agent skills are now eleven, each doing one thing, with descriptions that say
when to use it and which sibling to use instead. Every existing rule was kept and moved
to the skill that owns it. The resume and cover letter formats are unchanged.

### Skills
- `resumate` (reference) is the single home for "Parser-safe content" and now lists every
  skill. Other skills point to it instead of restating the rules.
- `resumate-apply` is a coordinator: intake, then research, tailor, cover letter,
  questions, supporting materials, review, build, and handoff.
- Split out of `resumate-apply`: `resumate-research`, `resumate-tailor`,
  `resumate-cover-letter`, and `resumate-voice` (the writing rules, now shared by
  letters, summaries, and form answers).
- Split out of `resumate-capture`: `resumate-setup` (first-time import).
- New: `resumate-questions` (`answers.md`), `resumate-review` (final check, also after
  hand edits), and `resumate-interview-prep` (`interview-prep.md` once interviewing).

### New guidance (research-backed, not tested in Workday)
From a review of 2025 and 2026 recruiter surveys, ATS vendor documentation, and hiring
data. These are writing and process guidance, not parse results like the Workday tests
below.
- Quality over volume: a few strong applications, never mass-apply; the user sets
  their own number. Focused applicants outperform high-volume ones (Huntr / Wellfound,
  The Conversation, 2025-2026).
- The letter and "Why this company?" answers wait for the user's own reason; the resume
  can be drafted first.
- Screening (knockout) questions are recorded in `job.md` and answered in `answers.md`
  from confirmed facts only. They are the main automatic rejection path; the "75% of
  resumes auto-rejected" figure has no source (Enhancv recruiter interviews, Lever and
  Taleo docs, The Conversation).
- Free-text form answers are a deliverable, since many application sites never show the
  letter to the first reader (Wellfound).
- Research records posting freshness, the employer's AI-use and identity-verification
  policy, and possible referrals by name only, never contacting anyone (Ashby referral
  data, Greenhouse Real Talent, employer policies).
- Tailoring puts each real must-have skill in a bullet or the summary where it was used,
  since AI rankers grade each qualification against the parsed resume (Workday HiredScore
  Fit and Gap, Aug 2026). The summary opens with the most relevant accomplishment.
  Bullet lengths vary on purpose (uniform bullets are a measured AI tell, Careerminds
  2026).
- Letters tell one story with a detail the resume can't show, and don't reuse the
  user's other letters' openings, closings, or main story.
- More banned words and house formulas (foster, streamline, seamless, spearheaded, honed,
  delve, robust, "I'd bring that same", ...). Recruiters object to generic writing, not
  AI use as such; no AI-detector scores.
- Handoff reports the posting's age and asks the user to rewrite at least one sentence
  in their own words before submitting.
- Optional, only on request: README suggestions for linked public repos and a LinkedIn
  consistency check against the master.

### Other changes
- `resumate new` adds an `answers.md` template; `job.md` gains `posted:` and a
  *Screening questions* section; `research.md` gains *Posting*, *Employer policies*, and
  *Possible referrals*.
- `resumate check <app>` lists review markers in `answers.md` as well as `materials.md`.
- Workspace `AGENTS.md`, README, and `CLAUDE.md` describe the new skills.

## Unreleased: Workday-friendly resume structure

Based on three real Workday "autofill with resume" tests (one Workday tenant, Nov 2026).
Each change is marked **[tested]** when those tests back it directly, or **[guess]** when
it is ATS best practice that hasn't been re-tested in Workday.

### Rendering
- **[tested]** `modern` is now the default layout, and new workspaces get it in
  `resumate.yaml`. Workday parsed its `Title | dates` / `Org | Location` heading perfectly.
- **[tested]** New `style.entry_heading`: `stacked` (default, the shape above) or `one_line`
  (`Title | Org | Location | dates`). Classic now stacks too by default. The old classic
  heading, `Title – Org, Location | dates`, parsed nothing in Workday (that run also hit a
  transient Workday error, so it's suggestive rather than conclusive). `one_line` is
  **[guess]**: it uses pipes instead of dashes and commas, but is untested.
- **[tested]** The summary gets a heading (`Summary` by default, `summary_title` to change,
  `""` to remove). A summary with a date and no heading became a fake job in Workday.
  Whether the heading alone prevents that is **[guess]**, so `check` also warns about dates.
- **[guess]** Education entries take `degree`, `major`, and `minor`. The school stays in
  `title`, the degree prints on the org line, and the field prints as `Major: ...`.
  (Tested problem: "Bachelor of Science in Engineering in Computer Science" was read as
  field "Engineering Physics". The labeled line is the untested fix.)
- **[guess]** No en or em dashes from resumate itself: PDF titles (`Name Resume`,
  `Name Cover Letter | Role | Company`), certificate detail lines (`Issuer | Credential ID
  ... | url`), and the old classic heading all use pipes or spaces now.

### `resumate check` warnings (all warnings, never errors)
- **[tested]** Commas or parentheses in an `org` (split one job into two).
- **[tested]** An entry with an org but no `location` (company lost, entry split).
- **[tested]** A `Remote` location with no City, ST (company and bullets dropped). The
  suggested fix, a City, ST plus "remote" in a bullet, is **[guess]**.
- **[tested]** A date in the summary, or a summary with its heading turned off.
- **[tested]** A phone starting with `+1` (Workday's phone field rejected it).
- **[guess]** A degree written in `title`/`org` instead of `degree`/`major`, or a `degree`
  without a `major`.
- **[guess]** En or em dashes anywhere in rendered resume or cover-letter text. YAML `#`
  comments and Markdown `<!-- -->` comments are ignored.

### Docs and agent skills
- `resumate` skill: new "Parser-safe content" section, education fields, `entry_heading`.
- `resumate-apply` and `resumate-capture` skills, workspace `AGENTS.md`, README, and
  `CLAUDE.md` tell agents to follow those rules and clear `check`'s parse warnings.
- Sample master resume uses the new education fields, a City, ST for its remote job, and
  no en or em dashes.

### Compatibility
- Existing YAML still loads and renders unchanged in content. Visible differences: a
  `SUMMARY` heading above the summary, a classic layout that now stacks entry headings
  (`style.entry_heading: one_line` for a compact single line), and modern as the default
  for workspaces whose `resumate.yaml` doesn't set `layout`.
- `org` and `degree` can't both be set on one entry.
