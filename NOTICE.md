# Notices and Third-Party Attribution

## PDF Pro

- Author: Tariq Said
- Licence: MIT
- Copyright: Copyright (c) 2026 Tariq Said

PDF Pro is a ChatGPT Skill for creating, editing, reviewing, validating, and visually improving PDF files.

## UI/UX design inspiration

This skill's visual design guidance is inspired by:

- UI/UX Pro Max
- Author: NextLevelBuilder
- Licence: MIT
- Homepage: https://uupm.cc
- Repository: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill

The design-system ideas in this package are adapted as workflow guidance for PDF layout quality, accessibility, visual hierarchy, colour tokens, typography, spacing, and final review. This package does not claim ownership of UI/UX Pro Max or its upstream project.

## Bundled assets

- `assets/pdf.png` is included as the PDF Skill icon supplied for this package.
- `assets/design-tokens-starter.json` is included as a reusable design-token starter for PDF visual production.

## Runtime dependencies

Some scripts can use third-party Python libraries when available in the execution environment:

- `pypdf`
- `PyMuPDF` / `fitz`
- `reportlab`

These libraries are not bundled inside this skill. Their own licences apply when installed separately by the user or runtime environment.

## Responsibility for external services

When using external tools, APIs, converters, OCR services, storage services, or hosted fonts as part of a PDF task, ChatGPT should:

1. Identify the external service or dependency.
2. Avoid sending sensitive documents to external services unless the user has clearly requested or approved that workflow.
3. Mention any dependency-specific limitation that may affect the output.
4. Preserve attribution and licence notices when third-party assets, templates, fonts, icons, images, or design systems are used.
5. Prefer local/offline processing for confidential PDF content when practical.
