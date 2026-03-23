import { notFound } from "next/navigation";
import PrintCard from "@/components/PrintCard";
import LicenseTerms from "@/components/LicenseTerms";
import { series, getSeriesBySlug } from "@/data/series";
import type { Metadata } from "next";

interface Props {
  params: { slug: string };
}

export function generateStaticParams() {
  return series.map((s) => ({ slug: s.id }));
}

export function generateMetadata({ params }: Props): Metadata {
  const s = getSeriesBySlug(params.slug);
  if (!s) return { title: "Series Not Found" };
  return {
    title: `${s.name} — Geometry of Feeling`,
    description: s.description,
  };
}

export default function SeriesPage({ params }: Props) {
  const s = getSeriesBySlug(params.slug);
  if (!s) notFound();

  return (
    <div className="pt-28 pb-16">
      <div className="max-w-content mx-auto px-6">
        {/* Series header */}
        <div className="mb-16">
          <h1 className="text-2xl md:text-3xl font-mono font-light uppercase tracking-widest text-primary mb-4">
            {s.name}
          </h1>
          <p className="text-body text-secondary italic max-w-2xl mb-6">
            {s.tagline}
          </p>
          <p className="text-body text-secondary max-w-2xl mb-4">
            {s.description}
          </p>
          <p className="text-caption text-muted">{s.makingOf}</p>
        </div>

        {/* Pieces grid — 2-up on desktop */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12 mb-20">
          {s.pieces.map((piece) => (
            <PrintCard key={piece.id} piece={piece} showBuyButton />
          ))}
        </div>

        {/* Series bundle */}
        <div className="border border-border p-8 mb-8">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-6">
            <div>
              <h3 className="text-headline text-primary mb-2">
                Complete {s.name} Series
              </h3>
              <p className="text-body text-secondary">
                All {s.pieces.length} pieces as high-resolution PDFs.
                Print-ready at 300 DPI.
              </p>
              <p className="text-body text-secondary mt-1">
                <span className="line-through text-muted">
                  ${s.pieces.reduce((sum, p) => sum + p.price, 0)}
                </span>{" "}
                <span className="text-primary font-medium">
                  ${s.bundlePrice}
                </span>{" "}
                — save $
                {s.pieces.reduce((sum, p) => sum + p.price, 0) - s.bundlePrice}
              </p>
            </div>
            <a
              href={s.bundleGumroadUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="px-6 py-3 border border-primary text-caption uppercase tracking-widest text-primary hover:bg-primary hover:text-bg transition-colors duration-500 text-center whitespace-nowrap"
            >
              Download Bundle
            </a>
          </div>
        </div>

        <div className="mb-20">
          <LicenseTerms compact />
        </div>

        {/* The Story Behind This Series */}
        <details className="group mb-16">
          <summary className="cursor-pointer text-headline text-primary mb-4 list-none flex items-center gap-2">
            <span className="text-caption text-muted group-open:rotate-90 transition-transform duration-300">
              &#9654;
            </span>
            The Story Behind This Series
          </summary>
          <div className="pl-5 pt-4 max-w-2xl">
            <p className="text-body text-secondary">{s.story}</p>
            <p className="text-body text-secondary mt-4">
              Mathematical primitive: {s.mathematicalPrimitive}
            </p>
          </div>
        </details>
      </div>
    </div>
  );
}
