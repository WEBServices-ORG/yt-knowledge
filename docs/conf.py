# Configuration file for the Sphinx documentation builder.

project = "yt-knowledge"
copyright = "2024, User"
author = "User"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
]

templates_path = ["_templates"]
exclude_patterns = []

html_theme = "alabaster"
html_static_path = ["_static"]
