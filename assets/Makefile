# talisman build. Three pdflatex passes: cross-refs + TOC + tikz overlay
# ("remember picture") all need a second pass; the third stabilizes page numbers
# after the TOC shifts everything. Switch to lualatex ONLY if you confirmed its
# font runtime works (see references/environment.md) — pdflatex is the safe default.
MAIN := main
TEXFLAGS := -interaction=nonstopmode -halt-on-error

.PHONY: all clean
all: $(MAIN).pdf

$(MAIN).pdf: main.tex preamble.tex $(wildcard chapters/*.tex) $(wildcard figures/*.tex)
	pdflatex $(TEXFLAGS) $(MAIN).tex
	pdflatex $(TEXFLAGS) $(MAIN).tex
	pdflatex $(TEXFLAGS) $(MAIN).tex

clean:
	rm -f *.aux *.log *.toc *.out *.lof *.lot chapters/*.aux $(MAIN).pdf
