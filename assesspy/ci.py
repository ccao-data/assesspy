import math

import pandas as pd
import statsmodels.api as sm

from .metrics import cod, prd
from .utils import check_inputs


def boot_ci(
    fun,
    estimate: list[int] | list[float] | pd.Series,
    sale_price: list[int] | list[float] | pd.Series,
    nboot: int = 1000,
    alpha: float = 0.05,
) -> tuple[float, float]:
    """
    Calculate the non-parametric bootstrap confidence interval
    for a given set of numeric values and a chosen function.

    :param fun:
        Function to bootstrap. Must return a single float value.
    :param estimate:
        A list or ``pd.Series`` of estimated values.
        Must be the same length as ``sale_price``.
    :param sale_price:
        A list or ``pd.Series`` of sale prices.
        Must be the same length as ``estimate``.
    :param nboot:
        Default 1000. Number of iterations to use to estimate
        the output statistic confidence interval.
    :param alpha:
        Default 0.05. Float value indicating the confidence
        interval to return. 0.05 will return the 95% confidence interval.
    :type fun: function
    :type estimate: list[int] | list[float] | pd.Series
    :type sale_price: list[int] | list[float] | pd.Series
    :type nboot: int
    :type alpha: float

    :return:
        A tuple of floats containing the bootstrapped confidence
        interval of the input values.
    :rtype: tuple[float, float]

    :Example:

    .. code-block:: python

        # Calculate PRD confidence interval:
        import assesspy as ap

        ap.boot_ci(
            ap.prd,
            estimate = ap.ccao_sample().estimate,
            sale_price = ap.ccao_sample().sale_price,
            nboot = 1000
        )
    """
    if nboot <= 0:
        raise ValueError("'nboot' must be a positive integer greater than 0.")
    check_inputs(estimate, sale_price)
    df = pd.DataFrame({"estimate": estimate, "sale_price": sale_price})
    n: int = df.size

    # Take a random sample of input, with the same number of rows as input,
    # with replacement
    ests = pd.Series(index=range(nboot), dtype=float)
    for i in range(nboot):
        sample = df.sample(n=n, replace=True)
        ests[i] = fun(sample.iloc[:, 0], sample.iloc[:, 1])

    ci = (ests.quantile(alpha / 2), ests.quantile(1 - alpha / 2))

    return ci


def cod_ci(
    estimate: list[int] | list[float] | pd.Series,
    sale_price: list[int] | list[float] | pd.Series,
    nboot: int = 1000,
    alpha: float = 0.05,
) -> tuple[float, float]:
    """
    Calculate the non-parametric bootstrap confidence interval for COD.

    See also:
        :func:`boot_ci`
    """
    return boot_ci(
        cod, estimate=estimate, sale_price=sale_price, nboot=nboot, alpha=alpha
    )


def prd_ci(
    estimate: list[int] | list[float] | pd.Series,
    sale_price: list[int] | list[float] | pd.Series,
    nboot: int = 1000,
    alpha: float = 0.05,
) -> tuple[float, float]:
    """
    Calculate the non-parametric bootstrap confidence interval for PRD.

    See also:
        :func:`boot_ci`
    """
    return boot_ci(
        prd, estimate=estimate, sale_price=sale_price, nboot=nboot, alpha=alpha
    )


def prb_ci(
    estimate: list[int] | list[float] | pd.Series,
    sale_price: list[int] | list[float] | pd.Series,
    nboot: int = 1000,
    alpha: float = 0.05,
) -> tuple[float, float]:
    """
    Calculate the closed-form confidence interval for PRB. Unlike COD and PRB,
    this does not use bootstrapping.

    See also:
        :func:`boot_ci`
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
    prb_ci = prb_model.conf_int(alpha=alpha)[0].tolist()

    return prb_ci[0], prb_ci[1]
