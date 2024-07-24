import os
import sys

sys.path.append(os.path.abspath("../.."))

# Loads config from pyproject.toml
from sphinx_pyproject import SphinxConfig
config = SphinxConfig("../../pyproject.toml", globalns=globals())

# These options need to stay here since they're dictionaries
# which can't be parsed by sphinx-pyproject
source_suffix = {".rst": "restructuredtext", ".ipynb": "myst-nb"}
nb_render_image_options = {"width": "450px", "align": "center"}
