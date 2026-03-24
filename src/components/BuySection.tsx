"use client";

import { useState } from "react";
import { PRINT_SIZES } from "@/lib/products";
import { createCheckoutSession } from "@/app/actions/checkout";

interface BuySectionProps {
  pieceId: string;
}

export default function BuySection({ pieceId }: BuySectionProps) {
  const [selectedSize, setSelectedSize] = useState(PRINT_SIZES[0].id);
  const [loading, setLoading] = useState(false);

  const currentSize = PRINT_SIZES.find((s) => s.id === selectedSize)!;
  const priceDisplay = `$${currentSize.priceCents / 100}`;

  async function handleSubmit() {
    setLoading(true);
    try {
      const url = await createCheckoutSession(pieceId, selectedSize);
      window.location.href = url;
    } catch {
      setLoading(false);
    }
  }

  return (
    <div className="border border-border p-6 mb-4">
      <p className="text-headline text-primary mb-1">Fine Art Print</p>
      <p className="text-caption text-secondary mb-5">
        Hahnemuhle German Etching 310gsm — museum-grade matte
      </p>

      {/* Size selector */}
      <div className="flex gap-2 mb-5">
        {PRINT_SIZES.map((size) => (
          <button
            key={size.id}
            onClick={() => setSelectedSize(size.id)}
            className={`flex-1 py-2.5 text-caption font-mono border transition-all duration-300 ${
              selectedSize === size.id
                ? "border-primary bg-primary text-bg"
                : "border-border text-secondary hover:border-primary/40"
            }`}
          >
            <span className="block">{size.label}</span>
            <span className="block text-[11px] opacity-70">
              ${size.priceCents / 100}
            </span>
          </button>
        ))}
      </div>

      {/* Buy button */}
      <div className="flex items-center gap-4">
        <button
          onClick={handleSubmit}
          disabled={loading}
          className="flex-1 px-6 py-3 bg-primary text-bg text-caption uppercase tracking-widest hover:opacity-90 transition-opacity duration-500 disabled:opacity-50"
        >
          {loading ? "Redirecting..." : `Buy — ${priceDisplay}`}
        </button>
      </div>

      <p className="text-[11px] text-muted mt-3">
        Free shipping — 5-10 business days
      </p>
    </div>
  );
}
