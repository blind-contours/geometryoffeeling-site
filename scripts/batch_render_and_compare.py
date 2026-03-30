"""
Batch render extracted standalone scripts and compare against curated JPGs.
Outputs a similarity report.
"""
import os
import sys
import subprocess
import numpy as np
from PIL import Image

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_DIR = os.path.join(BASE, "mathematical_affect", "pieces")
OUTPUT_DIR = os.path.join(BASE, "mathematical_affect", "output")
PRINTS_DIR = os.path.join(BASE, "public", "prints")

# The 69 pieces we extracted (excluding wonder 3 that were removed from site)
PIECES = [
    ("anticipation", "anticipation_charge"),
    ("anticipation", "anticipation_convergence"),
    ("anticipation", "anticipation_countdown"),
    ("anticipation", "anticipation_kindling"),
    ("anticipation", "anticipation_potential"),
    ("awe", "awe_eclipse"),
    ("awe", "awe_gravitational_waves"),
    ("awe", "awe_singularity"),
    ("confusion", "confusion_aliased"),
    ("confusion", "confusion_labyrinth"),
    ("cycles", "cycles_breathing"),
    ("cycles", "cycles_loom"),
    ("cycles", "cycles_seasons"),
    ("envy", "envy_covet"),
    ("envy", "envy_glass_ceiling"),
    ("euphoria", "euphoria_crown"),
    ("euphoria", "euphoria_firework"),
    ("euphoria", "euphoria_prismatic"),
    ("euphoria", "euphoria_stained_glass"),
    ("fractured", "fractured_catastrophe_fold"),
    ("fractured", "fractured_glass_fracture"),
    ("fractured", "fractured_voronoi_shatter"),
    ("grief", "grief_absence"),
    ("grief", "grief_heaviside_cascade"),
    ("grief", "grief_weight"),
    ("growth", "growth_dendrite"),
    ("growth", "growth_lissajous_bloom"),
    ("growth", "growth_logistic_cascade"),
    ("growth", "growth_reaction_diffusion"),
    ("joy", "joy_bloom"),
    ("joy", "joy_confetti"),
    ("joy", "joy_lissajous"),
    ("joy", "joy_pinwheel"),
    ("joy", "joy_sunburst"),
    ("longing", "longing_harmonic_decay"),
    ("longing", "longing_magnetic"),
    ("longing", "longing_tantalus"),
    ("longing", "longing_zeno"),
    ("melancholy", "melancholy_dissolve"),
    ("melancholy", "melancholy_drift"),
    ("melancholy", "melancholy_lethe"),
    ("nostalgia", "nostalgia_heirloom"),
    ("nostalgia", "nostalgia_saudade"),
    ("nostalgia", "nostalgia_sepia"),
    ("overwhelm", "overwhelm_attractors"),
    ("overwhelm", "overwhelm_phase_flood"),
    ("overwhelm", "overwhelm_turbulence"),
    ("peace", "peace_cloud"),
    ("peace", "peace_harmonic"),
    ("pride", "pride_crown"),
    ("pride", "pride_spire"),
    ("pride", "pride_unfurl"),
    ("rage", "rage_chaos"),
    ("rage", "rage_detonation"),
    ("rage", "rage_eruption"),
    ("rage", "rage_shatter"),
    ("rage", "rage_shockwave"),
    ("resilience", "resilience_phoenix"),
    ("resilience", "resilience_repair"),
    ("shame", "shame_shrink"),
    ("solitude", "solitude_canopy"),
    ("surrender", "surrender_melt"),
    ("surrender", "surrender_terminal"),
    ("tension", "tension_buckling"),
    ("tension", "tension_fracture"),
    ("tension", "tension_opposition"),
    ("tension", "tension_torsion"),
    ("trust", "trust_handshake"),
    ("trust", "trust_mirror"),
]


def render_piece(series, piece_name):
    """Render a piece and return the PDF path."""
    script = os.path.join(PIECES_DIR, series, f"{piece_name}.py")
    if not os.path.exists(script):
        return None, f"Script not found: {script}"

    try:
        result = subprocess.run(
            [sys.executable, script],
            capture_output=True, text=True, timeout=120,
            cwd=BASE
        )
        if result.returncode != 0:
            return None, f"Render failed: {result.stderr[:200]}"
    except subprocess.TimeoutExpired:
        return None, "Render timed out"

    pdf_path = os.path.join(OUTPUT_DIR, f"{piece_name}.pdf")
    if not os.path.exists(pdf_path):
        return None, f"PDF not created at {pdf_path}"

    return pdf_path, None


def pdf_to_jpg(pdf_path, jpg_path):
    """Convert PDF to JPG using sips."""
    # First convert to PNG via sips
    png_path = jpg_path.replace('.jpg', '.png')
    try:
        subprocess.run(
            ["sips", "-s", "format", "png", "--resampleWidth", "1800",
             pdf_path, "--out", png_path],
            capture_output=True, timeout=30
        )
        # Then convert PNG to JPG with Pillow for consistency
        img = Image.open(png_path).convert('RGB')
        img.save(jpg_path, 'JPEG', quality=95, subsampling=0)
        os.remove(png_path)
        return True
    except Exception as e:
        return False


def compare_images(img1_path, img2_path):
    """Compare two images and return similarity score (0-100)."""
    try:
        img1 = Image.open(img1_path).convert('RGB')
        img2 = Image.open(img2_path).convert('RGB')

        # Resize to same dimensions for comparison
        size = (800, 533)  # 3:2 aspect
        img1 = img1.resize(size, Image.LANCZOS)
        img2 = img2.resize(size, Image.LANCZOS)

        arr1 = np.array(img1, dtype=np.float32)
        arr2 = np.array(img2, dtype=np.float32)

        # Mean absolute difference per pixel per channel
        diff = np.abs(arr1 - arr2).mean()
        # Convert to similarity percentage (0 diff = 100%, 255 diff = 0%)
        similarity = max(0, 100 * (1 - diff / 255))
        return similarity
    except Exception as e:
        return -1


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    render_dir = os.path.join(BASE, "review_flagged", "batch_compare")
    os.makedirs(render_dir, exist_ok=True)

    results = []
    total = len(PIECES)

    for idx, (series, piece_name) in enumerate(PIECES):
        print(f"[{idx+1}/{total}] {piece_name}...", end=" ", flush=True)

        # 1. Render
        pdf_path, err = render_piece(series, piece_name)
        if err:
            print(f"RENDER ERROR: {err}")
            results.append((piece_name, "RENDER_ERROR", err))
            continue

        # 2. Convert to JPG
        new_jpg = os.path.join(render_dir, f"{piece_name}.jpg")
        if not pdf_to_jpg(pdf_path, new_jpg):
            print("CONVERT ERROR")
            results.append((piece_name, "CONVERT_ERROR", ""))
            continue

        # 3. Compare with curated JPG
        curated_jpg = os.path.join(PRINTS_DIR, series, f"{piece_name}.jpg")
        if not os.path.exists(curated_jpg):
            print("NO CURATED JPG")
            results.append((piece_name, "NO_REFERENCE", ""))
            continue

        similarity = compare_images(new_jpg, curated_jpg)
        status = "MATCH" if similarity > 95 else "CLOSE" if similarity > 85 else "DIFFERENT"
        print(f"{status} ({similarity:.1f}%)")
        results.append((piece_name, status, f"{similarity:.1f}%"))

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    matches = sum(1 for _, s, _ in results if s == "MATCH")
    close = sum(1 for _, s, _ in results if s == "CLOSE")
    diff = sum(1 for _, s, _ in results if s == "DIFFERENT")
    errors = sum(1 for _, s, _ in results if "ERROR" in s or s == "NO_REFERENCE")
    print(f"MATCH (>95%):     {matches}")
    print(f"CLOSE (85-95%):   {close}")
    print(f"DIFFERENT (<85%): {diff}")
    print(f"ERRORS:           {errors}")

    # List non-matches
    if close + diff + errors > 0:
        print("\nNON-MATCHES:")
        for name, status, detail in results:
            if status != "MATCH":
                print(f"  {status:15s} {name:40s} {detail}")

    # Save results
    results_path = os.path.join(render_dir, "comparison_results.txt")
    with open(results_path, 'w') as f:
        for name, status, detail in results:
            f.write(f"{status}\t{name}\t{detail}\n")
    print(f"\nResults saved to {results_path}")


if __name__ == '__main__':
    main()
