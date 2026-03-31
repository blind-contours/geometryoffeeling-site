export interface Piece {
  id: string;
  title: string;
  series: string;
  equation: string;
  description: string;
  emotionalNote: string;
  background: string;
  imageUrl: string;
  gumroadUrl: string;
  price: number;
}

export interface Series {
  id: string;
  name: string;
  emotion: string;
  tagline: string;
  description: string;
  story: string;
  mathematicalPrimitive: string;
  background: string;
  palette: string[];
  pieces: Piece[];
  bundleGumroadUrl: string;
  bundlePrice: number;
  makingOf: string;
}

export const series: Series[] = [
  // ── FRACTURED ───────────────────────────────────────────
  {
    id: "fractured",
    name: "FRACTURED",
    emotion: "fracture, discontinuity, the moment things break",
    tagline: "Piecewise functions where the limit from the left never meets the limit from the right. The discontinuity is the emotion.",
    description: "Piecewise discontinuous functions rendered as visual fields. Each piece explores a different topology of breaking — bifurcation cascades, catastrophe folds, Voronoi shattering, seismic faults, glass fracture networks. The mathematics of rupture made visible.",
    story: "Fracture is not random. When a material breaks, it follows the physics of stress propagation. When a life breaks, it follows the topology of connection — the pieces that were closest fracture first. This series uses discontinuous functions, bifurcation diagrams, and Voronoi tessellation to map the geometry of things coming apart.",
    mathematicalPrimitive: "piecewise discontinuous functions, bifurcation, Voronoi tessellation",
    background: "#F5F0E0",
    palette: ["#3A5BA0", "#D4573B", "#E8A838", "#6B4E8B", "#2D8B6E"],
    makingOf: "47 renders. 5 survived.",
    pieces: [
      { id: "fractured-bifurcation", title: "Bifurcation", series: "fractured", equation: "x_{n+1} = rx_n(1 - x_n)", description: "I ran the logistic map over and over, watching one path split into two, then four, then dissolve into noise. There's a parameter value where everything holds — and one tick later, it doesn't.", emotionalNote: "That moment when one path becomes two and there's no going back", background: "#F5F0E0", imageUrl: "/prints/fractured/fractured_bifurcation.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "fractured-erosion", title: "Erosion", series: "fractured", equation: "∂z/∂t = D·∇²z", description: "Twenty-eight cliff profiles from the diffusion equation — a sharp face softening into gentle S-curves as water works the stone. Each line is the same cliff at a different moment in geological time.", emotionalNote: "The patience of water against stone", background: "#F5F0E0", imageUrl: "/prints/fractured/fractured_erosion.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "fractured-glass-fracture", title: "Glass Fracture", series: "fractured", equation: "K_I = σ√(πa)", description: "I modeled crack propagation using the Griffith criterion — each line follows the stress field through the material. The cracks aren't random. They go exactly where the structure was already weakest.", emotionalNote: "Every crack follows where the structure was already weakest", background: "#F5F0E0", imageUrl: "/prints/fractured/fractured_glass_fracture.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "fractured-seismic-fault", title: "Seismic Fault", series: "fractured", equation: "log₁₀(N) = a - bM", description: "Based on the Gutenberg-Richter law. Tension builds in silence along a fault line, then releases everything at once. The quiet before is part of the breaking.", emotionalNote: "The silence before the break is part of the break", background: "#F5F0E0", imageUrl: "/prints/fractured/fractured_seismic_fault.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "fractured-voronoi-shatter", title: "Voronoi Shatter", series: "fractured", equation: "V(p) = {x : d(x,p) ≤ d(x,q) ∀q}", description: "I scattered seed points and let the Voronoi algorithm divide the space — each cell claims whatever is closest to its center. It looks like shattered glass because that's literally the geometry of how glass breaks.", emotionalNote: "Space divided by proximity — the geometry of things coming apart", background: "#F5F0E0", imageUrl: "/prints/fractured/fractured_voronoi_shatter.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-fractured-bundle",
    bundlePrice: 169,
  },

  // ── CONNECTION ──────────────────────────────────────────
  {
    id: "connection",
    name: "CONNECTION",
    emotion: "attraction, companionship, the space between two people",
    tagline: "Two forms moving through the same space. Neither leads nor follows. The gap between them is the relationship.",
    description: "Five pieces exploring different forms of human connection — the pull of attraction, the steadiness of companionship, the dance of reciprocity, the permanence of devotion, and the slow miracle of finding harmony together.",
    story: "Connection is not union. It is two separate trajectories that choose proximity. These equations describe that precisely: two systems that influence each other without ever fully merging. The space between them is where the relationship lives.",
    mathematicalPrimitive: "magnetic fields, orbital mechanics, Lissajous curves, torus knots, Kuramoto synchronization",
    background: "#0A0A12",
    palette: ["#C8887A", "#E8C878", "#D4988A", "#B87A70", "#F0D890"],
    makingOf: "77 renders. 5 survived.",
    pieces: [
      { id: "connection-magnetic", title: "Magnetic", series: "connection", equation: "B = B₁ + B₂, ∇×B = μ₀J", description: "Two fields reaching toward each other across dark space. The pull between them is invisible, but it shapes everything — bending every line, curving every path. You can't see the force. You can feel it.", emotionalNote: "The invisible pull that shapes everything around it", background: "#E8D8B8", imageUrl: "/prints/connection/connection_magnetic.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "connection-orbit-pair", title: "Orbit Pair", series: "connection", equation: "r(θ) = a(1−e²)/(1+e·cosθ)", description: "Two orbits circling the same invisible center. They never touch, never drift apart. Something neither one can see holds them together — and has, quietly, for as long as they've been moving.", emotionalNote: "Held together by the same invisible center", background: "#E8D8B8", imageUrl: "/prints/connection/connection_orbit_pair.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "connection-lissajous", title: "Lissajous", series: "connection", equation: "x = sin(3t), y = sin(2t + φ)", description: "Two frequencies tracing a single curve — the same motion, half a beat apart. It looks like a dance because it is one. Two rhythms close enough to share a path, different enough to make it beautiful.", emotionalNote: "The same motion, half a beat apart", background: "#E8D8B8", imageUrl: "/prints/connection/connection_lissajous.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "connection-torus-knot", title: "Torus Knot", series: "connection", equation: "x = (R+r·cos(qt))cos(pt)", description: "A single continuous curve that loops around itself, forming a knot that can never be untied without cutting. Once it's tied, that's it. Some connections are like that — permanent not because they're rigid, but because they're woven too deeply to undo.", emotionalNote: "Woven too deeply to come apart", background: "#E8D8B8", imageUrl: "/prints/connection/connection_torus_knot.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "connection-phase-sync", title: "Phase Sync", series: "connection", equation: "dθ/dt = ω + (K/N)Σsin(θⱼ−θᵢ)", description: "Dozens of independent rhythms, each on its own frequency, gradually finding each other. No conductor, no signal — just proximity and time. The coherence that emerges wasn't planned. It was earned.", emotionalNote: "Scattered rhythms finding the same beat", background: "#E8D8B8", imageUrl: "/prints/connection/connection_phase_sync.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-connection-bundle",
    bundlePrice: 169,
  },

  // ── TENSION ─────────────────────────────────────────────
  {
    id: "tension",
    name: "TENSION",
    emotion: "strain, opposition, systems that cannot rest",
    tagline: "Lorentzian resonance and beating frequencies. Systems that cannot rest and will not resolve.",
    description: "Interference patterns, opposing forces, torsional stress, and buckling columns. Systems held between competing demands — too much energy to rest, too constrained to move.",
    story: "Tension is not conflict. Conflict resolves. Tension is the state between resolution and collapse — the beam that holds because opposing forces balance perfectly. Inspired by the psychological intensity of Munch's color field.",
    mathematicalPrimitive: "interference, torsion, buckling, opposing forces",
    background: "#1A1A1A",
    palette: ["#E8D42A", "#D4282A", "#F0E648", "#CC1A1C", "#FFF060"],
    makingOf: "38 renders. 5 survived.",
    pieces: [
      { id: "tension-buckling", title: "Buckling", series: "tension", equation: "P_cr = π²EI / (KL)²", description: "I computed Euler's critical load — the exact force where a column buckles. One newton below, perfectly stable. At that threshold, catastrophic failure. There's no warning.", emotionalNote: "The line between holding and collapse is exact", background: "#1A1A1A", imageUrl: "/prints/tension/tension_buckling.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "tension-fracture", title: "Fracture", series: "tension", equation: "σ = Eε (until σ > σ_y)", description: "Hooke's law pushed past the yield point. The relationship between stress and strain is perfectly linear — until it isn't. I wanted to show that invisible threshold.", emotionalNote: "The invisible line between bending and breaking", background: "#1A1A1A", imageUrl: "/prints/tension/tension_fracture.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "tension-interference", title: "Interference", series: "tension", equation: "A(x) = A₁sin(k₁x) + A₂sin(k₂x)", description: "Two wave sources creating an interference pattern. Where they align, the signal doubles. Where they oppose, total silence. No in-between.", emotionalNote: "Where two forces meet, they double or they cancel", background: "#1A1A1A", imageUrl: "/prints/tension/tension_interference.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "tension-opposition", title: "Opposition", series: "tension", equation: "F_net = F₁ - F₂ = 0, |F₁| > 0", description: "Equal and opposite forces in perfect balance. The net force is zero, but the internal stress is immense. Nothing moves. Everything strains.", emotionalNote: "Perfect balance isn't peace — it's maximum contained force", background: "#1A1A1A", imageUrl: "/prints/tension/tension_opposition.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "tension-torsion", title: "Torsion", series: "tension", equation: "τ = Tr/J", description: "Shear stress in a twisted shaft — maximum at the surface, zero at the center. The outside carries all the strain while the core feels nothing.", emotionalNote: "The outside holds all the strain while the center feels nothing", background: "#1A1A1A", imageUrl: "/prints/tension/tension_torsion.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-tension-bundle",
    bundlePrice: 169,
  },

  // ── GRIEF ───────────────────────────────────────────────
  {
    id: "grief",
    name: "GRIEF",
    emotion: "decay, absence, the quiet after loss",
    tagline: "Exponential decay toward zero. Half-life curves draining from two directions. The plateau that holds until the edges yield.",
    description: "Heat diffusion, step-function cascades, spectral erosion, voids, and weight fields. The mathematics of things disappearing — not suddenly, but according to precise laws of decay. The quietest series.",
    story: "Grief obeys the mathematics of decay. The half-life equation — f(t) = e^(-λt) — describes how radioactive isotopes lose their energy, but it also describes how the intensity of grief diminishes over time. It never reaches zero. The asymptote is forever.",
    mathematicalPrimitive: "exponential decay, heat diffusion, step functions, erosion",
    background: "#DDD9D2",
    palette: ["#7A8B9A", "#9A8A9A", "#C8D4E0", "#A0A8B0", "#D0C8D0"],
    makingOf: "83 renders. 5 survived.",
    pieces: [
      { id: "grief-void", title: "Void", series: "grief", equation: "|x/a|^p + |y/b|^q = 1", description: "Lines flow around an empty center — crowding toward the absence but never entering it. I shaped it as a superellipse with sharp points at top and bottom. Everything bends toward what's gone.", emotionalNote: "Everything bends toward what's no longer there", background: "#DDD9D2", imageUrl: "/prints/grief/grief_void.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "grief-weight", title: "Weight", series: "grief", equation: "y(x) = a·cosh((x−c)/a)", description: "Catenary curves sagging under increasing load — cables hanging from two fixed points, each one heavier than the last. I kept adding weight until the whole frame drooped.", emotionalNote: "The weight that bends everything down", background: "#DDD9D2", imageUrl: "/prints/grief/grief_weight.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "grief-heaviside-cascade", title: "Heaviside Cascade", series: "grief", equation: "H(t−tₙ) = {0, t<tₙ; 1, t≥tₙ}", description: "Stacked Heaviside step functions — each drop sudden and irreversible. The staircase only goes down. I couldn't make it go any other direction.", emotionalNote: "Each step down is permanent", background: "#DDD9D2", imageUrl: "/prints/grief/grief_heaviside_cascade.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "grief-absence", title: "Absence", series: "grief", equation: "f(x) = Σ aₙ·e^(−λₙt)·cos(nπx)", description: "Fourier modes decaying at different rates. The high frequencies go first, then the mid-range, then the bass. Presence dissolving harmonic by harmonic until only silence is left.", emotionalNote: "What remains when the last frequency fades", background: "#DDD9D2", imageUrl: "/prints/grief/grief_absence.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "grief-heat-diffusion", title: "Heat Diffusion", series: "grief", equation: "∂u/∂t = α·∂²u/∂x²", description: "I placed multiple heat sources and let them diffuse over time. Sharp spires of warmth that spread and flatten until you can't tell they were ever there.", emotionalNote: "Warmth that spreads until you can't tell it was ever there", background: "#DDD9D2", imageUrl: "/prints/grief/grief_heat_diffusion.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-grief-bundle",
    bundlePrice: 169,
  },

  // ── GROWTH ──────────────────────────────────────────────
  {
    id: "growth",
    name: "GROWTH",
    emotion: "emergence, branching, reaching toward light",
    tagline: "L-system branching at thirteen levels. Space colonization networks. Thirty-four lines reaching toward light.",
    description: "Fractal trees, mycelial networks, sigmoid thaw transitions, and bifurcation cascades. Growth is not linear — it is recursive, branching, alive.",
    story: "Growth follows rules. The branching of trees obeys L-system grammars. Mycelial networks colonize space through attractor fields. A dormant tree thaws from the roots up via sigmoid activation. This series renders these growth algorithms as minimalist art — each piece generated by the mathematics it depicts.",
    mathematicalPrimitive: "L-systems, space colonization, sigmoid activation, logistic maps",
    background: "#F5F0E6",
    palette: ["#1A4D2E", "#2E8B4A", "#6BBF6E", "#A8D86E", "#E8D878"],
    makingOf: "140 renders. 6 survived.",
    pieces: [
      { id: "growth-branch", title: "Branch", series: "growth", equation: "A→F[−θA][+θA], 13 levels, θ=35°, r=0.82", description: "A single L-system rule — branch left, branch right — applied thirteen times. The same three-character grammar at every scale produces a fractal canopy that looks alive.", emotionalNote: "Three characters of code, infinite complexity", background: "#F5F0E6", imageUrl: "/prints/growth/growth_branch.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "growth-thaw", title: "Thaw", series: "growth", equation: "G(t) = G₀·σ(r(t−t₀))", description: "A tree waking up. The lower branches stay dormant — bare brown wood. As you move up, a sigmoid activation function triggers the thaw. Buds open, green floods in. The most emotionally clear piece in the series.", emotionalNote: "Dormancy giving way to life, branch by branch", background: "#F5F0E6", imageUrl: "/prints/growth/growth_thaw.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "growth-arise", title: "Arise", series: "growth", equation: "x(t) = x₀ − d·α·t, y(t) = y₀ + H·t", description: "Thirty-four lines rising from a spread baseline, gently converging toward center as they grow. Phototropism reduced to linear interpolation. Simple, but it captures something about reaching.", emotionalNote: "Reaching upward, converging toward light", background: "#F5F0E6", imageUrl: "/prints/growth/growth_arise.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "growth-mycelium", title: "Mycelium", series: "growth", equation: "6×SC(attract, kill, step)", description: "Six spore germination sites each grow a branching network through a shared attractor field using the Runions space colonization algorithm. The pipe model gives thick trunks tapering to gossamer tips. An unseen architecture.", emotionalNote: "The hidden network that connects everything underground", background: "#F5F0E6", imageUrl: "/prints/growth/growth_mycelium.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "growth-meadow", title: "Meadow", series: "growth", equation: "y_n(t) = h_n·t, h_n ∼ Beta(3, 1.5)", description: "Fifty-five stems at variable heights — a field in growth. Heights drawn from a Beta distribution: most stems tall, a few still rising. The randomness of a real meadow, captured in one equation.", emotionalNote: "A field where everything grows at its own pace", background: "#F5F0E6", imageUrl: "/prints/growth/growth_meadow.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "growth-bifurcation", title: "Bifurcation", series: "growth", equation: "x_{n+1} = rx_n(1 - x_n), r ∈ [2.5, 4]", description: "The logistic map's bifurcation diagram, but I read it as a growth story — a single strategy that splits and splits again until it's irreducibly complex.", emotionalNote: "Simple beginnings branching until they can't be simplified", background: "#F5F0E6", imageUrl: "/prints/growth/growth_bifurcation.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-growth-bundle",
    bundlePrice: 169,
  },

  // ── CYCLES ──────────────────────────────────────────────
  {
    id: "cycles",
    name: "CYCLES",
    emotion: "return, repetition, the pattern that comes back",
    tagline: "Phase portraits closing on themselves. Möbius strips with no beginning. Orbits that always return to where they started.",
    description: "Closed orbits, phase portraits, Möbius topology, and recurrence plots. Mathematics that loops — systems that always return, never quite the same way twice.",
    story: "The universe is built on cycles. Seasons, tides, heartbeats, orbits — patterns that return without being asked. This series renders the geometry of return: phase portraits that close, orbits that repeat, and Möbius strips that have no beginning or end.",
    mathematicalPrimitive: "closed orbits, phase portraits, Möbius topology, recurrence",
    background: "#F0E8DA",
    palette: ["#5A9A50", "#C8A030", "#B85A30", "#4A6A90"],
    makingOf: "60 renders. 11 survived.",
    pieces: [
      { id: "cycles-seasons", title: "Seasons", series: "cycles", equation: "T(t) = T̄ + A·sin(2πt/P + φ)", description: "I stacked sinusoidal temperature curves — each layer a different year. Same rhythm, never quite the same amplitude. The year breathing in and out.", emotionalNote: "The same rhythm, never the same amplitude", background: "#F0E8DA", imageUrl: "/prints/cycles/cycles_seasons.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },

      { id: "cycles-loom", title: "Loom", series: "cycles", equation: "x(t) = x(t + T), T = 2π/ω", description: "I wove warp and weft from periodic functions — threads that return at exact intervals, creating fabric from nothing but rhythm.", emotionalNote: "Rhythm weaving itself into something solid", background: "#F0E8DA", imageUrl: "/prints/cycles/cycles_loom.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "cycles-moebius", title: "Möbius", series: "cycles", equation: "R·eⁱᵗ + r·cos(t/2)·eⁱᵗ", description: "The Möbius strip — a surface with only one side. You have to go around it twice to get back to where you started. That always got to me.", emotionalNote: "A loop that takes two passes to complete", background: "#F0E8DA", imageUrl: "/prints/cycles/cycles_moebius.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "cycles-phase-portrait", title: "Phase Portrait", series: "cycles", equation: "x'' − μ(1−x²)x' + x = 0", description: "The Van der Pol oscillator — every trajectory spirals toward the same limit cycle. Doesn't matter where you start. You end up in the same loop.", emotionalNote: "Every starting point leads to the same loop", background: "#F0E8DA", imageUrl: "/prints/cycles/cycles_phase_portrait.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "cycles-breathing", title: "Breathing", series: "cycles", equation: "r(t) = r₀ + A·sin(ωt + φ)", description: "Concentric circles expanding and contracting. The simplest cycle there is — lungs filling and emptying. I kept it minimal on purpose.", emotionalNote: "Expand, contract, repeat", background: "#F0E8DA", imageUrl: "/prints/cycles/cycles_breathing.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "cycles-pulse-train", title: "Pulse Train", series: "cycles", equation: "f(t) = Σ e^(−(t−nT)²/2σ²)", description: "Gaussian pulses at regular intervals — a heartbeat in math. Each pulse identical. The space between them is where the rhythm lives.", emotionalNote: "The space between beats is where rhythm lives", background: "#F0E8DA", imageUrl: "/prints/cycles/cycles_pulse_train.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "cycles-tidal", title: "Tidal", series: "cycles", equation: "h(t) = Σ Aₙcos(ωₙt + φₙ)", description: "Tidal harmonics — lunar and solar gravity superimposed, creating the rise and fall of water. The ocean responding to something it can't see.", emotionalNote: "The ocean responding to something it can't see", background: "#F0E8DA", imageUrl: "/prints/cycles/cycles_tidal.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-cycles-bundle",
    bundlePrice: 169,
  },

  // ── SHAME ───────────────────────────────────────────────
  {
    id: "shame",
    name: "SHAME",
    emotion: "contraction, withdrawal, making oneself small",
    tagline: "Surfaces folding inward. Contracting manifolds. The geometry of making yourself disappear.",
    description: "Contracting functions, crumpling surfaces, folding manifolds, shrinking envelopes, and veiled forms. The mathematics of systems that collapse toward their own center.",
    story: "Shame is a contraction. The body language is universal — shoulders curve inward, the head drops, the self tries to occupy less space. This series renders that inward collapse mathematically: surfaces that fold, envelopes that shrink, forms that hide behind their own geometry.",
    mathematicalPrimitive: "contraction mappings, surface folding, envelope collapse",
    background: "#E0DCE4",
    palette: ["#8A7090", "#706080", "#9080A0", "#604870", "#A090B0"],
    makingOf: "44 renders. 5 survived.",
    pieces: [
      { id: "shame-contraction", title: "Contraction", series: "shame", equation: "T(x) : ||T(x)-T(y)|| < ||x-y||", description: "A contraction mapping — every iteration pulls all points closer together. The fixed point is inevitable. I kept iterating and everything collapsed to the same spot.", emotionalNote: "Collapsing inward toward a point you can't avoid", background: "#E0DCE4", imageUrl: "/prints/shame/shame_contraction.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "shame-crumple", title: "Crumple", series: "shame", equation: "κ(s) → ∞ at fold lines", description: "A smooth surface developing infinite curvature at fold lines. The geometry of crumpling — once folded, the creases never fully come out.", emotionalNote: "Once folded, the creases never fully come out", background: "#E0DCE4", imageUrl: "/prints/shame/shame_crumple.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "shame-fold", title: "Fold", series: "shame", equation: "f(x) = f(−x), x → 0", description: "A function folding onto itself — two halves meeting and collapsing the space between them. Everything that was on the outside gets tucked away.", emotionalNote: "Folding inward until the outside disappears", background: "#E0DCE4", imageUrl: "/prints/shame/shame_fold.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "shame-shrink", title: "Shrink", series: "shame", equation: "A(t) = A₀ · e^{-λt}", description: "An exponentially decaying envelope — the amplitude shrinking until the signal becomes invisible. Still there, technically. But no one can see it.", emotionalNote: "Getting smaller until no one can see you", background: "#E0DCE4", imageUrl: "/prints/shame/shame_shrink.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-shame-bundle",
    bundlePrice: 169,
  },

  // ── SOLITUDE ────────────────────────────────────────────
  {
    id: "solitude",
    name: "SOLITUDE",
    emotion: "aloneness, vast space, a single presence",
    tagline: "One point in an infinite plane. One signal in silence. The mathematics of being the only thing present.",
    description: "Isolated points, single signals in vast fields, lighthouse beacons, island topologies, and echo functions. The mathematics of being alone — not lonely, but singular.",
    story: "Solitude is not loneliness. It is the experience of being the only signal in a vast field. The mathematics of isolation is sparse: a single point, a single frequency, a single source of light. This series uses extreme negative space to render that singularity.",
    mathematicalPrimitive: "isolated points, sparse signals, single-source propagation",
    background: "#E0DDD6",
    palette: ["#404850", "#2A4A3A", "#C8963A", "#5A6878", "#D4A840"],
    makingOf: "62 renders. 5 survived.",
    pieces: [
      { id: "solitude-basin", title: "Basin", series: "solitude", equation: "y = a(x−h)² + k", description: "A parabolic potential well with circles settled at the minimum. One has climbed to the rim, alone at the tip of the rising curve. I kept thinking about what made it leave.", emotionalNote: "The one who climbed out of the comfortable minimum", background: "#E0DDD6", imageUrl: "/prints/solitude/solitude_basin.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "solitude-signal", title: "Signal", series: "solitude", equation: "S(f) = A·δ(f−f₀) + η", description: "A dense field of overlapping frequencies — noise from every direction. One gold signal rises above it all. I made it unmistakable against the static.", emotionalNote: "One clear voice in a room full of noise", background: "#E0DDD6", imageUrl: "/prints/solitude/solitude_signal.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "solitude-skyline", title: "Skyline", series: "solitude", equation: "y_i = β(2,3)·H + ε", description: "Dense band of horizontal lines near the bottom, one gold line floating high above. Separated from everything below by pure empty space.", emotionalNote: "Separated from everything below by pure empty space", background: "#E0DDD6", imageUrl: "/prints/solitude/solitude_skyline.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "solitude-shadow", title: "Shadow", series: "solitude", equation: "I(x) = I₀·e^(−μx)", description: "A single gold vertical form casting a long diagonal shadow across the canvas. One presence and the proof that it exists.", emotionalNote: "One presence and the proof that it exists", background: "#E0DDD6", imageUrl: "/prints/solitude/solitude_shadow.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "solitude-drift", title: "Drift", series: "solitude", equation: "η(x) = A₁sin(k₁x + φ₁) + A₂cos(k₂x + φ₂)", description: "Twenty-eight wave equations flowing horizontally at different heights. One gold line cuts diagonally from bottom-left to top-right, riding the crests — surfing from one wave peak to the next.", emotionalNote: "Riding the crests, surfing from one wave to the next", background: "#E0DDD6", imageUrl: "/prints/solitude/solitude_drift.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-solitude-bundle",
    bundlePrice: 169,
  },

  // ── NOSTALGIA ───────────────────────────────────────────
  {
    id: "nostalgia",
    name: "NOSTALGIA",
    emotion: "remembering, fading, the warmth of what was",
    tagline: "Low-pass filtered memories. Daguerreotype decay. Music box harmonics winding down.",
    description: "Low-pass filters, photographic decay, music box harmonics, carousel functions, and remnant signals. The mathematics of memory — blurred, warm, and slowly losing resolution.",
    story: "Nostalgia is memory with its high frequencies removed. The details blur but the warmth remains. A low-pass filter does exactly this — it removes sharp edges and rapid changes, leaving only the slow, smooth underlying signal. This series renders that filtering as visual art.",
    mathematicalPrimitive: "low-pass filtering, harmonic decay, photographic degradation",
    background: "#F0E8D8",
    palette: ["#C8A060", "#A08040", "#E0C880", "#887030", "#D8B870"],
    makingOf: "42 renders. 4 survived.",
    pieces: [
      { id: "nostalgia-reaching", title: "Reaching", series: "nostalgia", equation: "y(t) → ∞, ∂y/∂t → 0", description: "A bold stem rising from an amber origin, thinning as it climbs. Tendrils arc off and sweep back toward where it started. I couldn't make it stop reaching back.", emotionalNote: "Moving forward but always reaching backward", background: "#F0E8D8", imageUrl: "/prints/nostalgia/nostalgia_reaching.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "nostalgia-heirloom", title: "Heirloom", series: "nostalgia", equation: "Sₙ = (1+εₙ)·λ·Sₙ₋₁", description: "The same shape passed down through iterations — each copy slightly larger, slightly less precise. The innermost form is still sharp. The outermost is barely a suggestion of what it was.", emotionalNote: "Each copy a little less precise than the last", background: "#F0E8D8", imageUrl: "/prints/nostalgia/nostalgia_heirloom.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "nostalgia-saudade", title: "Saudade", series: "nostalgia", equation: "r(θ) = r₀ + εθ + a·sin(3θ)", description: "Spirals that keep trying to close but drift outward — each orbit almost returns to where it started but never quite gets there. Named for the Portuguese word for longing without an object.", emotionalNote: "Almost closing, always drifting", background: "#F0E8D8", imageUrl: "/prints/nostalgia/nostalgia_saudade.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "nostalgia-sepia", title: "Sepia", series: "nostalgia", equation: "Σ αₖ·G(x,y;μₖ,σₖ)", description: "Overlapping Gaussian washes in amber, ochre, and sienna bleeding into each other. I was going for the soft focus of a memory you've recalled so many times the edges are gone.", emotionalNote: "A memory recalled so many times the edges are gone", background: "#F0E8D8", imageUrl: "/prints/nostalgia/nostalgia_sepia.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-nostalgia-bundle",
    bundlePrice: 169,
  },

  // ── DESIRE ──────────────────────────────────────────────
  {
    id: "desire",
    name: "DESIRE",
    emotion: "wanting, pull, gravitational attraction",
    tagline: "Gravitational inspiral. Pursuit curves that never close. The asymptote you cannot reach but cannot stop approaching.",
    description: "Gravitational inspiral, pursuit curves, orbital mechanics, flame dynamics, and eclipse geometry. Systems pulled toward something they cannot reach.",
    story: "Desire is a force field. It has direction, magnitude, and a source. The mathematics of attraction — gravitational wells, pursuit curves, orbital decay — describe systems that are pulled toward something with increasing urgency. This series renders that pull.",
    mathematicalPrimitive: "gravitational attraction, pursuit curves, orbital decay",
    background: "#2A2018",
    palette: ["#9A2030", "#C88030", "#D06020", "#B83040", "#C4A040"],
    makingOf: "20 renders. 5 survived.",
    pieces: [
      { id: "desire-pursuit", title: "Pursuit", series: "desire", equation: "dx/dt=αx−βxy, dy/dt=δxy−γy", description: "Lotka-Volterra predator-prey in phase space — layered orbits circling a fixed point. They never close and they never escape. Just endless approach.", emotionalNote: "Endless approach, never arrival", background: "#2A2018", imageUrl: "/prints/desire/desire_pursuit.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "desire-magnetism", title: "Magnetism", series: "desire", equation: "B=μ₀/(4π)·(3(m·r̂)r̂−m)/r³", description: "Magnetic field lines arcing between two poles. I drew the invisible force that shapes the space between two bodies — the pull you can feel but can't see.", emotionalNote: "The pull you can feel but can't see", background: "#2A2018", imageUrl: "/prints/desire/desire_magnetism.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "desire-pulse", title: "Pulse", series: "desire", equation: "f(t)=A·exp(−(t mod T)/σ)", description: "Rows of peaked waveforms accelerating — spacing tightening, amplitude rising. A heartbeat that won't slow down no matter what you do.", emotionalNote: "A heartbeat that won't slow down", background: "#2A2018", imageUrl: "/prints/desire/desire_pulse.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "desire-threshold", title: "Threshold", series: "desire", equation: "y=L/(1+e^(−k(t−t₀)))", description: "Logistic curves sweeping upward toward a limit they can never cross. I stacked them and each one asymptotes just below where it wants to be.", emotionalNote: "Rising toward a line that can never be crossed", background: "#2A2018", imageUrl: "/prints/desire/desire_threshold.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "desire-inspiral", title: "Inspiral", series: "desire", equation: "r(θ)=r₀·e^(−γθ)", description: "Concentric spirals tightening toward a glowing center. Gravitational decay pulling two bodies inward, accelerating as they go. I couldn't stop the convergence.", emotionalNote: "Accelerating toward something you can't stop", background: "#2A2018", imageUrl: "/prints/desire/desire_inspiral.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-desire-bundle",
    bundlePrice: 169,
  },

  // ── SURRENDER ───────────────────────────────────────────
  {
    id: "surrender",
    name: "SURRENDER",
    emotion: "letting go, release, allowing the fall",
    tagline: "Terminal velocity. Dissolution into equilibrium. The mathematics of ceasing to resist.",
    description: "Dissolution reactions, laminar flow, melting surfaces, settling particles, and shedding forms. Systems that stop fighting and allow the physics to take over.",
    story: "Surrender is not defeat. It is the moment a system stops expending energy to resist and allows the natural process to complete. A particle settling in fluid, a solid melting, a leaf releasing from its branch. These are not failures — they are completions.",
    mathematicalPrimitive: "dissolution, settling, laminar flow, phase transition",
    background: "#E4E0DC",
    palette: ["#5A5048", "#7A7068", "#9A9088", "#B0A898", "#C8C0B4"],
    makingOf: "59 renders. 5 survived.",
    pieces: [
      { id: "surrender-settle", title: "Settle", series: "surrender", equation: "y(t) = y_eq + (y₀ − y_eq)·e^(−t/τ)·cos(ω_d·t)", description: "Twenty-four underdamped oscillations settling to equilibrium. I arranged them symmetrically around a rest point and let them release their energy. They all find the same quiet.", emotionalNote: "Everything finding the same quiet", background: "#E8E4DE", imageUrl: "/prints/surrender/surrender_settle.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "surrender-melt", title: "Melt", series: "surrender", equation: "r(θ,s) = (1−s)·r_sq(θ) + s·r_circ", description: "A square morphing into a circle through twenty-two stages. I watched rigid geometry let go of its edges. It didn't break — it just stopped holding on.", emotionalNote: "Letting go of edges without breaking", background: "#E8E4DE", imageUrl: "/prints/surrender/surrender_melt.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "surrender-terminal", title: "Terminal", series: "surrender", equation: "v(t) = v_t·tanh(gt/v_t)", description: "Free-fall curves each approaching terminal velocity — the moment air resistance equals gravity and acceleration stops. You're still falling, but you've stopped fighting.", emotionalNote: "Still falling, but no longer accelerating", background: "#E8E4DE", imageUrl: "/prints/surrender/surrender_terminal.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "surrender-flow", title: "Flow", series: "surrender", equation: "dY = μ(Y_flow − Y)·dt + σ(1−t)·dW", description: "Thirty separate currents converging into a single stream. Each path gives up its own direction to join the whole. I didn't force them — the flow did.", emotionalNote: "Separate paths joining one current", background: "#E8E4DE", imageUrl: "/prints/surrender/surrender_flow.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-surrender-bundle",
    bundlePrice: 169,
  },

  // ── WONDER ──────────────────────────────────────────────
  {
    id: "wonder",
    name: "WONDER",
    emotion: "awe at structure, the surprise of hidden order",
    tagline: "Apollonian gaskets, strange attractors, recursive depth. The mathematics that makes you stop and stare.",
    description: "Apollonian gaskets, harmonographs, Mandelbrot orbits, recursive structures, and strange attractors. Mathematics that reveals unexpected beauty — order emerging from simple rules.",
    story: "Wonder is the feeling of encountering structure where you expected chaos. A fractal that generates infinite complexity from three lines of code. A strange attractor that never repeats but always stays bounded. This series renders the mathematics that provokes that feeling.",
    mathematicalPrimitive: "fractals, strange attractors, recursive geometry",
    background: "#0A0A18",
    palette: ["#4080C0", "#60A0E0", "#80C0FF", "#2060A0", "#A0D0FF"],
    makingOf: "72 renders. 5 survived.",
    pieces: [
      { id: "wonder-recursion", title: "Recursion", series: "wonder", equation: "f(n) = f(f(n-1))", description: "Midpoint displacement — the same fractal rule applied at every scale. Each ridgeline is built by subdividing, displacing, subdividing again. The mountains in the distance carry the same structure as the ones up close. That's what stopped me: the sameness across scales. You look out at a landscape and the horizon repeats the foreground, smaller and fainter but identical in its roughness. Nature doing the same thing over and over.", emotionalNote: "The same pattern, all the way back", background: "#DDD9D2", imageUrl: "/prints/wonder/wonder_recursion.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "wonder-strange-attractor", title: "Strange Attractor", series: "wonder", equation: "dx=−y−z, dy=x+ay, dz=b+z(x−c)", description: "Three simple equations — each variable pulling on the others. I let it run and the trajectory never repeated, never diverged, never settled. It just kept tracing new paths through the same region of space, forever. Deterministic but unpredictable. Everything about its future is already decided by the equations, and yet you could watch it for a lifetime and never see the same moment twice. The kind of wonder that makes me quiet, like staring at a fire.", emotionalNote: "Determined and yet never the same twice", background: "#DDD9D2", imageUrl: "/prints/wonder/wonder_strange_attractor.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "wonder-transform", title: "Transform", series: "wonder", equation: "w = z + a/(z − z₀)", description: "The small circle is you, the viewer. Looking right, you take in the world — information flowing outward, sweeping wide. But the curves loop back, returning to reshape the observer. Perception becomes reality becomes perception again. A conformal mapping as feedback loop.", emotionalNote: "Perception shapes reality shapes perception", background: "#DDD9D2", imageUrl: "/prints/wonder/wonder_transform.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "wonder-apollonian-gasket", title: "Apollonian Gasket", series: "wonder", equation: "k₄ = k₁+k₂+k₃ + 2√(k₁k₂+k₂k₃+k₁k₃)", description: "Start with three circles tangent to each other inside a fourth. In every gap, fit the largest circle that touches all three neighbors. Repeat. The gaps never fill completely — there's always room for one more circle, smaller and smaller, forever. Infinity nested in the cracks between things.", emotionalNote: "Infinity nested in the cracks between things", background: "#4d476d", imageUrl: "/prints/wonder/wonder_apollonian_gasket.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-wonder-bundle",
    bundlePrice: 169,
  },

  // ── PEACE ───────────────────────────────────────────────
  {
    id: "peace",
    name: "PEACE",
    emotion: "stillness, resolution, equilibrium achieved",
    tagline: "Laplacian steady state. Resolved harmonics. Sand settling into the shape the wind intended.",
    description: "Steady-state solutions, resolved harmonics, settling surfaces, zen garden raking patterns, and cloud formations at equilibrium. Systems that have arrived.",
    story: "Peace is not the absence of force. It is the state after all forces have balanced. The Laplace equation describes this: ∇²f = 0 means every point is the average of its neighbors. No tension. No gradient. Every point in agreement with its surroundings.",
    mathematicalPrimitive: "Laplacian equilibrium, steady-state, resolved harmonics",
    background: "#F0EDE8",
    palette: ["#B0C8B8", "#90B0A0", "#A8C0B0", "#78A090", "#D0E0D0"],
    makingOf: "20 renders. 7 survived.",
    pieces: [
      { id: "peace-horizon", title: "Horizon", series: "peace", equation: "y → c as x → ±∞", description: "Layered atmospheric bands resolving into a single horizon line. The simplest possible landscape. I stripped away everything until only the line between sky and earth remained.", emotionalNote: "Everything stripped down to one line", background: "#F0EDE8", imageUrl: "/prints/peace/peace_horizon.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "peace-breath", title: "Breath", series: "peace", equation: "A(t) = A₀·sin(2πt/T)", description: "Concentric ellipses expanding and contracting. Inhale expands, exhale contracts. I timed the rhythm to my own breathing while making it.", emotionalNote: "Breathing made visible", background: "#F0EDE8", imageUrl: "/prints/peace/peace_breath.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "peace-cloud", title: "Cloud", series: "peace", equation: "ρ(x,y) = Σ Gₖ(x,y,σₖ)", description: "Gaussian density fields drifting in still air. Soft overlapping forms with no edges and no urgency. Nothing needs to happen here.", emotionalNote: "Nothing needs to happen here", background: "#F0EDE8", imageUrl: "/prints/peace/peace_cloud.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "peace-still-water", title: "Still Water", series: "peace", equation: "∇²φ = 0", description: "Laplacian equilibrium — every point is exactly the average of its neighbors. No tension, no gradient. That's literally the mathematical definition of rest.", emotionalNote: "Every point in agreement with what surrounds it", background: "#F0EDE8", imageUrl: "/prints/peace/peace_still_water.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "peace-sand", title: "Sand", series: "peace", equation: "∂h/∂t = -∇·(h·v) + D∇²h", description: "Wind-formed ripples in sand — parallel ridges self-organized by diffusion. I let the simulation run until the surface found its own shape. The wind decided.", emotionalNote: "The shape the wind decided on", background: "#F0EDE8", imageUrl: "/prints/peace/peace_sand.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "peace-harmonic", title: "Harmonic", series: "peace", equation: "ψ = A·sin(nπx/L)·sin(nπy/L)", description: "Standing waves layered at different frequencies. Each mode coexists without interfering with the others. Vibration that has found its form and keeps it.", emotionalNote: "Vibration that found its form and keeps it", background: "#F0EDE8", imageUrl: "/prints/peace/peace_harmonic.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-peace-bundle",
    bundlePrice: 169,
  },

  // ── AWE ─────────────────────────────────────────────────
  {
    id: "awe",
    name: "AWE",
    emotion: "overwhelmed by scale, the sublime",
    tagline: "Solar corona streaming past totality. Accretion disks bending light. Blast waves seeding the periodic table.",
    description: "Eclipse coronas, black hole accretion, supernova blast waves, inverse-square radiance, and interstellar nebulae. The cosmic sublime — mathematics at scales where comprehension dissolves into wonder.",
    story: "Awe is the emotion at the boundary of comprehension. Burke called it the sublime — the overwhelming encounter with something vast. Standing under the Milky Way, watching a solar eclipse, seeing the Hubble Deep Field. This series renders the mathematics of cosmic scale: gravitational lensing, stellar death, light itself.",
    mathematicalPrimitive: "inverse-square law, orbital mechanics, blast waves, gravitational lensing",
    background: "#0A0A10",
    palette: ["#D0A040", "#C88030", "#D4AA40", "#3A5AA0", "#5A3A8A"],
    makingOf: "20 renders. 8 survived.",
    pieces: [
      { id: "awe-deep-field", title: "Deep Field", series: "awe", equation: "N(>S) ~ S^{-3/2}", description: "I scattered ten thousand points of light at every depth — spirals, ellipticals, smears of color. The Hubble Ultra Deep Field as math. Every speck is an entire galaxy.", emotionalNote: "Every speck is an entire galaxy", background: "#0A0A10", imageUrl: "/prints/awe/awe_deep_field.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "awe-murmuration", title: "Murmuration", series: "awe", equation: "v_i = α·align + β·cohere + γ·separate", description: "1400 particles each following three simple rules — align, cohere, separate. Together they sweep through the frame like a flock of starlings. I didn't choreograph any of it.", emotionalNote: "Three rules, no choreography", background: "#1E2030", imageUrl: "/prints/awe/awe_murmuration.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "awe-eclipse", title: "Eclipse", series: "awe", equation: "I(r) = I_corona / r", description: "Solar corona during totality. Streamers of plasma radiating outward, a diamond ring at the limb. I built it from an inverse-distance field — the math the sun actually follows.", emotionalNote: "What the sun reveals only when it's hidden", background: "#0A0A10", imageUrl: "/prints/awe/awe_eclipse.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "awe-singularity", title: "Singularity", series: "awe", equation: "r(φ) = a(1-e²)/(1+e·cosφ)", description: "An accretion disk spiraling into a black hole. I bent the light paths around the event horizon and watched time dilate to infinity at the photon sphere. The math is real.", emotionalNote: "Where gravity bends light and time stops", background: "#0A0A10", imageUrl: "/prints/awe/awe_singularity.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "awe-radiance", title: "Radiance", series: "awe", equation: "I(r) = I₀/r²", description: "120 rays from a brilliant center, each dimming with the square of distance. The inverse-square law — light never quite reaches zero no matter how far you go.", emotionalNote: "Light that never quite reaches zero", background: "#0A0A10", imageUrl: "/prints/awe/awe_radiance.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "awe-cosmic-web", title: "Cosmic Web", series: "awe", equation: "ρ(r) ~ Σ G_ij / r", description: "I rendered the large-scale structure of the universe — galaxies connected by dark matter filaments, nodes glowing where the threads converge. This is what the universe looks like from far enough away.", emotionalNote: "The skeleton of everything", background: "#0A0A10", imageUrl: "/prints/awe/awe_cosmic_web.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "awe-gravitational-waves", title: "Gravitational Waves", series: "awe", equation: "h(r,t) = A·cos(kr-ωt)/r", description: "Quadrupole distortions expanding outward from two merging black holes — spacetime itself stretching and compressing. LIGO detected these. They're real.", emotionalNote: "Ripples in spacetime that were actually detected", background: "#0A0A10", imageUrl: "/prints/awe/awe_gravitational_waves.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "awe-overview", title: "Overview", series: "awe", equation: "h/R ≈ 0.01‰", description: "Earth's atmosphere as a thin luminous arc against the void — the Overview Effect. I drew it to scale. That line is impossibly thin. Everything I know is under it.", emotionalNote: "Everything is under that thin line", background: "#0A0A10", imageUrl: "/prints/awe/awe_overview.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-awe-bundle",
    bundlePrice: 169,
  },

  // ── RESILIENCE ──────────────────────────────────────────
  {
    id: "resilience",
    name: "RESILIENCE",
    emotion: "recovery, repair, growing back stronger",
    tagline: "Overshoot and recovery. Phoenix curves rising past the original baseline. The mathematics of coming back.",
    description: "Recovery dynamics, repair functions, phoenix curves, forging processes, and growth after damage. Systems that return — often stronger — after being pushed past their limits.",
    story: "Resilience is not endurance. Endurance holds. Resilience breaks and reforms. The mathematics of recovery — systems that overshoot their original baseline after perturbation, materials that harden under stress, networks that reroute around damage — describe the geometry of coming back.",
    mathematicalPrimitive: "overshoot recovery, strain hardening, network repair",
    background: "#E8E0D8",
    palette: ["#A06020", "#C08030", "#806018", "#E0A040", "#604010"],
    makingOf: "56 renders. 5 survived.",
    pieces: [
      { id: "resilience-forged", title: "Forged", series: "resilience", equation: "σ_y(ε) = σ₀ + Kε^n", description: "Strain hardening — material that becomes stronger each time it's hit. The yield point actually increases with every deformation. I thought about that a lot.", emotionalNote: "Stronger at every point it was hit", background: "#E8E0D8", imageUrl: "/prints/resilience/resilience_forged.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "resilience-growth", title: "Growth", series: "resilience", equation: "dN/dt = r(K' - N), K' > K", description: "Post-traumatic growth modeled as logistic recovery — but to a carrying capacity higher than the original. Growing back past where you started.", emotionalNote: "Growing back past where you started", background: "#E8E0D8", imageUrl: "/prints/resilience/resilience_growth.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "resilience-phoenix", title: "Phoenix", series: "resilience", equation: "f(t) = A(1 - e^{-t/τ₁})e^{t/τ₂}, τ₂ > τ₁", description: "An exponential recovery that overshoots — the function rises past where it began. Not just back to baseline. Beyond it.", emotionalNote: "Not just recovery — beyond where you started", background: "#E8E0D8", imageUrl: "/prints/resilience/resilience_phoenix.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "resilience-recovery", title: "Recovery", series: "resilience", equation: "x(t) = x_eq + (x₀-x_eq)e^{-t/τ} + overshoot", description: "Damped recovery with overshoot — the system swings past equilibrium before settling. I kept the overshoot in the final render. That extra is what matters.", emotionalNote: "Swinging past center before finding balance", background: "#E8E0D8", imageUrl: "/prints/resilience/resilience_recovery.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "resilience-repair", title: "Repair", series: "resilience", equation: "G(t) = G₀(1 - e^{-t/τ_r}) · H(t-t_d)", description: "A delayed repair function — nothing happens right after the damage. There's a pause. Then the exponential recovery begins. The delay felt important to keep.", emotionalNote: "The pause before the repair begins", background: "#E8E0D8", imageUrl: "/prints/resilience/resilience_repair.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-resilience-bundle",
    bundlePrice: 169,
  },

  // ── TRUST ───────────────────────────────────────────────
  {
    id: "trust",
    name: "TRUST",
    emotion: "synchrony, mutual vulnerability, shared rhythm",
    tagline: "Synchronized breathing. Handshake protocols. Mirror neurons rendered as mathematics.",
    description: "Synchronization functions, handshake protocols, mirror dynamics, mutual phase-locking, and woven trajectories. The mathematics of two systems choosing to be vulnerable together.",
    story: "Trust is not certainty. It is the willingness to synchronize with another system without guarantees. The mathematics of trust involves mutual phase-locking — two oscillators that choose to align, weaving patterns that neither could produce alone.",
    mathematicalPrimitive: "synchronization, mutual phase-locking, weaving, handshake",
    background: "#E8E4E0",
    palette: ["#506878", "#687888", "#788898", "#405868", "#8898A8"],
    makingOf: "37 renders. 5 survived.",
    pieces: [
      { id: "trust-breath-together", title: "Breath Together", series: "trust", equation: "φ₁(t) - φ₂(t) → 0 as t → ∞", description: "Two oscillators converging to zero phase difference. They sync up not because they're forced to, but because the coupling lets them. Nobody asked them to breathe together.", emotionalNote: "Choosing the same rhythm without being asked", background: "#E8E4E0", imageUrl: "/prints/trust/trust_breath_together.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "trust-handshake", title: "Handshake", series: "trust", equation: "SYN → SYN-ACK → ACK", description: "The TCP three-way handshake rendered as art. SYN, SYN-ACK, ACK — I reach out, you acknowledge, I confirm. The simplest protocol of mutual recognition.", emotionalNote: "I reach out. You respond. I confirm.", background: "#E8E4E0", imageUrl: "/prints/trust/trust_handshake.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "trust-mirror", title: "Mirror", series: "trust", equation: "y₁(t) = αy₂(t-τ) + (1-α)y₁(t-τ)", description: "Delayed mirroring — one system following the other with a lag, weighted between self and other. I tuned the balance until neither system lost itself.", emotionalNote: "Following without losing yourself", background: "#E8E4E0", imageUrl: "/prints/trust/trust_mirror.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },

      { id: "trust-weave", title: "Weave", series: "trust", equation: "f(x,y) = sin(x)sin(y) + sin(x)cos(y)", description: "Two sinusoidal functions interlocking — warp and weft creating a fabric. Neither thread is strong alone. Together they hold.", emotionalNote: "Neither strong alone, together they hold", background: "#E8E4E0", imageUrl: "/prints/trust/trust_weave.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-trust-bundle",
    bundlePrice: 169,
  },

  // ── PRIDE ───────────────────────────────────────────────
  {
    id: "pride",
    name: "PRIDE",
    emotion: "identity, solidarity, sheltering one another, standing together",
    tagline: "Superellipse arches, ocean harmonics, and interlocking weaves. The mathematics of being proud of who you are — and standing together.",
    description: "Pride is about your unique glow and light and identity. It is also about standing together — protecting each other, weaving resilience from individual strands, being different waves but moving as one ocean.",
    story: "Pride is being proud of who you are. Your unique light, your identity, your glow. But pride is also what happens when those lights stand together. Superellipse arches — y = h(1−|s|^p) — nest inside each other, each curve sheltering the one beneath it. The exponent p softens each arch differently, but they all share the same center. That is protection. Ocean wave equations — h = ΣAᵢcos(kᵢx−ωᵢt) — layer seventy-eight lines through the full LGBTQ+ spectrum, each wave its own color and frequency, but all of them part of the same sea. That is unity without sameness. Unfurling curves — x = x₀ + A·sⁿ·sin(ωs) — start from a single shared root and find their own paths upward, diverging but never disconnected. Different destinations from the same origin. And interlocking sinusoidal strands — f(x,y) = A·sin(ω₁x)·sin(ω₂y) — weave trans and rainbow palettes into fabric. No single thread holds alone. The strength is in the crossing. That is resilience.",
    mathematicalPrimitive: "superellipse nesting, wave superposition, parametric divergence, sinusoidal weave",
    background: "#f3eee7",
    palette: ["#f6f2ef", "#f5a9b8", "#5bcffb", "#ffd100", "#7f2dbd"],
    makingOf: "New series — building out.",
    pieces: [
      { id: "pride-shelter", title: "Shelter", series: "pride", equation: "y = h(1−|s|^p)", description: "Twenty-four nested superellipse arches, each one smaller and softer than the one outside it. Every arch is a person standing over someone so they don't have to stand alone.", emotionalNote: "Each arch protecting the one beneath it", background: "#f3eee7", imageUrl: "/prints/pride/pride_shelter.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "pride-waves", title: "Waves", series: "pride", equation: "h = ΣAᵢcos(kᵢx−ωᵢt)", description: "Seventy-eight ocean lines moving through the full LGBTQ+ spectrum — trans blue, pink, and white woven through the classic rainbow. Many waves, one sea. Every color present, none token.", emotionalNote: "Many waves, one sea", background: "#f3eee7", imageUrl: "/prints/pride/pride_waves.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "pride-unfurling", title: "Unfurling", series: "pride", equation: "x = x₀ + A·sⁿ·sin(ωs)", description: "Sixty-two lines rooted at a single point, unfurling upward through the full LGBTQ+ spectrum. Something that was contained, choosing to open — every line finding its own path from the same origin.", emotionalNote: "Something contained, choosing to open", background: "#f3eee7", imageUrl: "/prints/pride/pride_unfurling.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "pride-woven-resilience", title: "Woven Resilience", series: "pride", equation: "f(x,y) = A·sin(ω₁x+φ)·sin(ω₂y+ψ)", description: "Trans palette woven through rainbow — eighteen horizontal strands interlocking with eighteen vertical strands. Woven together to create resilience. No single thread holds alone; the strength is in the crossing.", emotionalNote: "The strength is in the crossing", background: "#f3eee7", imageUrl: "/prints/pride/pride_woven_resilience.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "pride-golden-ratio", title: "Golden Ratio", series: "pride", equation: "θₙ = n · 137.508°, rₙ = √n", description: "Three hundred and fifty dots placed at the golden angle — the same irrational rotation sunflowers use to pack seeds. Trans pink, blue, and white woven through the full rainbow spectrum. Every color finding its place without crowding any other.", emotionalNote: "Every color finding its place", background: "#f3eee7", imageUrl: "/prints/pride/pride_golden_ratio.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "pride-flourish", title: "Flourish", series: "pride", equation: "x(t) = t + a·sin(2πt), y(t) = b·sin(πt)^c", description: "Sixteen calligraphic sweeps rising to a peak — each line thickens at the crest like a brushstroke pressed into paper. The full LGBTQ+ spectrum from trans pink to deep violet, every color confident and unapologetic.", emotionalNote: "Every color confident and unapologetic", background: "#f3eee7", imageUrl: "/prints/pride/pride_flourish.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-pride-bundle",
    bundlePrice: 169,
  },

  // ── ANTICIPATION ────────────────────────────────────────
  {
    id: "anticipation",
    name: "ANTICIPATION",
    emotion: "building, gathering, the moment before",
    tagline: "Charge accumulating on a capacitor. Convergent sequences approaching their limit. The held breath before the event.",
    description: "Capacitor charging curves, convergent sequences, countdown functions, kindling thresholds, and potential energy surfaces. The mathematics of systems approaching a threshold they haven't yet crossed.",
    story: "Anticipation is potential energy. The mathematics of 'almost' — convergent sequences, charging capacitors, systems approaching but not yet reaching a critical threshold. This series renders the geometry of the moment before.",
    mathematicalPrimitive: "convergence, accumulation, threshold approach, potential energy",
    background: "#E8E4DC",
    palette: ["#8A7A50", "#A09060", "#706840", "#B8A878", "#605830"],
    makingOf: "46 renders. 5 survived.",
    pieces: [
      { id: "anticipation-charge", title: "Charge", series: "anticipation", equation: "V(t) = V₀(1 - e^{-t/RC})", description: "A capacitor charging — voltage rising toward maximum, each moment adding less than the last. It gets so close you'd swear it's there, but mathematically it never arrives.", emotionalNote: "So close you'd swear it's there, but it never arrives", background: "#E8E4DC", imageUrl: "/prints/anticipation/anticipation_charge.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "anticipation-countdown", title: "Countdown", series: "anticipation", equation: "f(t) = N - ⌊t/Δt⌋", description: "A step function counting down — each step identical. The last one looks exactly like all the others, but it changes everything.", emotionalNote: "The last step looks the same but changes everything", background: "#E8E4DC", imageUrl: "/prints/anticipation/anticipation_countdown.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "anticipation-kindling", title: "Kindling", series: "anticipation", equation: "T(t) = T_ign - ΔT·e^{-t/τ}", description: "Temperature approaching ignition — exponentially closing the gap, the combustion threshold right there. Almost. Almost. Not yet.", emotionalNote: "Almost. Almost. Not yet.", background: "#E8E4DC", imageUrl: "/prints/anticipation/anticipation_kindling.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-anticipation-bundle",
    bundlePrice: 169,
  },

  // ── LONGING ─────────────────────────────────────────────
  {
    id: "longing",
    name: "LONGING",
    emotion: "reaching toward what recedes, the ache of distance",
    tagline: "Zeno's paradox — always halving the distance, never arriving. Harmonic decay toward an unreachable tone.",
    description: "Harmonic decay, magnetic field lines, Tantalus functions, vanishing points, and Zeno sequences. The mathematics of distance that cannot be closed.",
    story: "Longing is Zeno's paradox made emotional. You halve the distance, then halve it again, always approaching, never arriving. The mathematics of asymptotic approach — functions that tend toward a limit they will never reach — perfectly describe the geometry of wanting something that remains just beyond.",
    mathematicalPrimitive: "asymptotic approach, harmonic decay, vanishing point, Zeno's paradox",
    background: "#E0E4E8",
    palette: ["#6080A0", "#8090A0", "#4060A0", "#A0B0C0", "#506890"],
    makingOf: "51 renders. 5 survived.",
    pieces: [
      { id: "longing-harmonic-decay", title: "Harmonic Decay", series: "longing", equation: "f(t) = A₀ · cos(ωt) · e^{-γt}", description: "A damped harmonic oscillator. Each swing shorter than the last, but it never fully stops. The memory of motion fading without ever disappearing.", emotionalNote: "Fading without ever disappearing", background: "#E0E4E8", imageUrl: "/prints/longing/longing_harmonic_decay.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "longing-magnetic", title: "Magnetic", series: "longing", equation: "F = μ₀m₁m₂/(4πr²)", description: "Magnetic field lines reaching toward each other across empty space. They get close — they curve toward each other — but they don't connect.", emotionalNote: "Reaching across empty space without connecting", background: "#E0E4E8", imageUrl: "/prints/longing/longing_magnetic.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "longing-tantalus", title: "Tantalus", series: "longing", equation: "lim_{x→a} f(x) = L, f(a) undefined", description: "A removable discontinuity — the limit exists, but the value at that point doesn't. You can see exactly where it should be. You just can't be there.", emotionalNote: "You can see exactly where it should be but can't be there", background: "#E0E4E8", imageUrl: "/prints/longing/longing_tantalus.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "longing-vanishing", title: "Vanishing", series: "longing", equation: "x' = x·f/(f+d), y' = y·f/(f+d)", description: "Perspective projection — parallel lines converging to a vanishing point that recedes as you approach. The destination is always visible and always the same distance away.", emotionalNote: "Always visible, always the same distance away", background: "#E0E4E8", imageUrl: "/prints/longing/longing_vanishing.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-longing-bundle",
    bundlePrice: 169,
  },
];

export const allPieces: Piece[] = series.flatMap((s) => s.pieces);

export const collectionPrice = 450;
export const collectionGumroadUrl = "https://gumroad.com/l/placeholder-full-collection";

export interface HeroSlide {
  pieceId: string;
  textColor: "white" | "black";
}

export const heroSlides: HeroSlide[] = [
  { pieceId: "desire-pursuit", textColor: "black" },
  { pieceId: "growth-branch", textColor: "black" },
  { pieceId: "pride-waves", textColor: "black" },
  { pieceId: "grief-void", textColor: "black" },
  { pieceId: "wonder-strange-attractor", textColor: "white" },
];

export const featuredSeriesIds = [
  "awe",
  "connection",
  "grief",
  "pride",
  "peace",
  "wonder",
  "desire",
  "cycles",
  "solitude",
  "growth",
];

export const featuredPieceIds = [
  "grief-void",
  "awe-eclipse",
  "growth-branch",
  "peace-horizon",
  "wonder-apollonian-gasket",
  "pride-flourish",
  "connection-orbit-pair",
  "desire-pursuit",
];

export function getSeriesBySlug(slug: string): Series | undefined {
  return series.find((s) => s.id === slug);
}

export function getPieceBySlug(slug: string): Piece | undefined {
  return allPieces.find((p) => p.id === slug);
}

export function getPiecesBySeries(seriesId: string): Piece[] {
  return allPieces.filter((p) => p.series === seriesId);
}
