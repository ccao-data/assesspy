# Import necessary libraries
import numpy as np
import statsmodels.api as sm
from .utils import check_inputs


# COD, PRD, PRB functions
def cod(ratio):

    """
    COD is the average absolute percent deviation from the
    median ratio. It is a measure of horizontal equity in assessment.
    Horizontal equity means properties with a similar fair market value
    should be similarly assessed.

    Lower COD indicates higher uniformity/horizontal equity in assessment.
    The IAAO sets uniformity standards that define generally accepted ranges
    for COD depending on property class. See `IAAO Standard on Ratio Studies`_
    Section 9.1, Table 1.3 for a full list of standard COD ranges.

    .. _IAAO Standard on Ratio Studies: https://www.iaao.org/media/standards/Standard_on_Ratio_Studies.pdf

    .. note::
        The IAAO recommends trimming outlier ratios before calculating COD,
        as it is extremely sensitive to large outliers. The typical method used is
        dropping values beyond 3 * IQR (inner-quartile range). See
        `IAAO Standard on Ratio Studies`_ Appendix B.1.

    :param ratio:
        A numeric vector of ratios centered around 1, where the
        numerator of the ratio is the estimated fair market value and the
        denominator is the actual sale price.
    :type ratio: numeric

    :return: A numeric vector containing the COD of ``ratios``.
    :rtype: float

    :Example:

    .. code-block:: python

        # Calculate COD:
        import assesspy as ap

        ap.cod(ap.ratios_sample().ratio)
    """

    # Input checking and error handling
    check_inputs(ratio)

    ratio = np.array(ratio)

    n = ratio.size
    median_ratio = np.median(ratio)
    cod = 100 / median_ratio * (sum(abs(ratio - median_ratio)) / n)

    return cod


def prd(assessed, sale_price):

    """
    PRD is the mean ratio divided by the mean ratio weighted by sale
    price. It is a measure of vertical equity in assessment. Vertical equity
    means that properties at different levels of the income distribution
    should be similarly assessed.

    PRD centers slightly above 1 and has a generally accepted value of between
    0.98 and 1.03, as defined in the `IAAO Standard on Ratio Studies`_
    Section 9.2.7. Higher PRD values indicate regressivity in assessment.

    .. _IAAO Standard on Ratio Studies: https://www.iaao.org/media/standards/Standard_on_Ratio_Studies.pdf

    .. note::
       The IAAO recommends trimming outlier ratios before calculating PRD,
       as it is extremely sensitive to large outliers. PRD is being deprecated in
       favor of PRB, which is less sensitive to outliers and easier to interpret.

    :param assessed:
        A numeric vector of assessed values. Must be the same length as ``sale_price``.
    :param sale_price:
        A numeric vector of sale prices. Must be the same length
        as ``assessed``.
    :type assessed: numeric
    :type sale_price: numeric

    :return: A numeric vector containing the PRD of the input vectors.
    :rtype: float

    :Example:

    .. code-block:: python

        # Calculate PRD:
        import assesspy as ap

        ap.prd(ap.ratios_sample().assessed, ap.ratios_sample().sale_price)
    """

    assessed = np.array(assessed)
    sale_price = np.array(sale_price)

    # Input checking and error handling
    check_inputs(assessed, sale_price)

    ratio = assessed / sale_price
    prd = ratio.mean() / np.average(a=ratio, weights=sale_price)

    return prd


def prb(assessed, sale_price, round=None):

    """
    PRB is an index of vertical equity that quantifies the
    relationship betweem ratios and assessed values as a percentage. In
    concrete terms, a PRB of 0.02 indicates that, on average, ratios increase
    by 2\% whenever assessed values increase by 100 percent.

    PRB is centered around 0 and has a generally accepted value of between
    -0.05 and 0.05, as defined in the `IAAO Standard on Ratio Studies`_
    Section 9.2.7. Higher PRB values indicate progressivity in assessment,
    while negative values indicate regressivity.

    .. _IAAO Standard on Ratio Studies: https://www.iaao.org/media/standards/Standard_on_Ratio_Studies.pdf

    .. note: PRB is significantly less sensitive to outliers than PRD or COD.

    :param assessed:
        A numeric vector of assessed values. Must be the same
        length as ``sale_price``.
    :param sale_price:
        A numeric vector of sale prices. Must be the same length
        as ``assessed``.
    :param round:
        Indicate desired rounding for output.
    :type assessed: numeric
    :type sale_price: numeric
    :type round: int

    :return: A numeric vector containing the PRB of the input vectors.
    :rtype: float

    :Example:

    .. code-block:: python

        # Calculate PRB:
        import assesspy as ap

        ap.prb(ap.ratios_sample().assessed, ap.ratios_sample().sale_price)
    """

    assessed = np.array(assessed)
    sale_price = np.array(sale_price)

    # Input checking and error handling
    check_inputs(assessed, sale_price)

    ratio = assessed / sale_price
    median_ratio = np.median(ratio)

    lhs = (ratio - median_ratio) / median_ratio
    rhs = np.log(((assessed / median_ratio) + sale_price) / 2) / np.log(2)

    lhs = np.array(lhs)
    rhs = np.array(rhs)

    prb_model = sm.OLS(lhs, rhs).fit()

    prb_val = float(prb_model.params)
    prb_ci = prb_model.conf_int(alpha=0.05)[0].tolist()

    if round is not None:

        prb_val = np.round(prb_val, round)
        prb_ci = np.round(prb_ci, round)

    return {"prb": prb_val, "95% ci": prb_ci}


# Functions to determine whether assessment fairness criteria has been met
def cod_met(x): return 5 <= x <= 15


def prd_met(x): return 0.98 <= x <= 1.03


def prb_met(x): return -0.05 <= x <= 0.05
