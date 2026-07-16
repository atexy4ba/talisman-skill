# Talisman — agent playbook

Talisman turns a codebase into a polished, on-brand PDF guide (LaTeX → PDF): a
designed cover page, the product's real colors and logo, native TikZ diagrams
(domain models, flows, state machines), and a subtle branded page background.

This file is the **cross-agent entry point** (the `AGENTS.md` convention). Any
coding AI agent that reads it should follow the workflow below. `SKILL.md` holds
the same workflow in Claude Code's skill format — both drive the identical steps,
so keep them in sync if you edit one.

## When to run this

Trigger whenever the user wants a **designed, multi-page PDF derived from a real
codebase** — an internal guide, onboarding manual, technical brief, feature
overview, handbook, whitepaper, or "cover page / page de garde with our logo" —
as opposed to a quick README or a slide deck. Cues include ".tex to pdf",
"branded PDF", "document how this app works", or "in the style of <product>".

## The workflow (full detail in `SKILL.md`)

1. **Extract brand identity** — palette from the app's CSS (convert `oklch()`
   with `scripts/oklch_to_hex.py`), logo (convert with `scripts/prepare_logo.py`),
   font character.
2. **Research real content** — data model, lifecycle, feature modules,
   integration points. Decide a table of contents by necessity, not padding.
3. **Scaffold** — copy `assets/preamble.tex`, `assets/main.tex`, `assets/Makefile`
   into `docs/guide/` and fill the `<<PLACEHOLDER>>` brand values.
4. **Write chapters** — one file each, grounded in the code, with worked
   setup + handling use-cases.
5. **Add diagrams** — domain model, a flow, a state machine; recipes and
   anti-collision rules in `references/diagrams.md`.
6. **Cover + background** — full-bleed brand cover with the logo; call
   `\brandpagebg` once for the subtle content-page background.
7. **Build and verify visually** — `cd docs/guide && make`, check
   `pdftotext main.pdf - | grep -c '??'` is 0, then render pages with `pdftoppm`
   and actually look. Compiling clean does not mean it looks right.

## Environment first

Before phase 3, probe the toolchain (engines, LaTeX packages, fonts, image
tools) — see `references/environment.md`. Default to `pdflatex`; use
`lualatex`/`xelatex` only if their font runtime actually works. That file also
has the compile-error playbook.

## Repo map

- `scripts/` — `oklch_to_hex.py` (CSS colors → hex), `prepare_logo.py` (logo → PNG).
- `assets/` — `preamble.tex`, `main.tex`, `Makefile` (the branded templates).
- `references/` — `environment.md` (toolchain/fallbacks), `diagrams.md` (TikZ recipes).
