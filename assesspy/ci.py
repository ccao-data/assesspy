# Import necessary libraries
import pandas as pd
from pandas.api.types import is_numeric_dtype
from .formulas import cod
from .formulas import prd
from .utils import check_inputs


def boot_ci(fun, nboot=100, alpha=0.05, **kwargs):

    """
    Calculate the non-parametric bootstrap confidence interval
    for a given numeric input and a chosen function.

    Parameters
    ----------
    fun : function
        Function to bootstrap. Must return a single value.
    nboot : int
        Default 100. Number of iterations to use to estimate
        the output statistic confidence interval.
    alpha : float
        Default 0.05. Numeric value indicating the confidence
        interval to return. 0.05 will return the 95\% confidence interval.
    kwargs : numeric
        Arguments passed on to `fun`.

    Returns
    -------
    list[float]
        A two-long list of floats containing the bootstrapped confidence
        interval of the input vector(s).

    Examples
    --------
    ```
    # Detect outliers:
    import assesspy as ap

    ap.is_outlier(asspy.ratios_sample().ratio)
    ```

    """

    # Make sure prd is passed arguments in correct order
    if fun.__name__ == 'prd' and set(['assessed', 'sale_price']).issubset(kwargs.keys()):
        kwargs = (kwargs["assessed"], kwargs["sale_price"])
    elif fun.__name__ == 'prd' and not set(['assessed', 'sale_price']).issubset(kwargs.keys()):
        raise Exception(
                "PRD function expects argurments 'assessed' and 'sale_price'."
                )
    else:
        kwargs = tuple(kwargs.values())

    check_inputs(kwargs)  # Input checking and error handling

    num_kwargs = len(kwargs)
    kwargs = pd.DataFrame(kwargs).T
    n = len(kwargs)

    # Check that the input function returns a numeric vector
    out = fun(kwargs.iloc[:, 0]) if num_kwargs < 2 else fun(
        kwargs.iloc[:, 0], kwargs.iloc[:, 1]
        )
    if not is_numeric_dtype(out):
        raise Exception("Input function outputs non-numeric datatype.")

    ests = []

    # Take a random sample of input, with the same number of rows as input,
    # with replacement.
    for i in list(range(1, nboot)):
        sample = kwargs.sample(n=n, replace=True)
        if fun.__name__ == 'cod' or num_kwargs == 1:
            ests.append(fun(sample.iloc[:, 0]))
        elif fun.__name__ == 'prd':
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


def prd_ci(assessed, sale_price, nboot=100, alpha=0.05):

    return boot_ci(prd, assessed, sale_price, nboot=nboot, alpha=alpha)
