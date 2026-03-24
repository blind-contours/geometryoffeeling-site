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

        {/* Collection callout */}
        <div className="border border-border p-6 md:p-8 mb-16">
          <h2 className="text-headline text-primary mb-2">
            The Complete {s.name} Series — {s.pieces.length} Pieces
          </h2>
          <p className="text-body text-secondary mb-1">
            From $45 each — museum-grade Hahnemuhle German Etching prints.
          </p>
          <p className="text-caption text-muted">
            Free shipping on every order. Collect the full series and see the emotion unfold.
          </p>
        </div>

        {/* Pieces grid — 2-up on desktop */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12 mb-20">
          {s.pieces.map((piece) => (
            <PrintCard key={piece.id} piece={piece} showBuyButton />
          ))}
        </div>

        {/* Print info */}
        <div className="border border-border p-8 mb-8">
          <h3 className="text-headline text-primary mb-2">
            Fine Art Prints
          </h3>
          <p className="text-body text-secondary mb-1">
            Hahnemuhle German Etching 310gsm — museum-grade matte.
          </p>
          <p className="text-body text-secondary">
            8&times;10&quot; — $45 &nbsp;|&nbsp; 16&times;20&quot; — $95 &nbsp;|&nbsp; 24&times;36&quot; — $175
          </p>
          <p className="text-caption text-muted mt-2">
            Free shipping — 5-10 business days
          </p>
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
