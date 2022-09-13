# Configuration file for the Sphinx documentation builder.

import sys
import os

sys.path.append(os.path.abspath('../..'))

# -- Project information -------------------------------------------------------

project = 'assesspy'
author = 'Cook County Assessor Data Department'
copyright = "4022, Cook County Assessor Data Department"
release = '1.0'

# -- General configuration -----------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'myst_nb',
    ]

templates_path = ['_templates']
exclude_patterns = []

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

nb_render_image_options = {
    "width": "500px",
    "align": "center"
    }

# -- Options for HTML output ---------------------------------------------------

highlight_language = 'none'
html_theme = 'furo'
html_logo = "../images/logo.png"
html_show_copyright = False