# Gemini Usage Notes

PDF Pro can be adapted for Gemini Gems by using this repository as a structured instruction and reference package.

## Recommended Gemini setup

1. Use `SKILL.md` as the main workflow guidance.
2. Add files from `references/` as supporting knowledge.
3. Add `README.md` as the public overview.
4. Use `GEMINI.md` or `platforms/gemini.md` as the Gemini-specific instruction note.
5. Run scripts manually in a local Python environment when PDF operations are required.

## Operating workflow

Gemini should follow the same production process:

- Identify the PDF task.
- Inspect the input.
- Perform the smallest safe operation.
- Render or inspect the result.
- Validate before delivery.
- Clearly state limitations.

## Execution limits

If Gemini cannot execute local code or access files, it should provide exact commands for the user or a coding agent to run locally.

Do not claim a PDF has been changed, validated, rendered, or redacted unless the operation was actually executed and checked.
