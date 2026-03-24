"use client";

import { useState } from "react";

export default function EmailCapture() {
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">("idle");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!email) return;
    setStatus("loading");
    try {
      const res = await fetch("/api/subscribe", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });
      if (res.ok) {
        setStatus("success");
        setEmail("");
      } else {
        setStatus("error");
      }
    } catch {
      setStatus("error");
    }
  }

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
          {status === "success" ? (
            <p className="text-body text-primary">You&apos;re in. I&apos;ll be in touch.</p>
          ) : (
            <form onSubmit={handleSubmit} className="flex gap-2 max-w-md mx-auto">
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="your@email.com"
                required
                className="flex-1 bg-bg border border-border px-4 py-3 text-body text-primary placeholder:text-muted focus:outline-none focus:border-secondary"
              />
              <button
                type="submit"
                disabled={status === "loading"}
                className="px-6 py-3 border border-primary text-caption uppercase tracking-widest text-primary hover:bg-primary hover:text-bg transition-colors duration-500 disabled:opacity-50"
              >
                {status === "loading" ? "..." : "Subscribe"}
              </button>
            </form>
          )}
          {status === "error" && (
            <p className="text-caption text-red-500 mt-3">Something went wrong. Please try again.</p>
          )}
        </div>
      </div>
    </section>
  );
}
