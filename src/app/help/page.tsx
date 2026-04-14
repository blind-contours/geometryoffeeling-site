import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Help — Geometry of Feeling",
  description:
    "Shipping, returns, print care, and FAQs for Geometry of Feeling fine art prints.",
  openGraph: {
    title: "Help — Geometry of Feeling",
    description:
      "Shipping, returns, print care, and FAQs for Geometry of Feeling fine art prints.",
  },
  twitter: {
    card: "summary_large_image",
  },
};

const faqJsonLd = {
  "@context": "https://schema.org",
  "@type": "FAQPage",
  mainEntity: [
    {
      "@type": "Question",
      name: "How long does shipping take?",
      acceptedAnswer: {
        "@type": "Answer",
        text: "Free worldwide shipping on every order, with delivery in 5-10 business days. Prints are produced and shipped from the facility nearest to you via Prodigi's global network. Tracking is provided via email once your order ships.",
      },
    },
    {
      "@type": "Question",
      name: "What paper are the prints on?",
      acceptedAnswer: {
        "@type": "Answer",
        text: "All prints use Hahnemühle German Etching 310gsm — a museum-grade, warm white, velvety matte paper. Printed with archival pigment inks (giclée) by a Fine Art Trade Guild approved printer. Prints feel richer and more tactile in person than on screen.",
      },
    },
    {
      "@type": "Question",
      name: "What sizes are available?",
      acceptedAnswer: {
        "@type": "Answer",
        text: "Four sizes are available: 12×8\" ($45), 24×16\" ($95), 36×24\" ($175), and 48×32\" ($295). The 48×32\" size is available on select pieces. All prints are landscape orientation.",
      },
    },
    {
      "@type": "Question",
      name: "What if my print arrives damaged?",
      acceptedAnswer: {
        "@type": "Answer",
        text: "Email hello@geometryoffeeling.com with a photo of the damage. We offer free reprinting and free reshipping for any quality issue — no questions asked. Please notify within 14 days of delivery.",
      },
    },
    {
      "@type": "Question",
      name: "How should I care for my print?",
      acceptedAnswer: {
        "@type": "Answer",
        text: "Handle prints by the edges to avoid fingerprints. For UV protection, use frames with acrylic or UV glass in sunlit rooms. Store flat in a cool, dry place if not immediately framing. See our framing guide for recommended frames at every size.",
      },
    },
  ],
};

export default function HelpPage() {
  return (
    <div className="pt-28 pb-16">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(faqJsonLd) }}
      />
      <div className="max-w-content mx-auto px-6">
        <div className="max-w-2xl">
          <h1 className="text-2xl font-mono font-light text-primary mb-4">
            Help
          </h1>
          <p className="text-body text-secondary mb-12">
            Everything you need to know about ordering, shipping, and caring for
            your prints.
          </p>

          {/* Shipping */}
          <section className="mb-12">
            <h2 className="text-headline uppercase tracking-widest text-primary mb-6">
              Shipping
            </h2>
            <ul className="space-y-3 text-body text-secondary">
              <li className="flex gap-3">
                <span className="text-primary shrink-0">+</span>
                Free worldwide shipping on every order.
              </li>
              <li className="flex gap-3">
                <span className="text-primary shrink-0">+</span>
                Delivery in 5-10 business days.
              </li>
              <li className="flex gap-3">
                <span className="text-primary shrink-0">+</span>
                Printed and shipped from the facility nearest to you via
                Prodigi&apos;s global network.
              </li>
              <li className="flex gap-3">
                <span className="text-primary shrink-0">+</span>
                Tracking provided via email once your order ships.
              </li>
            </ul>
          </section>

          {/* Paper & Printing */}
          <section className="mb-12">
            <h2 className="text-headline uppercase tracking-widest text-primary mb-6">
              Paper &amp; Printing
            </h2>
            <ul className="space-y-3 text-body text-secondary">
              <li className="flex gap-3">
                <span className="text-primary shrink-0">+</span>
                Hahnem&uuml;hle German Etching 310gsm — museum-grade, warm
                white, velvety matte.
              </li>
              <li className="flex gap-3">
                <span className="text-primary shrink-0">+</span>
                Archival pigment inks (gicl&eacute;e).
              </li>
              <li className="flex gap-3">
                <span className="text-primary shrink-0">+</span>
                Fine Art Trade Guild approved printing.
              </li>
              <li className="flex gap-3">
                <span className="text-primary shrink-0">+</span>
                Prints feel richer and more tactile in person than on screen.
              </li>
            </ul>
          </section>

          {/* Sizes */}
          <section className="mb-12">
            <h2 className="text-headline uppercase tracking-widest text-primary mb-6">
              Sizes
            </h2>
            <div className="border border-border divide-y divide-border mb-4">
              <div className="flex justify-between px-4 py-3">
                <span className="text-body text-primary">12&times;8&quot;</span>
                <span className="text-body text-secondary">$45</span>
              </div>
              <div className="flex justify-between px-4 py-3">
                <span className="text-body text-primary">
                  24&times;16&quot;
                </span>
                <span className="text-body text-secondary">$95</span>
              </div>
              <div className="flex justify-between px-4 py-3">
                <span className="text-body text-primary">
                  36&times;24&quot;
                </span>
                <span className="text-body text-secondary">$175</span>
              </div>
              <div className="flex justify-between px-4 py-3">
                <span className="text-body text-primary">
                  48&times;32&quot;
                </span>
                <span className="text-body text-secondary">$295</span>
              </div>
            </div>
            <p className="text-caption text-muted">
              48 &times; 32 available on select pieces. All prints landscape
              orientation.
            </p>
          </section>

          {/* Replacements & Quality */}
          <section className="mb-12">
            <h2 className="text-headline uppercase tracking-widest text-primary mb-6">
              Replacements &amp; Quality
            </h2>
            <ul className="space-y-3 text-body text-secondary">
              <li className="flex gap-3">
                <span className="text-primary shrink-0">+</span>
                Prints are produced and fulfilled by Prodigi, a Fine Art Trade
                Guild approved printer.
              </li>
              <li className="flex gap-3">
                <span className="text-primary shrink-0">+</span>
                If your print arrives damaged or defective, email{" "}
                <a
                  href="mailto:hello@geometryoffeeling.com"
                  className="text-primary underline underline-offset-4 hover:opacity-70 transition-opacity duration-500"
                >
                  hello@geometryoffeeling.com
                </a>{" "}
                with a photo.
              </li>
              <li className="flex gap-3">
                <span className="text-primary shrink-0">+</span>
                Free reprint and free reshipping for any quality issue — no
                questions asked.
              </li>
              <li className="flex gap-3">
                <span className="text-primary shrink-0">+</span>
                Please notify within 14 days of delivery.
              </li>
              <li className="flex gap-3">
                <span className="text-primary shrink-0">+</span>
                <a
                  href="https://www.prodigi.com/faq/returns-and-cancellations/"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-primary underline underline-offset-4 hover:opacity-70 transition-opacity duration-500"
                >
                  Prodigi&apos;s returns FAQ &rarr;
                </a>
              </li>
            </ul>
          </section>

          {/* Care & Display */}
          <section className="mb-12">
            <h2 className="text-headline uppercase tracking-widest text-primary mb-6">
              Care &amp; Display
            </h2>
            <ul className="space-y-3 text-body text-secondary">
              <li className="flex gap-3">
                <span className="text-primary shrink-0">+</span>
                See our{" "}
                <Link
                  href="/printing"
                  className="text-primary underline underline-offset-4 hover:opacity-70 transition-opacity duration-500"
                >
                  framing guide
                </Link>{" "}
                for recommended frames at every size.
              </li>
              <li className="flex gap-3">
                <span className="text-primary shrink-0">+</span>
                Handle prints by the edges to avoid fingerprints.
              </li>
              <li className="flex gap-3">
                <span className="text-primary shrink-0">+</span>
                For UV protection, use frames with acrylic or UV glass in sunlit
                rooms.
              </li>
              <li className="flex gap-3">
                <span className="text-primary shrink-0">+</span>
                Store flat in a cool, dry place if not immediately framing.
              </li>
            </ul>
          </section>

          {/* Contact */}
          <section className="border border-primary p-6">
            <h2 className="text-headline text-primary mb-3">Contact</h2>
            <p className="text-body text-secondary mb-2">
              <a
                href="mailto:hello@geometryoffeeling.com"
                className="text-primary underline underline-offset-4 hover:opacity-70 transition-opacity duration-500"
              >
                hello@geometryoffeeling.com
              </a>
            </p>
            <p className="text-caption text-muted">
              Typical response within 24 hours.
            </p>
          </section>
        </div>
      </div>
    </div>
  );
}
