# Configuration file for the Sphinx documentation builder.
#
# Full list of options can be found in the Sphinx documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sys
import os

sys.path.append(os.path.abspath('../..'))

# -- Project information -------------------------------------------------------

project = 'assesspy'
author = 'Cook County Assessor Data Department'
copyright = "2022, Cook County Assessor Data Department"
release = '1.0'

# -- General configuration -----------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'myst_nb',
    ]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output ---------------------------------------------------

highlight_language = 'none'
html_theme = 'furo'
html_logo = "../images/logo.png"
html_show_copyright = False

# -- Options for HTML output ---------------------------------------------------

source_suffix = {
    '.rst': 'restructuredtext',
    '.ipynb': 'myst-nb'
}

myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "html_image",
]

suppress_warnings = ["mystnb.unknown_mime_type"]