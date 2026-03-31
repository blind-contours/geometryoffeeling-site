import PrintCard from "@/components/PrintCard";
import Link from "next/link";
import { series } from "@/data/series";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title:
    "Gifts for Math Lovers & Engineers | Unique STEM Art Prints — Geometry of Feeling",
  description:
    "The perfect gift for math lovers, engineers, physicists, and data scientists. Fine art prints derived from real equations — Lorenz attractors, Fourier series, coupled oscillators. Beautiful enough for anyone, meaningful for those who read the math. From $45.",
  openGraph: {
    title:
      "Gifts for Math Lovers & Engineers | Unique STEM Art Prints — Geometry of Feeling",
    description:
      "The perfect gift for math lovers, engineers, physicists, and data scientists. Fine art prints derived from real equations — Lorenz attractors, Fourier series, coupled oscillators. Beautiful enough for anyone, meaningful for those who read the math. From $45.",
    images: [
      {
        url: "/prints/connection/connection_lissajous.jpg",
        width: 1680,
        height: 1155,
      },
    ],
  },
};

const baseUrl =
  process.env.NEXT_PUBLIC_URL || "https://geometryoffeeling.com";

// Pick approachable, gift-worthy pieces across series
const giftPickSeriesIds = [
  "connection",
  "awe",
  "wonder",
  "growth",
  "resilience",
  "peace",
  "cycles",
];

export default function GiftsForStemPage() {
  const giftSeries = giftPickSeriesIds
    .map((id) => series.find((s) => s.id === id))
    .filter(Boolean);
  const giftPieces = giftSeries.flatMap((s) => s!.pieces);

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    name: "Gifts for Math Lovers & Engineers — Unique STEM Art Prints",
    description:
      "Fine art prints derived from real mathematical equations. The perfect gift for math lovers, engineers, physicists, and data scientists. Museum-quality giclée prints from $45 with free shipping.",
    mainEntity: {
      "@type": "ItemList",
      numberOfItems: giftPieces.length,
      itemListElement: giftPieces.slice(0, 20).map((p, i) => ({
        "@type": "ListItem",
        position: i + 1,
        url: `${baseUrl}/piece/${p.id}`,
        name: p.title,
      })),
    },
  };

  return (
    <div className="pt-28 pb-16">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <div className="max-w-content mx-auto px-6">
        <h1 className="text-2xl md:text-3xl font-mono font-light text-primary mb-4">
          Gifts for Math Lovers & Engineers
        </h1>
        <p className="text-body text-secondary max-w-2xl mb-4">
          Art that rewards knowing the math — but doesn&#39;t require it. Every
          print in this collection is generated from a real equation: Lissajous
          curves, Lorenz attractors, Fourier decompositions, coupled pendulums.
          The piece is beautiful on its own. The equation printed alongside it is
          a second layer for those who read that language.
        </p>
        <p className="text-body text-secondary max-w-2xl mb-4">
          These make exceptional gifts for mathematicians, physicists, engineers,
          data scientists, and anyone who finds elegance in precision. Each print
          ships flat in a rigid mailer, ready to frame.
        </p>
        <p className="text-caption text-muted mb-4">
          Museum-quality giclée on Hahnemühle German Etching 310gsm. Three
          sizes: 12&times;8&quot; ($45), 24&times;16&quot; ($95),
          36&times;24&quot; ($175). Free shipping.
        </p>
        <p className="text-caption text-muted mb-12">
          Not sure which piece? The 12&times;8&quot; size at $45 is the perfect
          entry point — museum-grade paper, real equation, ready to frame.
        </p>

        {giftSeries.map((s) => (
          <div key={s!.id} className="mb-16">
            <h2 className="text-headline uppercase tracking-widest text-primary mb-2">
              <Link
                href={`/series/${s!.id}`}
                className="hover:opacity-70 transition-opacity duration-500"
              >
                {s!.name}
              </Link>
            </h2>
            <p className="text-body text-secondary mb-6 max-w-2xl italic">
              {s!.tagline}
            </p>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
              {s!.pieces.map((piece) => (
                <PrintCard key={piece.id} piece={piece} />
              ))}
            </div>
          </div>
        ))}

        <div className="border border-border p-8 mt-8">
          <h2 className="text-headline text-primary mb-2">
            Custom Pieces
          </h2>
          <p className="text-body text-secondary mb-4">
            Want a truly one-of-a-kind gift?{" "}
            <Link
              href="/custom"
              className="text-primary underline underline-offset-4 hover:opacity-70 transition-opacity duration-500"
            >
              Commission a custom print
            </Link>{" "}
            — choose any equation, any palette, any size.
          </p>
        </div>
      </div>
    </div>
  );
}
