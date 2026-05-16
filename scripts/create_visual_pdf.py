#!/usr/bin/env python3
"""Create a polished fixed-layout PDF from a JSON specification.

Example JSON:
{
  "title": "Project Report",
  "subtitle": "Executive summary",
  "author": "Team Name",
  "pages": [
    {"heading": "Overview", "body": ["Point one", "Point two"], "callout": "Key message"}
  ],
  "theme": {
    "primary": "#2563EB",
    "background": "#F9FAFB",
    "foreground": "#111827",
    "muted": "#6B7280",
    "border": "#E5E7EB"
  }
}
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from textwrap import wrap
from typing import Dict, Iterable, List

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


DEFAULT_THEME = {
    'primary': '#2563EB',
    'background': '#F9FAFB',
    'foreground': '#111827',
    'muted': '#6B7280',
    'border': '#E5E7EB',
    'surface': '#FFFFFF',
    'accent': '#1D4ED8',
}


def hex_color(value: str):
    return colors.HexColor(value)


def theme_value(theme: Dict[str, str], key: str):
    return hex_color(theme.get(key, DEFAULT_THEME[key]))


def draw_wrapped(c: canvas.Canvas, text: str, x: float, y: float, max_width_chars: int, leading: float, font: str, size: float, fill) -> float:
    c.setFillColor(fill)
    c.setFont(font, size)
    for line in wrap(str(text), width=max_width_chars) or ['']:
        c.drawString(x, y, line)
        y -= leading
    return y


def draw_header(c: canvas.Canvas, width: float, height: float, title: str, subtitle: str, theme: Dict[str, str]) -> None:
    c.setFillColor(theme_value(theme, 'background'))
    c.rect(0, 0, width, height, fill=1, stroke=0)
    c.setFillColor(theme_value(theme, 'primary'))
    c.rect(0, height - 0.22 * inch, width, 0.22 * inch, fill=1, stroke=0)
    c.setFillColor(theme_value(theme, 'foreground'))
    c.setFont('Helvetica-Bold', 26)
    c.drawString(0.72 * inch, height - 0.85 * inch, title[:88])
    if subtitle:
        c.setFillColor(theme_value(theme, 'muted'))
        c.setFont('Helvetica', 11)
        c.drawString(0.72 * inch, height - 1.12 * inch, subtitle[:110])


def draw_footer(c: canvas.Canvas, width: float, page_num: int, theme: Dict[str, str]) -> None:
    c.setStrokeColor(theme_value(theme, 'border'))
    c.line(0.72 * inch, 0.56 * inch, width - 0.72 * inch, 0.56 * inch)
    c.setFillColor(theme_value(theme, 'muted'))
    c.setFont('Helvetica', 8)
    c.drawRightString(width - 0.72 * inch, 0.36 * inch, f'Page {page_num}')


def draw_cover(c: canvas.Canvas, spec: Dict, width: float, height: float, theme: Dict[str, str]) -> None:
    c.setFillColor(theme_value(theme, 'background'))
    c.rect(0, 0, width, height, fill=1, stroke=0)
    c.setFillColor(theme_value(theme, 'primary'))
    c.roundRect(width - 2.3 * inch, height - 2.4 * inch, 1.45 * inch, 1.45 * inch, 18, fill=1, stroke=0)
    c.setFillColor(theme_value(theme, 'accent'))
    c.circle(width - 1.0 * inch, height - 1.15 * inch, 0.45 * inch, fill=1, stroke=0)
    c.setFillColor(theme_value(theme, 'foreground'))
    c.setFont('Helvetica-Bold', 34)
    y = height - 2.7 * inch
    for line in wrap(spec.get('title', 'Untitled PDF'), width=25)[:3]:
        c.drawString(0.85 * inch, y, line)
        y -= 0.45 * inch
    subtitle = spec.get('subtitle', '')
    if subtitle:
        y -= 0.2 * inch
        y = draw_wrapped(c, subtitle, 0.88 * inch, y, 58, 16, 'Helvetica', 12, theme_value(theme, 'muted'))
    author = spec.get('author') or spec.get('team') or ''
    if author:
        c.setFont('Helvetica-Bold', 9)
        c.setFillColor(theme_value(theme, 'primary'))
        c.drawString(0.88 * inch, 1.18 * inch, str(author).upper()[:80])


def draw_content_page(c: canvas.Canvas, page: Dict, spec: Dict, width: float, height: float, theme: Dict[str, str], page_num: int) -> None:
    draw_header(c, width, height, page.get('heading') or spec.get('title', 'Document'), page.get('eyebrow', ''), theme)
    y = height - 1.65 * inch
    left = 0.78 * inch
    right = width - 0.78 * inch
    body_width_chars = 86

    intro = page.get('intro')
    if intro:
        y = draw_wrapped(c, intro, left, y, 82, 16, 'Helvetica', 10.5, theme_value(theme, 'foreground'))
        y -= 0.18 * inch

    callout = page.get('callout')
    if callout:
        box_h = 0.82 * inch
        c.setFillColor(theme_value(theme, 'surface'))
        c.setStrokeColor(theme_value(theme, 'border'))
        c.roundRect(left, y - box_h + 0.1 * inch, right - left, box_h, 10, fill=1, stroke=1)
        c.setFillColor(theme_value(theme, 'primary'))
        c.rect(left, y - box_h + 0.1 * inch, 0.08 * inch, box_h, fill=1, stroke=0)
        draw_wrapped(c, callout, left + 0.25 * inch, y - 0.18 * inch, 78, 14, 'Helvetica-Bold', 10, theme_value(theme, 'foreground'))
        y -= box_h + 0.22 * inch

    body = page.get('body', [])
    if isinstance(body, str):
        body = [body]
    for item in body:
        if y < 1.25 * inch:
            draw_footer(c, width, page_num, theme)
            c.showPage()
            page_num += 1
            draw_header(c, width, height, page.get('heading') or spec.get('title', 'Document'), 'continued', theme)
            y = height - 1.65 * inch
        c.setFillColor(theme_value(theme, 'primary'))
        c.circle(left + 0.04 * inch, y + 0.03 * inch, 0.035 * inch, fill=1, stroke=0)
        y = draw_wrapped(c, str(item), left + 0.18 * inch, y, body_width_chars, 14, 'Helvetica', 9.8, theme_value(theme, 'foreground'))
        y -= 0.09 * inch

    metrics = page.get('metrics', [])
    if metrics:
        y -= 0.15 * inch
        card_w = (right - left - 0.24 * inch) / min(3, len(metrics))
        x = left
        for i, metric in enumerate(metrics[:3]):
            c.setFillColor(theme_value(theme, 'surface'))
            c.setStrokeColor(theme_value(theme, 'border'))
            c.roundRect(x, y - 0.78 * inch, card_w, 0.72 * inch, 8, fill=1, stroke=1)
            c.setFillColor(theme_value(theme, 'primary'))
            c.setFont('Helvetica-Bold', 18)
            c.drawString(x + 0.15 * inch, y - 0.33 * inch, str(metric.get('value', ''))[:18])
            c.setFillColor(theme_value(theme, 'muted'))
            c.setFont('Helvetica', 8)
            c.drawString(x + 0.15 * inch, y - 0.55 * inch, str(metric.get('label', ''))[:34])
            x += card_w + 0.12 * inch
    draw_footer(c, width, page_num, theme)


def create_pdf(spec_path: Path, out_path: Path, page_size: str) -> None:
    spec = json.loads(spec_path.read_text(encoding='utf-8'))
    theme = {**DEFAULT_THEME, **spec.get('theme', {})}
    size = A4 if page_size.lower() == 'a4' else letter
    width, height = size
    c = canvas.Canvas(str(out_path), pagesize=size)
    draw_cover(c, spec, width, height, theme)
    c.showPage()
    pages = spec.get('pages') or [{'heading': 'Overview', 'body': spec.get('body', [])}]
    for i, page in enumerate(pages, start=2):
        draw_content_page(c, page, spec, width, height, theme, i)
        c.showPage()
    c.save()
    print(f'Wrote {out_path}')


def main() -> None:
    parser = argparse.ArgumentParser(description='Create a visual PDF from JSON')
    parser.add_argument('spec', help='Path to JSON content specification')
    parser.add_argument('--out', required=True, help='Output PDF path')
    parser.add_argument('--page-size', choices=['a4', 'letter'], default='a4')
    args = parser.parse_args()
    create_pdf(Path(args.spec), Path(args.out), args.page_size)


if __name__ == '__main__':
    main()
