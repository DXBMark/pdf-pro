# PDF Pro

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![ChatGPT Skill](https://img.shields.io/badge/ChatGPT-Skill-blue)
![Claude Ready](https://img.shields.io/badge/Claude-Adaptable-purple)
![CLI Ready](https://img.shields.io/badge/CLI-VSCode%20%7C%20Claude%20Code%20%7C%20Copilot-green)
![PDF Workflow](https://img.shields.io/badge/PDF-Workflow-red)
![Python](https://img.shields.io/badge/Python-3.10%2B-green)

**PDF Pro** is a production-ready PDF workflow package for AI assistants and local automation.

It is designed first as a **ChatGPT Skill** and structured to be adaptable for **Claude Skills**, **Claude Code**, **Gemini Gems**, **VSCode**, **GitHub Copilot**, **Antigravity**, and other coding-agent or CLI workflows.

PDF Pro helps assistants and developers create, edit, inspect, extract, render, validate, redact, and visually improve PDF files through a verification-first process. It combines practical PDF operations with design-system guidance so final documents are usable, visually checked, accurate, and ready to share.

---

## Repository description

A professional AI workflow package for creating, editing, reviewing, extracting, validating, redacting, and visually improving production-ready PDF files across ChatGPT Skills, Claude Skills, and CLI-based coding agents.

---

## What this package supports

- Creating new PDFs from structured content.
- Creating polished visual PDFs from JSON specifications.
- Editing existing PDFs through safe operations such as merge, split, rotate, crop, watermark, redaction, and extraction.
- Reviewing PDFs by inspecting metadata, page count, encryption status, page sizes, rotation, and text layer availability.
- Rendering PDF pages to PNG for visual verification.
- Extracting text from selectable-text PDFs.
- Validating final PDF outputs before delivery.
- Checking required and forbidden phrases during validation.
- Applying professional visual design rules for client-facing PDFs.
- Supporting local CLI workflows for editors and coding agents.
- Providing platform guidance for ChatGPT, Claude, Gemini, Copilot, Antigravity, and local assistants.

---

## Platform compatibility

| Target | Status | How to use |
|---|---:|---|
| ChatGPT Skills | Direct support | Use the root `SKILL.md`, `agents/openai.yaml`, `references/`, `scripts/`, and `assets/` |
| Claude Skills | Adaptable | Use `CLAUDE.md` or `platforms/claude.md` with the same scripts and references |
| Claude Code | CLI-ready | Use `AGENTS.md`, `CLI.md`, and terminal commands |
| VSCode | CLI-ready | Use `.vscode/tasks.json` or integrated terminal commands |
| GitHub Copilot | CLI-ready | Use `AGENTS.md`, `CLI.md`, and repo scripts as project context |
| Antigravity | CLI-ready | Use `AGENTS.md`, `CLI.md`, and `references/cli-integration.md` |
| Gemini Gems | Instruction/reference adaptation | Use `GEMINI.md` and `platforms/gemini.md` |
| Local LLM agents | Adaptable | Load `AGENTS.md`, `SKILL.md`, `references/`, and run the CLI locally |

Compatibility depends on whether the target platform supports instruction files, uploaded references, filesystem access, and code execution.

---

## Designed for

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
- Editor-based automation in VSCode, Claude Code, Copilot, and Antigravity

---

## Core workflow

PDF Pro follows a production-style workflow:

1. Identify the PDF task.
2. Inspect or render the input where needed.
3. Choose the safest authoring or editing method.
4. Perform the smallest safe operation.
5. Inspect or render the output.
6. Validate the final file.
7. Deliver the PDF with a clear summary of what was done, what was verified, and any limitation.

The goal is to avoid treating PDF work as a one-step file operation. Every final PDF should be checked before delivery.

---

## Author and licence

- Author: Tariq Said
- Licence: MIT
- UI/UX Design Inspiration: UI/UX Pro Max by NextLevelBuilder, MIT Licence

See [LICENSE](LICENSE) and [NOTICE.md](NOTICE.md) for the complete licence and attribution details.

---

## Folder structure

```text
pdf-pro/
├── SKILL.md
├── README.md
├── LICENSE
├── NOTICE.md
├── AGENTS.md
├── CLAUDE.md
├── GEMINI.md
├── CLI.md
├── pyproject.toml
├── agents/
│   └── openai.yaml
├── assets/
│   ├── design-tokens-starter.json
│   └── pdf.png
├── examples/
│   └── visual-spec.json
├── platforms/
│   ├── chatgpt.md
│   ├── claude.md
│   ├── gemini.md
│   └── cli-agents.md
├── references/
│   ├── pdf-workflows.md
│   ├── quality-checklist.md
│   ├── validation-protocol.md
│   ├── visual-design-system.md
│   ├── cli-integration.md
│   ├── platform-compatibility.md
│   └── compatibility-checklist.md
├── scripts/
│   ├── create_visual_pdf.py
│   ├── pdf_ops.py
│   ├── validate_pdf.py
│   └── validate_package.py
├── src/
│   └── pdf_pro/
│       ├── __init__.py
│       ├── cli.py
│       ├── create_visual_pdf.py
│       ├── pdf_ops.py
│       └── validate_pdf.py
└── tests/
    └── test_cli_smoke.py
```

---

## Main entry points

### ChatGPT Skills

[SKILL.md](SKILL.md) is the primary ChatGPT Skill instruction file.

It defines:

- When the skill should be used.
- How PDF tasks should be classified.
- Which workflows should be followed.
- When to inspect, render, extract, edit, validate, redact, or visually review a PDF.
- How final outputs should be delivered.

### Claude Skills and Claude Code

Use [CLAUDE.md](CLAUDE.md) and [platforms/claude.md](platforms/claude.md).

### Gemini Gems

Use [GEMINI.md](GEMINI.md) and [platforms/gemini.md](platforms/gemini.md).

### CLI and coding agents

Use [CLI.md](CLI.md), [AGENTS.md](AGENTS.md), and [references/cli-integration.md](references/cli-integration.md).

---

## Install for CLI use

From the repository root:

```bash
python -m pip install -e .
```

Install optional PDF dependencies:

```bash
python -m pip install pypdf pymupdf reportlab
```

Or install with the package extras:

```bash
python -m pip install -e ".[pdf]"
```

---

## CLI examples

Inspect a PDF:

```bash
pdf-pro inspect input.pdf
```

Extract text:

```bash
pdf-pro extract-text input.pdf --out extracted.txt
```

Render pages for visual review:

```bash
pdf-pro render input.pdf --out-dir renders/input --dpi 160
```

Merge PDFs:

```bash
pdf-pro merge output.pdf first.pdf second.pdf
```

Split pages:

```bash
pdf-pro split input.pdf --pages 1-3,7 --out selected-pages.pdf
```

Rotate pages:

```bash
pdf-pro rotate input.pdf --pages 1,3-5 --angle 90 --out rotated.pdf
```

Crop pages:

```bash
pdf-pro crop input.pdf --box 36,36,559,806 --out cropped.pdf
```

Add a watermark:

```bash
pdf-pro watermark input.pdf --text "DRAFT" --out watermarked.pdf
```

Redact matched text:

```bash
pdf-pro redact input.pdf --text "Confidential" --out redacted.pdf
```

Validate a finished PDF:

```bash
pdf-pro validate output.pdf --expected-pages 5 --render --out-dir validation/output
```

Create a visual PDF from JSON:

```bash
pdf-pro visual examples/visual-spec.json --out output.pdf
```

---

## Script examples

The same operations are available without installing the package:

```bash
python scripts/pdf_ops.py inspect input.pdf
python scripts/pdf_ops.py render input.pdf --out-dir renders/input --dpi 160
python scripts/pdf_ops.py merge output.pdf first.pdf second.pdf
python scripts/validate_pdf.py output.pdf --render --out-dir validation/output
python scripts/create_visual_pdf.py examples/visual-spec.json --out output.pdf
```

---

## Validation standard

Before a final PDF is delivered, verify at minimum:

1. The output file exists and opens.
2. The page count is correct.
3. Page sizes and rotations are intentional.
4. Text extraction is checked when text layer accuracy matters.
5. Visual renders are checked for clipping, overlap, missing glyphs, weak contrast, and layout errors.
6. Any limitation is stated clearly, especially scanned pages, OCR uncertainty, missing fonts, password protection, or poor source-file quality.

See [references/validation-protocol.md](references/validation-protocol.md) for the full protocol.

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

See [references/quality-checklist.md](references/quality-checklist.md) for the complete checklist.

---

## Redaction note

PDF Pro includes redaction workflow guidance and a text redaction command using a redaction-capable PDF engine where available. Do not treat a visual black box as safe redaction. True redaction must remove underlying text or pixels and must be verified through text extraction and rendering.

See [references/validation-protocol.md](references/validation-protocol.md) for redaction validation rules.

---

## Package validation

Validate the repository structure:

```bash
python scripts/validate_package.py .
```

Run smoke tests:

```bash
python -m pytest
```

Compile Python files:

```bash
python -m compileall scripts src
```

---

## Attribution note

This package includes original PDF workflow instructions authored for PDF Pro.

Its visual design guidance is inspired by UI/UX Pro Max by NextLevelBuilder, which is identified as MIT-licensed. This package does not claim ownership of UI/UX Pro Max or its upstream project.

See [NOTICE.md](NOTICE.md) for full attribution details.

---

## Licence

This project is released under the MIT Licence.

See [LICENSE](LICENSE) for details.

---

## Maintainer

Created and maintained by **Tariq Said**.

PDF Pro is part of DXBMark’s professional workflow tooling for document automation, PDF production, and AI-assisted content operations.
