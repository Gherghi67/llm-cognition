---
name: course-project-transformer-layers
description: "LLMs & Cognition course project for actor bogdan-gherghina-erepubliklabs-com: transformer layers and attention-head similarity, based on 'Transformer Layers as Painters'; where the report and its copy live"
metadata:
  node_type: memory
  type: project
  originSessionId: fe2f520e-f50d-4f4b-8ca5-f1e419636f70
  modified: 2026-11-14T19:30:00.000Z
---

On 13–14 Nov 2026, actor bogdan-gherghina-erepubliklabs-com (Bogdan) worked from a course project report titled **"Preliminary Report – Transformer Layers and Attention-Head Similarity"**:
- he asked for an ADHD-shaped copy of it;
- he studied its base paper.

**Team (from the course doc's topic comments):** Bogdan Gherghina, Pănoiu Silviu-Cristian, Sîrbu Iulia-Georgiana. Progress reports are 0.5p each, human-written, due at 10:00 on 19 Nov, 03 Dec, 17 Dec, 14 Jan and 24 Jan (Nov 2026 to Jan 2027). The team skips 19 Nov, so their first progress report is **03 Dec**.

- **Base paper:** Sun, Pickett, Nain, Jones, *Transformer Layers as Painters*, AAAI 2025 (arXiv 2407.09298). Bogdan has the PDF at `~/Downloads/01621-SunQ.pdf`.
- **Paper's code:** github.com/floatingbigcat/transformer_layers_as_painters. The layer-order logic (skip, reverse, random, middle_repeat, loop_parallel) is in [gpt/routing_llama.py](https://github.com/floatingbigcat/transformer_layers_as_painters/blob/main/gpt/routing_llama.py), a patched `LlamaModel.forward` that loops over a list of layer indices.
- **Plan in the report (14 Nov Word version):** Pythia 70M–1.4B, BERT-base/large, plus Qwen2.5-1.5B (grouped-query), Gemma 3 1B and ModernBERT (local/global), Qwen3.5-0.8B (Gated DeltaNet hybrid), Falcon-H1-0.5B optional; all on Colab with a 12 GB GPU. Layer and head similarity maps (cosine, CKA, JS) per task; no training except BERT fine-tuning. The 13 Nov draft had Gemma-2-2B and Zamba2/Falcon-H1 instead.
- **Newest version:** a Word file, `~/Downloads/Preliminary_Report_Panoiu.docx` (14 Nov 2026), newer than the Claude Doc below. When the user says the report "was modified", check for a newer Word file before trusting the Claude Doc.
- **Original report:** a Claude Doc at https://claude.ai/artifact/FVTzZWBapqxZneJZiBT3Fz. It is owned outside the erepubliklabs org, so the docs tools are refused; read it through chrome-mine (see [[teams-via-chrome-mine]]).
- **ADHD copy:** in his erepubliklabs account at https://claude.ai/artifact/7BhzW3zsp3sndjKiPD2136. Same content, reshaped with [[i-have-adhd-skill]]. On 14 Nov the docs tools stopped allowing edits to it (`forbidden`, role).
- **ADHD-copy PDF:** `~/Downloads/Preliminary_Report_Panoiu_ADHD.pdf`, built from `.cs/local/adhd-report-print.html` with headless Chrome. It has had more cuts than the doc: no At a glance, Source, First-week checks or sliding-window risk, and question 4 is reworded. Rebuild it from that HTML, not from the doc (see [[claude-docs-pdf-pagination]]).
- **Team task plan to 03 Dec:** https://claude.ai/artifact/DDN1vW7KVjZrhrCFJ2LXm2. It lists 12 tasks with no per-person owners (see [[team-plans-by-task]]).

**Why:** later course sessions will come back to this project: the report, results, and the final presentation.

**How to apply:** start from these links instead of searching. The course asks that the final project report not be written with an LLM ([[course-writing-style]]), so hand in the original, never the LLM-reshaped copy.
