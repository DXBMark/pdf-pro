#!/usr/bin/env python3
"""Validate PDF Pro repository and skill package structure."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List

REQUIRED_FILES = [
    'SKILL.md',
    'README.md',
    'LICENSE',
    'NOTICE.md',
    'AGENTS.md',
    'CLAUDE.md',
    'GEMINI.md',
    'CLI.md',
    'pyproject.toml',
    'agents/openai.yaml',
    'assets/pdf.png',
    'assets/design-tokens-starter.json',
    'references/pdf-workflows.md',
    'references/quality-checklist.md',
    'references/validation-protocol.md',
    'references/visual-design-system.md',
    'references/cli-integration.md',
    'references/platform-compatibility.md',
    'references/compatibility-checklist.md',
    'platforms/chatgpt.md',
    'platforms/claude.md',
    'platforms/gemini.md',
    'platforms/cli-agents.md',
    'scripts/pdf_ops.py',
    'scripts/validate_pdf.py',
    'scripts/create_visual_pdf.py',
    'scripts/validate_package.py',
    'src/pdf_pro/__init__.py',
    'src/pdf_pro/cli.py',
    'src/pdf_pro/pdf_ops.py',
    'src/pdf_pro/validate_pdf.py',
    'src/pdf_pro/create_visual_pdf.py',
]


def parse_frontmatter(text: str) -> Dict[str, str]:
    match = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
    if not match:
        raise ValueError('SKILL.md does not start with YAML frontmatter')
    result: Dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ':' in line:
            key, value = line.split(':', 1)
            result[key.strip()] = value.strip()
    return result


def validate(root: Path) -> Dict[str, object]:
    errors: List[str] = []
    warnings: List[str] = []
    checks: List[str] = []

    for rel in REQUIRED_FILES:
        path = root / rel
        if not path.exists():
            errors.append(f'Missing required file: {rel}')
        else:
            checks.append(f'Found {rel}')

    skill_md = root / 'SKILL.md'
    if skill_md.exists():
        try:
            fm = parse_frontmatter(skill_md.read_text(encoding='utf-8'))
            name = fm.get('name')
            description = fm.get('description')
            if name != 'pdf-pro':
                errors.append("SKILL.md name must be 'pdf-pro'")
            if not description:
                errors.append('SKILL.md description is missing')
            elif len(description) > 1024:
                errors.append('SKILL.md description exceeds 1024 characters')
            checks.append('SKILL.md frontmatter parsed')
        except Exception as exc:
            errors.append(str(exc))

    readme = root / 'README.md'
    if readme.exists():
        content = readme.read_text(encoding='utf-8')
        if 'Suggested GitHub topics' in content:
            warnings.append('README.md contains Suggested GitHub topics; prefer GitHub About topics instead')
        for rel in ['LICENSE', 'NOTICE.md', 'SKILL.md', 'CLAUDE.md', 'GEMINI.md', 'CLI.md']:
            if f']({rel})' not in content and rel in ['LICENSE', 'NOTICE.md']:
                warnings.append(f'README may not link {rel} interactively')

    return {
        'valid': not errors,
        'errors': errors,
        'warnings': warnings,
        'checks': checks,
        'required_file_count': len(REQUIRED_FILES),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description='Validate PDF Pro repository structure')
    parser.add_argument('path', nargs='?', default='.', help='Repository root path')
    parser.add_argument('--json-out', help='Optional path for JSON report')
    args = parser.parse_args()

    report = validate(Path(args.path).resolve())
    if args.json_out:
        out = Path(args.json_out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report['valid'] else 1)


if __name__ == '__main__':
    main()
