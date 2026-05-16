# PDF Pro

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![ChatGPT Skill](https://img.shields.io/badge/ChatGPT-Skill-blue)
![PDF Workflow](https://img.shields.io/badge/PDF-Workflow-red)
![Python](https://img.shields.io/badge/Python-3.x-green)

**PDF Pro** is a professional ChatGPT Skill for production-ready PDF workflows.

It helps ChatGPT create, edit, inspect, extract, validate, and visually improve PDF files using a structured verification-first process. The skill is designed for workflows where the final PDF must be usable, visually checked, accurate, and ready to share.

PDF Pro combines practical PDF operations with structured design guidance inspired by UI/UX Pro Max, helping produce documents that are not only technically correct but also clear, readable, and visually polished.

---

## Repository description

A professional ChatGPT Skill for creating, editing, reviewing, extracting, validating, and visually improving production-ready PDF files.

---

## What this skill supports

PDF Pro supports a wide range of professional PDF tasks, including:

- Creating new PDFs from structured content.
- Editing existing PDFs through safe operations such as merge, split, rotate, watermark, and extraction.
- Reviewing PDFs by inspecting metadata, page count, encryption status, page sizes, rotation, and text layer availability.
- Rendering PDF pages to PNG for visual verification.
- Extracting text from selectable-text PDFs.
- Applying professional visual design rules for client-facing PDFs.
- Creating polished reports, handouts, one-pagers, certificates, dashboards, worksheets, and branded documents.
- Running a validation protocol before delivery.
- Reporting limitations clearly, especially when working with scanned pages, missing fonts, OCR uncertainty, or poor source quality.

---

## Designed for

PDF Pro is suitable for:

- Client-facing reports
- Branded PDF documents
- Certificates
- One-page documents
- Educational handouts
- Worksheets
- Dashboards
- Internal reports
- Policy documents
- PDF inspection workflows
- PDF extraction workflows
- Safe PDF editing workflows
- Visual review before final delivery

---

## Core workflow

PDF Pro follows a production-style workflow:

1. Identify the PDF task.
2. Inspect or render the input where needed.
3. Choose the safest authoring or editing method.
4. Perform the operation.
5. Inspect or render the output.
6. Validate the final file.
7. Deliver the PDF with a clear summary of what was done and what was verified.

The goal is to avoid treating PDF work as a one-step file operation. Every final PDF should be checked before delivery.

---

## Author and licence

- Author: Tariq Said
- Licence: MIT
- UI/UX Design Inspiration: UI/UX Pro Max by NextLevelBuilder, MIT Licence

See `LICENSE` and `NOTICE.md` for the complete licence and attribution details.

---

## Folder structure

```text
pdf-pro/
├── SKILL.md
├── README.md
├── LICENSE
├── NOTICE.md
├── agents/
│   └── openai.yaml
├── assets/
│   ├── design-tokens-starter.json
│   └── pdf.png
├── references/
│   ├── pdf-workflows.md
│   ├── quality-checklist.md
│   ├── validation-protocol.md
│   └── visual-design-system.md
└── scripts/
    ├── create_visual_pdf.py
    ├── pdf_ops.py
    └── validate_pdf.py
```

---

## Main entry point

`SKILL.md` is the primary instruction file used by ChatGPT.

It defines:

- When the skill should be used.
- How PDF tasks should be classified.
- Which workflows should be followed.
- When to inspect, render, extract, edit, validate, or visually review a PDF.
- How final outputs should be delivered to the user.

---

## Helper scripts

Run scripts from inside the `pdf-pro` folder, or pass absolute paths.

---

### Install optional dependencies

The helper scripts may use common Python PDF packages depending on the operation.

```bash
python -m pip install pypdf pymupdf reportlab
```

---

### Inspect a PDF

Use this to check metadata, page count, encryption status, page sizes, rotation, and text availability.

```bash
python scripts/pdf_ops.py inspect input.pdf
```

---

### Extract text

Use this for PDFs that contain a selectable text layer.

```bash
python scripts/pdf_ops.py extract-text input.pdf --out extracted.txt
```

---

### Render pages for visual review

Use this when layout, tables, diagrams, scans, signatures, charts, or visual quality matter.

```bash
python scripts/pdf_ops.py render input.pdf --out-dir renders/input --dpi 160
```

---

### Merge PDFs

Combine multiple PDF files into one output file.

```bash
python scripts/pdf_ops.py merge output.pdf first.pdf second.pdf
```

---

### Split pages

Extract selected pages from a PDF.

```bash
python scripts/pdf_ops.py split input.pdf --pages 1-3,7 --out selected-pages.pdf
```

---

### Rotate pages

Rotate selected pages by a specified angle.

```bash
python scripts/pdf_ops.py rotate input.pdf --pages 1,3-5 --angle 90 --out rotated.pdf
```

---

### Add a watermark

Apply a text watermark to a PDF.

```bash
python scripts/pdf_ops.py watermark input.pdf --text "DRAFT" --out watermarked.pdf
```

---

### Validate a finished PDF

Use this before delivering a final PDF.

```bash
python scripts/validate_pdf.py output.pdf --expected-pages 5 --render --out-dir validation/output
```

The validation script checks whether the file exists, opens successfully, has the expected page count when provided, exposes page dimensions and rotation, optionally extracts text statistics, and optionally renders pages for visual review.

---

## Creating visual PDFs

PDF Pro includes a helper script for generating polished fixed-layout PDFs from a structured JSON content specification.

```bash
python scripts/create_visual_pdf.py input.json --out output.pdf
```

This is useful for:

- One-pagers
- Certificates
- Visual reports
- Simple branded documents
- Presentation-style PDF pages
- Structured handouts

For complex long-form documents, it is often better to author the content in DOCX or Markdown first, then convert and validate the final PDF.

---

## External dependencies

The helper scripts may use these Python libraries:

- `pypdf` for metadata inspection, splitting, merging, rotation, watermark composition, and text extraction.
- `PyMuPDF`, imported as `fitz`, for rendering PDF pages to images.
- `reportlab` for fixed-layout PDF creation and watermark generation.

These libraries are not bundled inside this skill. Their own licences apply when installed separately by the user or runtime environment.

---

## Validation standard

Before a final PDF is delivered, verify at minimum:

1. The output file exists and opens.
2. The page count is correct.
3. Page sizes and rotations are intentional.
4. Text extraction is checked when text layer accuracy matters.
5. Visual renders are checked for clipping, overlap, missing glyphs, weak contrast, and layout errors.
6. Any limitation is stated clearly, especially scanned pages, OCR uncertainty, missing fonts, or source-file quality issues.

See `references/validation-protocol.md` for the full protocol.

---

## Visual design guidance

For visual or client-facing PDFs, PDF Pro uses design-system thinking inspired by UI/UX Pro Max.

The design priorities are:

1. Accessibility
2. Readable typography
3. Clear visual hierarchy
4. Consistent spacing
5. Strong alignment
6. Sufficient contrast
7. Predictable layout structure
8. Purposeful use of colour
9. Clean chart and table presentation
10. Final visual verification through rendered page images

The default visual standard is restrained, readable, accessible, and polished. Decoration should never make the document harder to scan.

---

## Quality checklist

Before delivering a visual PDF, check:

- No clipped text.
- No overlapping elements.
- No missing glyphs.
- No broken images.
- No accidental page rotation.
- Margins are consistent.
- Headings are clear.
- Tables are readable.
- Charts are labelled.
- Colours have enough contrast.
- The PDF opens successfully.
- Rendered pages match the intended layout.

See `references/quality-checklist.md` for the complete checklist.

---

## Safe editing principle

PDF Pro prioritises safe operations.

For existing PDFs, the recommended process is:

1. Inspect the file first.
2. Render pages if the visual layout matters.
3. Apply the smallest safe edit.
4. Inspect and render the output.
5. Summarise exactly what changed.

For redaction, do not simply draw black rectangles over text. True redaction must remove the underlying text or pixels and then be verified by extraction and rendering.

---

## Example use cases

PDF Pro can help ChatGPT handle requests such as:

```text
Create a polished PDF report from this content.
```

```text
Inspect this PDF and tell me whether it has selectable text.
```

```text
Merge these PDFs into one file and validate the result.
```

```text
Split pages 1 to 3 from this PDF.
```

```text
Rotate pages 2 and 4 by 90 degrees.
```

```text
Extract the text from this PDF.
```

```text
Render this PDF so I can visually check the layout.
```

```text
Create a branded certificate as a PDF.
```

```text
Review this PDF for layout issues before I send it to a client.
```

---

## Suggested GitHub topics

```text
chatgpt-skill
pdf
pdf-tools
pdf-generation
pdf-editing
pdf-validation
document-automation
visual-design
report-generation
python
pypdf
pymupdf
reportlab
```

---

## Attribution note

This skill includes original PDF workflow instructions authored for this package.

Its visual design guidance is inspired by UI/UX Pro Max by NextLevelBuilder, which is identified as MIT-licensed. This package does not claim ownership of UI/UX Pro Max or its upstream project.

See `NOTICE.md` for full attribution details.

---

## Licence

This project is released under the MIT Licence.

See `LICENSE` for details.

---

## Maintainer

Created and maintained by **Tariq Said**.

PDF Pro is part of DXBMark’s professional workflow tooling for document automation, PDF production, and AI-assisted content operations.
