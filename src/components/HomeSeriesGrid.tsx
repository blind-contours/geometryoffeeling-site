"use client";

import Image from "next/image";
import Link from "next/link";
import { useState } from "react";
import type { Series } from "@/data/series";

interface HomeSeriesGridProps {
  series: Series;
  index: number;
}

export default function HomeSeriesGrid({ series, index }: HomeSeriesGridProps) {
  const [hoveredPiece, setHoveredPiece] = useState<string | null>(null);
  const isRight = index % 2 === 1;

  return (
    <div
      className={`flex flex-col ${
        isRight ? "md:items-end" : "md:items-start"
      } mb-24`}
    >
      <div className={`max-w-2xl ${isRight ? "md:text-right" : "md:text-left"}`}>
        <h3 className="text-headline uppercase tracking-widest text-primary mb-1">
          {series.name}
        </h3>
        <p className="text-body text-secondary italic mb-6">{series.tagline}</p>
      </div>

      {/* Desktop: tight grid / Mobile: horizontal scroll */}
      <div className="group/grid relative w-full">
        {/* Desktop grid */}
        <div
          className="hidden md:grid gap-0 transition-all duration-700"
          style={{
            gridTemplateColumns: `repeat(${Math.min(series.pieces.length, 5)}, 1fr)`,
          }}
        >
          {series.pieces.map((piece) => (
            <Link
              key={piece.id}
              href={`/piece/${piece.id}`}
              className="relative block"
              onMouseEnter={() => setHoveredPiece(piece.id)}
              onMouseLeave={() => setHoveredPiece(null)}
            >
              <div
                className={`relative overflow-hidden transition-transform duration-500 ${
                  hoveredPiece === piece.id ? "scale-105 z-10" : ""
                }`}
                style={{ backgroundColor: series.background }}
              >
                <Image
                  src={piece.imageUrl}
                  alt={`${piece.title} — ${piece.equation}`}
                  width={240}
                  height={165}
                  className="w-full h-auto block"
                />
              </div>
              {hoveredPiece === piece.id && (
                <p className="absolute -bottom-6 left-0 right-0 text-center text-caption text-secondary whitespace-nowrap">
                  {piece.title}
                </p>
              )}
            </Link>
          ))}
        </div>

        {/* Mobile: horizontal scroll row */}
        <div className="md:hidden relative">
          <div className="flex overflow-x-auto gap-3 scrollbar-hide -mx-6 px-6 snap-x snap-mandatory">
            {series.pieces.map((piece) => (
              <Link
                key={piece.id}
                href={`/piece/${piece.id}`}
                className="flex-shrink-0 block snap-start"
                style={{ width: "65vw" }}
              >
                <div
                  className="overflow-hidden"
                  style={{ backgroundColor: series.background }}
                >
                  <Image
                    src={piece.imageUrl}
                    alt={`${piece.title} — ${piece.equation}`}
                    width={240}
                    height={165}
                    className="w-full h-auto block"
                  />
                </div>
                <p className="text-center text-caption text-secondary mt-1 truncate px-1">
                  {piece.title}
                </p>
              </Link>
            ))}
          </div>
          {/* Right-edge gradient to signal scrollability */}
          <div className="absolute right-0 top-0 bottom-6 w-8 bg-gradient-to-l from-bg to-transparent pointer-events-none" />
        </div>
      </div>

      <div className={`mt-10 ${isRight ? "md:text-right" : ""}`}>
        <Link
          href={`/series/${series.id}`}
          className="text-caption uppercase tracking-widest text-secondary hover:text-primary transition-colors duration-500"
        >
          Explore series &rarr;
        </Link>
      </div>
    </div>
  );
}
