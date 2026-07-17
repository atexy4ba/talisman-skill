# TikZ diagram recipes (v1)

All assume the palette and shared styles from `preamble.tex`. Four families cover
most software docs. Each diagram in its own `figures/<name>.tex`, `\input` from the
chapter inside a `figure` environment.

## Universal rules (anti-collision)

1. **Never name a style `step`, `state`, `box`, `grid`, `node`** — reserved by TikZ.
2. **Mask edge labels**: use `lbl/.style` (pre-defined in preamble) — `fill=white`
   punches a hole behind the label.
3. **Color-group** related nodes and add cluster captions.
4. **Use pre-defined styles** from preamble (`spine`, `side`, `stg`, `open`, `done`,
   `stop`) instead of redefining every time.

## Family A — Domain model (ER-ish)

Vertical spine of core entities with side clusters. All styles pre-defined:

```latex
\begin{tikzpicture}
  \node[spine] (a) at (0,6) {EntityA};
  \node[spine] (b) at (0,4.4) {EntityB};
  \node[side]  (u) at (-4.6,4.4) {EntityC};
  \draw[arr] (a) -- node[lbl]{relates} (b);
  \draw[arr] (b.west) -- node[lbl,pos=.55]{owned by} (u.east);
  \node[font=\scriptsize\bfseries\color{brandmain}] at (0,6.7) {CORE};
\end{tikzpicture}
```

Add cluster labels with `\node[font=\scriptsize\bfseries\color{brandalt}]`.

## Family B — Flow / wizard / pipeline

Numbered stages left-to-right with auto-badged steps:

```latex
\begin{tikzpicture}[node distance=5mm]
  \node[stg] (s1) {First\\Step};
  \node[stg, right=of s1] (s2) {Second\\Step};
  \node[stg, right=of s2] (s3) {Third\\Step};
  \foreach \i/\n in {s1/1, s2/2, s3/3} \node[badge] at (\i.north west) {\n};
  \draw[arr] (s1) -- (s2);  \draw[arr] (s2) -- (s3);
\end{tikzpicture}
```

For 4+ steps, chain them with `right=of` and `node distance=4mm`.

## Family C — State machine (FSM)

Statuses as colored states with curved transitions. Semantic colors from preamble:

```latex
\begin{tikzpicture}[node distance=18mm and 30mm]
  \node[open] (n) {NEW};
  \node[open, right=of n] (r) {REVIEW};
  \node[done, above right=8mm and 30mm of r] (a) {APPROVED};
  \node[stop, below right=8mm and 30mm of r] (x) {REJECTED};
  \draw[arr] (n) -- node[lbl,above]{submit} (r);
  \draw[arr] (r.east) to[out=25,in=180]
    node[lbl,pos=.55,sloped,above]{approve} (a.west);
  \draw[arr] (r.east) to[out=-25,in=180]
    node[lbl,pos=.55,sloped,below]{reject} (x.west);
\end{tikzpicture}
```

Add legend: `\diagramlegend{brandmain}{Active}{okgreen}{Success}{noamber}{Reject}`

## Family D — Architecture / system layout

Box-within-box diagrams for system architecture, module nesting, or deployment:

```latex
\begin{tikzpicture}[
    container/.style={draw=brandmain, rounded corners=4pt, thick,
      inner sep=8pt, align=center, font=\small\bfseries},
    component/.style={draw=brandaccent, fill=brandbg, rounded corners=2pt,
      minimum width=20mm, minimum height=8mm, font=\small},
    arr/.style={-{Latex[length=2.2mm]}, brandgray, semithick}]
  \node[container] (sys) {System Name
    \tikz{\node[component] (c1) at (0,0) {Component A};
          \node[component] (c2) at (2.5,0) {Component B};
          \draw[arr] (c1) -- (c2);}};
\end{tikzpicture}
```

Or use `fit` for grouping:

```latex
\begin{tikzpicture}
  \node[component] (db) at (0,0) {Database};
  \node[component] (api) at (0,1.2) {API Layer};
  \node[component] (ui) at (0,2.4) {Frontend};
  \node[container, fit=(db)(api)(ui), label={above:Application}] {};
  \draw[arr] (ui) -- (api);
  \draw[arr] (api) -- (db);
\end{tikzpicture}
```

## Time-saver: reusable fragments

Shared styles are already in `preamble.tex`. For repeated diagram shapes, use
`\tikzset` in a shared `figures/common.tex` file.

## Performance: standalone diagram compilation

For large documents, compile each diagram as a standalone PDF once:

```bash
for f in figures/*.tex; do
  pdflatex -jobname="figures/$(basename $f .tex)" \
    "\documentclass{standalone}\input{preamble}\begin{document}\input{$f}\end{document}"
done
```

Then in chapters: `\includegraphics{figures/diagram-name}`.
This avoids recompiling TikZ on every build run.
