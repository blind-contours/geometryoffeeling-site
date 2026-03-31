import Link from "next/link";
import SeriesCard from "@/components/SeriesCard";
import { series } from "@/data/series";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title:
    "Emotional Art Prints | Minimalist Art About Grief, Connection, Awe & More — Geometry of Feeling",
  description:
    "Emotional art that means something. 26 series of minimalist fine art prints exploring grief, connection, awe, desire, solitude, overwhelm, joy, and surrender through mathematics. Art that expresses feelings through the equations that share their shape. Museum-quality prints from $45.",
  keywords: [
    "emotional art prints",
    "art about grief",
    "art about connection",
    "minimalist art with emotion",
    "art that expresses feelings",
    "meaningful wall art",
    "calming emotional art",
    "abstract art about emotion",
    "art about solitude",
    "art about awe",
  ],
  openGraph: {
    title:
      "Emotional Art Prints | Minimalist Art About Grief, Connection, Awe & More — Geometry of Feeling",
    description:
      "Emotional art that means something. 26 series of minimalist fine art prints exploring grief, connection, awe, desire, solitude, overwhelm, joy, and surrender through mathematics. Art that expresses feelings through the equations that share their shape. Museum-quality prints from $45.",
    images: [
      {
        url: "/prints/grief/grief_void.jpg",
        width: 1680,
        height: 1155,
      },
    ],
  },
};

const baseUrl =
  process.env.NEXT_PUBLIC_URL || "https://geometryoffeeling.com";

// Group by emotional valence for the page structure
const heavyEmotions = [
  "grief",
  "longing",
  "nostalgia",
  "solitude",
  "shame",
];
const tenseEmotions = [
  "tension",
  "overwhelm",
  "confusion",
  "fractured",
  "rage",
];
const warmEmotions = [
  "connection",
  "desire",
  "trust",
  "pride",
  "anticipation",
];
const lightEmotions = [
  "wonder",
  "awe",
  "peace",
  "growth",
  "resilience",
  "surrender",
  "cycles",
];

function getSeriesGroup(ids: string[]) {
  return ids.map((id) => series.find((s) => s.id === id)).filter(Boolean);
}

export default function ArtAboutEmotionPage() {
  const heavy = getSeriesGroup(heavyEmotions);
  const tense = getSeriesGroup(tenseEmotions);
  const warm = getSeriesGroup(warmEmotions);
  const light = getSeriesGroup(lightEmotions);

  const allEmotionNames = series.map((s) => s.emotion.split(",")[0].trim());
  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    name: "Art About Emotion — Abstract Art Exploring Human Feeling Through Mathematics",
    description: `Abstract fine art prints exploring ${allEmotionNames.slice(0, 10).join(", ")}, and more. Each emotion rendered through the mathematical equation that shares its shape.`,
    mainEntity: {
      "@type": "ItemList",
      numberOfItems: series.length,
      itemListElement: series.map((s, i) => ({
        "@type": "ListItem",
        position: i + 1,
        url: `${baseUrl}/series/${s.id}`,
        name: `${s.name} — ${s.emotion}`,
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
          Art About Emotion
        </h1>
        <p className="text-body text-secondary max-w-2xl mb-4">
          Every piece in this collection begins with a specific human emotion and
          asks: what mathematical function has the same shape as this feeling?
          Grief becomes exponential decay. Connection becomes coupled
          oscillators. Awe becomes singularities. The equations are real. The
          feelings are real. The correspondence between them is the art.
        </p>
        <p className="text-body text-secondary max-w-2xl mb-4">
          26 series. 26 emotions. Each one uses a different class of
          mathematical functions to render a different quality of feeling. Browse
          by the emotion you want to see on your wall.
        </p>
        <p className="text-caption text-muted mb-16">
          Museum-quality giclée on Hahnemühle German Etching 310gsm. From $45
          with free shipping.
        </p>

        <section className="mb-16">
          <h2 className="text-lg font-mono font-light text-primary mb-2">
            Loss & Solitude
          </h2>
          <p className="text-body text-muted mb-8">
            Decay curves, step functions, catenary sag, spectral erosion. The
            mathematics of things disappearing.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
            {heavy.map((s) => (
              <SeriesCard key={s!.id} series={s!} />
            ))}
          </div>
        </section>

        <section className="mb-16">
          <h2 className="text-lg font-mono font-light text-primary mb-2">
            Tension & Rupture
          </h2>
          <p className="text-body text-muted mb-8">
            Interference, torsion, bifurcation, turbulence. Systems held between
            competing forces.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
            {tense.map((s) => (
              <SeriesCard key={s!.id} series={s!} />
            ))}
          </div>
        </section>

        <section className="mb-16">
          <h2 className="text-lg font-mono font-light text-primary mb-2">
            Connection & Desire
          </h2>
          <p className="text-body text-muted mb-8">
            Coupled oscillators, phase synchronization, topological knots. Two
            systems that choose proximity.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
            {warm.map((s) => (
              <SeriesCard key={s!.id} series={s!} />
            ))}
          </div>
        </section>

        <section className="mb-16">
          <h2 className="text-lg font-mono font-light text-primary mb-2">
            Joy, Awe & Growth
          </h2>
          <p className="text-body text-muted mb-8">
            Fibonacci spirals, harmonic convergence, singularities, emergent
            patterns. The mathematics of expansion.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
            {light.map((s) => (
              <SeriesCard key={s!.id} series={s!} />
            ))}
          </div>
        </section>

        <div className="border border-border p-8">
          <h2 className="text-headline text-primary mb-2">
            Not sure which emotion?
          </h2>
          <p className="text-body text-secondary mb-4">
            Browse all pieces in the{" "}
            <Link
              href="/shop"
              className="text-primary underline underline-offset-4 hover:opacity-70 transition-opacity duration-500"
            >
              shop
            </Link>
            , or see the{" "}
            <Link
              href="/collections/minimalist-prints"
              className="text-primary underline underline-offset-4 hover:opacity-70 transition-opacity duration-500"
            >
              quietest, most minimal pieces
            </Link>{" "}
            if you want calm wall art.
          </p>
        </div>
      </div>
    </div>
  );
}
