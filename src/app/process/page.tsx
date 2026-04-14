import Link from "next/link";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title:
    "Hand-Coded, Not AI-Generated | How Geometry of Feeling Is Made",
  description:
    "See how Geometry of Feeling creates minimalist generative art by hand-coding equations in Python. No prompts, no image generators — just mathematics, structure, and feeling.",
  keywords: [
    "hand-coded generative art",
    "not AI-generated art",
    "how mathematical art is made",
    "generative art process",
    "Python generative art",
    "hand-coded art prints",
    "mathematical art process",
  ],
  openGraph: {
    title:
      "Hand-Coded, Not AI-Generated | How Geometry of Feeling Is Made",
    description:
      "See how Geometry of Feeling creates minimalist generative art by hand-coding equations in Python. No prompts, no image generators — just mathematics, structure, and feeling.",
    images: [
      {
        url: "/prints/awe/awe_eclipse.jpg",
        width: 1680,
        height: 1155,
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    images: ["/prints/awe/awe_eclipse.jpg"],
  },
};

const faqItems = [
  {
    question: "Are these works AI-generated?",
    answer:
      "No. Every piece is built from code I write by hand in Python. I do not use image generators, prompts, or style transfer.",
  },
  {
    question: "What does hand-coded mean?",
    answer:
      "It means the underlying structure of each image comes from rules, equations, and systems I write directly, then refine through iteration.",
  },
  {
    question: "Do I need to understand math to connect with the work?",
    answer:
      "No. The math is the cause of the image, not a barrier to it. The point is the feeling.",
  },
  {
    question: "Why use mathematics to make emotional art?",
    answer:
      "Because mathematics can govern motion, tension, repetition, decay, attraction, spread, and structure. Those are also emotional experiences.",
  },
  {
    question: "Are these available as prints?",
    answer:
      "Yes. Museum-quality giclée prints on Hahnemühle German Etching 310gsm are available throughout the site in multiple sizes, starting from $45 with free shipping.",
  },
];

const faqJsonLd = {
  "@context": "https://schema.org",
  "@type": "FAQPage",
  mainEntity: faqItems.map((item) => ({
    "@type": "Question",
    name: item.question,
    acceptedAnswer: {
      "@type": "Answer",
      text: item.answer,
    },
  })),
};

export default function ProcessPage() {
  return (
    <div className="pt-28 pb-16">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(faqJsonLd) }}
      />
      <div className="max-w-content mx-auto px-6">
        <div className="max-w-2xl">
          {/* Hero */}
          <h1 className="text-2xl md:text-3xl font-mono font-light text-primary mb-8">
            Hand-Coded, Not AI-Generated
          </h1>
          <p className="text-lg font-mono font-light text-primary leading-relaxed mb-4">
            Every piece on Geometry of Feeling begins as code I write by hand in Python.
          </p>
          <p className="text-body text-secondary mb-12">
            No image generators. No style transfer. No prompts.<br />
            Just equations, structure, color, revision, and feeling.
          </p>

          <div className="border-t border-border mb-16" />

          {/* Intro */}
          <section className="mb-16">
            <p className="text-body text-secondary mb-4">
              There are a lot of ways to make an image now. This is mine.
            </p>
            <p className="text-body text-secondary mb-4">
              Geometry of Feeling is built from mathematical systems that I write,
              test, and revise by hand. Every line in every piece traces back to
              code. The equation is not something I add afterward as a concept or
              caption. It is the cause of the image.
            </p>
            <p className="text-body text-secondary mb-4">
              That difference matters to me.
            </p>
            <p className="text-body text-secondary mb-4">
              I am not asking a model to imitate a style. I am building a
              structure and pushing it until it starts to feel like something
              human: awe, grief, peace, connection, belonging, desire, growth.
            </p>
            <p className="text-body text-secondary">
              The work begins in mathematics, but it is made in pursuit of feeling.
            </p>
          </section>

          {/* What hand-coded means */}
          <section className="mb-16">
            <h2 className="text-headline uppercase tracking-widest text-primary mb-6">
              What Hand-Coded Means Here
            </h2>
            <p className="text-body text-secondary mb-4">
              For me, hand-coded means the image is built from rules I choose and
              shape directly.
            </p>
            <p className="text-body text-secondary mb-4">That can mean:</p>
            <ul className="text-body text-secondary space-y-2 mb-6 ml-4">
              <li>— a field of corona filaments tapering into darkness</li>
              <li>— a set of vortices turning into blocks</li>
              <li>— concentric rings warped until they soften into something organic</li>
              <li>— branching systems repeating until they begin to feel alive</li>
              <li>— oscillators moving from chaos into synchrony</li>
            </ul>
            <p className="text-body text-secondary mb-4">
              The image does not appear because I asked for it in language. It
              appears because I wrote the behavior that produces it.
            </p>
            <p className="text-body text-secondary mb-4">
              Then I revise. I change the density, spacing, rhythm, turbulence,
              color transitions, thresholds, symmetry, asymmetry, softness, scale.
            </p>
            <p className="text-body text-secondary">
              And I keep changing them until the image stops feeling like an output
              and starts feeling like a piece.
            </p>
          </section>

          {/* Why I care */}
          <section className="mb-16">
            <h2 className="text-headline uppercase tracking-widest text-primary mb-6">
              Why I Care About the Difference
            </h2>
            <p className="text-body text-secondary mb-4">
              Because the process shapes the meaning.
            </p>
            <p className="text-body text-secondary mb-4">
              If a piece is about grief, I want the structure of the image to carry
              that grief. I want the mathematics itself to behave like diffusion,
              disappearance, reorganization, absence.
            </p>
            <p className="text-body text-secondary mb-4">
              If a piece is about awe, I want the image to feel governed by
              radiance, orbit, scale, singularity, collapse.
            </p>
            <p className="text-body text-secondary mb-4">
              If a piece is about belonging, I want the form to hold rather than
              simply decorate.
            </p>
            <p className="text-body text-secondary mb-4">
              That is why I work this way. The feeling is not laid on top. It is
              built in.
            </p>
          </section>

          {/* How a piece gets made */}
          <section className="mb-16">
            <h2 className="text-headline uppercase tracking-widest text-primary mb-6">
              How a Piece Gets Made
            </h2>
            <div className="space-y-6">
              <div>
                <p className="text-body text-primary font-medium mb-1">
                  1. A feeling comes first
                </p>
                <p className="text-body text-secondary">
                  Usually the process starts with a feeling that seems too abstract
                  to draw directly: awe, grief, peace, longing, tenderness,
                  humility. I ask what kind of system might behave like that feeling.
                </p>
              </div>
              <div>
                <p className="text-body text-primary font-medium mb-1">
                  2. A rule or equation follows
                </p>
                <p className="text-body text-secondary">
                  That system might be a field, a branching process, a diffusion
                  equation, a recursive subdivision, coupled oscillators, a
                  gravitational or radiative decay, concentric rings warped by
                  noise, a dynamical system like the Lorenz attractor.
                </p>
              </div>
              <div>
                <p className="text-body text-primary font-medium mb-1">
                  3. I build the image from the rule
                </p>
                <p className="text-body text-secondary">
                  From there I write the code by hand in Python and begin generating
                  variations.
                </p>
              </div>
              <div>
                <p className="text-body text-primary font-medium mb-1">
                  4. I revise until the piece feels inevitable
                </p>
                <p className="text-body text-secondary">
                  Most of the work is revision: less noise, more restraint, fewer
                  lines, softer edges, stronger convergence, better color, clearer
                  tension, better silence. A lot of the final image comes from
                  removing things.
                </p>
              </div>
            </div>
          </section>

          <div className="border-t border-border mb-16" />

          {/* Deep Examples */}
          <h2 className="text-headline uppercase tracking-widest text-primary mb-10">
            Four Pieces, Up Close
          </h2>

          {/* Eclipse */}
          <section className="mb-16">
            <h3 className="text-body text-primary font-medium mb-1">
              <Link
                href="/piece/awe-eclipse"
                className="underline underline-offset-4 hover:opacity-70 transition-opacity duration-500"
              >
                Eclipse
              </Link>
              <span className="text-muted font-normal"> — Awe</span>
            </h3>
            <p className="text-body text-secondary mb-4">
              I wanted to render the feeling of seeing an eclipse in code. Not just
              the image of it, but that strange mix of awe, stillness, and pressure
              when the light turns unreal. So Eclipse was built from hand-coded
              corona filaments tapering from gold into darkness. No glow effect. No
              brush. No filter. Just radiance, density, and the hush of an
              impossible ring of light.
            </p>
            <div className="bg-primary text-bg p-6 overflow-x-auto mb-2">
              <pre className="text-caption leading-relaxed">
{`# ECLIPSE — Corona filaments
# I(r) = I_corona / r
# Each filament radiates outward from the rim,
# intensity falling with inverse distance from the corona edge.
# Thousands of lines, each one tapered from bright gold to nothing.`}
              </pre>
            </div>
            <p className="text-caption text-muted italic">
              The inverse-distance field gives each filament its natural taper —
              bright at the rim, fading into the surrounding dark.
            </p>
          </section>

          {/* Gravity */}
          <section className="mb-16">
            <h3 className="text-body text-primary font-medium mb-1">
              <Link
                href="/piece/comprehending-gravity"
                className="underline underline-offset-4 hover:opacity-70 transition-opacity duration-500"
              >
                Gravity
              </Link>
              <span className="text-muted font-normal"> — Comprehending</span>
            </h3>
            <p className="text-body text-secondary mb-4">
              Gravity begins with streamlines moving through vortices. Then the
              densest motion gets subdivided into blocks until turbulence
              crystallizes into structure. The storm is still there. It has just
              been squared. That matters because the piece is part of
              Comprehending — a series about what understanding does to motion,
              complexity, and living things when we force them into clarity.
            </p>
            <div className="bg-primary text-bg p-6 overflow-x-auto mb-2">
              <pre className="text-caption leading-relaxed">
{`# GRAVITY — Paired vortex fields turned to blocks
# dr/dt = -∇Φ, Φ ∝ 1/|r − r₀|
# Streamlines trace through a gravitational potential,
# then recursive block-averaging squares the turbulence
# into comprehensible structure.`}
              </pre>
            </div>
            <p className="text-caption text-muted italic">
              Streamlines become blocks — the same field, seen through the
              simplifying lens of understanding.
            </p>
          </section>

          {/* Nest */}
          <section className="mb-16">
            <h3 className="text-body text-primary font-medium mb-1">
              <Link
                href="/piece/belonging-nest"
                className="underline underline-offset-4 hover:opacity-70 transition-opacity duration-500"
              >
                Nest
              </Link>
              <span className="text-muted font-normal"> — Belonging</span>
            </h3>
            <p className="text-body text-secondary mb-4">
              Nest starts as concentric rings, then softens through layered
              distortion until the geometry feels less mechanical and more held.
              What I care about in a piece like this is not just the form. It is
              the feeling that the center is being kept, not trapped.
            </p>
            <div className="bg-primary text-bg p-6 overflow-x-auto mb-2">
              <pre className="text-caption leading-relaxed">
{`# NEST — Domain-warped concentric rings
# f(r,θ) = e^(−r²/σ²) · [0.6 + 0.4·cos(kr)ⁿ]
# Concentric rings shaped by a Gaussian envelope,
# then warped with layered noise until perfect circles
# become something softer — something that holds.`}
              </pre>
            </div>
            <p className="text-caption text-muted italic">
              The warping is the whole point — perfect geometry becoming shelter.
            </p>
          </section>

          {/* Heat Diffusion */}
          <section className="mb-16">
            <h3 className="text-body text-primary font-medium mb-1">
              <Link
                href="/piece/grief-heat-diffusion"
                className="underline underline-offset-4 hover:opacity-70 transition-opacity duration-500"
              >
                Heat Diffusion
              </Link>
              <span className="text-muted font-normal"> — Grief</span>
            </h3>
            <p className="text-body text-secondary mb-4">
              Heat Diffusion is one equation run again and again. The first curve
              holds all its intensity in one concentrated place. Each step after, it
              flattens and spreads. The math does not know it is about grief. It
              just knows that concentrated things dissipate.
            </p>
            <div className="bg-primary text-bg p-6 overflow-x-auto mb-2">
              <pre className="text-caption leading-relaxed">
{`# HEAT DIFFUSION — One equation, repeated
# ∂u/∂t = α · ∂²u/∂x²
# A single concentrated peak of warmth,
# run through the diffusion equation at increasing time steps.
# Each pass flattens and spreads.
# Eventually the source is gone.`}
              </pre>
            </div>
            <p className="text-caption text-muted italic">
              Warmth that spreads until you can&apos;t tell where it started.
            </p>
          </section>

          <div className="border-t border-border mb-16" />

          {/* What this is not saying */}
          <section className="mb-16">
            <h2 className="text-headline uppercase tracking-widest text-primary mb-6">
              What This Page Is Not Saying
            </h2>
            <p className="text-body text-secondary">
              This is not a claim that one way of making images is morally pure and
              another is not. It is just a statement of what this work is. Geometry
              of Feeling is not AI-generated. It is hand-coded. That matters here
              because the process is inseparable from the meaning. The image is not
              only what you see. It is also the behavior that created it.
            </p>
          </section>

          {/* Why it matters for prints */}
          <section className="mb-16">
            <h2 className="text-headline uppercase tracking-widest text-primary mb-6">
              Why It Matters for the Finished Print
            </h2>
            <p className="text-body text-secondary">
              I think people can feel the difference when a piece has been built
              this way. Not because they can read the code. Not because they need to
              understand the equation. But because the work carries a certain kind
              of internal necessity. The lines are there for a reason. The densities
              are there for a reason. The silence is there for a reason. That is
              what I want the prints to hold: not just beauty, but structure with
              emotional consequence.
            </p>
          </section>

          {/* FAQ */}
          <section className="mb-16">
            <h2 className="text-headline uppercase tracking-widest text-primary mb-6">
              Questions
            </h2>
            <div className="space-y-6">
              {faqItems.map((item) => (
                <div key={item.question}>
                  <p className="text-body text-primary font-medium mb-1">
                    {item.question}
                  </p>
                  <p className="text-body text-secondary">{item.answer}</p>
                </div>
              ))}
            </div>
          </section>

          <div className="border-t border-border mb-16" />

          {/* CTA */}
          <section>
            <p className="text-body text-secondary mb-6">
              I think of these works as minimalist art prints built from exact
              systems in search of human feeling. Not prompts. Not imitation. Not
              randomness mistaken for mystery. Just code, revision, restraint, and
              the long process of turning a structure into something that feels
              true.
            </p>
            <div className="flex flex-wrap gap-4">
              <Link
                href="/shop"
                className="px-6 py-3 border border-primary text-caption uppercase tracking-widest text-primary hover:bg-primary hover:text-bg transition-colors duration-500"
              >
                Browse All Prints
              </Link>
              <Link
                href="/emotions"
                className="px-6 py-3 border border-border text-caption uppercase tracking-widest text-secondary hover:text-primary hover:border-primary transition-colors duration-500"
              >
                Shop by Emotion
              </Link>
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}
