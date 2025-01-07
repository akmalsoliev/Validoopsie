project = "Validoopsie"
copyright = "2025, Akmal Soliev"
author = "Akmal Soliev"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "piccolo_theme",
    "myst_parser",
]

templates_path = ["_templates"]
exclude_patterns = []

source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "markdown",
    ".md": "markdown",
}

html_theme = "piccolo_theme"
html_logo = "../../assets/validoopsie-text.png"
html_favicon = "../../assets/logo.png"
html_static_path = ["_static"]
