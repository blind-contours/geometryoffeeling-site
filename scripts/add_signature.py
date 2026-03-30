#!/usr/bin/env python3
"""
Batch-add signature overlay to all piece scripts.

For each script, this:
1. Adds `from signature_utils import add_signature` import
2. Inserts add_signature(fig, ax, BG) call before the save step

Idempotent — safe to re-run (skips already-patched files).
"""

import os
import re
import glob

PIECES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          '..', 'mathematical_affect', 'pieces')

IMPORT_LINE = "from signature_utils import add_signature"


def detect_bg_var(source):
    """Detect the background color variable name."""
    if re.search(r'^BG_COLOR\s*=', source, re.MULTILINE):
        return 'BG_COLOR'
    if re.search(r'^BG\s*=', source, re.MULTILINE):
        return 'BG'
    return None


def detect_margin(source):
    """Check if this is a margin piece."""
    return 'MARGIN_COLOR' in source


def patch_file(filepath):
    """Add signature to a single script. Returns True if modified."""
    with open(filepath, 'r') as f:
        source = f.read()

    # Skip if already patched
    if 'add_signature' in source:
        return False

    bg_var = detect_bg_var(source)
    if bg_var is None:
        print(f"  WARNING: no BG variable found in {os.path.basename(filepath)}")
        return False

    is_margin = detect_margin(source)
    sig_bg_var = 'MARGIN_COLOR' if is_margin else bg_var

    if is_margin:
        sig_call_line = f"    add_signature(fig, ax, {sig_bg_var}, margin_piece=True, margin_bottom=FIG_H * 0.08)"
    else:
        sig_call_line = f"    add_signature(fig, ax, {sig_bg_var})"

    lines = source.split('\n')
    new_lines = []
    import_added = False
    sig_added = False

    for i, line in enumerate(lines):
        stripped = line.strip()

        # --- Add import after last top-level import ---
        if not import_added:
            is_import = (line.startswith('import ') or line.startswith('from '))
            next_is_not_import = (
                i + 1 >= len(lines) or
                not (lines[i + 1].startswith('import ') or
                     lines[i + 1].startswith('from '))
            )
            if is_import and next_is_not_import:
                new_lines.append(line)
                new_lines.append(IMPORT_LINE)
                import_added = True
                continue

        # --- Insert signature call before save ---
        if not sig_added:
            # Pattern A: save(fig, ...) call inside render()
            if stripped.startswith('save(fig,'):
                new_lines.append(sig_call_line)
                new_lines.append(line)
                sig_added = True
                continue

            # Pattern B: fig.subplots_adjust followed by fig.savefig
            if stripped.startswith('fig.subplots_adjust('):
                # Check if fig.savefig follows within a few lines
                has_savefig = any('fig.savefig' in lines[j]
                                  for j in range(i + 1, min(i + 5, len(lines))))
                if has_savefig:
                    new_lines.append(sig_call_line)
                    new_lines.append(line)
                    sig_added = True
                    continue

            # Pattern B variant: fig.savefig() directly (no preceding subplots_adjust)
            # Only match inside render(), not inside def save()
            if stripped.startswith('fig.savefig('):
                indent = len(line) - len(line.lstrip())
                # Must be indented (inside a function) and not inside def save()
                if indent >= 4:
                    # Check we're not inside def save() by scanning backward
                    in_save_func = False
                    for j in range(i - 1, max(i - 10, -1), -1):
                        if lines[j].strip().startswith('def save('):
                            in_save_func = True
                            break
                        if lines[j].strip().startswith('def ') and 'save' not in lines[j]:
                            break
                    if not in_save_func:
                        new_lines.append(sig_call_line)
                        new_lines.append(line)
                        sig_added = True
                        continue

        new_lines.append(line)

    if not import_added:
        print(f"  WARNING: couldn't add import to {os.path.basename(filepath)}")
        return False
    if not sig_added:
        print(f"  WARNING: couldn't find save point in {os.path.basename(filepath)}")
        return False

    result = '\n'.join(new_lines)
    with open(filepath, 'w') as f:
        f.write(result)
    return True


def main():
    scripts = sorted(glob.glob(os.path.join(PIECES_DIR, '*', '*.py')))
    print(f"Found {len(scripts)} scripts")

    patched = 0
    skipped = 0
    failed = 0
    for path in scripts:
        name = os.path.basename(path)
        try:
            changed = patch_file(path)
            if changed:
                patched += 1
                print(f"  patched: {name}")
            else:
                skipped += 1
                print(f"  (skip):  {name}")
        except Exception as e:
            failed += 1
            print(f"  FAILED:  {name}: {e}")

    print(f"\nDone: {patched} patched, {skipped} skipped, {failed} failed")


if __name__ == '__main__':
    main()
