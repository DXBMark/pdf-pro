# PDF workflows

## 1. New PDF creation

Use this route when the user wants a new PDF, report, packet, guide, handout, worksheet, dashboard export, certificate, poster, or branded one-pager.

1. Clarify only missing essentials: page size, audience, content, brand constraints, and required output format.
2. Select layout type:
   - Document layout: heading hierarchy, paragraphs, tables, references, page numbers.
   - Visual layout: cover page, cards, callouts, charts, diagrams, hero sections.
   - Form layout: labelled fields, clear grouping, instructions, signature/date areas.
3. Build content first. Do not start with decoration.
4. Apply design tokens: semantic colours, typography scale, spacing rhythm, consistent borders/radius.
5. Generate the PDF.
6. Render to PNG and inspect visually before delivery.

## 2. Existing PDF edits

Use the smallest safe edit. Preserve original page sizes unless the user asks otherwise.

1. Inspect metadata and page count.
2. Render before editing if the task affects layout or visual appearance.
3. Apply edit:
   - merge: combine files in requested order.
   - split: preserve selected page ranges.
   - rotate: rotate selected pages only.
   - watermark: add transparent text or label without covering critical content.
   - crop: verify coordinates and avoid cutting headers, footers, signatures, or page numbers.
4. Render the output and compare visually with the intended change.

## 3. Review and summarisation

1. Inspect for text layer, page count, encryption, metadata, and attachments.
2. Extract text where available.
3. Render pages when the user asks about appearance, layout quality, tables, charts, diagrams, signatures, handwriting, or scans.
4. Summarise by section, not by arbitrary page count, when the document has headings.
5. Include uncertainty where the file is scanned, low-resolution, partially corrupt, password-protected, or lacks a reliable text layer.

## 4. Extraction

Use the right extraction route:

- Text: text layer extraction first.
- Tables: combine text extraction with visual verification when values matter.
- Images: extract original embedded images if available; otherwise render page regions.
- Forms: list fields, types, options, default values, and current values.
- Attachments: identify embedded files and export only when requested.

## 5. Forms

For fillable forms:

1. Inspect field names and field types.
2. Map user-provided values to exact field names.
3. Fill the form.
4. Flatten only when requested or when appearance streams are unreliable.
5. Render and verify completed fields are visible.

For non-fillable forms:

1. Render the page.
2. Identify text boxes or checkboxes by coordinates.
3. Stamp text or marks into the correct boxes.
4. Render again and verify placement.

## 6. Redaction

True redaction must remove content, not hide it.

1. Identify exact text, region, or page objects to redact.
2. Apply redaction using a redaction-capable PDF library or rasterise-and-rebuild when necessary.
3. Verify by extracting text from the output and checking the redacted content is absent.
4. Render visually to ensure redaction marks appear clean and no sensitive content remains visible.

## 7. Conversion

Prefer source-native authoring when possible:

- DOCX to PDF for long reports and text-heavy business documents.
- PPTX to PDF for slide-like, visual, and presentation layouts.
- HTML to PDF for web-styled documents with CSS control.
- ReportLab/fixed-layout generation for deterministic programmatic documents.

Always inspect the converted PDF for page breaks, missing fonts, glyph issues, and clipped text.
