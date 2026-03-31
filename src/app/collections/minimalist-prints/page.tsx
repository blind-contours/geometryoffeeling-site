import PrintCard from "@/components/PrintCard";
import Link from "next/link";
import { series, allPieces } from "@/data/series";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title:
    "Minimalist Fine Art Prints | Calm Abstract Wall Art for Home — Geometry of Feeling",
  description:
    "Minimalist fine art prints with emotional depth — calm, meaningful wall art for your living room, bedroom, or office. Each piece expresses a feeling through mathematical equations. Museum-quality giclée on Hahnemühle German Etching 310gsm. From $45 with free shipping.",
  keywords: [
    "minimalist fine art prints",
    "minimalist art with emotion",
    "calm art for living room",
    "abstract wall art",
    "meaningful wall art",
    "minimalist wall art for bedroom",
    "calming emotional art",
    "contemporary fine art prints",
  ],
  openGraph: {
    title:
      "Minimalist Fine Art Prints | Calm Abstract Wall Art for Home — Geometry of Feeling",
    description:
      "Minimalist fine art prints with emotional depth — calm, meaningful wall art for your living room, bedroom, or office. Each piece expresses a feeling through mathematical equations. Museum-quality giclée on Hahnemühle German Etching 310gsm. From $45 with free shipping.",
    images: [
      {
        url: "/prints/peace/peace_harmonic_decay.jpg",
        width: 1680,
        height: 1155,
      },
    ],
  },
};

const baseUrl =
  process.env.NEXT_PUBLIC_URL || "https://geometryoffeeling.com";

// Series with calm, minimal aesthetics
const curatedSeriesIds = [
  "peace",
  "solitude",
  "grief",
  "surrender",
  "nostalgia",
  "longing",
  "trust",
];

export default function MinimalistPrintsPage() {
  const curatedSeries = curatedSeriesIds
    .map((id) => series.find((s) => s.id === id))
    .filter(Boolean);
  const curatedPieces = curatedSeries.flatMap((s) => s!.pieces);

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    name: "Minimalist Fine Art Prints",
    description:
      "Minimalist fine art prints for home and office. Clean abstract compositions derived from mathematical equations. Museum-quality giclée prints.",
    mainEntity: {
      "@type": "ItemList",
      numberOfItems: curatedPieces.length,
      itemListElement: curatedPieces.slice(0, 20).map((p, i) => ({
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
          Minimalist Fine Art Prints
        </h1>
        <p className="text-body text-secondary max-w-2xl mb-4">
          Clean, quiet compositions for spaces that need breathing room. Every
          print in this collection is built from a mathematical equation — curves
          of decay, fields of stillness, harmonic progressions that resolve into
          silence. The result is abstract wall art that feels considered without
          being busy.
        </p>
        <p className="text-body text-secondary max-w-2xl mb-4">
          These are not decorative patterns. Each piece begins with a human
          emotion — peace, solitude, grief, surrender — and renders it through
          the function that shares its shape. The minimalism comes from the
          mathematics: one equation, one feeling, nothing extra.
        </p>
        <p className="text-caption text-muted mb-12">
          Museum-quality giclée on Hahnemühle German Etching 310gsm. Three
          sizes from $45. Free shipping on every order.
        </p>

        {curatedSeries.map((s) => (
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
            Looking for something specific?
          </h2>
          <p className="text-body text-secondary mb-4">
            Browse all {allPieces.length} pieces in the{" "}
            <Link
              href="/shop"
              className="text-primary underline underline-offset-4 hover:opacity-70 transition-opacity duration-500"
            >
              full catalog
            </Link>
            , or{" "}
            <Link
              href="/custom"
              className="text-primary underline underline-offset-4 hover:opacity-70 transition-opacity duration-500"
            >
              commission a custom piece
            </Link>{" "}
            in your preferred colors and dimensions.
          </p>
        </div>
      </div>
    </div>
  );
}
