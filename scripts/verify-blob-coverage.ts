/**
 * Verify that every piece on the site has:
 * 1. A matching PDF in Vercel Blob storage
 * 2. A matching JPG in public/prints/
 *
 * Also generates an HTML review page for visual comparison.
 *
 * Usage:
 *   BLOB_READ_WRITE_TOKEN=vercel_blob_rw_... npx tsx scripts/verify-blob-coverage.ts
 */

import { list } from "@vercel/blob";
import { existsSync, writeFileSync } from "fs";
import { join } from "path";

// Extract piece data from series.ts at runtime
async function getAllPieces() {
  const { series } = await import("../src/data/series");
  return series.flatMap((s) =>
    s.pieces.map((p) => ({
      id: p.id,
      title: p.title,
      series: s.id,
      seriesName: s.name,
      imageUrl: p.imageUrl,
      blobKey: p.id.replace(/-/g, "_"),
    }))
  );
}

async function main() {
  if (!process.env.BLOB_READ_WRITE_TOKEN) {
    console.error("Set BLOB_READ_WRITE_TOKEN before running this script.");
    process.exit(1);
  }

  const pieces = await getAllPieces();
  console.log(`Found ${pieces.length} pieces in series.ts\n`);

  // Fetch all blobs from store
  const allBlobs = new Map<string, string>();
  let cursor: string | undefined;
  do {
    const result = await list({ prefix: "prints/", limit: 500, cursor });
    for (const blob of result.blobs) {
      allBlobs.set(blob.pathname, blob.url);
    }
    cursor = result.hasMore ? result.cursor : undefined;
  } while (cursor);

  console.log(`Found ${allBlobs.size} files in blob store\n`);

  const missing: { piece: string; issue: string }[] = [];
  const matched: {
    id: string;
    title: string;
    series: string;
    seriesName: string;
    jpgPath: string;
    jpgExists: boolean;
    blobUrl: string | null;
    imageUrl: string;
  }[] = [];

  for (const piece of pieces) {
    const blobPath = `prints/${piece.blobKey}.pdf`;
    const blobUrl = allBlobs.get(blobPath) || null;
    const jpgPath = join(process.cwd(), "public", piece.imageUrl);
    const jpgExists = existsSync(jpgPath);

    if (!blobUrl) {
      missing.push({ piece: piece.id, issue: `No blob PDF (expected ${blobPath})` });
    }
    if (!jpgExists) {
      missing.push({ piece: piece.id, issue: `No JPG at ${piece.imageUrl}` });
    }

    matched.push({
      id: piece.id,
      title: piece.title,
      series: piece.series,
      seriesName: piece.seriesName,
      jpgPath: piece.imageUrl,
      jpgExists,
      blobUrl,
      imageUrl: piece.imageUrl,
    });
  }

  // Report
  if (missing.length === 0) {
    console.log("ALL PIECES HAVE MATCHING BLOB PDF AND JPG\n");
  } else {
    console.log(`MISSING FILES (${missing.length}):`);
    for (const m of missing) {
      console.log(`  ${m.piece}: ${m.issue}`);
    }
    console.log();
  }

  // Summary by series
  const bySeries = new Map<string, { total: number; withBlob: number; withJpg: number }>();
  for (const m of matched) {
    const s = bySeries.get(m.seriesName) || { total: 0, withBlob: 0, withJpg: 0 };
    s.total++;
    if (m.blobUrl) s.withBlob++;
    if (m.jpgExists) s.withJpg++;
    bySeries.set(m.seriesName, s);
  }

  console.log("Series coverage:");
  for (const [name, s] of bySeries) {
    const blobOk = s.withBlob === s.total ? "OK" : `${s.withBlob}/${s.total}`;
    const jpgOk = s.withJpg === s.total ? "OK" : `${s.withJpg}/${s.total}`;
    console.log(`  ${name.padEnd(20)} Blob: ${blobOk.padEnd(6)} JPG: ${jpgOk}`);
  }

  // Generate HTML review page
  const html = generateReviewPage(matched);
  const outPath = join(process.cwd(), "review_flagged", "blob_review.html");
  writeFileSync(outPath, html);
  console.log(`\nReview page: ${outPath}`);
  console.log("Open in browser to visually compare JPGs (site) vs PDFs (blob)");
}

function generateReviewPage(
  pieces: {
    id: string;
    title: string;
    series: string;
    seriesName: string;
    jpgPath: string;
    jpgExists: boolean;
    blobUrl: string | null;
    imageUrl: string;
  }[]
) {
  const rows = pieces
    .map(
      (p) => `
    <div class="piece ${!p.blobUrl ? "missing-blob" : ""} ${!p.jpgExists ? "missing-jpg" : ""}" data-series="${p.series}">
      <div class="header">
        <span class="series-tag">${p.seriesName}</span>
        <span class="title">${p.title}</span>
        <span class="id">${p.id}</span>
        ${!p.blobUrl ? '<span class="badge bad">NO BLOB</span>' : '<span class="badge good">BLOB OK</span>'}
        ${!p.jpgExists ? '<span class="badge bad">NO JPG</span>' : ""}
      </div>
      <div class="images">
        <div class="img-col">
          <div class="label">Website JPG</div>
          ${p.jpgExists ? `<img src="../public${p.imageUrl}" loading="lazy" />` : '<div class="placeholder">MISSING</div>'}
        </div>
        <div class="img-col">
          <div class="label">Blob PDF <a href="${p.blobUrl || "#"}" target="_blank" style="color:#8af;font-size:11px;">(open in new tab)</a></div>
          ${p.blobUrl ? `<embed src="${p.blobUrl}" type="application/pdf" class="pdf-embed" />` : '<div class="placeholder">MISSING</div>'}
        </div>
      </div>
    </div>`
    )
    .join("\n");

  return `<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Blob Coverage Review</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: -apple-system, system-ui, sans-serif; background: #111; color: #eee; padding: 20px; }
  h1 { margin-bottom: 10px; }
  .stats { margin-bottom: 20px; color: #aaa; }
  .filters { margin-bottom: 20px; display: flex; gap: 8px; flex-wrap: wrap; }
  .filters button { padding: 6px 14px; border: 1px solid #444; background: #222; color: #ccc; border-radius: 4px; cursor: pointer; font-size: 13px; }
  .filters button.active { background: #446; border-color: #668; color: #fff; }
  .filter-issues { padding: 6px 14px; border: 1px solid #844; background: #422; color: #faa; border-radius: 4px; cursor: pointer; font-size: 13px; }
  .filter-issues.active { background: #644; border-color: #a66; }
  .piece { border: 1px solid #333; border-radius: 8px; margin-bottom: 16px; padding: 16px; background: #1a1a1a; }
  .piece.missing-blob { border-color: #a33; }
  .header { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; flex-wrap: wrap; }
  .series-tag { background: #335; padding: 3px 10px; border-radius: 4px; font-size: 12px; text-transform: uppercase; }
  .title { font-size: 18px; font-weight: 600; }
  .id { color: #888; font-size: 13px; font-family: monospace; }
  .badge { padding: 2px 8px; border-radius: 3px; font-size: 11px; font-weight: 600; }
  .badge.good { background: #243; color: #6d6; }
  .badge.bad { background: #432; color: #f66; }
  .images { display: flex; gap: 20px; }
  .img-col { flex: 1; }
  .img-col .label { font-size: 12px; color: #888; margin-bottom: 6px; text-transform: uppercase; }
  .img-col img { width: 100%; border-radius: 4px; }
  .pdf-embed { width: 100%; height: 400px; border-radius: 4px; border: 1px solid #333; }
  .placeholder { padding: 40px; text-align: center; background: #322; border-radius: 4px; color: #f66; }
  .hidden { display: none; }
</style>
</head>
<body>
<h1>Blob Coverage Review</h1>
<div class="stats">${pieces.length} pieces | ${pieces.filter((p) => p.blobUrl).length} with blob | ${pieces.filter((p) => !p.blobUrl).length} missing blob</div>
<div class="filters">
  <button class="active" onclick="filterSeries('all')">All</button>
  <button class="filter-issues" onclick="filterIssues()">Issues Only</button>
  ${[...new Set(pieces.map((p) => p.series))].map((s) => `<button onclick="filterSeries('${s}')">${s}</button>`).join("\n  ")}
</div>
${rows}
<script>
function filterSeries(s) {
  document.querySelectorAll('.piece').forEach(el => {
    el.classList.toggle('hidden', s !== 'all' && el.dataset.series !== s);
  });
  document.querySelectorAll('.filters button').forEach(b => b.classList.remove('active'));
  if (s === 'all') document.querySelector('.filters button').classList.add('active');
  else document.querySelectorAll('.filters button').forEach(b => { if (b.textContent === s) b.classList.add('active'); });
}
function filterIssues() {
  const btn = document.querySelector('.filter-issues');
  const active = btn.classList.toggle('active');
  document.querySelectorAll('.piece').forEach(el => {
    if (active) el.classList.toggle('hidden', !el.classList.contains('missing-blob') && !el.classList.contains('missing-jpg'));
    else el.classList.remove('hidden');
  });
}
</script>
</body>
</html>`;
}

main().catch(console.error);
