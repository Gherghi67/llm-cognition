# Session Summary: llm-cognition

**Date:** 2026-11-02 to 2026-11-14
**Duration:** Short conversations spread over twelve days:
- 2 Nov: Teams access
- 6–7 Nov: first commit, labs repo cloned
- 8 Nov: role prep
- 10 Nov: slides
- 12 Nov: speech, Fig. 5 check
- 13–14 Nov: project report copy, the Painters paper
- 14 Nov: Lab 1 in the `lab1` feature worktree (about an hour), then `/finish lab1`
- 14 Nov evening (about 2.5 h): the ADHD copy re-synced with the newer Word report, PDFs of the report and the copy, and a team task plan to the 03 Dec checkpoint; then this wrap

## Objective

The session started as "how can I connect Claude to MS Teams". It grew into Bogdan's coursework for the University of Bucharest course LLMs & Cognition 2026, in three strands:

1. **Paper presentation (2–12 Nov).** Bogdan was the Methodology Expert (ME) for Team 4's 12 Nov talk on arXiv 2604.12816, "The role of System 1 and System 2 semantic memory structure in human and LLM biases". Their part covered the bias-measurement method, how the results were obtained, and the conclusion.
2. **Course project (13–14 Nov).** An ADHD-friendly copy of the project's preliminary report, "Transformer Layers and Attention-Head Similarity", in Bogdan's own claude.ai account. Then explanations of the base paper, *Transformer Layers as Painters*. On the evening of 14 Nov: re-sync the copy with the team's newer Word report, produce PDFs, and plan the team's work up to the first progress report.
3. **Lab 1 (14 Nov).** Fetch Lab 1 from the course GitHub, explain its ideas, do the assignment, and land it on `main`.

## Environment

- macOS, Claude Code CLI; one commit and one wrap ran in Codex. Repo `/Users/bogdan.gherghina/Documents/llm-cognition` on `main`. Its origin is not GitHub, so there are no PRs, and nothing has been pushed.
- University material is read through the local `chrome-mine` MCP, which attaches to Bogdan's own signed-in Chrome. It covers Teams (unibuc student account), Google Docs, and claude.ai docs the docs connector can't reach.
- There are two claude.ai accounts: the erepubliklabs org account this Claude Code uses, and a personal one signed in on Chrome. Docs owned by the personal account are refused by the docs tools.
- Lab 1 ran in the cs feature worktree `llm-cognition@lab1` (branch `cs/lab1`), now retired. Sibling worktrees `llm-cognition@lab2` and `@lab3` exist, both still at `05054b0` with no work recorded.
- The labs need a Python 3.11 uv venv, because the system `python3` is 3.15 and the notebooks pin torch 2.0.1.

## Key Discoveries

**Getting at the material.**
- The M365 connector and Graph routes were dead ends: erepubliklabs isn't on Microsoft 365, and unibuc doesn't grant students admin consent. Scraping in Bogdan's own Chrome works (`reference_teams-via-chrome-mine`).
- The same route reads a claude.ai Doc the connector refuses. `take_snapshot` returns the text; `evaluate_script` only returns the title, because the body sits in nested iframes.

**The bias paper.**
- Three three-layer networks (humans, Mistral-7B, Llama-3.1-8B): free associations are System 1; definitions and categories are System 2. Bias is measured with `spreadr` spreading activation and Wilcoxon effect sizes.
- The authors' earlier LWOW repo fills the method gaps (r = z/√n, L2 normalization, weighted edges), and its graphs match Table 2 exactly.
- WordNet gives *man* many more direct links to person-type hubs than *woman*, which may explain why human categories lean male. Untested.
- Fig. 5's significance stars are never defined in the paper, which makes Q4 in the 8 Nov brief ("no p-values") wrong.

**The project.**
- The report plans per-task similarity maps of layers and attention heads on frozen small models, on Colab with a 12 GB GPU. No results yet.
  - The newest version is the Word file `Preliminary_Report_Panoiu.docx` (14 Nov). It is newer than the claude.ai doc.
  - Its model list: Pythia 70M–1.4B, BERT and ModernBERT, Qwen2.5-1.5B, Gemma 3 1B, Qwen3.5-0.8B (Gated DeltaNet), and Falcon-H1-0.5B as optional. The 13 Nov draft had Gemma-2-2B and Zamba2 instead.
- The team is Bogdan Gherghina, Pănoiu Silviu-Cristian and Sîrbu Iulia-Georgiana. Progress reports are 0.5p each, human-written, due at 10:00. The team skips 19 Nov, so its first report is **03 Dec**.
- Question 4 of the report asks whether the instructor expects the paper's skip/reorder interventions, or only the similarity analysis. That decides how much GPU time the project needs.
- In the Painters code, layer order changes through a patched `forward` that loops over a list of layer indices (`gpt/routing_llama.py`). Reordering works without fine-tuning because every layer maps tokens × d to tokens × d.
- The "ADHD skill" is `i-have-adhd` (skills.sh/ayghri/i-have-adhd), not installed; read its SKILL.md with `gh api`.

**Producing documents.**
- Word 16.115's AppleScript `save as` fails with -1708, so .docx → PDF goes through Pages.
- The Claude Docs PDF export strands labels above short tables and has no page-break block. Headings fix the stranded labels, but then tables split. Full control needs your own HTML printed with headless Chrome (`table{break-inside:avoid}`).
- `textutil` html → docx flattens tables.
- On the evening of 14 Nov, the docs tools began refusing edits to the ADHD copy (`forbidden`, role).

**Lab 1.**
- The labs come from github.com/bucuram/llms-and-cognition-labs (lab0–lab6, after Raschka's *LLMs from Scratch*). The open Chrome tab found it; `gh search` didn't.
- The notebooks still carry 2025 deadlines (Lab 1 says 31 Oct 2025). The 2026 deadline and upload form have to come from Teams.
- Headless runs need `nbconvert --allow-errors`, because the labs include deliberate errors (cell 59's `KeyError: 'Hello'`).
- Assignment results: `"Akwirw ier"` → `[33901, 86, 343, 86, 220, 959]` (Ak | w | ir | w | " " | ier), which decodes back exactly. On the story's 5,145 tokens the loader gives 2,572 non-overlapping samples at (2, 2) and 2,569 samples at (8, 2), where neighbouring windows share 6 tokens.

**Finishing a feature here.** This repo tracks `.cs/` in git, which turned `/finish lab1` into five separate blocks:
- integrate refuses over any base dirt, including the timeline line cs writes after each integrate;
- retire refuses over the feature's uncommitted `.cs/` notes, even after `finish.sh report` says `retire: ready`;
- both sides add `.cs/summary.md`;
- `.cs/README.md` conflicts when both sides changed it;
- `MEMORY.md`'s `merge=ours` silently drops `main`'s entries when `main` is merged into a worktree.

The workaround order is in `project_finishing-features-tracked-cs.md`.

## Changes Made

- **Commits on `main`:**
  - `05054b0` (6 Nov): course brief and session notes.
  - `c95d623`: Lab 1 notebook and `.gitignore` entries for `.venv/`, `__pycache__/`, `.ipynb_checkpoints/` and `the-verdict.txt`.
  - `04e7e70`: base session notes (8–14 Nov) and the methodology brief source.
  - `436770c`: lab1's session notes, with its summary at `.cs/features/lab1/summary.md`.
  - `5044783`: merges `main` into `cs/lab1`; keeps both READMEs' text and rebuilds `MEMORY.md` as the union.
  - `338e9a3`: a cs timeline line.
  - Merges `4940242` and `9cc0467` from the two integrates.
- **Retired** the `lab1` worktree and branch. cs moved `lab1/the-verdict.txt` to the system trash; the notebook downloads it again. The lab venv is gone with the worktree.
- **Local only:** `llms-and-cognition-labs/` (a clone with its own `.git`) is listed in `.git/info/exclude` instead of being committed.
- **Published (8–10 Nov):** the Methodology brief and Bogdan's 11 slides in the team template style, with the slide text rewritten to read as Bogdan's own.
- **Created (13 Nov):** the ADHD-shaped Claude Doc of the project report.
- **Edited (14 Nov):** the ADHD copy.
  - Re-synced with the Word report.
  - Trimmed: "(ADHD copy)" dropped from the title, and everything above At a glance removed.
  - Bold labels turned into level-3 headings.
- **Created (14 Nov):** the team task doc. It has 12 tasks from 20 Nov to 02 Dec, with Task, Due and Status columns and no owners, as Bogdan asked.
- **In chat only:** the 12 Nov speech and Q&A cheat sheet, and the Lab 1 concept explanations (`<|unk|>`, tensors, token and positional embeddings, biases).
- **Memory:** entries on course writing style, ugrep, the ADHD skill, the course project, the labs repo, the lab environment, and finishing features with tracked `.cs/`. The chrome-mine reference now also covers claude.ai docs.

## Key Files & Outputs

- `lab1/lab1.ipynb`: Lab 1 with the completed, executed assignment. This is the file to submit.
- `.cs/features/lab1/summary.md`: the lab1 worktree's own summary.
- ADHD copy of the project report: https://claude.ai/artifact/7BhzW3zsp3sndjKiPD2136. The original is https://claude.ai/artifact/FVTzZWBapqxZneJZiBT3Fz (personal account). The newest report is `~/Downloads/Preliminary_Report_Panoiu.docx`.
- `~/Downloads/Preliminary_Report_Panoiu.pdf`: the Word report as a PDF, made with Pages. This is the one to hand in.
- `~/Downloads/Preliminary_Report_Panoiu_ADHD.pdf`: the trimmed ADHD version, 4 pages, built with Chrome from `.cs/local/adhd-report-print.html`.
  - It has more cuts than the doc: no At a glance, Source, First-week checks or sliding-window risk, and question 4 is reworded.
  - `~/Downloads/Preliminary_Report_Panoiu_ADHD.docx` is broken (made with textutil). Delete or rebuild it.
- Team task plan to 03 Dec: https://claude.ai/artifact/DDN1vW7KVjZrhrCFJ2LXm2.
- Slides: https://claude.ai/artifact/SW4gavEyH1vpkJ8Yba2Az6 (v7, shared by link). The artifact is the only copy; the scratchpad source won't survive.
- Methodology brief: https://claude.ai/artifact/38h6BbrZdyayj3uiKYKCaT, source `artifacts/methodology-expert-brief.html`.
- Course brief: https://claude.ai/artifact/JRQr1GKXkD8YnHT9JeH7A8, source `artifacts/llm-cognition-brief.html`.

## Outcome

- **Presentation:** slides, speech and Q&A were ready for 12 Nov. Whether the talk went ahead isn't recorded.
- **Project:** the Word report and its PDF are ready to hand in. The ADHD version exists as a doc and a PDF, and the two have drifted apart. The team plan for the 03 Dec first progress report is in a shared-ready doc.
- **Lab 1:** done, executed and on `main`, but **not submitted**. Confirm the 2026 deadline and form on Teams first.
- **Open tasks (native list):**
  - #1: let `nvim-tab` open a file;
  - #2: correct Q4 in the Methodology brief;
  - #3 and #4: ugrep and zsh quoting notes in `~/.claude/CLAUDE.md`;
  - #5 and #6: make `finish.sh` catch worktree and base dirt before integrate or retire;
  - #7: stop cs's own timeline line from blocking the next integrate.
- The wrap's own changes (this summary, the memory entries, the narrative) are uncommitted.

## Notes for Future Reference

- The course asks that the final project report not be written with an LLM and requires an LLM-disclosure section. Submit the original report, never the reshaped copy.
- For "take labN from the github", fetch `labN.ipynb` from `bucuram/llms-and-cognition-labs` with `gh api`. Recreate the venv with `uv venv --python 3.11 --seed .venv` plus the pinned installs (`project_lab-notebook-env.md`). Deadlines and forms come from Teams, never from the notebook.
- Before `/finish lab2` or `/finish lab3`, follow `project_finishing-features-tracked-cs.md`. Those worktrees will hit the same summary.md, README and MEMORY.md conflicts.
- When a claim depends on a paper's figures, look at the figure images first. A text-only summary produced the wrong Q4.
- To change the ADHD PDF, edit `.cs/local/adhd-report-print.html` and re-run headless Chrome. Before overwriting the file, close it in Acrobat (`tell application "Adobe Acrobat" to close document … saving no`).
- Team plans have no per-person owners (`feedback_team-plans-by-task`).
- Commit `.cs/` files only when Bogdan asks.
