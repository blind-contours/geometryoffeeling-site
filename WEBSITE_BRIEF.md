# Geometry of Feeling — Website Brief
## Build Instructions for geometryoffeeling.com

---

## PART 1: WHO WE ARE AND WHY WE ARE DIFFERENT

### The Market Problem

The online mathematical art market is dominated by:
- **Redbubble/Society6**: Fractal screensavers, Mandelbrot sets, geometric patterns, Pi Day jokes. Mass-produced, algorithmically generic, no emotional intent.
- **AI-generated art**: Floods of Midjourney/DALL-E outputs — visually impressive, emotionally hollow. 76% of buyers don't consider AI art "genuine." Collectors specifically seek the *story and intent* behind a work.
- **Data visualization posters**: Science-poster aesthetics — "here is information" not "here is feeling."
- **Minimalist geometric art**: Scandinavian circles and lines. Beautiful but cold. No meaning beneath the surface.

**None of them answer the question: what does grief look like as an equation?**

### Our Positioning

**Mathematical Affect** is the only fine art brand that uses mathematical functions as an emotional language. Every piece is:
1. **Rooted in human history** — each emotion was researched across millennia of art, philosophy, and culture before a single line was drawn
2. **Mathematically faithful** — the equation in the label is real, correct, and chosen because its *behavior* mirrors the emotion's dynamics
3. **Curated by a human** — every piece was selected through iterative human judgment, not algorithmic output
4. **Minimalist in the tradition of Tōhaku, Rothko, and Agnes Martin** — the negative space is as intentional as the curve

The tagline: **"The geometry of feeling."**

The anti-positioning: We are not AI art. We are not data visualization. We are not decorative geometry. We are **mathematical fine art for people who feel things deeply and think precisely.**

### The Target Audience

**Primary**: Mathematically-minded people who also feel deeply — engineers, scientists, programmers, academics, architects, designers. People who have a proof on their shelf and a poem in their drawer. Age 28-55.

**Secondary**: Art collectors who want something genuinely novel — not another abstract expressionist print, not another AI image. People who want to explain their wall art at dinner parties and have something real to say.

**Tertiary**: Gift buyers for the above — "I bought this for my sister who is a physicist and just went through a breakup. It's called *Settling* and it's a damped oscillation."

### What Sets Us Apart (The Pitch)

> *In a world of AI-generated imagery, we went the other direction. Every piece starts with a human emotion — grief, growth, overwhelm, connection — and asks: what mathematical function has the same shape as this feeling? We researched that emotion across human history, across art and philosophy and science, and then built the image from first principles. The equation at the bottom isn't decoration. It's the reason the image looks the way it does. This is minimalist fine art where the mathematics and the emotion are the same thing.*

---

## PART 1B: THE HUMAN-MADE DISTINCTION (CRITICAL POSITIONING)

This must appear prominently on the homepage, about page, and every series page. It is our single most important differentiator in 2026.

### What We Are

Every piece in this collection was:

1. **Built by a human, in Python, using real mathematical equations** — not prompted into an AI image generator. The code is the medium. The equation is the subject. The emotion is the intent.

2. **Researched before it was rendered** — each emotion was studied across human art history, philosophy, and mathematics before a single parameter was chosen. We asked: what does this emotion do over time? Does it decay? Does it oscillate? Does it branch? Does it converge? Then we found the function that behaves the same way.

3. **Evaluated as art, not just output** — every piece went through iterative human curation. Hundreds of renders were made. Most were rejected. The ones you see survived because they passed a simple test: does this image make you feel the emotion it claims to represent?

4. **Minimalist by intention, not by limitation** — the negative space is chosen. The palette is chosen. The equation label at the bottom is real, correct, and the reason the image looks the way it does.

### What We Are Not

This is not AI-generated art. AI image generators — Midjourney, DALL-E, Stable Diffusion — take a text prompt and pattern-match against billions of training images. They produce visually impressive outputs with no underlying structure, no mathematical truth, and no intentional emotional architecture.

We went the opposite direction. We started with the emotion. We found the mathematics. We wrote the code. We rendered, evaluated, and curated. The process took months. Each series represents dozens of hours of research, coding, and aesthetic judgment.

**The equation at the bottom of every piece is not decoration. It is the proof.**

### Use This Language On The Site

> *"Built by a human. Rendered in Python. Grounded in mathematics. Every piece is the result of asking one question: what does this emotion look like as an equation?"*

> *"In a world of AI-generated imagery, we went the other direction. This is minimalist fine art built from mathematical first principles — not prompted, not generated, not automated. Every curve was chosen. Every parameter was earned."*

> *"The equation at the bottom of each piece is real. It is the reason the image looks the way it does. This is not a style filter applied to a photograph. This is what the function actually looks like when you render it."*

---

## PART 2: THE ART — WHAT WE HAVE

### Final Image Files — Use These Exact Files

The agent must use **only** the following files. These are the final, curated, approved pieces for each series.

**FRACTURED** (4 pieces):
- `FINAL_fractured_drift.pdf`
- `FINAL_fractured_lean.pdf`
- `FINAL_fractured_surge.pdf`
- `FINAL_fractured_scattered.pdf`

**CONNECTION** (4 pieces):
- `FINAL_connection_lissajous.pdf`
- `FINAL_connection_helix.pdf`
- `FINAL_connection_rose.pdf`
- `FINAL_connection_damped.pdf`

**TENSION** (3 pieces):
- `FINAL_tension_beat.pdf`
- `FINAL_tension_stretch.pdf`
- `FINAL_tension_resonance.pdf`

**OVERWHELM** (5 pieces):
- `overwhelm_correlated.pdf`
- `overwhelm_fbm.pdf`
- `overwhelm_moire.pdf`
- `overwhelm_streams.pdf`
- `overwhelm_interference.pdf`

**GRIEF** (5 pieces):
- `grief_whirlpool_grey_a.pdf`
- `grief_hourglass_v2.pdf`
- `grief_preservation_v2.pdf`
- `grief_stillness_a.pdf`
- `grief_mono.pdf`

**GROWTH** (8 pieces):
- `growth_fib_c.pdf`
- `growth_up_a.pdf`
- `growth_up_b.pdf`
- `growth_up_c.pdf`
- `growth_branch_a.pdf`
- `growth_branch_c.pdf`
- `growth_branch_f.pdf`
- `growth_branch_h.pdf`

**Image conversion**: Convert all PDFs to JPG/PNG for web display (800px wide for previews, keep original PDF as the download product). Use `pdf2image` or `ImageMagick` in a build script.

### Six Complete Series

**FRACTURED** — piecewise discontinuous functions. Emotional fracture, the moment things break.
- Background: Light cream (#F5F0E0)
- Palette: Cool-to-warm progressions
- Pieces: Drift, Lean, Surge, Scattered
- The discontinuity IS the emotion

**CONNECTION** — parametric curve pairs with phase offsets. Two things following each other.
- Background: Near-black (#0A0A12)
- Palette: Amber and gold against dark
- Pieces: Lissajous, Helix, Rose, Damped
- The phase offset between curves IS the relationship

**TENSION** — Lorentzian envelopes, beating frequencies. Systems that cannot rest.
- Background: Dark charcoal (#1A1A1A)
- Palette: Electric yellow, red accent
- Pieces: Beat, Stretch, Resonance IV
- Inspired by Munch's The Scream — electric yellow against dark ground

**OVERWHELM** — multiple simultaneous systems. Too much at once, beautifully.
- Background: Near-black (#0A0A12)
- Palette: Full mixed spectrum — 10 colors competing
- Pieces: Correlated walks, Fourier harmonics, Moiré, Parallel streams, Interference field
- The density IS the overwhelm

**GRIEF** — exponential decay, sigmoid transfer, damped oscillation.
- Background: Cool grey (#DDD9D2)
- Palette: Muted slate blues, dusty mauve, pale ice
- Key pieces: Half-Life Whirlpool (signature), Hourglass, Preservation, Stillness
- The quietest series — the absence of color IS the grief

**GROWTH** — L-system branching, golden spiral, upwelling field lines.
- Background: Warm ivory (#F5F0E6)
- Palette: Dark green to spring green to pale gold
- Key pieces: Fractal Canopy, Three Seasons, Two Trees Reaching, Seven Spring Colors, Fibonacci Tiling, Upwelling A/B/C

### Pricing Strategy
- **Digital download (PDF, print-ready)**: $18–$28 per piece
- **Individual series (4-5 pieces)**: $65–$90 (20% bundle discount)
- **Complete collection (all 6 series)**: $220 (40% discount)
- **Future**: Limited edition physical prints via Gelato or Fine Art America, $45–$85

---

## PART 3: WEBSITE DESIGN BRIEF

### Core Design Principles

**The website is itself a piece of the art.** It should feel like walking into a quiet gallery, not browsing a marketplace.

1. **Extreme whitespace** — let each image breathe. Never two images competing for attention on the same screen.
2. **Monospace typography** — everywhere. The typeface is Courier, IBM Plex Mono, or JetBrains Mono. This signals mathematical precision.
3. **No color in the UI** — the UI is white, off-white, and near-black. All color comes from the art.
4. **Slow and deliberate** — no animations except slow fades. No hover effects except subtle opacity change. No music.
5. **The equation is always visible** — every piece shows its equation label as part of the display, not hidden metadata.

### Typography
```
Primary font: IBM Plex Mono (Google Fonts — free)
Fallback: JetBrains Mono, Courier New, monospace

Headline: 18px, weight 400, letter-spacing 0.05em
Body: 14px, weight 300, line-height 1.8
Label/caption: 11px, weight 300, letter-spacing 0.08em
All text: uppercase sparingly, sentence case preferred
```

### Color System (UI only)
```
Background:       #FAFAF8   (warm off-white — like the art backgrounds)
Surface:          #F2F0EC
Border:           #E0DDD8
Text primary:     #1A1A18
Text secondary:   #6A6A68
Text muted:       #9A9A98
Accent:           none — the art provides all color
```

### Layout
- **Max content width**: 1200px, centered
- **Grid**: 12-column, 24px gutter
- **Image display**: full-bleed on individual piece pages, 2-up on series pages, 3-up on overview
- **Mobile**: single column, full-width images

---

## PART 4: SITE ARCHITECTURE

### Pages

#### `/` — Home
**The most important page. It must do one thing: stop the visitor.**

**Hero section:**
- Full-screen rotating hero: one piece from the collection fades slowly (8s crossfade)
- Centered over the image: *"The geometry of feeling."* in monospace, white, low opacity
- On scroll: hero fades out

**Positioning statement (below hero, white background):**
- Large monospace: *"Mathematical fine art for people who think precisely and feel deeply."*
- Two short paragraphs: the pitch + the human-made distinction (see Part 1B)
- Small callout: *"Built in Python. Evaluated as art. Not AI-generated."* — this line in a subtle bordered box or subtle rule

**Series collection grid (the key UX innovation):**

Each of the 6 series is presented as a **tight icon grid** — all pieces in the series shown together as small thumbnails (approximately 120×80px), side by side with no gap, forming a single visual unit. This lets the viewer experience the series as a cohesive collection at a glance — the emotional palette, the shared background color, the family resemblance between pieces.

Layout per series:
```
[SERIES NAME — all caps monospace, left-aligned]
[one-line emotional description]
[tight grid of all piece thumbnails, no spacing between them]
[                      "Explore series →"              ]
```

The thumbnail grid is **clickable as a whole** — hovering the grid subtly brightens all images together (they feel like one object). Clicking any individual thumbnail opens that piece's detail page. Clicking "Explore series →" goes to the series page.

On hover of an individual thumbnail: that single image scales up slightly (1.05×) and shows the piece title in a small monospace label below — but all other thumbnails remain unchanged. This creates the "expand one piece" interaction without leaving the page.

Stack all 6 series vertically down the homepage, alternating alignment (series 1 left-aligned icon grid, series 2 right-aligned, etc.) for visual rhythm.

**No buy button on the homepage.** Let them fall in love with the series first.

**Footer**: geometryoffeeling.com — email capture — Instagram / LinkedIn / Pinterest links

#### `/series` — All Series
- 6 cards, one per series
- Each card: series name, emotional description, 2-image preview, "Explore series →"
- Clean grid, generous spacing

#### `/series/[name]` — Individual Series Page
- Series name large at top
- One-paragraph description: the emotion, the mathematical structure, the research reference
- All pieces in the series, 2-up grid on desktop
- Each piece: title, equation (monospace), and buy button
- "The Story Behind This Series" — expandable section with the human context

#### `/piece/[name]` — Individual Piece Page
- The image, large, centered
- Title in monospace
- The full equation label
- One paragraph: what this equation is, why it matches this emotion
- "Part of: [Series Name]" → link to series
- Buy options: Digital Download ($X) / Add to Series Bundle
- Related pieces from same series

#### `/about` — The Concept
This is the differentiation page. Tell the full story:
- Why mathematics and emotion
- How each series is made (research → mathematical selection → iteration → human curation)
- The explicit statement: this is not AI-generated art. Every piece was designed by a human using mathematics as a medium.
- The art history context (briefly — Tōhaku's negative space, Rothko's fields, Agnes Martin's lines)
- Photo or bio of the creator (optional but increases authenticity and purchase conversion)

#### `/shop` — All Prints Available
- Filter by: series / emotion / background color / price
- Sort by: newest / most popular / price
- Clean product grid
- "Start with a series" prominent CTA — bundles convert better than individual pieces

#### `/downloads` — After Purchase
- Gated page, accessible via purchase link
- High-resolution PDFs (300 DPI, print-ready)
- Printing instructions: recommended paper (fine art matte, 80lb+), recommended sizes
- Frame guide

---

## PART 5: COPY FRAMEWORK

### The Core Copy (use everywhere)

**One-liner**: The geometry of feeling.

**Tagline**: Mathematical fine art for people who think precisely and feel deeply.

**Pitch (3 sentences)**:
> Every piece begins with a human emotion — grief, growth, connection — and asks: what mathematical function has the same shape as this feeling? We researched that emotion across art history and science, then built the image from first principles. The equation isn't decoration. It's the reason the piece looks the way it does.

**Anti-pitch** (what we're not):
> This is not AI-generated art. It is not data visualization. It is not decorative geometry. It is mathematical fine art — minimalist, precise, and rooted in the same human experiences that produced every other great work of art.

### Series Descriptions (short version for cards)

**FRACTURED** — *Piecewise functions where the limit from the left never meets the limit from the right. The discontinuity is the emotion.*

**CONNECTION** — *Two parametric curves with a phase offset. Neither leads nor follows. The gap between them is the relationship.*

**TENSION** — *Lorentzian resonance and beating frequencies. Systems that cannot rest and will not resolve.*

**OVERWHELM** — *Twelve harmonics, eight wave sources, twenty-two parallel streams. Each coherent alone. Together, unresolvable.*

**GRIEF** — *Exponential decay toward zero. Half-life curves draining from two directions. The plateau that holds until the edges yield.*

**GROWTH** — *L-system branching at thirteen levels. Golden spirals tiling the plane. Thirty-four lines reaching toward light.*

---

## PART 6: SEO AND DISCOVERABILITY STRATEGY

### Primary Keywords
- mathematical fine art prints
- equation art prints
- mathematics and emotion art
- minimalist mathematical art
- geometry of feeling
- abstract math art
- scientific art prints
- data art prints
- fractal fine art

### Long-tail Keywords (high intent, lower competition)
- "grief as a mathematical equation"
- "growth fractal art print"
- "minimalist art for scientists"
- "gift for mathematician who loves art"
- "art prints with equations"
- "mathematical emotion art"
- "geometric fine art prints minimalist"

### Content Strategy (drives organic traffic)
Create blog posts / series pages around:
1. **"What does grief look like as a mathematical function?"** — explores the series, links to buy
2. **"The mathematics of human connection"** — the Connection series story
3. **"Why I chose the golden spiral for growth"** — the art historical research
4. **"How Tōhaku's Pine Trees influenced our Growth series"** — art history + our work
5. **"The difference between data visualization and mathematical fine art"** — explicit differentiation

Each post ends with: view the [SERIES NAME] series →

### Social Strategy

**Instagram / TikTok**: The "math behind the art" format. Short video: show the equation, then reveal the image. "This is what tension looks like as a mathematical function." Voiceover explains in 30 seconds. No face needed — just equation, image, narration.

**LinkedIn**: Target the mathematician/scientist/engineer audience. "I built a fine art series based on how grief behaves as a differential equation." This audience shares.

**Pinterest**: Mathematical art is highly pinnable. Long vertical format works well for the landscape prints. Pin every piece individually with alt text containing the equation and emotion keywords.

---

## PART 7: CONVERSION OPTIMIZATION

### What Converts in Fine Art Print Sales (from research)

1. **Show prints in context** — generate mockups of each piece framed on a wall. Listings with wall mockups sell 20-30% better.
2. **Series bundles convert better than individual pieces** — price the bundle at 20% off and make it prominent.
3. **Tell the story** — buyers of fine art buy the meaning, not just the image. Every page should answer "why does this exist?"
4. **Instant download reduces friction** — digital downloads have near-zero cart abandonment vs physical print shipping
5. **Print instructions matter** — tell buyers exactly what paper and size to print at. It removes the last uncertainty.
6. **Email capture before leaving** — offer a free download (one piece from each series as a preview pack) in exchange for email

### Pricing Psychology
- Never price at $20 — price at $18 (feels like a deal) or $22 (feels like value)
- Series bundles: show the "you save $X" clearly
- The full collection should feel like a luxury purchase — price it at $220-240, not $150
- Free preview (one piece per series as low-res) builds trust and desire

### Trust Signals
- The full equation shown on every piece (proves mathematical authenticity)
- The research story on series pages (proves human intent and curation)
- Explicit "not AI generated" statement somewhere visible — this matters to buyers
- Print quality specifications (300 DPI, PDF, fine art ready)

---

## PART 8: TECHNICAL STACK

### Recommended Stack
```
Framework:    Next.js 14 (App Router)
Styling:      Tailwind CSS + custom CSS variables
Deployment:   Vercel (connects to your domain in minutes)
Payments:     Gumroad (easiest for digital downloads)
              OR Stripe + custom delivery
Analytics:    Vercel Analytics (free) + Plausible (privacy-friendly)
Email:        Resend or Mailchimp for capture
Images:       Next.js Image component with optimization
```

### Why Gumroad for Launch
- Zero dev time to set up
- Handles payments, delivery, VAT globally
- You keep ~93% after fees
- Can embed buy buttons directly in Next.js pages
- Easy to migrate to Stripe later if needed

### File Structure
```
/app
  /page.tsx                    — home
  /about/page.tsx              — concept page
  /series/page.tsx             — all series
  /series/[slug]/page.tsx      — individual series
  /piece/[slug]/page.tsx       — individual piece
  /shop/page.tsx               — all prints
/components
  /PrintCard.tsx               — reusable print display
  /SeriesCard.tsx              — series overview card
  /Hero.tsx                    — homepage hero with rotating image
  /EquationLabel.tsx           — monospace equation display
/data
  /series.ts                   — all series metadata
  /pieces.ts                   — all piece metadata + Gumroad links
/public
  /prints/                     — compressed preview images (800px wide)
  /mockups/                    — wall mockup renders
```

### Series Data Structure
```typescript
interface Piece {
  id: string
  title: string
  series: string
  equation: string          // "f(t) = e^(-λt)"
  description: string       // one paragraph
  emotionalNote: string     // "the area beneath the curve is what remains"
  background: string        // hex color
  imageUrl: string
  mockupUrl: string
  gumroadUrl: string
  price: number
}

interface Series {
  id: string
  name: string              // "GRIEF"
  emotion: string           // "decay, draining away, quiet and still"
  description: string       // full paragraph
  mathematicalPrimitive: string
  background: string
  palette: string[]
  pieces: Piece[]
  bundleGumroadUrl: string
  bundlePrice: number
}
```

---

## PART 9: LAUNCH SEQUENCE

### Week 1 — Site Live
- [ ] Deploy on Vercel with geometryoffeeling.com domain
- [ ] All 6 series live with preview images
- [ ] Gumroad products set up for all pieces and bundles
- [ ] Email capture with free preview pack (1 piece per series, low-res)
- [ ] About page with full concept explanation

### Week 2 — Content
- [ ] First Instagram post: "What does grief look like as a mathematical function?" — reveal video
- [ ] First LinkedIn post: the differentiation story
- [ ] Pinterest: pin all 25+ pieces individually
- [ ] First blog post live on the site

### Week 3+ — Growth
- [ ] TikTok series: equation → image reveals
- [ ] Reach out to science/math influencers for shares
- [ ] Submit to design blogs (It's Nice That, Colossal, Brain Pickings successor The Marginalian)
- [ ] Consider limited run of physical prints via Fine Art America or Gelato

### Key Metric Targets (Month 1)
- Email list: 500 subscribers
- Instagram followers: 1,000
- Revenue: $500-1,500 (25-75 downloads)
- Conversion rate target: 2-3% of visitors

---

## PART 10: THE ONE THING

If the website does one thing, it is this:

**A stranger lands on the page, sees an image they don't understand, reads the equation, reads the title, reads one sentence of explanation — and feels something.**

That is the conversion moment. Not the buy button. Not the price. Not the bundle deal. The moment when a scientist sees *Settling* — `f(t) = e^(-λt)·cos(ωt)` — and thinks: *that is exactly what grief feels like.*

Everything else on the site is in service of that moment.

Build toward it.
