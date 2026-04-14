import Image from "next/image";
import Link from "next/link";
import { series } from "@/data/series";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title:
    "Emotional Art by Theme | Awe, Grief, Peace, Connection, Belonging & More — Geometry of Feeling",
  description:
    "Explore emotional minimalist art by theme. Browse awe, grief, peace, connection, belonging, desire, growth, and 13 more hand-coded abstract print series — each built from the mathematics of a feeling.",
  keywords: [
    "emotional art by theme",
    "abstract art about grief",
    "art about connection",
    "art about awe",
    "art about peace",
    "art about belonging",
    "emotional minimalist art",
    "mathematical art by emotion",
  ],
  openGraph: {
    title:
      "Emotional Art by Theme — Geometry of Feeling",
    description:
      "Explore emotional minimalist art by theme. 20 series, each built from the mathematics of a feeling.",
    images: [
      {
        url: "/prints/connection/connection_magnetic.jpg",
        width: 1680,
        height: 1155,
      },
    ],
  },
};

function getLeadImage(s: (typeof series)[number]): string {
  if (s.homePieceIds && s.homePieceIds.length > 0) {
    const piece = s.pieces.find((p) => p.id === s.homePieceIds![0]);
    if (piece) return piece.imageUrl;
  }
  return s.pieces[0]?.imageUrl ?? "";
}

function getLeadTitle(s: (typeof series)[number]): string {
  if (s.homePieceIds && s.homePieceIds.length > 0) {
    const piece = s.pieces.find((p) => p.id === s.homePieceIds![0]);
    if (piece) return piece.title;
  }
  return s.pieces[0]?.title ?? s.name;
}

const moodGroups = [
  {
    label: "Calmer",
    ids: ["peace", "belonging", "surrender", "trust"],
  },
  {
    label: "More expansive",
    ids: ["awe", "wonder", "solitude"],
  },
  {
    label: "Emotionally serious",
    ids: ["grief", "comprehending", "longing"],
  },
  {
    label: "Alive and growing",
    ids: ["growth", "cycles", "resilience"],
  },
  {
    label: "Relational",
    ids: ["connection", "desire", "trust", "pride"],
  },
  {
    label: "Holds tension",
    ids: ["tension", "fractured"],
  },
  {
    label: "Quiet proportion",
    ids: ["humility", "nostalgia", "surrender"],
  },
];

export default function EmotionsPage() {
  return (
    <div className="pt-28 pb-16">
      <div className="max-w-content mx-auto px-6">
        <h1 className="text-2xl md:text-3xl font-mono font-light text-primary mb-4">
          Emotional Art by Theme
        </h1>
        <p className="text-body text-secondary max-w-2xl mb-4">
          Geometry of Feeling is organized by emotion. Each series begins with a
          feeling — awe, grief, peace, connection, belonging, desire, growth —
          then translates it into a mathematical system that behaves the same
          way. Browse the work by the emotional atmosphere you want to live with.
        </p>
        <p className="text-caption text-muted mb-12">
          {series.length} series. {series.reduce((n, s) => n + s.pieces.length, 0)} pieces.
          Every one hand-coded in Python.
        </p>

        {/* All series */}
        <div className="space-y-16 mb-20">
          {series.map((s) => {
            const leadImage = getLeadImage(s);
            const leadTitle = getLeadTitle(s);

            return (
              <div
                key={s.id}
                className="md:grid md:grid-cols-[280px_1fr] md:gap-8 items-start"
              >
                {leadImage && (
                  <Link
                    href={`/series/${s.id}`}
                    className="block mb-4 md:mb-0 hover:opacity-90 transition-opacity duration-500"
                  >
                    <Image
                      src={leadImage}
                      alt={`${leadTitle} — ${s.name} series`}
                      width={560}
                      height={385}
                      className="w-full object-cover border border-border"
                    />
                  </Link>
                )}
                <div>
                  <h2 className="text-headline uppercase tracking-widest text-primary mb-2">
                    <Link
                      href={`/series/${s.id}`}
                      className="hover:opacity-70 transition-opacity duration-500"
                    >
                      {s.name}
                    </Link>
                  </h2>
                  <p className="text-body text-secondary mb-2">
                    {s.emotion.charAt(0).toUpperCase() + s.emotion.slice(1)}.
                  </p>
                  <p className="text-body text-secondary mb-3 italic">
                    {s.homeDescriptor || s.tagline}
                  </p>
                  <p className="text-caption text-muted">
                    {s.pieces.length} piece{s.pieces.length !== 1 ? "s" : ""} —{" "}
                    <Link
                      href={`/series/${s.id}`}
                      className="text-primary underline underline-offset-4 hover:opacity-70 transition-opacity duration-500"
                    >
                      Explore {s.name.toLowerCase()}
                    </Link>
                  </p>
                </div>
              </div>
            );
          })}
        </div>

        <div className="border-t border-border mb-16" />

        {/* Choose by mood */}
        <section className="mb-16 max-w-2xl">
          <h2 className="text-xl font-mono font-light text-primary mb-6">
            Choose by Mood
          </h2>
          <p className="text-body text-secondary mb-8">
            Not sure where to start? Here are groupings by the atmosphere a
            series creates in a room.
          </p>
          <div className="space-y-6">
            {moodGroups.map((group) => (
              <div key={group.label}>
                <p className="text-body text-primary font-medium mb-1">
                  If you want your space to feel {group.label.toLowerCase()}
                </p>
                <p className="text-body text-secondary">
                  {group.ids.map((id, i) => {
                    const s = series.find((s) => s.id === id);
                    if (!s) return null;
                    return (
                      <span key={id}>
                        {i > 0 && ", "}
                        <Link
                          href={`/series/${id}`}
                          className="text-primary underline underline-offset-4 hover:opacity-70 transition-opacity duration-500"
                        >
                          {s.name.charAt(0) + s.name.slice(1).toLowerCase()}
                        </Link>
                      </span>
                    );
                  })}
                </p>
              </div>
            ))}
          </div>
        </section>

        {/* Closing */}
        <section className="mb-16 max-w-2xl">
          <p className="text-body text-secondary">
            People do not live with art as a category. They live with it as an
            atmosphere. This guide is here to help you find the emotional climate
            that feels right in your home.
          </p>
        </section>

        {/* CTA */}
        <div className="flex flex-wrap gap-4">
          <Link
            href="/series"
            className="px-6 py-3 border border-primary text-caption uppercase tracking-widest text-primary hover:bg-primary hover:text-bg transition-colors duration-500"
          >
            Browse All Series
          </Link>
          <Link
            href="/collections/calm-art-for-interiors"
            className="px-6 py-3 border border-border text-caption uppercase tracking-widest text-secondary hover:text-primary hover:border-primary transition-colors duration-500"
          >
            Start with Calm Interiors
          </Link>
          <Link
            href="/shop"
            className="px-6 py-3 border border-border text-caption uppercase tracking-widest text-secondary hover:text-primary hover:border-primary transition-colors duration-500"
          >
            Shop
          </Link>
        </div>
      </div>
    </div>
  );
}
