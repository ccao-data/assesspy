# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information ----------------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
import os

sys.path.append(os.path.abspath('../..'))

project = 'assesspy'
author = 'Cook County Assessor Data Department'
copyright = "2022, Cook County Assessor Data Department"
release = '1.0'

# -- General configuration ----------------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'nbsphinx',
    'recommonmark',
    ]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output ----------------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
html_logo = "../images/logo.png"

# Use svg rather than png for matlib plots

nbsphinx_execute_arguments = [
    "--InlineBackend.figure_formats={'svg', 'pdf'}",
    "--InlineBackend.rc=figure.dpi=96",
]