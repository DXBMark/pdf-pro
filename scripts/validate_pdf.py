#!/usr/bin/env python3
"""Validate PDF outputs for the pdf-pro skill.

Checks that a PDF exists, opens, has expected page properties, optionally extracts
text, and optionally renders pages for visual review.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set


def _require(module_name: str):
    try:
        return __import__(module_name)
    except Exception as exc:
        raise SystemExit(f"Missing dependency '{module_name}': {exc}") from exc


def parse_pages(spec: Optional[str], total: int) -> List[int]:
    if not spec:
        return list(range(total))
    result: Set[int] = set()
    for raw_part in spec.split(','):
        part = raw_part.strip()
        if not part:
            continue
        if '-' in part:
            start_s, end_s = part.split('-', 1)
            start, end = int(start_s), int(end_s)
            if start < 1 or end > total or start > end:
                raise SystemExit(f"Invalid page range '{part}' for {total} pages")
            result.update(range(start - 1, end))
        else:
            page = int(part)
            if page < 1 or page > total:
                raise SystemExit(f"Invalid page '{part}' for {total} pages")
            result.add(page - 1)
    return sorted(result)


def inspect_with_pypdf(path: Path) -> Dict[str, Any]:
    pypdf = _require('pypdf')
    reader = pypdf.PdfReader(str(path))
    pages: List[Dict[str, Any]] = []
    for i, page in enumerate(reader.pages, start=1):
        mediabox = page.mediabox
        pages.append({
            'page': i,
            'width_pt': float(mediabox.width),
            'height_pt': float(mediabox.height),
            'rotation': int(page.get('/Rotate', 0) or 0),
        })
    return {
        'encrypted': bool(reader.is_encrypted),
        'page_count': len(reader.pages),
        'metadata': {k: str(v) for k, v in (reader.metadata or {}).items()},
        'pages': pages,
        '_reader': reader,
    }


def render_pages(path: Path, out_dir: Path, dpi: int, pages_spec: Optional[str], total_pages: int) -> Dict[str, Any]:
    fitz = _require('fitz')
    doc = fitz.open(str(path))
    selected = parse_pages(pages_spec, total_pages)
    out_dir.mkdir(parents=True, exist_ok=True)
    zoom = dpi / 72.0
    matrix = fitz.Matrix(zoom, zoom)
    rendered: List[str] = []
    for index in selected:
        page = doc.load_page(index)
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        out_path = out_dir / f'page-{index + 1:03d}.png'
        pix.save(str(out_path))
        rendered.append(str(out_path))
    return {'dpi': dpi, 'rendered_pages': rendered}


def extract_text(reader: Any, pages_spec: Optional[str], text_out: Optional[Path]) -> Dict[str, Any]:
    total = len(reader.pages)
    selected = parse_pages(pages_spec, total)
    chunks: List[str] = []
    per_page: List[Dict[str, Any]] = []
    for index in selected:
        text = reader.pages[index].extract_text() or ''
        chunks.append(f"\n\n--- Page {index + 1} ---\n{text}")
        per_page.append({
            'page': index + 1,
            'characters': len(text),
            'has_text': bool(text.strip()),
        })
    combined = ''.join(chunks).strip() + '\n'
    if text_out:
        text_out.parent.mkdir(parents=True, exist_ok=True)
        text_out.write_text(combined, encoding='utf-8')
    return {
        'pages_checked': per_page,
        'total_characters': sum(item['characters'] for item in per_page),
        'text_output': str(text_out) if text_out else None,
    }


def validate(args: argparse.Namespace) -> int:
    path = Path(args.input)
    report: Dict[str, Any] = {
        'file': str(path),
        'exists': path.exists(),
        'valid': False,
        'checks': [],
        'warnings': [],
        'errors': [],
    }

    if not path.exists():
        report['errors'].append('File does not exist.')
        print(json.dumps(report, indent=2))
        return 2

    report['size_bytes'] = path.stat().st_size

    try:
        info = inspect_with_pypdf(path)
    except Exception as exc:
        report['errors'].append(f'Could not open or parse PDF: {exc}')
        print(json.dumps(report, indent=2))
        return 2

    reader = info.pop('_reader')
    report.update(info)
    report['checks'].append('PDF opens and basic page metadata was read.')

    if args.expected_pages is not None:
        if report['page_count'] == args.expected_pages:
            report['checks'].append(f'Page count matches expected value: {args.expected_pages}.')
        else:
            report['errors'].append(
                f"Page count mismatch: expected {args.expected_pages}, got {report['page_count']}."
            )

    if report.get('encrypted'):
        report['warnings'].append('PDF is encrypted; some operations may be limited.')

    if args.extract_text:
        try:
            report['text_check'] = extract_text(reader, args.pages, Path(args.text_out) if args.text_out else None)
            report['checks'].append('Text extraction check completed.')
            if report['text_check']['total_characters'] == 0:
                report['warnings'].append('No extractable text found in checked pages. This may be a scanned or image-only PDF.')
        except Exception as exc:
            report['errors'].append(f'Text extraction failed: {exc}')

    if args.render:
        try:
            out_dir = Path(args.out_dir or 'validation-renders')
            report['render_check'] = render_pages(path, out_dir, args.dpi, args.pages, report['page_count'])
            report['checks'].append('Render check completed. Inspect rendered PNG files visually.')
        except Exception as exc:
            report['errors'].append(f'Render check failed: {exc}')

    report['valid'] = len(report['errors']) == 0
    print(json.dumps(report, indent=2))
    return 0 if report['valid'] else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Validate a PDF output file.')
    parser.add_argument('input', help='PDF file to validate')
    parser.add_argument('--expected-pages', type=int, help='Expected page count')
    parser.add_argument('--pages', help='Pages to render or extract, e.g. 1,3-5')
    parser.add_argument('--render', action='store_true', help='Render selected pages to PNG files')
    parser.add_argument('--out-dir', help='Directory for rendered page images')
    parser.add_argument('--dpi', type=int, default=160, help='Render DPI')
    parser.add_argument('--extract-text', action='store_true', help='Run text extraction check')
    parser.add_argument('--text-out', help='Optional path for extracted text output')
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    raise SystemExit(validate(args))


if __name__ == '__main__':
    main()
