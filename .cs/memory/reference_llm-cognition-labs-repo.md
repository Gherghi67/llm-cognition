---
name: llm-cognition-labs-repo
description: "Where the LLMs and Cognition lab notebooks live (github.com/bucuram/llms-and-cognition-labs), how assignments are submitted, and the stale deadline text"
metadata:
  node_type: memory
  type: reference
  originSessionId: 40882191-73cc-4b09-bd61-fdf5a007161a
  modified: 2026-11-14T18:14:14.000Z
---

The LLMs and Cognition 2026 lab notebooks are in the public repo https://github.com/bucuram/llms-and-cognition-labs. It has lab0–lab6.ipynb, helper_functions.py, previous_labs.py and pytorch-tutorial.ipynb. Fetch a file with `gh api repos/bucuram/llms-and-cognition-labs/contents/<file> -H "Accept: application/vnd.github.raw"`.

Each lab ends with an "Assignment" section that is submitted through a Google Form (lab2: https://forms.gle/qyM6u9RAQjm7pfeEA). The form returns HTTP 401 to WebFetch because it needs a Google sign-in, so its fields can't be read that way. Measured on Claude Code 2.1.325, 2026-11-14.

lab2's deadline line reads "November 14th, 2025", which is text from the course's 2025 run. Take the real 2026 dates from Teams, not from the notebooks.
