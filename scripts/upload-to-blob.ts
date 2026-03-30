/**
 * Upload high-res print files to Vercel Blob.
 *
 * Usage:
 *   BLOB_READ_WRITE_TOKEN=vercel_blob_... npx tsx scripts/upload-to-blob.ts
 *
 * Reads PDFs from:
 *   1. mathematical_affect/output/ (standalone script renders)
 *   2. mathematical_affect/{series}/final_series/ (legacy renders, fallback)
 *
 * Uploads each to Vercel Blob keyed by piece ID.
 */

import { put } from "@vercel/blob";
import { readFileSync, readdirSync, existsSync } from "fs";
import { join, basename } from "path";

const BASE_DIR = join(process.cwd(), "mathematical_affect");
const OUTPUT_DIR = join(BASE_DIR, "output");

async function main() {
  if (!process.env.BLOB_READ_WRITE_TOKEN) {
    console.error("Set BLOB_READ_WRITE_TOKEN before running this script.");
    process.exit(1);
  }

  if (!existsSync(BASE_DIR)) {
    console.error(`Directory not found: ${BASE_DIR}`);
    console.error("Run this script from the project root.");
    process.exit(1);
  }

  let uploaded = 0;
  const seen = new Set<string>();

  // 1. Upload from mathematical_affect/output/ (preferred — latest renders)
  if (existsSync(OUTPUT_DIR)) {
    const files = readdirSync(OUTPUT_DIR).filter((f) => f.endsWith(".pdf"));
    for (const file of files) {
      const filePath = join(OUTPUT_DIR, file);
      const pieceId = basename(file, ".pdf");
      const blobPath = `prints/${pieceId}.pdf`;

      console.log(`Uploading ${filePath} → ${blobPath}`);

      const content = readFileSync(filePath);
      const blob = await put(blobPath, content, {
        access: "private",
        addRandomSuffix: false,
        allowOverwrite: true,
      });

      console.log(`  ✓ ${blob.url}`);
      seen.add(pieceId);
      uploaded++;
    }
  }

  // 2. Upload from legacy final_series/ directories (only if not already uploaded)
  const seriesDirs = readdirSync(BASE_DIR, { withFileTypes: true })
    .filter((d) => d.isDirectory())
    .map((d) => d.name);

  for (const seriesDir of seriesDirs) {
    const finalDir = join(BASE_DIR, seriesDir, "final_series");
    if (!existsSync(finalDir)) continue;

    const files = readdirSync(finalDir).filter(
      (f) => f.endsWith(".pdf") || f.endsWith(".png") || f.endsWith(".tiff")
    );

    for (const file of files) {
      const pieceId = basename(file, ".pdf")
        .replace(".png", "")
        .replace(".tiff", "");

      if (seen.has(pieceId)) continue; // Already uploaded from output/

      const filePath = join(finalDir, file);
      const blobPath = `prints/${pieceId}.pdf`;

      console.log(`Uploading (legacy) ${filePath} → ${blobPath}`);

      const content = readFileSync(filePath);
      const blob = await put(blobPath, content, {
        access: "private",
        addRandomSuffix: false,
        allowOverwrite: true,
      });

      console.log(`  ✓ ${blob.url}`);
      seen.add(pieceId);
      uploaded++;
    }
  }

  console.log(`\nDone. Uploaded ${uploaded} files.`);
}

main().catch(console.error);
