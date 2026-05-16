# PDF Validation Protocol

Use this protocol before telling the user that a PDF is final, correct, ready, fixed, redacted, merged, split, or visually polished.

## Minimum validation

Always confirm these points:

1. The output file exists.
2. The PDF opens without parser errors.
3. The page count matches the requested output.
4. Page size, orientation, and rotation are intentional.
5. The output file size is reasonable for the content.
6. Any user-requested operation is reflected in the final file.

Recommended command:

```bash
python scripts/validate_pdf.py output.pdf
```

With an expected page count:

```bash
python scripts/validate_pdf.py output.pdf --expected-pages 5
```

## Visual validation

Use visual validation when the user asks for design, layout, branding, forms, tables, charts, posters, certificates, one-pagers, handouts, scanned pages, redactions, stamps, signatures, or page-level changes.

Recommended command:

```bash
python scripts/validate_pdf.py output.pdf --render --out-dir validation/output --dpi 160
```

Check rendered PNG files for:

- clipped text
- overlapping objects
- missing glyphs
- broken images
- incorrect page order
- weak hierarchy
- poor contrast
- margins that are too tight
- headers, footers, tables, and charts crossing page boundaries
- watermarks covering important content
- redaction marks that do not fully cover the intended visual region

## Text-layer validation

Use text-layer validation when the PDF must be searchable, copyable, accessible, or properly redacted.

Recommended command:

```bash
python scripts/validate_pdf.py output.pdf --extract-text --text-out validation/output.txt
```

Check:

- whether text extraction returns meaningful text
- whether expected phrases appear
- whether removed or redacted sensitive text is absent
- whether page ordering in extracted text is correct
- whether scanned pages are correctly identified as having limited or no text layer

## Redaction validation

For true redaction, never rely only on drawing a black box, white box, or shape over text.

A valid redaction workflow must verify both:

1. Visual layer: the sensitive content is not visible in rendered pages.
2. Text layer: the sensitive content cannot be extracted from the PDF.

Recommended checks:

```bash
python scripts/validate_pdf.py redacted.pdf --render --extract-text --text-out validation/redacted.txt
```

Then search the extracted text for the sensitive terms. If any sensitive term remains, the PDF is not safely redacted.

## Merge, split, and rotation validation

For merge operations:

- confirm final page count equals the sum of included pages
- render the first page of each source boundary when practical
- confirm bookmarks or metadata limitations if relevant

For split operations:

- confirm selected pages match the requested page range
- confirm no unrequested pages remain

For rotation operations:

- inspect rotation metadata
- render affected pages to confirm orientation visually

## Form validation

For PDF forms:

- confirm fields are filled with the intended values
- confirm whether the form should remain editable or be flattened
- render final pages to check field overflow and alignment
- avoid claiming a form is flattened unless verified

## Accessibility and design validation

For professional visual PDFs:

- use readable type size
- preserve adequate foreground/background contrast
- avoid colour-only meaning
- label charts clearly
- use consistent spacing, alignment, and page rhythm
- verify page renders at the target size

## Final response requirement

When delivering a finished PDF, include:

1. The file link.
2. A brief summary of what was created or changed.
3. What validation was completed.
4. Any limitations, such as scanned pages, OCR uncertainty, missing fonts, unavailable source files, or third-party service dependency.


## Package validation

For repository or release validation, run:

```bash
python scripts/validate_package.py .
python -m compileall scripts src
```

If installed as a package, also run:

```bash
pdf-pro --help
pdf-pro validate --help
```

## CLI validation

For CLI-generated PDFs, include the command used and the validation result in the delivery summary. Prefer writing validation outputs to `validation/<document-name>/`.

Recommended pattern:

```bash
pdf-pro inspect input.pdf
pdf-pro <operation> input.pdf --out output.pdf
pdf-pro validate output.pdf --render --extract-text --out-dir validation/output --text-out validation/output.txt
```
