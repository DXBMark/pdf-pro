#!/usr/bin/env python3
"""Unified PDF Pro CLI."""

from __future__ import annotations

import argparse
import sys

from pdf_pro import __version__
from pdf_pro import pdf_ops, validate_pdf, create_visual_pdf


def main(argv: list[str] | None = None) -> None:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in {'-h', '--help'}:
        print_help()
        return
    if argv[0] in {'-V', '--version', 'version'}:
        print(__version__)
        return

    command = argv[0]
    rest = argv[1:]

    if command == 'validate':
        parser = validate_pdf.build_parser()
        args = parser.parse_args(rest)
        raise SystemExit(validate_pdf.validate(args))
    if command == 'visual':
        old = sys.argv[:]
        try:
            sys.argv = ['pdf-pro visual'] + rest
            create_visual_pdf.main()
        finally:
            sys.argv = old
        return

    # Forward all PDF operation commands to pdf_ops.
    parser = pdf_ops.build_parser()
    args = parser.parse_args(argv)
    args.func(args)


def print_help() -> None:
    print("""PDF Pro CLI

Usage:
  pdf-pro <command> [options]

PDF operations:
  inspect        Inspect PDF metadata, pages, rotation, and text availability
  extract-text   Extract selectable text
  render         Render pages to PNG files
  merge          Merge PDFs
  split          Extract selected pages
  rotate         Rotate selected pages
  crop           Set crop boxes on selected pages
  watermark      Add a text watermark
  redact         Redact matched text or explicit rectangles

Other commands:
  validate       Validate a final PDF
  visual         Create a visual PDF from a JSON specification
  version        Show version

Examples:
  pdf-pro inspect input.pdf
  pdf-pro render input.pdf --out-dir renders/input --dpi 160
  pdf-pro validate output.pdf --render --out-dir validation/output
  pdf-pro visual examples/visual-spec.json --out output.pdf
""")


if __name__ == '__main__':
    main()
