---
name: claude-docs-pdf-pagination
description: "Claude Docs PDF export cannot keep a table on one page or force a page break; for print control, render your own HTML with headless Chrome"
metadata:
  node_type: memory
  type: project
  originSessionId: 0f4662d1-814e-492e-b153-cd7f677da902
  modified: 2026-11-14T17:54:41.429Z
---

Measured on Claude Code 2.1.325, 2026-11-14, exporting a Claude Doc with the docs `export` tool (format pdf, renderer `pdf-w1`):
- **Short tables:** a table that doesn't fit moves to the next page whole. A plain bold-paragraph label above it stays behind, leaving a stranded label and a near-empty page.
- **Headings:** headings do stay with the next block. Turning labels into level-3 headings (`set attrs {"heading":3}`) fixes stranded labels, but then the table splits by rows instead.
- **No page break:** there is no page-break block. The insert law accepts paragraph, list, codeBlock, blockquote, table, embed, horizontalRule, pending, hardBreak, mention, date, dropdown and media.
- **HTML export:** it is bare markup with no CSS. It comes back inline as base64 (only a large export such as a PDF lands in tool-results/), so it can't be turned into a file without retyping it.
- **HTML → docx:** macOS `textutil -convert docx` flattens tables into one cell per line and drops list numbers. Don't use it for documents with tables.

**What worked for full print control:** a hand-built HTML file printed with headless Chrome (`--headless=new --user-data-dir=<scratch> --no-pdf-header-footer --print-to-pdf`). Its CSS: `@page { size: A4; @top-left / @bottom-right margin boxes }`, `table { break-inside: avoid }`, `h2, h3 { break-after: avoid }`, `p:has(+ table) { break-after: avoid }`. Check its text against the docs PDF with a pypdf bag-of-words compare (`uv run --with pypdf`).

**Why:** a user who asks for "this table on one page" can't get it from the docs PDF tool, and rounds spent on heading tweaks don't fix it.

**How to apply:** for page-layout requests, go straight to the Chrome route. For docx with real tables, use python-docx, not textutil. Related: [[docx-to-pdf-via-pages]].
