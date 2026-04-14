import PrintCard from "@/components/PrintCard";
import Link from "next/link";
import { series, allPieces } from "@/data/series";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title:
    "Calm Art for Interiors | Minimalist Prints for Quiet Modern Spaces — Geometry of Feeling",
  alternates: { canonical: "/collections/calm-art-for-interiors" },
  description:
    "Shop calm minimalist art for interiors from Geometry of Feeling. Hand-coded abstract prints in blue, sage, sand, and warm neutral palettes for quiet modern spaces. Museum-quality giclée on Hahnemühle German Etching 310gsm. From $45 with free shipping.",
  keywords: [
    "calm art for interiors",
    "minimalist art for living room",
    "peaceful wall art",
    "calm wall art for bedroom",
    "quiet abstract art prints",
    "neutral art for modern home",
    "serene minimalist prints",
    "calming office art",
    "japandi wall art",
    "wabi-sabi art prints",
    "warm minimalism art",
    "earth tone abstract art",
    "neutral abstract wall art",
    "organic abstract art",
    "art for therapy office",
    "art for meditation room",
    "art for wellness space",
  ],
  openGraph: {
    title:
      "Calm Art for Interiors | Minimalist Prints for Quiet Modern Spaces — Geometry of Feeling",
    description:
      "Shop calm minimalist art for interiors. Hand-coded abstract prints in blue, sage, sand, and warm neutral palettes. Museum-quality giclée prints from $45.",
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

const moodGroups = [
  {
    mood: "For stillness",
    seriesIds: ["peace"],
    description:
      "Equilibrium fields, horizon lines, and breathing rhythms. Pieces that resolve into silence.",
  },
  {
    mood: "For warmth and shelter",
    seriesIds: ["belonging"],
    description:
      "Domain-warped rings, soft potential wells, and translucent layered forms. Pieces that hold rather than display.",
  },
  {
    mood: "For release",
    seriesIds: ["surrender"],
    description:
      "Terminal velocity, freefall, and the moment resistance gives way. Pieces about ceasing to fight.",
  },
  {
    mood: "For quiet rhythm",
    seriesIds: ["trust"],
    description:
      "Handshakes, mirrored signals, and interlocking weaves. Pieces about choosing the same rhythm.",
  },
  {
    mood: "For memory",
    seriesIds: ["nostalgia"],
    description:
      "Fading edges, warm blurs, and traces of what was. Pieces where the warmth stays and the details soften.",
  },
  {
    mood: "For space",
    seriesIds: ["solitude", "longing", "humility"],
    description:
      "Vast fields, isolated signals, and the mathematics of being small. Pieces that give a room breathing room.",
  },
];

export default function CalmArtPage() {
  const allCuratedPieces = moodGroups.flatMap((group) =>
    group.seriesIds.flatMap(
      (id) => series.find((s) => s.id === id)?.pieces ?? []
    )
  );

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    name: "Calm Art for Interiors",
    description:
      "Calm minimalist art prints for interiors — quiet geometric works in blue, sage, sand, and warm neutral palettes, hand-coded in Python from mathematical equations.",
    mainEntity: {
      "@type": "ItemList",
      numberOfItems: allCuratedPieces.length,
      itemListElement: allCuratedPieces.slice(0, 30).map((p, i) => ({
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
          Calm Art for Interiors
        </h1>
        <p className="text-body text-secondary max-w-2xl mb-4">
          Calm does not mean empty. In these pieces, calm comes from proportion,
          spacing, repetition, softened boundaries, and restrained color. The
          equations are different — equilibrium fields, breathing rhythms,
          domain-warped rings, fading harmonics — but the feeling is the same:
          room to breathe.
        </p>
        <p className="text-body text-secondary max-w-2xl mb-4">
          Every piece in this collection is hand-coded in Python. No image
          generators, no prompts. The quietness you see is the quietness of the
          mathematics underneath.
        </p>
        <p className="text-caption text-muted mb-12">
          Museum-quality giclée on Hahnemühle German Etching 310gsm. Three sizes
          from $45. Free shipping on every order.
        </p>

        {moodGroups.map((group) => {
          const groupSeries = group.seriesIds
            .map((id) => series.find((s) => s.id === id))
            .filter(Boolean);

          return (
            <div key={group.mood} className="mb-20">
              <h2 className="text-xl font-mono font-light text-primary mb-2">
                {group.mood}
              </h2>
              <p className="text-body text-secondary mb-8 max-w-2xl">
                {group.description}
              </p>

              {groupSeries.map((s) => (
                <div key={s!.id} className="mb-12">
                  <h3 className="text-headline uppercase tracking-widest text-primary mb-2">
                    <Link
                      href={`/series/${s!.id}`}
                      className="hover:opacity-70 transition-opacity duration-500"
                    >
                      {s!.name}
                    </Link>
                  </h3>
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
            </div>
          );
        })}

        {/* Room guidance */}
        <div className="border-t border-border pt-12 mb-12 max-w-2xl">
          <h2 className="text-headline uppercase tracking-widest text-primary mb-6">
            Which Pieces Suit Which Rooms
          </h2>
          <div className="space-y-4">
            <p className="text-body text-secondary">
              <span className="text-primary">Living room —</span> Peace and
              Belonging work well at larger sizes. Horizon, Guardian, and Nest are
              among the most popular for the main wall.
            </p>
            <p className="text-body text-secondary">
              <span className="text-primary">Bedroom —</span> Surrender, Trust,
              and the quieter Peace pieces (Breath, Cloud) pair well with spaces
              meant for rest.
            </p>
            <p className="text-body text-secondary">
              <span className="text-primary">Home office —</span> Solitude
              pieces (Signal, Drift, Basin) bring focused energy without
              distraction. Longing adds contemplative depth.
            </p>
            <p className="text-body text-secondary">
              <span className="text-primary">Entryway —</span> Humility
              (Grounded) and Nostalgia pieces set a tone immediately — proportioned,
              warm, considered.
            </p>
          </div>
        </div>

        {/* CTA */}
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
            , explore work{" "}
            <Link
              href="/emotions"
              className="text-primary underline underline-offset-4 hover:opacity-70 transition-opacity duration-500"
            >
              by emotion
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
