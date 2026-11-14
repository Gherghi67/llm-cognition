---
name: bash-grep-is-ugrep
description: "In Claude Code's Bash here, grep is a shell function running ugrep; context patterns like .\\{0,120\\}word fail with 'exceeds complexity limits'"
metadata:
  node_type: memory
  type: project
  originSessionId: 33af6982-c57e-476e-a95f-8e5a1bd20f7a
  modified: 2026-11-12T19:07:26.250Z
---

In this environment's Claude Code Bash tool, `grep` is not GNU or BSD grep. It's a shell function from Claude Code's shell snapshot that runs **ugrep 7.8.4**. Patterns that wrap a match in bounded-repetition context, such as `grep -o '.\{0,120\}word.\{0,90\}'`, fail with `ugrep: error ... exceeds complexity limits`. Plain matches and `-c` counts work.

To show a few characters of context around each match, use Python, which worked: `python3 -I -c "import re; t=open(f).read(); [print(t[m.start()-90:m.end()+70]) for m in re.finditer(r'word', t, re.I)]"`. Line-level `grep -n` piped to `cut -c` also works.

Measured on Claude Code 2.1.322, 2026-11-12.
