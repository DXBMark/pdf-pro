# CLI and editor integration

PDF Pro can be used from the terminal, VSCode tasks, Claude Code, GitHub Copilot, Antigravity, and other coding-agent environments.

## Install locally

```bash
python -m pip install -e .[pdf]
```

## Command pattern

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
pdf-pro validate output.pdf --render --extract-text --out-dir validation/output
pdf-pro visual examples/visual-spec.json --out output.pdf
```

## VSCode

Use `.vscode/tasks.json` or the integrated terminal. Recommended tasks include package validation, PDF validation, render, and visual PDF generation.

## Claude Code

Ask Claude Code to inspect `AGENTS.md`, then run the required `pdf-pro` or `python scripts/...` commands. Require it to show validation output before claiming completion.

## Copilot

Use Copilot Chat with explicit terminal commands. Keep source PDFs immutable and generate new outputs.

## Antigravity

Use the same local CLI commands. Ask the agent to follow `AGENTS.md` and `references/validation-protocol.md`.

## Output discipline

- Put generated PDFs in `outputs/` or a user-specified path.
- Put renders in `validation/<job-name>/renders/`.
- Put extracted text in `validation/<job-name>/text.txt`.
- Put validation JSON in `validation/<job-name>/report.json` when using `--json-out`.
