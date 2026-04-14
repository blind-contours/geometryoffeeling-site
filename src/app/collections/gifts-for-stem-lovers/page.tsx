import PrintCard from "@/components/PrintCard";
import Link from "next/link";
import { series } from "@/data/series";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title:
    "Gifts for Thinkers & Life Moments | Unique Art Prints — Geometry of Feeling",
  alternates: { canonical: "/collections/gifts-for-stem-lovers" },
  description:
    "Meaningful art gifts for math lovers, engineers, therapists, and life's big moments — PhD graduations, new homes, sympathy, and milestones. Fine art prints derived from real equations. Beautiful enough for anyone, meaningful for those who read the math. From $45.",
  keywords: [
    "gifts for math lovers",
    "gift for engineer",
    "gift for data scientist",
    "gift for physicist",
    "gift for PhD graduation",
    "gift for therapist",
    "gift for philosophy major",
    "gift for architect",
    "unique housewarming gift art",
    "sympathy gift art",
    "STEM art prints",
  ],
  openGraph: {
    title:
      "Gifts for Thinkers & Life Moments | Unique Art Prints — Geometry of Feeling",
    description:
      "Meaningful art gifts for math lovers, engineers, therapists, and life's big moments. Fine art prints derived from real equations. From $45.",
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
    name: "Gifts for Thinkers & Life Moments — Unique Art Prints",
    description:
      "Meaningful art gifts for math lovers, engineers, therapists, PhD graduations, sympathy, and milestones. Fine art prints derived from real mathematical equations. Museum-quality giclée prints from $45 with free shipping.",
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
          Gifts for Thinkers & Life Moments
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
          data scientists, therapists, architects, and anyone who finds elegance
          in precision. They also mark life&#39;s turning points — PhD
          graduations, new homes, moments of loss — with something that holds
          meaning. Each print ships flat in a rigid mailer, ready to frame.
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

        {/* Gifts for Life Moments */}
        <div className="border-t border-border pt-12 mb-12 max-w-2xl">
          <h2 className="text-xl font-mono font-light text-primary mb-6">
            Gifts for Life Moments
          </h2>
          <p className="text-body text-secondary mb-8">
            Some moments deserve something more than a card. These are pieces
            chosen for the feeling they hold — not just the way they look.
          </p>
          <div className="space-y-4">
            <p className="text-body text-secondary">
              <span className="text-primary">PhD graduation —</span>{" "}
              <Link href="/series/growth" className="text-primary underline underline-offset-4 hover:opacity-70 transition-opacity duration-500">Growth</Link> and{" "}
              <Link href="/series/resilience" className="text-primary underline underline-offset-4 hover:opacity-70 transition-opacity duration-500">Resilience</Link>.
              {" "}Pieces about systems that persist, branch, and expand through difficulty.
            </p>
            <p className="text-body text-secondary">
              <span className="text-primary">Sympathy —</span>{" "}
              <Link href="/series/grief" className="text-primary underline underline-offset-4 hover:opacity-70 transition-opacity duration-500">Grief</Link> and{" "}
              <Link href="/series/peace" className="text-primary underline underline-offset-4 hover:opacity-70 transition-opacity duration-500">Peace</Link>.
              {" "}Art that holds loss without dramatizing it. Diffusion, equilibrium, quiet resolution.
            </p>
            <p className="text-body text-secondary">
              <span className="text-primary">New home —</span>{" "}
              <Link href="/series/belonging" className="text-primary underline underline-offset-4 hover:opacity-70 transition-opacity duration-500">Belonging</Link> and{" "}
              <Link href="/series/peace" className="text-primary underline underline-offset-4 hover:opacity-70 transition-opacity duration-500">Peace</Link>.
              {" "}Domain-warped rings, equilibrium fields — pieces about shelter and arriving.
            </p>
            <p className="text-body text-secondary">
              <span className="text-primary">For a therapist —</span>{" "}
              <Link href="/series/peace" className="text-primary underline underline-offset-4 hover:opacity-70 transition-opacity duration-500">Peace</Link> and{" "}
              <Link href="/series/trust" className="text-primary underline underline-offset-4 hover:opacity-70 transition-opacity duration-500">Trust</Link>.
              {" "}Resolved harmonics and mirrored signals — art that communicates safety.
            </p>
          </div>
        </div>

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
