"use client";

import { useEffect, useRef, useState } from "react";
import Image from "next/image";

interface PdfCanvasProps {
  url: string;
  background?: string;
  fallbackSrc: string;
  fallbackAlt: string;
  fallbackWidth: number;
  fallbackHeight: number;
}

export default function PdfCanvas({
  url,
  background,
  fallbackSrc,
  fallbackAlt,
  fallbackWidth,
  fallbackHeight,
}: PdfCanvasProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [status, setStatus] = useState<"loading" | "ready" | "error">("loading");

  useEffect(() => {
    let cancelled = false;

    async function renderPdf() {
      try {
        const pdfjsLib = await import("pdfjs-dist");
        pdfjsLib.GlobalWorkerOptions.workerSrc = "/pdf.worker.min.mjs";

        const loadingTask = pdfjsLib.getDocument({
          url,
          disableAutoFetch: false,
          enableXfa: false,
        });
        const pdf = await loadingTask.promise;
        if (cancelled) return;

        const page = await pdf.getPage(1);
        if (cancelled) return;

        const canvas = canvasRef.current;
        if (!canvas) return;

        // Render at 3x scale for maximum crispness
        const viewport = page.getViewport({ scale: 3 });

        canvas.width = viewport.width;
        canvas.height = viewport.height;

        const ctx = canvas.getContext("2d");
        if (!ctx) return;

        const renderTask = page.render({
          canvasContext: ctx,
          viewport,
          canvas,
        });
        await renderTask.promise;
        if (!cancelled) setStatus("ready");
      } catch (err) {
        console.error("PDF render failed:", err);
        if (!cancelled) setStatus("error");
      }
    }

    renderPdf();
    return () => { cancelled = true; };
  }, [url]);

  if (status === "error") {
    return (
      <Image
        src={fallbackSrc}
        alt={fallbackAlt}
        width={fallbackWidth}
        height={fallbackHeight}
        unoptimized
        className="w-full h-auto"
        style={{ backgroundColor: background }}
      />
    );
  }

  return (
    <div className="w-full" style={{ backgroundColor: background }}>
      {status === "loading" && (
        <div className="flex items-center justify-center py-40">
          <div className="text-white/50 text-sm">Loading high-res view...</div>
        </div>
      )}
      <canvas
        ref={canvasRef}
        className="w-full h-auto"
        style={{ display: status === "loading" ? "none" : "block" }}
      />
    </div>
  );
}
