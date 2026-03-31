"use client";

import { useEffect, useRef, useState } from "react";

interface PdfCanvasProps {
  url: string;
  background?: string;
}

export default function PdfCanvas({ url, background }: PdfCanvasProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    let cancelled = false;

    async function renderPdf() {
      try {
        const pdfjsLib = await import("pdfjs-dist");
        pdfjsLib.GlobalWorkerOptions.workerSrc = `https://cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjsLib.version}/pdf.worker.min.mjs`;

        const pdf = await pdfjsLib.getDocument(url).promise;
        if (cancelled) return;

        const page = await pdf.getPage(1);
        if (cancelled) return;

        const canvas = canvasRef.current;
        if (!canvas) return;

        // Scale to fit viewport width while maintaining aspect ratio
        // Use 2x for retina sharpness
        const baseScale = 2;
        const viewport = page.getViewport({ scale: baseScale });

        canvas.width = viewport.width;
        canvas.height = viewport.height;

        const ctx = canvas.getContext("2d");
        if (!ctx) return;

        await page.render({ canvasContext: ctx, viewport, canvas }).promise;
        if (!cancelled) setLoading(false);
      } catch {
        if (!cancelled) {
          setError(true);
          setLoading(false);
        }
      }
    }

    renderPdf();
    return () => { cancelled = true; };
  }, [url]);

  if (error) return null;

  return (
    <div className="w-full" style={{ backgroundColor: background }}>
      {loading && (
        <div className="flex items-center justify-center py-40">
          <div className="text-white/50 text-sm">Loading high-res view...</div>
        </div>
      )}
      <canvas
        ref={canvasRef}
        className="w-full h-auto"
        style={{ display: loading ? "none" : "block" }}
      />
    </div>
  );
}
