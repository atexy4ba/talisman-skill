# TikZ diagram recipes

Native TikZ diagrams (no graphviz/mermaid dependency) that match the brand. Three
families cover most software docs. All assume the palette from `preamble.tex`
(`brandmain`, `brandink`, `brandaccent`, `brandalt`, `brandgray`, plus semantic
`okgreen`/`noamber` and their `*lt` tints).

Put each diagram in its own `figures/<name>.tex` and `\input{}` it from the
chapter inside a `figure` environment with a `\caption` and `\label`. Keeping them
as separate files keeps chapters readable and lets you regenerate one diagram
without touching prose.

## Universal rules (learned the hard way)

1. **Never name a style `step`, `state`, `box`, `grid`, `node`** — reserved by
   TikZ. Use `wizstep`, `st`, `entity`.
2. **Mask edge labels** so they never look like they sit on a node:
   `lbl/.style={font=\scriptsize\color{brandgray}, fill=white, inner sep=1.6pt}`.
   The `fill=white` punches a hole in whatever's behind the label.
3. **Subtle depth** via `\usetikzlibrary{shadows}` and
   `drop shadow={shadow xshift=0.6pt, shadow yshift=-0.6pt, opacity=0.18}`.
4. **Color-group** related nodes (e.g. blue spine / green cluster / amber cluster)
   and add tiny uppercase cluster captions — it turns a node soup into a legible map.
5. Gradient node fills read as modern: `top color=brandmainlt, bottom color=white`.

## Family A — entity / domain model (ER-ish)

A vertical "spine" of core entities with side clusters. Route edges so no label
crosses a node; put side clusters on a clean grid.

```latex
\begin{tikzpicture}[
    entity/.style={draw, fill=white, rounded corners=3pt, minimum width=28mm,
      minimum height=9mm, font=\small\bfseries, align=center,
      drop shadow={shadow xshift=0.6pt, shadow yshift=-0.6pt, opacity=0.18}},
    spine/.style={entity, draw=brandmain, top color=brandmainlt, bottom color=white},
    side/.style={entity, draw=brandalt, top color=brandalt!18, bottom color=white},
    lbl/.style={font=\scriptsize\color{brandgray}, fill=white, inner sep=1.6pt},
    arr/.style={-{Latex[length=2.2mm]}, brandgray, semithick}, x=1cm, y=1cm]
  \node[spine] (a) at (0,6) {Workspace};
  \node[spine] (b) at (0,4.4) {Project};
  \node[spine] (c) at (0,2.8) {Item};
  \node[side]  (u) at (-4.6,4.4) {User};
  \draw[arr] (a) -- node[lbl]{contains} (b);
  \draw[arr] (b) -- node[lbl]{has many} (c);
  \draw[arr] (b.west) -- node[lbl,pos=.55]{owned by} (u.east);
  \node[font=\scriptsize\bfseries\color{brandmain}] at (0,6.7) {CORE};
\end{tikzpicture}
```

Key: place child nodes so vertical edges are straight; send side-cluster edges to
distinct anchors (`.north east`, `.south east`) so their labels don't stack.

## Family B — linear flow / wizard / pipeline

Numbered stages left-to-right with badges. Good for "how to create X" steps.

```latex
\begin{tikzpicture}[node distance=5mm,
    stg/.style={draw=brandmain, top color=brandmainlt, bottom color=white,
      rounded corners=3pt, minimum width=26mm, minimum height=13mm, align=center,
      font=\small\bfseries, text=brandink,
      drop shadow={shadow xshift=0.6pt, shadow yshift=-0.6pt, opacity=0.18}},
    badge/.style={circle, fill=brandmain, text=white, font=\scriptsize\bfseries,
      inner sep=1.4pt, minimum size=5.5mm},
    arr/.style={-{Latex[length=2.4mm]}, brandmain, thick}]
  \node[stg] (s1) {First\\Step};
  \node[stg, right=of s1] (s2) {Second\\Step};
  \node[stg, right=of s2] (s3) {Third\\Step};
  \foreach \i/\n in {s1/1, s2/2, s3/3} \node[badge] at (\i.north west) {\n};
  \draw[arr] (s1) -- (s2);  \draw[arr] (s2) -- (s3);
\end{tikzpicture}
```

## Family C — state machine / workflow (FSM)

Statuses as colored states, transitions as curved labeled arrows, plus a legend.
Use semantic colors: brand blue = active/open, green = success/terminal, amber =
rejected/terminal.

```latex
\begin{tikzpicture}[node distance=18mm and 30mm,
    st/.style={draw, rounded corners=3pt, minimum width=26mm, minimum height=12mm,
      align=center, font=\small\bfseries, text=brandink,
      drop shadow={shadow xshift=0.6pt, shadow yshift=-0.6pt, opacity=0.18}},
    open/.style={st, draw=brandmain, top color=brandmainlt, bottom color=white},
    done/.style={st, draw=okgreen, top color=okgreenlt, bottom color=white},
    stop/.style={st, draw=noamber, top color=noamberlt, bottom color=white},
    lbl/.style={font=\scriptsize\color{brandgray}, fill=white, inner sep=1.8pt},
    arr/.style={-{Latex[length=2.4mm]}, brandgray, semithick}]
  \node[open] (n) {NEW};
  \node[open, right=of n] (r) {REVIEW};
  \node[done, above right=8mm and 30mm of r] (a) {APPROVED};
  \node[stop, below right=8mm and 30mm of r] (x) {REJECTED};
  \draw[arr] (n) -- node[lbl,above]{submit} (r);
  \draw[arr] (r.east) to[out=25,in=180] node[lbl,pos=.55,sloped,above]{approve} (a.west);
  \draw[arr] (r.east) to[out=-25,in=180] node[lbl,pos=.55,sloped,below]{reject} (x.west);
\end{tikzpicture}
```

Add small `initial`/`terminal` tags under states with a `tag` style, and a small
swatch legend row so the color coding is self-explanatory.

## After every diagram

Render the page (`pdftoppm`, see environment.md) and LOOK. The #1 defect is edge
labels overlapping nodes — the `fill=white` mask fixes most, but crossing edges on
a hub node still need manual re-anchoring or orthogonal routing (`-|`, `|-`).
