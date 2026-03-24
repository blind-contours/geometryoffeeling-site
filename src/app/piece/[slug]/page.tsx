import Link from "next/link";
import { notFound } from "next/navigation";
import EquationLabel from "@/components/EquationLabel";
import PrintCard from "@/components/PrintCard";
import LicenseTerms from "@/components/LicenseTerms";
import ImageLightbox from "@/components/ImageLightbox";
import StickyBuyButton from "@/components/StickyBuyButton";
import BuySection from "@/components/BuySection";
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
    openGraph: {
      title: `${piece.title} — Geometry of Feeling`,
      description: piece.description,
      images: [{ url: piece.imageUrl, width: 1680, height: 1155 }],
    },
    twitter: {
      card: "summary_large_image",
      title: `${piece.title} — Geometry of Feeling`,
      description: piece.description,
      images: [piece.imageUrl],
    },
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
    <div className="pt-20 pb-24 md:pb-16">
      {/* Full-width image with lightbox */}
      <div
        className="w-full max-w-5xl mx-auto md:px-6 mb-12"
        style={{ backgroundColor: piece.background }}
      >
        <ImageLightbox
          src={piece.imageUrl}
          alt={`${piece.title} — ${piece.equation}`}
          width={1680}
          height={1155}
          background={piece.background}
        />
      </div>

      <div className="max-w-content mx-auto px-6">
        <div className="max-w-2xl">
          {/* Title and emotional note */}
          <h1 className="text-2xl font-mono font-light text-primary mb-2">
            {piece.title}
          </h1>
          <p className="text-body text-muted italic mb-8">
            {piece.emotionalNote}
          </p>

          {/* Description and equation */}
          <p className="text-body text-secondary mb-4">{piece.description}</p>
          <EquationLabel equation={piece.equation} className="text-sm mb-8" />

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
          <BuySection pieceId={piece.id} />

          {/* Custom piece CTA */}
          <div className="border border-border px-6 py-4 mb-8">
            <p className="text-body text-secondary">
              Want this piece in different colors or dimensions?{" "}
              <Link
                href={`/custom?piece=${piece.id}`}
                className="text-primary underline underline-offset-4 hover:opacity-70 transition-opacity duration-500"
              >
                Commission a custom version
              </Link>
            </p>
          </div>

          {s && (
            <p className="text-caption text-secondary mb-4">
              <Link
                href={`/series/${s.id}`}
                className="hover:text-primary transition-colors duration-500"
              >
                Browse the complete {s.name} series &rarr;
              </Link>
            </p>
          )}

          <div className="mb-8">
            <LicenseTerms compact />
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

      <StickyBuyButton pieceId={piece.id} title={piece.title} />
    </div>
  );
}
