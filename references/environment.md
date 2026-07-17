# Environment & toolchain fallbacks (optimized)

Talisman targets the messy reality of a random machine's LaTeX install. Probe
first, pick the path that works. Don't assume a clean TeX Live.

## Probe script (run once)

```bash
echo "=== Engines ==="
which pdflatex lualatex xelatex tectonic latexmk pandoc 2>/dev/null
echo "=== Packages ==="
for p in tikz eso-pic tcolorbox hyperref listings minted booktabs; do
  kpsewhich $p.sty >/dev/null 2>&1 && echo "  $p ✓" || echo "  $p ✗"
done
echo "=== Fonts ==="
for f in helvet avant sourcecodepro inconsolata; do
  kpsewhich $f.sty >/dev/null 2>&1 && echo "  $f ✓" || echo "  $f ✗"
done
echo "=== Image tools ==="
which convert magick dwebp inkscape rsvg-convert cairosvg 2>/dev/null
python3 -c "import PIL; print('  PIL ✓')" 2>/dev/null || echo "  PIL ✗"
echo "=== PDF tools ==="
which pdftotext pdftoppm pdfjam 2>/dev/null
```

## Engine fallback chain

```
tectonic --available
  ? fastest: auto-resolves packages, single pass
  ! no shell escape, no minted (pygments)
latexmk --auto-pass-count
  ? smart: runs pdflatex/lualatex exactly enough times
  ! requires full TeX Live
pdflatex --3-pass-fallback
  ? works everywhere, safest
  ! slowest, manual pass count
lualatex/xelatex --only-if-fontspec-works
  ? needed for real TTF/OTF fonts
  ! trap: luaotfload-main missing → fontspec dead
```

**Recommendation**: `latexmk -pdf` for reliability + speed. Fallback to 3x pdflatex
only if latexmk is absent.

## Large codebase optimization

For repos >500k LOC (Odoo, ERP, monorepos):

| Tactic | How |
|--------|-----|
| Skip node_modules/.git/.tox | `find . -path '*/node_modules' -prune -o ...` |
| Schema-first | Read models/ or ORM definitions, not every file |
| Module grep | `find . -name '__init__.py' -maxdepth 3` to find modules |
| Parallel research | One subagent per module area |
| Markdown fast path | Write in .md, convert via pandoc |
| Standalone diagrams | `\input` compiles each time; cache as PDF instead |
| Memory | Split into multiple small chapters, not one giant file |

## Font fallback table

| App font style | Closest pdflatex family (package) |
|----------------|-----------------------------------|
| geometric sans | Avant Garde `\fontfamily{pag}` |
| neutral/grotesque | Helvetica `helvet` (Nimbus Sans) |
| humanist sans | `helvet` scaled, or `lato`/`sourcesanspro` if installed |
| monospace (code) | `inconsolata` / `sourcecodepro` / `plex-mono` |
| default fallback | Latin Modern (`lmodern`) |

## Compile-error playbook

- **`The key '/tikz/step' requires a value`** — rename styles (`wizstep`, `st`).
- **`Undefined control sequence \lbl`** — use `{\scriptsize\color{...} label}`.
- **Overfull \hbox** from long paths — use `\url{...}` instead of `\texttt{...}`.
- **`\headheight is too small`** — `\setlength{\headheight}{15pt}`.
- **`??` in output** — needs another pass. `pdftotext main.pdf - | grep -c '??'` → 0.
- **`! Package minted Error: You must have `pygmentize' installed`** — falls back to
  `listings` automatically (autodetected in preamble.tex).
- **`Fatal error occurred, no output PDF file produced!`** — run with
  `-interaction=nonstopmode` to see all errors at once.

## Visual verification

```bash
latexmk -pdf main.pdf 2>&1 | tail -5
pdftotext main.pdf - | grep -c '??'
pdftoppm -png -r 95 -f 1 -l 1 main.pdf /tmp/cover
pdftoppm -png -r 95 -f 3 -l 6 main.pdf /tmp/content
```

Check: cover logo/title, diagram labels, background opacity, heading fonts, TOC
page numbers, no `??` markers.
