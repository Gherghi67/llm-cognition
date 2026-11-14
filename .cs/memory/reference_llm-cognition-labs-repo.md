---
name: llm-cognition-labs-repo
description: "The LLMs & Cognition course labs live at github.com/bucuram/llms-and-cognition-labs (lab0–lab6); \"take labN from the github\" means this repo; assignments go through a Google Form that needs sign-in"
metadata:
  node_type: memory
  type: reference
  originSessionId: 476541ec-b9b4-4a67-bf4c-82c7932e59cc
  modified: 2026-11-14T18:14:14.000Z
---

The course's lab notebooks are in the public repo **https://github.com/bucuram/llms-and-cognition-labs**. It holds `lab0.ipynb`–`lab6.ipynb`, `pytorch-tutorial.ipynb`, `helper_functions.py` and `previous_labs.py`. The labs follow rasbt/LLMs-from-scratch: Lab 1 text and tokens, 2 attention, 3 GPT from scratch, 4 pretraining, 5 classification fine-tuning, 6 instruction fine-tuning. Claudiu Creangă teaches the labs.

When the user says "take labN from the github", they mean this repo. A broad `gh search repos` does not find it. Fetch files with `gh api repos/bucuram/llms-and-cognition-labs/contents/<file> -H "Accept: application/vnd.github.raw"`.

Each notebook ends with an `## Assignment` section that is submitted through a Google Form (lab2: https://forms.gle/qyM6u9RAQjm7pfeEA). The form returns HTTP 401 to WebFetch because it needs a Google sign-in, so its fields can't be read that way (measured on Claude Code 2.1.325, 2026-11-14). As of 2026-11-14 the repo's last commit was 2025-10-08, so the deadlines written in the notebooks are from the 2025 run (Lab 1 says 31 Oct 2025, lab2 says 14 Nov 2025). Confirm the current deadline on the class Teams before relying on one; see [[teams-via-chrome-mine]].

Lab environment constraints are in [[lab-notebook-env]].
