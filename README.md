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

## Author and licence

- Author: Tariq Said
- Licence: MIT
- UI/UX Design Inspiration: UI/UX Pro Max by NextLevelBuilder, MIT Licence

See `LICENSE` and `NOTICE.md` for the complete licence and attribution details.

---
