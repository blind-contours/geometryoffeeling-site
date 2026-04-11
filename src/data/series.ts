export interface Piece {
  id: string;
  title: string;
  series: string;
  equation: string;
  description: string;
  emotionalNote: string;
  background: string;
  imageUrl: string;
  pdfUrl?: string;
  price: number;
}

export interface Series {
  id: string;
  name: string;
  emotion: string;
  /**
   * Short SEO-friendly descriptor used in page titles and meta.
   * Should read like natural English next to the series name in a title,
   * e.g. "Cosmic Abstract Art Prints About Scale and the Sublime".
   */
  seoDescriptor?: string;
  /**
   * Concrete, visually descriptive sentence shown under the tagline on the
   * homepage series blocks. Should name colors and mathematical substrate so
   * crawlers and humans both know what they are about to see.
   */
  homeDescriptor?: string;
  tagline: string;
  description: string;
  story: string;
  mathematicalPrimitive: string;
  background: string;
  palette: string[];
  pieces: Piece[];
  homePieceIds?: string[];
  makingOf: string;
}

export const series: Series[] = [
  // ── FRACTURED ───────────────────────────────────────────
  {
    id: "fractured",
    name: "FRACTURED",
    seoDescriptor: "Minimalist Abstract Art Prints About Breaking and Rupture",
    emotion: "fracture, discontinuity, the moment things break",
    tagline: "The moment things come apart. Not randomly — along every line of weakness that was already there.",
    description: "Three pieces exploring different geometries of breaking — the threshold where order dissolves, the patience of erosion, and the path a crack follows through weakness. Each piece is built from the mathematics of how things actually come apart.",
    story: "Fracture is not random. When a material breaks, it follows the physics of stress propagation. When a life breaks, it follows the topology of connection — the pieces that were closest fracture first. This series uses discontinuous functions, bifurcation diagrams, and Voronoi tessellation to map the geometry of things coming apart.",
    mathematicalPrimitive: "piecewise discontinuous functions, bifurcation, Voronoi tessellation",
    background: "#F5F0E0",
    palette: ["#3A5BA0", "#D4573B", "#E8A838", "#6B4E8B", "#2D8B6E"],
    makingOf: "47 renders. 3 survived.",
    pieces: [
      { id: "fractured-bifurcation", title: "Bifurcation", series: "fractured", equation: "x_{n+1} = rx_n(1 - x_n)", description: "One road becomes two. Then four. Then the path dissolves into something no map can follow. I kept staring at that threshold — the last moment before complexity takes over, when a single choice still holds everything together. The logistic map does this with one parameter. Life does it with one decision.", emotionalNote: "That moment when one path becomes two and there's no going back", background: "#F5F0E0", imageUrl: "/prints/fractured/fractured_bifurcation.jpg", price: 45 },
      { id: "fractured-erosion", title: "Erosion", series: "fractured", equation: "∂z/∂t = D·∇²z", description: "Time does not break stone. It reshapes it — slowly, patiently, without force. I rendered the same cliff face twenty-eight times, each one softer than the last, sharp edges rounding into curves over geological time. The patience of water against stone.", emotionalNote: "The patience of water against stone", background: "#F5F0E0", imageUrl: "/prints/fractured/fractured_erosion.jpg", price: 45 },
      { id: "fractured-glass-fracture", title: "Glass Fracture", series: "fractured", equation: "K_I = σ√(πa)", description: "A break doesn't happen at random. It follows every weakness that was already there — the invisible fault lines, the places where structure was thinnest. I kept looking at the pattern and realized: cracks don't choose where to go. The material already decided that long before the impact.", emotionalNote: "Every crack follows where the structure was already weakest", background: "#F5F0E0", imageUrl: "/prints/fractured/fractured_glass_fracture.jpg", price: 45 },
    ],
  },

  // ── CONNECTION ──────────────────────────────────────────
  {
    id: "connection",
    name: "CONNECTION",
    seoDescriptor: "Minimalist Abstract Art Prints About Attraction and Orbit",
    homeDescriptor: "Abstract prints in warm gold and terracotta on deep indigo, built from magnetic field lines, Lorenz attractors, and the slow synchronization of coupled oscillators.",
    emotion: "attraction, companionship, the space between two people",
    tagline: "Two forms moving through the same space. Neither leads nor follows. The gap between them is the relationship.",
    description: "Five pieces exploring different forms of human connection — the pull of attraction, the steadiness of companionship, the dance of reciprocity, the permanence of devotion, and the slow miracle of finding harmony together.",
    story: "Connection is not union. It is two separate trajectories that choose proximity. These equations describe that precisely: two systems that influence each other without ever fully merging. The space between them is where the relationship lives.",
    mathematicalPrimitive: "magnetic fields, orbital mechanics, Lissajous curves, torus knots, Kuramoto synchronization",
    background: "#0A0A12",
    palette: ["#C8887A", "#E8C878", "#D4988A", "#B87A70", "#F0D890"],
    makingOf: "77 renders. 5 survived.",
    homePieceIds: ["connection-magnetic", "connection-lorenz", "connection-phase-sync"],
    pieces: [
      { id: "connection-magnetic", title: "Magnetic", series: "connection", equation: "B = B₁ + B₂, ∇×B = μ₀J", description: "Two fields reaching toward each other across dark space. The pull between them is invisible, but it shapes everything — bending every line, curving every path. You can't see the force. You can feel it.", emotionalNote: "The invisible pull that shapes everything around it", background: "#E8D8B8", imageUrl: "/prints/connection/connection_magnetic.jpg", price: 45 },
      { id: "connection-lorenz", title: "Lorenz", series: "connection", equation: "dx/dt = σ(y−x), dy/dt = x(ρ−z)−y", description: "Two paths starting from almost the same place, tracing the same strange attractor — then slowly, inevitably diverging. The butterfly shape isn't decorative. It's what happens when a system is sensitive to everything. Closeness doesn't guarantee staying close.", emotionalNote: "Starting together doesn't mean staying together", background: "#E8D8B8", imageUrl: "/prints/connection/connection_lorenz.jpg", price: 45 },
      { id: "connection-phase-sync", title: "Phase Sync", series: "connection", equation: "dθ/dt = ω + (K/N)Σsin(θⱼ−θᵢ)", description: "Dozens of independent rhythms, each on its own frequency, gradually finding each other. No conductor, no signal — just proximity and time. They keep their own character while slowly aligning, until difference becomes harmony instead of distance. The coherence wasn't planned. It was earned.", emotionalNote: "Scattered rhythms finding the same beat", background: "#E8D8B8", imageUrl: "/prints/connection/connection_phase_sync.jpg", price: 45 },
      { id: "connection-torus-knot", title: "Torus Knot", series: "connection", equation: "x = (R+r·cos(qt))cos(pt)", description: "A single continuous curve that loops around itself, forming a knot that can never be untied without cutting. Once it's tied, that's it. Some connections are like that — permanent not because they're rigid, but because they're woven too deeply to undo.", emotionalNote: "Woven too deeply to come apart", background: "#E8D8B8", imageUrl: "/prints/connection/connection_torus_knot.jpg", price: 45 },
      { id: "connection-lissajous", title: "Lissajous", series: "connection", equation: "x = sin(3t), y = sin(2t + φ)", description: "Two frequencies tracing a single curve — the same motion, half a beat apart. It looks like a dance because it is one. Two rhythms close enough to share a path, different enough to make it beautiful.", emotionalNote: "The same motion, half a beat apart", background: "#E8D8B8", imageUrl: "/prints/connection/connection_lissajous.jpg", price: 45 },
    ],
  },

  // ── TENSION ─────────────────────────────────────────────
  {
    id: "tension",
    name: "TENSION",
    seoDescriptor: "Minimalist Abstract Art Prints About Strain and Opposition",
    emotion: "strain, opposition, systems that cannot rest",
    tagline: "The space between holding and collapse. Systems that cannot rest and will not resolve.",
    description: "Interference patterns, opposing forces, structural thresholds, and invisible fault lines. Systems held between competing demands — too much energy to rest, too constrained to move.",
    story: "Tension is not conflict. Conflict resolves. Tension is the state between resolution and collapse — the beam that holds because opposing forces balance perfectly. Inspired by the psychological intensity of Munch's color field.",
    mathematicalPrimitive: "interference, torsion, buckling, opposing forces",
    background: "#1A1A1A",
    palette: ["#E8D42A", "#D4282A", "#F0E648", "#CC1A1C", "#FFF060"],
    makingOf: "38 renders. 3 survived.",
    pieces: [
      { id: "tension-buckling", title: "Buckling", series: "tension", equation: "P_cr = π²EI / (KL)²", description: "There is a weight you can carry and a weight you cannot, and the line between them is exact. One measure below, everything holds. One above, everything gives. I wanted to sit right on that line — the moment before structural failure, when stability and collapse are separated by almost nothing. Built from Euler's critical load, the precise threshold where a column buckles.", emotionalNote: "The line between holding and collapse is exact", background: "#1A1A1A", imageUrl: "/prints/tension/tension_buckling.jpg", price: 45 },
      { id: "tension-fracture", title: "Fracture", series: "tension", equation: "σ = Eε (until σ > σ_y)", description: "Everything bends before it breaks. The relationship between pressure and response is perfectly proportional — right up to the invisible moment it isn't. I kept pushing the curve, watching the linear region stretch, knowing the yield point was coming. That last instant of elasticity before something permanent happens.", emotionalNote: "The invisible line between bending and breaking", background: "#1A1A1A", imageUrl: "/prints/tension/tension_fracture.jpg", price: 45 },
      { id: "tension-opposition", title: "Opposition", series: "tension", equation: "F_net = F₁ - F₂ = 0, |F₁| > 0", description: "Nothing moves. Everything strains. Two equal forces pressing from opposite directions hold each other in perfect stillness — but the stillness is not peace. It is maximum contained force, balanced on an edge. Built from static equilibrium, where the net force is zero but the internal stress is immense.", emotionalNote: "Perfect balance isn't peace — it's maximum contained force", background: "#1A1A1A", imageUrl: "/prints/tension/tension_opposition.jpg", price: 45 },
    ],
  },

  // ── GRIEF ───────────────────────────────────────────────
  {
    id: "grief",
    name: "GRIEF",
    seoDescriptor: "Minimalist Abstract Art Prints About Loss and Decay",
    homeDescriptor: "Minimalist prints in slate grey and pale lavender, built from exponential decay, heat diffusion, and the step functions of irreversible loss.",
    emotion: "decay, absence, the quiet after loss",
    tagline: "The mathematics of what disappears. Warmth that spreads until you can't find the source. Steps that only go down.",
    description: "Five pieces exploring different shapes of loss — absence that bends the space around it, weight that accumulates silently, grief that falls in sudden steps, presence that fades layer by layer, and warmth that disperses until the source is gone. The quietest series.",
    story: "Grief obeys the mathematics of decay. The half-life equation — f(t) = e^(-λt) — describes how radioactive isotopes lose their energy, but it also describes how the intensity of grief diminishes over time. It never reaches zero. The asymptote is forever.",
    mathematicalPrimitive: "exponential decay, heat diffusion, step functions, erosion",
    background: "#DDD9D2",
    palette: ["#7A8B9A", "#9A8A9A", "#C8D4E0", "#A0A8B0", "#D0C8D0"],
    makingOf: "83 renders. 5 survived.",
    homePieceIds: ["grief-void", "grief-absence", "grief-heat-diffusion"],
    pieces: [
      { id: "grief-void", title: "Void", series: "grief", equation: "|x/a|^p + |y/b|^q = 1", description: "Everything bends toward what's no longer there. Lines crowd toward the center of the frame, curving around an emptiness they cannot enter. The absence has weight — it shapes the space around it, pulls everything inward, refuses to be filled.", emotionalNote: "Everything bends toward what's no longer there", background: "#DDD9D2", imageUrl: "/prints/grief/grief_void.jpg", price: 45 },
      { id: "grief-heat-diffusion", title: "Heat Diffusion", series: "grief", equation: "∂u/∂t = α·∂²u/∂x²", description: "Warmth that was sharp and specific — here, in this place, from this person — spreading outward until you can't tell where it started. The edges soften. The source disappears. Eventually the whole field is the same temperature. I kept looking for where the warmth began. It was gone.", emotionalNote: "Warmth that spreads until you can't tell it was ever there", background: "#DDD9D2", imageUrl: "/prints/grief/grief_heat_diffusion.jpg", price: 45 },
      { id: "grief-weight", title: "Weight", series: "grief", equation: "y(x) = a·cosh((x−c)/a)", description: "Some grief is not sharp. It is heavy. It settles over everything — each day a little more, bending what was upright into something that sags. Cables hanging lower with each added load, the frame slowly giving way. Built from catenary curves under increasing weight.", emotionalNote: "The weight that bends everything down", background: "#DDD9D2", imageUrl: "/prints/grief/grief_weight.jpg", price: 45 },
      { id: "grief-heaviside-cascade", title: "Heaviside Cascade", series: "grief", equation: "H(t−tₙ) = {0, t<tₙ; 1, t≥tₙ}", description: "Grief does not always fade smoothly. Sometimes it falls in steps. A voice disappears from your routine. A place loses its meaning. A future quietly drops away. This piece holds that staircase of loss — sudden, uneven, irreversible. Built from stacked step functions, where each descent happens all at once and cannot be undone.", emotionalNote: "Each step down is permanent", background: "#DDD9D2", imageUrl: "/prints/grief/grief_heaviside_cascade.jpg", price: 45 },
      { id: "grief-absence", title: "Absence", series: "grief", equation: "f(x) = Σ aₙ·e^(−λₙt)·cos(nπx)", description: "What leaves first is not the whole thing, but the edges. Then the texture. Then the body of it. Absence rarely arrives all at once — it thins the world gradually, until what remains is only a trace of what used to fill the room. Built from decaying harmonics, a structure in which presence fades layer by layer over time.", emotionalNote: "What remains when the last frequency fades", background: "#DDD9D2", imageUrl: "/prints/grief/grief_absence.jpg", price: 45 },
    ],
  },

  // ── GROWTH ──────────────────────────────────────────────
  {
    id: "growth",
    name: "GROWTH",
    seoDescriptor: "Organic Generative Art Prints About Branching and Light",
    homeDescriptor: "Organic generative prints in forest green and warm gold, built from L-system branching, space-colonization networks, and the mathematics of reaching toward light.",
    emotion: "emergence, branching, reaching toward light",
    tagline: "One rule applied thirteen levels deep. A meadow growing at its own pace. The mathematics of reaching toward light.",
    description: "Fractal canopies, underground networks, rising stems, and branching strategies. Growth is not linear — it is recursive, emergent, and alive. Each piece is generated by the algorithm it depicts.",
    story: "Growth follows rules. The branching of trees obeys L-system grammars. Mycelial networks colonize space through attractor fields. A dormant tree thaws from the roots up via sigmoid activation. This series renders these growth algorithms as minimalist art — each piece generated by the mathematics it depicts.",
    mathematicalPrimitive: "L-systems, space colonization, sigmoid activation, power-law expansion, amplitude amplification",
    background: "#F5F0E6",
    palette: ["#1A4D2E", "#2E8B4A", "#6BBF6E", "#A8D86E", "#E8D878"],
    makingOf: "182 renders. 6 survived.",
    homePieceIds: ["growth-branch", "growth-mycelium", "growth-arise"],
    pieces: [
      { id: "growth-branch", title: "Branch", series: "growth", equation: "A→F[−θA][+θA], 13 levels, θ=35°, r=0.82", description: "One rule, applied again and again: branch left, branch right. Thirteen levels deep, and a canopy emerges — alive, complex, unmistakably a tree. All of it from three characters of code. I watched it build itself and thought: that's how growth works.", emotionalNote: "Three characters of code, infinite complexity", background: "#F5F0E6", imageUrl: "/prints/growth/growth_branch.jpg", price: 45 },
      { id: "growth-strata", title: "Strata", series: "growth", equation: "h(n) = 0.1 + H·(n/N)^1.3, color(n) = palette[(n/N)^0.65]", description: "I struggled with this one. Most generative art about growth follows L-systems or reaction-diffusion — branching corals, fractal ferns. Beautiful, but it renders more as science than feeling. I wanted expansion. Something radiating from a core heat that ripples outward like the earth itself. Not the textbook kind of growth — the kind with real movement in it.", emotionalNote: "Reverberations pushing out from a core", background: "#F5F0E6", imageUrl: "/prints/growth/growth_strata.jpg", price: 45 },
      { id: "growth-mycelium", title: "Mycelium", series: "growth", equation: "SC(attract, kill, step) + nutrient zones", description: "A single spore finds its way. One origin point sends hyphae branching outward, thick trunks tapering to gossamer tips, shifting color each time the network discovers a new nutrient zone. Built from the space colonization algorithm — the same logic real fungi use to claim territory underground.", emotionalNote: "The hidden network that connects everything underground", background: "#F5F0E6", imageUrl: "/prints/growth/growth_mycelium.jpg", price: 45 },
      { id: "growth-arise", title: "Arise", series: "growth", equation: "x(t) = x₀ − d·α·t, y(t) = y₀ + H·t", description: "I know this one seems simple. But sit with it for a minute — the longer you look, the more it feels like it's lifting. There's a quiet upward force in it, something gathering strength. That's all it needs to do.", emotionalNote: "Reaching upward, converging toward light", background: "#F5F0E6", imageUrl: "/prints/growth/growth_arise.jpg", price: 45 },
    ],
  },

  // ── CYCLES ──────────────────────────────────────────────
  {
    id: "cycles",
    name: "CYCLES",
    seoDescriptor: "Minimalist Abstract Art Prints About Return and Rhythm",
    emotion: "return, repetition, the pattern that comes back",
    tagline: "Patterns that return without being asked. Loops that take two passes to complete. Orbits that always come home.",
    description: "Woven rhythms, breathing forms, tidal harmonics, and closed orbits. Mathematics that loops — systems that always return, never quite the same way twice.",
    story: "The universe is built on cycles. Seasons, tides, heartbeats, orbits — patterns that return without being asked. This series renders the geometry of return: phase portraits that close, orbits that repeat, and Möbius strips that have no beginning or end.",
    mathematicalPrimitive: "closed orbits, phase portraits, Möbius topology, recurrence",
    background: "#F0E8DA",
    palette: ["#5A9A50", "#C8A030", "#B85A30", "#4A6A90"],
    makingOf: "60 renders. 11 survived.",
    homePieceIds: ["cycles-moebius", "cycles-seasons"],
    pieces: [
      { id: "cycles-moebius", title: "Möbius", series: "cycles", equation: "R·eⁱᵗ + r·cos(t/2)·eⁱᵗ", description: "A loop that takes two passes to complete. You walk the surface and arrive where you started — but on the other side. You have to go around again to truly return. Some cycles demand that you become different before they let you finish. Built from the Möbius strip, a surface with only one side.", emotionalNote: "A loop that takes two passes to complete", background: "#F0E8DA", imageUrl: "/prints/cycles/cycles_moebius.jpg", price: 45 },
      { id: "cycles-seasons", title: "Seasons", series: "cycles", equation: "T(t) = T̄ + A·sin(2πt/P + φ)", description: "Layers of years stacked on top of each other — warming and cooling, warming and cooling. The same shape every time, but none identical. I grew up in a place with real seasons, and the thing about them is you think you remember what winter feels like until it comes back and surprises you again.", emotionalNote: "The same rhythm, never the same amplitude", background: "#F0E8DA", imageUrl: "/prints/cycles/cycles_seasons.jpg", price: 45 },
      { id: "cycles-loom", title: "Loom", series: "cycles", equation: "x(t) = x(t + T), T = 2π/ω", description: "I wanted to show what repetition builds. Threads crossing at exact intervals, each one predictable alone, but the fabric they make is something neither could be. That's what cycles do if you stay with them long enough — the routine becomes the structure you live inside.", emotionalNote: "Rhythm weaving itself into something solid", background: "#F0E8DA", imageUrl: "/prints/cycles/cycles_loom.jpg", price: 45 },
      { id: "cycles-tidal", title: "Tidal", series: "cycles", equation: "h(t) = Σ Aₙcos(ωₙt + φₙ)", description: "The ocean responding to something it can't see. Lunar and solar gravity pulling from different distances, their rhythms superimposed into the rise and fall of water — a cycle governed by forces far away and utterly silent. The ocean doesn't know why it moves. It just does.", emotionalNote: "The ocean responding to something it can't see", background: "#F0E8DA", imageUrl: "/prints/cycles/cycles_tidal.jpg", price: 45 },
      { id: "cycles-phase-portrait", title: "Phase Portrait", series: "cycles", equation: "x'' − μ(1−x²)x' + x = 0", description: "Every path spirals toward the same loop. It doesn't matter where you start — different speeds, different angles, different intentions — you end up tracing the same orbit. Some patterns are that strong. Built from the Van der Pol oscillator, where every trajectory converges to a single limit cycle.", emotionalNote: "Every starting point leads to the same loop", background: "#F0E8DA", imageUrl: "/prints/cycles/cycles_phase_portrait.jpg", price: 45 },
      { id: "cycles-breathing", title: "Breathing", series: "cycles", equation: "r(t) = r₀ + A·sin(ωt + φ)", description: "Expand. Contract. Repeat. The simplest cycle there is — lungs filling and emptying, the body's most fundamental rhythm reduced to concentric circles. Nothing needs to be added.", emotionalNote: "Expand, contract, repeat", background: "#F0E8DA", imageUrl: "/prints/cycles/cycles_breathing.jpg", price: 45 },
    ],
  },

  // ── SOLITUDE ────────────────────────────────────────────
  {
    id: "solitude",
    name: "SOLITUDE",
    seoDescriptor: "Minimalist Abstract Art Prints About Aloneness and Space",
    emotion: "aloneness, vast space, a single presence",
    tagline: "One point in an infinite plane. One signal in silence. The mathematics of being the only thing present.",
    description: "Isolated points, single signals in vast fields, lighthouse beacons, island topologies, and echo functions. The mathematics of being alone — not lonely, but singular.",
    story: "Solitude is not loneliness. It is the experience of being the only signal in a vast field. The mathematics of isolation is sparse: a single point, a single frequency, a single source of light. This series uses extreme negative space to render that singularity.",
    mathematicalPrimitive: "isolated points, sparse signals, single-source propagation",
    background: "#E0DDD6",
    palette: ["#404850", "#2A4A3A", "#C8963A", "#5A6878", "#D4A840"],
    makingOf: "62 renders. 5 survived.",
    pieces: [
      { id: "solitude-signal", title: "Signal", series: "solitude", equation: "S(f) = A·δ(f−f₀) + η", description: "One clear voice in a room full of noise. I filled the canvas with overlapping frequencies — static from every direction — and then placed one gold line rising above it all. It's not trying to be louder. It's just different enough to be unmistakable. Singular, not lonely.", emotionalNote: "One clear voice in a room full of noise", background: "#E0DDD6", imageUrl: "/prints/solitude/solitude_signal.jpg", price: 45 },
      { id: "solitude-basin", title: "Basin", series: "solitude", equation: "y = a(x−h)² + k", description: "Most settle where it's comfortable — at the bottom, where the curve is flat and the energy is lowest. One has climbed to the rim, alone at the edge of the rising wall. What made it leave?", emotionalNote: "The one who climbed out of the comfortable minimum", background: "#E0DDD6", imageUrl: "/prints/solitude/solitude_basin.jpg", price: 45 },
      { id: "solitude-drift", title: "Drift", series: "solitude", equation: "η(x) = A₁sin(k₁x + φ₁) + A₂cos(k₂x + φ₂)", description: "Twenty-eight currents flowing horizontally, and one gold line cutting diagonally across all of them. Not fighting the motion, not following it — just passing through on its own trajectory. I think solitude is sometimes like that. You're in the same world as everyone else. You're just moving through it differently.", emotionalNote: "Riding the crests, surfing from one wave to the next", background: "#E0DDD6", imageUrl: "/prints/solitude/solitude_drift.jpg", price: 45 },
      { id: "solitude-shadow", title: "Shadow", series: "solitude", equation: "I(x) = I₀·e^(−μx)", description: "One presence and the proof that it exists. A single gold form casting a long diagonal shadow across the canvas — the kind of aloneness that still leaves a mark on everything around it.", emotionalNote: "One presence and the proof that it exists", background: "#E0DDD6", imageUrl: "/prints/solitude/solitude_shadow.jpg", price: 45 },
      { id: "solitude-skyline", title: "Skyline", series: "solitude", equation: "y_i = β(2,3)·H + ε", description: "Separated from everything below by pure empty space. A dense band of lines near the bottom and one gold line floating high above — not fleeing, not lost, just elsewhere. The distance is the point.", emotionalNote: "Separated from everything below by pure empty space", background: "#E0DDD6", imageUrl: "/prints/solitude/solitude_skyline.jpg", price: 45 },
    ],
  },

  // ── NOSTALGIA ───────────────────────────────────────────
  {
    id: "nostalgia",
    name: "NOSTALGIA",
    seoDescriptor: "Minimalist Abstract Art Prints About Memory and Warmth",
    emotion: "remembering, fading, the warmth of what was",
    tagline: "Memory with its edges removed. The warmth stays. The details blur. Nothing quite comes back the same.",
    description: "Reaching stems, inherited forms, spirals that never close, and colors that bleed. The mathematics of memory — blurred, warm, and slowly losing resolution.",
    story: "Nostalgia is memory with its high frequencies removed. The details blur but the warmth remains. A low-pass filter does exactly this — it removes sharp edges and rapid changes, leaving only the slow, smooth underlying signal. This series renders that filtering as visual art.",
    mathematicalPrimitive: "low-pass filtering, harmonic decay, photographic degradation",
    background: "#F0E8D8",
    palette: ["#C8A060", "#A08040", "#E0C880", "#887030", "#D8B870"],
    makingOf: "42 renders. 4 survived.",
    pieces: [
      { id: "nostalgia-reaching", title: "Reaching", series: "nostalgia", equation: "y(t) → ∞, ∂y/∂t → 0", description: "Moving forward but always reaching backward. A bold stem rising from an amber origin, thinning as it climbs, tendrils arcing off and sweeping back toward where it started. I couldn't make it stop reaching back.", emotionalNote: "Moving forward but always reaching backward", background: "#F0E8D8", imageUrl: "/prints/nostalgia/nostalgia_reaching.jpg", price: 45 },
      { id: "nostalgia-heirloom", title: "Heirloom", series: "nostalgia", equation: "Sₙ = (1+εₙ)·λ·Sₙ₋₁", description: "What is handed down is never perfectly preserved. It changes in the carrying — slightly altered, slightly marked, made more intimate by use. Each form a little less precise than the last, a little more itself.", emotionalNote: "Each copy a little less precise than the last", background: "#F0E8D8", imageUrl: "/prints/nostalgia/nostalgia_heirloom.jpg", price: 45 },
      { id: "nostalgia-saudade", title: "Saudade", series: "nostalgia", equation: "r(θ) = r₀ + εθ + a·sin(3θ)", description: "Almost closing. Always drifting. Spirals that keep trying to return to where they started but never quite get there — each orbit a near-miss, close enough to feel like home but always slightly off. Named for the Portuguese word for longing without an object.", emotionalNote: "Almost closing, always drifting", background: "#F0E8D8", imageUrl: "/prints/nostalgia/nostalgia_saudade.jpg", price: 45 },
      { id: "nostalgia-sepia", title: "Sepia", series: "nostalgia", equation: "Σ αₖ·G(x,y;μₖ,σₖ)", description: "A memory recalled so many times the edges are gone. Overlapping washes of amber and ochre bleeding into each other — the soft focus of something you've replayed until the details are warm and unreliable. Built from superimposed Gaussian distributions, the mathematics of blurring.", emotionalNote: "A memory recalled so many times the edges are gone", background: "#F0E8D8", imageUrl: "/prints/nostalgia/nostalgia_sepia.jpg", price: 45 },
    ],
  },

  // ── DESIRE ──────────────────────────────────────────────
  {
    id: "desire",
    name: "DESIRE",
    seoDescriptor: "Minimalist Abstract Art Prints About Longing and Gravity",
    homeDescriptor: "Abstract prints in crimson, ember, and burnished brass, built from pursuit curves, magnetic dipoles, logistic thresholds, and the inspiral of orbital decay.",
    emotion: "wanting, pull, gravitational attraction",
    tagline: "The ache of approach. Pursuit curves that never close. The pull that accelerates as you get closer.",
    description: "Pursuit curves, magnetic attraction, accelerating pulses, threshold crossings, and gravitational inspiral. Systems pulled toward something they cannot reach — with increasing urgency.",
    story: "Desire is a force field. It has direction, magnitude, and a source. The mathematics of attraction — gravitational wells, pursuit curves, orbital decay — describe systems that are pulled toward something with increasing urgency. This series renders that pull.",
    mathematicalPrimitive: "gravitational attraction, pursuit curves, orbital decay",
    background: "#E8D8D0",
    palette: ["#9A2030", "#C88030", "#D06020", "#B83040", "#C4A040"],
    makingOf: "20 renders. 5 survived.",
    homePieceIds: ["desire-pursuit", "desire-magnetism", "desire-threshold"],
    pieces: [
      { id: "desire-pursuit", title: "Pursuit", series: "desire", equation: "dx/dt=αx−βxy, dy/dt=δxy−γy", description: "I tried to make them meet. They won't — they circle each other endlessly, always closing the distance, never arriving. The system doesn't allow it. The approach is the point, not the arrival. That ache of almost-touching is where desire actually lives.", emotionalNote: "Endless approach, never arrival", background: "#E8D8D0", imageUrl: "/prints/desire/desire_pursuit.jpg", price: 45 },
      { id: "desire-threshold", title: "Threshold", series: "desire", equation: "y=L/(1+e^(−k(t−t₀)))", description: "There is a moment when wanting stops being quiet. What begins as pressure becomes certainty; what was held back starts to move. I kept looking for that point of no return — the instant feeling becomes action. Built from a logistic threshold, the curve of slow build, sudden turning, and irreversible change.", emotionalNote: "Rising toward a line that can never be crossed", background: "#E8D8D0", imageUrl: "/prints/desire/desire_threshold.jpg", price: 45 },
      { id: "desire-magnetism", title: "Magnetism", series: "desire", equation: "B=μ₀/(4π)·(3(m·r̂)r̂−m)/r³", description: "The pull you can feel but can't see. Invisible force arcing between two bodies, shaping the space around them, bending every nearby path. You know it's there because everything curves. I wanted to render that — the thing that isn't visible but reshapes everything around it.", emotionalNote: "The pull you can feel but can't see", background: "#E8D8D0", imageUrl: "/prints/desire/desire_magnetism.jpg", price: 45 },
      { id: "desire-inspiral", title: "Inspiral", series: "desire", equation: "r(θ)=r₀·e^(−γθ)", description: "Accelerating toward something you can't stop. Concentric spirals tightening toward a glowing center, each orbit faster and closer than the last. I kept watching the curves accelerate inward and thought — that's what it feels like. The closer you get, the less choice you have.", emotionalNote: "Accelerating toward something you can't stop", background: "#E8D8D0", imageUrl: "/prints/desire/desire_inspiral.jpg", price: 45 },
      { id: "desire-pulse", title: "Pulse", series: "desire", equation: "f(t)=A·exp(−(t mod T)/σ)", description: "A heartbeat that won't slow down. Peaked waveforms accelerating — spacing tightening, amplitude rising, each beat arriving sooner and harder than the last. The rhythm of wanting something more with every passing moment.", emotionalNote: "A heartbeat that won't slow down", background: "#E8D8D0", imageUrl: "/prints/desire/desire_pulse.jpg", price: 45 },
    ],
  },

  // ── SURRENDER ───────────────────────────────────────────
  {
    id: "surrender",
    name: "SURRENDER",
    seoDescriptor: "Minimalist Abstract Art Prints About Release and Letting Go",
    emotion: "letting go, release, allowing the fall",
    tagline: "The moment resistance gives way. Not collapse — completion. The mathematics of ceasing to fight.",
    description: "Settling oscillations, softening edges, and converging streams. Systems that stop resisting and allow the natural process to complete.",
    story: "Surrender is not defeat. It is the moment a system stops expending energy to resist and allows the natural process to complete. A particle settling in fluid, a solid melting, a leaf releasing from its branch. These are not failures — they are completions.",
    mathematicalPrimitive: "dissolution, settling, laminar flow, phase transition",
    background: "#E4E0DC",
    palette: ["#5A5048", "#7A7068", "#9A9088", "#B0A898", "#C8C0B4"],
    makingOf: "59 renders. 5 survived.",
    pieces: [
      { id: "surrender-settle", title: "Settle", series: "surrender", equation: "y(t) = y_eq + (y₀ − y_eq)·e^(−t/τ)·cos(ω_d·t)", description: "Everything finding the same quiet. Twenty-four oscillations releasing their energy symmetrically around a rest point — each swing smaller than the last, the motion softening until stillness arrives. Not forced. Earned.", emotionalNote: "Everything finding the same quiet", background: "#E8E4DE", imageUrl: "/prints/surrender/surrender_settle.jpg", price: 45 },
      { id: "surrender-melt", title: "Melt", series: "surrender", equation: "r(θ,s) = (1−s)·r_sq(θ) + s·r_circ", description: "Letting go of edges without breaking. A rigid square softening into a circle through twenty-two stages — not collapsing, not failing, just releasing the tension of holding a shape it no longer needs. Built from geometric interpolation between angular and circular forms.", emotionalNote: "Letting go of edges without breaking", background: "#E8E4DE", imageUrl: "/prints/surrender/surrender_melt.jpg", price: 45 },
      { id: "surrender-flow", title: "Flow", series: "surrender", equation: "dY = μ(Y_flow − Y)·dt + σ(1−t)·dW", description: "Thirty separate paths, each with its own starting angle, each following its own line. Then the current. One by one they stop resisting and join the same direction — nobody forced them, nobody asked. They just stopped fighting what was already moving.", emotionalNote: "Separate paths joining one current", background: "#E8E4DE", imageUrl: "/prints/surrender/surrender_flow.jpg", price: 45 },
    ],
  },

  // ── WONDER ──────────────────────────────────────────────
  {
    id: "wonder",
    name: "WONDER",
    seoDescriptor: "Cosmic Generative Art Prints About Hidden Order and Structure",
    homeDescriptor: "Cosmic generative prints in deep blue and pale violet, built from Apollonian circle packings, conformal inversions, and the recursive depth of nested infinity.",
    emotion: "awe at structure, the surprise of hidden order",
    tagline: "The feeling of going deeper and finding no end. Recursive depth, strange attractors, patterns that never repeat.",
    description: "Recursive landscapes, strange attractors, conformal transformations, and infinite circle packings. Mathematics that reveals unexpected beauty — order emerging from simple rules.",
    story: "Wonder is the feeling of encountering structure where you expected chaos. A fractal that generates infinite complexity from three lines of code. A strange attractor that never repeats but always stays bounded. This series renders the mathematics that provokes that feeling.",
    mathematicalPrimitive: "fractals, strange attractors, recursive geometry",
    background: "#0A0A18",
    palette: ["#4080C0", "#60A0E0", "#80C0FF", "#2060A0", "#A0D0FF"],
    makingOf: "72 renders. 5 survived.",
    homePieceIds: ["wonder-apollonian-gasket", "wonder-meditation"],
    pieces: [
      { id: "wonder-apollonian-gasket", title: "Apollonian Gasket", series: "wonder", equation: "k₄ = k₁+k₂+k₃ + 2√(k₁k₂+k₂k₃+k₁k₃)", description: "Infinity nested in the cracks between things. Three circles touching inside a fourth, and in every gap, the largest circle that fits. Repeat. The gaps never fill completely — there's always room for one more, smaller and smaller, forever. The deeper you look, the more there is. Built from Apollonian circle packing, where infinity hides in the spaces between.", emotionalNote: "Infinity nested in the cracks between things", background: "#DDD9D2", imageUrl: "/prints/wonder/wonder_apollonian_gasket.jpg", price: 45 },
      { id: "wonder-transform", title: "Transform", series: "wonder", equation: "w = z + a/(z − z₀)", description: "The small circle is you, the viewer. Looking right, you take in the world — information flowing outward, sweeping wide. But the curves loop back, returning to reshape the observer. Perception becomes reality becomes perception again. A conformal mapping as feedback loop.", emotionalNote: "Perception shapes reality shapes perception", background: "#DDD9D2", imageUrl: "/prints/wonder/wonder_transform.jpg", price: 45 },
      { id: "wonder-meditation", title: "Meditation", series: "wonder", equation: "w = R²/z̄", description: "Ten days of silence. Somewhere around day seven, the boundary between body and mind stopped meaning anything. Not dissolved — inverted. What had been two separate experiences became one field, and in the narrow passage between them, something opened that I'd never felt before. This piece came from that. Parallel lines pass through a circle inversion and become arcs that converge on a single luminous point — the place where separation ends and a new dimension of experience begins.", emotionalNote: "What opens when body and mind stop being two things", background: "#DDD9D2", imageUrl: "/prints/wonder/wonder_meditation.jpg", price: 45 },
    ],
  },

  // ── HUMILITY ───────────────────────────────────────────
  {
    id: "humility",
    name: "HUMILITY",
    seoDescriptor: "Minimalist Abstract Art Prints About Scale and Proportion",
    emotion: "proportion restored, the self in context of vastness",
    tagline: "The mathematics of smallness. Convergence and the quiet that comes from knowing your scale.",
    description: "Converging field lines and plumb lines. Systems that locate a single point inside something immeasurably larger — and find peace there.",
    story: "Humility isn't self-erasure. It's proportion. A plumb line finds true vertical — not by assertion but by letting gravity decide. This piece renders the mathematics of locating yourself accurately inside something vast.",
    mathematicalPrimitive: "convergence, gravitational alignment",
    background: "#CCC2AA",
    palette: ["#50A0D0", "#7868D0", "#C06060", "#D09040", "#F0D040"],
    makingOf: "40 renders. 1 survived.",
    pieces: [
      { id: "humility-plumb", title: "Plumb", series: "humility", equation: "lim_{n→∞} x_n = c, ∇·g = −4πGρ", description: "Forty lines converging on a single point of light, then a plumb line dropping from it. Everything above is searching; everything below has found its answer. I wanted to render the moment proportion is restored — when the self stops asserting and lets gravity decide what's true.", emotionalNote: "Letting gravity decide what's true", background: "#CCC2AA", imageUrl: "/prints/humility/humility_plumb.jpg", price: 45 },
    ],
  },

  // ── PEACE ───────────────────────────────────────────────
  {
    id: "peace",
    name: "PEACE",
    seoDescriptor: "Blue Minimalist Abstract Art Prints About Stillness",
    homeDescriptor: "Minimalist prints in sage and seafoam, built from Laplacian equilibrium, equipotential contours, and the single horizon line where every force has balanced.",
    emotion: "stillness, resolution, equilibrium achieved",
    tagline: "After all forces have balanced. Sand shaped by wind. Water with no gradient. The mathematics of having arrived.",
    description: "Horizons, breathing forms, drifting clouds, standing waves, and still water. Systems that have found their equilibrium and hold it.",
    story: "Peace is not the absence of force. It is the state after all forces have balanced. The Laplace equation describes this: ∇²f = 0 means every point is the average of its neighbors. No tension. No gradient. Every point in agreement with its surroundings.",
    mathematicalPrimitive: "Laplacian equilibrium, steady-state, resolved harmonics",
    background: "#F0EDE8",
    palette: ["#B0C8B8", "#90B0A0", "#A8C0B0", "#78A090", "#D0E0D0"],
    makingOf: "20 renders. 7 survived.",
    homePieceIds: ["peace-field-guardian", "peace-horizon", "peace-breath"],
    pieces: [
      { id: "peace-field-guardian", title: "Guardian", series: "peace", equation: "V(r) = q₁/|r−r₁| + q₂/|r−r₂|", description: "Two charges, one large and one small. The larger field wraps around the smaller one the way a parent's calm extends around a child. Equipotential contour lines trace the invisible architecture of protection. Not symmetry — shelter.", emotionalNote: "The invisible architecture of protection", background: "#F0EDE8", imageUrl: "/prints/peace/peace_field_guardian.jpg", price: 45 },
      { id: "peace-horizon", title: "Horizon", series: "peace", equation: "y → c as x → ±∞", description: "Everything stripped down to one line. Layered atmospheric bands resolving into the single boundary between sky and earth — the simplest possible landscape. I kept removing things until only the horizon was left.", emotionalNote: "Everything stripped down to one line", background: "#F0EDE8", imageUrl: "/prints/peace/peace_horizon.jpg", price: 45 },
      { id: "peace-enso-dialogue", title: "Dialogue", series: "peace", equation: "r(θ) = R + Σ aₖsin(kθ + φₖ), k ∈ {1,2,3,5,8}", description: "Two imperfect circles, ocean and sage, overlapping like two people in conversation. They weave over and under each other at the crossings — neither one dominates. Each circle is its own breath, its own arc, but they share the space between them.", emotionalNote: "Neither one dominates", background: "#F0EDE8", imageUrl: "/prints/peace/peace_enso_dialogue.jpg", price: 45 },
      { id: "peace-breath", title: "Breath", series: "peace", equation: "A(t) = A₀·sin(2πt/T)", description: "Concentric rings expanding on the inhale, contracting on the exhale. I timed them to a breathing rhythm — the simplest cycle the body knows. There's nothing else in the frame because nothing else is needed.", emotionalNote: "Breathing made visible", background: "#F0EDE8", imageUrl: "/prints/peace/peace_breath.jpg", price: 45 },
      { id: "peace-harmonic", title: "Harmonic", series: "peace", equation: "ψ = A·sin(nπx/L)·sin(nπy/L)", description: "Every frequency found its place and stayed there. Standing waves layered at different modes, each one coexisting without interfering with the others — like a room where every voice has found its register and nobody needs to be louder. Sound that has resolved into structure.", emotionalNote: "Vibration that found its form and keeps it", background: "#F0EDE8", imageUrl: "/prints/peace/peace_harmonic.jpg", price: 45 },
      { id: "peace-cloud", title: "Cloud", series: "peace", equation: "ρ(x,y) = Σ Gₖ(x,y,σₖ)", description: "Nothing needs to happen here. Soft overlapping forms drifting in still air — no edges, no urgency, no destination. Just presence, weightless and unhurried.", emotionalNote: "Nothing needs to happen here", background: "#F0EDE8", imageUrl: "/prints/peace/peace_cloud.jpg", price: 45 },
    ],
  },

  // ── AWE ─────────────────────────────────────────────────
  {
    id: "awe",
    name: "AWE",
    seoDescriptor: "Cosmic Abstract Art Prints About Scale and the Sublime",
    homeDescriptor: "Cosmic abstract prints in gold, indigo, and deep violet, built from solar coronas, gravitational lensing, and the inverse-square radiance of distant stars.",
    emotion: "overwhelmed by scale, the sublime",
    tagline: "The cosmic sublime. Solar coronas, gravitational waves, ten thousand galaxies in a single frame.",
    description: "Eclipse coronas, black hole accretion, flocking algorithms, inverse-square radiance, and the large-scale structure of the universe. Mathematics at scales where comprehension dissolves into wonder.",
    story: "Awe is the emotion at the boundary of comprehension. Burke called it the sublime — the overwhelming encounter with something vast. Standing under the Milky Way, watching a solar eclipse, seeing the Hubble Deep Field. This series renders the mathematics of cosmic scale: gravitational lensing, stellar death, light itself.",
    mathematicalPrimitive: "inverse-square law, orbital mechanics, blast waves, gravitational lensing",
    background: "#0A0A10",
    palette: ["#D0A040", "#C88030", "#D4AA40", "#3A5AA0", "#5A3A8A"],
    makingOf: "20 renders. 8 survived.",
    homePieceIds: ["awe-eclipse", "awe-radiance", "awe-singularity"],
    pieces: [
      { id: "awe-eclipse", title: "Eclipse", series: "awe", equation: "I(r) = I_corona / r", description: "What the sun reveals only when it's hidden. Streamers of plasma radiating outward during totality, a diamond ring at the limb — the corona visible for a few minutes of darkness. Built from an inverse-distance field, the math the sun actually follows.", emotionalNote: "What the sun reveals only when it's hidden", background: "#534027", imageUrl: "/prints/awe/awe_eclipse.jpg", price: 45 },
      { id: "awe-singularity", title: "Singularity", series: "awe", equation: "r(φ) = a(1-e²)/(1+e·cosφ)", description: "Where gravity bends light and time stops. An accretion disk spiraling into a black hole, light paths curving around the event horizon, time dilating to infinity at the photon sphere. The math is real. Built from relativistic orbital mechanics and gravitational lensing.", emotionalNote: "Where gravity bends light and time stops", background: "#0A0A10", imageUrl: "/prints/awe/awe_singularity.jpg", price: 45 },
      { id: "awe-radiance", title: "Radiance", series: "awe", equation: "I(r) = I₀/r²", description: "Light that never quite reaches zero. One hundred twenty rays streaming from a brilliant center, each dimming with distance but never disappearing — no matter how far you go. The stubbornness of what shines.", emotionalNote: "Light that never quite reaches zero", background: "#0A0A10", imageUrl: "/prints/awe/awe_radiance.jpg", price: 45 },
      { id: "awe-cosmic-web", title: "Cosmic Web", series: "awe", equation: "ρ(r) ~ Σ G_ij / r", description: "The skeleton of everything. Galaxies connected by dark matter filaments, nodes glowing where the threads converge. This is what the universe looks like from far enough away.", emotionalNote: "The skeleton of everything", background: "#151b31", imageUrl: "/prints/awe/awe_cosmic_web.jpg", price: 45 },
      { id: "awe-deep-field", title: "Deep Field", series: "awe", equation: "N(>S) ~ S^{-3/2}", description: "Every speck is an entire galaxy. Ten thousand points of light at every depth — spirals, ellipticals, faint smears of color. The image that made humanity realize how small we are.", emotionalNote: "Every speck is an entire galaxy", background: "#0A0A10", imageUrl: "/prints/awe/awe_deep_field.jpg", price: 45 },
      { id: "awe-gravitational-waves", title: "Gravitational Waves", series: "awe", equation: "h(r,t) = A·cos(kr-ωt)/r", description: "Spacetime itself stretching and compressing. Ripples expanding outward from two merging black holes — not moving through space, but moving space. LIGO detected these. They're real.", emotionalNote: "Ripples in spacetime that were actually detected", background: "#23345e", imageUrl: "/prints/awe/awe_gravitational_waves.jpg", price: 45 },
      { id: "awe-murmuration", title: "Murmuration", series: "awe", equation: "v_i = α·align + β·cohere + γ·separate", description: "No choreographer. No conductor. Just three simple rules — align, cohere, separate — and 1,400 particles sweep through the frame like a flock of starlings turning in unison. I didn't choreograph any of it. The collective intelligence just emerged.", emotionalNote: "Three rules, no choreography", background: "#1E2030", imageUrl: "/prints/awe/awe_murmuration.jpg", price: 45 },
      { id: "awe-overview", title: "Overview", series: "awe", equation: "h/R ≈ 0.01‰", description: "Everything is under that thin line. Earth's atmosphere as a luminous arc against the void — drawn to scale. The line is impossibly thin. Everything anyone has ever known, felt, built, or loved exists beneath it.", emotionalNote: "Everything is under that thin line", background: "#0A0A10", imageUrl: "/prints/awe/awe_overview.jpg", price: 45 },
    ],
  },

  // ── RESILIENCE ──────────────────────────────────────────
  {
    id: "resilience",
    name: "RESILIENCE",
    seoDescriptor: "Minimalist Abstract Art Prints About Recovery and Repair",
    emotion: "recovery, repair, growing back stronger",
    tagline: "Stronger where it was hit. Systems that break and reform past where they started.",
    description: "Strain hardening, post-traumatic growth, and overshoot recovery. Systems that return — often stronger — after being pushed past their limits.",
    story: "Resilience is not endurance. Endurance holds. Resilience breaks and reforms. The mathematics of recovery — systems that overshoot their original baseline after perturbation, materials that harden under stress, networks that reroute around damage — describe the geometry of coming back.",
    mathematicalPrimitive: "overshoot recovery, strain hardening, network repair",
    background: "#E8E0D8",
    palette: ["#A06020", "#C08030", "#806018", "#E0A040", "#604010"],
    makingOf: "56 renders. 3 survived.",
    pieces: [
      { id: "resilience-forged", title: "Forged", series: "resilience", equation: "σ_y(ε) = σ₀ + Kε^n", description: "I kept hitting it and it kept getting stronger. Layer after layer of stress, each deformation raising the threshold for the next one — bands of increasing density, each one harder than the last. What should have weakened it made it more resistant.", emotionalNote: "Stronger at every point it was hit", background: "#E8E0D8", imageUrl: "/prints/resilience/resilience_forged.jpg", price: 45 },
      { id: "resilience-phoenix", title: "Phoenix", series: "resilience", equation: "f(t) = A(1 - e^{-t/τ₁})e^{t/τ₂}, τ₂ > τ₁", description: "A sharp plunge, then a long rising arc that clears the starting line. The function drops to nearly nothing and comes back with more than it lost. I made the overshoot dramatic on purpose — that upward sweep past the origin is the whole point of the piece.", emotionalNote: "Not just recovery — beyond where you started", background: "#E8E0D8", imageUrl: "/prints/resilience/resilience_phoenix.jpg", price: 45 },
      { id: "resilience-recovery", title: "Recovery", series: "resilience", equation: "x(t) = x_eq + (x₀-x_eq)e^{-t/τ} + overshoot", description: "Wide oscillations narrowing, each one overshooting less, until the motion goes quiet. The system doesn't come back gently — it overcorrects, swings too far, then slowly finds center. I kept the early overcorrections visible. They're messy and imprecise, but that's what healing actually looks like.", emotionalNote: "Swinging past center before finding balance", background: "#E8E0D8", imageUrl: "/prints/resilience/resilience_recovery.jpg", price: 45 },
    ],
  },

  // ── TRUST ───────────────────────────────────────────────
  {
    id: "trust",
    name: "TRUST",
    seoDescriptor: "Minimalist Abstract Art Prints About Synchrony and Rhythm",
    emotion: "synchrony, mutual vulnerability, shared rhythm",
    tagline: "Choosing the same rhythm without being asked. The mathematics of mutual vulnerability.",
    description: "Synchronized breathing, mutual recognition, delayed mirroring, and interlocking trajectories. Two systems choosing to align — weaving patterns that neither could produce alone.",
    story: "Trust is not certainty. It is the willingness to synchronize with another system without guarantees. The mathematics of trust involves mutual phase-locking — two oscillators that choose to align, weaving patterns that neither could produce alone.",
    mathematicalPrimitive: "synchronization, mutual phase-locking, weaving, handshake",
    background: "#E8E4E0",
    palette: ["#506878", "#687888", "#788898", "#405868", "#8898A8"],
    makingOf: "37 renders. 5 survived.",
    pieces: [
      { id: "trust-breath-together", title: "Breath Together", series: "trust", equation: "φ₁(t) - φ₂(t) → 0 as t → ∞", description: "Two oscillators that sync up — not because they're forced to, but because the coupling lets them. Nobody asked them to breathe together. They just did. I kept watching it happen and couldn't figure out who started first.", emotionalNote: "Choosing the same rhythm without being asked", background: "#E8E4E0", imageUrl: "/prints/trust/trust_breath_together.jpg", price: 45 },
      { id: "trust-handshake", title: "Handshake", series: "trust", equation: "SYN → SYN-ACK → ACK", description: "I reach out. You acknowledge. I confirm. Three signals — that's all trust is at the start. A hand extended, a hand taken, a shared recognition that both sides showed up. Before anything else can happen, this has to.", emotionalNote: "I reach out. You respond. I confirm.", background: "#E8E4E0", imageUrl: "/prints/trust/trust_handshake.jpg", price: 45 },
      { id: "trust-mirror", title: "Mirror", series: "trust", equation: "y₁(t) = αy₂(t-τ) + (1-α)y₁(t-τ)", description: "Following without losing yourself. One system tracking the other with a slight delay — not copying, but responding. The balance has to be right. Too much mimicry and one voice drowns. Too little and they drift apart.", emotionalNote: "Following without losing yourself", background: "#E8E4E0", imageUrl: "/prints/trust/trust_mirror.jpg", price: 45 },

      { id: "trust-weave", title: "Weave", series: "trust", equation: "f(x,y) = sin(x)sin(y) + sin(x)cos(y)", description: "Neither strong alone. Together they hold. Two functions interlocking — warp and weft creating a fabric that neither thread could be on its own. The strength is in the crossing.", emotionalNote: "Neither strong alone, together they hold", background: "#E8E4E0", imageUrl: "/prints/trust/trust_weave.jpg", price: 45 },
    ],
  },

  // ── PRIDE ───────────────────────────────────────────────
  {
    id: "pride",
    name: "PRIDE",
    seoDescriptor: "Minimalist Abstract Art Prints About Identity and Solidarity",
    emotion: "identity, solidarity, sheltering one another, standing together",
    tagline: "Superellipse arches, ocean harmonics, and interlocking weaves. The mathematics of being proud of who you are — and standing together.",
    description: "Pride is about your unique glow and light and identity. It is also about standing together — protecting each other, weaving resilience from individual strands, being different waves but moving as one ocean.",
    story: "Pride is being proud of who you are. Your unique light, your identity, your glow. But pride is also what happens when those lights stand together. Superellipse arches — y = h(1−|s|^p) — nest inside each other, each curve sheltering the one beneath it. The exponent p softens each arch differently, but they all share the same center. That is protection. Ocean wave equations — h = ΣAᵢcos(kᵢx−ωᵢt) — layer seventy-eight lines through the full LGBTQ+ spectrum, each wave its own color and frequency, but all of them part of the same sea. That is unity without sameness. Unfurling curves — x = x₀ + A·sⁿ·sin(ωs) — start from a single shared root and find their own paths upward, diverging but never disconnected. Different destinations from the same origin. Interlocking sinusoidal strands — f(x,y) = A·sin(ω₁x)·sin(ω₂y) — weave trans and rainbow palettes into fabric. No single thread holds alone. The strength is in the crossing. That is resilience. And gaussian bumps on converging perspective lines — y = Σhᵢe^(−(t−cᵢ)²/2wᵢ²) — turn a vanishing-point road into something that has been traveled. The bumps aren't even. Some cluster, some come alone. The road ahead has bumps too. That is honesty.",
    mathematicalPrimitive: "superellipse nesting, wave superposition, parametric divergence, sinusoidal weave, gaussian perspective road",
    background: "#f3eee7",
    palette: ["#f6f2ef", "#f5a9b8", "#5bcffb", "#ffd100", "#7f2dbd"],
    makingOf: "New series — building out.",
    pieces: [
      { id: "pride-waves", title: "Waves", series: "pride", equation: "h = ΣAᵢcos(kᵢx−ωᵢt)", description: "Many waves, one sea. Seventy-eight ocean lines moving through the full LGBTQ+ spectrum — trans blue, pink, and white woven through the classic rainbow. Every color its own frequency, every frequency part of the same water.", emotionalNote: "Many waves, one sea", background: "#f3eee7", imageUrl: "/prints/pride/pride_waves.jpg", price: 45 },
      { id: "pride-woven-resilience", title: "Woven Resilience", series: "pride", equation: "f(x,y) = A·sin(ω₁x+φ)·sin(ω₂y+ψ)", description: "Trans palette woven through rainbow — eighteen horizontal strands interlocking with eighteen vertical strands, each one visible and distinct. Fabric doesn't work as individual threads. It only holds when they cross. That's the whole point.", emotionalNote: "The strength is in the crossing", background: "#f3eee7", imageUrl: "/prints/pride/pride_woven_resilience.jpg", price: 45 },
      { id: "pride-unfurling", title: "Unfurling", series: "pride", equation: "x = x₀ + A·sⁿ·sin(ωs)", description: "Something contained, choosing to open. Sixty-two lines rooted at a single point, unfurling upward through the full LGBTQ+ spectrum — each one finding its own path from the same origin. Different destinations, one beginning.", emotionalNote: "Something contained, choosing to open", background: "#f3eee7", imageUrl: "/prints/pride/pride_unfurling.jpg", price: 45 },
      { id: "pride-shelter", title: "Shelter", series: "pride", equation: "y = h(1−|s|^p)", description: "Each arch protecting the one beneath it. Twenty-four curves nested inside each other — every one smaller and softer than the one outside it. Every arch is someone standing over someone else so they don't have to stand alone.", emotionalNote: "Each arch protecting the one beneath it", background: "#f3eee7", imageUrl: "/prints/pride/pride_shelter.jpg", price: 45 },
    ],
  },

  // ── LONGING ─────────────────────────────────────────────
  {
    id: "longing",
    name: "LONGING",
    seoDescriptor: "Minimalist Abstract Art Prints About Distance and Reaching",
    emotion: "reaching toward what recedes, the ache of distance",
    tagline: "Always halving the distance, never arriving. The geometry of wanting what stays just beyond.",
    description: "Damped oscillations, magnetic near-misses, unreachable limits, and vanishing points. The mathematics of distance that cannot be closed.",
    story: "Longing is Zeno's paradox made emotional. You halve the distance, then halve it again, always approaching, never arriving. The mathematics of asymptotic approach — functions that tend toward a limit they will never reach — perfectly describe the geometry of wanting something that remains just beyond.",
    mathematicalPrimitive: "asymptotic approach, harmonic decay, vanishing point, Zeno's paradox",
    background: "#E0E4E8",
    palette: ["#6080A0", "#8090A0", "#4060A0", "#A0B0C0", "#506890"],
    makingOf: "51 renders. 3 survived.",
    pieces: [
      { id: "longing-harmonic-decay", title: "Harmonic Decay", series: "longing", equation: "f(t) = A₀ · cos(ωt) · e^{-γt}", description: "I set an oscillation going and watched it fade. Each swing shorter, each return weaker, but it never fully stopped — the motion kept coming back, diminished, reaching for an amplitude it used to have. That's what longing sounds like to me. The echo of something that's still moving inside you.", emotionalNote: "Fading without ever disappearing", background: "#E0E4E8", imageUrl: "/prints/longing/longing_harmonic_decay.jpg", price: 45 },
      { id: "longing-magnetic", title: "Magnetic", series: "longing", equation: "F = μ₀m₁m₂/(4πr²)", description: "Reaching across empty space without connecting. Field lines curving toward each other — they get close, they bend, they almost touch — but they don't. The distance between them is charged with everything that can't be said.", emotionalNote: "Reaching across empty space without connecting", background: "#E0E4E8", imageUrl: "/prints/longing/longing_magnetic.jpg", price: 45 },
      { id: "longing-vanishing", title: "Vanishing", series: "longing", equation: "x' = x·f/(f+d), y' = y·f/(f+d)", description: "Always visible. Always the same distance away. Parallel lines converging to a point that recedes as you approach — the destination that stays on the horizon no matter how far you walk. I kept rendering it hoping the lines would meet. They won't.", emotionalNote: "Always visible, always the same distance away", background: "#E0E4E8", imageUrl: "/prints/longing/longing_vanishing.jpg", price: 45 },
    ],
  },

  // ── COMPREHENDING ───────────────────────────────────────
  {
    id: "comprehending",
    name: "COMPREHENDING",
    seoDescriptor: "Geometric Abstract Triptych About Cognition and Clarity",
    homeDescriptor: "A geometric triptych in deep blue, bronze, and rust, built from paired vortex fields and recursive block averaging — a single continuous field drawn twice.",
    emotion: "understanding as reduction, the simplifying mind meeting continuous reality",
    tagline: "Every act of understanding is an act of reduction. The vortices are turned into squares. Comprehension and reduction are the same word.",
    description: "Every act of understanding is an act of reduction. The universe is continuous and infinite in its detail; the mind that perceives it is finite. To make sense of complexity, we have to compress it — to take something that flows and twists and replace it with something we can hold in a single thought. We do not see the world directly. We see a model of it, built by the mind in the act of looking.",
    story: "This series depicts that encounter. Each piece is generated from a single mathematical field, drawn twice: once as continuous flow lines (the world as it is), and once as averaged rectangular blocks (the world as the mind holds it). The vortices are turned into squares. Comprehension and reduction are the same word.",
    mathematicalPrimitive: "paired vortex fields, streamline integration, recursive block averaging",
    background: "#DDD9D2",
    palette: ["#3870B0", "#957A42", "#9A4A2E", "#1C2838", "#F4ECD2"],
    makingOf: "A single field, drawn twice.",
    homePieceIds: ["comprehending-gravity", "comprehending-depth", "comprehending-clarity"],
    pieces: [
      { id: "comprehending-clarity", title: "Clarity", series: "comprehending", equation: "ψ(r) = -(Γ/2π)·log|r − r₀|", description: "The mind reaches toward complexity from the side. A dominant attractor sits at the edge of the canvas; the blocks accumulate along the bottom, gathering to meet what is coming. The moment before understanding — when the storm is still held at arm's length and the self is still mostly self. Built from a single point vortex, the simplest field that carries any structure at all.", emotionalNote: "The moment before understanding", background: "#DDD9D2", imageUrl: "/prints/comprehending/comprehending_clarity.jpg", price: 45 },
      { id: "comprehending-depth", title: "Depth", series: "comprehending", equation: "ψ(r) = Σᵢ -(Γᵢ/2π)·log|r − rᵢ|", description: "The mind enters the field. Multiple attractors press against the blocks; the flow lines wrap around the rectangles and the rectangles intrude into the spirals. There is no clean separation between the world and the model. The moment understanding is being built — when the continuous and the discrete are no longer separable, and every square holds a vortex and every vortex leaks into a square.", emotionalNote: "The moment understanding is being built", background: "#DDD9D2", imageUrl: "/prints/comprehending/comprehending_depth.jpg", price: 45 },
      { id: "comprehending-gravity", title: "Gravity", series: "comprehending", equation: "dr/dt = -∇Φ, Φ ∝ 1/|r − r₀|", description: "The mind releases. A single attractor drives a diagonal sweep that eventually dissolves into the rectangles. What was sharp becomes diffuse. What we keep is always less than what we encountered. I kept staring at the bottom of the frame — the black cells where the flow finally gives way to pure block, the place where the model takes over completely. That is the thing we walk away with.", emotionalNote: "What we keep is always less than what we encountered", background: "#DDD9D2", imageUrl: "/prints/comprehending/comprehending_gravity.jpg", price: 45 },
    ],
  },

  // ── BELONGING ─────────────────────────────────────────────
  {
    id: "belonging",
    name: "BELONGING",
    seoDescriptor: "Warm Generative Art Prints About Shelter, Tenderness, and Being Held",
    homeDescriptor: "Warm generative prints in honey, terracotta, and sage on linen ground, built from domain-warped radial fields, soft potential wells, and translucent layered forms that cradle and contain.",
    emotion: "shelter, tenderness, the quiet relief of having a place to rest",
    tagline: "Being held inside something. Gradient that cradles rather than flattens or pulls.",
    description: "Belonging is a series of generative artworks about being held. Built in Python from softly interacting mathematical forms, each piece creates the feeling of one presence cradled within another — nested, sheltered, and gently contained. Translucent layers and calm, caring color shifts evoke warmth, tenderness, and the quiet relief of having a place to rest.",
    story: "These pieces are built from domain-warped radial fields — concentric rings distorted by sinusoidal coordinate shifts until they lose their mathematical precision and begin to breathe. Each form is rendered as dozens of translucent color-mapped layers composited over a warm linen ground. The palette stays in the register of honey, terracotta, sage, and rose dust — domestic warmth, not cosmic intensity. Where two forms meet, a blue membrane marks the boundary between holder and held.",
    mathematicalPrimitive: "domain-warped radial fields, soft potential wells, FBM noise, translucent alpha compositing",
    background: "#E8DFD0",
    palette: ["#D4A860", "#B87A60", "#8BA092", "#C89080", "#5A7A98"],
    makingOf: "180+ renders across 7 rounds. 4 survived.",
    homePieceIds: ["belonging-nest", "belonging-warmth", "belonging-home"],
    pieces: [
      { id: "belonging-warmth", title: "Warmth", series: "belonging", equation: "T(r) = exp(−r²/σ²)", description: "Radiance without a visible source. A single warm field fills the frame so completely you forget you're looking at it — the way real warmth works, felt before it's seen. The colors move from sand through honey to deep sienna at the center, and a faint blue membrane at the boundary reminds you that even warmth has an edge, a place where inside becomes outside.", emotionalNote: "Felt before it is seen", background: "#E8DFD0", imageUrl: "/prints/belonging/belonging_warmth.jpg", price: 45 },
      { id: "belonging-nest", title: "Nest", series: "belonging", equation: "f(r,θ) = e^(−r²/σ²)·[0.6 + 0.4·cos(kr)ⁿ]", description: "A received interior. Concentric rings warped just enough to stop being geometry and start being shelter — each one slightly imperfect, all holding a common dark core. The deepest reds sit at the center where the rings converge, the place that everything else is built around and oriented toward.", emotionalNote: "Where shape meets comfort", background: "#E8DFD0", imageUrl: "/prints/belonging/belonging_nest.jpg", price: 45 },
      { id: "belonging-held", title: "Held", series: "belonging", equation: "ψ = G_sling(r) + G_held(r_w), r_w = domain_warp(r)", description: "Two forms, one inside the other. The outer presence — cooler, sage-toned, open — curves around a warmer body that has settled into it. They don't merge. The held form keeps its own rings, its own center, its own temperature. Being held doesn't mean being absorbed. It means having something around you that is shaped by your weight.", emotionalNote: "Shaped by your weight", background: "#E8DFD0", imageUrl: "/prints/belonging/belonging_held.jpg", price: 45 },
      { id: "belonging-home", title: "Home", series: "belonging", equation: "H(r) = Σ Gᵢ(r) · veil(r) + ghost_rings(r)", description: "The settled version. Warmth without urgency, structure without tension. The ghost of a held form's rings floats beneath broad, overlapping warm zones — a memory of being cradled that has softened into simply being somewhere familiar. No single center dominates. The whole frame feels lived in.", emotionalNote: "The whole frame feels lived in", background: "#E8DFD0", imageUrl: "/prints/belonging/belonging_home.jpg", price: 45 },
    ],
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
  { pieceId: "grief-void", textColor: "black" },
  { pieceId: "awe-eclipse", textColor: "white" },
  { pieceId: "comprehending-gravity", textColor: "black" },
  { pieceId: "peace-horizon", textColor: "black" },
  { pieceId: "connection-magnetic", textColor: "white" },
  { pieceId: "belonging-home", textColor: "black" },
];

export const featuredSeriesIds = [
  "awe",
  "grief",
  "desire",
  "belonging",
  "comprehending",
  "peace",
  "connection",
  "growth",
];

export const featuredPieceIds = [
  "grief-void",
  "awe-eclipse",
  "comprehending-gravity",
  "peace-horizon",
  "belonging-home",
  "connection-magnetic",
  "peace-field-guardian",
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
