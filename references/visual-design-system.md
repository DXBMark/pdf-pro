# Visual design system for professional PDFs

Use these rules when the PDF must look polished, branded, presentation-ready, or client-facing.

## Design philosophy

Design the page as a communication surface. The document should guide the reader through space, hierarchy, and contrast before they read the details. Use layout to make meaning obvious.

Keep visual decisions systematic. Every colour, line, shadow, border, icon, and chart must have a job. Remove anything that does not improve comprehension or trust.

Prefer quiet confidence over decorative noise. Most professional PDFs benefit from restrained colour, strong alignment, generous spacing, and concise headings.

## Layout system

- Use a grid. Align headings, text blocks, tables, cards, captions, and charts to shared edges.
- Keep margins generous. For A4/Letter documents, use at least 36pt margins; use 48-60pt for premium layouts.
- Use spacing rhythm. Prefer 4/8pt increments for padding, gaps, and section spacing.
- Avoid dense full-width paragraphs. Use 60-85 characters per line for readable body text.
- Break long content into sections with clear headings, callouts, tables, or side notes.
- Keep repeated elements consistent: headers, footers, page numbers, section labels, chart captions.

## Typography

- Use one or two font families. Use weight, size, and spacing for hierarchy.
- Body text should usually be 9.5-11.5pt for print-style PDFs and 12-14pt for screen-first PDFs.
- Use line height around 1.4-1.7 for body text.
- Use tabular figures for data, totals, prices, attendance, dates, and metrics.
- Avoid all-caps body text. Reserve uppercase for small labels only.
- Do not rely on font availability. If custom fonts are unavailable, use safe built-in fonts and maintain hierarchy.

## Colour and accessibility

- Use semantic colour roles: background, foreground, primary, secondary, border, muted, success, warning, destructive.
- Maintain contrast: body text should meet at least 4.5:1 against its background; large headings at least 3:1.
- Do not use colour alone to communicate status. Add text labels, icons, or patterns.
- Use restrained palettes: 2-5 colours are usually enough.
- Check dark backgrounds carefully. Reverse text must be large enough and high contrast.

## Components

### Cover page
- Use one dominant focal element: title, brand mark, key graphic, or strong typographic composition.
- Include only essential metadata: subtitle, author/team, date, version, classification if required.

### Tables
- Align numbers right and text left.
- Keep row height comfortable.
- Use subtle dividers; avoid heavy gridlines unless the table is dense.
- Repeat headers on long tables when possible.
- Add units in headers, not repeated in every cell.

### Charts
- Choose the chart type based on the question:
  - trend: line chart.
  - comparison: bar chart.
  - part-to-whole with fewer than 5 categories: donut or stacked bar.
  - distribution: histogram or box plot.
  - relationship: scatter plot.
- Add direct labels or clear legends.
- Include axis labels and units.
- Do not rely on red/green only.
- Provide a short insight title above the chart.

### Callouts
- Use callouts sparingly for decisions, risks, actions, or key findings.
- Keep callout text short.
- Use consistent border/radius/padding.

### Forms
- Labels must be visible, not placeholder-only.
- Group related fields.
- Add helper text for ambiguous inputs.
- Make signature/date areas clear.
- Keep checkboxes and radio buttons large enough to mark cleanly.

## High-end canvas mode

Use this for posters, visual manifestos, premium one-pagers, and museum-quality visual compositions.

- 90% visual structure, 10% essential text.
- Text acts as a visual element, not a paragraph container.
- Use geometric precision, repetition, negative space, and controlled rhythm.
- Nothing should overlap accidentally or fall off the page.
- Refine existing elements before adding more.
- The final page should look intentionally composed, not assembled.

## Anti-patterns

Avoid:

- Random colours with no semantic purpose.
- Low-contrast grey text.
- Inconsistent margins, card padding, border radius, or shadow depth.
- Decorative gradients that reduce readability.
- Tables pasted as screenshots when editable text is possible.
- Overcrowded pages with no scan path.
- Mixed icon styles.
- Unverified page breaks.
