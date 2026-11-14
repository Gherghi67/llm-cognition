---
status: active
created: 2026-11-02
tags: []
aliases: ["llm-cognition"]
---
# Session: llm-cognition

**Started:** 2026-11-02 11:36:19
**Location:** erp-bogdang-mac:/Users/bogdan.gherghina/Documents/llm-cognition

## Objective

how can I connect claude to ms teams

**lab1 worktree (2026-11-14):** take Lab 1 from the course GitHub, explain its concepts, and do its assignment.

lab2 worktree (2026-11-14): fetch and work on lab2.ipynb (Coding Attention Mechanisms) from github.com/bucuram/llms-and-cognition-labs.

## Environment

macOS laptop, Claude Code CLI. Research question only, no code involved. lab2 worktree: labs run in a uv Python 3.12 venv at .venv/ (gitignored; Homebrew python3 3.15 has no torch wheels). claude.ai connectors (Gmail, Drive, Slack) already show up in this Claude Code session as mcp__claude_ai_* tools.

lab1 worktree: feature worktree `llm-cognition@lab1` on branch `cs/lab1`. Notebooks run in a gitignored Python 3.11 uv venv at `.venv` (torch 2.0.1, tiktoken 0.7.0), because the system `python3` is 3.15.

## Outcome

Teams connected by scraping the user's own Chrome through a local `chrome-mine` MCP (chrome-devtools-mcp --autoConnect), with no app registration. The official M365 connector and Graph MCP were ruled out because the Teams account is a University of Bucharest student account. First use: read the LLMs and Cognition 2026 class and published the course brief artifact https://claude.ai/artifact/JRQr1GKXkD8YnHT9JeH7A8.

The session then moved on to preparing Bogdan's Methodology Expert part for Team 4's 12 Nov presentation of arXiv 2604.12816. Outputs:
- the role brief, https://claude.ai/artifact/38h6BbrZdyayj3uiKYKCaT;
- 11 slides in the team's template style, https://claude.ai/artifact/SW4gavEyH1vpkJ8Yba2Az6;
- the course labs repo, cloned into `llms-and-cognition-labs/`.

Open items: present on 12 Nov, pick the project topic by 14 Nov, and correct Q4 in the role brief.

13–14 Nov: read the course project's preliminary report ("Transformer Layers and Attention-Head Similarity"). It lives in the user's personal claude.ai account, so it was read through chrome-mine. Made an ADHD-shaped copy with the i-have-adhd skill in the erepubliklabs account: https://claude.ai/artifact/7BhzW3zsp3sndjKiPD2136. Explained the base paper's painters analogy and how its code reorders layers.

lab1 worktree: Lab 1 ("Working with Text") was copied from github.com/bucuram/llms-and-cognition-labs into `lab1/lab1.ipynb`. Both assignment parts are done there with outputs and short write-ups: the BPE breakdown of "Akwirw ier", and the data loader runs with (2,2) and (8,2). Not yet submitted. The notebook's 31 Oct 2025 deadline is stale and needs confirming on Teams. Committed and integrated into main on 14 Nov.

lab2 worktree (2026-11-14): both assignment parts solved and executed. Part 1: GPT-2-sized MultiHeadAttention = 2,360,064 params. Part 2: BertViz on bert-base-uncased in labs/lab2_bertviz.ipynb. Submission zip at labs/lab2.zip. Not submitted (Google Form needs sign-in; check the real deadline on Teams). Committed on 14 Nov.
