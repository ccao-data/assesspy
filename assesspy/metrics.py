import math

import pandas as pd
import statsmodels.api as sm

from .utils import check_inputs


def cod(
    estimate: list[int] | list[float] | pd.Series,
    sale_price: list[int] | list[float] | pd.Series,
) -> float:
    """
    COD is the average absolute percent deviation from the median ratio.
    It is a measure of horizontal equity in assessment. Horizontal equity means
    properties with a similar fair market value should be similarly assessed.

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

    :param estimate:
        A list or ``pd.Series`` of estimated values.
        Must be the same length as ``sale_price``.
    :param sale_price:
        A list or ``pd.Series`` of sale prices.
        Must be the same length as ``estimate``.
    :type estimate: pd.Series
    :type sale_price: pd.Series

    :return: A single float value containing the COD of the inputs.
    :rtype: float

    :Example:

    .. code-block:: python

        # Calculate COD:
        import assesspy as ap

        ap.cod(ap.ratios_sample().estimate, ap.ratios_sample().sale_price)
    """
    check_inputs(estimate, sale_price)
    estimate = pd.Series(estimate, dtype=float)
    sale_price = pd.Series(sale_price, dtype=float)
    ratio: pd.Series = estimate / sale_price

    n: int = ratio.size
    median_ratio: float = ratio.median()
    ratio_minus_med: pd.Series = ratio - median_ratio
    abs_diff_sum: float = ratio_minus_med.abs().sum()
    cod: float = float(100 / median_ratio * (abs_diff_sum / n))

    return cod


def prd(
    estimate: list[float | int] | pd.Series,
    sale_price: list[float | int] | pd.Series,
) -> float:
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
       favor of PRB and MKI, which are less sensitive to outliers and easier
       to interpret.

    :param estimate:
        A list or ``pd.Series`` of estimated values.
        Must be the same length as ``sale_price``.
    :param sale_price:
        A list or ``pd.Series`` of sale prices.
        Must be the same length as ``estimate``.
    :type estimate: pd.Series
    :type sale_price: pd.Series

    :return: A single float value containing the PRD of the inputs.
    :rtype: float

    :Example:

    .. code-block:: python

        # Calculate PRD:
        import assesspy as ap

        ap.prd(ap.ratios_sample().estimate, ap.ratios_sample().sale_price)
    """
    check_inputs(estimate, sale_price)
    estimate = pd.Series(estimate, dtype=float)
    sale_price = pd.Series(sale_price, dtype=float)
    ratio: pd.Series = estimate / sale_price

    prd: float = float(
        ratio.mean() / (ratio * sale_price / sale_price.sum()).sum()
    )

    return prd


def prb(
    estimate: list[float | int] | pd.Series,
    sale_price: list[float | int] | pd.Series,
) -> float:
    r"""
    PRB is an index of vertical equity that quantifies the
    relationship between ratios and estimated values as a percentage. In
    concrete terms, a PRB of 0.02 indicates that, on average, ratios increase
    by 2\% whenever the estimated values increase by 100 percent.

    PRB is centered around 0 and has a generally accepted value of between
    -0.05 and 0.05, as defined in the `IAAO Standard on Ratio Studies`_
    Section 9.2.7. Higher PRB values indicate progressivity in assessment,
    while negative values indicate regressivity.

    .. _IAAO Standard on Ratio Studies: https://www.iaao.org/media/standards/Standard_on_Ratio_Studies.pdf

    .. note: PRB is significantly less sensitive to outliers than PRD or COD.

    :param estimate:
        A list or ``pd.Series`` of estimated values.
        Must be the same length as ``sale_price``.
    :param sale_price:
        A list or ``pd.Series`` of sale prices.
        Must be the same length as ``estimate``.
    :type estimate: pd.Series
    :type sale_price: pd.Series

    :return: A single float value containing the PRB of the inputs.
    :rtype: float

    :Example:

    .. code-block:: python

        # Calculate PRB:
        import assesspy as ap

        ap.prb(ap.ratios_sample().estimate, ap.ratios_sample().sale_price)
    """
    check_inputs(estimate, sale_price)
    estimate = pd.Series(estimate, dtype=float)
    sale_price = pd.Series(sale_price, dtype=float)
    ratio: pd.Series = estimate / sale_price
    median_ratio: float = ratio.median()

    lhs: pd.Series = (ratio - median_ratio) / median_ratio
    rhs: pd.Series = ((estimate / median_ratio) + sale_price).apply(
        lambda x: math.log2(x / 2)
    )

    prb_model = sm.OLS(lhs.to_numpy(), rhs.to_numpy()).fit()
    prb = float(prb_model.params[0])

    return prb


def _calculate_gini(
    estimate: list[float | int] | pd.Series,
    sale_price: list[float | int] | pd.Series,
) -> tuple[float, float]:
    """
    Helper function to calculate the Gini coefficients of sales and estimated
    values. Note that the estimated value Gini is based on the sale price order.
    """
    check_inputs(estimate, sale_price)

    # Mergesort is required for stable sort results
    df = pd.DataFrame(
        {"estimate": estimate, "sale_price": sale_price}
    ).sort_values(by="sale_price", kind="mergesort")
    a_sorted: pd.Series = df["estimate"]
    sp_sorted: pd.Series = df["sale_price"]
    n: int = a_sorted.size

    assessed_sum: float = sum(a_sorted[i] * (i + 1) for i in range(n))
    g_assessed: float = 2 * assessed_sum / a_sorted.sum() - (n + 1)
    gini_assessed: float = g_assessed / float(n)

    sale_price_sum: float = sum(sp_sorted[i] * (i + 1) for i in range(n))
    g_sale_price: float = 2 * sale_price_sum / sp_sorted.sum() - (n + 1)
    gini_sale_price: float = g_sale_price / float(n)

    return gini_assessed, gini_sale_price


def mki(
    estimate: list[float | int] | pd.Series,
    sale_price: list[float | int] | pd.Series,
) -> float:
    r"""
        The Modified Kakwani Index (MKI) is a Gini-based measure to test for
        vertical equity in assessment. It first orders properties by sale price
        (ascending), then calculates the Gini coefficient for sale values
        and estimated values (while remaining ordered by sale price). The
        Modified Kakwani Index is the ratio between the coefficients:
        $Gini of Estimated Values / Gini of Sale Prices$.
    _
        For the Modified Kakwani Index:

        MKI < 1 is regressive
        MKI = 1 is vertical equity
        MKI > 1 is progressive

        .. Quintos, C. (2020). A Gini measure for vertical equity in property
            assessments. https://researchexchange.iaao.org/jptaa/vol17/iss2/2

        .. Quintos, C. (2021). A Gini decomposition of the sources of inequality in
            property assessments. https://researchexchange.iaao.org/jptaa/vol18/iss2/6

        :param estimate:
            A list or ``pd.Series`` of estimated values.
            Must be the same length as ``sale_price``.
        :param sale_price:
            A list or ``pd.Series`` of sale prices.
            Must be the same length as ``estimate``.
        :type estimate: pd.Series
        :type sale_price: pd.Series

        :return: A single float value containing the MKI of the inputs.
        :rtype: float

        :Example:

        .. code-block:: python

            # Calculate MKI:
            import assesspy as ap

            ap.mki(ap.ratios_sample().estimate, ap.ratios_sample().sale_price)
    """
    check_inputs(estimate, sale_price)
    estimate = pd.Series(estimate, dtype=float)
    sale_price = pd.Series(sale_price, dtype=float)

    gini_assessed, gini_sale_price = _calculate_gini(estimate, sale_price)
    mki = float(gini_assessed / gini_sale_price)

    return mki


def ki(
    estimate: list[float | int] | pd.Series,
    sale_price: list[float | int] | pd.Series,
) -> float:
    r"""
    The Kakwani Index (KI) is a Gini-based measure to test for
    vertical equity in assessment. It first orders properties by sale price
    (ascending), then calculates the Gini coefficient for sale values and
    estimated values (while remaining ordered by sale price). The Kakwani Index
    is the difference between the coefficients:
    $Gini of Estimated Values - Gini of Sale Prices$.

    For the Kakwani Index:

    KI < 0 is regressive
    KI = 0 is vertical equity
    KI > 0 is progressive

    :param estimate:
        A list or ``pd.Series`` of estimated values.
        Must be the same length as ``sale_price``.
    :param sale_price:
        A list or ``pd.Series`` of sale prices.
        Must be the same length as ``estimate``.
    :type estimate: pd.Series
    :type sale_price: pd.Series

    :return: A single float value containing the PRB of the inputs.
    :rtype: float

    :Example:

    .. code-block:: python

        # Calculate KI:
        import assesspy as ap

        ap.ki(ap.ratios_sample().estimate, ap.ratios_sample().sale_price)
    """

    check_inputs(estimate, sale_price)
    estimate = pd.Series(estimate, dtype=float)
    sale_price = pd.Series(sale_price, dtype=float)

    gini_assessed, gini_sale_price = _calculate_gini(estimate, sale_price)
    ki = float(gini_assessed - gini_sale_price)

    return ki


# Functions to determine whether IAAO/Quintos fairness criteria is met
def cod_met(x: float) -> bool:
    return 5 <= x <= 15


def prd_met(x: float) -> bool:
    return 0.98 <= x <= 1.03


def prb_met(x: float) -> bool:
    return -0.05 <= x <= 0.05


def mki_met(x: float) -> bool:
    return 0.95 <= x <= 1.05