import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Printing Guide — Geometry of Feeling",
  description: "Museum-grade fine art prints on Hahnemühle German Etching 310gsm — printing and framing guide.",
  openGraph: {
    title: "Printing Guide — Geometry of Feeling",
    description: "Museum-grade fine art prints on Hahnemühle German Etching 310gsm — printing and framing guide.",
  },
  twitter: {
    card: "summary_large_image",
  },
};

export default function PrintingPage() {
  return (
    <div className="pt-28 pb-16">
      <div className="max-w-content mx-auto px-6">
        <div className="max-w-2xl">
          <h1 className="text-2xl font-mono font-light text-primary mb-4">
            How to Print
          </h1>
          <p className="text-body text-secondary mb-12">
            Your files are 300 DPI print-ready PDFs. Here is everything you need
            to get gallery-quality results.
          </p>

          <section className="mb-12">
            <h2 className="text-headline uppercase tracking-widest text-primary mb-6">
              Recommended Paper
            </h2>
            <p className="text-body text-secondary mb-4">
              Fine art matte, 180&ndash;220gsm, acid-free. This is the paper used
              in galleries. It produces deep blacks, subtle texture, and no glare.
            </p>
            <p className="text-body text-muted">
              Do not use glossy photo paper. The art was designed for matte
              surfaces.
            </p>
          </section>

          <section className="mb-12">
            <h2 className="text-headline uppercase tracking-widest text-primary mb-6">
              Sizes That Work
            </h2>
            <p className="text-body text-secondary mb-4">
              The files are 11&times;7.5 inches at 300 DPI (landscape orientation).
            </p>
            <div className="border border-border divide-y divide-border">
              {[
                { size: '11 x 7.5"', note: "Exact file size — sharpest possible" },
                { size: '14 x 10"', note: "Slight upscale, still sharp" },
                { size: '18 x 12"', note: "Ideal wall size — my recommendation" },
                { size: '24 x 16"', note: "Large statement piece — maximum recommended size" },
              ].map((row) => (
                <div key={row.size} className="flex justify-between px-4 py-3">
                  <span className="text-body text-primary font-medium">
                    {row.size}
                  </span>
                  <span className="text-body text-secondary">{row.note}</span>
                </div>
              ))}
            </div>
            <p className="text-caption text-muted mt-3">
              Do not exceed 24&times;16&quot; for digital downloads — resolution will
              degrade.
            </p>
          </section>

          <section className="mb-12">
            <h2 className="text-headline uppercase tracking-widest text-primary mb-6">
              Where to Print
            </h2>
            <div className="space-y-4 text-body text-secondary">
              <div>
                <p className="text-primary">Online (recommended)</p>
                <ul className="list-disc list-inside text-caption mt-1 space-y-1">
                  <li>Mpix.com — best quality, fine art paper options</li>
                  <li>Nations Photo Lab — professional results</li>
                  <li>Printingforless.com — bulk orders</li>
                </ul>
              </div>
              <div>
                <p className="text-primary">Local</p>
                <ul className="list-disc list-inside text-caption mt-1 space-y-1">
                  <li>
                    FedEx Office — request fine art paper (not standard glossy)
                  </li>
                  <li>Local print shop — best option if available</li>
                </ul>
              </div>
            </div>
          </section>

          <section className="mb-12">
            <h2 className="text-headline uppercase tracking-widest text-primary mb-6">
              Framing
            </h2>
            <p className="text-body text-secondary mb-4">
              Simple black or natural wood frame, white mat. The art is minimal —
              the frame should be too.
            </p>
            <p className="text-body text-secondary">
              IKEA RIBBA fits 18&times;12&quot; with matting. For custom framing,
              request UV-protective glass and acid-free mat board.
            </p>
          </section>

          <section className="border border-border p-6">
            <h2 className="text-headline text-primary mb-3">Color Note</h2>
            <p className="text-body text-secondary">
              Files are RGB. Colors may shift slightly in print — this is normal
              for any digital-to-print workflow. For critical color accuracy,
              request an ICC profile preview at a professional lab.
            </p>
          </section>
        </div>
      </div>
    </div>
  );
}
