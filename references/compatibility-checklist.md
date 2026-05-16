# Compatibility checklist

Use this checklist before publishing a release or claiming multi-platform readiness.

## ChatGPT Skill

- `SKILL.md` exists at the repository root.
- Frontmatter contains only supported fields and valid lowercase hyphen-case `name`.
- `agents/openai.yaml` exists.
- Icon exists at `assets/pdf.png`.
- Helper scripts referenced in `SKILL.md` exist.
- Reference files referenced in `SKILL.md` exist.

## Claude Skills and Claude Code

- `CLAUDE.md` exists.
- `platforms/claude.md` exists.
- Instructions do not rely on OpenAI-only metadata.
- Claude is told to use the same scripts and validation protocol.

## Gemini Gems

- `GEMINI.md` exists.
- `platforms/gemini.md` exists.
- Instructions explain how to use references as uploaded knowledge.
- Code execution limits are stated clearly.

## CLI and coding agents

- `CLI.md` exists.
- `AGENTS.md` exists.
- `pyproject.toml` exposes `pdf-pro = pdf_pro.cli:main`.
- `src/pdf_pro/cli.py` exists.
- Script wrappers in `scripts/` work without package installation.
- `.vscode/tasks.json` exists.

## Validation

Run:

```bash
python scripts/validate_package.py .
python -m compileall scripts src
python scripts/pdf_ops.py --help
python scripts/validate_pdf.py --help
python scripts/create_visual_pdf.py --help
```

If installed:

```bash
pdf-pro --help
pdf-pro validate --help
```
