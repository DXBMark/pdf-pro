#!/usr/bin/env python3
"""PDF operations helper for PDF Pro.

Supported commands:
  inspect input.pdf
  extract-text input.pdf --out text.txt
  render input.pdf --out-dir renders --dpi 160 [--pages 1,3-5]
  merge output.pdf input1.pdf input2.pdf [...]
  split input.pdf --pages 1-3,7 --out output.pdf
  rotate input.pdf --pages 1,3-5 --angle 90 --out output.pdf
  crop input.pdf --box left,bottom,right,top --out output.pdf [--pages 1,3-5]
  watermark input.pdf --text "DRAFT" --out output.pdf
  redact input.pdf --text "Secret" --out redacted.pdf [--pages 1,3-5]
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


def _require(module_name: str):
    try:
        return __import__(module_name)
    except Exception as exc:  # pragma: no cover - environment dependent
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


def parse_box(value: str) -> Tuple[float, float, float, float]:
    try:
        parts = [float(p.strip()) for p in value.split(',')]
    except ValueError as exc:
        raise SystemExit('Box must contain numeric values: left,bottom,right,top') from exc
    if len(parts) != 4:
        raise SystemExit('Box must contain four values: left,bottom,right,top')
    left, bottom, right, top = parts
    if right <= left or top <= bottom:
        raise SystemExit('Invalid box: right must be greater than left and top must be greater than bottom')
    return left, bottom, right, top


def write_json_or_text(data: Dict[str, Any], as_json: bool = True) -> None:
    if as_json:
        print(json.dumps(data, indent=2))
    else:
        for key, value in data.items():
            print(f'{key}: {value}')


def inspect_pdf(args: argparse.Namespace) -> None:
    pypdf = _require('pypdf')
    path = Path(args.input)
    if not path.exists():
        raise SystemExit(f'File not found: {path}')
    reader = pypdf.PdfReader(str(path))
    pages = []
    for i, page in enumerate(reader.pages, start=1):
        mediabox = page.mediabox
        cropbox = page.cropbox
        text = ''
        try:
            text = page.extract_text() or ''
        except Exception:
            text = ''
        pages.append({
            'page': i,
            'width_pt': float(mediabox.width),
            'height_pt': float(mediabox.height),
            'cropbox': [float(cropbox.left), float(cropbox.bottom), float(cropbox.right), float(cropbox.top)],
            'rotation': int(page.get('/Rotate', 0) or 0),
            'has_text': bool(text.strip()),
            'text_characters': len(text),
        })
    info = {
        'file': str(path),
        'exists': path.exists(),
        'size_bytes': path.stat().st_size,
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
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
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
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
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
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
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
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, 'wb') as f:
        writer.write(f)
    print(f"Wrote {args.out}")


def crop_pdf(args: argparse.Namespace) -> None:
    pypdf = _require('pypdf')
    reader = pypdf.PdfReader(args.input)
    selected = set(parse_pages(args.pages, len(reader.pages)))
    left, bottom, right, top = parse_box(args.box)
    writer = pypdf.PdfWriter()
    for index, page in enumerate(reader.pages):
        if index in selected:
            page.cropbox.lower_left = (left, bottom)
            page.cropbox.upper_right = (right, top)
        writer.add_page(page)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, 'wb') as f:
        writer.write(f)
    print(f"Wrote {args.out}")


def watermark_pdf(args: argparse.Namespace) -> None:
    pypdf = _require('pypdf')
    _require('reportlab')
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
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, 'wb') as f:
        writer.write(f)
    print(f"Wrote {args.out}")


def redact_pdf(args: argparse.Namespace) -> None:
    fitz = _require('fitz')
    if not args.text and not args.rect:
        raise SystemExit('Provide --text and/or --rect for redaction')
    doc = fitz.open(args.input)
    selected = set(parse_pages(args.pages, doc.page_count)) if args.pages else set(range(doc.page_count))
    fill = tuple(args.fill)
    redactions = []

    rect_specs = args.rect or []
    rects_by_page: Dict[int, List[Any]] = {}
    for spec in rect_specs:
        try:
            page_s, coords_s = spec.split(':', 1)
            page_index = int(page_s) - 1
            coords = [float(x.strip()) for x in coords_s.split(',')]
            if len(coords) != 4:
                raise ValueError
        except ValueError as exc:
            raise SystemExit('Rect format must be page:x0,y0,x1,y1') from exc
        rects_by_page.setdefault(page_index, []).append(fitz.Rect(coords))

    for index in selected:
        page = doc.load_page(index)
        page_rects = []
        if args.text:
            matches = page.search_for(args.text)
            page_rects.extend(matches)
        page_rects.extend(rects_by_page.get(index, []))
        for rect in page_rects:
            page.add_redact_annot(rect, fill=fill)
        if page_rects:
            page.apply_redactions()
        redactions.append({'page': index + 1, 'redaction_count': len(page_rects)})

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    doc.save(args.out, garbage=4, deflate=True)
    print(json.dumps({'output': args.out, 'redactions': redactions}, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='PDF Pro operations helper')
    sub = parser.add_subparsers(dest='command', required=True)

    p = sub.add_parser('inspect', help='Inspect PDF metadata, pages, rotation, and text availability')
    p.add_argument('input')
    p.set_defaults(func=inspect_pdf)

    p = sub.add_parser('extract-text', help='Extract selectable text from a PDF')
    p.add_argument('input')
    p.add_argument('--pages')
    p.add_argument('--out')
    p.set_defaults(func=extract_text)

    p = sub.add_parser('render', help='Render PDF pages to PNG files')
    p.add_argument('input')
    p.add_argument('--out-dir', required=True)
    p.add_argument('--dpi', type=int, default=160)
    p.add_argument('--pages')
    p.set_defaults(func=render_pdf)

    p = sub.add_parser('merge', help='Merge PDFs into one output file')
    p.add_argument('output')
    p.add_argument('inputs', nargs='+')
    p.set_defaults(func=merge_pdfs)

    p = sub.add_parser('split', help='Extract selected pages into a new PDF')
    p.add_argument('input')
    p.add_argument('--pages', required=True)
    p.add_argument('--out', required=True)
    p.set_defaults(func=split_pdf)

    p = sub.add_parser('rotate', help='Rotate selected pages')
    p.add_argument('input')
    p.add_argument('--pages')
    p.add_argument('--angle', type=int, required=True)
    p.add_argument('--out', required=True)
    p.set_defaults(func=rotate_pdf)

    p = sub.add_parser('crop', help='Set the crop box for selected pages')
    p.add_argument('input')
    p.add_argument('--box', required=True, help='left,bottom,right,top in PDF points')
    p.add_argument('--pages')
    p.add_argument('--out', required=True)
    p.set_defaults(func=crop_pdf)

    p = sub.add_parser('watermark', help='Apply a text watermark')
    p.add_argument('input')
    p.add_argument('--text', required=True)
    p.add_argument('--out', required=True)
    p.add_argument('--pages')
    p.add_argument('--angle', type=float, default=35)
    p.add_argument('--opacity', type=float, default=0.12)
    p.add_argument('--size', type=int, default=72)
    p.set_defaults(func=watermark_pdf)

    p = sub.add_parser('redact', help='Apply true redaction for matched text or explicit rectangles using PyMuPDF')
    p.add_argument('input')
    p.add_argument('--text', help='Text to search and redact')
    p.add_argument('--rect', action='append', help='Explicit redaction rectangle, format page:x0,y0,x1,y1; may be repeated')
    p.add_argument('--pages')
    p.add_argument('--out', required=True)
    p.add_argument('--fill', nargs=3, type=float, default=[0, 0, 0], help='RGB fill values from 0 to 1')
    p.set_defaults(func=redact_pdf)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
