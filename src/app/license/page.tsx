import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "License — Geometry of Feeling",
  alternates: { canonical: "/license" },
  description: "Personal use license terms for Geometry of Feeling fine art prints.",
  openGraph: {
    title: "License — Geometry of Feeling",
    description: "Personal use license terms for Geometry of Feeling fine art prints.",
  },
  twitter: {
    card: "summary_large_image",
  },
};

export default function LicensePage() {
  return (
    <div className="pt-28 pb-16">
      <div className="max-w-content mx-auto px-6">
        <div className="max-w-2xl">
          <h1 className="text-2xl font-mono font-light text-primary mb-12">
            License Terms
          </h1>

          <section className="mb-12">
            <h2 className="text-headline uppercase tracking-widest text-primary mb-6">
              Personal Use License
            </h2>
            <p className="text-body text-secondary mb-6">
              Every purchase from Geometry of Feeling includes a Personal Use
              License. This license is granted automatically upon purchase and
              applies to all fine art prints.
            </p>
          </section>

          <section className="mb-12">
            <h2 className="text-headline uppercase tracking-widest text-primary mb-6">
              What You Can Do
            </h2>
            <ul className="space-y-3 text-body text-secondary">
              <li className="flex gap-3">
                <span className="text-primary">+</span>
                Display your print for personal use in any setting
              </li>
              <li className="flex gap-3">
                <span className="text-primary">+</span>
                Display in your home, office, or personal space
              </li>
              <li className="flex gap-3">
                <span className="text-primary">+</span>
                Gift a printed copy to one other person
              </li>
              <li className="flex gap-3">
                <span className="text-primary">+</span>
                Use as a phone or desktop wallpaper for personal use
              </li>
              <li className="flex gap-3">
                <span className="text-primary">+</span>
                Share photos of your prints displayed in your space on social
                media (attribution appreciated)
              </li>
            </ul>
          </section>

          <section className="mb-12">
            <h2 className="text-headline uppercase tracking-widest text-primary mb-6">
              What Is Not Included
            </h2>
            <ul className="space-y-3 text-body text-secondary">
              <li className="flex gap-3">
                <span className="text-muted">&minus;</span>
                Commercial use of any kind (merchandise, products, branding)
              </li>
              <li className="flex gap-3">
                <span className="text-muted">&minus;</span>
                Resale of digital files or printed copies
              </li>
              <li className="flex gap-3">
                <span className="text-muted">&minus;</span>
                Reproducing or scanning prints for distribution
              </li>
              <li className="flex gap-3">
                <span className="text-muted">&minus;</span>
                Inclusion in AI training datasets
              </li>
              <li className="flex gap-3">
                <span className="text-muted">&minus;</span>
                Modification or derivative works for distribution
              </li>
            </ul>
          </section>

          <section className="border-t border-border pt-12">
            <p className="text-body text-secondary">
              For commercial licensing inquiries, please email{" "}
              <span className="text-primary">hello@geometryoffeeling.com</span>.
            </p>
          </section>
        </div>
      </div>
    </div>
  );
}
