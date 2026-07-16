<div align="center">

<img src="icon.svg" alt="Talisman scroll icon" width="200" height="200"/>

# Talisman

**Turn a codebase into a beautiful, accurate, brand-styled PDF book.**

*A Claude skill for generating polished LaTeX → PDF guides, handbooks, and whitepapers — with a designed cover page, the product's real colors and logo, native TikZ diagrams, and a subtle branded background.*

</div>

---

## What it does

Point Talisman at a codebase and it produces a `docs/guide/` LaTeX project that
builds to a print-ready `main.pdf`:

- **Grounded in the real code** — the content describes what the application
  actually does (read from the schema, modules, and flows), not the aspirational
  claims in a marketing README.
- **On-brand** — it extracts the product's real palette (even from modern
  `oklch()` CSS), its logo, and the character of its fonts, so the document looks
  like it came from the product itself.
- **Designed, not dumped** — a full-bleed cover page ("page de garde") with the
  logo, colored section headings in a geometric display font, a slim branded page
  background, and callout boxes for notes and caveats.
- **Illustrated** — native TikZ diagrams (no Graphviz/Mermaid dependency) for
  domain models, step-by-step flows, and state machines.

> **Why "talisman"?** A talisman is a crafted object that carries the essence of
> the thing it represents. This skill distills a whole codebase into a single
> artifact you can hold — hence the enchanted-scroll icon.

## How it works

The skill drives a seven-phase workflow (see [`SKILL.md`](SKILL.md) for the full
detail):

1. **Extract the brand identity** — grep the web app's CSS/theme for the palette,
   convert `oklch()` values to hex, find and convert the logo, note the font.
2. **Research the real content** — read the data model, lifecycle, feature
   modules, and integration points; decide a table of contents *by necessity*.
3. **Scaffold the LaTeX project** — copy the templates, fill the brand
   placeholders.
4. **Write the chapters** — one file each, grounded in the code, with worked
   use-cases (setup + handling walkthroughs).
5. **Add TikZ diagrams** — domain model, at least one flow, at least one state
   machine.
6. **Build the cover + branded background** — full-bleed brand cover with the
   logo; a faint edge-bar + corner watermark on content pages.
7. **Build and verify visually** — compile with `pdflatex`, then render pages to
   PNG and actually look, because "compiles clean" ≠ "looks right".

## Repository structure

```
talisman/
├── SKILL.md                    # the 7-phase workflow + trigger description
├── icon.svg                    # this scroll icon
├── scripts/
│   ├── oklch_to_hex.py         # convert CSS oklch() brand colors → LaTeX hex
│   └── prepare_logo.py         # webp/png logo → PNG + sample its background color
├── assets/
│   ├── preamble.tex            # branded core: fonts, palette, boxes, header, background
│   ├── main.tex                # full-bleed cover + document shell
│   └── Makefile                # 3-pass pdflatex build
└── references/
    ├── environment.md          # toolchain probing, engine/font fallbacks, error playbook
    └── diagrams.md             # TikZ recipes for the 3 diagram families + anti-collision rules
```

## Installation

Talisman is a [Claude](https://claude.com/claude-code) skill. Install it by
cloning into your skills directory:

```bash
git clone https://github.com/atexy4ba/talisman-skill.git ~/.claude/skills/talisman
```

Then invoke it in a session with `/talisman`, or just describe the deliverable
("make a branded PDF guide of how this app works") and it triggers on its own.

## Requirements

The skill probes the environment and adapts, but the happy path wants:

| Need                | Tool                                                        |
|---------------------|-------------------------------------------------------------|
| PDF engine          | `pdflatex` (default; `lualatex`/`xelatex` only if their font runtime works) |
| LaTeX packages      | `tikz`, `eso-pic`, `tcolorbox`, `hyperref`, `listings`, `booktabs` |
| Fonts (fallback)    | `helvet`, Avant Garde (`pag`) — or the closest installed match |
| Color conversion    | `python3`                                                   |
| Logo conversion     | `python3` + `Pillow` (webp/png), or `rsvg-convert`/`inkscape` for svg |
| Visual verification | `pdftoppm` (poppler)                                         |

`references/environment.md` documents the fallbacks when any of these are missing
or broken.

## The bundled scripts

**`oklch_to_hex.py`** — modern apps define colors in `oklch()`, which LaTeX can't
use. Convert them:

```bash
python3 scripts/oklch_to_hex.py 0.26624 0.15944 267.227
# oklch(0.26624 0.15944 267.227) -> #090E71  rgb(9, 14, 113)
```

**`prepare_logo.py`** — pdflatex can't read `.webp` (common for app logos).
Convert to PNG and get the background color for the cover color-match trick:

```bash
python3 scripts/prepare_logo.py public/logo.webp figures/logo.png
```

## What it encodes

Beyond the happy path, the skill captures the messy realities of building LaTeX on
an arbitrary machine, so future runs don't relearn them:

- `pdflatex`-first (many installs have a broken `lualatex` font runtime).
- Matching the app font's *character* with the closest installed family when the
  exact webfont isn't shippable — and saying so honestly.
- `.webp`/`.svg` logo conversion, and the cover trick of matching the cover fill
  to the logo's square so a monogram floats seamlessly.
- The recurring compile bugs: reserved TikZ keywords (`step`, `state`), overfull
  lines from long code paths, multi-pass builds for cross-references.
- **Always render to PNG and look** — the single most important verification step.

## License

MIT.
