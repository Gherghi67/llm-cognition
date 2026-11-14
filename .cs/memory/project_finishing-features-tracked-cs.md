---
name: finishing-features-tracked-cs
description: "How to get /finish through in llm-cognition, whose .cs/ is tracked in git: commit both sides' notes, avoid the summary.md/README.md conflicts, and repair MEMORY.md after merging main into a worktree"
metadata:
  node_type: memory
  type: project
  originSessionId: 9e4e30f5-9eca-4f5d-bea9-fa5075f16de1
  modified: 2026-11-14T15:39:15.215Z
---

llm-cognition tracks `.cs/` in git. On 2026-11-14 `/finish lab1` hit five blocks in a row. The lab2 and lab3 worktrees, both cut at 05054b0, will hit the same ones.

- `cs <base> -integrate-feature` refuses over any uncommitted change in the base, including the `.cs/timeline.jsonl` line cs appends after each integrate. Commit that line (or the base's notes) before integrating again.
- `cs <base> -retire-feature` refuses over tracked dirt in the worktree, which includes the feature's `.cs/` files. They have to be committed and integrated; cs's fuse step only covers repos where `.cs` is ignored. `finish.sh report` still prints `retire: ready` while that dirt is there, so don't rely on it.
- The base and the feature both create `.cs/summary.md`, an add/add conflict. Store the feature's copy at `.cs/features/<task>/summary.md`, the path cs's own fuse uses.
- `.cs/README.md` has no merge rule, so it conflicts when both sides changed it. Run `git merge main` in the worktree and keep both sides.
- `.cs/memory/MEMORY.md` is `merge=ours`. Merging main into the worktree keeps the worktree's index and silently drops main's entries. Rebuild it as main's file plus the feature's new lines before committing the merge. The base-side integrate is safe because cs appends the missing pointers itself.
- Before integrating, preview the merge with `git merge-tree --write-tree --name-only main cs/<task>`.

Measured on Claude Code 2.1.325 with cs 2026.11.7, 2026-11-14. Re-check once either version changes; tasks #5–#7 propose fixing the refusals.

**Why:** each refusal or conflict cost a separate round trip during the lab1 finish.
**How to apply:** before `/finish lab2` or `/finish lab3`, commit the worktree's work and notes with the user's go-ahead, apply the summary.md and MEMORY.md steps above, and confirm the preview is clean.
