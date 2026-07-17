# talisman build — three backends, pick the fastest one that works.
# Probe order: tectonic > latexmk > pdflatex (fallback).
# Usage:
#   make          — auto-detect best backend and build
#   make fast     — force tectonic (fastest)
#   make smart    — force latexmk (auto pass-count)
#   make safe     — force 3x pdflatex (works everywhere)
#   make clean    — remove build artifacts

MAIN := main
TEXFLAGS := -interaction=nonstopmode -halt-on-error

.PHONY: all fast smart safe clean

all:
	@if command -v tectonic >/dev/null 2>&1; then \
	  echo "=== tectonic (fastest) ===" && \
	  tectonic $(MAIN).tex; \
	elif command -v latexmk >/dev/null 2>&1; then \
	  echo "=== latexmk (smart passes) ===" && \
	  latexmk -pdf -interaction=nonstopmode $(MAIN).tex; \
	else \
	  echo "=== pdflatex 3-pass (fallback) ===" && \
	  pdflatex $(TEXFLAGS) $(MAIN).tex && \
	  pdflatex $(TEXFLAGS) $(MAIN).tex && \
	  pdflatex $(TEXFLAGS) $(MAIN).tex; \
	fi

fast:
	tectonic $(MAIN).tex

smart:
	latexmk -pdf -interaction=nonstopmode $(MAIN).tex

safe:
	pdflatex $(TEXFLAGS) $(MAIN).tex
	pdflatex $(TEXFLAGS) $(MAIN).tex
	pdflatex $(TEXFLAGS) $(MAIN).tex

# Separate targets for each backend to enable parallel diagram builds
diagrams: $(wildcard figures/*.tex)
	@for f in $^; do \
	  base=$$(basename "$$f" .tex); \
	  echo "Building $$base..."; \
	  pdflatex -interaction=nonstopmode "$$f" 2>/dev/null || true; \
	done

# pdfjam or similar for merging standalone diagrams if needed
merge: diagrams
	@if command -v pdfjam >/dev/null 2>&1; then \
	  echo "Diagrams prepared as standalone PDFs"; \
	fi

clean:
	rm -f *.aux *.log *.toc *.out *.lof *.lot *.fdb_latexmk *.fls *.synctex.gz
	rm -f chapters/*.aux figures/*.aux figures/*.log figures/*.pdf
	rm -f $(MAIN).pdf
