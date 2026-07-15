---
name: talisman
description: >-
  Generate a polished, on-brand PDF guide/handbook/whitepaper from a codebase or
  project using LaTeX (.tex -> .pdf), with a designed cover page, the product's
  real brand colors and logo, a subtle branded page background, and native TikZ
  diagrams (domain models, flows, state machines). Use this whenever the user
  wants to produce a documentation booklet, internal guide, onboarding manual,
  technical brief, feature overview, or any branded PDF derived from an app —
  even if they just say ".tex to pdf", "make a PDF guide", "document how X works",
  "page de garde"/"cover page with our logo", or "in the style of <product>".
  Trigger it when the deliverable is a designed multi-page PDF grounded in a real
  codebase, not a quick README or a slide deck.
---

# Talisman

Turn a codebase into a beautiful, accurate, brand-styled PDF book. The output is a
`docs/guide/` LaTeX project (`main.tex` + `preamble.tex` + `chapters/*` +
`figures/*` + `Makefile`) that builds to `main.pdf`.

Two things make or break the result, in order: **accuracy** (describe what the
code actually does, not what a marketing README claims) and **brand fidelity**
(the real colors, logo, and font character of the product). Everything else is
craft on top.

## Workflow

Do these in order. Phases 1–2 can overlap.

### 1. Extract the brand identity from the codebase

The document should look like it came from the product. Find:

- **Colors** — grep the web app's CSS/theme for the palette: `globals.css`,
  `tailwind.config.*`, `theme.*`, shadcn `:root` blocks, `--primary`,
  `--brand-*`. Modern apps define these in `oklch()` — LaTeX can't use that, so
  run `scripts/oklch_to_hex.py` to convert. Capture: a signature/brand color, the
  darkest shade (body ink), 1–2 accents, a muted gray.
- **Logo** — find it (`public/*logo*`, `*.webp`, `favicon`, a `BrandLogo`
  component pointing at a default asset). pdflatex can't read webp/svg; run
  `scripts/prepare_logo.py` to get a PNG and its background color.
- **Fonts** — note the app's font (e.g. Outfit, Inter, Geist) so you can match its
  *character* with an installed LaTeX family. See `references/environment.md` —
  you almost never get the exact font; pick the closest one that's installed and
  note the substitution honestly.

### 2. Research the real content

Read the code, not the aspirational README. For a case/CRM/workflow/SaaS app the
backbone is usually: the data model (an ORM schema / `schema.prisma` /
migrations), the core lifecycle, the feature modules, and the integration points.
Spawn an Explore/subagent for a thorough pass if the codebase is large. Note
file:line references for the claims you'll make. Flag any place where two parts of
the code/docs disagree — surface it as a "known drift point" box rather than
picking a side silently.

Then decide the **table of contents by necessity**: what a reader genuinely needs
(what it is → domain model → core how-to → each key feature → concrete worked
use-cases → glossary). Don't pad to hit a page count, don't artificially cap it.

### 3. Scaffold the LaTeX project

Create `docs/guide/` (or a location the user names). Copy and fill the templates:

- `assets/preamble.tex` → `preamble.tex` — replace every `<<PLACEHOLDER>>` with
  the extracted palette, the display/body fonts, the product name, the logo
  initial for the header mark.
- `assets/main.tex` → `main.tex` — the shell + cover.
- `assets/Makefile` → `Makefile`.

Put the converted logo in `figures/`.

### 4. Write the chapters

One file per chapter in `chapters/NN-name.tex`. Ground each claim in what you read
in phase 2. Use the `notebox`/`warnbox` environments for asides and drift points.
Include **worked use-cases** (setup + handling walkthroughs) — they're what make a
guide usable rather than a reference dump. Reuse real code (e.g. an existing HMAC
signing sample, an example payload) verbatim where the codebase already has it.

### 5. Add TikZ diagrams

A good software guide has a domain-model diagram, at least one flow diagram, and
at least one state-machine diagram. Use the recipes and the anti-collision rules
in `references/diagrams.md`. One `figures/<name>.tex` per diagram, `\input` from
its chapter.

### 6. Build the cover + branded background

The cover is the "page de garde" the user cares about. The template does a
full-bleed brand-color cover with the logo; if the logo is a monogram on a solid
square, match the cover fill to that square's color so the mark floats seamlessly.
`\brandpagebg` (called once after the cover in `main.tex`) applies the subtle
edge-bar + corner-watermark background to all content pages — keep it faint so
print stays clean.

### 7. Build and verify visually — do not skip

```bash
cd docs/guide && make          # 3 pdflatex passes (refs + TOC + tikz overlay)
pdftotext main.pdf - | grep -c '??'    # must be 0 (no unresolved refs)
pdftoppm -png -r 95 -f 1 -l 1 main.pdf /tmp/cover   # then Read the PNGs
```

LaTeX compiling clean does NOT mean it looks right. Render the cover, every
diagram page, and a text page to PNG and actually look at them. The recurring
defects: overlapping diagram labels, a visible seam around the logo, a background
that's too heavy, headings not in the display font, unresolved `??` refs. Fix and
rebuild until it genuinely looks good. See `references/environment.md` for the
compile-error playbook and toolchain fallbacks (engine choice, missing fonts,
image conversion) — probe the environment there BEFORE assuming a clean install.

## Bundled resources

- `scripts/oklch_to_hex.py` — convert app `oklch()` colors to LaTeX hex.
- `scripts/prepare_logo.py` — webp/png → PNG + sample the logo background color.
- `assets/preamble.tex`, `assets/main.tex`, `assets/Makefile` — the branded
  templates to copy and fill.
- `references/environment.md` — toolchain probing, engine/font fallbacks, the
  compile-error playbook. Read at phase 3 and phase 7.
- `references/diagrams.md` — TikZ recipes for the three diagram families and the
  rules that keep them from rendering broken. Read at phase 5.
