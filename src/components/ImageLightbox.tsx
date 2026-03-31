"use client";

import Image from "next/image";
import { useState, useEffect } from "react";

interface ImageLightboxProps {
  src: string;
  alt: string;
  width: number;
  height: number;
  background?: string;
}

export default function ImageLightbox({
  src,
  alt,
  width,
  height,
  background,
}: ImageLightboxProps) {
  const [open, setOpen] = useState(false);

  useEffect(() => {
    if (!open) return;
    const handleKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") setOpen(false);
    };
    document.body.style.overflow = "hidden";
    window.addEventListener("keydown", handleKey);
    return () => {
      document.body.style.overflow = "";
      window.removeEventListener("keydown", handleKey);
    };
  }, [open]);

  return (
    <>
      <div className="relative cursor-zoom-in" onClick={() => setOpen(true)}>
        <Image
          src={src}
          alt={alt}
          width={width}
          height={height}
          quality={90}
          className="w-full h-auto"
          priority
          style={{ backgroundColor: background }}
        />
        <span className="absolute bottom-3 right-3 text-caption bg-black/50 text-white/80 px-2 py-1 rounded md:hidden">
          Tap to zoom
        </span>
      </div>

      {open && (
        <div
          className="fixed inset-0 z-50 bg-black/95 flex items-start justify-center overflow-auto"
          onClick={() => setOpen(false)}
        >
          <button
            onClick={() => setOpen(false)}
            className="fixed top-4 right-4 z-50 min-w-[44px] min-h-[44px] flex items-center justify-center text-black text-3xl font-bold hover:text-black/70"
            aria-label="Close lightbox"
          >
            &times;
          </button>
          <div
            className="min-w-[200vw] md:min-w-0 md:max-w-[90vw] md:my-8"
            onClick={(e) => e.stopPropagation()}
          >
            <Image
              src={src}
              alt={alt}
              width={width * 2}
              height={height * 2}
              unoptimized
              className="w-full h-auto"
              style={{ backgroundColor: background }}
            />
          </div>
        </div>
      )}
    </>
  );
}
