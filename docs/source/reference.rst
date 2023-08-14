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

Kakwani Index and Modified Kakwani Index (KI_MKI)
^^^^^^^^^^^^^^^^^^^^^^^^

The Kakwani Index (KI) and the Modified Kakwani Index (MKI) are Gini-based measures
to test for vertical equity. The work by comparing the cumulative distribution of
assessed values to the distribution of sale prices.

:doc:`mki() <mki>` |nbsp|
:doc:`mk_met() <mki_met>` |nbsp|
:doc:`ki() <ki>`

Other functions
^^^^^^^^^^^^^^^

| Calculate bootstrapped confidence intervals

:doc:`boot_ci() <ci>`

| Detect sales chasing in a vector of sales ratios

:doc:`detect_chasing() <sales_chasing>` |nbsp|
:doc:`detect_chasing_cdf() <sales_chasing>` |nbsp|
:doc:`detect_chasing_dist() <sales_chasing>`

| Calculate bootstrapped confidence intervals

:doc:`is_outlier() <outliers>` |nbsp|
:doc:`quantile_outlier() <outliers>` |nbsp|
:doc:`iqr_outlier() <outliers>`

Data
----

| Sample data used for testing and demonstrations

:doc:`ratios_sample() <ratios_sample>`

.. |nbsp| unicode:: 0xA0
