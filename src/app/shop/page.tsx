"use client";

import { useState } from "react";
import PrintCard from "@/components/PrintCard";
import Link from "next/link";
import { series, allPieces } from "@/data/series";

export default function ShopPage() {
  const [filterSeries, setFilterSeries] = useState<string>("all");
  const [sortBy, setSortBy] = useState<string>("series");

  const filtered =
    filterSeries === "all"
      ? allPieces
      : allPieces.filter((p) => p.series === filterSeries);

  const sorted = [...filtered].sort((a, b) => {
    if (sortBy === "price-low") return a.price - b.price;
    if (sortBy === "price-high") return b.price - a.price;
    if (sortBy === "title") return a.title.localeCompare(b.title);
    return 0; // default: series order
  });

  return (
    <div className="pt-28 pb-16">
      <div className="max-w-content mx-auto px-6">
        <h1 className="text-headline uppercase tracking-widest text-primary mb-2">
          Shop
        </h1>
        <p className="text-body text-secondary max-w-xl mb-8">
          Museum-grade fine art prints on Hahnemuhle German Etching 310gsm. Free shipping.
        </p>

        {/* Start with a series — prominent CTA */}
        <div className="border border-border p-8 mb-12">
          <h2 className="text-headline text-primary mb-2">
            Start with a series
          </h2>
          <p className="text-body text-secondary mb-4">
            Series bundles save 20% and give you a cohesive collection built
            around a single emotional theme.
          </p>
          <div className="flex flex-wrap gap-3">
            {series.map((s) => (
              <Link
                key={s.id}
                href={`/series/${s.id}`}
                className="px-4 py-2 border border-border text-caption uppercase tracking-widest text-secondary hover:text-primary hover:border-primary transition-colors duration-500"
              >
                {s.name}
              </Link>
            ))}
          </div>
        </div>

        {/* Pricing info */}
        <div className="border border-primary p-8 mb-12">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-6">
            <div>
              <h2 className="text-headline text-primary mb-2">
                Three Sizes, One Paper
              </h2>
              <p className="text-body text-secondary">
                10&times;8&quot; — $45 &nbsp;|&nbsp; 20&times;16&quot; — $95 &nbsp;|&nbsp; 36&times;24&quot; — $175
              </p>
              <p className="text-caption text-muted mt-2">
                Free shipping — 5-10 business days
              </p>
            </div>
          </div>
        </div>

        {/* Filters */}
        <div className="flex flex-col sm:flex-row gap-4 mb-12">
          <div className="flex items-center gap-2">
            <label className="text-caption uppercase tracking-widest text-muted">
              Filter:
            </label>
            <select
              value={filterSeries}
              onChange={(e) => setFilterSeries(e.target.value)}
              className="bg-bg border border-border px-3 py-2 text-body text-primary focus:outline-none focus:border-secondary"
            >
              <option value="all">All Series</option>
              {series.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.name}
                </option>
              ))}
            </select>
          </div>
          <div className="flex items-center gap-2">
            <label className="text-caption uppercase tracking-widest text-muted">
              Sort:
            </label>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="bg-bg border border-border px-3 py-2 text-body text-primary focus:outline-none focus:border-secondary"
            >
              <option value="series">Series Order</option>
              <option value="price-low">Price: Low to High</option>
              <option value="price-high">Price: High to Low</option>
              <option value="title">Title A-Z</option>
            </select>
          </div>
        </div>

        {/* Product grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-10">
          {sorted.map((piece) => (
            <PrintCard key={piece.id} piece={piece} showBuyButton />
          ))}
        </div>
      </div>
    </div>
  );
}
