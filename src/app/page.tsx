import Link from "next/link";
import Hero from "@/components/Hero";
import HomeSeriesGrid from "@/components/HomeSeriesGrid";
import PrintCard from "@/components/PrintCard";
import EmailCapture from "@/components/EmailCapture";
import { series, featuredSeriesIds, featuredPieceIds, getPieceBySlug } from "@/data/series";
import type { Metadata } from "next";

export const metadata: Metadata = {
  openGraph: {
    title:
      "Geometry of Feeling — Minimalist Fine Art Prints | Mathematical Art for Home & Office",
    description:
      "Minimalist fine art prints where every piece begins with a human emotion — grief, awe, connection, desire — and renders it through the mathematical equation that shares its shape. Museum-quality giclée prints on Hahnemühle German Etching 310gsm. From $45 with free shipping.",
    images: [
      { url: "/prints/awe/awe_singularity.jpg", width: 1680, height: 1155 },
    ],
  },
  twitter: {
    card: "summary_large_image",
    images: ["/prints/awe/awe_singularity.jpg"],
  },
};

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
      <section className="max-w-content mx-auto px-6 py-24 md:text-center">
        <h2 className="text-xl md:text-2xl font-mono font-light leading-relaxed text-primary max-w-3xl md:mx-auto mb-12">
          I find the equation hiding inside real things — and I draw it.
        </h2>

        <div className="max-w-2xl md:mx-auto space-y-6 mb-12">
          <p className="text-body md:text-[17px] md:leading-relaxed text-secondary md:text-primary/80">
            I spend weeks researching how things actually work. How a tree
            bifurcates as it grows. How stress propagates through cracking
            glass. How two coupled pendulums reshape each other&apos;s motion.
            How heat diffuses until you can&apos;t tell it was ever there.
          </p>
          <p className="text-body md:text-[17px] md:leading-relaxed text-secondary md:text-primary/80">
            I find the governing equation, write the code in Python, and render
            the image from first principles — then strip away everything until
            only the essential geometry remains. Each series connects a human
            emotion to the mathematics that shares its shape. Grief follows
            exponential decay. Connection mirrors coupled oscillators. The
            equation isn&apos;t decoration. It&apos;s the reason the piece exists.
          </p>
          <p className="text-body md:text-[17px] md:leading-relaxed text-secondary md:text-primary/80">
            No AI. No prompts. No generation. Every curve was chosen.
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
      <section className="max-w-gallery mx-auto px-6 lg:px-10 pb-32">
        <h2 className="text-headline-lg uppercase tracking-widest text-primary mb-8">
          Featured Pieces
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-gallery-gap">
          {featuredPieces.map((piece) => (
            <PrintCard key={piece.id} piece={piece} showBuyButton />
          ))}
        </div>
      </section>

      <hr className="border-border max-w-gallery mx-auto" />

      {/* Series collection grid */}
      <section className="max-w-gallery mx-auto px-6 lg:px-10 py-24">
        {featuredSeries.map((s, i) => (
          <HomeSeriesGrid key={s.id} series={s} index={i} />
        ))}

        <div className="text-center mt-8">
          <Link
            href="/series"
            className="inline-block text-caption md:text-[13px] uppercase tracking-widest text-primary border-b border-primary/30 pb-1 hover:border-primary transition-colors duration-500"
          >
            Explore all {series.length} series &rarr;
          </Link>
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

      {/* Email capture */}
      <EmailCapture />
    </>
  );
}
