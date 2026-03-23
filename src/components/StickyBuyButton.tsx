"use client";

import { useState, useEffect } from "react";

interface StickyBuyButtonProps {
  title: string;
  price: number;
  gumroadUrl: string;
}

export default function StickyBuyButton({
  title,
  price,
  gumroadUrl,
}: StickyBuyButtonProps) {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setVisible(window.scrollY > 400);
    };
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  if (!visible) return null;

  return (
    <div className="fixed bottom-0 left-0 right-0 z-40 md:hidden bg-bg/95 backdrop-blur-sm border-t border-border px-4 py-3">
      <div className="flex items-center justify-between gap-3">
        <div className="min-w-0">
          <p className="text-caption text-primary truncate">{title}</p>
          <p className="text-caption text-secondary">${price}</p>
        </div>
        <a
          href={gumroadUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="flex-shrink-0 px-5 py-2.5 bg-primary text-bg text-caption uppercase tracking-widest whitespace-nowrap"
        >
          Purchase
        </a>
      </div>
    </div>
  );
}
