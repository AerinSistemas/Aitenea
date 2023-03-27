# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    = 
SPHINXBUILD   = sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build
PAPER         =

PAPEROPT_a4     = -D latex_paper_size=a4
LATEX-NAME = aitenea

SCREENOPTS = -D latex_elements.pointsize=12pt -D latex_elements.classoptions=,openany,oneside -D latex_elements.preamble=\\usepackage{mfgan} -D pygments_style=my_pygment_style.BookStyle -D code_example_wrap=67
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help makefile pdf

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

%: pdf
	$(SPHINXBUILD) -b latex $(SCREENOPTS) $(ALLSPHINXOPTS) $(BUILDDIR)/latex
	sed -i .bak -f process-latex $(BUILDDIR)/latex/$(LATEX-NAME).tex
	rsync -a latex/ $(BUILDDIR)/latex/
	$(MAKE) -C $(BUILDDIR)/latex pdf