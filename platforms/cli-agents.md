# Agent Instructions for PDF Pro

These instructions are for coding agents such as Claude Code, GitHub Copilot, Antigravity, VSCode agents, and local LLM agents.

## Primary rule

Do not claim a PDF task is complete until the output has been inspected or validated.

## Required reading order

1. `README.md` for repository overview.
2. `CLI.md` for terminal commands.
3. `references/validation-protocol.md` for final checks.
4. `references/pdf-workflows.md` for task-specific workflows.
5. `references/visual-design-system.md` for visual PDFs.

## Command preference

Prefer the installed CLI:

```bash
pdf-pro inspect input.pdf
pdf-pro validate output.pdf --render --extract-text --out-dir validation/output
```

Fallback to scripts:

```bash
python scripts/pdf_ops.py inspect input.pdf
python scripts/validate_pdf.py output.pdf --render --extract-text --out-dir validation/output
```

## Safety rules

- Never overwrite source PDFs unless explicitly instructed.
- Write modified files to a new path.
- For redaction, verify both the rendered image and extracted text.
- For visual layouts, render pages and inspect for clipping, overlap, missing glyphs, weak contrast, and bad margins.
- For scanned PDFs, state OCR uncertainty.
- For missing dependencies, report the dependency and install command.

## Delivery format

Report:

1. Commands run.
2. Output file path.
3. Validation completed.
4. Any limitation.


See also `CLI.md` and `references/cli-integration.md`.
