#!/usr/bin/env python3
"""
Batch render all piece scripts to PDF, then convert to high-res JPG.

Pipeline:
  1. Run each .py script to generate PDF in mathematical_affect/output/
  2. Convert PDF → PNG at 3600px width via sips
  3. Convert PNG → JPG at quality=95, subsampling=0 via Pillow
  4. Place JPG in public/prints/{series}/

Parallelized with concurrent.futures for speed.
"""

import os
import sys
import glob
import subprocess
import tempfile
import shutil
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

# Paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_DIR = os.path.join(PROJECT_ROOT, 'mathematical_affect', 'pieces')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'mathematical_affect', 'output')
PRINTS_DIR = os.path.join(PROJECT_ROOT, 'public', 'prints')

# Render settings
JPG_WIDTH = 3600  # pixels — good for 4K displays
JPG_QUALITY = 95
MAX_WORKERS = 6


def get_piece_name(script_path):
    """Extract piece name from script path."""
    return os.path.splitext(os.path.basename(script_path))[0]


def get_series_name(script_path):
    """Extract series name from script path."""
    return os.path.basename(os.path.dirname(script_path))


def render_pdf(script_path):
    """Run a piece script to generate its PDF. Returns (name, pdf_path, error)."""
    name = get_piece_name(script_path)
    pdf_path = os.path.join(OUTPUT_DIR, f"{name}.pdf")

    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True, text=True, timeout=120,
            cwd=os.path.dirname(script_path)
        )
        if result.returncode != 0:
            return (name, None, f"Script error: {result.stderr[:200]}")
        if not os.path.exists(pdf_path):
            return (name, None, f"PDF not created at {pdf_path}")
        return (name, pdf_path, None)
    except subprocess.TimeoutExpired:
        return (name, None, "Timeout (120s)")
    except Exception as e:
        return (name, None, str(e))


def convert_to_jpg(pdf_path, series_name, piece_name):
    """Convert PDF → high-res JPG. Returns (piece_name, jpg_path, error)."""
    try:
        from PIL import Image
    except ImportError:
        return (piece_name, None, "Pillow not installed")

    series_dir = os.path.join(PRINTS_DIR, series_name)
    os.makedirs(series_dir, exist_ok=True)
    jpg_path = os.path.join(series_dir, f"{piece_name}.jpg")

    with tempfile.TemporaryDirectory() as tmpdir:
        png_path = os.path.join(tmpdir, f"{piece_name}.png")

        # PDF → PNG via sips (macOS)
        result = subprocess.run(
            ['sips', '-s', 'format', 'png',
             '--resampleWidth', str(JPG_WIDTH),
             pdf_path, '--out', png_path],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode != 0 or not os.path.exists(png_path):
            return (piece_name, None, f"sips error: {result.stderr[:200]}")

        # PNG → JPG via Pillow (quality=95, no chroma subsampling)
        try:
            img = Image.open(png_path)
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            img.save(jpg_path, 'JPEG', quality=JPG_QUALITY, subsampling=0)
            return (piece_name, jpg_path, None)
        except Exception as e:
            return (piece_name, None, f"Pillow error: {e}")


def render_and_convert(script_path):
    """Full pipeline: script → PDF → JPG."""
    name = get_piece_name(script_path)
    series = get_series_name(script_path)

    # Step 1: Render PDF
    _, pdf_path, error = render_pdf(script_path)
    if error:
        return (name, series, None, f"Render: {error}")

    # Step 2: Convert to JPG
    _, jpg_path, error = convert_to_jpg(pdf_path, series, name)
    if error:
        return (name, series, None, f"Convert: {error}")

    return (name, series, jpg_path, None)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Batch render all pieces')
    parser.add_argument('--render-only', action='store_true',
                        help='Only render PDFs, skip JPG conversion')
    parser.add_argument('--convert-only', action='store_true',
                        help='Only convert existing PDFs to JPG')
    parser.add_argument('--filter', type=str, default=None,
                        help='Only process scripts matching this pattern (e.g., "desire")')
    parser.add_argument('--workers', type=int, default=MAX_WORKERS,
                        help=f'Number of parallel workers (default: {MAX_WORKERS})')
    parser.add_argument('--test', type=int, default=0,
                        help='Only process N scripts (for testing)')
    args = parser.parse_args()

    scripts = sorted(glob.glob(os.path.join(PIECES_DIR, '*', '*.py')))
    if args.filter:
        scripts = [s for s in scripts if args.filter in s]
    if args.test:
        scripts = scripts[:args.test]

    print(f"Processing {len(scripts)} scripts with {args.workers} workers")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    successes = 0
    failures = []

    if args.convert_only:
        # Just convert existing PDFs
        for script_path in scripts:
            name = get_piece_name(script_path)
            series = get_series_name(script_path)
            pdf_path = os.path.join(OUTPUT_DIR, f"{name}.pdf")
            if not os.path.exists(pdf_path):
                failures.append((name, "PDF not found"))
                continue
            _, jpg_path, error = convert_to_jpg(pdf_path, series, name)
            if error:
                failures.append((name, error))
                print(f"  FAIL: {name} — {error}")
            else:
                successes += 1
                print(f"  OK: {name} → {jpg_path}")
    elif args.render_only:
        # Just render PDFs
        with ProcessPoolExecutor(max_workers=args.workers) as executor:
            futures = {executor.submit(render_pdf, s): s for s in scripts}
            for future in as_completed(futures):
                name, pdf_path, error = future.result()
                if error:
                    failures.append((name, error))
                    print(f"  FAIL: {name} — {error}")
                else:
                    successes += 1
                    print(f"  OK: {name}")
    else:
        # Full pipeline: render + convert
        with ProcessPoolExecutor(max_workers=args.workers) as executor:
            futures = {executor.submit(render_and_convert, s): s for s in scripts}
            for future in as_completed(futures):
                name, series, jpg_path, error = future.result()
                if error:
                    failures.append((name, error))
                    print(f"  FAIL: {name} — {error}")
                else:
                    successes += 1
                    print(f"  OK: {name}")

    print(f"\n{'='*60}")
    print(f"Results: {successes} succeeded, {len(failures)} failed")
    if failures:
        print(f"\nFailures:")
        for name, error in sorted(failures):
            print(f"  {name}: {error}")

    return 0 if not failures else 1


if __name__ == '__main__':
    sys.exit(main())
