#!/usr/bin/env python3
"""Small PDF operations helper for the pdf-pro skill.

Supported commands:
  inspect input.pdf
  extract-text input.pdf --out text.txt
  render input.pdf --out-dir renders --dpi 160 [--pages 1,3-5]
  merge output.pdf input1.pdf input2.pdf [...]
  split input.pdf --pages 1-3,7 --out output.pdf
  rotate input.pdf --pages 1,3-5 --angle 90 --out output.pdf
  watermark input.pdf --text "DRAFT" --out output.pdf
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
from pathlib import Path
from typing import Iterable, List, Sequence, Set


def _require(module_name: str):
    try:
        return __import__(module_name)
    except Exception as exc:  # pragma: no cover - environment dependent
        raise SystemExit(f"Missing dependency '{module_name}': {exc}") from exc


def parse_pages(spec: str | None, total: int) -> List[int]:
    if not spec:
        return list(range(total))
    result: Set[int] = set()
    for part in spec.split(','):
        part = part.strip()
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


def inspect_pdf(args: argparse.Namespace) -> None:
    pypdf = _require('pypdf')
    path = Path(args.input)
    reader = pypdf.PdfReader(str(path))
    pages = []
    for i, page in enumerate(reader.pages, start=1):
        mediabox = page.mediabox
        pages.append({
            'page': i,
            'width_pt': float(mediabox.width),
            'height_pt': float(mediabox.height),
            'rotation': int(page.get('/Rotate', 0) or 0),
        })
    info = {
        'file': str(path),
        'exists': path.exists(),
        'size_bytes': path.stat().st_size if path.exists() else None,
        'encrypted': bool(reader.is_encrypted),
        'page_count': len(reader.pages),
        'metadata': {k: str(v) for k, v in (reader.metadata or {}).items()},
        'pages': pages,
    }
    print(json.dumps(info, indent=2))


def extract_text(args: argparse.Namespace) -> None:
    pypdf = _require('pypdf')
    reader = pypdf.PdfReader(args.input)
    selected = parse_pages(args.pages, len(reader.pages))
    chunks = []
    for index in selected:
        text = reader.pages[index].extract_text() or ''
        chunks.append(f"\n\n--- Page {index + 1} ---\n{text}")
    output = ''.join(chunks).strip() + '\n'
    if args.out:
        Path(args.out).write_text(output, encoding='utf-8')
        print(f"Wrote {args.out}")
    else:
        print(output)


def render_pdf(args: argparse.Namespace) -> None:
    fitz = _require('fitz')
    doc = fitz.open(args.input)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    selected = parse_pages(args.pages, doc.page_count)
    zoom = args.dpi / 72.0
    matrix = fitz.Matrix(zoom, zoom)
    written = []
    for index in selected:
        page = doc.load_page(index)
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        out_path = out_dir / f"page-{index + 1:03d}.png"
        pix.save(str(out_path))
        written.append(str(out_path))
    print(json.dumps({'rendered': written, 'dpi': args.dpi}, indent=2))


def merge_pdfs(args: argparse.Namespace) -> None:
    pypdf = _require('pypdf')
    writer = pypdf.PdfWriter()
    for file_path in args.inputs:
        reader = pypdf.PdfReader(file_path)
        for page in reader.pages:
            writer.add_page(page)
    with open(args.output, 'wb') as f:
        writer.write(f)
    print(f"Wrote {args.output}")


def split_pdf(args: argparse.Namespace) -> None:
    pypdf = _require('pypdf')
    reader = pypdf.PdfReader(args.input)
    selected = parse_pages(args.pages, len(reader.pages))
    writer = pypdf.PdfWriter()
    for index in selected:
        writer.add_page(reader.pages[index])
    with open(args.out, 'wb') as f:
        writer.write(f)
    print(f"Wrote {args.out}")


def rotate_pdf(args: argparse.Namespace) -> None:
    pypdf = _require('pypdf')
    if args.angle % 90 != 0:
        raise SystemExit('Angle must be a multiple of 90')
    reader = pypdf.PdfReader(args.input)
    selected = set(parse_pages(args.pages, len(reader.pages)))
    writer = pypdf.PdfWriter()
    for index, page in enumerate(reader.pages):
        if index in selected:
            page.rotate(args.angle)
        writer.add_page(page)
    with open(args.out, 'wb') as f:
        writer.write(f)
    print(f"Wrote {args.out}")


def watermark_pdf(args: argparse.Namespace) -> None:
    pypdf = _require('pypdf')
    reportlab_canvas = _require('reportlab.pdfgen.canvas')
    reportlab_pagesizes = _require('reportlab.lib.pagesizes')
    reportlab_colors = _require('reportlab.lib.colors')
    from io import BytesIO
    from reportlab.pdfgen import canvas
    from reportlab.lib.colors import Color

    reader = pypdf.PdfReader(args.input)
    writer = pypdf.PdfWriter()
    selected = set(parse_pages(args.pages, len(reader.pages))) if args.pages else set(range(len(reader.pages)))

    for index, page in enumerate(reader.pages):
        if index in selected:
            width = float(page.mediabox.width)
            height = float(page.mediabox.height)
            packet = BytesIO()
            c = canvas.Canvas(packet, pagesize=(width, height))
            c.saveState()
            c.translate(width / 2, height / 2)
            c.rotate(args.angle)
            c.setFillColor(Color(0.1, 0.1, 0.1, alpha=args.opacity))
            c.setFont('Helvetica-Bold', args.size)
            c.drawCentredString(0, 0, args.text)
            c.restoreState()
            c.save()
            packet.seek(0)
            overlay = pypdf.PdfReader(packet).pages[0]
            page.merge_page(overlay)
        writer.add_page(page)
    with open(args.out, 'wb') as f:
        writer.write(f)
    print(f"Wrote {args.out}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='PDF operations helper')
    sub = parser.add_subparsers(dest='command', required=True)

    p = sub.add_parser('inspect')
    p.add_argument('input')
    p.set_defaults(func=inspect_pdf)

    p = sub.add_parser('extract-text')
    p.add_argument('input')
    p.add_argument('--pages')
    p.add_argument('--out')
    p.set_defaults(func=extract_text)

    p = sub.add_parser('render')
    p.add_argument('input')
    p.add_argument('--out-dir', required=True)
    p.add_argument('--dpi', type=int, default=160)
    p.add_argument('--pages')
    p.set_defaults(func=render_pdf)

    p = sub.add_parser('merge')
    p.add_argument('output')
    p.add_argument('inputs', nargs='+')
    p.set_defaults(func=merge_pdfs)

    p = sub.add_parser('split')
    p.add_argument('input')
    p.add_argument('--pages', required=True)
    p.add_argument('--out', required=True)
    p.set_defaults(func=split_pdf)

    p = sub.add_parser('rotate')
    p.add_argument('input')
    p.add_argument('--pages')
    p.add_argument('--angle', type=int, required=True)
    p.add_argument('--out', required=True)
    p.set_defaults(func=rotate_pdf)

    p = sub.add_parser('watermark')
    p.add_argument('input')
    p.add_argument('--text', required=True)
    p.add_argument('--out', required=True)
    p.add_argument('--pages')
    p.add_argument('--angle', type=float, default=35)
    p.add_argument('--opacity', type=float, default=0.12)
    p.add_argument('--size', type=int, default=72)
    p.set_defaults(func=watermark_pdf)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
