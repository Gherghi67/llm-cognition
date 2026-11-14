# Session Summary: llm-cognition@lab2

**Date:** 2026-11-14
**Duration:** about 2h45m, 17:30–20:15 EET, in one conversation in the `cs/lab2` feature worktree of `llm-cognition`

## Objective

Get lab2 ("Coding Attention Mechanisms") from the course labs repo github.com/bucuram/llms-and-cognition-labs, understand the theory behind it, and solve its assignment for the LLMs and Cognition 2026 course (University of Bucharest master's).

The base session `llm-cognition` (2026-11-02) had earlier connected Claude to the user's university Teams through `chrome-mine` and published the course brief. That's where the course context (classes, Bogdan's 12 Nov presentation, the 14 Nov project deadline) comes from.

## Environment

macOS, Claude Code 2.1.325, a cs feature worktree on branch `cs/lab2`. Homebrew `python3` is 3.15.2, and torch has no wheels for it, so the labs run in a uv-made Python 3.12 venv at `.venv/` (gitignored) with torch 2.15, transformers 5.23, bertviz 1.4.1, matplotlib and nbconvert.

## Key Discoveries

- **lab2 is self-contained.** It's chapter 3 of Raschka's *LLMs from scratch*: simplified self-attention, then trainable Q/K/V, a causal mask with dropout, and multi-head attention. It imports only torch and needs none of the repo's helper files.
- **The notebook's deadline text is stale.** It says "November 14th, 2025", copied from the 2025 run of the course. The real 2026 date has to come from Teams.
- **The submission form can't be read from here.** The Google Form (forms.gle/qyM6u9RAQjm7pfeEA) returns 401 to WebFetch because it needs a Google sign-in, so its required fields are still unknown. chrome-mine, the user's signed-in Chrome, was never tried for it; that's filed as a follow-up task.
- **Part 1 answer.** A GPT-2-small-sized `MultiHeadAttention(768, 768, 1024, 0.0, 12)` has 2,360,064 parameters: query/key/value 3 × 589,824 plus out_proj 590,592. The causal mask is a buffer, not a parameter. With `qkv_bias=True`, as in the real GPT-2, it's 2,362,368.
- **Part 2: what BERT attends to across the two sentences** (`bert-base-uncased`; A = "The old fisherman dragged his boat onto the beach because a storm was coming.", B = "He tied it to a wooden post and hurried home before the rain started."; layers and heads counted from 0):
  - boat→it 0.61 (layer 10, head 2)
  - storm→rain 0.67 (layer 10, head 10), where "a / was / coming" also point to "rain" (0.71–0.88)
  - his→he 0.51 (layer 10, head 10)
  - layer 5, head 5 behaves like a pronoun head: the/old/fisherman→he 0.22–0.31 and boat→it 0.30
  - coming→started 0.27 (layer 11, head 8)
  - in the reverse direction, it→boat reaches 0.78 (layer 9, head 1)
  - averaged over all 144 heads, A words send only 8% of their attention to B, 34% to their own sentence and 58% to [CLS]/[SEP]/punctuation. Cross-sentence links sit in a few specific heads, mostly in the late layers.
- **BertViz makes notebooks huge.** It writes every attention weight into the notebook as text, so a sentence pair made the notebook 28 MB and its HTML 14 MB. Rounding the weights to 3 decimals in float64 just for the views cut them to 8.5 MB and 4.2 MB, and the view still renders (checked with headless Chrome).
- **Theory covered on the way** (the user asked for "ELI18" explanations tied to lab2's own numbers): hidden states; self-attention; the weighted-sum formula z⁽ⁱ⁾ = Σⱼ αᵢⱼ v⁽ʲ⁾; how attention weights are computed (dot product, then softmax instead of dividing by the sum, then scaling by √d_k).

## Changes Made

- **`labs/lab2.ipynb`:**
  - added the Part 1 solution cell and its answer cell, plus a short Part 2 answer under the Question cell
  - re-ran the whole notebook so the new cells have outputs
- **`labs/lab2_bertviz.ipynb`:** a new notebook for Part 2, with:
  - head view and model view
  - a table ranking A→B word pairs and their strongest heads
  - pronoun checks in the other direction
  - the share of attention going to each destination
  - a 2×2 heatmap of four heads
  - the written answer
- **Comments removed:** at the user's request, from all solution code (instructor comments in lab2's original cells kept).
- **`.gitignore`:** added `.venv/`.
- **Memory:**
  - `reference_llm-cognition-labs-repo.md`: repo location, the form that needs sign-in, the stale deadlines
  - `feedback_lab-code-no-comments.md`: no comments in lab solution code
- **Task #1 filed:** widen the chrome-mine memory pointer to cover course pages behind a sign-in.

Nothing was committed.

## Key Files & Outputs

All of these are untracked, uncommitted work; git has no commit from this session.

- `labs/lab2.ipynb`: the lab with the Part 1 solution
- `labs/lab2_bertviz.ipynb`: Part 2 (8.5 MB)
- `labs/lab2.zip`: the two notebooks with their outputs, ready to submit (1.4 MB)
- `labs/lab2_bertviz_heads.png`: static heatmap of four heads, in case the form wants an image
- `labs/lab2_bertviz_head_view.html`: standalone interactive head view; needs internet for its JavaScript libraries
- `.venv/`: the Python 3.12 lab environment (gitignored)

## Outcome

Both parts of the lab2 assignment are solved, have been run, and are packed in `labs/lab2.zip`. Not yet done:
- submitting it (the form needs the user's Google sign-in)
- checking the real 2026 deadline on Teams
- deciding whether to keep the chosen sentences: changing them means re-running the notebook and updating the hand-typed numbers in the answer text

The worktree is ready for `/finish lab2` from the base session once the user decides what to commit.

## Notes for Future Reference

- Later labs (lab3–lab6) come from the same repo. Reuse `uv venv --python 3.12 .venv`, since the default `python3` 3.15 has no torch, and run notebooks with `.venv/bin/jupyter nbconvert --to notebook --execute --inplace`.
- Write lab solution code without comments, and put explanations in markdown cells.
- Don't take deadlines from the notebooks; check Teams.
- To read the sign-in-gated Google Form, try chrome-mine in the user's own Chrome (Task #1). The plugin `chrome-devtools` browser was locked by another session's profile; headless Chrome with a scratch `--user-data-dir` worked for local rendering checks.
- NotebookEdit couldn't be used on these notebooks: the Read tool refuses notebooks over 25k tokens, and NotebookEdit requires a Read first. Edits went through `nbformat` scripts instead.
