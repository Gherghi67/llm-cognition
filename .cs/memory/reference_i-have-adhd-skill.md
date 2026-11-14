---
name: i-have-adhd-skill
description: "When the user says \"that ADHD skill\" they mean i-have-adhd (skills.sh/ayghri/i-have-adhd); it is not installed locally"
metadata:
  node_type: memory
  type: reference
  originSessionId: fe2f520e-f50d-4f4b-8ca5-f1e419636f70
  modified: 2026-11-13T15:19:02.819Z
---

"That ADHD skill" = **i-have-adhd** by ayghri: https://www.skills.sh/ayghri/i-have-adhd/i-have-adhd, GitHub https://github.com/ayghri/i-have-adhd, file https://github.com/ayghri/i-have-adhd/blob/main/skills/i-have-adhd/SKILL.md (MIT). It is not in `~/.claude/skills` or the installed plugins. Read it with `gh api repos/ayghri/i-have-adhd/contents/skills/i-have-adhd/SKILL.md --jq .content | base64 -d`.

It shapes output, not content:
- next action first;
- numbered steps, each one bounded action;
- specific time estimates;
- lists of five or fewer, grouped and ranked;
- completed work made visible;
- no preamble, recap or closing pleasantries.

Once invoked it stays on for the session until "stop adhd mode" or "normal mode".

First used 13 Nov 2026 to make an ADHD-shaped copy of the project report (see [[narrative.bogdan-gherghina-erepubliklabs-com]], [[teams-via-chrome-mine]]).
