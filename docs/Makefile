.PHONY: help html clean

SPHINXOPTS ?= -W
SPHINXBUILD ?= sphinx-build
SOURCEDIR = source
BUILDDIR = build

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

html:
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

clean:
	rm -rf "$(BUILDDIR)"
