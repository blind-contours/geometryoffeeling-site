import Link from "next/link";
import Hero from "@/components/Hero";
import HomeSeriesGrid from "@/components/HomeSeriesGrid";
import PrintCard from "@/components/PrintCard";
import EmailCapture from "@/components/EmailCapture";
import { series, featuredSeriesIds, featuredPieceIds, getPieceBySlug } from "@/data/series";

const featuredSeries = featuredSeriesIds
  .map((id) => series.find((s) => s.id === id)!)
  .filter(Boolean);

const featuredPieces = featuredPieceIds
  .map((id) => getPieceBySlug(id)!)
  .filter(Boolean);

export default function Home() {
  return (
    <>
      <Hero />

      {/* Positioning statement */}
      <section className="max-w-content mx-auto px-6 py-24">
        <h2 className="text-lg md:text-xl font-mono font-light leading-relaxed text-primary max-w-3xl mb-12">
          Mathematical fine art for people who think precisely and feel deeply.
        </h2>

        <div className="max-w-2xl space-y-6 mb-12">
          <p className="text-body text-secondary">
            Every piece begins with a human emotion — grief, growth, connection
            — and asks: what mathematical function has the same shape as this
            feeling? I research the emotion across art history and science,
            then build the image from first principles. The equation isn&apos;t
            decoration. It&apos;s the reason the piece looks the way it does.
          </p>
          <p className="text-body text-secondary">
            In a world of AI-generated imagery, I went the other direction.
            Minimalist fine art built from mathematical first principles
            — not prompted, not generated, not automated. Every curve was chosen.
            Every parameter was earned.
          </p>
        </div>

        <div className="border border-border px-6 py-4 inline-block">
          <p className="text-caption uppercase tracking-widest text-secondary">
            Built in Python. Evaluated as art. No AI generated images.
          </p>
        </div>
      </section>

      {/* Featured pieces */}
      <section className="max-w-content mx-auto px-6 pb-24">
        <h2 className="text-headline uppercase tracking-widest text-primary mb-8">
          Featured Pieces
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          {featuredPieces.map((piece) => (
            <PrintCard key={piece.id} piece={piece} showBuyButton />
          ))}
        </div>
      </section>

      {/* Custom prints callout */}
      <section className="max-w-content mx-auto px-6 pb-24">
        <div className="border border-border p-8 md:p-12 text-center">
          <h2 className="text-lg md:text-xl font-mono font-light text-primary mb-4">
            Want Something Unique?
          </h2>
          <p className="text-body text-secondary max-w-xl mx-auto mb-6">
            I write the code that generates every piece — meaning custom colors,
            dimensions, and entirely new compositions are possible. Tell me what
            you&apos;re envisioning.
          </p>
          <Link
            href="/custom"
            className="inline-block px-8 py-3 border border-primary text-caption uppercase tracking-widest text-primary hover:bg-primary hover:text-bg transition-colors duration-500"
          >
            Commission a Custom Piece
          </Link>
        </div>
      </section>

      {/* Series collection grid */}
      <section className="max-w-content mx-auto px-6 pb-24">
        {featuredSeries.map((s, i) => (
          <HomeSeriesGrid key={s.id} series={s} index={i} />
        ))}

        <div className="text-center mt-8">
          <Link
            href="/series"
            className="text-caption uppercase tracking-widest text-secondary hover:text-primary transition-colors duration-500"
          >
            Explore all {series.length} series &rarr;
          </Link>
        </div>
      </section>

      {/* Email capture */}
      <EmailCapture />
    </>
  );
}
