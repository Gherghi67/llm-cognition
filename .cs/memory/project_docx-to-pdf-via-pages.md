---
name: docx-to-pdf-via-pages
description: "On this Mac, convert .docx to PDF through Pages AppleScript; Word 16.115's AppleScript \"save as\" fails with -1708 and there is no pandoc or LibreOffice"
metadata:
  node_type: memory
  type: project
  originSessionId: 0f4662d1-814e-492e-b153-cd7f677da902
  modified: 2026-11-14T16:42:24.809Z
---

On 14 Nov 2026, converting `~/Downloads/Preliminary_Report_Panoiu.docx` to PDF ([[course-project-transformer-layers]]):
- **What failed:** Microsoft Word 16.115 rejects `save as … file format format PDF` over osascript with error -1708 ("doesn't understand the save as message"). That happens whether the document is addressed by name, as `active document`, as `document 1`, or in a `tell` block, and with either an HFS or a POSIX path.
- **What is missing:** pandoc, LibreOffice/soffice and docx2pdf are not installed.
- **What worked:** Pages via osascript (`open` the docx, `export d to file <POSIX file> as PDF`, `close d saving no`, then quit Pages if it wasn't running before). Hyperlinks survive.
- **Pages fidelity gap:** it drops the thin rule under table header rows. That rule comes from the pandoc-style "Table" style, which has a bottom border on firstRow.

**Why:** this saves retrying the Word route.

**How to apply:**
- Go straight to Pages for docx → PDF.
- Read the result back with the Read tool (pages param) to check the layout.
- If exact Word rendering matters, the user exports it in Word by hand: File → Save As → PDF.
