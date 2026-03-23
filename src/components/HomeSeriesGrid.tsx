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

      {/* Tight icon grid */}
      <div className="group/grid relative">
        <div
          className="grid gap-0 transition-all duration-700"
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
