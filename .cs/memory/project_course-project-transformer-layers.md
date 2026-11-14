---
name: course-project-transformer-layers
description: "LLMs & Cognition course project for actor bogdan-gherghina-erepubliklabs-com: transformer layers and attention-head similarity, based on 'Transformer Layers as Painters'; where the report and its copy live"
metadata:
  node_type: memory
  type: project
  originSessionId: fe2f520e-f50d-4f4b-8ca5-f1e419636f70
  modified: 2026-11-14T14:32:04.152Z
---

On 13–14 Nov 2026, actor bogdan-gherghina-erepubliklabs-com (Bogdan) worked from a course project report titled **"Preliminary Report – Transformer Layers and Attention-Head Similarity"**:
- he asked for an ADHD-shaped copy of it;
- he studied its base paper.

The report's "Team:" line names Pănoiu Silviu-Cristian. Whether Bogdan is a co-author is not recorded.

- **Base paper:** Sun, Pickett, Nain, Jones, *Transformer Layers as Painters*, AAAI 2025 (arXiv 2407.09298). Bogdan has the PDF at `~/Downloads/01621-SunQ.pdf`.
- **Paper's code:** github.com/floatingbigcat/transformer_layers_as_painters. The layer-order logic (skip, reverse, random, middle_repeat, loop_parallel) is in [gpt/routing_llama.py](https://github.com/floatingbigcat/transformer_layers_as_painters/blob/main/gpt/routing_llama.py), a patched `LlamaModel.forward` that loops over a list of layer indices.
- **Plan in the report:** Pythia 70M–1.4B, BERT-base/large, plus Qwen2.5-1.5B, Gemma-2-2B and a small Zamba2 or Falcon-H1, all on Colab with a 12 GB GPU. Layer and head similarity maps (cosine, CKA, JS) per task; no training except BERT fine-tuning.
- **Original report:** a Claude Doc at https://claude.ai/artifact/FVTzZWBapqxZneJZiBT3Fz. It is owned outside the erepubliklabs org, so the docs tools are refused; read it through chrome-mine (see [[teams-via-chrome-mine]]).
- **ADHD copy:** in his erepubliklabs account at https://claude.ai/artifact/7BhzW3zsp3sndjKiPD2136. Same content, reshaped with [[i-have-adhd-skill]].

**Why:** later course sessions will come back to this project: the report, results, and the final presentation.

**How to apply:** start from these links instead of searching. The course asks that the final project report not be written with an LLM ([[course-writing-style]]), so hand in the original, never the LLM-reshaped copy.
