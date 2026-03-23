import Link from "next/link";
import Hero from "@/components/Hero";
import HomeSeriesGrid from "@/components/HomeSeriesGrid";
import { series, featuredSeriesIds } from "@/data/series";

const featuredSeries = featuredSeriesIds
  .map((id) => series.find((s) => s.id === id)!)
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
            feeling? We researched that emotion across art history and science,
            then built the image from first principles. The equation isn&apos;t
            decoration. It&apos;s the reason the piece looks the way it does.
          </p>
          <p className="text-body text-secondary">
            In a world of AI-generated imagery, we went the other direction.
            This is minimalist fine art built from mathematical first principles
            — not prompted, not generated, not automated. Every curve was chosen.
            Every parameter was earned.
          </p>
        </div>

        <div className="border border-border px-6 py-4 inline-block">
          <p className="text-caption uppercase tracking-widest text-secondary">
            Built in Python. Evaluated as art. Not AI-generated.
          </p>
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
    </>
  );
}
