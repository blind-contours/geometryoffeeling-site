#!/usr/bin/env python3
"""
Fix signature placement: move add_signature() from inside save() to render().

For scripts with def save(fig, name), the add_signature call was incorrectly
placed inside save() where ax is not in scope. This moves it to render(),
right before the save(fig, ...) call.
"""

import os
import re
import glob

PIECES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          '..', 'mathematical_affect', 'pieces')


def fix_file(filepath):
    """Fix signature placement in a single file. Returns True if modified."""
    with open(filepath, 'r') as f:
        source = f.read()

    # Only fix files that have def save() AND add_signature inside it
    if not re.search(r'def save\(fig\s*,\s*name\)', source):
        return False
    if 'add_signature' not in source:
        return False

    lines = source.split('\n')
    new_lines = []
    sig_line_text = None
    removed_from_save = False

    # Step 1: Find and remove add_signature from inside save()
    in_save_func = False
    for i, line in enumerate(lines):
        stripped = line.strip()

        if re.match(r'def save\(fig\s*,\s*name\)', stripped):
            in_save_func = True
            new_lines.append(line)
            continue

        if in_save_func:
            if stripped.startswith('add_signature('):
                # Capture the call text and skip this line
                sig_line_text = stripped
                removed_from_save = True
                in_save_func = False
                continue
            # Any non-indented line (or new def) ends save()
            if stripped and not line.startswith(' ') and not line.startswith('\t'):
                in_save_func = False

        new_lines.append(line)

    if not removed_from_save or sig_line_text is None:
        return False

    # Step 2: Insert add_signature before save(fig, ...) call in render()
    final_lines = []
    inserted = False
    for i, line in enumerate(new_lines):
        stripped = line.strip()
        if not inserted and stripped.startswith('save(fig,'):
            # Get indent of the save call
            indent = line[:len(line) - len(line.lstrip())]
            final_lines.append(f"{indent}{sig_line_text}")
            inserted = True
        final_lines.append(line)

    if not inserted:
        print(f"  WARNING: couldn't find save(fig,...) call in {os.path.basename(filepath)}")
        return False

    result = '\n'.join(final_lines)
    with open(filepath, 'w') as f:
        f.write(result)
    return True


def main():
    scripts = sorted(glob.glob(os.path.join(PIECES_DIR, '*', '*.py')))
    fixed = 0
    skipped = 0
    for path in scripts:
        name = os.path.basename(path)
        if fix_file(path):
            fixed += 1
            print(f"  fixed: {name}")
        else:
            skipped += 1

    print(f"\nDone: {fixed} fixed, {skipped} skipped (no fix needed)")


if __name__ == '__main__':
    main()
