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
      { id: "fractured-bifurcation", title: "Bifurcation", series: "fractured", equation: "x_{n+1} = rx_n(1 - x_n)", description: "The logistic map's period-doubling cascade — a single path splitting into two, then four, then chaos.", emotionalNote: "The point where a single path becomes irreconcilable futures", background: "#F5F0E0", imageUrl: "/prints/fractured/fractured_bifurcation.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "fractured-catastrophe-fold", title: "Catastrophe Fold", series: "fractured", equation: "V(x) = x⁴ + ax² + bx", description: "A cusp catastrophe — the smooth surface that suddenly drops. Named after René Thom's catastrophe theory.", emotionalNote: "The smooth surface that suddenly drops away", background: "#F5F0E0", imageUrl: "/prints/fractured/fractured_catastrophe_fold.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "fractured-glass-fracture", title: "Glass Fracture", series: "fractured", equation: "K_I = σ√(πa)", description: "Stress intensity at a crack tip — the mathematics of fracture mechanics. Each line propagates according to the Griffith criterion.", emotionalNote: "Every crack follows the path of least resistance through the structure", background: "#F5F0E0", imageUrl: "/prints/fractured/fractured_glass_fracture.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "fractured-seismic-fault", title: "Seismic Fault", series: "fractured", equation: "log₁₀(N) = a - bM", description: "The Gutenberg-Richter law — tension accumulates in silence, then releases all at once along the fault.", emotionalNote: "Tension that accumulates invisibly until the ground itself gives way", background: "#F5F0E0", imageUrl: "/prints/fractured/fractured_seismic_fault.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "fractured-voronoi-shatter", title: "Voronoi Shatter", series: "fractured", equation: "V(p) = {x : d(x,p) ≤ d(x,q) ∀q}", description: "Voronoi tessellation — the geometry of territory. Each cell claims the space closest to its center.", emotionalNote: "The space between things, divided by what is closest to each", background: "#F5F0E0", imageUrl: "/prints/fractured/fractured_voronoi_shatter.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-fractured-bundle",
    bundlePrice: 82,
  },

  // ── CONNECTION ──────────────────────────────────────────
  {
    id: "connection",
    name: "CONNECTION",
    emotion: "closeness, following, the space between two things",
    tagline: "Two parametric curves with a phase offset. Neither leads nor follows. The gap between them is the relationship.",
    description: "Parametric curve pairs with phase offsets, coupled oscillators, and topological knots. Two systems that move through space together — sometimes synchronized, sometimes drifting, always tethered.",
    story: "Connection is not union. It is two separate trajectories that choose proximity. The coupled oscillator equations describe this precisely: two systems that influence each other's frequency, amplitude, and phase. They never fully merge. The space between them is where the relationship lives.",
    mathematicalPrimitive: "parametric curves, coupled oscillators, topological knots",
    background: "#0A0A12",
    palette: ["#D4A856", "#E8C878", "#C49A3C", "#F0D890", "#B08830"],
    makingOf: "62 renders. 5 survived.",
    pieces: [
      { id: "connection-coupled-oscillators", title: "Coupled Oscillators", series: "connection", equation: "ẍ₁ = -ω₁²x₁ + κ(x₂ - x₁)", description: "Two oscillators connected by a spring — each pulling the other toward its own rhythm.", emotionalNote: "Two rhythms learning to coexist", background: "#0A0A12", imageUrl: "/prints/connection/connection_coupled_oscillators.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "connection-double-helix", title: "Double Helix", series: "connection", equation: "r(t) = (cos t, sin t, t/2π) ± d/2", description: "Two helical curves winding around a shared axis — never touching, always equidistant.", emotionalNote: "Parallel paths winding around a shared center", background: "#0A0A12", imageUrl: "/prints/connection/connection_double_helix.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "connection-phase-sync", title: "Phase Sync", series: "connection", equation: "dθ/dt = ω + K sin(θ₂ - θ₁)", description: "The Kuramoto model of phase synchronization — oscillators that gradually align their rhythms.", emotionalNote: "The moment two separate rhythms find the same beat", background: "#0A0A12", imageUrl: "/prints/connection/connection_phase_sync.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "connection-torus-knot", title: "Torus Knot", series: "connection", equation: "r(t) = ((R + r cos qt) cos pt, ...)", description: "A curve that winds around a torus — topologically, it cannot be untied without cutting.", emotionalNote: "A bond that cannot be undone without breaking the topology", background: "#0A0A12", imageUrl: "/prints/connection/connection_torus_knot.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "connection-two-body", title: "Two Body", series: "connection", equation: "F = -Gm₁m₂/r² · r̂", description: "The gravitational two-body problem — two masses orbiting their common center. Each shapes the other's path.", emotionalNote: "Two masses shaping each other's orbits", background: "#0A0A12", imageUrl: "/prints/connection/connection_two_body.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-connection-bundle",
    bundlePrice: 82,
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
      { id: "tension-buckling", title: "Buckling", series: "tension", equation: "P_cr = π²EI / (KL)²", description: "Euler's critical load — the exact force at which a column buckles. Below this threshold, perfectly stable. At this threshold, catastrophic failure.", emotionalNote: "The exact threshold between holding and collapse", background: "#1A1A1A", imageUrl: "/prints/tension/tension_buckling.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "tension-fracture", title: "Fracture", series: "tension", equation: "σ = Eε (until σ > σ_y)", description: "Hooke's law pushed past the yield point — the linear relationship that holds perfectly until it doesn't.", emotionalNote: "The invisible line between bending and breaking", background: "#1A1A1A", imageUrl: "/prints/tension/tension_fracture.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "tension-interference", title: "Interference", series: "tension", equation: "A(x) = A₁sin(k₁x) + A₂sin(k₂x)", description: "Two wave sources creating an interference pattern — peaks where the waves align, silence where they cancel.", emotionalNote: "Where two forces meet, they either amplify or annihilate", background: "#1A1A1A", imageUrl: "/prints/tension/tension_interference.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "tension-opposition", title: "Opposition", series: "tension", equation: "F_net = F₁ - F₂ = 0, |F₁| > 0", description: "Equal and opposite forces in perfect balance — the net force is zero, but the internal stress is immense.", emotionalNote: "Perfect balance is not peace — it is maximum contained force", background: "#1A1A1A", imageUrl: "/prints/tension/tension_opposition.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "tension-torsion", title: "Torsion", series: "tension", equation: "τ = Tr/J", description: "The shear stress in a twisted shaft — maximum at the surface, zero at the center.", emotionalNote: "The outside holds all the strain while the center feels nothing", background: "#1A1A1A", imageUrl: "/prints/tension/tension_torsion.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-tension-bundle",
    bundlePrice: 82,
  },

  // ── OVERWHELM ───────────────────────────────────────────
  {
    id: "overwhelm",
    name: "OVERWHELM",
    emotion: "too much, saturation, systems past capacity",
    tagline: "Twelve harmonics, eight wave sources, twenty-two parallel streams. Each coherent alone. Together, unresolvable.",
    description: "Multiple simultaneous systems rendered together — strange attractors, Kuramoto synchronization, Lévy flights, phase floods, and turbulent flow. The density is the overwhelm.",
    story: "Overwhelm is not confusion. Each individual signal is clear. The problem is that there are too many of them. This series renders dozens of simultaneous mathematical systems in the same visual field. The palette uses the full spectrum because overwhelm does not discriminate.",
    mathematicalPrimitive: "multi-system superposition, turbulence, swarm dynamics",
    background: "#0A0A12",
    palette: ["#E84040", "#40A0E8", "#E8D040", "#40E888", "#D040E8", "#E88040", "#4060E8", "#A0E840", "#E840A0", "#40E8D0"],
    makingOf: "91 renders. 5 survived.",
    pieces: [
      { id: "overwhelm-attractors", title: "Attractors", series: "overwhelm", equation: "dx/dt = σ(y-x), dy/dt = x(ρ-z)-y", description: "Multiple Lorenz attractors rendered simultaneously — each following its own deterministic chaos.", emotionalNote: "Every path is determined, but together they are unreadable", background: "#0A0A12", imageUrl: "/prints/overwhelm/overwhelm_attractors.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "overwhelm-kuramoto", title: "Kuramoto", series: "overwhelm", equation: "dθᵢ/dt = ωᵢ + (K/N)Σsin(θⱼ - θᵢ)", description: "The Kuramoto model with dozens of oscillators — each trying to synchronize, none fully succeeding.", emotionalNote: "Dozens of rhythms trying and failing to align", background: "#0A0A12", imageUrl: "/prints/overwhelm/overwhelm_kuramoto.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "overwhelm-levy-swarm", title: "Levy Swarm", series: "overwhelm", equation: "P(x) ~ |x|^{-1-α}, 0 < α < 2", description: "A swarm of Lévy flights — heavy-tailed random walks with occasional enormous jumps.", emotionalNote: "Random motion that refuses to stay bounded", background: "#0A0A12", imageUrl: "/prints/overwhelm/overwhelm_levy_swarm.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "overwhelm-phase-flood", title: "Phase Flood", series: "overwhelm", equation: "ψ(x,t) = Σ Aₙ e^{i(kₙx - ωₙt + φₙ)}", description: "Dozens of complex wave functions superposed — the resulting field is everywhere nonzero and nowhere still.", emotionalNote: "Every point in space vibrating from every direction at once", background: "#0A0A12", imageUrl: "/prints/overwhelm/overwhelm_phase_flood.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "overwhelm-turbulence", title: "Turbulence", series: "overwhelm", equation: "Re = ρvL/μ >> Re_cr", description: "Fluid flow past the critical Reynolds number — order becomes chaos through a cascade of instabilities.", emotionalNote: "Order dissolving into chaos at every scale simultaneously", background: "#0A0A12", imageUrl: "/prints/overwhelm/overwhelm_turbulence.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-overwhelm-bundle",
    bundlePrice: 82,
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
      { id: "grief-heat-diffusion", title: "Heat Diffusion", series: "grief", equation: "∂u/∂t = α∇²u", description: "The heat equation — temperature spreading until everything reaches equilibrium. The initial intensity diffuses outward, flattening.", emotionalNote: "Intensity that spreads thinner until it becomes ambient", background: "#DDD9D2", imageUrl: "/prints/grief/grief_heat_diffusion.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "grief-heaviside-cascade", title: "Heaviside Cascade", series: "grief", equation: "H(t - t₀) = {0, t < t₀; 1, t ≥ t₀}", description: "A cascade of Heaviside step functions — each one a sudden drop, a new absence.", emotionalNote: "Loss arriving in discrete collapses, each one a new floor", background: "#DDD9D2", imageUrl: "/prints/grief/grief_heaviside_cascade.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "grief-spectral-erosion", title: "Spectral Erosion", series: "grief", equation: "S(f,t) = S₀(f) · e^{-γ(f)t}", description: "A frequency spectrum losing its higher harmonics over time — detail fading, leaving only the essential tone.", emotionalNote: "The richness of memory eroding to a single tone", background: "#DDD9D2", imageUrl: "/prints/grief/grief_spectral_erosion.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "grief-void", title: "Void", series: "grief", equation: "∫∫ ρ(x,y) dA → 0", description: "A density field collapsing toward emptiness — the mathematical description of a space that used to contain something.", emotionalNote: "The shape of what used to be there", background: "#DDD9D2", imageUrl: "/prints/grief/grief_void.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "grief-weight", title: "Weight", series: "grief", equation: "F = mg, m(t) = m₀(1 - e^{-t/τ})", description: "A mass that increases with time — the weight of grief that grows heavier before the exponential saturation levels it.", emotionalNote: "The weight that arrives slowly and saturates", background: "#DDD9D2", imageUrl: "/prints/grief/grief_weight.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-grief-bundle",
    bundlePrice: 82,
  },

  // ── GROWTH ──────────────────────────────────────────────
  {
    id: "growth",
    name: "GROWTH",
    emotion: "emergence, branching, reaching toward light",
    tagline: "L-system branching at thirteen levels. Golden spirals tiling the plane. Thirty-four lines reaching toward light.",
    description: "Bifurcation diagrams, dendritic growth, Lissajous blooms, logistic cascades, and reaction-diffusion patterns. Growth is not linear — it is fractal.",
    story: "Growth follows rules. The branching of trees obeys L-system grammars. The spiral of a nautilus follows the golden ratio. Reaction-diffusion systems create the spots on leopards and the stripes on zebrafish. This series renders these growth algorithms as minimalist art.",
    mathematicalPrimitive: "L-systems, bifurcation, reaction-diffusion, logistic maps",
    background: "#F5F0E6",
    palette: ["#1A4D2E", "#2E8B4A", "#6BBF6E", "#A8D86E", "#E8D878"],
    makingOf: "140 renders. 5 survived.",
    pieces: [
      { id: "growth-bifurcation", title: "Bifurcation", series: "growth", equation: "x_{n+1} = rx_n(1 - x_n), r ∈ [2.5, 4]", description: "The logistic map's bifurcation diagram read as a growth narrative — a single strategy splitting into increasing complexity.", emotionalNote: "Simple beginnings branching into irreducible complexity", background: "#F5F0E6", imageUrl: "/prints/growth/growth_bifurcation.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "growth-dendrite", title: "Dendrite", series: "growth", equation: "L → F[+L][-L]FL", description: "An L-system rendering dendritic branching — recursive grammar producing infinite complexity from simple rules.", emotionalNote: "The same rule applied at every scale, forever branching", background: "#F5F0E6", imageUrl: "/prints/growth/growth_dendrite.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "growth-lissajous-bloom", title: "Lissajous Bloom", series: "growth", equation: "x = A sin(at + δ), y = B sin(bt)", description: "Lissajous curves with slowly evolving parameters — the figure blooming outward as the frequency ratio shifts.", emotionalNote: "Oscillation that opens outward like a flower", background: "#F5F0E6", imageUrl: "/prints/growth/growth_lissajous_bloom.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "growth-logistic-cascade", title: "Logistic Cascade", series: "growth", equation: "dN/dt = rN(1 - N/K)", description: "The logistic growth equation — population expanding rapidly, then slowing as it approaches carrying capacity.", emotionalNote: "Rapid expansion learning to respect its own limits", background: "#F5F0E6", imageUrl: "/prints/growth/growth_logistic_cascade.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "growth-reaction-diffusion", title: "Reaction Diffusion", series: "growth", equation: "∂u/∂t = Dᵤ∇²u + f(u,v)", description: "A Turing reaction-diffusion system — two chemicals diffusing at different rates, creating spontaneous pattern.", emotionalNote: "Pattern emerging from nothing but diffusion and reaction", background: "#F5F0E6", imageUrl: "/prints/growth/growth_reaction_diffusion.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-growth-bundle",
    bundlePrice: 82,
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
    background: "#E8E4DA",
    palette: ["#4A6B8A", "#6B8BAA", "#8AABCA", "#3A5B7A", "#2A4B6A"],
    makingOf: "55 renders. 5 survived.",
    pieces: [
      { id: "cycles-loom", title: "Loom", series: "cycles", equation: "x(t) = x(t + T), T = 2π/ω", description: "Periodic trajectories woven together — threads that repeat at exact intervals, creating fabric from rhythm.", emotionalNote: "Threads that return to the same place and weave something new", background: "#E8E4DA", imageUrl: "/prints/cycles/cycles_loom.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "cycles-moebius", title: "Moebius", series: "cycles", equation: "r(t) = ((2 + cos(t/2))cos t, (2 + cos(t/2))sin t, sin(t/2))", description: "The Möbius strip — a surface with only one side. You must traverse it twice to return to where you started.", emotionalNote: "A loop that requires two passes to complete", background: "#E8E4DA", imageUrl: "/prints/cycles/cycles_moebius.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "cycles-orbit", title: "Orbit", series: "cycles", equation: "r(θ) = a(1-e²)/(1 + e cos θ)", description: "Kepler's orbital equation — the ellipse traced by every planet. Always returning, never arriving.", emotionalNote: "Always returning, never arriving", background: "#E8E4DA", imageUrl: "/prints/cycles/cycles_orbit.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "cycles-phase-portrait", title: "Phase Portrait", series: "cycles", equation: "ẋ = f(x,y), ẏ = g(x,y)", description: "The phase portrait of a dynamical system — every possible trajectory drawn in the same plane. Closed curves are the cycles.", emotionalNote: "Every possible future drawn at once", background: "#E8E4DA", imageUrl: "/prints/cycles/cycles_phase_portrait.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "cycles-recurrence", title: "Recurrence", series: "cycles", equation: "R(i,j) = Θ(ε - ||x_i - x_j||)", description: "A recurrence plot — marking every moment a system returns close to a previous state. The dark bands reveal hidden periodicity.", emotionalNote: "Every moment the past returns close enough to recognize", background: "#E8E4DA", imageUrl: "/prints/cycles/cycles_recurrence.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-cycles-bundle",
    bundlePrice: 82,
  },

  // ── CONFUSION ───────────────────────────────────────────
  {
    id: "confusion",
    name: "CONFUSION",
    emotion: "disorientation, tangling, loss of clarity",
    tagline: "Aliased signals, impossible knots, labyrinths with no exit. The geometry of not knowing which way is forward.",
    description: "Aliased signals, topological knots, labyrinths, tangles, and vertigo spirals. Systems that fold back on themselves until the path forward becomes invisible.",
    story: "Confusion is not ignorance. It is the state of having too many valid interpretations. Aliasing occurs when a signal is sampled too slowly — the true frequency becomes indistinguishable from a false one. This series renders that ambiguity as visual structure.",
    mathematicalPrimitive: "aliasing, topological knots, labyrinth generation, tangled trajectories",
    background: "#E6E2DC",
    palette: ["#8A7A6A", "#6A8A7A", "#7A6A8A", "#9A8A7A", "#6A7A8A"],
    makingOf: "52 renders. 5 survived.",
    pieces: [
      { id: "confusion-aliased", title: "Aliased", series: "confusion", equation: "f_alias = |f - n·f_s|, n = round(f/f_s)", description: "A signal sampled below the Nyquist rate — the true frequency becomes indistinguishable from its aliases.", emotionalNote: "When the truth and its reflections become indistinguishable", background: "#E6E2DC", imageUrl: "/prints/confusion/confusion_aliased.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "confusion-knot", title: "Knot", series: "confusion", equation: "K: S¹ → S³", description: "A topological knot — a closed curve in three-dimensional space that cannot be untangled without cutting.", emotionalNote: "A path that crosses itself until the beginning is lost", background: "#E6E2DC", imageUrl: "/prints/confusion/confusion_knot.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "confusion-labyrinth", title: "Labyrinth", series: "confusion", equation: "maze(x,y) = {0,1} | ∃! path(start, end)", description: "A generated labyrinth with exactly one solution — the path exists, but finding it requires exhaustive search.", emotionalNote: "The solution exists but cannot be seen from inside", background: "#E6E2DC", imageUrl: "/prints/confusion/confusion_labyrinth.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "confusion-tangle", title: "Tangle", series: "confusion", equation: "γ(t): [0,1] → R³, self-intersecting", description: "Multiple space curves that intersect and interleave — each individually traceable, together inseparable.", emotionalNote: "Individually clear, collectively inseparable", background: "#E6E2DC", imageUrl: "/prints/confusion/confusion_tangle.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "confusion-vertigo", title: "Vertigo", series: "confusion", equation: "r(t) = e^{-at}(cos ωt, sin ωt, t)", description: "A spiral that simultaneously ascends and decays — the visual field tilts until orientation is lost.", emotionalNote: "The spiral that makes the ground uncertain", background: "#E6E2DC", imageUrl: "/prints/confusion/confusion_vertigo.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-confusion-bundle",
    bundlePrice: 82,
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
      { id: "shame-contraction", title: "Contraction", series: "shame", equation: "T(x) : ||T(x)-T(y)|| < ||x-y||", description: "A contraction mapping — every iteration brings all points closer together. The fixed point is inevitable.", emotionalNote: "Collapsing toward a point that cannot be avoided", background: "#E0DCE4", imageUrl: "/prints/shame/shame_contraction.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "shame-crumple", title: "Crumple", series: "shame", equation: "κ(s) → ∞ at fold lines", description: "A smooth surface developing infinite curvature at fold lines — the geometry of crumpling paper.", emotionalNote: "Smoothness collapsing into sharp, irreversible folds", background: "#E0DCE4", imageUrl: "/prints/shame/shame_crumple.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "shame-fold", title: "Fold", series: "shame", equation: "f(x) = f(−x), x → 0", description: "A function folding onto itself — the two halves meeting and collapsing the space between them.", emotionalNote: "Folding inward until the outside is hidden", background: "#E0DCE4", imageUrl: "/prints/shame/shame_fold.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "shame-shrink", title: "Shrink", series: "shame", equation: "A(t) = A₀ · e^{-λt}", description: "An envelope that decays exponentially — the amplitude shrinking until the signal becomes invisible.", emotionalNote: "Making yourself smaller until you disappear", background: "#E0DCE4", imageUrl: "/prints/shame/shame_shrink.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "shame-veil", title: "Veil", series: "shame", equation: "f(x) = f(x) · (1 - g(x))", description: "A function multiplied by its own complement — the signal masking itself, hiding behind its own structure.", emotionalNote: "Hiding behind the structure of what you are", background: "#E0DCE4", imageUrl: "/prints/shame/shame_veil.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-shame-bundle",
    bundlePrice: 82,
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
    background: "#E8ECF0",
    palette: ["#4A6078", "#607890", "#7890A8", "#3A5068", "#2A4058"],
    makingOf: "36 renders. 5 survived.",
    pieces: [
      { id: "solitude-echo", title: "Echo", series: "solitude", equation: "f(t - τ) · α^n, α < 1", description: "A signal repeating with decay — each echo quieter than the last, the space between them growing.", emotionalNote: "A voice returning quieter each time", background: "#E8ECF0", imageUrl: "/prints/solitude/solitude_echo.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "solitude-footprints", title: "Footprints", series: "solitude", equation: "δ(x - x_n), n = 1,2,...,N", description: "A sequence of Dirac deltas — discrete points along a path. Presence marked, then left behind.", emotionalNote: "Evidence of passage through an empty field", background: "#E8ECF0", imageUrl: "/prints/solitude/solitude_footprints.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "solitude-island", title: "Island", series: "solitude", equation: "Ω = {x : f(x) > 0} ⊂ R², |∂Ω| < ∞", description: "A compact region surrounded by zero — an island of nonzero values in an infinite plane of nothing.", emotionalNote: "The only nonzero region in an infinite plane", background: "#E8ECF0", imageUrl: "/prints/solitude/solitude_island.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "solitude-lighthouse", title: "Lighthouse", series: "solitude", equation: "I(r) = I₀/r² · rect(θ/Δθ)", description: "A single directional source — intensity falling off with the square of distance, sweeping through darkness.", emotionalNote: "One source of light sweeping an infinite dark", background: "#E8ECF0", imageUrl: "/prints/solitude/solitude_lighthouse.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "solitude-wanderer", title: "Wanderer", series: "solitude", equation: "x(t) = x₀ + ∫₀ᵗ v(s)ds, v random", description: "A single random walk in an empty plane — no other walkers, no boundaries, no destination.", emotionalNote: "A single path with nowhere it needs to be", background: "#E8ECF0", imageUrl: "/prints/solitude/solitude_wanderer.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-solitude-bundle",
    bundlePrice: 82,
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
    makingOf: "48 renders. 5 survived.",
    pieces: [
      { id: "nostalgia-carousel", title: "Carousel", series: "nostalgia", equation: "r(t) = R · e^{iωt}, ω → 0", description: "Circular motion slowing to a stop — the carousel winding down, each revolution slower than the last.", emotionalNote: "Going around one more time, slower each pass", background: "#F0E8D8", imageUrl: "/prints/nostalgia/nostalgia_carousel.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "nostalgia-daguerreotype", title: "Daguerreotype", series: "nostalgia", equation: "I(x,y,t) = I₀(x,y) · e^{-t/τ} + η(x,y)", description: "Image intensity decaying with time, noise accumulating — the mathematics of a photograph slowly disappearing.", emotionalNote: "An image slowly becoming its own ghost", background: "#F0E8D8", imageUrl: "/prints/nostalgia/nostalgia_daguerreotype.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "nostalgia-locket", title: "Locket", series: "nostalgia", equation: "f(x) = f₀(x) * g(σ), σ → ∞", description: "A signal convolved with an ever-widening Gaussian — the original sharpness blurring into soft warmth.", emotionalNote: "The edges of memory softening into warmth", background: "#F0E8D8", imageUrl: "/prints/nostalgia/nostalgia_locket.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "nostalgia-music-box", title: "Music Box", series: "nostalgia", equation: "x(t) = Σ Aₙe^{-γₙt}sin(nωt)", description: "Harmonic overtones decaying at different rates — the higher notes fade first, leaving only the fundamental.", emotionalNote: "The melody simplifying as the mechanism slows", background: "#F0E8D8", imageUrl: "/prints/nostalgia/nostalgia_music_box.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "nostalgia-remnant", title: "Remnant", series: "nostalgia", equation: "R(x) = lim_{t→∞} f(x,t)", description: "The asymptotic remainder — what survives after everything that can fade has faded.", emotionalNote: "What remains when everything else has faded", background: "#F0E8D8", imageUrl: "/prints/nostalgia/nostalgia_remnant.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-nostalgia-bundle",
    bundlePrice: 82,
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
    background: "#1A0A0A",
    palette: ["#D43030", "#E85020", "#F08030", "#C82020", "#FF6040"],
    makingOf: "58 renders. 5 survived.",
    pieces: [
      { id: "desire-eclipse", title: "Eclipse", series: "desire", equation: "I(r) = I₀ · (1 - disk(r/R))", description: "A luminous field occluded by a dark disk — the brightest ring appears at the boundary of what is hidden.", emotionalNote: "The brightest light at the edge of what you cannot see", background: "#1A0A0A", imageUrl: "/prints/desire/desire_eclipse.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "desire-flame", title: "Flame", series: "desire", equation: "∂T/∂t = α∇²T + Q(x,y)", description: "Advection-diffusion with a heat source — energy flowing upward, consuming and renewing.", emotionalNote: "Energy that consumes itself to stay alive", background: "#1A0A0A", imageUrl: "/prints/desire/desire_flame.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "desire-hunger", title: "Hunger", series: "desire", equation: "dN/dt = rN(1 - N/K) - aN/(1+bN)", description: "Predator-prey with Holling type II — consumption that saturates but never ceases.", emotionalNote: "Need that grows faster than it can be satisfied", background: "#1A0A0A", imageUrl: "/prints/desire/desire_hunger.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "desire-inspiral", title: "Inspiral", series: "desire", equation: "r(t) = r₀(1 - t/t_c)^{1/4}", description: "Gravitational wave inspiral — two masses spiraling closer, accelerating, radiating energy as they approach merger.", emotionalNote: "Accelerating toward something inevitable", background: "#1A0A0A", imageUrl: "/prints/desire/desire_inspiral.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "desire-pursuit", title: "Pursuit", series: "desire", equation: "dr/dt = v₁ · (r_target - r)/||r_target - r||", description: "The pursuit curve — always heading directly toward a moving target, the path curving but never arriving.", emotionalNote: "Always moving toward, never arriving", background: "#1A0A0A", imageUrl: "/prints/desire/desire_pursuit.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-desire-bundle",
    bundlePrice: 82,
  },

  // ── MELANCHOLY ──────────────────────────────────────────
  {
    id: "melancholy",
    name: "MELANCHOLY",
    emotion: "sadness without crisis, a low sustained tone",
    tagline: "Entropy increasing slowly. Drift without destination. The Lethe flowing at the speed of forgetting.",
    description: "Entropy fields, slow drift functions, elegiac decay, dissolution, and the river Lethe. Sadness that is not acute but ambient — a background hum of loss.",
    story: "Melancholy is not grief. Grief has an object. Melancholy is a state — a slow, pervasive sadness that colors everything without breaking anything. The mathematics of entropy describes this: systems that slowly lose order, not catastrophically, but inevitably.",
    mathematicalPrimitive: "entropy, drift, slow decay, dissolution",
    background: "#D8D4D0",
    palette: ["#708090", "#8090A0", "#6070A0", "#506080", "#405070"],
    makingOf: "61 renders. 5 survived.",
    pieces: [
      { id: "melancholy-dissolve", title: "Dissolve", series: "melancholy", equation: "c(t) = c₀ · e^{-kt}", description: "Concentration decaying in solution — the sharp definition of a substance spreading into homogeneous nothing.", emotionalNote: "Definition spreading until it becomes everything and nothing", background: "#D8D4D0", imageUrl: "/prints/melancholy/melancholy_dissolve.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "melancholy-drift", title: "Drift", series: "melancholy", equation: "dx = μdt + σdW", description: "Brownian motion with weak drift — a slow, purposeless migration. Direction exists but barely matters.", emotionalNote: "Movement without purpose, direction without urgency", background: "#D8D4D0", imageUrl: "/prints/melancholy/melancholy_drift.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "melancholy-elegy", title: "Elegy", series: "melancholy", equation: "f(t) = A · t^{-α}, α ∈ (0,1)", description: "Power-law decay — slower than exponential, the signal fades but refuses to vanish. A long, slow diminuendo.", emotionalNote: "Fading slower than grief, refusing to fully vanish", background: "#D8D4D0", imageUrl: "/prints/melancholy/melancholy_elegy.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "melancholy-entropy", title: "Entropy", series: "melancholy", equation: "S = -k Σ pᵢ ln pᵢ, dS/dt ≥ 0", description: "Shannon entropy increasing — the system slowly losing the information that once made it ordered.", emotionalNote: "Order slowly becoming indistinguishable from noise", background: "#D8D4D0", imageUrl: "/prints/melancholy/melancholy_entropy.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "melancholy-lethe", title: "Lethe", series: "melancholy", equation: "∂c/∂t + v·∇c = D∇²c", description: "Advection-diffusion in a slow river — the substance carried downstream and dispersed. Named for the river of forgetting.", emotionalNote: "The slow current that carries memory away", background: "#D8D4D0", imageUrl: "/prints/melancholy/melancholy_lethe.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-melancholy-bundle",
    bundlePrice: 82,
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
    palette: ["#A09888", "#B8B0A0", "#908878", "#C8C0B0", "#787068"],
    makingOf: "39 renders. 5 survived.",
    pieces: [
      { id: "surrender-dissolution", title: "Dissolution", series: "surrender", equation: "dm/dt = -kA(c_s - c)", description: "The Noyes-Whitney equation — a solid dissolving into solution. The rate depends on the gap between what is and what could be.", emotionalNote: "The boundary between solid and dissolved, crossing willingly", background: "#E4E0DC", imageUrl: "/prints/surrender/surrender_dissolution.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "surrender-flow", title: "Flow", series: "surrender", equation: "∇·v = 0, Re << 1", description: "Stokes flow — fluid so viscous that inertia is irrelevant. The system does not resist. It flows.", emotionalNote: "Motion without resistance, form without friction", background: "#E4E0DC", imageUrl: "/prints/surrender/surrender_flow.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "surrender-melt", title: "Melt", series: "surrender", equation: "ρL(ds/dt) = k(∂T/∂n)", description: "The Stefan condition — the moving boundary of a melting solid. Form yielding to heat, releasing its structure.", emotionalNote: "Structure releasing itself to become something else", background: "#E4E0DC", imageUrl: "/prints/surrender/surrender_melt.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "surrender-settle", title: "Settle", series: "surrender", equation: "v_t = (2r²(ρ_p - ρ_f)g)/(9μ)", description: "Stokes' settling law — a particle finding its terminal velocity. No longer accelerating. Just falling.", emotionalNote: "The moment resistance stops and gravity completes the work", background: "#E4E0DC", imageUrl: "/prints/surrender/surrender_settle.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "surrender-shed", title: "Shed", series: "surrender", equation: "f(t) = f₀ · H(t₀ - t)", description: "A Heaviside function in reverse — present and then absent. The clean release of what was held.", emotionalNote: "The clean release of what was held", background: "#E4E0DC", imageUrl: "/prints/surrender/surrender_shed.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-surrender-bundle",
    bundlePrice: 82,
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
      { id: "wonder-apollonian-gasket", title: "Apollonian Gasket", series: "wonder", equation: "(k₁+k₂+k₃+k₄)² = 2(k₁²+k₂²+k₃²+k₄²)", description: "Descartes' Circle Theorem iterated — circles packed inside circles, the gaps filled to infinity.", emotionalNote: "Infinity nested inside a finite space", background: "#0A0A18", imageUrl: "/prints/wonder/wonder_apollonian_gasket.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "wonder-harmonograph", title: "Harmonograph", series: "wonder", equation: "x = A₁sin(f₁t+φ₁)e^{-d₁t} + A₂sin(f₂t+φ₂)e^{-d₂t}", description: "Two damped pendulums coupled by a drawing surface — the pattern emerges from the interaction of decay rates.", emotionalNote: "Beauty emerging from the interaction of simple motions", background: "#0A0A18", imageUrl: "/prints/wonder/wonder_harmonograph.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "wonder-mandelbrot-orbit", title: "Mandelbrot Orbit", series: "wonder", equation: "z_{n+1} = z_n² + c", description: "Individual orbits of the Mandelbrot iteration — not the set boundary, but the trajectories themselves.", emotionalNote: "The invisible paths that define the boundary of chaos", background: "#0A0A18", imageUrl: "/prints/wonder/wonder_mandelbrot_orbit.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "wonder-recursion", title: "Recursion", series: "wonder", equation: "f(n) = f(f(n-1))", description: "A function that calls itself — each level of depth revealing new structure, the whole containing copies of itself.", emotionalNote: "The whole containing copies of itself at every scale", background: "#0A0A18", imageUrl: "/prints/wonder/wonder_recursion.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "wonder-strange-attractor", title: "Strange Attractor", series: "wonder", equation: "dx/dt = σ(y-x), dy/dt = x(ρ-z)-y, dz/dt = xy-βz", description: "The Lorenz attractor — deterministic chaos that never repeats but always stays on the same manifold.", emotionalNote: "Infinite complexity within a bounded space", background: "#0A0A18", imageUrl: "/prints/wonder/wonder_strange_attractor.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-wonder-bundle",
    bundlePrice: 82,
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
    makingOf: "41 renders. 5 survived.",
    pieces: [
      { id: "peace-cloud", title: "Cloud", series: "peace", equation: "∂ρ/∂t = 0, ∇·(ρv) = 0", description: "A density field at steady state — no longer changing, no longer flowing. Present and still.", emotionalNote: "The moment everything stops moving and simply exists", background: "#F0EDE8", imageUrl: "/prints/peace/peace_cloud.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "peace-resolved", title: "Resolved", series: "peace", equation: "∇²f = 0", description: "The Laplace equation — every point is the average of its neighbors. No tension, no gradient. Pure equilibrium.", emotionalNote: "Every point in agreement with its surroundings", background: "#F0EDE8", imageUrl: "/prints/peace/peace_resolved.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "peace-sand", title: "Sand", series: "peace", equation: "∂h/∂t = ν∇²h - λ(∇h)² + η", description: "The KPZ equation at steady state — a surface shaped by deposition and smoothing. The final form the landscape was always becoming.", emotionalNote: "The shape the surface was always becoming", background: "#F0EDE8", imageUrl: "/prints/peace/peace_sand.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "peace-settled", title: "Settled", series: "peace", equation: "v(t) → 0, x(t) → x_eq", description: "A damped system at rest — velocity approaching zero, position approaching equilibrium. The oscillations have ended.", emotionalNote: "The oscillations have ended. Only stillness remains.", background: "#F0EDE8", imageUrl: "/prints/peace/peace_settled.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "peace-zen-garden", title: "Zen Garden", series: "peace", equation: "ψ = A · sin(kx) · sin(ky)", description: "Standing wave pattern in two dimensions — a fixed geometry of nodes and antinodes. Nothing moves. Everything vibrates.", emotionalNote: "Perfect stillness made of perfect vibration", background: "#F0EDE8", imageUrl: "/prints/peace/peace_zen_garden.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-peace-bundle",
    bundlePrice: 82,
  },

  // ── AWE ─────────────────────────────────────────────────
  {
    id: "awe",
    name: "AWE",
    emotion: "overwhelmed by scale, the sublime",
    tagline: "Cathedral proportions. Chladni patterns appearing from vibration. Singularities where the mathematics breaks down.",
    description: "Cathedral geometry, Chladni plate patterns, monolithic forms, radiance functions, and singularity fields. Mathematics that evokes the experience of standing before something immeasurably larger than yourself.",
    story: "Awe is the emotion at the boundary of comprehension. The mathematics of awe involves scale — functions that span orders of magnitude, patterns that emerge from seemingly nothing, singularities where the rules change. This series renders those boundary experiences.",
    mathematicalPrimitive: "scale invariance, Chladni patterns, singularity, radiance",
    background: "#0A0A10",
    palette: ["#D0B080", "#E0C898", "#C0A070", "#F0D8A8", "#B09060"],
    makingOf: "65 renders. 5 survived.",
    pieces: [
      { id: "awe-cathedral", title: "Cathedral", series: "awe", equation: "h(x) = Σ Aₙ sin(nπx/L), n → ∞", description: "Fourier series converging to a gothic arch — infinite harmonics summing to create a single soaring form.", emotionalNote: "Infinite harmonics summing to create one soaring form", background: "#0A0A10", imageUrl: "/prints/awe/awe_cathedral.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "awe-chladni", title: "Chladni", series: "awe", equation: "∇⁴w - k⁴w = 0", description: "Chladni plate vibration patterns — sand collecting at the nodal lines, revealing the invisible geometry of sound.", emotionalNote: "The invisible structure of sound made visible", background: "#0A0A10", imageUrl: "/prints/awe/awe_chladni.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "awe-monolith", title: "Monolith", series: "awe", equation: "f(x,y) = H(x-a)H(b-x)H(y-c)H(d-y)", description: "A rectangular indicator function — mathematically simple, visually absolute. A form that simply is.", emotionalNote: "A form so simple it becomes absolute", background: "#0A0A10", imageUrl: "/prints/awe/awe_monolith.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "awe-radiance", title: "Radiance", series: "awe", equation: "L(x,ω) = Lₑ + ∫ f_r L_i cos θ dω", description: "The rendering equation — the complete mathematical description of how light fills a space.", emotionalNote: "The complete mathematics of how light fills a space", background: "#0A0A10", imageUrl: "/prints/awe/awe_radiance.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "awe-singularity", title: "Singularity", series: "awe", equation: "f(z) = 1/(z-z₀)ⁿ, n ≥ 1", description: "A pole in the complex plane — the function approaches infinity, the rules change, and everything organizes around the singularity.", emotionalNote: "The point where the mathematics breaks down and reorganizes everything", background: "#0A0A10", imageUrl: "/prints/awe/awe_singularity.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-awe-bundle",
    bundlePrice: 82,
  },

  // ── ENVY ────────────────────────────────────────────────
  {
    id: "envy",
    name: "ENVY",
    emotion: "comparison, mirroring, the distance between you and them",
    tagline: "Mirror functions. Glass ceilings at y = c. Shadow projections of brighter forms.",
    description: "Mirror reflections, barrier functions, shadow projections, covetous proximity curves, and surveillance geometry. The mathematics of watching something you cannot have.",
    story: "Envy is a function of distance — not physical distance, but the gap between what you are and what you see someone else being. It requires a mirror: you must be able to see the comparison clearly. This series renders that geometry of comparison.",
    mathematicalPrimitive: "reflection, barrier functions, projection, proximity",
    background: "#0C1A0C",
    palette: ["#40A040", "#308030", "#50C050", "#206020", "#60E060"],
    makingOf: "40 renders. 5 survived.",
    pieces: [
      { id: "envy-covet", title: "Covet", series: "envy", equation: "d(x, S) = inf{||x-s|| : s ∈ S}", description: "The distance function to a set — measuring the gap between where you are and where you want to be.", emotionalNote: "The exact measure of the gap between here and there", background: "#0C1A0C", imageUrl: "/prints/envy/envy_covet.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "envy-glass-ceiling", title: "Glass Ceiling", series: "envy", equation: "f(x) = min(g(x), c)", description: "A function clamped at a ceiling — growth permitted to a point, then truncated. The barrier is invisible from below.", emotionalNote: "Growing freely until you hit the invisible barrier", background: "#0C1A0C", imageUrl: "/prints/envy/envy_glass_ceiling.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "envy-mirror", title: "Mirror", series: "envy", equation: "f(-x) = f(x)", description: "A function reflected across an axis — the same form, reversed. Everything you see is yourself, inverted.", emotionalNote: "Everything you see in them is yourself, reversed", background: "#0C1A0C", imageUrl: "/prints/envy/envy_mirror.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "envy-shadow", title: "Shadow", series: "envy", equation: "P(x) = x - (x·n̂)n̂", description: "Orthogonal projection — the shadow cast by a higher-dimensional object onto a lower plane. Always less than the original.", emotionalNote: "A flattened version of something that exists in more dimensions", background: "#0C1A0C", imageUrl: "/prints/envy/envy_shadow.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "envy-watch", title: "Watch", series: "envy", equation: "θ(t) = arctan(y(t)/x(t))", description: "An angle function tracking a moving point — the geometry of surveillance, of eyes that follow.", emotionalNote: "The angle that always points toward what you're watching", background: "#0C1A0C", imageUrl: "/prints/envy/envy_watch.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-envy-bundle",
    bundlePrice: 82,
  },

  // ── RAGE ────────────────────────────────────────────────
  {
    id: "rage",
    name: "RAGE",
    emotion: "explosive force, destruction, uncontained energy",
    tagline: "Detonation wavefronts. Shockwave propagation. Systems that exceed every boundary at once.",
    description: "Detonation physics, shockwave propagation, chaotic bursts, shattering dynamics, and eruption mechanics. Energy that has exceeded all containment.",
    story: "Rage is energy without containment. The mathematics of explosion — detonation waves, shock fronts, energy release rates — describe systems where the internal pressure exceeds every boundary simultaneously. This series renders that moment of total release.",
    mathematicalPrimitive: "detonation, shockwave, energy release, chaotic burst",
    background: "#1A0A0A",
    palette: ["#E82020", "#FF4040", "#FF6010", "#CC1010", "#FF8030"],
    makingOf: "42 renders. 5 survived.",
    pieces: [
      { id: "rage-chaos", title: "Chaos", series: "rage", equation: "x_{n+1} = 4x_n(1-x_n)", description: "The logistic map at r=4 — fully chaotic. Every initial condition leads to a completely unpredictable trajectory.", emotionalNote: "Every path leads to complete unpredictability", background: "#1A0A0A", imageUrl: "/prints/rage/rage_chaos.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "rage-detonation", title: "Detonation", series: "rage", equation: "D = √(2(γ²-1)q)", description: "The Chapman-Jouguet detonation velocity — the minimum speed at which a detonation wave can propagate.", emotionalNote: "The minimum speed of total destruction", background: "#1A0A0A", imageUrl: "/prints/rage/rage_detonation.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "rage-eruption", title: "Eruption", series: "rage", equation: "p(z) = ρgz + p₀, p > p_yield", description: "Pressure exceeding yield strength — the magma chamber equation. Containment fails. Everything comes up.", emotionalNote: "Pressure that has exceeded every possible containment", background: "#1A0A0A", imageUrl: "/prints/rage/rage_eruption.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "rage-shatter", title: "Shatter", series: "rage", equation: "E_release > Σ G_c · A_crack", description: "Griffith fracture — when the energy available exceeds the surface energy of all possible cracks simultaneously.", emotionalNote: "Energy exceeding every crack surface at once", background: "#1A0A0A", imageUrl: "/prints/rage/rage_shatter.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "rage-shockwave", title: "Shockwave", series: "rage", equation: "v > c, M = v/c >> 1", description: "Motion faster than the medium can communicate — the Mach cone. The wave arrives before the warning.", emotionalNote: "The wave arriving before the warning", background: "#1A0A0A", imageUrl: "/prints/rage/rage_shockwave.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-rage-bundle",
    bundlePrice: 82,
  },

  // ── JOY ─────────────────────────────────────────────────
  {
    id: "joy",
    name: "JOY",
    emotion: "radiance, expansion, light from the center",
    tagline: "Sunburst functions. Confetti scatter. Lissajous curves in perfect bloom.",
    description: "Sunburst radiation, confetti scatter distributions, Lissajous blooms, pinwheel symmetry, and bloom functions. Energy radiating outward from a center.",
    story: "Joy is centrifugal — it radiates outward. The mathematics of radiation, scatter, and bloom describe systems that expand from a center with no resistance. Light. Confetti. Fireworks. This series captures the geometry of feeling that goes outward.",
    mathematicalPrimitive: "radial expansion, scatter distributions, symmetric bloom",
    background: "#FFFCF0",
    palette: ["#E8A020", "#F0C040", "#E06030", "#D04080", "#40A0D0"],
    makingOf: "45 renders. 5 survived.",
    pieces: [
      { id: "joy-bloom", title: "Bloom", series: "joy", equation: "r(θ) = a + b·cos(nθ), a > b", description: "A rose curve expanding — petals opening as the amplitude grows. The geometry of blooming.", emotionalNote: "Petals opening without hesitation", background: "#FFFCF0", imageUrl: "/prints/joy/joy_bloom.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "joy-confetti", title: "Confetti", series: "joy", equation: "P(x,y) ~ Uniform(Ω), N >> 1", description: "Uniform random scatter — every point equally likely, no clustering, no preference. Pure equiprobable celebration.", emotionalNote: "Every point equally likely, the mathematics of celebration", background: "#FFFCF0", imageUrl: "/prints/joy/joy_confetti.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "joy-lissajous", title: "Lissajous", series: "joy", equation: "x = sin(3t), y = sin(4t)", description: "A Lissajous figure at a 3:4 frequency ratio — the closed curve of two harmonics in perfect relationship.", emotionalNote: "Two harmonics dancing in perfect ratio", background: "#FFFCF0", imageUrl: "/prints/joy/joy_lissajous.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "joy-pinwheel", title: "Pinwheel", series: "joy", equation: "f(r,θ) = cos(nθ + αr)", description: "A spiral pinwheel — rotational symmetry with radial twist. The pattern spins without effort.", emotionalNote: "Spinning without friction, turning without effort", background: "#FFFCF0", imageUrl: "/prints/joy/joy_pinwheel.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "joy-sunburst", title: "Sunburst", series: "joy", equation: "I(r,θ) = I₀ · (1/r) · Σ δ(θ - 2πn/N)", description: "Radial intensity along N directions — light streaming outward from a center in equal measure.", emotionalNote: "Light streaming outward in every direction equally", background: "#FFFCF0", imageUrl: "/prints/joy/joy_sunburst.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-joy-bundle",
    bundlePrice: 82,
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
      { id: "resilience-forged", title: "Forged", series: "resilience", equation: "σ_y(ε) = σ₀ + Kε^n", description: "Strain hardening — material that becomes stronger each time it is deformed. The yield point increases with every blow.", emotionalNote: "Becoming stronger at the point of each deformation", background: "#E8E0D8", imageUrl: "/prints/resilience/resilience_forged.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "resilience-growth", title: "Growth", series: "resilience", equation: "dN/dt = r(K' - N), K' > K", description: "Post-traumatic growth — recovery to a new carrying capacity higher than the original.", emotionalNote: "Growing back past the original capacity", background: "#E8E0D8", imageUrl: "/prints/resilience/resilience_growth.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "resilience-phoenix", title: "Phoenix", series: "resilience", equation: "f(t) = A(1 - e^{-t/τ₁})e^{t/τ₂}, τ₂ > τ₁", description: "An exponential recovery that exceeds the initial value — the function rises past where it began.", emotionalNote: "Rising past where you began", background: "#E8E0D8", imageUrl: "/prints/resilience/resilience_phoenix.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "resilience-recovery", title: "Recovery", series: "resilience", equation: "x(t) = x_eq + (x₀-x_eq)e^{-t/τ} + overshoot", description: "Damped recovery with overshoot — the system swings past equilibrium before settling. The overshoot is the extra.", emotionalNote: "Swinging past center before settling into something new", background: "#E8E0D8", imageUrl: "/prints/resilience/resilience_recovery.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "resilience-repair", title: "Repair", series: "resilience", equation: "G(t) = G₀(1 - e^{-t/τ_r}) · H(t-t_d)", description: "Delayed repair function — damage at time t_d, then exponential recovery of structural integrity.", emotionalNote: "The repair beginning only after the damage is complete", background: "#E8E0D8", imageUrl: "/prints/resilience/resilience_repair.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-resilience-bundle",
    bundlePrice: 82,
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
      { id: "trust-breath-together", title: "Breath Together", series: "trust", equation: "φ₁(t) - φ₂(t) → 0 as t → ∞", description: "Two oscillators converging to zero phase difference — breathing in sync, not by force but by choice.", emotionalNote: "Choosing the same rhythm without being asked", background: "#E8E4E0", imageUrl: "/prints/trust/trust_breath_together.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "trust-handshake", title: "Handshake", series: "trust", equation: "SYN → SYN-ACK → ACK", description: "The TCP three-way handshake — a protocol of mutual acknowledgment. I reach out. You acknowledge. I confirm.", emotionalNote: "I reach out. You acknowledge. I confirm.", background: "#E8E4E0", imageUrl: "/prints/trust/trust_handshake.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "trust-mirror", title: "Mirror", series: "trust", equation: "y₁(t) = αy₂(t-τ) + (1-α)y₁(t-τ)", description: "Delayed mirroring — one system following the other with a lag, weighted between self and other.", emotionalNote: "Following without losing yourself", background: "#E8E4E0", imageUrl: "/prints/trust/trust_mirror.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "trust-sync", title: "Sync", series: "trust", equation: "dφ/dt = Δω - K sin(φ)", description: "The Adler equation — phase synchronization with detuning. Trust is choosing to lock despite the frequency difference.", emotionalNote: "Locking into shared rhythm despite different natural frequencies", background: "#E8E4E0", imageUrl: "/prints/trust/trust_sync.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "trust-weave", title: "Weave", series: "trust", equation: "f(x,y) = sin(x)sin(y) + sin(x)cos(y)", description: "Two sinusoidal functions interlocking — warp and weft creating a fabric stronger than either thread alone.", emotionalNote: "Two patterns interlocking to create something stronger than either alone", background: "#E8E4E0", imageUrl: "/prints/trust/trust_weave.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-trust-bundle",
    bundlePrice: 82,
  },

  // ── EUPHORIA ────────────────────────────────────────────
  {
    id: "euphoria",
    name: "EUPHORIA",
    emotion: "peak intensity, maximum amplitude, the ceiling",
    tagline: "Crown functions at maximum amplitude. Kaleidoscopic symmetry. Stained glass tessellation at full saturation.",
    description: "Maximum-amplitude functions, kaleidoscopic symmetry groups, crown waveforms, prismatic refraction, and stained glass tessellation. Systems at peak intensity — the mathematical ceiling.",
    story: "Euphoria is a system at maximum amplitude. It cannot go higher. The mathematics of extrema — peaks, crowns, saturated color fields — describe moments of maximum intensity. These are not sustainable states, which makes them precious.",
    mathematicalPrimitive: "maximum amplitude, symmetry groups, tessellation, refraction",
    background: "#0A0A14",
    palette: ["#E040E0", "#40E0E0", "#E0E040", "#E04040", "#40E040"],
    makingOf: "50 renders. 5 survived.",
    pieces: [
      { id: "euphoria-crown", title: "Crown", series: "euphoria", equation: "f(θ) = |cos(nθ/2)|^{1/n}", description: "A supercircle in polar coordinates — the curve crowns at its vertices, each peak a maximum.", emotionalNote: "Every vertex a peak, every peak a crown", background: "#0A0A14", imageUrl: "/prints/euphoria/euphoria_crown.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "euphoria-firework", title: "Firework", series: "euphoria", equation: "r(t) = v₀t - ½gt², θ ~ Uniform(0,2π)", description: "Radial ballistic trajectories — launched from a single point, expanding in all directions, then falling.", emotionalNote: "Everything expanding from one brilliant moment", background: "#0A0A14", imageUrl: "/prints/euphoria/euphoria_firework.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "euphoria-kaleidoscope", title: "Kaleidoscope", series: "euphoria", equation: "f(r,θ) = f(r, θ + 2π/n), n = 6", description: "A function with n-fold rotational symmetry — every rotation reveals the same pattern. Perfect repeated beauty.", emotionalNote: "The same beauty repeated at every angle", background: "#0A0A14", imageUrl: "/prints/euphoria/euphoria_kaleidoscope.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "euphoria-prismatic", title: "Prismatic", series: "euphoria", equation: "n(λ) = A + B/λ² + C/λ⁴", description: "Cauchy's dispersion equation — white light separated into its spectrum. Every wavelength revealed.", emotionalNote: "White light separated into everything it contains", background: "#0A0A14", imageUrl: "/prints/euphoria/euphoria_prismatic.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "euphoria-stained-glass", title: "Stained Glass", series: "euphoria", equation: "T(λ,x,y) = Σ cᵢ · χ_{Ωᵢ}(x,y) · S(λ)", description: "Spectral transmission through colored regions — tessellated domains each filtering light differently.", emotionalNote: "Light passing through colored geometry", background: "#0A0A14", imageUrl: "/prints/euphoria/euphoria_stained_glass.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-euphoria-bundle",
    bundlePrice: 82,
  },

  // ── PRIDE ───────────────────────────────────────────────
  {
    id: "pride",
    name: "PRIDE",
    emotion: "standing tall, earned height, structural dignity",
    tagline: "Golden ratio proportions. Spires rising to computed vertices. The mathematics of earned height.",
    description: "Golden ratio geometry, spire functions, crown curves, flourish dynamics, and unfurling sequences. Systems that have earned their height and display it with structural integrity.",
    story: "Pride is vertical. The mathematics of pride involves height, proportion, and the golden ratio — the ratio that appears in architecture, nature, and art whenever a structure achieves a proportion that feels earned rather than forced.",
    mathematicalPrimitive: "golden ratio, vertical growth, proportioned structure",
    background: "#F0EDE6",
    palette: ["#C8A040", "#A08030", "#E0C060", "#887020", "#D8B850"],
    makingOf: "43 renders. 5 survived.",
    pieces: [
      { id: "pride-crown", title: "Crown", series: "pride", equation: "r(θ) = 1 + ε·cos(nθ), n ≥ 5", description: "A perturbed circle with high-frequency peaks — a crown formed by small deviations from perfection.", emotionalNote: "Perfection with earned peaks", background: "#F0EDE6", imageUrl: "/prints/pride/pride_crown.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "pride-flourish", title: "Flourish", series: "pride", equation: "γ(t) = (t·cos(t), t·sin(t), t²)", description: "A spiral expanding upward and outward — each revolution wider and higher than the last.", emotionalNote: "Each revolution wider and higher than the last", background: "#F0EDE6", imageUrl: "/prints/pride/pride_flourish.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "pride-golden-ratio", title: "Golden Ratio", series: "pride", equation: "φ = (1 + √5)/2 ≈ 1.618...", description: "The golden ratio rendered as geometric proportion — the division that every human eye recognizes as right.", emotionalNote: "The proportion that every eye recognizes as right", background: "#F0EDE6", imageUrl: "/prints/pride/pride_golden_ratio.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "pride-spire", title: "Spire", series: "pride", equation: "h(x) = H · (1 - |x/w|^p)^{1/p}", description: "A superelliptic spire — a form that rises to a computed vertex with structural grace.", emotionalNote: "Rising to a point with structural inevitability", background: "#F0EDE6", imageUrl: "/prints/pride/pride_spire.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "pride-unfurl", title: "Unfurl", series: "pride", equation: "θ(t) = θ₀ + (π - θ₀)(1 - e^{-t/τ})", description: "An angle opening from folded to fully extended — the unfurling of something that was contained.", emotionalNote: "Opening from contained to fully extended", background: "#F0EDE6", imageUrl: "/prints/pride/pride_unfurl.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-pride-bundle",
    bundlePrice: 82,
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
      { id: "anticipation-charge", title: "Charge", series: "anticipation", equation: "V(t) = V₀(1 - e^{-t/RC})", description: "A capacitor charging — voltage rising toward its maximum, each moment adding less than the last but never arriving.", emotionalNote: "Approaching capacity without ever quite reaching it", background: "#E8E4DC", imageUrl: "/prints/anticipation/anticipation_charge.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "anticipation-convergence", title: "Convergence", series: "anticipation", equation: "aₙ → L as n → ∞, |aₙ - L| < ε", description: "A sequence converging to its limit — each term closer than the last, the destination certain but never reached.", emotionalNote: "Each step closer, the destination certain but never reached", background: "#E8E4DC", imageUrl: "/prints/anticipation/anticipation_convergence.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "anticipation-countdown", title: "Countdown", series: "anticipation", equation: "f(t) = N - ⌊t/Δt⌋", description: "A discrete step function counting down — each step equal, the final step indistinguishable from the others.", emotionalNote: "Equal steps where the last one changes everything", background: "#E8E4DC", imageUrl: "/prints/anticipation/anticipation_countdown.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "anticipation-kindling", title: "Kindling", series: "anticipation", equation: "T(t) = T_ign - ΔT·e^{-t/τ}", description: "Temperature approaching ignition — exponentially closing the gap, the combustion threshold just above.", emotionalNote: "The temperature almost at ignition", background: "#E8E4DC", imageUrl: "/prints/anticipation/anticipation_kindling.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "anticipation-potential", title: "Potential", series: "anticipation", equation: "U(x) = mgh, h = h_max", description: "Gravitational potential energy at maximum height — all the energy stored, none yet released.", emotionalNote: "All energy stored, none yet released", background: "#E8E4DC", imageUrl: "/prints/anticipation/anticipation_potential.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-anticipation-bundle",
    bundlePrice: 82,
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
      { id: "longing-harmonic-decay", title: "Harmonic Decay", series: "longing", equation: "f(t) = A₀ · cos(ωt) · e^{-γt}", description: "A damped harmonic oscillator — each swing shorter than the last, the memory of motion fading but never gone.", emotionalNote: "Each return shorter than the last, but never fully gone", background: "#E0E4E8", imageUrl: "/prints/longing/longing_harmonic_decay.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "longing-magnetic", title: "Magnetic", series: "longing", equation: "F = μ₀m₁m₂/(4πr²)", description: "Magnetic field lines — curves that reach toward each other across empty space, never quite connecting.", emotionalNote: "Lines reaching across empty space", background: "#E0E4E8", imageUrl: "/prints/longing/longing_magnetic.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "longing-tantalus", title: "Tantalus", series: "longing", equation: "lim_{x→a} f(x) = L, f(a) undefined", description: "A function with a removable discontinuity — the limit exists, the value does not. You can see it but cannot be there.", emotionalNote: "The value exists at every point except the one you want", background: "#E0E4E8", imageUrl: "/prints/longing/longing_tantalus.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "longing-vanishing", title: "Vanishing", series: "longing", equation: "x' = x·f/(f+d), y' = y·f/(f+d)", description: "Perspective projection — parallel lines converging to a vanishing point. The destination visible but unreachable.", emotionalNote: "The destination visible and forever receding", background: "#E0E4E8", imageUrl: "/prints/longing/longing_vanishing.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
      { id: "longing-zeno", title: "Zeno", series: "longing", equation: "S = Σ (½)ⁿ = 1, but no finite step reaches 1", description: "Zeno's dichotomy — the sum converges to 1, but each step only covers half the remaining distance.", emotionalNote: "Always halving the distance, never arriving", background: "#E0E4E8", imageUrl: "/prints/longing/longing_zeno.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 22 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-longing-bundle",
    bundlePrice: 82,
  },
];

export const allPieces: Piece[] = series.flatMap((s) => s.pieces);

export const collectionPrice = 220;
export const collectionGumroadUrl = "https://gumroad.com/l/placeholder-full-collection";

export interface HeroSlide {
  pieceId: string;
  textColor: "white" | "black";
}

export const heroSlides: HeroSlide[] = [
  { pieceId: "awe-singularity", textColor: "white" },
  { pieceId: "connection-coupled-oscillators", textColor: "white" },
  { pieceId: "grief-void", textColor: "black" },
  { pieceId: "overwhelm-attractors", textColor: "white" },
  { pieceId: "cycles-loom", textColor: "black" },
  { pieceId: "wonder-strange-attractor", textColor: "white" },
  { pieceId: "desire-pursuit", textColor: "white" },
  { pieceId: "growth-reaction-diffusion", textColor: "black" },
];

export const featuredSeriesIds = [
  "awe",
  "connection",
  "overwhelm",
  "grief",
  "surrender",
  "desire",
  "cycles",
  "solitude",
  "peace",
  "nostalgia",
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
