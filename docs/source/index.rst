.. assesspy documentation master file, created by
   sphinx-quickstart on Mon Aug 22 13:41:30 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

AssessPy package
================

.. toctree::
   :hidden:
   :caption: Contents:

   reference
   vignettes

.. toctree::
   :hidden:
   :caption: Appendix:

   authors
   license
   Source Code <https://github.com/ccao-data/assesspy>

AssessPy is a software package for Python developed by the Cook County
Assessor's (CCAO) Data Department. The codebase for the CCAO's CAMA system
uses a wide range of functions regularly, and packaging these functions
streamlines and standardizes their use. The CCAO is publishing this package
to make it available to assessors, reporters, and citizens everywhere.

For assessors, we believe that this package will reduce the complexity
of calculating ratio statistics and detecting sales chasing. We also
believe that reporters, taxpayers, and members of academia will find
this package helpful in monitoring the performance of local assessors
and conducting research.

For detailed documentation on included functions and data, :doc:`visit the
full reference list <reference>`_.

For examples of specific tasks you can complete with ``assesspy``
functions, see the :doc:`vignettes page <vignettes>`_.

Installation
------------

You can install the released version of ``assesspy`` using pip:

.. code-block:: python

    pip install assesspy

Once it's installed, you can use it just like any other package. Simply
call ``import assesspy`` at the beginning of your script.
