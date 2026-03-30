#!/usr/bin/env python3
"""
Strip all equation labels from piece scripts.

Handles two patterns:
  Pattern A (139 scripts): def label(ax, eq) function + label(ax, ...) calls
  Pattern B (27 scripts):  inline ax.text() calls placing equation text

Idempotent — safe to re-run.
"""

import os
import re
import glob

PIECES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          '..', 'mathematical_affect', 'pieces')


def strip_label_function(source):
    """Remove def label(ax, ...) function definition (entire block)."""
    # Match the function def + body (indented lines following it)
    # Handles: def label(ax,eq):  /  def label(ax, eq):  /  def label(ax, eq, note=None):
    pattern = r'\ndef label\(ax[^)]*\):\n(?:[ \t]+[^\n]*\n)+'
    return re.sub(pattern, '\n', source)


def strip_label_calls(source):
    """Remove label(ax, ...) function calls."""
    # Match: label(ax, "...") with possible multiline string
    # Single-line calls like: label(ax, "equation")
    pattern = r'[ \t]*label\(ax,\s*"[^"]*"\)\n'
    source = re.sub(pattern, '', source)
    # Also handle calls with note parameter
    pattern2 = r'[ \t]*label\(ax,\s*"[^"]*",\s*"[^"]*"\)\n'
    source = re.sub(pattern2, '', source)
    return source


def strip_inline_equation_text(source):
    """Remove inline ax.text() calls that place equation text.

    These are identified by containing fontfamily='monospace' and are
    typically equation labels at low alpha.
    """
    lines = source.split('\n')
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Check for comment lines preceding an ax.text equation label
        # e.g., "# Equation label" or "# --- Equation label ---"
        if i + 1 < len(lines) and re.match(r'\s*#.*(?:equation|label|eq\b)', stripped, re.IGNORECASE):
            # Look ahead to see if next non-blank line is ax.text with monospace
            j = i + 1
            while j < len(lines) and lines[j].strip() == '':
                j += 1
            if j < len(lines) and 'ax.text(' in lines[j]:
                # Check if this ax.text block contains monospace
                block_start = j
                block_end = j
                paren_depth = 0
                for k in range(j, len(lines)):
                    paren_depth += lines[k].count('(') - lines[k].count(')')
                    block_end = k
                    if paren_depth <= 0:
                        break
                block = '\n'.join(lines[block_start:block_end + 1])
                if 'monospace' in block:
                    # Also check for eq = "..." variable assignment before
                    if i > 0 and re.match(r'\s*eq\s*=\s*["\']', lines[i - 1].strip()):
                        # Remove the eq assignment too (already handled in result)
                        if result and re.match(r'\s*eq\s*=\s*["\']', result[-1].strip()):
                            result.pop()
                    i = block_end + 1
                    continue

        # Check for standalone ax.text with monospace (no preceding comment)
        if 'ax.text(' in stripped:
            # Collect the full multi-line call
            block_start = i
            block_end = i
            paren_depth = 0
            for k in range(i, len(lines)):
                paren_depth += lines[k].count('(') - lines[k].count(')')
                block_end = k
                if paren_depth <= 0:
                    break
            block = '\n'.join(lines[block_start:block_end + 1])
            if 'monospace' in block:
                # Check for preceding eq = "..." variable assignment
                if result and re.match(r'\s*eq\s*=\s*["\']', result[-1].strip()):
                    result.pop()
                # Also remove preceding blank comment about equation
                while result and result[-1].strip() == '':
                    # Don't remove too many blank lines — just one
                    break
                i = block_end + 1
                continue

        result.append(line)
        i += 1

    return '\n'.join(result)


def strip_file(filepath):
    """Strip all equation labels from a single file."""
    with open(filepath, 'r') as f:
        original = f.read()

    source = original

    # Pattern A: remove label function and calls
    if 'def label(' in source:
        source = strip_label_function(source)
        source = strip_label_calls(source)

    # Pattern B: remove inline ax.text equation labels
    # Check for ax.text with monospace that aren't inside a label function
    if 'monospace' in source and 'ax.text(' in source:
        source = strip_inline_equation_text(source)

    # Clean up: remove double blank lines that may result from removal
    source = re.sub(r'\n{3,}', '\n\n', source)

    if source != original:
        with open(filepath, 'w') as f:
            f.write(source)
        return True
    return False


def main():
    scripts = sorted(glob.glob(os.path.join(PIECES_DIR, '*', '*.py')))
    print(f"Found {len(scripts)} scripts")

    modified = 0
    skipped = 0
    for path in scripts:
        name = os.path.basename(path)
        changed = strip_file(path)
        if changed:
            modified += 1
            print(f"  stripped: {name}")
        else:
            skipped += 1
            print(f"  (clean): {name}")

    print(f"\nDone: {modified} modified, {skipped} already clean")


if __name__ == '__main__':
    main()
