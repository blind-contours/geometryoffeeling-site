"use client";

import Image from "next/image";
import Link from "next/link";
import { useState, useEffect, useRef } from "react";
import { heroSlides, getPieceBySlug } from "@/data/series";
import type { Piece } from "@/data/series";

interface ResolvedSlide {
  piece: Piece;
  textColor: "white" | "black";
}

const slides: ResolvedSlide[] = heroSlides
  .map((s) => ({ piece: getPieceBySlug(s.pieceId)!, textColor: s.textColor }))
  .filter((s) => s.piece);

export default function Hero() {
  const [currentIndex, setCurrentIndex] = useState(0);
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const startAutoplay = () => {
    if (intervalRef.current) clearInterval(intervalRef.current);
    intervalRef.current = setInterval(() => {
      setCurrentIndex((prev) => (prev + 1) % slides.length);
    }, 6000);
  };

  useEffect(() => {
    startAutoplay();
    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleDotClick = (i: number) => {
    setCurrentIndex(i);
    startAutoplay();
  };

  const current = slides[currentIndex];
  const textClasses =
    current.textColor === "white" ? "text-white/80" : "text-black/80";
  const dotActive =
    current.textColor === "white" ? "bg-white/80" : "bg-black/60";
  const dotInactive =
    current.textColor === "white" ? "bg-white/30" : "bg-black/20";

  return (
    <section className="relative h-screen w-full overflow-hidden bg-primary">
      {/* All slides stacked — only current is visible */}
      {slides.map((slide, i) => (
        <div
          key={slide.piece.id}
          className={`absolute inset-0 transition-opacity duration-[2000ms] ${
            i === currentIndex ? "opacity-100" : "opacity-0"
          }`}
        >
          <Image
            src={slide.piece.imageUrl}
            alt={slide.piece.title}
            fill
            className="object-cover object-center"
            priority={i === 0}
            style={{ backgroundColor: slide.piece.background }}
          />
          <div className="absolute inset-0 bg-black/20" />
        </div>
      ))}

      {/* Title + equation */}
      <div className="absolute inset-0 flex items-center justify-center">
        <div className="text-center px-6">
          <h1
            className={`${textClasses} text-2xl md:text-4xl font-mono font-light tracking-[0.15em] transition-colors duration-[2000ms]`}
          >
            The geometry of feeling.
          </h1>
          <p
            key={current.piece.id}
            className={`${textClasses} text-caption mt-4 tracking-widest opacity-0 animate-[fadeIn_1s_ease-in_forwards]`}
          >
            {current.piece.equation}
          </p>
          <Link
            href="/shop"
            className={`inline-block mt-8 px-8 py-3 border ${
              current.textColor === "white"
                ? "border-white/60 text-white/80 hover:bg-white/10"
                : "border-black/40 text-black/80 hover:bg-black/5"
            } text-caption uppercase tracking-widest transition-all duration-500`}
          >
            Shop Prints
          </Link>
        </div>
      </div>

      {/* Navigation dots */}
      <div className="absolute bottom-8 left-0 right-0 flex justify-center">
        <div className="flex gap-1">
          {slides.map((_, i) => (
            <button
              key={i}
              onClick={() => handleDotClick(i)}
              className="w-11 h-11 flex items-center justify-center"
              aria-label={`Show image ${i + 1}`}
            >
              <span
                className={`block w-2 h-2 rounded-full transition-all duration-500 ${
                  i === currentIndex ? dotActive : dotInactive
                }`}
              />
            </button>
          ))}
        </div>
      </div>
    </section>
  );
}
