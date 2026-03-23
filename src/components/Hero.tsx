"use client";

import Image from "next/image";
import { useState, useEffect, useCallback } from "react";
import { series } from "@/data/series";

// Pick one piece from every other series for visual variety
const heroImages = series
  .filter((_, i) => i % 3 === 0)
  .map((s) => s.pieces[0])
  .slice(0, 8);

export default function Hero() {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isTransitioning, setIsTransitioning] = useState(false);

  const advance = useCallback(() => {
    setIsTransitioning(true);
    setTimeout(() => {
      setCurrentIndex((prev) => (prev + 1) % heroImages.length);
      setIsTransitioning(false);
    }, 2000);
  }, []);

  useEffect(() => {
    const interval = setInterval(advance, 8000);
    return () => clearInterval(interval);
  }, [advance]);

  const current = heroImages[currentIndex];

  return (
    <section className="relative h-screen w-full overflow-hidden bg-primary">
      <div
        className={`absolute inset-0 transition-opacity duration-[2000ms] ${
          isTransitioning ? "opacity-0" : "opacity-100"
        }`}
      >
        <Image
          src={current.imageUrl}
          alt={current.title}
          fill
          className="object-cover"
          priority
          style={{ backgroundColor: current.background }}
        />
        <div className="absolute inset-0 bg-black/20" />
      </div>

      <div className="absolute inset-0 flex items-center justify-center">
        <h1 className="text-white/80 text-lg md:text-2xl font-mono font-light tracking-[0.15em] text-center px-6">
          The geometry of feeling.
        </h1>
      </div>

      <div className="absolute bottom-8 left-0 right-0 flex justify-center">
        <div className="flex gap-2">
          {heroImages.map((_, i) => (
            <button
              key={i}
              onClick={() => {
                setIsTransitioning(true);
                setTimeout(() => {
                  setCurrentIndex(i);
                  setIsTransitioning(false);
                }, 2000);
              }}
              className={`w-1.5 h-1.5 rounded-full transition-opacity duration-500 ${
                i === currentIndex ? "bg-white/80" : "bg-white/30"
              }`}
              aria-label={`Show image ${i + 1}`}
            />
          ))}
        </div>
      </div>
    </section>
  );
}
