import PrintCard from "@/components/PrintCard";
import Link from "next/link";
import { series, allPieces } from "@/data/series";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title:
    "Mathematical Art Prints | Equation Art & Generative Art — Geometry of Feeling",
  alternates: { canonical: "/collections/mathematical-art" },
  description:
    "Art prints derived from real mathematical equations — Lorenz attractors, Fourier series, bifurcation diagrams, coupled oscillators, and more. Every piece is code-generated from a specific function. Museum-quality giclée prints from $45.",
  keywords: [
    "mathematical art prints",
    "equation art",
    "generative art prints",
    "algorithm art prints",
    "code-generated art",
    "fractal art prints",
    "data visualization art",
    "Python generative art",
    "parametric art prints",
    "sacred geometry art",
  ],
  openGraph: {
    title:
      "Mathematical Art Prints | Equation Art & Generative Art — Geometry of Feeling",
    description:
      "Art prints derived from real mathematical equations — Lorenz attractors, Fourier series, bifurcation diagrams, coupled oscillators, and more. Every piece is code-generated from a specific function. Museum-quality giclée prints from $45.",
    images: [
      {
        url: "/prints/awe/awe_singularity.jpg",
        width: 1680,
        height: 1155,
      },
    ],
  },
};

const baseUrl =
  process.env.NEXT_PUBLIC_URL || "https://geometryoffeeling.com";

// Series that showcase the math angle most strongly
const featuredSeriesIds = [
  "awe",
  "connection",
  "cycles",
  "growth",
  "tension",
];

export default function MathematicalArtPage() {
  const featuredSeries = featuredSeriesIds
    .map((id) => series.find((s) => s.id === id))
    .filter(Boolean);

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    name: "Mathematical Art Prints — Equation Art & Generative Art",
    description:
      "Fine art prints derived from mathematical equations. Lorenz attractors, Fourier series, bifurcation diagrams, coupled oscillators. Code-generated generative art printed on museum-quality paper.",
    mainEntity: {
      "@type": "ItemList",
      numberOfItems: allPieces.length,
      itemListElement: allPieces.slice(0, 20).map((p, i) => ({
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
          Mathematical Art Prints
        </h1>
        <p className="text-body text-secondary max-w-2xl mb-4">
          Every piece in this collection is generated from a real mathematical
          equation. Lorenz attractors, Fourier series, bifurcation diagrams,
          coupled oscillators, Voronoi tessellations, catastrophe folds — each
          rendered in Python and evaluated as art. No AI. No randomness for its
          own sake. Just equations that happen to look like feelings.
        </p>
        <p className="text-body text-secondary max-w-2xl mb-4">
          This is generative art in the truest sense: code that takes a function
          and a set of parameters and produces a visual field. The artist&#39;s
          role is choosing which equation maps to which emotion, tuning the
          parameters until the output resonates, and curating ruthlessly — over
          1,200 renders were produced; fewer than 170 survived.
        </p>
        <p className="text-body text-secondary max-w-2xl mb-4">
          The equations are printed alongside each piece. If you know the math,
          you can read the feeling. If you don&#39;t, the image speaks for
          itself.
        </p>
        <p className="text-caption text-muted mb-12">
          Museum-quality giclée on Hahnemühle German Etching 310gsm. Three
          sizes: 12&times;8&quot; ($45), 24&times;16&quot; ($95),
          36&times;24&quot; ($175). Free shipping.
        </p>

        {featuredSeries.map((s) => (
          <div key={s!.id} className="mb-16">
            <h2 className="text-headline uppercase tracking-widest text-primary mb-2">
              <Link
                href={`/series/${s!.id}`}
                className="hover:opacity-70 transition-opacity duration-500"
              >
                {s!.name}
              </Link>
            </h2>
            <p className="text-caption text-muted mb-1">
              {s!.mathematicalPrimitive}
            </p>
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
            All {allPieces.length} Pieces
          </h2>
          <p className="text-body text-secondary mb-4">
            Browse the{" "}
            <Link
              href="/shop"
              className="text-primary underline underline-offset-4 hover:opacity-70 transition-opacity duration-500"
            >
              complete catalog
            </Link>{" "}
            across all series, or explore{" "}
            <Link
              href="/series"
              className="text-primary underline underline-offset-4 hover:opacity-70 transition-opacity duration-500"
            >
              series by emotion
            </Link>
            .
          </p>
        </div>
      </div>
    </div>
  );
}
