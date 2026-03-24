"use client";

import { useState, useEffect } from "react";
import { PRINT_SIZES } from "@/lib/products";
import { createCheckoutSession } from "@/app/actions/checkout";

interface StickyBuyButtonProps {
  pieceId: string;
  title: string;
}

export default function StickyBuyButton({
  pieceId,
  title,
}: StickyBuyButtonProps) {
  const [visible, setVisible] = useState(false);
  const [selectedSize, setSelectedSize] = useState(PRINT_SIZES[0].id);
  const [loading, setLoading] = useState(false);

  const currentSize = PRINT_SIZES.find((s) => s.id === selectedSize)!;

  useEffect(() => {
    const handleScroll = () => {
      setVisible(window.scrollY > 400);
    };
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  async function handleSubmit() {
    setLoading(true);
    try {
      const url = await createCheckoutSession(pieceId, selectedSize);
      window.location.href = url;
    } catch {
      setLoading(false);
    }
  }

  if (!visible) return null;

  return (
    <div className="fixed bottom-0 left-0 right-0 z-40 md:hidden bg-bg/95 backdrop-blur-sm border-t border-border px-4 py-3">
      <div className="flex items-center justify-between gap-3">
        <div className="min-w-0 flex-1">
          <p className="text-caption text-primary truncate">{title}</p>
          <div className="flex gap-1.5 mt-1">
            {PRINT_SIZES.map((size) => (
              <button
                key={size.id}
                onClick={() => setSelectedSize(size.id)}
                className={`px-2 py-0.5 text-[10px] font-mono border transition-all ${
                  selectedSize === size.id
                    ? "border-primary bg-primary text-bg"
                    : "border-border text-muted"
                }`}
              >
                {size.dimensions}
              </button>
            ))}
          </div>
        </div>
        <button
          onClick={handleSubmit}
          disabled={loading}
          className="flex-shrink-0 px-5 py-2.5 bg-primary text-bg text-caption uppercase tracking-widest whitespace-nowrap disabled:opacity-50"
        >
          {loading
            ? "..."
            : `$${currentSize.priceCents / 100}`}
        </button>
      </div>
    </div>
  );
}
