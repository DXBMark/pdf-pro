# Claude Usage Notes

PDF Pro can be adapted for Claude Skills and Claude Code workflows.

Use this repository as a structured PDF production workflow package with instructions, references, assets, and executable helper scripts.

## Main instruction source

Use `SKILL.md` as the main workflow guide. When the instructions mention ChatGPT, interpret that as the active assistant using this package.

For Claude-specific usage, also read `platforms/claude.md`.

## Operating workflow

Claude should follow this workflow for PDF tasks:

1. Identify the PDF task: create, review, extract, edit, convert, redact, form-fill, visual redesign, or CLI automation.
2. Inspect or render the input before changing it when working with an existing PDF.
3. Use the smallest safe operation for edits.
4. Render or inspect the output after changes.
5. Validate any produced or modified PDF.
6. Report what changed, what was verified, and any limitations.

## Reference files

Use these files when relevant:

- `references/pdf-workflows.md` for task-specific workflows.
- `references/visual-design-system.md` for visual or client-facing PDFs.
- `references/quality-checklist.md` before delivery.
- `references/validation-protocol.md` before claiming a PDF is final, correct, ready, fixed, redacted, merged, split, or polished.
- `references/cli-integration.md` for Claude Code and terminal workflows.

## Helper scripts

Examples:

```bash
python scripts/pdf_ops.py inspect input.pdf
python scripts/pdf_ops.py render input.pdf --out-dir renders/input --dpi 160
python scripts/pdf_ops.py merge output.pdf first.pdf second.pdf
python scripts/validate_pdf.py output.pdf --render --out-dir validation/output
python scripts/create_visual_pdf.py examples/visual-spec.json --out output.pdf
```

If installed as a local package:

```bash
pdf-pro inspect input.pdf
pdf-pro validate output.pdf --render --out-dir validation/output
```

## Dependency notes

Install optional dependencies when needed:

```bash
python -m pip install pypdf pymupdf reportlab
```

## Redaction safety

For redaction, do not cover text with a rectangle only. True redaction must remove underlying text or pixels and be verified through text extraction and rendering.

Prefer local processing for confidential PDFs where possible.
