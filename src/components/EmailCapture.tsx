"use client";

export default function EmailCapture() {
  return (
    <section className="border-t border-border">
      <div className="max-w-content mx-auto px-6 py-24">
        <div className="max-w-xl mx-auto text-center">
          <h2 className="text-lg md:text-xl font-mono font-light text-primary mb-4">
            Stay in the loop
          </h2>
          <p className="text-body text-secondary mb-8">
            I send one email when a new series drops. No spam, no algorithms
            — just new work.
          </p>
          <form
            onSubmit={(e) => e.preventDefault()}
            className="flex gap-2 max-w-md mx-auto"
          >
            <input
              type="email"
              placeholder="your@email.com"
              className="flex-1 bg-bg border border-border px-4 py-3 text-body text-primary placeholder:text-muted focus:outline-none focus:border-secondary"
            />
            <button
              type="submit"
              className="px-6 py-3 border border-primary text-caption uppercase tracking-widest text-primary hover:bg-primary hover:text-bg transition-colors duration-500"
            >
              Subscribe
            </button>
          </form>
        </div>
      </div>
    </section>
  );
}
