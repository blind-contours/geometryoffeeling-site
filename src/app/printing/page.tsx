import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Framing Guide — Geometry of Feeling",
  alternates: { canonical: "/printing" },
  description:
    "How to frame your Geometry of Feeling fine art print. Recommended frames for every size with direct links.",
  openGraph: {
    title: "Framing Guide — Geometry of Feeling",
    description:
      "How to frame your Geometry of Feeling fine art print. Recommended frames for every size with direct links.",
  },
  twitter: {
    card: "summary_large_image",
  },
};

const frames = {
  small: {
    size: '12 \u00d7 8"',
    prints: "Entry-level — desk, shelf, or small wall",
    options: [
      {
        name: "Craig Frames 1WB3BK",
        price: "$17",
        note: "Clean contemporary profile, hand-crafted in Michigan. Our top pick.",
        url: "https://www.amazon.com/Craig-Frames-1WB3BK-12-Inch-Picture/dp/B0046B5K18",
        colors: "Black, White, Natural, Walnut",
      },
      {
        name: "upsimples 8x12 Frame",
        price: "$12",
        note: "Best budget option. Shatter-resistant glass, clean lines.",
        url: "https://www.amazon.com/upsimples-Picture-Display-Pictures-Without/dp/B0BQQZ2FCJ",
        colors: "Black, Brown",
      },
      {
        name: "Fkvat Aluminum Frame",
        price: "$10/ea (4-pack)",
        note: "Ultra-thin metal profile. Modern and minimal — great for sets.",
        url: "https://www.amazon.com/Fkvat-Aluminum-Vertical-Horizontal-Tabletop/dp/B0C1TXYK6W",
        colors: "Black, Brass, Gold, Silver",
      },
    ],
  },
  medium: {
    size: '24 \u00d7 16"',
    prints: "Wall piece — living room, office, bedroom",
    options: [
      {
        name: "Craig Frames 1WB3BK",
        price: "$28",
        note: "Same series as the 12\u00d78 — consistent look across sizes.",
        url: "https://www.amazon.com/Craig-Frames-1WB3BK-24-Inch-Smooth/dp/B0049OEQ4Y",
        colors: "Black, White, Natural, Walnut",
      },
      {
        name: "Homeforia Metal Frame",
        price: "$40",
        note: "Aluminum with tempered glass. Sharp, gallery feel.",
        url: "https://www.amazon.com/16-24-POSTER-FRAME-BLACK/dp/B0BJBKNM7X",
        colors: "Black, Silver, Gold, Natural Wood",
      },
      {
        name: "Frame Amo Modern Frame",
        price: "$22",
        note: "5,000+ reviews. Clean MDF with acrylic face.",
        url: "https://www.amazon.com/Frame-Amo-Modern-Picture-Poster/dp/B07PF5M1SY",
        colors: "Black, White, Walnut Brown",
      },
    ],
  },
  large: {
    size: '36 \u00d7 24"',
    prints: "Statement piece — main wall, above sofa, entryway",
    options: [
      {
        name: "IKEA R\u00d6DALM",
        price: "$10",
        note: "Unbeatable value. The 24\u00d736 is a perfect fit.",
        url: "https://www.ikea.com/us/en/p/roedalm-frame-black-30548932/",
        colors: "Black ($10), White ($10), Birch ($15), Oak ($40)",
      },
      {
        name: "Craig Frames 1WB3BK",
        price: "$35",
        note: "Matches the smaller Craig Frames for a cohesive collection.",
        url: "https://www.amazon.com/Craig-Frames-1WB3BK-36-Inch-Picture/dp/B0046B7NGI",
        colors: "Black, White, Natural, Walnut",
      },
      {
        name: "Homeforia Metal Frame",
        price: "$60",
        note: "Premium aluminum, tempered glass. Gallery quality.",
        url: "https://www.amazon.com/24X36-POSTER-PICTURE-FRAME-BLACK/dp/B0D3MDVFTP",
        colors: "Black, Silver, Rose Gold",
      },
    ],
  },
  xlarge: {
    size: '48 \u00d7 32"',
    prints: "Gallery piece — feature wall, above dining table, office lobby",
    options: [
      {
        name: "MCS Floating Frame",
        price: "$75",
        note: "Floating canvas-style frame. The print appears to hover — dramatic at this scale.",
        url: "https://www.amazon.com/MCS-Floating-Frame-32x48-Natural/dp/B08JQ7GLHP",
        colors: "Black, Natural, Walnut",
      },
      {
        name: "Craig Frames Colori",
        price: "$55",
        note: "Clean wide-profile frame. Solid wood, fits 32\u00d748 prints exactly.",
        url: "https://www.amazon.com/Craig-Frames-Colori-Picture-Poster/dp/B00JGKR0UE",
        colors: "Black, White, Grey",
      },
      {
        name: "Americanflat 32x48 Frame",
        price: "$65",
        note: "Composite wood with shatter-resistant glass. Slim gallery profile.",
        url: "https://www.amazon.com/Americanflat-Composite-Shatter-Resistant-Hanging-Hardware/dp/B0CYZ5ZZGZ",
        colors: "Black, White",
      },
    ],
  },
};

export default function PrintingPage() {
  return (
    <div className="pt-28 pb-16">
      <div className="max-w-content mx-auto px-6">
        <div className="max-w-2xl">
          <h1 className="text-2xl font-mono font-light text-primary mb-4">
            Framing Guide
          </h1>
          <p className="text-body text-secondary mb-12">
            Every print ships flat and unframed on Hahnem&uuml;hle German
            Etching 310gsm — museum-grade matte paper with a warm, textured
            finish. Here are frames we recommend for each size.
          </p>

          {/* Your Print */}
          <section className="mb-12">
            <h2 className="text-headline uppercase tracking-widest text-primary mb-6">
              Your Print
            </h2>
            <div className="border border-border divide-y divide-border">
              <div className="flex justify-between px-4 py-3">
                <span className="text-body text-primary">Paper</span>
                <span className="text-body text-secondary">
                  Hahnem&uuml;hle German Etching 310gsm
                </span>
              </div>
              <div className="flex justify-between px-4 py-3">
                <span className="text-body text-primary">Finish</span>
                <span className="text-body text-secondary">
                  Warm white, velvety matte texture
                </span>
              </div>
              <div className="flex justify-between px-4 py-3">
                <span className="text-body text-primary">Orientation</span>
                <span className="text-body text-secondary">
                  Landscape (wider than tall)
                </span>
              </div>
              <div className="flex justify-between px-4 py-3">
                <span className="text-body text-primary">Sizes</span>
                <span className="text-body text-secondary">
                  12&times;8&quot; &nbsp;|&nbsp; 24&times;16&quot; &nbsp;|&nbsp;
                  36&times;24&quot; &nbsp;|&nbsp; 48&times;32&quot;
                </span>
              </div>
            </div>
          </section>

          {/* Frame Recommendations */}
          {(
            Object.entries(frames) as [
              string,
              (typeof frames)[keyof typeof frames],
            ][]
          ).map(([key, section]) => (
            <section key={key} className="mb-12">
              <h2 className="text-headline uppercase tracking-widest text-primary mb-2">
                {section.size}
              </h2>
              <p className="text-caption text-muted mb-6">{section.prints}</p>
              <div className="space-y-6">
                {section.options.map((frame) => (
                  <div key={frame.name} className="border border-border p-5">
                    <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-2 mb-2">
                      <a
                        href={frame.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-body text-primary hover:opacity-70 transition-opacity duration-500"
                      >
                        {frame.name} &rarr;
                      </a>
                      <span className="text-body text-primary font-medium">
                        {frame.price}
                      </span>
                    </div>
                    <p className="text-caption text-secondary mb-1">
                      {frame.note}
                    </p>
                    <p className="text-caption text-muted">{frame.colors}</p>
                  </div>
                ))}
              </div>
            </section>
          ))}

          {/* Tips */}
          <section className="mb-12">
            <h2 className="text-headline uppercase tracking-widest text-primary mb-6">
              Framing Tips
            </h2>
            <ul className="space-y-3 text-body text-secondary">
              <li className="flex gap-3">
                <span className="text-primary shrink-0">+</span>
                Use the frame without a mat for the cleanest look — the print
                fills the full frame edge to edge.
              </li>
              <li className="flex gap-3">
                <span className="text-primary shrink-0">+</span>
                Black or natural wood frames complement the warm paper tone
                best.
              </li>
              <li className="flex gap-3">
                <span className="text-primary shrink-0">+</span>
                For UV protection, choose frames with acrylic or UV glass —
                especially in sunlit rooms.
              </li>
              <li className="flex gap-3">
                <span className="text-primary shrink-0">+</span>
                Hang at eye level (center of the piece at roughly 57 inches from
                the floor — the gallery standard).
              </li>
            </ul>
          </section>

          {/* Matching Set */}
          <section className="border border-primary p-6 mb-12">
            <h2 className="text-headline text-primary mb-3">
              Want a matching set?
            </h2>
            <p className="text-body text-secondary mb-4">
              The Craig Frames 1WB3BK comes in all four sizes with the same
              clean profile. Order a set for a cohesive gallery wall — from
              about $80 total.
            </p>
            <Link
              href="/shop"
              className="text-caption uppercase tracking-widest text-primary hover:opacity-70 transition-opacity duration-500"
            >
              Browse prints &rarr;
            </Link>
          </section>

          {/* Color Note */}
          <section className="border border-border p-6">
            <h2 className="text-headline text-primary mb-3">
              A Note on Color
            </h2>
            <p className="text-body text-secondary">
              German Etching paper has a warm white tone that gives each piece a
              subtle warmth you won&apos;t see on screen. This is intentional —
              the prints feel richer and more tactile in person than they appear
              digitally.
            </p>
          </section>
        </div>
      </div>
    </div>
  );
}
