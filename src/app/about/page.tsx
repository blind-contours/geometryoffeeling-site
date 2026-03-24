import ProcessStats from "@/components/ProcessStats";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "About — Geometry of Feeling",
  description:
    "David McCoy, Ph.D. — statistician, researcher, artist. Every piece starts with a human emotion and asks: what mathematical function has the same shape as this feeling?",
};

export default function AboutPage() {
  return (
    <div className="pt-28 pb-16">
      <div className="max-w-content mx-auto px-6">
        <div className="max-w-2xl">
          {/* About the Artist */}
          <section className="mb-20">
            <div className="mb-10">
              {/* Add your photo: save as /public/david-mccoy.jpg (square, ~400x400px)
                  then uncomment the img tag below and remove the placeholder div */}
              <div className="w-28 h-28 bg-surface border border-border mb-6 flex items-center justify-center">
                <span className="text-muted text-caption">Photo</span>
              </div>
              {/* <img src="/david-mccoy.jpg" alt="David McCoy" className="w-28 h-28 object-cover border border-border mb-6" /> */}
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
                people collect records — Lorenz attractors for the chaos of
                overwhelm, coupled oscillators for connection, exponential
                decay for grief, L-system branching for growth, Voronoi
                tessellation for fracture, orbital mechanics for desire,
                murmuration algorithms for awe. Each one a mathematical system
                that genuinely behaves the way an emotion does.
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
              Why Mathematics and Emotion
            </h3>
            <div className="space-y-4">
              <p className="text-body text-secondary">
                Every piece begins with a question: what does this emotion look
                like as an equation?
              </p>
              <p className="text-body text-secondary">
                Grief decays exponentially — intense at first, diminishing over
                time, but never reaching zero. Growth branches fractally — each
                new level of complexity generated by the same recursive rule.
                Connection follows coupled oscillators — two systems influencing
                each other&apos;s rhythm without ever fully merging.
              </p>
              <p className="text-body text-secondary">
                These aren&apos;t metaphors. The mathematical functions genuinely
                behave the way the emotions do. The equation at the bottom of
                each piece isn&apos;t decoration — it&apos;s the reason the image
                looks the way it does.
              </p>
            </div>
          </section>

          <section className="mb-16">
            <h3 className="text-headline uppercase tracking-widest text-primary mb-6">
              How Each Series Is Made
            </h3>
            <div className="space-y-4">
              <p className="text-body text-secondary">
                <span className="text-primary">Research.</span> Before I render
                a single line, I study the emotion across millennia of human
                art, philosophy, and science. What does this feeling do over
                time? Does it decay? Oscillate? Branch? Converge?
              </p>
              <p className="text-body text-secondary">
                <span className="text-primary">Mathematical selection.</span>{" "}
                I choose the function class because its behavior mirrors the
                emotion&apos;s dynamics. Exponential decay for grief. L-system
                branching for growth. Parametric coupling for connection.
              </p>
              <p className="text-body text-secondary">
                <span className="text-primary">Iteration.</span> I render
                hundreds of parameter variations in Python. The palette, the
                density, the negative space — every visual property maps to a
                mathematical parameter.
              </p>
              <p className="text-body text-secondary">
                <span className="text-primary">Curation.</span> Most renders
                get rejected. The ones that survive pass a simple test: does
                this image make me feel the emotion it claims to represent?
              </p>
            </div>
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
            <div className="space-y-4">
              <p className="text-body text-secondary">
                AI image generators — Midjourney, DALL-E, Stable Diffusion —
                take a text prompt and pattern-match against billions of training
                images. They produce visually impressive outputs with no
                underlying mathematical structure, no intentional emotional
                architecture, and no verifiable truth.
              </p>
              <p className="text-body text-secondary">
                I went the opposite direction. I start with the emotion. I
                find the mathematics. I write the code. I render, evaluate,
                and curate. The process takes months. Each series represents
                dozens of hours of research, coding, and aesthetic judgment.
              </p>
              <p className="text-body text-secondary">
                The equation at the bottom of every piece is not a label. It is
                the proof.
              </p>
            </div>

            <div className="border border-border p-6 mt-8">
              <p className="text-body text-secondary italic">
                Built by hand. Rendered in Python. Grounded in mathematics.
                Every piece comes from asking one question: what does this
                emotion look like as an equation?
              </p>
            </div>
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
              Art Historical Context
            </h3>
            <div className="space-y-4">
              <p className="text-body text-secondary">
                This work stands in a tradition of artists who used reduction and
                restraint as a means of intensification:
              </p>
              <p className="text-body text-secondary">
                <span className="text-primary">
                  Hasegawa T&#333;haku&apos;s Pine Trees
                </span>{" "}
                — the negative space is as carefully composed as the brushwork.
                What is not painted matters as much as what is.
              </p>
              <p className="text-body text-secondary">
                <span className="text-primary">
                  Mark Rothko&apos;s color fields
                </span>{" "}
                — emotion rendered through large-scale color relationships, with
                no representational content. The feeling is in the field itself.
              </p>
              <p className="text-body text-secondary">
                <span className="text-primary">Agnes Martin&apos;s grids</span>{" "}
                — mathematical structure used as a vehicle for meditative calm.
                The geometry is the experience.
              </p>
              <p className="text-body text-secondary">
                This work adds one dimension to that tradition: every visual
                decision traces back to a mathematical function. The geometry
                isn&apos;t arbitrary. The equation is the reason the image looks
                the way it does.
              </p>
            </div>
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

          <section className="border-t border-border pt-12">
            <p className="text-lg font-mono font-light text-primary leading-relaxed">
              The equation at the bottom of each piece is real. It&apos;s the
              reason the image looks the way it does. This isn&apos;t a style
              filter applied to a photograph. This is what the function actually
              looks like when I render it.
            </p>
          </section>
        </div>
      </div>
    </div>
  );
}
