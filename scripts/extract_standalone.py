"""
Extract standalone render scripts from production *_final*.py files.
Creates one .py file per piece in mathematical_affect/pieces/{series}/
"""
import ast
import os
import re
import textwrap

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CODE_DIR = os.path.join(BASE, "mathematical_affect", "code")
PIECES_DIR = os.path.join(BASE, "mathematical_affect", "pieces")

# Mapping: (series, piece_name) -> (source_file, render_func_name)
EXTRACTIONS = [
    # anticipation
    ("anticipation", "anticipation_charge", "anticipation_final.py", "render_charge"),
    ("anticipation", "anticipation_convergence", "anticipation_final.py", "render_convergence"),
    ("anticipation", "anticipation_countdown", "anticipation_final.py", "render_countdown"),
    ("anticipation", "anticipation_kindling", "anticipation_final.py", "render_kindling"),
    ("anticipation", "anticipation_potential", "anticipation_final.py", "render_potential"),
    # awe
    ("awe", "awe_eclipse", "awe_cosmic_final.py", "render_eclipse"),
    ("awe", "awe_gravitational_waves", "awe_cosmic_final.py", "render_gravitational_waves"),
    ("awe", "awe_singularity", "awe_cosmic_final.py", "render_singularity"),
    # confusion
    ("confusion", "confusion_aliased", "confusion_final.py", "render_aliased"),
    ("confusion", "confusion_labyrinth", "confusion_final.py", "render_labyrinth"),
    # cycles
    ("cycles", "cycles_breathing", "cycles_final_v2.py", "render_breathing"),
    ("cycles", "cycles_loom", "cycles_final_v2.py", "render_loom"),
    ("cycles", "cycles_seasons", "cycles_final_v2.py", "render_seasons"),
    # envy
    ("envy", "envy_covet", "envy_final.py", "render_covet"),
    ("envy", "envy_glass_ceiling", "envy_final.py", "render_glass_ceiling"),
    # euphoria
    ("euphoria", "euphoria_crown", "euphoria_final.py", "render_crown"),
    ("euphoria", "euphoria_firework", "euphoria_final.py", "render_firework"),
    ("euphoria", "euphoria_prismatic", "euphoria_final.py", "render_prismatic"),
    ("euphoria", "euphoria_stained_glass", "euphoria_final.py", "render_stained_glass"),
    # fractured
    ("fractured", "fractured_catastrophe_fold", "fractured_final.py", "render_catastrophe_fold"),
    ("fractured", "fractured_glass_fracture", "fractured_final.py", "render_glass_fracture"),
    ("fractured", "fractured_voronoi_shatter", "fractured_final.py", "render_voronoi_shatter"),
    # grief
    ("grief", "grief_absence", "grief_final_v2.py", "render_absence"),
    ("grief", "grief_heaviside_cascade", "grief_final_v2.py", "render_heaviside_cascade"),
    ("grief", "grief_weight", "grief_final_v2.py", "render_weight"),
    # growth
    ("growth", "growth_dendrite", "growth_final_v2.py", "render_dendrite"),
    ("growth", "growth_lissajous_bloom", "growth_final_v2.py", "render_lissajous_bloom"),
    ("growth", "growth_logistic_cascade", "growth_final_v2.py", "render_logistic_cascade"),
    ("growth", "growth_reaction_diffusion", "growth_final_v2.py", "render_reaction_diffusion"),
    # joy
    ("joy", "joy_bloom", "joy_final.py", "render_bloom"),
    ("joy", "joy_confetti", "joy_final.py", "render_confetti"),
    ("joy", "joy_lissajous", "joy_final.py", "render_lissajous"),
    ("joy", "joy_pinwheel", "joy_final.py", "render_pinwheel"),
    ("joy", "joy_sunburst", "joy_final.py", "render_sunburst"),
    # longing
    ("longing", "longing_harmonic_decay", "longing_final.py", "render_harmonic_decay"),
    ("longing", "longing_magnetic", "longing_final.py", "render_magnetic"),
    ("longing", "longing_tantalus", "longing_final.py", "render_tantalus"),
    ("longing", "longing_zeno", "longing_final.py", "render_zeno"),
    # melancholy
    ("melancholy", "melancholy_dissolve", "melancholy_final.py", "render_dissolve"),
    ("melancholy", "melancholy_drift", "melancholy_final.py", "render_drift"),
    ("melancholy", "melancholy_lethe", "melancholy_final.py", "render_lethe"),
    # nostalgia
    ("nostalgia", "nostalgia_heirloom", "nostalgia_final_v2.py", "render_heirloom"),
    ("nostalgia", "nostalgia_saudade", "nostalgia_final_v2.py", "render_saudade"),
    ("nostalgia", "nostalgia_sepia", "nostalgia_final_v2.py", "render_sepia"),
    # overwhelm
    ("overwhelm", "overwhelm_attractors", "overwhelm_final.py", "render_attractors"),
    ("overwhelm", "overwhelm_phase_flood", "overwhelm_final.py", "render_phase_flood"),
    ("overwhelm", "overwhelm_turbulence", "overwhelm_final.py", "render_turbulence"),
    # peace
    ("peace", "peace_cloud", "peace_final_v2.py", "render_cloud"),
    ("peace", "peace_harmonic", "peace_final_v2.py", "render_harmonic"),
    # pride
    ("pride", "pride_crown", "pride_final.py", "render_crown"),
    ("pride", "pride_spire", "pride_final.py", "render_spire"),
    ("pride", "pride_unfurl", "pride_final.py", "render_unfurl"),
    # rage
    ("rage", "rage_chaos", "rage_final.py", "render_chaos"),
    ("rage", "rage_detonation", "rage_final.py", "render_detonation"),
    ("rage", "rage_eruption", "rage_final.py", "render_eruption"),
    ("rage", "rage_shatter", "rage_final.py", "render_shatter"),
    ("rage", "rage_shockwave", "rage_final.py", "render_shockwave"),
    # resilience
    ("resilience", "resilience_phoenix", "resilience_final.py", "render_phoenix"),
    ("resilience", "resilience_repair", "resilience_final.py", "render_repair"),
    # shame
    ("shame", "shame_shrink", "shame_final.py", "render_shrink"),
    # solitude
    ("solitude", "solitude_canopy", "solitude_final_v2.py", "render_canopy"),
    # surrender
    ("surrender", "surrender_melt", "surrender_final_v2.py", "render_melt"),
    ("surrender", "surrender_terminal", "surrender_final_v2.py", "render_terminal"),
    # tension
    ("tension", "tension_buckling", "tension_final.py", "render_buckling"),
    ("tension", "tension_fracture", "tension_final.py", "render_fracture"),
    ("tension", "tension_opposition", "tension_final.py", "render_opposition"),
    ("tension", "tension_torsion", "tension_final.py", "render_torsion"),
    # trust
    ("trust", "trust_handshake", "trust_final.py", "render_handshake"),
    ("trust", "trust_mirror", "trust_final.py", "render_mirror"),
    # wonder
    ("wonder", "wonder_apollonian_gasket", "wonder_final.py", "render_apollonian_gasket"),
    ("wonder", "wonder_harmonograph", "wonder_final.py", "render_harmonograph"),
    ("wonder", "wonder_mandelbrot_orbit", "wonder_final.py", "render_mandelbrot_orbit"),
]


def extract_function_source(source_lines, func_name):
    """Extract a function definition and all its body from source lines."""
    # Find the function definition line
    func_start = None
    for i, line in enumerate(source_lines):
        if re.match(rf'^def {func_name}\s*\(', line):
            func_start = i
            break

    if func_start is None:
        return None

    # Find the end of the function (next top-level def, class, or significant comment block)
    func_end = len(source_lines)

    for i in range(func_start + 1, len(source_lines)):
        line = source_lines[i]
        stripped = line.strip()

        # Skip empty lines
        if not stripped:
            continue

        # Top-level non-indented code that isn't a comment = new block
        if line and not line[0].isspace() and stripped:
            # New function or class definition
            if stripped.startswith('def ') or stripped.startswith('class ') or stripped.startswith('if __name__'):
                func_end = i
                break
            # Section header comments (ASCII or Unicode box chars)
            if re.match(r'^#\s*[═━─=─]{3,}', stripped):
                func_end = i
                break

    # Trim trailing blank lines
    while func_end > func_start and not source_lines[func_end - 1].strip():
        func_end -= 1

    return source_lines[func_start:func_end]


def extract_boilerplate(source_lines):
    """Extract everything before the first render_ function."""
    for i, line in enumerate(source_lines):
        if re.match(r'^def render_', line):
            # Go back past any comment block
            j = i - 1
            while j >= 0 and (source_lines[j].strip().startswith('#') or not source_lines[j].strip()):
                j -= 1
            return source_lines[:j + 1]
    return source_lines


def make_standalone(series, piece_name, source_file, func_name):
    """Create a standalone script for a piece."""
    source_path = os.path.join(CODE_DIR, source_file)
    if not os.path.exists(source_path):
        print(f"  ERROR: {source_file} not found")
        return False

    with open(source_path) as f:
        source = f.read()
    source_lines = source.split('\n')

    # Extract the boilerplate
    boilerplate_lines = extract_boilerplate(source_lines)
    boilerplate = '\n'.join(boilerplate_lines)

    # Extract the render function
    func_lines = extract_function_source(source_lines, func_name)
    if func_lines is None:
        print(f"  ERROR: {func_name} not found in {source_file}")
        return False

    func_source = '\n'.join(func_lines)

    # Rename the function to just render()
    func_source = re.sub(rf'^def {func_name}\s*\(', 'def render(', func_source, count=1)

    # Fix OUTPUT_DIR to use the standalone pattern
    # Remove old path variables from boilerplate
    boilerplate = re.sub(r'^SCRIPT_DIR\s*=.*$', '', boilerplate, flags=re.MULTILINE)
    boilerplate = re.sub(r'^OUTPUT_DIR\s*=.*$', '', boilerplate, flags=re.MULTILINE)
    boilerplate = re.sub(r'^JPEG_DIR\s*=.*$', '', boilerplate, flags=re.MULTILINE)
    boilerplate = re.sub(r'^PDF_DIR\s*=.*$', '', boilerplate, flags=re.MULTILINE)
    boilerplate = re.sub(r'^PNG_DIR\s*=.*$', '', boilerplate, flags=re.MULTILINE)
    boilerplate = re.sub(r'^BASE\s*=\s*os\.path\.join\(SCRIPT_DIR.*$', '', boilerplate, flags=re.MULTILINE)
    boilerplate = re.sub(r'^JPG_DIR\s*=.*$', '', boilerplate, flags=re.MULTILINE)

    # Remove the old docstring and replace with new one
    # Strip leading docstrings
    boilerplate = re.sub(r'^"""[\s\S]*?"""', '', boilerplate, count=1).lstrip('\n')

    # Also strip any second docstring
    if boilerplate.lstrip().startswith('"""'):
        boilerplate = re.sub(r'^"""[\s\S]*?"""', '', boilerplate, count=1).lstrip('\n')

    # Remove os.makedirs calls from boilerplate
    boilerplate = re.sub(r'^os\.makedirs.*$', '', boilerplate, flags=re.MULTILINE)

    # Clean up multiple blank lines
    boilerplate = re.sub(r'\n{3,}', '\n\n', boilerplate)

    # Build the title
    title_parts = piece_name.split('_')
    # Capitalize series name
    series_cap = series.capitalize()
    piece_title = ' '.join(w.capitalize() for w in title_parts)

    # Replace save function with standard one that uses OUTPUT_DIR
    # First, detect what BG color the save uses
    bg_match = re.search(r"facecolor\s*=\s*([A-Z_]+|'[^']*'|\"[^\"]*\")", boilerplate)
    bg_var = "BG"
    if bg_match:
        bg_var = bg_match.group(1)
    # Check if BG is actually defined
    if 'BG' not in boilerplate and bg_var == 'BG':
        bg_var = "'#F8F6F2'"  # safe default

    # Remove the existing save function from boilerplate
    boilerplate = re.sub(
        r'def save\(fig\s*,\s*name\)[\s\S]*?(?=\ndef |\n[A-Z]|\nSCRIPT|\Z)',
        '', boilerplate
    ).rstrip()

    # Remove any leftover JPEG conversion code in boilerplate
    boilerplate = re.sub(r'^\s*#.*jpeg.*convert.*$', '', boilerplate, flags=re.MULTILINE | re.IGNORECASE)

    # Clean up multiple blank lines
    boilerplate = re.sub(r'\n{3,}', '\n\n', boilerplate)

    # Build the standalone script
    script = f'"""\nGeometry of Feeling — {series_cap}: {piece_title}\nStandalone render script\n"""\n\n'
    script += boilerplate.strip() + '\n\n'

    # Add standard save function, SCRIPT_DIR, OUTPUT_DIR
    script += "SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))\n"
    script += "OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')\n\n"
    script += f"def save(fig, name):\n"
    script += f"    os.makedirs(OUTPUT_DIR, exist_ok=True)\n"
    script += f"    if not name.endswith('.pdf'):\n"
    script += f"        name = name + '.pdf'\n"
    script += f"    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)\n"
    script += f"    fig.savefig(os.path.join(OUTPUT_DIR, name),\n"
    script += f"                format='pdf', facecolor={bg_var})\n"
    script += f"    plt.close(fig)\n"
    script += f"    print(f'saved {{name}}')\n"

    # Fix save calls in render function that pass name without .pdf
    # Some scripts call save(fig, "name") without .pdf extension
    # Our save function handles that now

    # Add the render function
    script += '\n\n' + func_source.strip() + '\n'

    # Add main block
    script += f"\n\nif __name__ == '__main__':\n    render()\n"

    # Write the file
    out_dir = os.path.join(PIECES_DIR, series)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{piece_name}.py")

    # Don't overwrite existing files
    if os.path.exists(out_path):
        print(f"  SKIP (exists): {out_path}")
        return False

    with open(out_path, 'w') as f:
        f.write(script)

    print(f"  OK: {piece_name}.py")
    return True


def main():
    created = 0
    skipped = 0
    errors = 0

    for series, piece_name, source_file, func_name in EXTRACTIONS:
        result = make_standalone(series, piece_name, source_file, func_name)
        if result:
            created += 1
        elif result is False:
            # Check if it was a skip or error
            out_path = os.path.join(PIECES_DIR, series, f"{piece_name}.py")
            if os.path.exists(out_path):
                skipped += 1
            else:
                errors += 1

    print(f"\nDone: {created} created, {skipped} skipped (exist), {errors} errors")


if __name__ == '__main__':
    main()
