# PDF Pro

PDF Pro is a ChatGPT Skill for professional PDF creation, editing, inspection, extraction, visual review, and presentation-quality PDF layout work.

It is designed for workflows where the final PDF must be usable, visually checked, and ready to share. The skill combines PDF operations with structured design guidance inspired by UI/UX Pro Max.

## Author and licence

- Author: Tariq Said
- Licence: MIT
- UI/UX Design Inspiration: UI/UX Pro Max by NextLevelBuilder, MIT License

See `LICENSE` and `NOTICE.md` for the complete licence and attribution details.

## What this skill supports

- Create new PDFs from structured content.
- Edit existing PDFs through safe operations such as merge, split, rotate, watermark, and extraction.
- Review PDFs by inspecting metadata, page count, encryption status, page sizes, and text layer availability.
- Render PDF pages to PNG for visual verification.
- Extract text from selectable-text PDFs.
- Apply professional visual design rules for client-facing PDFs, handouts, reports, one-pagers, certificates, dashboards, and branded documents.
- Use a validation protocol before delivery.

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

## Main entry point

`SKILL.md` is the primary instruction file used by ChatGPT. It defines when the skill should be used and how PDF work should be handled.

## Helper scripts

Run scripts from inside the `pdf-pro` folder, or pass absolute paths.

### Inspect a PDF

```bash
python scripts/pdf_ops.py inspect input.pdf
```

### Extract text

```bash
python scripts/pdf_ops.py extract-text input.pdf --out extracted.txt
```

### Render pages for visual review

```bash
python scripts/pdf_ops.py render input.pdf --out-dir renders/input --dpi 160
```

### Merge PDFs

```bash
python scripts/pdf_ops.py merge output.pdf first.pdf second.pdf
```

### Split pages

```bash
python scripts/pdf_ops.py split input.pdf --pages 1-3,7 --out selected-pages.pdf
```

### Rotate pages

```bash
python scripts/pdf_ops.py rotate input.pdf --pages 1,3-5 --angle 90 --out rotated.pdf
```

### Add a watermark

```bash
python scripts/pdf_ops.py watermark input.pdf --text "DRAFT" --out watermarked.pdf
```

### Validate a finished PDF

```bash
python scripts/validate_pdf.py output.pdf --expected-pages 5 --render --out-dir validation/output
```

The validation script checks whether the file exists, opens successfully, has the expected page count when provided, exposes page dimensions and rotation, optionally extracts text statistics, and optionally renders pages for visual review.

## External dependencies

The helper scripts may use common Python PDF packages depending on the operation:

- `pypdf` for metadata inspection, splitting, merging, rotation, watermark composition, and text extraction.
- `PyMuPDF` imported as `fitz` for rendering PDF pages to images.
- `reportlab` for fixed-layout PDF creation and watermark generation.

The skill does not bundle these third-party libraries. Install them in the execution environment when required:

```bash
python -m pip install pypdf pymupdf reportlab
```

## Validation standard

Before a final PDF is delivered, verify at minimum:

1. The output file exists and opens.
2. The page count is correct.
3. Page sizes and rotations are intentional.
4. Text extraction is checked when text layer accuracy matters.
5. Visual renders are checked for clipping, overlap, missing glyphs, weak contrast, and layout errors.
6. Any limitation is stated clearly, especially scanned pages, OCR uncertainty, missing fonts, or source-file quality issues.

See `references/validation-protocol.md` for the full protocol.

## Attribution note

This skill includes original PDF workflow instructions authored for this package. Its visual design guidance is inspired by UI/UX Pro Max by NextLevelBuilder, which is identified by the user as MIT-licensed. This package does not claim ownership of UI/UX Pro Max.
