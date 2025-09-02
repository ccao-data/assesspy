import random
from typing import Union

import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype

CCAO_LOWER_QUANTILE = 0.05
CCAO_UPPER_QUANTILE = 0.95


# Pulled from data architecture master
def ccao_drop_outliers(
    estimate: Union[list[int], list[float], pd.Series],
    sale_price: Union[list[int], list[float], pd.Series],
) -> tuple[pd.Series, pd.Series, float]:
    """
    Helper function to drop the top and bottom N% (usually 5%) of the input
    ratios, per CCAO SOPs and IAAO recommendation.
    """
    ratio: pd.Series = estimate / sale_price
    ratio_not_outlier = ratio.between(
        ratio.quantile(CCAO_LOWER_QUANTILE),
        ratio.quantile(CCAO_UPPER_QUANTILE),
        inclusive="neither",
    ).reset_index(drop=True)

    estimate_no_outliers = estimate[ratio_not_outlier]
    sale_price_no_outliers = sale_price[ratio_not_outlier]
    n: float = float(estimate_no_outliers.size)

    return estimate_no_outliers, sale_price_no_outliers, n


# Copied from master


def check_inputs(*args, check_gt_zero: bool = True) -> None:
    out_msg = [""]
    for x in args:
        check = pd.Series(x)

        if not is_numeric_dtype(check):
            out_msg.append("All input values must be numeric.")
        if check.isnull().any():
            out_msg.append("All input values cannot be null.")
        if len(check) <= 1:
            out_msg.append("All input values must have length greater than 1.")
        if not all(np.isfinite(check) | check.isnull()):
            out_msg.append("All input values cannot be infinite.")
        if any(check <= 0) and check_gt_zero:
            out_msg.append("All input values must be greater than 0.")

    lengths = [len(pd.Series(x)) for x in args]
    if len(set(lengths)) > 1:
        out_msg.append("All input values must have the same length.")

    out_msg_set = set(out_msg)
    if len(out_msg_set) > 1:
        raise Exception("\n".join(out_msg_set))


def _calculate_gini(
    estimate: Union[list[int], list[float], pd.Series],
    sale_price: Union[list[int], list[float], pd.Series],
) -> tuple[float, float]:
    """
    Helper function to calculate the Gini coefficients of sales and estimated
    values. Note that the estimated value Gini is based on the sale price order.
    """
    check_inputs(estimate, sale_price)

    estimate = (
        pd.Series(estimate, dtype=float)
        .rename("estimate")
        .reset_index(drop=True)
    )
    sale_price = (
        pd.Series(sale_price, dtype=float)
        .rename("sale_price")
        .reset_index(drop=True)
    )
    df = pd.concat([estimate, sale_price], axis=1)
    # Mergesort is required for stable sort results
    # I think it's better here to add a second sort for fmv too
    df.sort_values(by=["sale_price"], kind="mergesort", inplace=True)
    df.reset_index(drop=True, inplace=True)
    a_sorted, sp_sorted = df["estimate"], df["sale_price"]
    n: int = a_sorted.size

    assessed_sum: float = sum(a_sorted[i] * (i + 1) for i in range(n))
    g_assessed: float = 2 * assessed_sum / a_sorted.sum() - (n + 1)
    gini_assessed: float = g_assessed / float(n)

    sale_price_sum: float = sum(sp_sorted[i] * (i + 1) for i in range(n))
    g_sale_price: float = 2 * sale_price_sum / sp_sorted.sum() - (n + 1)
    gini_sale_price: float = g_sale_price / float(n)

    return gini_assessed, gini_sale_price


def mki(
    estimate: Union[list[int], list[float], pd.Series],
    sale_price: Union[list[int], list[float], pd.Series],
) -> float:
    r"""
    The Modified Kakwani Index (MKI) is a Gini-based measure to test for
    vertical equity in assessment. It first orders properties by sale price
    (ascending), then calculates the Gini coefficient for sale values
    and estimated values (while remaining ordered by sale price). The
    Modified Kakwani Index is the ratio between the coefficients:
    $Gini of Estimated Values / Gini of Sale Prices$.

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
    :type estimate: Array-like numeric values
    :type sale_price: Array-like numeric values

    :return: A single float value containing the MKI of the inputs.
    :rtype: float

    :Example:

    .. code-block:: python

        # Calculate MKI:
        import assesspy as ap

        ap.mki(ap.ccao_sample().estimate, ap.ccao_sample().sale_price)
    """
    check_inputs(estimate, sale_price)
    estimate = pd.Series(estimate, dtype=float)
    sale_price = pd.Series(sale_price, dtype=float)

    gini_assessed, gini_sale_price = _calculate_gini(estimate, sale_price)
    mki = float(gini_assessed / gini_sale_price)

    return mki


df = pd.read_csv("assesspy/data/test_data.csv")

# Exported two datasets here with different random seeds and they were identical
# There were no differences in the non-outliers
df_1 = ccao_drop_outliers(df.fmv, df.sale_price)
df_1 = pd.DataFrame({"fmv": df_1[0], "sale_price": df_1[1]})

output = mki(df_1.fmv, df_1.sale_price)

random.seed(4356)

output_2 = mki(df_1.fmv, df_1.sale_price)

output
output_2
