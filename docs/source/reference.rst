=========
Reference
=========

Functions
---------

Coefficient of Dispersion (COD)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

COD is the average absolute percent deviation from the median ratio.
It is a measure of horizontal equity in assessment. Horizontal equity means
properties with a similar fair market value should be similarly assessed.

:doc:`cod() <cod>` |nbsp|
:doc:`cod_ci() <cod>` |nbsp|
:doc:`cod_met() <cod>`


Price-Related Differential (PRD)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

PRD is the mean ratio divided by the mean ratio weighted by sale price.
It is a measure of vertical equity in assessment. Vertical equity means
that properties at different levels of the income distribution should be
similarly assessed.

:doc:`prd() <prd>` |nbsp|
:doc:`prd_ci() <prd>` |nbsp|
:doc:`prd_met() <prd>`


Price-Related Bias (PRB)
^^^^^^^^^^^^^^^^^^^^^^^^

PRB is an index of vertical equity that quantifies the relationship betweem
ratios and assessed values as a percentage. In concrete terms, a PRB of 0.02
indicates that, on average, ratios increase by 2% whenever assessed values
increase by 100 percent.

:doc:`prb() <prb>` |nbsp|
:doc:`prb_ci() <prb>` |nbsp|
:doc:`prb_met() <prb>`


Kakwani Index (KI)
^^^^^^^^^^^^^^^^^^

The Kakwani Index (KI) is a Gini-based measure to test for vertical equity.
The output is the ordered cumulative distribution of assessed values minus
the ordered distribution of sale prices.

:doc:`ki() <ki>`


Modified Kakwani Index (MKI)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Modified Kakwani Index (MKI) is a Gini-based measure to test for vertical
equity. The output is the ordered cumulative distribution of assessed values
divided by the ordered distribution of sale prices.

:doc:`mki() <mki>` |nbsp|
:doc:`mki_met() <mki>`


Other functions
^^^^^^^^^^^^^^^

| Calculate confidence intervals

:doc:`boot_ci() <ci>`

| Detect sales chasing in sale ratios

:doc:`is_sales_chased() <sales_chasing>`

| Detect outlier values

:doc:`is_outlier() <outliers>`

| Calculate if median_ratio is within the acceptable range

:doc:`med_ratio_met() <med_ratio_met>`


Data
----

| Sample data used for testing and demonstrations

:doc:`ccao_sample() <ccao_sample>`
:doc:`quintos_sample() <quintos_sample>`

.. |nbsp| unicode:: 0xA0
