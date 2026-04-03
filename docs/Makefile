# Makefile for Sphinx documentation

SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

.PHONY: help html clean serve

help:
	@echo "Available targets:"
	@echo "  html   - Build HTML documentation"
	@echo "  serve  - Start local development server"
	@echo "  clean  - Remove build artifacts"

html:
	$(SPHINXBUILD) -b html $(SPHINXOPTS) $(SOURCEDIR) $(BUILDDIR)
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

serve: html
	@echo "Starting server at http://localhost:8000"
	@cd $(BUILDDIR)/html && python -m http.server 8000

clean:
	rm -rf $(BUILDDIR)/*
	@echo "Build artifacts cleaned."