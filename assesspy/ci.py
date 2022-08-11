# Import necessary libraries
import pandas as pd
from pandas.api.types import is_numeric_dtype
from .formulas import cod
from .formulas import prd
from .utils import check_inputs


def boot_ci(fun, *args, nboot=100, alpha=0.05):

    """
    Calculate the non-parametric bootstrap confidence interval
    for a given numeric input and a chosen function.

    Parameters
    ----------
    fun : function
        Function to bootstrap. Must return a single value.
    args* : numeric
        Arguments passed on to `fun`.
    nboot : int
        Default 100. Number of iterations to use to estimate
        the output statistic confidence interval.
    alpha : float
        Default 0.05. Numeric value indicating the confidence
        interval to return. 0.05 will return the 95\% confidence interval.

    Returns
    -------
    list[float]
        A two-long list of floats containing the bootstrapped confidence
        interval of the input vector(s).

    Examples
    --------
    Calculate PRD confidence interval

    boot_ci(
        assesspy.prd,
        assessed = assesspy.ratios_sample().assessed,
        sale_price = assesspy.ratios_sample().sale_price,
        nboot = 100
        )

    """

    check_inputs(args)  # Input checking and error handling

    num_args = len(args)
    args = pd.DataFrame(args).T
    n = len(args)

    # Check that the input function returns a numeric vector
    out = fun(args.iloc[:, 0]) if num_args < 2 else fun(
        args.iloc[:, 0], args.iloc[:, 1]
        )
    if not is_numeric_dtype(out):
        raise Exception("Input function outputs non-numeric datatype.")

    ests = []

    # Take a random sample of input, with the same number of rows as input,
    # with replacement.
    for i in list(range(1, nboot)):
        sample = args.sample(n=n, replace=True)
        if fun.__name__ == 'cod' or num_args == 1:
            ests.append(fun(sample.iloc[:, 0]))
        elif fun.__name__ in ['prd']:
            ests.append(fun(sample.iloc[:, 0], sample.iloc[:, 1]))
        else:
            raise Exception(
                "Input function should require 1 argument or be assesspy.prd."
                )

    ests = pd.Series(ests)

    ci = [ests.quantile(alpha / 2), ests.quantile(1 - alpha / 2)]

    return ci


# Formula specific bootstrapping functions
def cod_ci(ratio, nboot=100, alpha=0.05):

    return boot_ci(cod, ratio, nboot=nboot, alpha=alpha)


def prd_ci(fmv, sale_price, nboot=100, alpha=0.05):

    return boot_ci(prd, fmv, sale_price, nboot=nboot, alpha=alpha)
