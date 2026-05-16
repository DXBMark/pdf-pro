---
name: pdf-pro
description: professional pdf creation, editing, review, conversion, extraction, visual verification, forms, redaction, cli automation, and presentation-quality layout design. use when chatgpt needs to create a new pdf, modify an existing pdf, inspect or summarize a pdf, extract text/tables/images, combine/split/rotate/crop/watermark pages, fill or flatten forms, redact content, convert documents to pdf, validate outputs, or improve the visual design of a pdf using ui/ux and design-system guidance.
---

# PDF Pro

Use this skill to handle PDF work as a verified production workflow, not a one-step file operation. Prioritise accuracy, visual verification, safe PDF operations, and clean design.

## Core operating rule

Always use this loop unless the user only asks for a high-level explanation:

1. Identify the PDF task: create, review, extract, edit, convert, redact, form-fill, visual redesign, or CLI automation.
2. Choose the safest authoring path:
   - Text-heavy reports, policies, letters, and long documents: author in DOCX or Markdown first, then convert to PDF when tooling supports it.
   - Slide-like layouts, posters, one-pagers, certificates, dashboards, and visual reports: use fixed-layout PDF creation or slide authoring, then export and verify.
   - Existing PDF edits: inspect and render pages before editing when layout matters.
   - CLI/automation tasks: use the bundled scripts or the `pdf-pro` CLI interface when the package is installed.
3. Inspect or render the input before changing it when working with an existing PDF.
4. Perform the smallest safe operation that satisfies the request.
5. Re-render or inspect the output.
6. Validate the final PDF using `scripts/validate_pdf.py` when a file is produced or modified.
7. Deliver the final PDF plus a short summary of what changed, what was verified, and any limitations.

Never claim a PDF is correct without checking the output file exists and can be opened or inspected. For final deliverables, follow `references/validation-protocol.md` and record any limitation clearly.

## Bundled helpers

Use these scripts when they fit the task. Run scripts from inside the skill folder or pass absolute paths.

- `scripts/pdf_ops.py`: inspect, merge, split, rotate, crop, watermark, redact text, extract text, and render pages to PNG for verification.
- `scripts/create_visual_pdf.py`: generate a polished PDF from a JSON content specification using design tokens.
- `scripts/validate_pdf.py`: validate a final PDF by checking file existence, parser readability, page count, optional text extraction, forbidden/required phrases, and optional page renders.
- `scripts/validate_package.py`: validate that the repository contains the expected skill, platform, CLI, script, reference, and asset files.
- `README.md`: user and maintainer documentation, including ownership, licence, dependencies, platform compatibility, CLI usage, and examples.
- `LICENSE`: MIT licence for PDF Pro.
- `NOTICE.md`: attribution and third-party dependency notices, including UI/UX Pro Max by NextLevelBuilder.
- `references/pdf-workflows.md`: exact workflows for creation, editing, extraction, forms, redaction, conversion, and verification.
- `references/visual-design-system.md`: UI/UX Pro Max inspired design rules for high-quality PDF layouts.
- `references/quality-checklist.md`: final QA checklist before delivery.
- `references/validation-protocol.md`: formal verification rules for final PDF outputs.
- `references/cli-integration.md`: CLI and editor integration guidance for VSCode, Antigravity, Claude Code, Copilot, and other coding agents.
- `references/platform-compatibility.md`: platform-specific usage guidance for ChatGPT Skills, Claude Skills, Gemini Gems, CLI agents, and local LLM workflows.
- `references/compatibility-checklist.md`: checklist for release validation across supported targets.
- `assets/design-tokens-starter.json`: reusable colour, spacing, type, radius, and shadow tokens.
- `assets/pdf.png`: skill icon.

## Creation workflow

For a new PDF:

1. Decide the output type: report, handout, visual one-pager, packet, form, certificate, invoice, worksheet, dashboard, or portfolio.
2. Load `references/visual-design-system.md` when the user expects professional visual design, branding, layout polish, colour palette, typography, charts, or a PDF that should look presentation-ready.
3. Use `scripts/create_visual_pdf.py` for quick fixed-layout PDFs from structured JSON, or use a richer document/slide workflow when the content is complex.
4. Render the finished PDF using `scripts/pdf_ops.py render` and check the images for clipped text, overlaps, broken glyphs, poor margins, and weak hierarchy.
5. Validate the finished file with `scripts/validate_pdf.py`. Use `--render` for visual or client-facing PDFs.
6. If the PDF is visual or client-facing, run the final review against `references/quality-checklist.md`.

Default visual standard: restrained, readable, accessible, and polished. Avoid decoration that makes the document harder to scan.

## Editing workflow

For an existing PDF:

1. Inspect first:
   ```bash
   python scripts/pdf_ops.py inspect input.pdf
   ```
2. Render pages when layout matters:
   ```bash
   python scripts/pdf_ops.py render input.pdf --out-dir renders/input --dpi 160
   ```
3. Apply the smallest safe edit: merge, split, rotate, crop, watermark, extraction, form filling, or redaction-specific workflow.
4. Inspect and render the output.
5. Summarise exactly which pages changed.

For true redaction, never cover text with a black rectangle only. Use a redaction-capable workflow that removes underlying text or pixels, then verify by text extraction and rendering.

## Review and extraction workflow

For review, summary, or extraction:

1. Inspect the file metadata, page count, encryption status, and text availability.
2. Extract text when the PDF has a text layer.
3. Render pages when the user asks about visual layout, diagrams, tables, charts, signatures, scans, stamps, screenshots, or placement.
4. Flag OCR uncertainty for scanned pages. Do not overstate confidence when the text layer is missing or poor.
5. For tables, compare extracted data with page renders when accuracy matters.

## UI/UX Pro Max integration

Use design-system thinking for any PDF with a visible layout. Apply these priorities:

1. Accessibility: readable type, sufficient contrast, clear hierarchy, labelled charts, and no colour-only meaning.
2. Layout: consistent grid, generous margins, aligned edges, predictable spacing, and no horizontal crowding.
3. Typography: limited font families, clear scale, line height around 1.4-1.7 for body copy, and tabular figures for data.
4. Colour: semantic palette with primary, secondary, background, foreground, border, muted, success, warning, and destructive tokens.
5. Visual polish: restrained shadows, consistent radius, intentional whitespace, and chart choices matched to the data.
6. Verification: render and inspect the PDF as images before delivery.

For premium visual PDFs, treat text as part of the composition. Use short headings, clear callouts, and purposeful visual rhythm instead of dense paragraphs.

## CLI and agent integration

When the package is installed locally, the same helpers can be called with the `pdf-pro` command:

```bash
pdf-pro inspect input.pdf
pdf-pro render input.pdf --out-dir renders/input --dpi 160
pdf-pro validate output.pdf --render --out-dir validation/output
pdf-pro visual examples/visual-spec.json --out output.pdf
```

For VSCode, Antigravity, Claude Code, Copilot, and other coding agents, load `AGENTS.md`, `CLI.md`, and `references/cli-integration.md` when the user asks for editor automation, terminal workflows, package installation, or repository integration.

## Platform compatibility

Use this package directly as a ChatGPT Skill. For Claude Skills, Claude Code, Gemini Gems, Copilot, Antigravity, and local agent workflows, use the platform notes in `CLAUDE.md`, `GEMINI.md`, `AGENTS.md`, `CLI.md`, and `platforms/`.

Do not overclaim a platform feature. If the target assistant cannot execute code, provide the commands for a local terminal or coding-agent environment instead.

## Response format after completion

Use this structure in the final message when a PDF is created or edited:

- State the output file link.
- Summarise the main changes or contents.
- State what verification was completed.
- Mention limitations only when relevant, such as missing fonts, scanned pages, OCR uncertainty, password protection, unavailable source files, or third-party dependency limits.

Keep the user-facing summary concise. Do not expose internal script logs unless the user asks.
