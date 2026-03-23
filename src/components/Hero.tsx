"use client";

import Image from "next/image";
import { useState, useEffect, useRef, useCallback } from "react";
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
  const [nextIndex, setNextIndex] = useState<number | null>(null);
  const [fadeIn, setFadeIn] = useState(false);

  // Refs to avoid stale closures in the interval
  const currentRef = useRef(currentIndex);
  const transitioningRef = useRef(false);
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  currentRef.current = currentIndex;

  const goTo = useCallback((target: number) => {
    if (transitioningRef.current) return;
    if (target === currentRef.current) return;
    transitioningRef.current = true;
    setNextIndex(target);
    // Double rAF so the next-image element renders at opacity-0 first
    requestAnimationFrame(() => {
      requestAnimationFrame(() => setFadeIn(true));
    });
    timeoutRef.current = setTimeout(() => {
      setCurrentIndex(target);
      currentRef.current = target;
      setNextIndex(null);
      setFadeIn(false);
      transitioningRef.current = false;
    }, 2000);
  }, []);

  const startAutoplay = useCallback(() => {
    if (intervalRef.current) clearInterval(intervalRef.current);
    intervalRef.current = setInterval(() => {
      const next = (currentRef.current + 1) % slides.length;
      goTo(next);
    }, 6000);
  }, [goTo]);

  // Start autoplay on mount
  useEffect(() => {
    startAutoplay();
    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
      if (timeoutRef.current) clearTimeout(timeoutRef.current);
    };
  }, [startAutoplay]);

  const handleDotClick = (i: number) => {
    goTo(i);
    startAutoplay(); // reset timer
  };

  const current = slides[currentIndex];
  const next = nextIndex !== null ? slides[nextIndex] : null;

  const textClasses =
    current.textColor === "white" ? "text-white/80" : "text-black/80";
  const dotActive =
    current.textColor === "white" ? "bg-white/80" : "bg-black/60";
  const dotInactive =
    current.textColor === "white" ? "bg-white/30" : "bg-black/20";

  return (
    <section className="relative h-screen w-full overflow-hidden bg-primary">
      {/* Layer A: current image — always fully visible */}
      <div className="absolute inset-0">
        <Image
          src={current.piece.imageUrl}
          alt={current.piece.title}
          fill
          className="object-cover object-center"
          priority
          style={{ backgroundColor: current.piece.background }}
        />
        <div className="absolute inset-0 bg-black/20" />
      </div>

      {/* Layer B: next image — fades in on top, then unmounts */}
      {next && (
        <div
          className={`absolute inset-0 transition-opacity duration-[2000ms] ${
            fadeIn ? "opacity-100" : "opacity-0"
          }`}
        >
          <Image
            src={next.piece.imageUrl}
            alt={next.piece.title}
            fill
            className="object-cover object-center"
            style={{ backgroundColor: next.piece.background }}
          />
          <div className="absolute inset-0 bg-black/20" />
        </div>
      )}

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
