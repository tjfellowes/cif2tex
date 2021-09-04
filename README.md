# cif2tex

A little tool to generate crystal data (for a thesis or manuscript) in LaTeX. Should work with all valid CIFs. If no datablock is supplied it will parse the first one found. Just needs cctbx (install with conda).

## Usage
python cif2tex.py test.cif [optional CIF datablock name]

Prints the raw LaTeX to stdout and also produces a minimal .tex file which can be compiled with pdflatex. 
