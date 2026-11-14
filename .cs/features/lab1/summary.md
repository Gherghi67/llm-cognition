# Session Summary: llm-cognition (lab1 worktree)

**Date:** 2026-11-14
**Duration:** about 1 hour (16:31–17:30 EET), one conversation in the feature worktree `llm-cognition@lab1` (branch `cs/lab1`)

## Objective

Get Lab 1 of the University of Bucharest "LLMs and Cognition 2026" course from its GitHub repo, understand the ideas it teaches, and complete its assignment. Earlier work in the parent session (2026-11-02) connected Claude to the user's university Teams and produced a course brief. This worktree builds on that context but is about the first lab.

## Environment

- macOS (Apple silicon), Claude Code CLI, a cs feature worktree of the `llm-cognition` session.
- The `chrome-mine` MCP attached to the user's own Chrome. That is how the repo was found: `lab1.ipynb` was already open in a tab.
- `gh` is logged in as the user, so public repo files are fetched with `gh api`.
- Homebrew `python3` is 3.15.2 with no torch, tiktoken or Jupyter. `uv` is available.

## Key Discoveries

- **Course labs repo: github.com/bucuram/llms-and-cognition-labs.** It holds lab0–lab6 plus a PyTorch tutorial, closely following Raschka's *LLMs from Scratch*: tokens, attention, GPT from scratch, pretraining, then two kinds of fine-tuning. A broad `gh search repos` didn't find it. The open Chrome tab did.
- **The deadlines in the notebooks are from last year.** The repo's last commit is 2025-10-08, and Lab 1 says "Deadline: October 31th, 2025". The 2026 deadline and form link still need checking on Teams.
- **Lab 1 runs on its own.** It doesn't import `helper_functions.py` or `previous_labs.py`, and it downloads `the-verdict.txt` at runtime.
- **Environment constraint.** The notebooks pin `torch==2.0.1` and `tiktoken==0.7.0`. torch 2.0.1 has no wheels for Python 3.15, so the labs need a Python 3.11 venv. `numpy<2` is required with it, and `uv venv --seed` puts pip in the venv so the notebooks' `%pip` cells work.
- **Running a notebook headless needs `--allow-errors`.** The labs deliberately trigger errors to teach a point (cell 59's `KeyError: 'Hello'` shows why a vocabulary-only tokenizer needs `<|unk|>`).
- **Assignment results:**
  - `"Akwirw ier"` encodes to `[33901, 86, 343, 86, 220, 959]`, which is Ak | w | ir | w | " " | ier, and decodes back exactly. BPE needs no `<|unk|>`.
  - Over the story's 5,145 tokens, the data loader gives 2,572 samples with no overlap for (max_length=2, stride=2). For (8, 2) it gives 2,569 samples, neighbouring windows share 6 tokens, and each token appears in up to 4 windows.
- **Labs 2 and 3** build attention with `qkv_bias=False`, and Lab 3's output head has `bias=False`. This came up while explaining biases.

## Changes Made

- **Lab material:** copied `lab1.ipynb` unchanged from upstream commit `d04a067` into `lab1/`.
- **Assignment:** under the notebook's Assignment heading, added three code cells for Part 1 and two for Part 2, each part followed by a short markdown write-up. Then executed the whole notebook in place, so every cell has fresh outputs; the only error is the intentional one in cell 59.
- **Environment:** created `.venv` (Python 3.11; torch 2.0.1, tiktoken 0.7.0, numpy<2, nbconvert, ipykernel).
- **`.gitignore`:** added `.venv/`, `__pycache__/`, `.ipynb_checkpoints/` and `the-verdict.txt`.
- **Teaching (no files):** explained, using the notebook's own outputs, why `<|unk|>` helps and what it costs, what a tensor is, token embeddings at an "eli18" level, why a positional embedding behaves like a bias and a token embedding doesn't, and what a bias is in a neural network.

## Key Files & Outputs

No commits in this worktree. Everything is on disk, uncommitted:

- `lab1/lab1.ipynb`: Lab 1 with the completed and executed assignment. This is the file to submit.
- `lab1/the-verdict.txt`: downloaded by the notebook (gitignored).
- `.gitignore`: the Python/Jupyter entries above.
- `.cs/memory/reference_llm-cognition-labs-repo.md` and `.cs/memory/project_lab-notebook-env.md`: new durable memory entries.
- `.cs/README.md`: added the lab1 objective, environment and outcome.

## Outcome

Lab 1 was fetched, explained and completed. Both assignment parts are in the notebook with real outputs and short explanations, run with the exact versions the lab asks for. **Still open:** confirm the 2026 Lab 1 deadline and form on Teams, upload the notebook, and integrate the worktree with `/finish lab1` from the `llm-cognition` session (commit first, if the user wants the lab in git history).

## Notes for Future Reference

- For "take labN from the github", fetch `labN.ipynb` from `bucuram/llms-and-cognition-labs` with `gh api ... -H "Accept: application/vnd.github.raw"`. Check whether it imports `helper_functions.py` or `previous_labs.py`; later labs probably do.
- The `.venv` lives in this worktree and disappears when the worktree is retired. Recreate it with `uv venv --python 3.11 --seed .venv` and the pinned installs (see `project_lab-notebook-env.md`).
- On this machine `grep` is ugrep. A bounded-repetition `grep -oE` over minified notebook JSON failed with "exceeds complexity limits"; parse notebooks with Python's `json` instead.
- Assignment deadlines and forms: always confirm on the class Teams through `chrome-mine`, never from the notebook.
