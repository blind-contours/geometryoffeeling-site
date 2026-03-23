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
}

export const series: Series[] = [
  {
    id: "fractured",
    name: "FRACTURED",
    emotion: "fracture, discontinuity, the moment things break",
    tagline:
      "Piecewise functions where the limit from the left never meets the limit from the right. The discontinuity is the emotion.",
    description:
      "Piecewise discontinuous functions rendered as visual fields. Each piece explores a different topology of breaking — bifurcation cascades, catastrophe folds, Voronoi shattering, seismic faults, glass fracture networks. The mathematics of rupture made visible.",
    story:
      "Fracture is not random. When a material breaks, it follows the physics of stress propagation. When a life breaks, it follows the topology of connection — the pieces that were closest fracture first. This series uses discontinuous functions, bifurcation diagrams, and Voronoi tessellation to map the geometry of things coming apart. The math is real: these are the same equations that describe fault lines, shattered glass, and phase transitions.",
    mathematicalPrimitive: "piecewise discontinuous functions, bifurcation, Voronoi tessellation",
    background: "#F5F0E0",
    palette: ["#3A5BA0", "#D4573B", "#E8A838", "#6B4E8B", "#2D8B6E"],
    pieces: [
      {
        id: "fractured-bifurcation",
        title: "Bifurcation",
        series: "fractured",
        equation: "x_{n+1} = rx_n(1 - x_n)",
        description:
          "The logistic map's period-doubling cascade — a single path splitting into two, then four, then chaos. The moment when one future becomes many, and none of them converge.",
        emotionalNote: "The point where a single path becomes irreconcilable futures",
        background: "#F5F0E0",
        imageUrl: "/prints/fractured/fractured_bifurcation.jpg",
        gumroadUrl: "https://gumroad.com/l/placeholder",
        price: 22,
      },
      {
        id: "fractured-catastrophe-fold",
        title: "Catastrophe Fold",
        series: "fractured",
        equation: "V(x) = x^4 + ax^2 + bx",
        description:
          "A cusp catastrophe — the smooth surface that suddenly drops. Named after René Thom's catastrophe theory: systems that change gradually until they don't.",
        emotionalNote: "The smooth surface that suddenly drops away",
        background: "#F5F0E0",
        imageUrl: "/prints/fractured/fractured_catastrophe_fold.jpg",
        gumroadUrl: "https://gumroad.com/l/placeholder",
        price: 22,
      },
      {
        id: "fractured-glass-fracture",
        title: "Glass Fracture",
        series: "fractured",
        equation: "K_I = σ√(πa)",
        description:
          "Stress intensity at a crack tip — the mathematics of fracture mechanics. Each line propagates according to the Griffith criterion, branching where the energy demands it.",
        emotionalNote: "Every crack follows the path of least resistance through the structure",
        background: "#F5F0E0",
        imageUrl: "/prints/fractured/fractured_glass_fracture.jpg",
        gumroadUrl: "https://gumroad.com/l/placeholder",
        price: 22,
      },
      {
        id: "fractured-seismic-fault",
        title: "Seismic Fault",
        series: "fractured",
        equation: "log₁₀(N) = a - bM",
        description:
          "The Gutenberg-Richter law — the power law governing earthquake magnitudes. Tension accumulates in silence, then releases all at once along the fault.",
        emotionalNote: "Tension that accumulates invisibly until the ground itself gives way",
        background: "#F5F0E0",
        imageUrl: "/prints/fractured/fractured_seismic_fault.jpg",
        gumroadUrl: "https://gumroad.com/l/placeholder",
        price: 22,
      },
      {
        id: "fractured-voronoi-shatter",
        title: "Voronoi Shatter",
        series: "fractured",
        equation: "V(p) = {x : d(x,p) ≤ d(x,q) ∀q}",
        description:
          "Voronoi tessellation — the geometry of territory. Each cell claims the space closest to its center. When the centers shift, the boundaries break and reform.",
        emotionalNote: "The space between things, divided by what is closest to each",
        background: "#F5F0E0",
        imageUrl: "/prints/fractured/fractured_voronoi_shatter.jpg",
        gumroadUrl: "https://gumroad.com/l/placeholder",
        price: 22,
      },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-fractured-bundle",
    bundlePrice: 75,
  },
  {
    id: "connection",
    name: "CONNECTION",
    emotion: "closeness, following, the space between two things",
    tagline:
      "Two parametric curves with a phase offset. Neither leads nor follows. The gap between them is the relationship.",
    description:
      "Parametric curve pairs with phase offsets, coupled oscillators, and topological knots. Two systems that move through space together — sometimes synchronized, sometimes drifting, always tethered. The mathematics of being bound to another.",
    story:
      "Connection is not union. It is two separate trajectories that choose proximity. The coupled oscillator equations describe this precisely: two systems that influence each other's frequency, amplitude, and phase. They never fully merge. The space between them — the phase offset — is where the relationship lives. This series renders that space as light against darkness.",
    mathematicalPrimitive: "parametric curves, coupled oscillators, topological knots",
    background: "#0A0A12",
    palette: ["#D4A856", "#E8C878", "#C49A3C", "#F0D890", "#B08830"],
    pieces: [
      {
        id: "connection-coupled-oscillators",
        title: "Coupled Oscillators",
        series: "connection",
        equation: "ẍ₁ = -ω₁²x₁ + κ(x₂ - x₁)",
        description:
          "Two oscillators connected by a spring — each pulling the other toward its own rhythm. The coupling constant κ determines whether they synchronize or fight.",
        emotionalNote: "Two rhythms learning to coexist",
        background: "#0A0A12",
        imageUrl: "/prints/connection/connection_coupled_oscillators.jpg",
        gumroadUrl: "https://gumroad.com/l/placeholder",
        price: 22,
      },
      {
        id: "connection-double-helix",
        title: "Double Helix",
        series: "connection",
        equation: "r(t) = (cos t, sin t, t/2π) ± d/2",
        description:
          "Two helical curves winding around a shared axis — never touching, always equidistant. The geometry of DNA, and of two lives spiraling forward together.",
        emotionalNote: "Parallel paths winding around a shared center",
        background: "#0A0A12",
        imageUrl: "/prints/connection/connection_double_helix.jpg",
        gumroadUrl: "https://gumroad.com/l/placeholder",
        price: 22,
      },
      {
        id: "connection-phase-sync",
        title: "Phase Sync",
        series: "connection",
        equation: "dθ/dt = ω + K sin(θ₂ - θ₁)",
        description:
          "The Kuramoto model of phase synchronization — oscillators that gradually align their rhythms. The moment two independent cycles lock into shared time.",
        emotionalNote: "The moment two separate rhythms find the same beat",
        background: "#0A0A12",
        imageUrl: "/prints/connection/connection_phase_sync.jpg",
        gumroadUrl: "https://gumroad.com/l/placeholder",
        price: 22,
      },
      {
        id: "connection-torus-knot",
        title: "Torus Knot",
        series: "connection",
        equation: "r(t) = ((R + r cos qt) cos pt, (R + r cos qt) sin pt, r sin qt)",
        description:
          "A curve that winds around a torus — looping through and around itself without ever crossing. Topologically, it cannot be untied without cutting.",
        emotionalNote: "A bond that cannot be undone without breaking the topology",
        background: "#0A0A12",
        imageUrl: "/prints/connection/connection_torus_knot.jpg",
        gumroadUrl: "https://gumroad.com/l/placeholder",
        price: 22,
      },
      {
        id: "connection-two-body",
        title: "Two Body",
        series: "connection",
        equation: "F = -Gm₁m₂/r² · r̂",
        description:
          "The gravitational two-body problem — two masses orbiting their common center. Each shapes the other's path. Neither is stationary.",
        emotionalNote: "Two masses shaping each other's orbits",
        background: "#0A0A12",
        imageUrl: "/prints/connection/connection_two_body.jpg",
        gumroadUrl: "https://gumroad.com/l/placeholder",
        price: 22,
      },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-connection-bundle",
    bundlePrice: 75,
  },
  {
    id: "tension",
    name: "TENSION",
    emotion: "strain, opposition, systems that cannot rest",
    tagline:
      "Lorentzian resonance and beating frequencies. Systems that cannot rest and will not resolve.",
    description:
      "Interference patterns, opposing forces, torsional stress, and buckling columns. Systems held between competing demands — too much energy to rest, too constrained to move. The visual field of unresolved force.",
    story:
      "Tension is not conflict. Conflict resolves. Tension is the state between resolution and collapse — the beam that holds because opposing forces balance perfectly. This series draws from structural mechanics, wave interference, and torsional dynamics. Each piece is a system under stress, rendered in electric yellow against dark ground, inspired by the psychological intensity of Munch's color field.",
    mathematicalPrimitive: "interference, torsion, buckling, opposing forces",
    background: "#1A1A1A",
    palette: ["#E8D42A", "#D4282A", "#F0E648", "#CC1A1C", "#FFF060"],
    pieces: [
      {
        id: "tension-buckling",
        title: "Buckling",
        series: "tension",
        equation: "P_cr = π²EI / (KL)²",
        description:
          "Euler's critical load — the exact force at which a column buckles. Below this threshold, perfectly stable. At this threshold, catastrophic failure. There is no warning.",
        emotionalNote: "The exact threshold between holding and collapse",
        background: "#1A1A1A",
        imageUrl: "/prints/tension/tension_buckling.jpg",
        gumroadUrl: "https://gumroad.com/l/placeholder",
        price: 24,
      },
      {
        id: "tension-fracture",
        title: "Fracture",
        series: "tension",
        equation: "σ = Eε (until σ > σ_y)",
        description:
          "Hooke's law pushed past the yield point — the linear relationship between stress and strain that holds perfectly until it doesn't. The elastic limit is invisible until it's crossed.",
        emotionalNote: "The invisible line between bending and breaking",
        background: "#1A1A1A",
        imageUrl: "/prints/tension/tension_fracture.jpg",
        gumroadUrl: "https://gumroad.com/l/placeholder",
        price: 24,
      },
      {
        id: "tension-interference",
        title: "Interference",
        series: "tension",
        equation: "A(x) = A₁sin(k₁x) + A₂sin(k₂x)",
        description:
          "Two wave sources creating an interference pattern — constructive and destructive zones alternating across the field. Peaks where the waves align, silence where they cancel.",
        emotionalNote: "Where two forces meet, they either amplify or annihilate",
        background: "#1A1A1A",
        imageUrl: "/prints/tension/tension_interference.jpg",
        gumroadUrl: "https://gumroad.com/l/placeholder",
        price: 24,
      },
      {
        id: "tension-opposition",
        title: "Opposition",
        series: "tension",
        equation: "F_net = F₁ - F₂ = 0, |F₁| > 0",
        description:
          "Equal and opposite forces in perfect balance — the net force is zero, but the internal stress is immense. Static equilibrium is not peace. It is maximum tension, perfectly contained.",
        emotionalNote: "Perfect balance is not peace — it is maximum contained force",
        background: "#1A1A1A",
        imageUrl: "/prints/tension/tension_opposition.jpg",
        gumroadUrl: "https://gumroad.com/l/placeholder",
        price: 24,
      },
      {
        id: "tension-torsion",
        title: "Torsion",
        series: "tension",
        equation: "τ = Tr/J",
        description:
          "The shear stress in a twisted shaft — maximum at the surface, zero at the center. The outside holds all the strain while the core remains untouched.",
        emotionalNote: "The outside holds all the strain while the center feels nothing",
        background: "#1A1A1A",
        imageUrl: "/prints/tension/tension_torsion.jpg",
        gumroadUrl: "https://gumroad.com/l/placeholder",
        price: 24,
      },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-tension-bundle",
    bundlePrice: 80,
  },
  {
    id: "overwhelm",
    name: "OVERWHELM",
    emotion: "too much, saturation, systems past capacity",
    tagline:
      "Twelve harmonics, eight wave sources, twenty-two parallel streams. Each coherent alone. Together, unresolvable.",
    description:
      "Multiple simultaneous systems rendered together — strange attractors, Kuramoto synchronization, Lévy flights, phase floods, and turbulent flow. Each system is beautiful alone. Together, they exceed the capacity to resolve. The density is the overwhelm.",
    story:
      "Overwhelm is not confusion. Each individual signal is clear. The problem is that there are too many of them. This series renders 10, 20, 50 simultaneous mathematical systems in the same visual field — attractors, swarms, phase-locked oscillators, turbulent flows. The palette uses the full spectrum because overwhelm does not discriminate. Everything arrives at once.",
    mathematicalPrimitive: "multi-system superposition, turbulence, swarm dynamics",
    background: "#0A0A12",
    palette: [
      "#E84040",
      "#40A0E8",
      "#E8D040",
      "#40E888",
      "#D040E8",
      "#E88040",
      "#4060E8",
      "#A0E840",
      "#E840A0",
      "#40E8D0",
    ],
    pieces: [
      {
        id: "overwhelm-attractors",
        title: "Attractors",
        series: "overwhelm",
        equation: "dx/dt = σ(y-x), dy/dt = x(ρ-z)-y, dz/dt = xy-βz",
        description:
          "Multiple Lorenz attractors rendered simultaneously — each following its own deterministic chaos, together creating a visual field that cannot be parsed into individual trajectories.",
        emotionalNote: "Every path is determined, but together they are unreadable",
        background: "#0A0A12",
        imageUrl: "/prints/overwhelm/overwhelm_attractors.jpg",
        gumroadUrl: "https://gumroad.com/l/placeholder",
        price: 24,
      },
      {
        id: "overwhelm-kuramoto",
        title: "Kuramoto",
        series: "overwhelm",
        equation: "dθᵢ/dt = ωᵢ + (K/N)Σsin(θⱼ - θᵢ)",
        description:
          "The Kuramoto model with dozens of oscillators — each trying to synchronize, none fully succeeding. The coupling is too weak for the diversity of natural frequencies.",
        emotionalNote: "Dozens of rhythms trying and failing to align",
        background: "#0A0A12",
        imageUrl: "/prints/overwhelm/overwhelm_kuramoto.jpg",
        gumroadUrl: "https://gumroad.com/l/placeholder",
        price: 24,
      },
      {
        id: "overwhelm-levy-swarm",
        title: "Levy Swarm",
        series: "overwhelm",
        equation: "P(x) ~ |x|^(-1-α), 0 < α < 2",
        description:
          "A swarm of Lévy flights — heavy-tailed random walks with occasional enormous jumps. Unlike Brownian motion, Lévy walkers do not stay local. They fill space unpredictably.",
        emotionalNote: "Random motion that refuses to stay bounded",
        background: "#0A0A12",
        imageUrl: "/prints/overwhelm/overwhelm_levy_swarm.jpg",
        gumroadUrl: "https://gumroad.com/l/placeholder",
        price: 24,
      },
      {
        id: "overwhelm-phase-flood",
        title: "Phase Flood",
        series: "overwhelm",
        equation: "ψ(x,t) = Σ Aₙ e^(i(kₙx - ωₙt + φₙ))",
        description:
          "Dozens of complex wave functions superposed — each with its own frequency, wavenumber, and phase. The resulting field is everywhere nonzero and nowhere still.",
        emotionalNote: "Every point in space vibrating from every direction at once",
        background: "#0A0A12",
        imageUrl: "/prints/overwhelm/overwhelm_phase_flood.jpg",
        gumroadUrl: "https://gumroad.com/l/placeholder",
        price: 24,
      },
      {
        id: "overwhelm-turbulence",
        title: "Turbulence",
        series: "overwhelm",
        equation: "Re = ρvL/μ >> Re_cr",
        description:
          "Fluid flow past the critical Reynolds number — the transition from laminar to turbulent. Order becomes chaos not gradually, but through a cascade of instabilities at every scale.",
        emotionalNote: "Order dissolving into chaos at every scale simultaneously",
        background: "#0A0A12",
        imageUrl: "/prints/overwhelm/overwhelm_turbulence.jpg",
        gumroadUrl: "https://gumroad.com/l/placeholder",
        price: 24,
      },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-overwhelm-bundle",
    bundlePrice: 80,
  },
  {
    id: "grief",
    name: "GRIEF",
    emotion: "decay, absence, the quiet after loss",
    tagline:
      "Exponential decay toward zero. Half-life curves draining from two directions. The plateau that holds until the edges yield.",
    description:
      "Heat diffusion, step-function cascades, spectral erosion, voids, and weight fields. The mathematics of things disappearing — not suddenly, but according to precise laws of decay. The quietest series. The absence of color is the grief.",
    story:
      "Grief obeys the mathematics of decay. The half-life equation — f(t) = e^(-λt) — describes how radioactive isotopes lose their energy, but it also describes how the intensity of grief diminishes over time. It never reaches zero. The asymptote is forever. This series uses muted palettes, cool greys, and vast negative space because grief is not loud. It is the growing silence where something used to be.",
    mathematicalPrimitive: "exponential decay, heat diffusion, step functions, erosion",
    background: "#DDD9D2",
    palette: ["#7A8B9A", "#9A8A9A", "#C8D4E0", "#A0A8B0", "#D0C8D0"],
    pieces: [
      {
        id: "grief-heat-diffusion",
        title: "Heat Diffusion",
        series: "grief",
        equation: "∂u/∂t = α∇²u",
        description:
          "The heat equation — temperature spreading from hot to cold until everything reaches equilibrium. The initial intensity diffuses outward, flattening, never fully gone but everywhere diminished.",
        emotionalNote: "Intensity that spreads thinner until it becomes ambient",
        background: "#DDD9D2",
        imageUrl: "/prints/grief/grief_heat_diffusion.jpg",
        gumroadUrl: "https://gumroad.com/l/placeholder",
        price: 22,
      },
      {
        id: "grief-heaviside-cascade",
        title: "Heaviside Cascade",
        series: "grief",
        equation: "H(t - t₀) = {0, t < t₀; 1, t ≥ t₀}",
        description:
          "A cascade of Heaviside step functions — each one a sudden drop, a new absence. Loss does not arrive continuously. It arrives in discrete collapses, each one a new floor.",
        emotionalNote: "Loss arriving in discrete collapses, each one a new floor",
        background: "#DDD9D2",
        imageUrl: "/prints/grief/grief_heaviside_cascade.jpg",
        gumroadUrl: "https://gumroad.com/l/placeholder",
        price: 22,
      },
      {
        id: "grief-spectral-erosion",
        title: "Spectral Erosion",
        series: "grief",
        equation: "S(f,t) = S₀(f) · e^(-γ(f)t)",
        description:
          "A frequency spectrum losing its higher harmonics over time — the richness of a signal eroding until only the fundamental remains. Detail fading, leaving only the essential tone.",
        emotionalNote: "The richness of memory eroding to a single tone",
        background: "#DDD9D2",
        imageUrl: "/prints/grief/grief_spectral_erosion.jpg",
        gumroadUrl: "https://gumroad.com/l/placeholder",
        price: 22,
      },
      {
        id: "grief-void",
        title: "Void",
        series: "grief",
        equation: "∫∫ ρ(x,y) dA → 0",
        description:
          "A density field collapsing toward emptiness — the integral of presence approaching zero. The mathematical description of a space that used to contain something.",
        emotionalNote: "The shape of what used to be there",
        background: "#DDD9D2",
        imageUrl: "/prints/grief/grief_void.jpg",
        gumroadUrl: "https://gumroad.com/l/placeholder",
        price: 22,
      },
      {
        id: "grief-weight",
        title: "Weight",
        series: "grief",
        equation: "F = mg, m(t) = m₀(1 - e^(-t/τ))",
        description:
          "A mass that increases with time — the weight of grief that grows heavier before the exponential saturation levels it. The body feels it before the mind names it.",
        emotionalNote: "The weight that arrives slowly and saturates",
        background: "#DDD9D2",
        imageUrl: "/prints/grief/grief_weight.jpg",
        gumroadUrl: "https://gumroad.com/l/placeholder",
        price: 22,
      },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-grief-bundle",
    bundlePrice: 75,
  },
  {
    id: "growth",
    name: "GROWTH",
    emotion: "emergence, branching, reaching toward light",
    tagline:
      "L-system branching at thirteen levels. Golden spirals tiling the plane. Thirty-four lines reaching toward light.",
    description:
      "Bifurcation diagrams, dendritic growth, Lissajous blooms, logistic cascades, and reaction-diffusion patterns. The mathematics of systems that expand, branch, differentiate, and fill available space. Growth is not linear — it is fractal.",
    story:
      "Growth follows rules. The branching of trees obeys L-system grammars. The spiral of a nautilus follows the golden ratio. Reaction-diffusion systems create the spots on leopards and the stripes on zebrafish. This series renders these growth algorithms as minimalist art — dark greens and spring golds on warm ivory, inspired by the aesthetics of botanical illustration and the precision of computational biology.",
    mathematicalPrimitive: "L-systems, bifurcation, reaction-diffusion, logistic maps",
    background: "#F5F0E6",
    palette: ["#1A4D2E", "#2E8B4A", "#6BBF6E", "#A8D86E", "#E8D878"],
    pieces: [
      {
        id: "growth-bifurcation",
        title: "Bifurcation",
        series: "growth",
        equation: "x_{n+1} = rx_n(1 - x_n), r ∈ [2.5, 4]",
        description:
          "The logistic map's bifurcation diagram read as a growth narrative — a single population strategy splitting into increasingly complex behaviors as pressure increases.",
        emotionalNote: "Simple beginnings branching into irreducible complexity",
        background: "#F5F0E6",
        imageUrl: "/prints/growth/growth_bifurcation.jpg",
        gumroadUrl: "https://gumroad.com/l/placeholder",
        price: 22,
      },
      {
        id: "growth-dendrite",
        title: "Dendrite",
        series: "growth",
        equation: "L → F[+L][-L]FL",
        description:
          "An L-system rendering dendritic branching — the same algorithm that grows neural dendrites, river deltas, and lightning. Recursive grammar producing infinite complexity from simple rules.",
        emotionalNote: "The same rule applied at every scale, forever branching",
        background: "#F5F0E6",
        imageUrl: "/prints/growth/growth_dendrite.jpg",
        gumroadUrl: "https://gumroad.com/l/placeholder",
        price: 22,
      },
      {
        id: "growth-lissajous-bloom",
        title: "Lissajous Bloom",
        series: "growth",
        equation: "x = A sin(at + δ), y = B sin(bt)",
        description:
          "Lissajous curves with slowly evolving parameters — the figure blooming outward as the frequency ratio shifts. A flower drawn by oscillation.",
        emotionalNote: "Oscillation that opens outward like a flower",
        background: "#F5F0E6",
        imageUrl: "/prints/growth/growth_lissajous_bloom.jpg",
        gumroadUrl: "https://gumroad.com/l/placeholder",
        price: 22,
      },
      {
        id: "growth-logistic-cascade",
        title: "Logistic Cascade",
        series: "growth",
        equation: "dN/dt = rN(1 - N/K)",
        description:
          "The logistic growth equation — population expanding rapidly, then slowing as it approaches carrying capacity. The S-curve of every natural system finding its limit.",
        emotionalNote: "Rapid expansion learning to respect its own limits",
        background: "#F5F0E6",
        imageUrl: "/prints/growth/growth_logistic_cascade.jpg",
        gumroadUrl: "https://gumroad.com/l/placeholder",
        price: 22,
      },
      {
        id: "growth-reaction-diffusion",
        title: "Reaction Diffusion",
        series: "growth",
        equation: "∂u/∂t = Dᵤ∇²u + f(u,v)",
        description:
          "A Turing reaction-diffusion system — two chemicals diffusing at different rates, creating spontaneous pattern. The mathematics behind biological morphogenesis, from spots to stripes to labyrinths.",
        emotionalNote: "Pattern emerging from nothing but diffusion and reaction",
        background: "#F5F0E6",
        imageUrl: "/prints/growth/growth_reaction_diffusion.jpg",
        gumroadUrl: "https://gumroad.com/l/placeholder",
        price: 22,
      },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-growth-bundle",
    bundlePrice: 75,
  },
];

export const allPieces: Piece[] = series.flatMap((s) => s.pieces);

export const collectionPrice = 220;
export const collectionGumroadUrl = "https://gumroad.com/l/placeholder-full-collection";

export function getSeriesBySlug(slug: string): Series | undefined {
  return series.find((s) => s.id === slug);
}

export function getPieceBySlug(slug: string): Piece | undefined {
  return allPieces.find((p) => p.id === slug);
}

export function getPiecesBySeries(seriesId: string): Piece[] {
  return allPieces.filter((p) => p.series === seriesId);
}
