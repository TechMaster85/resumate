# Supporting materials

Drop anything here that could strengthen an application: portfolio PDFs, writing
samples, design docs you're allowed to share, transcripts, certificates, talk slides,
recommendation letters.

For each item, agents look for a sidecar note with the same name plus `.md`
(e.g. `writing-sample.pdf` + `writing-sample.pdf.md`) describing what it is, what it
shows, and any limits on sharing it:

```markdown
---
title: Design doc — streaming migration (sanitized)
shows: [system-design, technical-writing]
shareable: yes          # yes | ask-first | no
---
Public-safe version of the doc I wrote at Lakeshore. Good for platform/infra roles.
```

When tailoring an application, the agent reviews this folder and writes its
recommendation to `materials.md` in the application folder. Nothing here is ever
included automatically: copy what you decide to submit with
`resumate attach <application> <file>`.
