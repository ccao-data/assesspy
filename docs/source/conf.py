# Configuration file for the Sphinx documentation builder.

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