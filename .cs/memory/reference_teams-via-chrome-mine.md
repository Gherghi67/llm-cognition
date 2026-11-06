---
name: teams-via-chrome-mine
description: "How to read the user's university Microsoft Teams (s.unibuc.ro) — scrape it in their own Chrome via the local chrome-mine MCP; no Graph/app registration"
metadata:
  node_type: memory
  type: reference
  originSessionId: df3f1302-8fae-4c0e-a091-f4d770622329
  modified: 2026-11-02T20:58:24.654Z
---

The user's Teams account is a University of Bucharest student account (`bogdan.gherghina@s.unibuc.ro`), not erepubliklabs.com. erepubliklabs isn't on Microsoft 365. The user chose scraping over any Graph route. Don't propose Entra app registration, the claude.ai M365 connector or Graph MCP servers again unless asked.

**How:** in the llm-cognition project, the `chrome-mine` MCP (`npx chrome-devtools-mcp@1.11.0 --autoConnect`, local scope) attaches to the user's running Chrome, Default profile (gherghinabogdan7@gmail.com), where unibuc Teams is signed in at https://teams.cloud.microsoft/. Remote debugging must be on (chrome://inspect/#remote-debugging), and Chrome asks to Allow each connection. The plugin `chrome-devtools` server is a separate, signed-out browser, and the user does not want that one used ("not that browser").

**Scraping tips:** channel posts are under `[data-tid="channel-pane-message"]`, with `[data-tid="timestamp"]` title holding the full date. Assignments, Classwork and Shared are cross-origin iframes, so read them with take_snapshot. Embedded Google Docs read cleanly via `/document/d/<id>/mobilebasic` in a background tab. Close any tab you open. `filePath` outputs outside the workspace are refused.

Classes on that account: FMI 2026-2027, Deontology FMI Master, LLMs and Cognition 2026, Foundations of NLP 2026-2027.
