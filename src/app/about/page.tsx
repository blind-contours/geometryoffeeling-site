import Image from "next/image";
import ProcessStats from "@/components/ProcessStats";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title:
    "About the Artist — David McCoy, Ph.D. | Geometry of Feeling",
  description:
    "David McCoy, Ph.D. — statistician, researcher, and mathematical artist. Creator of Geometry of Feeling: minimalist fine art prints where every piece begins with a human emotion and renders it through the equation that shares its shape.",
  openGraph: {
    title:
      "About the Artist — David McCoy, Ph.D. | Geometry of Feeling",
    description:
      "David McCoy, Ph.D. — statistician, researcher, and mathematical artist. Creator of Geometry of Feeling: minimalist fine art prints where every piece begins with a human emotion and renders it through the equation that shares its shape.",
    images: [{ url: "/prints/growth/growth_reaction_diffusion.jpg", width: 1680, height: 1155 }],
  },
  twitter: {
    card: "summary_large_image",
    images: ["/prints/growth/growth_reaction_diffusion.jpg"],
  },
};

export default function AboutPage() {
  return (
    <div className="pt-28 pb-16">
      <div className="max-w-content mx-auto px-6">
        <div className="max-w-2xl">
          {/* About the Artist */}
          <section className="mb-20">
            <div className="mb-10">
              <Image
                src="/david-mccoy.jpg"
                alt="David McCoy at work — Singularity render on one screen, Python code on the other"
                width={800}
                height={550}
                className="w-full max-w-lg object-cover border border-border mb-8"
              />
              <h1 className="text-2xl font-mono font-light text-primary mb-1">
                David McCoy, Ph.D.
              </h1>
              <p className="text-caption text-muted">
                Statistician. Researcher. Artist.
              </p>
            </div>

            <div className="space-y-5">
              <p className="text-body text-secondary">
                By day, I work on clinical trials for artificial heart valves —
                devices for people in severe heart failure whose bodies are
                giving out. The patients in my studies are facing the worst
                outcome there is, and the statistics I write help determine
                whether a new valve will give them more time. It&apos;s precise
                work. It matters in the most human way possible.
              </p>
              <p className="text-body text-secondary">
                My training is in causal inference and targeted learning — I
                did my Ph.D. at UC Berkeley under Mark van der Laan, building
                statistical methods for understanding cause and effect in
                complex systems. Before that, I studied philosophy and cognitive
                neuroscience. I&apos;ve always been drawn to how things connect
                — how the structure of a system reveals something about what
                it does, what it means.
              </p>
              <p className="text-body text-secondary">
                The honest truth is I&apos;ve never been naturally gifted at
                math. Compared to my colleagues at Berkeley, I was always the
                one who needed more time, more intuition, more visual thinking.
                But that turned out to be the thing. Where others saw proofs, I
                saw shapes. Where they saw convergence theorems, I felt
                something.
              </p>
              <p className="text-body text-secondary">
                Over ten years ago, I had a simple idea: a circle sitting on
                top of a parabolic curve. Just that. It looked like solitude to
                me — a single form resting in a basin, alone but stable. I
                started sketching more: what does grief look like as a
                function? What shape does connection take? I realized quickly
                that coding these — the way I&apos;d been trained to build
                statistical models — was the right medium. Python, not pencil.
              </p>
              <p className="text-body text-secondary">
                So I started building. I collected equations the way other
                people collect records — coupled oscillators for connection,
                exponential decay for grief, L-system branching for growth,
                Voronoi tessellation for fracture, orbital mechanics for
                desire, murmuration algorithms for awe. Each one a
                mathematical system that genuinely behaves the way an
                emotion does.
              </p>
              <p className="text-body text-secondary">
                This became my craft. Something that made me feel like a kid
                again — at play, using everything I&apos;d learned and trained
                in, but pointed in a completely different direction. A place
                where all the work I&apos;d done on myself — emotionally,
                intellectually — could come together in a way that finally felt
                like me.
              </p>
              <p className="text-body text-secondary">
                These pieces are all a product of that journey. I&apos;m happy
                to share them in a world that feels increasingly confusing and
                flooded with AI-generated noise. This is intentional work that
                tries to cut through — to get back to what is fundamentally
                human: the mathematical language of the universe and the
                experience of being alive in it.
              </p>
            </div>
          </section>

          <div className="border-t border-border mb-20" />

          {/* The Work */}
          <h2 className="text-xl font-mono font-light text-primary mb-12">
            The Work
          </h2>

          <section className="mb-16">
            <h3 className="text-headline uppercase tracking-widest text-primary mb-6">
              How Each Series Is Made
            </h3>
            <p className="text-body text-secondary">
              It always starts with the emotion. I sit with it, study it — what
              does this feeling actually do over time? Then I go looking for the
              math that behaves the same way. Once I find it, I write Python code
              and render thousands of parameter variations: different palettes,
              densities, compositions. Most of them get rejected. The ones that
              survive pass one test — they make me feel the thing they claim to
              represent.
            </p>
          </section>

          {/* The actual code */}
          <section className="mb-16">
            <h3 className="text-headline uppercase tracking-widest text-primary mb-6">
              The Code
            </h3>
            <div className="bg-primary text-bg p-6 overflow-x-auto mb-4">
              <pre className="text-caption leading-relaxed">
{`# GRIEF — Settling
# f(t) = e^(-λt) · cos(ωt)
t = np.linspace(0, 1, 2000)
lam = 3.5   # decay rate — how fast grief fades
omega = 22  # frequency — how often it returns
ys = baseline + PH*0.44 * np.exp(-lam*t) * np.cos(omega*np.pi*t)`}
              </pre>
            </div>
            <p className="text-body text-secondary italic">
              The decay rate (λ) controls how fast the waves shrink. The
              frequency (ω) controls how often grief returns. I chose the
              parameters because they felt true.
            </p>
          </section>

          <section className="mb-16">
            <h3 className="text-headline uppercase tracking-widest text-primary mb-6">
              No AI Generated Images
            </h3>
            <p className="text-body text-secondary">
              Every line in every piece traces back to an equation I wrote by
              hand in Python. No image generators, no style transfer, no
              prompts. The equation at the bottom of each piece isn&apos;t a
              label — it&apos;s the reason the image looks the way it does.
            </p>
          </section>

          {/* Process stats */}
          <section className="mb-16">
            <h3 className="text-headline uppercase tracking-widest text-primary mb-8">
              By the Numbers
            </h3>
            <ProcessStats />
          </section>

          <section className="mb-16">
            <h3 className="text-headline uppercase tracking-widest text-primary mb-6">
              The Standard
            </h3>
            <p className="text-lg font-mono font-light text-primary leading-relaxed">
              The final question I ask of every piece: if this were hanging
              in a gallery with no label, would someone stop and feel something?
            </p>
          </section>
        </div>
      </div>
    </div>
  );
}
