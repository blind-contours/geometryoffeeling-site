import Image from "next/image";
import Link from "next/link";
import { notFound } from "next/navigation";
import EquationLabel from "@/components/EquationLabel";
import PrintCard from "@/components/PrintCard";
import {
  allPieces,
  getPieceBySlug,
  getSeriesBySlug,
  getPiecesBySeries,
} from "@/data/series";
import type { Metadata } from "next";

interface Props {
  params: { slug: string };
}

export function generateStaticParams() {
  return allPieces.map((p) => ({ slug: p.id }));
}

export function generateMetadata({ params }: Props): Metadata {
  const piece = getPieceBySlug(params.slug);
  if (!piece) return { title: "Piece Not Found" };
  return {
    title: `${piece.title} — Geometry of Feeling`,
    description: piece.description,
  };
}

export default function PiecePage({ params }: Props) {
  const piece = getPieceBySlug(params.slug);
  if (!piece) notFound();

  const s = getSeriesBySlug(piece.series);
  const relatedPieces = getPiecesBySeries(piece.series).filter(
    (p) => p.id !== piece.id
  );

  return (
    <div className="pt-20 pb-16">
      {/* Full-width image */}
      <div
        className="w-full max-w-5xl mx-auto px-6 mb-12"
        style={{ backgroundColor: piece.background }}
      >
        <Image
          src={piece.imageUrl}
          alt={`${piece.title} — ${piece.equation}`}
          width={1680}
          height={1155}
          className="w-full h-auto"
          priority
        />
      </div>

      <div className="max-w-content mx-auto px-6">
        <div className="max-w-2xl">
          {/* Title and equation */}
          <h1 className="text-2xl font-mono font-light text-primary mb-2">
            {piece.title}
          </h1>
          <EquationLabel
            equation={piece.equation}
            className="text-sm mb-8"
          />

          {/* Description */}
          <p className="text-body text-secondary mb-4">{piece.description}</p>
          <p className="text-body text-muted italic mb-8">
            {piece.emotionalNote}
          </p>

          {/* Series link */}
          {s && (
            <p className="text-caption text-secondary mb-8">
              Part of:{" "}
              <Link
                href={`/series/${s.id}`}
                className="text-primary hover:opacity-70 transition-opacity duration-500 underline underline-offset-4"
              >
                {s.name}
              </Link>
            </p>
          )}

          {/* Buy options */}
          <div className="border border-border p-6 mb-16">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              <div>
                <p className="text-headline text-primary">
                  Digital Download
                </p>
                <p className="text-caption text-secondary">
                  High-resolution PDF, 300 DPI, print-ready
                </p>
              </div>
              <div className="flex items-center gap-4">
                <span className="text-lg font-mono text-primary">
                  ${piece.price}
                </span>
                <a
                  href={piece.gumroadUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="px-6 py-3 border border-primary text-caption uppercase tracking-widest text-primary hover:bg-primary hover:text-bg transition-colors duration-500"
                >
                  Purchase
                </a>
              </div>
            </div>
            {s && (
              <div className="mt-4 pt-4 border-t border-border">
                <Link
                  href={`/series/${s.id}`}
                  className="text-caption text-secondary hover:text-primary transition-colors duration-500"
                >
                  Or get the complete {s.name} series for ${s.bundlePrice}{" "}
                  &rarr;
                </Link>
              </div>
            )}
          </div>
        </div>

        {/* Related pieces */}
        {relatedPieces.length > 0 && (
          <div>
            <h2 className="text-headline uppercase tracking-widest text-primary mb-8">
              More from {s?.name}
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6">
              {relatedPieces.map((p) => (
                <PrintCard key={p.id} piece={p} />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
