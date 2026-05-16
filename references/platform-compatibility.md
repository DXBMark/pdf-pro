# Platform compatibility

PDF Pro is designed to work as a direct ChatGPT Skill and as an adaptable workflow package for other assistants and coding agents.

## Direct support

### ChatGPT Skills

Use the root `SKILL.md` file as the main instruction entrypoint. Keep `agents/openai.yaml`, `assets/pdf.png`, `references/`, and `scripts/` in place.

## Adaptable support

### Claude Skills

Use `CLAUDE.md` or `platforms/claude.md` as the entrypoint. The root `SKILL.md` remains useful as workflow guidance, but Claude-specific instructions should avoid assuming OpenAI-only metadata.

### Claude Code

Use `AGENTS.md`, `CLI.md`, and the scripts or installed CLI.

### Gemini Gems

Use `GEMINI.md` or `platforms/gemini.md` as instruction material. Attach the reference files as supporting knowledge where supported.

### VSCode, Copilot, Antigravity, and local coding agents

Use the CLI route. Load `AGENTS.md`, `CLI.md`, and `references/cli-integration.md` into the agent context where practical.

## Compatibility boundaries

- If a platform cannot execute code, provide terminal commands rather than claiming the operation was performed.
- If a platform cannot access local files, ask the user to upload files or run commands locally.
- If a platform cannot render PDFs, validate with inspection and state that visual verification still needs local rendering.
- Do not claim true redaction unless text-layer and visual validation have both passed.
