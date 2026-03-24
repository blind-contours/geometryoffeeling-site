"use client";

import Link from "next/link";

export default function Footer() {
  return (
    <footer className="border-t border-border bg-surface mt-24">
      <div className="max-w-content mx-auto px-6 py-16">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
          <div>
            <p className="text-caption uppercase tracking-widest text-primary mb-4">
              geometryoffeeling.com
            </p>
            <p className="text-body text-secondary">
              Mathematical fine art for people who think precisely and feel
              deeply.
            </p>
          </div>

          <div>
            <p className="text-caption uppercase tracking-widest text-primary mb-4">
              Navigate
            </p>
            <div className="flex flex-col gap-2">
              <Link
                href="/series"
                className="text-body text-secondary hover:text-primary transition-colors duration-500"
              >
                All Series
              </Link>
              <Link
                href="/shop"
                className="text-body text-secondary hover:text-primary transition-colors duration-500"
              >
                Shop
              </Link>
              <Link
                href="/about"
                className="text-body text-secondary hover:text-primary transition-colors duration-500"
              >
                About
              </Link>
            </div>
          </div>

          <div>
            <p className="text-caption uppercase tracking-widest text-primary mb-4">
              Stay in touch
            </p>
            <p className="text-body text-secondary mb-4">
              One email when new series drop. No spam.
            </p>
            <form
              onSubmit={(e) => e.preventDefault()}
              className="flex gap-2"
            >
              <input
                type="email"
                placeholder="your@email.com"
                className="flex-1 bg-bg border border-border px-3 py-2 text-body text-primary placeholder:text-muted focus:outline-none focus:border-secondary"
              />
              <button
                type="submit"
                className="px-4 py-2 border border-primary text-caption uppercase tracking-widest text-primary hover:bg-primary hover:text-bg transition-colors duration-500"
              >
                Join
              </button>
            </form>
          </div>
        </div>

        <div className="mt-16 pt-8 border-t border-border flex flex-col md:flex-row justify-between items-center gap-4">
          <p className="text-caption text-muted">
            Built by hand. Rendered in Python. Grounded in mathematics.
          </p>
          <p className="text-caption text-muted">
            &copy; {new Date().getFullYear()} Mathematical Affect
          </p>
        </div>
      </div>
    </footer>
  );
}
