"use client";

import { useState } from "react";

export default function LicenseTerms({ compact = false }: { compact?: boolean }) {
  const [expanded, setExpanded] = useState(false);

  if (compact) {
    return (
      <div className="relative inline-block">
        <button
          onClick={() => setExpanded(!expanded)}
          className="text-caption text-muted hover:text-secondary transition-colors underline underline-offset-2"
        >
          License terms
        </button>
        {expanded && (
          <div className="absolute bottom-full left-0 mb-2 w-72 bg-surface border border-border p-4 z-50 shadow-sm">
            <p className="text-caption text-secondary leading-relaxed">
              Personal use license included. Print unlimited copies for your own
              walls. Gift one printed copy. Use as personal wallpaper. Not for
              commercial use, resale, or AI training datasets.
            </p>
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="border border-border p-6">
      <h3 className="text-headline text-primary mb-4">
        Personal Use License
      </h3>
      <p className="text-body text-secondary mb-4">
        Every purchase includes a personal use license. Print as many copies as
        you like for your own walls. Not for commercial use or resale.
      </p>
      <div className="space-y-2 text-body text-secondary">
        <p>Included:</p>
        <ul className="list-disc list-inside space-y-1 text-caption">
          <li>Print for personal use, unlimited times, any size</li>
          <li>Display in your home, office, or personal space</li>
          <li>Gift a printed copy to one other person</li>
          <li>Use as phone/desktop wallpaper for personal use</li>
        </ul>
        <p className="mt-3">Not included:</p>
        <ul className="list-disc list-inside space-y-1 text-caption text-muted">
          <li>Commercial use or resale</li>
          <li>Sharing digital files</li>
          <li>Use in AI training datasets</li>
        </ul>
      </div>
    </div>
  );
}
