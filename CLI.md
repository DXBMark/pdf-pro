# PDF Pro CLI

PDF Pro includes standalone Python scripts and an installable CLI entrypoint.

## Install

```bash
python -m pip install -e .[pdf]
```

## Commands

```bash
pdf-pro inspect input.pdf
pdf-pro extract-text input.pdf --out extracted.txt
pdf-pro render input.pdf --out-dir renders/input --dpi 160
pdf-pro merge output.pdf first.pdf second.pdf
pdf-pro split input.pdf --pages 1-3,7 --out selected-pages.pdf
pdf-pro rotate input.pdf --pages 1,3-5 --angle 90 --out rotated.pdf
pdf-pro crop input.pdf --box 36,36,559,806 --out cropped.pdf
pdf-pro watermark input.pdf --text "DRAFT" --out watermarked.pdf
pdf-pro redact input.pdf --text "Confidential" --out redacted.pdf
pdf-pro validate output.pdf --render --out-dir validation/output
pdf-pro visual examples/visual-spec.json --out output.pdf
```

## Script fallback

If the package is not installed, use scripts directly:

```bash
python scripts/pdf_ops.py inspect input.pdf
python scripts/validate_pdf.py output.pdf --render --out-dir validation/output
python scripts/create_visual_pdf.py examples/visual-spec.json --out output.pdf
```

## Recommended output folders

- `outputs/` for generated PDFs.
- `renders/` for page PNGs.
- `validation/` for validation renders, extracted text, and reports.

## Editor support

- VSCode: use `.vscode/tasks.json` or the integrated terminal.
- Claude Code: read `AGENTS.md`, then run CLI commands.
- Copilot: ask it to follow `AGENTS.md` and validate outputs.
- Antigravity: use the same CLI commands and validation protocol.
