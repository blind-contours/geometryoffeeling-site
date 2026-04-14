import PrintCard from "@/components/PrintCard";
import Link from "next/link";
import { series, allPieces } from "@/data/series";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title:
    "Art for Wellness & Therapeutic Spaces | Calming Prints for Therapy Offices — Geometry of Feeling",
  alternates: { canonical: "/collections/art-for-wellness-spaces" },
  description:
    "Calming art for therapy offices, yoga studios, meditation rooms, and wellness spaces. Hand-coded abstract prints that hold difficult feelings without dramatizing them. Museum-quality giclée on Hahnemühle German Etching 310gsm. From $45 with free shipping.",
  keywords: [
    "art for therapy office",
    "therapist office wall art",
    "art for meditation room",
    "calming art for waiting room",
    "art for yoga studio",
    "art for wellness space",
    "art for counseling room",
    "healing art prints",
  ],
  openGraph: {
    title:
      "Art for Wellness & Therapeutic Spaces | Calming Prints for Therapy Offices — Geometry of Feeling",
    description:
      "Calming art for therapy offices, yoga studios, meditation rooms, and wellness spaces. Hand-coded abstract prints. Museum-quality giclée prints from $45.",
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

const spaceGroups = [
  {
    space: "Therapy & Counseling Offices",
    seriesIds: ["peace", "grief", "belonging"],
    description:
      "Art that holds difficult feelings without dramatizing them. Equilibrium fields, diffusion curves, and domain-warped forms that give a room emotional range without pushing anyone toward a specific response.",
  },
  {
    space: "Yoga & Meditation Studios",
    seriesIds: ["peace", "surrender"],
    description:
      "Breathing rhythms, resolved harmonics, and the mathematics of letting go. Pieces that support stillness rather than competing with it.",
  },
  {
    space: "Waiting Rooms",
    seriesIds: ["trust", "belonging"],
    description:
      "Mirrored signals, handshake curves, and soft potential wells. Art that communicates safety before a word is spoken.",
  },
  {
    space: "Corporate Wellness",
    seriesIds: ["solitude", "peace", "trust"],
    description:
      "Restores rather than stimulates. Vast fields, equilibrium lines, and interlocking weaves that give a space room to breathe.",
  },
];

const faqItems = [
  {
    question: "What art is best for a therapy office?",
    answer:
      "Art that holds emotional range without directing it. Abstract work with resolved tension, soft forms, and warm neutrals tends to work well — it gives clients space to bring their own feelings rather than reacting to the art. The Peace, Grief, and Belonging series are designed with exactly this quality.",
  },
  {
    question: "Does wall art affect stress levels?",
    answer:
      "Research suggests that viewing certain types of art — particularly nature-based imagery, abstract work with soft curves, and compositions with visual balance — can lower cortisol and reduce perceived stress. Art with resolved mathematical harmony, like the equilibrium fields in the Peace series, creates an atmosphere of calm that people feel even when they are not consciously looking at it.",
  },
  {
    question: "What size art works best for an office?",
    answer:
      "For a therapy or counseling office, the 24×16\" size works well across from seating — large enough to be present without dominating. For waiting rooms and yoga studios, the 36×24\" size creates an anchor point. The 12×8\" size suits smaller spaces, grouped arrangements, or desks.",
  },
];

export default function WellnessSpacesPage() {
  const allCuratedPieces = spaceGroups.flatMap((group) =>
    group.seriesIds.flatMap(
      (id) => series.find((s) => s.id === id)?.pieces ?? []
    )
  );

  // Deduplicate pieces that appear in multiple groups
  const uniquePieces = Array.from(
    new Map(allCuratedPieces.map((p) => [p.id, p])).values()
  );

  const collectionJsonLd = {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    name: "Art for Wellness & Therapeutic Spaces",
    description:
      "Calming abstract art prints for therapy offices, yoga studios, meditation rooms, and wellness spaces. Hand-coded in Python from mathematical equations.",
    mainEntity: {
      "@type": "ItemList",
      numberOfItems: uniquePieces.length,
      itemListElement: uniquePieces.slice(0, 30).map((p, i) => ({
        "@type": "ListItem",
        position: i + 1,
        url: `${baseUrl}/piece/${p.id}`,
        name: p.title,
      })),
    },
  };

  const faqJsonLd = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: faqItems.map((item) => ({
      "@type": "Question",
      name: item.question,
      acceptedAnswer: {
        "@type": "Answer",
        text: item.answer,
      },
    })),
  };

  return (
    <div className="pt-28 pb-16">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(collectionJsonLd) }}
      />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(faqJsonLd) }}
      />
      <div className="max-w-content mx-auto px-6">
        <h1 className="text-2xl md:text-3xl font-mono font-light text-primary mb-4">
          Art for Wellness & Therapeutic Spaces
        </h1>
        <p className="text-body text-secondary max-w-2xl mb-4">
          The art in a therapeutic space matters more than most people think. It
          sets a tone before anything is said. These pieces are built from
          mathematics that resolves — equilibrium fields, breathing rhythms,
          diffusion curves, soft potential wells — and they bring that resolution
          into the room.
        </p>
        <p className="text-body text-secondary max-w-2xl mb-4">
          Every piece is hand-coded in Python. No image generators, no prompts.
          The calm you see comes from the structure of the equations underneath.
        </p>
        <p className="text-caption text-muted mb-12">
          Museum-quality giclée on Hahnemühle German Etching 310gsm. Three sizes
          from $45. Free shipping on every order.
        </p>

        {spaceGroups.map((group) => {
          const groupSeries = group.seriesIds
            .map((id) => series.find((s) => s.id === id))
            .filter(Boolean);

          return (
            <div key={group.space} className="mb-20">
              <h2 className="text-xl font-mono font-light text-primary mb-2">
                {group.space}
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

        {/* FAQ */}
        <div className="border-t border-border pt-12 mb-12 max-w-2xl">
          <h2 className="text-xl font-mono font-light text-primary mb-6">
            Common Questions
          </h2>
          <div className="space-y-6">
            {faqItems.map((item) => (
              <div key={item.question}>
                <p className="text-body text-primary font-medium mb-1">
                  {item.question}
                </p>
                <p className="text-body text-secondary">{item.answer}</p>
              </div>
            ))}
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
