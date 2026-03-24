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
import { PRINT_SIZES } from "@/lib/products";
import type { Metadata } from "next";

const baseUrl =
  process.env.NEXT_PUBLIC_URL || "https://geometryoffeeling.com";

interface Props {
  params: { slug: string };
}

export function generateStaticParams() {
  return allPieces.map((p) => ({ slug: p.id }));
}

export function generateMetadata({ params }: Props): Metadata {
  const piece = getPieceBySlug(params.slug);
  if (!piece) return { title: "Piece Not Found" };
  const s = getSeriesBySlug(piece.series);
  const seriesName = s?.name ?? piece.series;
  const description = `${piece.title} — a minimalist fine art print from the ${seriesName} series. ${piece.description} Museum-quality giclée on Hahnemühle German Etching. From $45.`;
  const title = `${piece.title} — Minimalist Mathematical Art Print | Geometry of Feeling`;
  return {
    title,
    description,
    openGraph: {
      title,
      description,
      images: [{ url: piece.imageUrl, width: 1680, height: 1155 }],
    },
    twitter: {
      card: "summary_large_image",
      title,
      description,
      images: [piece.imageUrl],
    },
  };
}

export default function PiecePage({ params }: Props) {
  const piece = getPieceBySlug(params.slug);
  if (!piece) notFound();

  const s = getSeriesBySlug(piece.series);
  const seriesName = s?.name ?? piece.series;
  const relatedPieces = getPiecesBySeries(piece.series).filter(
    (p) => p.id !== piece.id
  );

  const lowPrice = (Math.min(...PRINT_SIZES.map((sz) => sz.priceCents)) / 100).toFixed(2);
  const highPrice = (Math.max(...PRINT_SIZES.map((sz) => sz.priceCents)) / 100).toFixed(2);

  const pieceJsonLd = {
    "@context": "https://schema.org",
    "@type": ["Product", "VisualArtwork"],
    name: `${piece.title} — Mathematical Fine Art Print`,
    description: `Minimalist fine art print of ${piece.title.toLowerCase()} from the ${seriesName} series. ${piece.emotionalNote}. ${piece.description} Part of the ${seriesName} series exploring ${s?.emotion ?? "emotion"} through mathematics.`,
    image: `${baseUrl}${piece.imageUrl}`,
    artform: "Print",
    artMedium: "Giclée print on Hahnemühle German Etching 310gsm",
    creator: { "@type": "Person", name: "David McCoy" },
    brand: { "@type": "Brand", name: "Geometry of Feeling" },
    offers: {
      "@type": "AggregateOffer",
      lowPrice,
      highPrice,
      priceCurrency: "USD",
      availability: "https://schema.org/InStock",
      offerCount: PRINT_SIZES.length,
    },
    keywords: `minimalist fine art print, abstract wall art, ${s?.emotion ?? ""}, ${piece.title.toLowerCase()}, equation art, mathematical art`,
  };

  return (
    <div className="pt-20 pb-24 md:pb-16">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(pieceJsonLd) }}
      />
      {/* Full-width image with lightbox */}
      <div
        className="w-full max-w-5xl mx-auto md:px-6 mb-12"
        style={{ backgroundColor: piece.background }}
      >
        <ImageLightbox
          src={piece.imageUrl}
          alt={`${piece.title} — minimalist mathematical fine art print exploring ${s?.emotion ?? "emotion"}, from the ${seriesName} series by Geometry of Feeling`}
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
