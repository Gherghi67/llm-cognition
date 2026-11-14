---
name: lab-notebook-env
description: "Course lab notebooks pin torch==2.0.1 / tiktoken==0.7.0 and need a Python 3.11 venv (system python3 is 3.15); execute them with nbconvert --allow-errors"
metadata:
  node_type: memory
  type: project
  originSessionId: 476541ec-b9b4-4a67-bf4c-82c7932e59cc
  modified: 2026-11-14T15:30:22.964Z
---

The LLMs & Cognition lab notebooks ([[llm-cognition-labs-repo]]) pin `torch==2.0.1` and `tiktoken==0.7.0` in `%pip` cells. On this Mac, Homebrew `python3` is 3.15, which torch 2.0.1 has no wheels for.

This setup works: `uv venv --python 3.11 --seed .venv`, then `uv pip install --python .venv/bin/python "torch==2.0.1" "tiktoken==0.7.0" "numpy<2" nbconvert ipykernel`. `--seed` puts pip in the venv so the notebooks' `%pip` cells pass instead of failing. `numpy<2` is there because torch 2.0.1 was built against NumPy 1.x.

To run a notebook headless: `.venv/bin/jupyter nbconvert --to notebook --execute --inplace --allow-errors <nb>`. `--allow-errors` is needed because the labs include deliberate error demos (Lab 1 cell 59 raises `KeyError: 'Hello'`), which would otherwise stop the run.

The venv is gitignored and lives in the worktree, so it disappears when that worktree is retired. Recreate it per worktree.

Measured on Claude Code 2.1.325, 2026-11-14 (uv, macOS arm64, Python 3.11, Lab 1).
