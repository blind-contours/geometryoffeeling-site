"use client";

import { useState } from "react";

interface Props {
  defaultPiece?: string;
}

export default function CustomInquiryForm({ defaultPiece }: Props) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [piece, setPiece] = useState(defaultPiece ?? "");
  const [description, setDescription] = useState("");
  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">("idle");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!name || !email || !description) return;
    setStatus("loading");
    try {
      const res = await fetch("/api/inquire", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, piece, description }),
      });
      if (res.ok) {
        setStatus("success");
      } else {
        setStatus("error");
      }
    } catch {
      setStatus("error");
    }
  }

  if (status === "success") {
    return (
      <div className="text-center py-12">
        <h3 className="text-lg font-mono font-light text-primary mb-4">
          Inquiry received.
        </h3>
        <p className="text-body text-secondary">
          I&apos;ll review your request and get back to you within a few days.
        </p>
      </div>
    );
  }

  const inputClasses =
    "w-full bg-bg border border-border px-4 py-3 text-body text-primary placeholder:text-muted focus:outline-none focus:border-secondary";

  return (
    <form onSubmit={handleSubmit} className="space-y-6 max-w-lg">
      <div>
        <label htmlFor="name" className="block text-caption uppercase tracking-widest text-secondary mb-2">
          Name
        </label>
        <input
          id="name"
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
          className={inputClasses}
        />
      </div>

      <div>
        <label htmlFor="email" className="block text-caption uppercase tracking-widest text-secondary mb-2">
          Email
        </label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className={inputClasses}
        />
      </div>

      <div>
        <label htmlFor="piece" className="block text-caption uppercase tracking-widest text-secondary mb-2">
          Piece or series of interest <span className="normal-case tracking-normal">(optional)</span>
        </label>
        <input
          id="piece"
          type="text"
          value={piece}
          onChange={(e) => setPiece(e.target.value)}
          placeholder="e.g. Convergence, Grief series"
          className={inputClasses}
        />
      </div>

      <div>
        <label htmlFor="description" className="block text-caption uppercase tracking-widest text-secondary mb-2">
          What are you envisioning?
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          required
          rows={5}
          placeholder="Different colors, custom dimensions, a new composition inspired by a specific feeling..."
          className={inputClasses + " resize-vertical"}
        />
      </div>

      <button
        type="submit"
        disabled={status === "loading"}
        className="px-8 py-3 border border-primary text-caption uppercase tracking-widest text-primary hover:bg-primary hover:text-bg transition-colors duration-500 disabled:opacity-50"
      >
        {status === "loading" ? "Sending..." : "Send Inquiry"}
      </button>

      {status === "error" && (
        <p className="text-caption text-red-500">Something went wrong. Please try again.</p>
      )}
    </form>
  );
}
