<div align="center">

<img src="icon.png" alt="Talisman" width="150"/>

# ✦ Talisman

### Turn a codebase into a beautiful, brand-styled PDF book.

*A Claude skill that reads your app and writes a polished LaTeX → PDF guide —
with a designed cover, your real colors and logo, native diagrams, and a subtle
branded background.*

<br/>

![License](https://img.shields.io/badge/license-MIT-2227BE?style=flat-square)
![Claude Skill](https://img.shields.io/badge/Claude-skill-8A7BFF?style=flat-square)
![Engine](https://img.shields.io/badge/LaTeX-pdf-B45309?style=flat-square)
![Diagrams](https://img.shields.io/badge/diagrams-TikZ-15803D?style=flat-square)
![PRs](https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square)

</div>

---

<div align="center">

**[What it does](#-what-it-does)** · **[Install](#-install)** · **[Usage](#-usage)** · **[How it works](#️-how-it-works)** · **[Structure](#-repository-structure)** · **[Requirements](#-requirements)**

</div>

---

## ✨ What it does

Point Talisman at a repository and it produces a `docs/guide/` LaTeX project that
builds to a print-ready `main.pdf`.

|  | |
|---|---|
| 🎯 **Grounded in the real code** | Describes what the app *actually* does — read from the schema, modules, and flows — not the aspirational claims in a marketing README. |
| 🎨 **On-brand** | Extracts the product's real palette (even modern `oklch()` CSS), its logo, and the character of its fonts, so the document looks like it came from the product. |
| 📐 **Designed, not dumped** | A full-bleed cover page, colored headings in a geometric display font, a slim branded page background, and callout boxes for notes and caveats. |
| 🧩 **Illustrated** | Native TikZ diagrams — domain models, step-by-step flows, and state machines — with **no** Graphviz/Mermaid dependency. |

> **Why "talisman"?** A talisman is a crafted object that carries the essence of
> the thing it represents. This skill distills a whole codebase into a single
> artifact you can hold.

---

## 📦 Install

Talisman is a [Claude](https://claude.com/claude-code) skill. Clone it into your
skills directory:

```bash
git clone https://github.com/atexy4ba/talisman-skill.git ~/.claude/skills/talisman
```

Then in any session, run `/talisman` — or just describe the deliverable
("make a branded PDF guide of how this app works") and it triggers on its own.

---

## 🚀 Usage

```text
You:  /talisman  build an internal guide for this codebase

Claude:
  1. extracts your brand palette, logo, and fonts from the app
  2. reads the data model and features to get the content right
  3. scaffolds docs/guide/ and writes the chapters + TikZ diagrams
  4. builds the branded cover + subtle page background
  5. compiles with pdflatex and renders pages to verify visually
  → docs/guide/main.pdf
```

---

## 🛠️ How it works

A seven-phase workflow (full detail in [`SKILL.md`](SKILL.md)):

<table>
<tr><td align="center"><b>1</b></td><td><b>Extract brand identity</b><br/>Palette from CSS (<code>oklch()</code> → hex), logo, font character.</td></tr>
<tr><td align="center"><b>2</b></td><td><b>Research real content</b><br/>Data model, lifecycle, feature modules, integration points. TOC by necessity.</td></tr>
<tr><td align="center"><b>3</b></td><td><b>Scaffold</b><br/>Copy the templates, fill the brand placeholders.</td></tr>
<tr><td align="center"><b>4</b></td><td><b>Write chapters</b><br/>Grounded in the code, with worked setup + handling use-cases.</td></tr>
<tr><td align="center"><b>5</b></td><td><b>Add diagrams</b><br/>Domain model, a flow, a state machine (TikZ).</td></tr>
<tr><td align="center"><b>6</b></td><td><b>Cover + background</b><br/>Full-bleed brand cover with the logo; faint watermark on content pages.</td></tr>
<tr><td align="center"><b>7</b></td><td><b>Build & verify visually</b><br/>Compile, then render pages to PNG and actually look.</td></tr>
</table>

---

## 📁 Repository structure

```
talisman/
├── SKILL.md                    # the 7-phase workflow + trigger description
├── icon.png                    # skill icon
├── scripts/
│   ├── oklch_to_hex.py         # CSS oklch() brand colors → LaTeX hex
│   └── prepare_logo.py         # webp/png logo → PNG + sample its background color
├── assets/
│   ├── preamble.tex            # branded core: fonts, palette, boxes, header, background
│   ├── main.tex                # full-bleed cover + document shell
│   └── Makefile                # 3-pass pdflatex build
└── references/
    ├── environment.md          # toolchain probing, engine/font fallbacks, error playbook
    └── diagrams.md             # TikZ recipes for the 3 diagram families + anti-collision rules
```

---

## 🧰 Requirements

The skill probes the environment and adapts, but the happy path wants:

| Need | Tool |
|---|---|
| PDF engine | `pdflatex` (default; `lualatex`/`xelatex` only if their font runtime works) |
| LaTeX packages | `tikz`, `eso-pic`, `tcolorbox`, `hyperref`, `listings`, `booktabs` |
| Fonts (fallback) | `helvet`, Avant Garde (`pag`) — or the closest installed match |
| Color / logo conversion | `python3` + `Pillow` (webp/png); `rsvg-convert`/`inkscape` for svg |
| Visual verification | `pdftoppm` (poppler) |

`references/environment.md` documents the fallbacks when any of these are missing.

---

## 🔧 The bundled scripts

<details>
<summary><b><code>oklch_to_hex.py</code></b> — convert modern CSS colors LaTeX can't read</summary>

```bash
python3 scripts/oklch_to_hex.py 0.26624 0.15944 267.227
# oklch(0.26624 0.15944 267.227) -> #090E71  rgb(9, 14, 113)
```
</details>

<details>
<summary><b><code>prepare_logo.py</code></b> — <code>.webp</code> logo → PNG + background color</summary>

```bash
python3 scripts/prepare_logo.py public/logo.webp figures/logo.png
# prints the logo's background color for the cover color-match trick
```
</details>

---

## 🧠 What it encodes

Beyond the happy path, the skill captures the messy realities of building LaTeX on
an arbitrary machine, so future runs don't relearn them:

- `pdflatex`-first — many installs ship a broken `lualatex` font runtime.
- Matching the app font's *character* with the closest installed family when the
  exact webfont isn't shippable — and saying so honestly.
- `.webp`/`.svg` logo conversion, and the cover trick of matching the cover fill
  to the logo's square so a monogram floats seamlessly.
- The recurring compile bugs: reserved TikZ keywords (`step`, `state`), overfull
  lines from long code paths, multi-pass builds for cross-references.
- **Always render to PNG and look** — the single most important verification step.

---

## 🤝 Contributing

Issues and PRs welcome — new diagram recipes, font-fallback mappings, and
environment fixes are especially useful.

## 📄 License

[MIT](LICENSE) © atexy4ba

<div align="center"><sub>Built for Claude Code · crafted to look like it came from your product.</sub></div>
