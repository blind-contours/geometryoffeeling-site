"use client";

import Link from "next/link";
import { useState } from "react";

export default function Navigation() {
  const [open, setOpen] = useState(false);

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-bg/90 backdrop-blur-sm border-b border-border">
      <div className="max-w-content mx-auto px-6 h-14 flex items-center justify-between">
        <Link
          href="/"
          className="text-caption uppercase tracking-widest text-primary hover:opacity-70 transition-opacity duration-500"
        >
          Geometry of Feeling
        </Link>

        {/* Desktop */}
        <div className="hidden md:flex items-center gap-8">
          <Link
            href="/series"
            className="text-caption uppercase tracking-widest text-secondary hover:text-primary transition-colors duration-500"
          >
            Series
          </Link>
          <Link
            href="/shop"
            className="text-caption uppercase tracking-widest text-secondary hover:text-primary transition-colors duration-500"
          >
            Shop
          </Link>
          <Link
            href="/custom"
            className="text-caption uppercase tracking-widest text-secondary hover:text-primary transition-colors duration-500"
          >
            Custom
          </Link>
          <Link
            href="/printing"
            className="text-caption uppercase tracking-widest text-secondary hover:text-primary transition-colors duration-500"
          >
            Framing
          </Link>
          <Link
            href="/about"
            className="text-caption uppercase tracking-widest text-secondary hover:text-primary transition-colors duration-500"
          >
            About
          </Link>
        </div>

        {/* Mobile toggle */}
        <button
          onClick={() => setOpen(!open)}
          className="md:hidden min-h-[44px] min-w-[44px] flex items-center justify-center text-caption uppercase tracking-widest text-secondary"
          aria-label="Toggle menu"
        >
          {open ? "Close" : "Menu"}
        </button>
      </div>

      {/* Mobile menu */}
      {open && (
        <div className="md:hidden bg-bg border-b border-border px-6 pb-6 pt-2">
          <div className="flex flex-col">
            <Link
              href="/series"
              onClick={() => setOpen(false)}
              className="py-3 text-caption uppercase tracking-widest text-secondary hover:text-primary"
            >
              Series
            </Link>
            <Link
              href="/shop"
              onClick={() => setOpen(false)}
              className="py-3 text-caption uppercase tracking-widest text-secondary hover:text-primary"
            >
              Shop
            </Link>
            <Link
              href="/custom"
              onClick={() => setOpen(false)}
              className="py-3 text-caption uppercase tracking-widest text-secondary hover:text-primary"
            >
              Custom
            </Link>
            <Link
              href="/printing"
              onClick={() => setOpen(false)}
              className="py-3 text-caption uppercase tracking-widest text-secondary hover:text-primary"
            >
              Framing
            </Link>
            <Link
              href="/about"
              onClick={() => setOpen(false)}
              className="py-3 text-caption uppercase tracking-widest text-secondary hover:text-primary"
            >
              About
            </Link>
          </div>
        </div>
      )}
    </nav>
  );
}
