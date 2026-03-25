/**
 * Upload high-res print files to Vercel Blob.
 *
 * Usage:
 *   BLOB_READ_WRITE_TOKEN=vercel_blob_... npx tsx scripts/upload-to-blob.ts
 *
 * Expects high-res PDFs in mathematical_affect/{series}/final_series/
 * Uploads each to Vercel Blob keyed by piece ID.
 */

import { put } from "@vercel/blob";
import { readFileSync, readdirSync, existsSync } from "fs";
import { join, basename } from "path";

const BASE_DIR = join(process.cwd(), "mathematical_affect");

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

  const seriesDirs = readdirSync(BASE_DIR, { withFileTypes: true })
    .filter((d) => d.isDirectory())
    .map((d) => d.name);

  let uploaded = 0;

  for (const seriesDir of seriesDirs) {
    const finalDir = join(BASE_DIR, seriesDir, "final_series");
    if (!existsSync(finalDir)) continue;

    const files = readdirSync(finalDir).filter(
      (f) => f.endsWith(".pdf") || f.endsWith(".png") || f.endsWith(".tiff")
    );

    for (const file of files) {
      const filePath = join(finalDir, file);
      const pieceId = basename(file, ".pdf")
        .replace(".png", "")
        .replace(".tiff", "");
      const blobPath = `prints/${pieceId}.pdf`;

      console.log(`Uploading ${filePath} → ${blobPath}`);

      const content = readFileSync(filePath);
      const blob = await put(blobPath, content, {
        access: "private",
        addRandomSuffix: false,
        allowOverwrite: true,
      });

      console.log(`  ✓ ${blob.url}`);
      uploaded++;
    }
  }

  console.log(`\nDone. Uploaded ${uploaded} files.`);
}

main().catch(console.error);
