# Session Summary: llm-cognition

**Date:** 2026-11-02 to 2026-11-14
**Duration:** Short conversations spread over twelve days:
- 2 Nov: Teams access
- 6–7 Nov: commit, clone
- 8 Nov: role prep
- 10 Nov: slides
- 12 Nov: speech, Fig. 5 check
- 13–14 Nov: project report copy, the Painters paper

## Objective

The session started as "how can I connect Claude to MS Teams". It grew into Bogdan's coursework for the University of Bucharest course LLMs & Cognition 2026, in two phases:

1. **Paper presentation (2–12 Nov).** Bogdan was the Methodology Expert (ME) for Team 4's 12 Nov talk on arXiv 2604.12816, "The role of System 1 and System 2 semantic memory structure in human and LLM biases". He presented the bias-measurement method, how the results were obtained, and the conclusion.
2. **Course project (13–14 Nov).** He asked for an ADHD-friendly copy, in his own claude.ai account, of the project's preliminary report, "Transformer Layers and Attention-Head Similarity". He then asked for explanations of the base paper, *Transformer Layers as Painters*.

## Environment

- macOS, Claude Code CLI; one commit and one wrap ran in Codex. Repo `/Users/bogdan.gherghina/Documents/llm-cognition` on `main`.
- University material is read through the local `chrome-mine` MCP. It attaches to Bogdan's own signed-in Chrome (Default profile, his personal Google account). This covers:
  - Teams (unibuc student account);
  - Google Docs;
  - claude.ai docs that the docs connector can't reach.
- There are two claude.ai accounts:
  - the erepubliklabs org account, used by this Claude Code;
  - a personal one, signed in on his Chrome.

  A doc owned by the personal account sits outside the org, and the docs tools refuse to read it.

## Key Discoveries

**Getting at the material.**
- The M365 connector and Graph routes were dead ends: erepubliklabs isn't on Microsoft 365, and unibuc doesn't grant admin consent.
- Scraping in Bogdan's own Chrome works (`reference_teams-via-chrome-mine`).
- On 13 Nov the same route read a claude.ai Doc the docs connector refused. The doc body sits in nested iframes, so `evaluate_script` on the page only returns the title. `take_snapshot` returns the full text and links.

**The bias paper (phase 1).**
- Three three-layer networks (humans, Mistral-7B, Llama-3.1-8B): free associations are System 1; definitions and categories are System 2.
- Gender bias is measured with `spreadr` spreading activation, scored with Wilcoxon effect sizes.
- The authors' earlier LWOW repo fills the method gaps (r = z/√n, L2 normalization, weighted edges). Its graphs match Table 2 exactly.
- WordNet's richer links around *man* explain the odd result that human categories lean male. This explanation is untested.
- The Fig. 5 significance stars are never defined in the paper. The 8 Nov brief's Q4 ("no p-values") is wrong.

**The project (phase 2).**
- The report plans similarity maps of layers and attention heads, computed per task, on frozen small models:
  - Pythia 70M–1.4B and BERT;
  - Qwen2.5-1.5B, Gemma-2-2B and a small Zamba2 or Falcon-H1 for other attention designs.
- It runs on Colab with a 12 GB GPU and has no results yet.
- The "ADHD skill" Bogdan meant is `i-have-adhd` (skills.sh/ayghri/i-have-adhd). It is not installed locally. It shapes output: next action first, numbered steps, time estimates, lists of five or fewer, no preamble or closers. Once invoked it stays on for the session.

**The Painters paper (Sun et al., AAAI 2025).** The intro's analogy compares the middle layers to painters on an assembly line:
- the canvas is the hidden state;
- adding strokes or passing the canvas on is the residual connection;
- the shared vocabulary is the shared representation space.

The experiments partly confirm it:
- middle layers share a representation space;
- skipping and reordering them degrades performance gradually;
- the first and last layers are special;
- copies of one layer are worst, so layers are not interchangeable;
- reasoning tasks are the most order-sensitive ("collage vs. architectural scene").

In the authors' code, the order is changed by a patched `forward` that loops over a list of layer indices (`gpt/routing_llama.py`). This works because every layer maps tokens × d to tokens × d.

## Changes Made

- **Committed (6 Nov):** `05054b0`, the course brief and session notes. Nothing since is committed.
- **Cloned (7 Nov):** the course labs repo into `llms-and-cognition-labs/`. It is a nested git repo, untracked and not gitignored.
- **Published (8–10 Nov):** the Methodology brief and Bogdan's 11 presentation slides in the team template style. The slide text was rewritten to read as his own.
- **Created (13 Nov):** a Claude Doc in Bogdan's erepubliklabs account, "Preliminary Report – Transformer Layers (ADHD copy)". The original's content is reshaped:
  - next action and status first;
  - five tickable steps with time estimates;
  - small tables;
  - lists of at most five.
- **Speech (12 Nov):** a ~9–10 minute speech and a Q&A cheat sheet, delivered in chat only.
- **Memory:**
  - four new entries: `feedback_course-writing-style`, `project_bash-grep-is-ugrep`, `reference_i-have-adhd-skill`, `project_course-project-transformer-layers`;
  - the chrome-mine reference extended to cover claude.ai docs.

## Key Files & Outputs

- **ADHD copy of the project report:** https://claude.ai/artifact/7BhzW3zsp3sndjKiPD2136. The original is https://claude.ai/artifact/FVTzZWBapqxZneJZiBT3Fz (personal account). The raw snapshot is in `.cs/local/prelim-report-snapshot.txt`.
- **Slides:** https://claude.ai/artifact/SW4gavEyH1vpkJ8Yba2Az6 (v7, shared by link). The artifact is the copy of record; the scratchpad source won't survive.
- **Methodology brief:** https://claude.ai/artifact/38h6BbrZdyayj3uiKYKCaT, source `artifacts/methodology-expert-brief.html` (uncommitted).
- **Course brief:** https://claude.ai/artifact/JRQr1GKXkD8YnHT9JeH7A8, source `artifacts/llm-cognition-brief.html` (committed).
- **Base paper PDF:** `~/Downloads/01621-SunQ.pdf`. Code: github.com/floatingbigcat/transformer_layers_as_painters.

## Outcome

- **Phase 1:** Teams access works. The ME role, slides, speech and Q&A were ready for the 12 Nov talk. Whether the talk went ahead isn't recorded.
- **Phase 2:** the ADHD-shaped copy of the project report is in Bogdan's account. He understands the Painters analogy and how the paper changes layer order.
- **Still open (native task list):**
  - #1: let `nvim-tab` open a file;
  - #2: correct Q4 in the Methodology brief;
  - #3: note in `~/.claude/CLAUDE.md` that Bash grep is ugrep;
  - #4: add a zsh quoting note there (quote `?` URLs; no bare words starting with `=`).
- **Course deadline:** the topic and plan were due 14 Nov AoE (per the 2 Nov schedule). Whether the preliminary report is that deliverable is not confirmed.

## Notes for Future Reference

- The course asks that the final project report not be written with an LLM and requires an LLM-disclosure section. Submit the original report, never the LLM-reshaped copy. Flag this whenever helping with the report.
- If Bogdan says "use the ADHD skill", fetch `i-have-adhd`'s SKILL.md with `gh api` and keep its rules on until he says "stop adhd mode".
- When a claude.ai link comes from his personal account, the docs tools return `access` denied. Read it through chrome-mine `take_snapshot`, and close any tab you open.
- When a claim depends on a paper's figures, look at the figure images before stating it. A text-only summary led to the wrong Q4.
- Everything under `.cs/`, plus the methodology brief source, is uncommitted. Commit only when Bogdan asks.
