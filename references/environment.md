# Environment & toolchain fallbacks

Talisman targets the messy reality of a random machine's LaTeX install. Probe
first, then pick the path that works. Don't assume a clean TeX Live.

## Probe before you build

```bash
which pdflatex lualatex xelatex tectonic pandoc      # engines
kpsewhich tikz.sty eso-pic.sty tcolorbox.sty         # required packages
kpsewhich helvet.sty avant.sty                        # fallback fonts
which convert magick dwebp inkscape rsvg-convert      # image tools
python3 -c "import PIL; print('PIL ok')"              # logo conversion fallback
```

## Engine choice

**Default to `pdflatex`.** It's the most reliably installed and needs no font
runtime. Use `lualatex`/`xelatex` (with `fontspec`) ONLY if you both (a) have the
real app font TTFs and (b) confirmed the Unicode engine actually loads fonts.

Common trap: `lualatex` is present but `luaotfload-main` is missing —
`find / -name "luaotfload-main.lua"` returns nothing. Then `fontspec` is dead and
lualatex can't load any font. Don't fight it; use pdflatex.

## Fonts: echo the app without the app's font files

App fonts (Outfit, Inter, Geist, Satoshi, ...) are almost always Google/webfonts
not shippable to pdflatex, and there's usually no network to fetch them. Match the
*character* of the font with the closest INSTALLED family:

| App font style        | Closest pdflatex family (package)         |
|-----------------------|-------------------------------------------|
| geometric sans        | Avant Garde `\fontfamily{pag}` (round)    |
| neutral/grotesque sans| Helvetica `helvet` (Nimbus Sans)          |
| humanist sans         | `helvet` scaled, or `lato`/`sourcesanspro` if installed |
| default fallback      | Latin Modern (`lmodern`)                  |

Make the whole document sans (`\renewcommand{\familydefault}{\sfdefault}`) so it
reads like a product UI. Use a geometric display font for headings/cover only —
mixing one clean body sans + one distinctive display face looks intentional.

Record the substitution in a comment in `preamble.tex` — it's the one honest gap
vs. "use the exact app font", and the user should be able to see the reasoning.

For code listings: prefer `inconsolata`/`sourcecodepro`/`plex-mono` if installed
(closest to JetBrains/IBM Plex Mono); otherwise the default typewriter is fine.

## Logo conversion

pdflatex reads PDF/PNG/JPG, NOT webp or svg (both common for app logos).
- webp/png/jpg → PNG: `scripts/prepare_logo.py` (Pillow). It also prints the
  logo's background color — use it for the cover color-match trick.
- svg → PDF: `rsvg-convert -f pdf`, `inkscape --export-type=pdf`, or `cairosvg`.
  If none exist and it's simple (a monogram), consider redrawing it in TikZ.

## Compile-error playbook (seen in practice)

- **`The key '/tikz/step' requires a value`** — `step`, `state`, `box`, `grid`
  are reserved TikZ words. Rename your node styles (`wizstep`, `st`, `entity`).
- **`Undefined control sequence \lbl`** inside a node — a `lbl/.style` is a TikZ
  *style*, not a text macro. Don't put `\lbl{...}` in node text; use
  `{\scriptsize\color{...} label}` instead.
- **Overfull \hbox** from long code paths like `apps/web/.../Foo.tsx` — wrap in
  `\url{...}` (with `hyperref`) so it breaks, instead of `\texttt{...}`.
- **`\headheight is too small`** — `\setlength{\headheight}{15pt}`.
- **Undefined references / `??` in output** — needs another pass. The Makefile
  runs pdflatex 3× on purpose (refs + TOC shift + tikz overlay). Verify with
  `pdftotext main.pdf - | grep -c '??'` → must be 0.
- **`remember picture` overlay misplaced on first build** — it needs two passes;
  the 3-pass Makefile handles it.

## Verify visually — always

LaTeX "compiles clean" and still looks broken (overlapping diagram labels,
blended logo edges, color clashes). After building, render pages to PNG and
actually look:

```bash
pdftoppm -png -r 95 -f 1 -l 1 main.pdf /tmp/pg_cover   # cover
pdftoppm -png -r 95 -f 5 -l 8 main.pdf /tmp/pg         # diagram/content pages
```

Then read the PNGs. Check: cover logo/title, every diagram for label collisions,
the branded background isn't too heavy, headings use the display font, TOC page
numbers resolved.
