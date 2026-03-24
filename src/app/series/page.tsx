import SeriesCard from "@/components/SeriesCard";
import { series } from "@/data/series";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "All Series — Geometry of Feeling",
  description:
    "Twenty-six series exploring the intersection of mathematics and human emotion. Each series uses a different mathematical primitive to render a different feeling.",
  openGraph: {
    title: "All Series — Geometry of Feeling",
    description:
      "Twenty-six series exploring the intersection of mathematics and human emotion. Each series uses a different mathematical primitive to render a different feeling.",
    images: [{ url: "/prints/cycles/cycles_loom.jpg", width: 1680, height: 1155 }],
  },
  twitter: {
    card: "summary_large_image",
    images: ["/prints/cycles/cycles_loom.jpg"],
  },
};

export default function SeriesPage() {
  return (
    <div className="pt-28 pb-16">
      <div className="max-w-content mx-auto px-6">
        <h1 className="text-headline uppercase tracking-widest text-primary mb-2">
          Series
        </h1>
        <p className="text-body text-secondary max-w-xl mb-16">
          {series.length} mathematical languages for {series.length} human
          emotions. Each series uses a different class of functions to render a
          different quality of feeling.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-16">
          {series.map((s) => (
            <SeriesCard key={s.id} series={s} />
          ))}
        </div>
      </div>
    </div>
  );
}
