import type { Metadata } from "next";
import CustomInquiryForm from "@/components/CustomInquiryForm";

export const metadata: Metadata = {
  title: "Commission a Custom Piece — Geometry of Feeling",
  alternates: { canonical: "/custom" },
  description:
    "Commission a custom mathematical art print with your choice of colors, parameters, dimensions, or an entirely new composition.",
  openGraph: {
    title: "Commission a Custom Piece — Geometry of Feeling",
    description:
      "Commission a custom mathematical art print with your choice of colors, parameters, dimensions, or an entirely new composition.",
    images: [{ url: "/prints/wonder/wonder_apollonian_gasket.jpg", width: 1680, height: 1155 }],
  },
  twitter: {
    card: "summary_large_image",
    images: ["/prints/wonder/wonder_apollonian_gasket.jpg"],
  },
};

interface Props {
  searchParams: { piece?: string };
}

export default function CustomPage({ searchParams }: Props) {
  return (
    <div className="pt-20 pb-24">
      <div className="max-w-content mx-auto px-6">
        {/* Hero */}
        <div className="max-w-2xl py-16">
          <h1 className="text-2xl md:text-3xl font-mono font-light text-primary mb-6">
            Commission a Custom Piece
          </h1>
          <p className="text-body text-secondary leading-relaxed">
            I write the Python code that generates every piece — which means
            custom variations are genuinely possible and unique. Different
            colors, adjusted parameters, custom dimensions, or an entirely
            new composition built from a feeling you choose.
          </p>
        </div>

        {/* What's possible */}
        <section className="max-w-2xl mb-20">
          <h2 className="text-headline uppercase tracking-widest text-primary mb-6">
            What&apos;s Possible
          </h2>
          <div className="space-y-4 text-body text-secondary">
            <p>
              <strong className="text-primary">Color palette changes</strong> — take
              any existing piece and recast it in colors that match your space or mood.
            </p>
            <p>
              <strong className="text-primary">Parameter tweaks</strong> — adjust the
              density, curvature, or intensity of a composition for a subtler or bolder result.
            </p>
            <p>
              <strong className="text-primary">Custom dimensions</strong> — need a
              specific size for a particular wall? I can re-render at any aspect ratio.
            </p>
            <p>
              <strong className="text-primary">New compositions</strong> — describe a
              feeling, and I&apos;ll research its mathematical shape and build something
              from first principles.
            </p>
          </div>
        </section>

        {/* How it works */}
        <section className="max-w-2xl mb-20">
          <h2 className="text-headline uppercase tracking-widest text-primary mb-8">
            How It Works
          </h2>
          <div className="space-y-8">
            <div className="flex gap-6">
              <span className="text-2xl font-mono font-light text-muted">1</span>
              <div>
                <h3 className="text-body font-medium text-primary mb-1">Inquire</h3>
                <p className="text-body text-secondary">
                  Fill out the form below with what you have in mind — a reference
                  piece, colors, dimensions, or just a feeling.
                </p>
              </div>
            </div>
            <div className="flex gap-6">
              <span className="text-2xl font-mono font-light text-muted">2</span>
              <div>
                <h3 className="text-body font-medium text-primary mb-1">Collaborate</h3>
                <p className="text-body text-secondary">
                  I&apos;ll send you initial renders and we&apos;ll iterate until
                  it feels right. Most pieces go through 2–3 rounds.
                </p>
              </div>
            </div>
            <div className="flex gap-6">
              <span className="text-2xl font-mono font-light text-muted">3</span>
              <div>
                <h3 className="text-body font-medium text-primary mb-1">Receive</h3>
                <p className="text-body text-secondary">
                  Your piece is printed on Hahnem&uuml;hle German Etching 310gsm
                  paper and shipped to your door.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Pricing & turnaround */}
        <section className="max-w-2xl mb-20">
          <div className="border border-border px-6 py-6 space-y-2">
            <p className="text-body text-primary">
              Custom prints start at <strong>$200</strong>.
            </p>
            <p className="text-body text-secondary">
              Typical turnaround is 2–3 weeks from first conversation to shipped print.
            </p>
          </div>
        </section>

        {/* Inquiry form */}
        <section className="max-w-2xl">
          <h2 className="text-headline uppercase tracking-widest text-primary mb-8">
            Start a Conversation
          </h2>
          <CustomInquiryForm defaultPiece={searchParams.piece} />
        </section>
      </div>
    </div>
  );
}
