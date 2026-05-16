from pathlib import Path
import subprocess
import sys


def run(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, check=True)


def test_help_commands():
    root = Path(__file__).resolve().parents[1]
    run([sys.executable, "scripts/pdf_ops.py", "--help"], root)
    run([sys.executable, "scripts/validate_pdf.py", "--help"], root)
    run([sys.executable, "scripts/create_visual_pdf.py", "--help"], root)


def test_package_structure():
    root = Path(__file__).resolve().parents[1]
    run([sys.executable, "scripts/validate_package.py", "."], root)
