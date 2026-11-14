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

## Environment

macOS laptop, Claude Code CLI. Research question only, no code involved. claude.ai connectors (Gmail, Drive, Slack) already show up in this Claude Code session as mcp__claude_ai_* tools.

lab1 worktree: feature worktree `llm-cognition@lab1` on branch `cs/lab1`. Notebooks run in a gitignored Python 3.11 uv venv at `.venv` (torch 2.0.1, tiktoken 0.7.0), because the system `python3` is 3.15.

## Outcome

Teams connected by scraping the user's own Chrome through a local `chrome-mine` MCP (chrome-devtools-mcp --autoConnect), with no app registration. The official M365 connector and Graph MCP were ruled out because the Teams account is a University of Bucharest student account. First use: read the LLMs and Cognition 2026 class and published the course brief artifact https://claude.ai/artifact/JRQr1GKXkD8YnHT9JeH7A8.

lab1 worktree: Lab 1 ("Working with Text") was copied from github.com/bucuram/llms-and-cognition-labs into `lab1/lab1.ipynb`. Both assignment parts are done there with outputs and short write-ups: the BPE breakdown of "Akwirw ier", and the data loader runs with (2,2) and (8,2). Not yet submitted. The notebook's 31 Oct 2025 deadline is stale and needs confirming on Teams. Nothing committed.
