"""Sphinx configuration for search-smith."""

project = "search-smith"
author = "Eiichi YAMAMOTO"
copyright = "2026, Eiichi YAMAMOTO"
release = "0.1.0"

extensions: list[str] = []

templates_path = ["_templates"]
exclude_patterns = []

html_theme = "furo"
html_title = "search-smith"
html_static_path = ["_static"]
