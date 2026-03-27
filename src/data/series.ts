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
    emotion: "closeness, following, the space between two things",
    tagline: "Two parametric curves with a phase offset. Neither leads nor follows. The gap between them is the relationship.",
    description: "Parametric curve pairs with phase offsets, coupled oscillators, and topological knots. Two systems that move through space together — sometimes synchronized, sometimes drifting, always tethered.",
    story: "Connection is not union. It is two separate trajectories that choose proximity. The coupled oscillator equations describe this precisely: two systems that influence each other's frequency, amplitude, and phase. They never fully merge. The space between them is where the relationship lives.",
    mathematicalPrimitive: "parametric curves, coupled oscillators, topological knots",
    background: "#0A0A12",
    palette: ["#C8887A", "#E8C878", "#D4988A", "#B87A70", "#F0D890"],
    makingOf: "77 renders. 11 survived.",
    pieces: [
      { id: "connection-pendulum", title: "Pendulum", series: "connection", equation: "θ̈ = -(g/L)sinθ + k(θ₂ - θ₁)", description: "Two coupled pendulums trading energy back and forth in phase space. I tuned the coupling constant until their trajectories spiraled around each other without ever merging.", emotionalNote: "Energy passing between two systems that never merge", background: "#0A0A12", imageUrl: "/prints/connection/connection_pendulum.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "connection-orbit-pair", title: "Orbit Pair", series: "connection", equation: "r(θ) = a(1−e²)/(1+e·cosθ)", description: "Two elliptical orbits sharing a gravitational focus. They circle the same invisible center, locked together by something neither one can see.", emotionalNote: "Held together by the same invisible center", background: "#0A0A12", imageUrl: "/prints/connection/connection_orbit_pair.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "connection-magnetic", title: "Magnetic", series: "connection", equation: "B = B₁ + B₂, ∇×B = μ₀J", description: "I superimposed the fields of two magnetic dipoles and drew the lines arcing between them. The pull is invisible, but it shapes everything around it.", emotionalNote: "The invisible force that shapes the space between", background: "#0A0A12", imageUrl: "/prints/connection/connection_magnetic.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "connection-lissajous", title: "Lissajous", series: "connection", equation: "x = sin(3t), y = sin(2t + φ)", description: "A 3:2 Lissajous figure with a phase offset. Two frequencies tracing a single curve — the same motion, half a beat apart.", emotionalNote: "The same motion, half a beat apart", background: "#0A0A12", imageUrl: "/prints/connection/connection_lissajous.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "connection-entanglement", title: "Entanglement", series: "connection", equation: "|ψ⟩ = (|01⟩ - |10⟩)/√2", description: "Two signals separated in space but perfectly correlated. I added visible lines to trace what quantum mechanics says is there but can't be seen.", emotionalNote: "Connected across any distance", background: "#0A0A12", imageUrl: "/prints/connection/connection_entanglement.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "connection-torus-knot", title: "Torus Knot", series: "connection", equation: "x = (R+r·cos(qt))cos(pt)", description: "A curve wound around a torus at two frequencies, locked in a knot that can never be untied without cutting. Once it's tied, that's it.", emotionalNote: "Two frequencies locked together permanently", background: "#0A0A12", imageUrl: "/prints/connection/connection_torus_knot.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "connection-weave", title: "Weave", series: "connection", equation: "y₁ = sin(ωt), y₂ = sin(ωt + π/2)", description: "Pairs of sine waves crossing at every frequency — tight braids at the top, slow sweeping crossings at the bottom. I wanted to show interleaving at every scale.", emotionalNote: "Interleaving at every scale", background: "#0A0A12", imageUrl: "/prints/connection/connection_weave.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "connection-helix", title: "Helix", series: "connection", equation: "x = r·cos(t), y = r·sin(t), z = ct", description: "A double helix — two strands spiraling in parallel, always the same distance apart. They never touch. That constant distance is the whole point.", emotionalNote: "Always the same distance apart, never touching", background: "#0A0A12", imageUrl: "/prints/connection/connection_helix.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "connection-phase-sync", title: "Phase Sync", series: "connection", equation: "dθ/dt = ω + (K/N)Σsin(θⱼ−θᵢ)", description: "Kuramoto oscillators starting scattered and gradually locking into sync. The left side is chaos; the right side is coherence. I let the coupling do the work.", emotionalNote: "Scattered rhythms finding the same beat", background: "#0A0A12", imageUrl: "/prints/connection/connection_phase_sync.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "connection-rossler", title: "Rössler", series: "connection", equation: "ẋ = −y−z, ẏ = x+ay", description: "Two Rössler attractors coupled together — chaotic trajectories that shadow each other through folded space. Even in chaos, they stay close.", emotionalNote: "Chaos that stays close to chaos", background: "#0A0A12", imageUrl: "/prints/connection/connection_rossler.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "connection-braid", title: "Braid", series: "connection", equation: "σ₁σ₂σ₁ = σ₂σ₁σ₂", description: "Three strands crossing according to the braid group relations. The crossings aren't decorative — they're topologically distinct from a simple twist. You can't undo them.", emotionalNote: "Crossings that can't be undone", background: "#0A0A12", imageUrl: "/prints/connection/connection_braid.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
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
      { id: "overwhelm-attractors", title: "Attractors", series: "overwhelm", equation: "dx/dt = σ(y-x), dy/dt = x(ρ-z)-y", description: "I rendered multiple Lorenz attractors on top of each other. Each one follows its own deterministic path, but layered together they become unreadable. That's the point.", emotionalNote: "Every path makes sense alone — together they're unreadable", background: "#0A0A12", imageUrl: "/prints/overwhelm/overwhelm_attractors.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "overwhelm-kuramoto", title: "Kuramoto", series: "overwhelm", equation: "dθᵢ/dt = ωᵢ + (K/N)Σsin(θⱼ - θᵢ)", description: "Dozens of Kuramoto oscillators all trying to sync up and none of them fully succeeding. Each one is doing the right thing individually. Together it's too much.", emotionalNote: "Dozens of rhythms trying and failing to find each other", background: "#0A0A12", imageUrl: "/prints/overwhelm/overwhelm_kuramoto.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "overwhelm-levy-swarm", title: "Levy Swarm", series: "overwhelm", equation: "P(x) ~ |x|^{-1-α}, 0 < α < 2", description: "A swarm of Lévy flights — random walks that mostly take small steps but occasionally leap across the entire field. I couldn't keep them contained. That was the feeling I wanted.", emotionalNote: "Motion that refuses to stay bounded", background: "#0A0A12", imageUrl: "/prints/overwhelm/overwhelm_levy_swarm.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "overwhelm-phase-flood", title: "Phase Flood", series: "overwhelm", equation: "ψ(x,t) = Σ Aₙ e^{i(kₙx - ωₙt + φₙ)}", description: "I superposed dozens of complex wave functions. The resulting field is nonzero everywhere and still nowhere. Every point vibrates from every direction at once.", emotionalNote: "Nowhere still, nothing quiet", background: "#0A0A12", imageUrl: "/prints/overwhelm/overwhelm_phase_flood.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "overwhelm-turbulence", title: "Turbulence", series: "overwhelm", equation: "Re = ρvL/μ >> Re_cr", description: "Fluid flow past the critical Reynolds number. I pushed the simulation until the laminar lines broke apart — order dissolving into chaos at every scale simultaneously.", emotionalNote: "Order dissolving at every scale at once", background: "#0A0A12", imageUrl: "/prints/overwhelm/overwhelm_turbulence.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-overwhelm-bundle",
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
    tagline: "L-system branching at thirteen levels. Golden spirals tiling the plane. Thirty-four lines reaching toward light.",
    description: "Bifurcation diagrams, dendritic growth, Lissajous blooms, logistic cascades, and reaction-diffusion patterns. Growth is not linear — it is fractal.",
    story: "Growth follows rules. The branching of trees obeys L-system grammars. The spiral of a nautilus follows the golden ratio. Reaction-diffusion systems create the spots on leopards and the stripes on zebrafish. This series renders these growth algorithms as minimalist art.",
    mathematicalPrimitive: "L-systems, bifurcation, reaction-diffusion, logistic maps",
    background: "#F5F0E6",
    palette: ["#1A4D2E", "#2E8B4A", "#6BBF6E", "#A8D86E", "#E8D878"],
    makingOf: "140 renders. 5 survived.",
    pieces: [
      { id: "growth-bifurcation", title: "Bifurcation", series: "growth", equation: "x_{n+1} = rx_n(1 - x_n), r ∈ [2.5, 4]", description: "The logistic map's bifurcation diagram, but I read it as a growth story — a single strategy that splits and splits again until it's irreducibly complex.", emotionalNote: "Simple beginnings branching until they can't be simplified", background: "#F5F0E6", imageUrl: "/prints/growth/growth_bifurcation.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "growth-dendrite", title: "Dendrite", series: "growth", equation: "L → F[+L][-L]FL", description: "I wrote a simple L-system rule and let it recurse. The same grammar applied at every level produces branching that looks alive. Three characters of code, infinite complexity.", emotionalNote: "The same rule at every scale, branching forever", background: "#F5F0E6", imageUrl: "/prints/growth/growth_dendrite.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "growth-lissajous-bloom", title: "Lissajous Bloom", series: "growth", equation: "x = A sin(at + δ), y = B sin(bt)", description: "Lissajous curves where I slowly evolved the frequency ratio. The figure blooms outward as the parameters shift — oscillation opening like something alive.", emotionalNote: "Oscillation that opens outward", background: "#F5F0E6", imageUrl: "/prints/growth/growth_lissajous_bloom.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "growth-logistic-cascade", title: "Logistic Cascade", series: "growth", equation: "dN/dt = rN(1 - N/K)", description: "The logistic growth equation — rapid expansion that slows as it approaches carrying capacity. Growth that has to learn its own limits.", emotionalNote: "Expansion that learns to respect its own limits", background: "#F5F0E6", imageUrl: "/prints/growth/growth_logistic_cascade.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "growth-reaction-diffusion", title: "Reaction Diffusion", series: "growth", equation: "∂u/∂t = Dᵤ∇²u + f(u,v)", description: "A Turing reaction-diffusion system. Two chemicals diffusing at different rates, and pattern just appears — spots, stripes, waves. I didn't design the pattern. The math did.", emotionalNote: "Pattern that nobody designed", background: "#F5F0E6", imageUrl: "/prints/growth/growth_reaction_diffusion.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
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
      { id: "cycles-toroid", title: "Toroid", series: "cycles", equation: "(x²+y²+z²+R²−r²)² = 4R²(x²+y²)", description: "Cross-sections of a torus at different angles — nested loops through the surface of return. A cycle within a cycle within a cycle.", emotionalNote: "Cycles nested inside cycles", background: "#F0E8DA", imageUrl: "/prints/cycles/cycles_toroid.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
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
      { id: "confusion-aliased", title: "Aliased", series: "confusion", equation: "f_alias = |f - n·f_s|, n = round(f/f_s)", description: "I sampled a signal below the Nyquist rate and watched the true frequency become indistinguishable from its aliases. You can't tell which one is real anymore.", emotionalNote: "When the real signal and its reflections look identical", background: "#E6E2DC", imageUrl: "/prints/confusion/confusion_aliased.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "confusion-knot", title: "Knot", series: "confusion", equation: "K: S¹ → S³", description: "A topological knot — a closed curve in 3D space that crosses itself so many times you lose track of where it started. Can't be untangled without cutting.", emotionalNote: "A path that crosses itself until the start is lost", background: "#E6E2DC", imageUrl: "/prints/confusion/confusion_knot.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "confusion-labyrinth", title: "Labyrinth", series: "confusion", equation: "maze(x,y) = {0,1} | ∃! path(start, end)", description: "I generated a labyrinth with exactly one solution. The path exists — you just can't see it from inside. You have to try every wrong turn first.", emotionalNote: "The solution exists but can't be seen from inside", background: "#E6E2DC", imageUrl: "/prints/confusion/confusion_labyrinth.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "confusion-tangle", title: "Tangle", series: "confusion", equation: "γ(t): [0,1] → R³, self-intersecting", description: "Multiple space curves that intersect and interleave. Each one is individually traceable. Together they become inseparable. That gap between the parts and the whole is where confusion lives.", emotionalNote: "Clear individually, inseparable together", background: "#E6E2DC", imageUrl: "/prints/confusion/confusion_tangle.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "confusion-vertigo", title: "Vertigo", series: "confusion", equation: "r(t) = e^{-at}(cos ωt, sin ωt, t)", description: "A spiral that ascends and decays at the same time. I tilted the visual field until I lost my own sense of orientation making it.", emotionalNote: "The spiral that makes the ground feel uncertain", background: "#E6E2DC", imageUrl: "/prints/confusion/confusion_vertigo.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-confusion-bundle",
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
      { id: "shame-veil", title: "Veil", series: "shame", equation: "f(x) = f(x) · (1 - g(x))", description: "A function multiplied by its own complement — the signal using its own structure to mask itself. Hiding behind what you already are.", emotionalNote: "Hiding behind the structure of what you already are", background: "#E0DCE4", imageUrl: "/prints/shame/shame_veil.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
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
    makingOf: "42 renders. 5 survived.",
    pieces: [
      { id: "solitude-basin", title: "Basin", series: "solitude", equation: "y = a(x−h)² + k", description: "A parabolic potential well with circles settled at the minimum. One has climbed to the rim, alone at the tip of the rising curve. I kept thinking about what made it leave.", emotionalNote: "The one who climbed out of the comfortable minimum", background: "#E0DDD6", imageUrl: "/prints/solitude/solitude_basin.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "solitude-beacon", title: "Beacon", series: "solitude", equation: "A(r) = A₀/r²", description: "Overlapping ripple sources crowded together, interfering with each other. One signal radiates separately — its waves bend the others but never merge with them.", emotionalNote: "One signal radiating apart from the rest", background: "#E0DDD6", imageUrl: "/prints/solitude/solitude_beacon.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "solitude-canopy", title: "Canopy", series: "solitude", equation: "r(θ) = a·eᵇᶿ, branching", description: "Fractal branching from a single trunk — logarithmic spirals splitting and resplitting into a full canopy. One source becoming its own world.", emotionalNote: "A single root becoming its own world", background: "#E0DDD6", imageUrl: "/prints/solitude/solitude_canopy.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "solitude-signal", title: "Signal", series: "solitude", equation: "S(f) = A·δ(f−f₀) + η", description: "A dense field of overlapping frequencies — noise from every direction. One gold signal rises above it all. I made it unmistakable against the static.", emotionalNote: "One clear voice in a room full of noise", background: "#E0DDD6", imageUrl: "/prints/solitude/solitude_signal.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "solitude-wanderer", title: "Wanderer", series: "solitude", equation: "x(t) = x₀ + ∫₀ᵗ v(s)ds", description: "A single random walk across an empty plane. No other walkers, no boundaries, no destination. Just one path and all that space around it.", emotionalNote: "One path with nowhere it needs to be", background: "#E0DDD6", imageUrl: "/prints/solitude/solitude_wanderer.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
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
      { id: "melancholy-dissolve", title: "Dissolve", series: "melancholy", equation: "c(t) = c₀ · e^{-kt}", description: "Concentration decaying in solution. The sharp definition of a substance spreading until it's everywhere and nowhere. I watched it go from something to nothing.", emotionalNote: "Spreading until it's everywhere and nowhere", background: "#D8D4D0", imageUrl: "/prints/melancholy/melancholy_dissolve.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "melancholy-drift", title: "Drift", series: "melancholy", equation: "dx = μdt + σdW", description: "Brownian motion with weak drift — a slow, purposeless migration. There's technically a direction, but it barely matters.", emotionalNote: "Movement without purpose, direction without urgency", background: "#D8D4D0", imageUrl: "/prints/melancholy/melancholy_drift.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "melancholy-elegy", title: "Elegy", series: "melancholy", equation: "f(t) = A · t^{-α}, α ∈ (0,1)", description: "Power-law decay — slower than exponential. The signal fades but refuses to fully vanish. It just gets quieter and quieter without ever reaching silence.", emotionalNote: "Getting quieter without ever reaching silence", background: "#D8D4D0", imageUrl: "/prints/melancholy/melancholy_elegy.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "melancholy-entropy", title: "Entropy", series: "melancholy", equation: "S = -k Σ pᵢ ln pᵢ, dS/dt ≥ 0", description: "Shannon entropy increasing over time. I watched the system slowly lose the information that once made it ordered — structure dissolving into noise so gradually you can't point to when it changed.", emotionalNote: "Order dissolving into noise so slowly you can't point to when", background: "#D8D4D0", imageUrl: "/prints/melancholy/melancholy_entropy.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "melancholy-lethe", title: "Lethe", series: "melancholy", equation: "∂c/∂t + v·∇c = D∇²c", description: "Advection-diffusion in a slow river — substance carried downstream and dispersed. Named for the mythological river of forgetting. The current does the work.", emotionalNote: "The slow current that carries everything away", background: "#D8D4D0", imageUrl: "/prints/melancholy/melancholy_lethe.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-melancholy-bundle",
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
      { id: "surrender-drape", title: "Drape", series: "surrender", equation: "y = a·cosh(x/a)", description: "Catenary curves — the shape gravity gives to anything that hangs freely. I drew twenty arcs from tight to deep, each one yielding to the same force.", emotionalNote: "The shape gravity gives when you stop resisting", background: "#E8E4DE", imageUrl: "/prints/surrender/surrender_drape.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
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
      { id: "wonder-apollonian-gasket", title: "Apollonian Gasket", series: "wonder", equation: "(k₁+k₂+k₃+k₄)² = 2(k₁²+k₂²+k₃²+k₄²)", description: "I iterated Descartes' Circle Theorem — circles packed inside circles, every gap filled with a smaller circle. It never ends. Infinity nested inside a finite boundary.", emotionalNote: "Infinity inside a finite boundary", background: "#0A0A18", imageUrl: "/prints/wonder/wonder_apollonian_gasket.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "wonder-harmonograph", title: "Harmonograph", series: "wonder", equation: "x = A₁sin(f₁t+φ₁)e^{-d₁t} + A₂sin(f₂t+φ₂)e^{-d₂t}", description: "Two damped pendulums coupled by a drawing surface. I didn't design the pattern — it emerged from the interaction of their decay rates. That's what got me.", emotionalNote: "Beauty that nobody designed", background: "#0A0A18", imageUrl: "/prints/wonder/wonder_harmonograph.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "wonder-mandelbrot-orbit", title: "Mandelbrot Orbit", series: "wonder", equation: "z_{n+1} = z_n² + c", description: "I drew individual orbits of the Mandelbrot iteration — not the set boundary everyone knows, but the trajectories themselves. The invisible paths that define where chaos begins.", emotionalNote: "The paths nobody sees that define the boundary", background: "#0A0A18", imageUrl: "/prints/wonder/wonder_mandelbrot_orbit.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "wonder-recursion", title: "Recursion", series: "wonder", equation: "f(n) = f(f(n-1))", description: "A function that calls itself. Each level of depth reveals new structure identical to the whole. I kept zooming in and it never stopped.", emotionalNote: "Zoom in and it never stops", background: "#0A0A18", imageUrl: "/prints/wonder/wonder_recursion.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "wonder-strange-attractor", title: "Strange Attractor", series: "wonder", equation: "dx/dt = σ(y-x), dy/dt = x(ρ-z)-y, dz/dt = xy-βz", description: "The Lorenz attractor — deterministic chaos that never repeats but always stays bounded. I ran it for millions of iterations and it never left the manifold or traced the same path twice.", emotionalNote: "Never repeats, never leaves", background: "#0A0A18", imageUrl: "/prints/wonder/wonder_strange_attractor.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "wonder-transform", title: "Transform", series: "wonder", equation: "w = z + a/(z − z₀)", description: "A Joukowski-like conformal mapping — concentric circles warped by a pole singularity into nested airfoil lobes. Simple geometry revealing hidden structure through transformation.", emotionalNote: "Simple circles hiding something extraordinary", background: "#4f5d71", imageUrl: "/prints/wonder/wonder_transform.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
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
      { id: "peace-settled", title: "Settled", series: "peace", equation: "f(t) = Ae^(-γt)·sin(ωt)", description: "Twenty damped oscillations decaying into horizontal stillness, one by one. I waited for each voice to go quiet. The last one takes the longest.", emotionalNote: "The last oscillation going quiet", background: "#F0EDE8", imageUrl: "/prints/peace/peace_settled.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
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
      { id: "envy-covet", title: "Covet", series: "envy", equation: "d(x, S) = inf{||x-s|| : s ∈ S}", description: "The distance function to a set — I computed the exact gap between where you are and where you want to be. It's a real number. You can measure it.", emotionalNote: "The gap has an exact measurement", background: "#0C1A0C", imageUrl: "/prints/envy/envy_covet.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "envy-glass-ceiling", title: "Glass Ceiling", series: "envy", equation: "f(x) = min(g(x), c)", description: "A function clamped at a ceiling. Growth is permitted to a point, then truncated. You can't see the barrier from below — you only find it when you hit it.", emotionalNote: "You only find the ceiling when you hit it", background: "#0C1A0C", imageUrl: "/prints/envy/envy_glass_ceiling.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "envy-mirror", title: "Mirror", series: "envy", equation: "f(-x) = f(x)", description: "A function reflected across an axis. The same form, reversed. I kept staring at it and realized the mirror shows you more about yourself than about the other side.", emotionalNote: "The mirror shows you more about yourself", background: "#0C1A0C", imageUrl: "/prints/envy/envy_mirror.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "envy-shadow", title: "Shadow", series: "envy", equation: "P(x) = x - (x·n̂)n̂", description: "Orthogonal projection — the shadow of a higher-dimensional object onto a lower plane. Always less than the original. You only see the flattened version.", emotionalNote: "You only ever see the flattened version", background: "#0C1A0C", imageUrl: "/prints/envy/envy_shadow.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "envy-watch", title: "Watch", series: "envy", equation: "θ(t) = arctan(y(t)/x(t))", description: "An angle function that tracks a moving point. The geometry of eyes that follow — always computed, always pointing at what they can't look away from.", emotionalNote: "Eyes that can't look away", background: "#0C1A0C", imageUrl: "/prints/envy/envy_watch.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-envy-bundle",
    bundlePrice: 169,
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
      { id: "rage-chaos", title: "Chaos", series: "rage", equation: "x_{n+1} = 4x_n(1-x_n)", description: "The logistic map at r=4. Fully chaotic — every initial condition leads somewhere completely unpredictable. I ran it thousands of times and no two paths match.", emotionalNote: "No two paths match, ever", background: "#1A0A0A", imageUrl: "/prints/rage/rage_chaos.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "rage-detonation", title: "Detonation", series: "rage", equation: "D = √(2(γ²-1)q)", description: "The Chapman-Jouguet detonation velocity — the minimum speed at which a detonation wave can propagate. Below this speed, it fizzles. At this speed, everything goes.", emotionalNote: "The minimum speed at which everything goes", background: "#1A0A0A", imageUrl: "/prints/rage/rage_detonation.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "rage-eruption", title: "Eruption", series: "rage", equation: "p(z) = ρgz + p₀, p > p_yield", description: "Pressure exceeding yield strength — the magma chamber equation. I pushed the internal pressure past every boundary. Containment fails. Everything comes up.", emotionalNote: "Pressure that exceeds every boundary at once", background: "#1A0A0A", imageUrl: "/prints/rage/rage_eruption.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "rage-shatter", title: "Shatter", series: "rage", equation: "E_release > Σ G_c · A_crack", description: "Griffith fracture — the energy available exceeds the surface energy of all possible cracks simultaneously. Everything breaks in every direction at once.", emotionalNote: "Breaking in every direction at once", background: "#1A0A0A", imageUrl: "/prints/rage/rage_shatter.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "rage-shockwave", title: "Shockwave", series: "rage", equation: "v > c, M = v/c >> 1", description: "Motion faster than the medium can communicate — the Mach cone. The shockwave arrives before the warning. By the time you hear it, it's already past you.", emotionalNote: "It arrives before the warning", background: "#1A0A0A", imageUrl: "/prints/rage/rage_shockwave.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-rage-bundle",
    bundlePrice: 169,
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
      { id: "joy-bloom", title: "Bloom", series: "joy", equation: "r(θ) = a + b·cos(nθ), a > b", description: "A rose curve expanding — petals opening as the amplitude grows. I let each petal unfold without constraining it. The geometry of opening up.", emotionalNote: "Opening without hesitation", background: "#FFFCF0", imageUrl: "/prints/joy/joy_bloom.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "joy-confetti", title: "Confetti", series: "joy", equation: "P(x,y) ~ Uniform(Ω), N >> 1", description: "Uniform random scatter — every point equally likely, no clustering, no preference. I threw color everywhere with no plan. That felt right.", emotionalNote: "Color thrown everywhere with no plan", background: "#FFFCF0", imageUrl: "/prints/joy/joy_confetti.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "joy-lissajous", title: "Lissajous", series: "joy", equation: "x = sin(3t), y = sin(4t)", description: "A Lissajous figure at a 3:4 ratio — the closed curve two harmonics make when they're in perfect relationship. Clean, complete, satisfying.", emotionalNote: "Two harmonics in perfect relationship", background: "#FFFCF0", imageUrl: "/prints/joy/joy_lissajous.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "joy-pinwheel", title: "Pinwheel", series: "joy", equation: "f(r,θ) = cos(nθ + αr)", description: "A spiral pinwheel with rotational symmetry and radial twist. It spins without effort — no friction, no resistance, just turning.", emotionalNote: "Spinning without effort", background: "#FFFCF0", imageUrl: "/prints/joy/joy_pinwheel.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "joy-sunburst", title: "Sunburst", series: "joy", equation: "I(r,θ) = I₀ · (1/r) · Σ δ(θ - 2πn/N)", description: "Light streaming outward from a center in every direction equally. No direction favored, no angle brighter. I wanted pure radiance with no preference.", emotionalNote: "Light going everywhere equally", background: "#FFFCF0", imageUrl: "/prints/joy/joy_sunburst.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-joy-bundle",
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
      { id: "trust-sync", title: "Sync", series: "trust", equation: "dφ/dt = Δω - K sin(φ)", description: "The Adler equation — phase synchronization with detuning. Two systems with different natural frequencies choosing to lock anyway. That choice is the whole thing.", emotionalNote: "Locking in despite different natural frequencies", background: "#E8E4E0", imageUrl: "/prints/trust/trust_sync.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "trust-weave", title: "Weave", series: "trust", equation: "f(x,y) = sin(x)sin(y) + sin(x)cos(y)", description: "Two sinusoidal functions interlocking — warp and weft creating a fabric. Neither thread is strong alone. Together they hold.", emotionalNote: "Neither strong alone, together they hold", background: "#E8E4E0", imageUrl: "/prints/trust/trust_weave.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-trust-bundle",
    bundlePrice: 169,
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
      { id: "euphoria-crown", title: "Crown", series: "euphoria", equation: "f(θ) = |cos(nθ/2)|^{1/n}", description: "A supercircle in polar coordinates — the curve crowns at its vertices. I pushed each peak to maximum. That's what euphoria looks like mathematically: everything at the ceiling.", emotionalNote: "Everything at the ceiling", background: "#0A0A14", imageUrl: "/prints/euphoria/euphoria_crown.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "euphoria-firework", title: "Firework", series: "euphoria", equation: "r(t) = v₀t - ½gt², θ ~ Uniform(0,2π)", description: "Ballistic trajectories launched from a single point in all directions — expanding outward, then falling. One brilliant moment, then gravity. I kept the burst.", emotionalNote: "One brilliant moment, then gravity", background: "#0A0A14", imageUrl: "/prints/euphoria/euphoria_firework.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "euphoria-kaleidoscope", title: "Kaleidoscope", series: "euphoria", equation: "f(r,θ) = f(r, θ + 2π/n), n = 6", description: "Six-fold rotational symmetry — every 60 degrees reveals the same pattern. I kept rotating it and it never stopped being satisfying.", emotionalNote: "The same beauty at every angle", background: "#0A0A14", imageUrl: "/prints/euphoria/euphoria_kaleidoscope.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "euphoria-prismatic", title: "Prismatic", series: "euphoria", equation: "n(λ) = A + B/λ² + C/λ⁴", description: "Cauchy's dispersion equation — white light separated into its full spectrum. Every wavelength that was hidden inside, spread out and visible. All of it at once.", emotionalNote: "Everything that was hidden inside, visible at once", background: "#0A0A14", imageUrl: "/prints/euphoria/euphoria_prismatic.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "euphoria-stained-glass", title: "Stained Glass", series: "euphoria", equation: "T(λ,x,y) = Σ cᵢ · χ_{Ωᵢ}(x,y) · S(λ)", description: "Light passing through tessellated colored regions — each domain filtering differently. I was thinking about stained glass windows and how they turn light into feeling.", emotionalNote: "Light turned into color by geometry", background: "#0A0A14", imageUrl: "/prints/euphoria/euphoria_stained_glass.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
    ],
    bundleGumroadUrl: "https://gumroad.com/l/placeholder-euphoria-bundle",
    bundlePrice: 169,
  },

  // ── PRIDE ───────────────────────────────────────────────
  {
    id: "pride",
    name: "PRIDE",
    emotion: "protection, solidarity, sheltering one another",
    tagline: "Nested arches and converging waves. The mathematics of standing over someone so they can stand taller.",
    description: "Superellipse canopies and ocean harmonics in softened Pride palettes. Geometries of protection, unity, and shared strength.",
    story: "Pride is shelter. The mathematics of pride is not about standing tallest — it's about the geometry of standing over someone so they can stand taller. Arches nested inside arches, each one protecting the one beneath it.",
    mathematicalPrimitive: "superellipse nesting, wave superposition, protective enclosure",
    background: "#f3eee7",
    palette: ["#f6f2ef", "#f5a9b8", "#5bcffb", "#ffd100", "#7f2dbd"],
    makingOf: "New series — building out.",
    pieces: [
      { id: "pride-shelter", title: "Shelter", series: "pride", equation: "y = h(1−|s|^p)", description: "Twenty-four nested superellipse arches, each one smaller and softer than the one outside it. Every arch is a person standing over someone so they don't have to stand alone.", emotionalNote: "Each arch protecting the one beneath it", background: "#f3eee7", imageUrl: "/prints/pride/pride_shelter.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "pride-waves", title: "Waves", series: "pride", equation: "h = ΣAᵢcos(kᵢx−ωᵢt)", description: "Seventy-eight ocean lines moving through the full LGBTQ+ spectrum — trans blue, pink, and white woven through the classic rainbow. Many waves, one sea. Every color present, none token.", emotionalNote: "Many waves, one sea", background: "#f3eee7", imageUrl: "/prints/pride/pride_waves.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
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
      { id: "anticipation-convergence", title: "Convergence", series: "anticipation", equation: "aₙ → L as n → ∞, |aₙ - L| < ε", description: "A sequence converging to its limit. Each term closer than the last, the destination mathematically certain but never actually reached. I watched it approach for thousands of iterations.", emotionalNote: "Certain destination, never reached", background: "#E8E4DC", imageUrl: "/prints/anticipation/anticipation_convergence.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "anticipation-countdown", title: "Countdown", series: "anticipation", equation: "f(t) = N - ⌊t/Δt⌋", description: "A step function counting down — each step identical. The last one looks exactly like all the others, but it changes everything.", emotionalNote: "The last step looks the same but changes everything", background: "#E8E4DC", imageUrl: "/prints/anticipation/anticipation_countdown.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "anticipation-kindling", title: "Kindling", series: "anticipation", equation: "T(t) = T_ign - ΔT·e^{-t/τ}", description: "Temperature approaching ignition — exponentially closing the gap, the combustion threshold right there. Almost. Almost. Not yet.", emotionalNote: "Almost. Almost. Not yet.", background: "#E8E4DC", imageUrl: "/prints/anticipation/anticipation_kindling.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
      { id: "anticipation-potential", title: "Potential", series: "anticipation", equation: "U(x) = mgh, h = h_max", description: "Gravitational potential at maximum height. All energy stored, none released yet. I rendered the moment of maximum stillness before everything moves.", emotionalNote: "Everything stored, nothing released yet", background: "#E8E4DC", imageUrl: "/prints/anticipation/anticipation_potential.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
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
      { id: "longing-zeno", title: "Zeno", series: "longing", equation: "S = Σ (½)ⁿ = 1, but no finite step reaches 1", description: "Zeno's dichotomy — each step covers half the remaining distance. The sum converges to 1 but no finite number of steps gets you there. I drew every step I could.", emotionalNote: "Always halving the distance, never arriving", background: "#E0E4E8", imageUrl: "/prints/longing/longing_zeno.jpg", gumroadUrl: "https://gumroad.com/l/placeholder", price: 45 },
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
  { pieceId: "pride-waves", textColor: "black" },
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

export const featuredPieceIds = [
  "grief-void",
  "pride-waves",
  "connection-coupled-oscillators",
  "cycles-moebius",
  "awe-radiance",
  "peace-horizon",
  "desire-pursuit",
  "nostalgia-reaching",
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
