# Import necessary libraries
import pandas as pd
from pandas.api.types import is_numeric_dtype
from .formulas import cod
from .formulas import prd
from .utils import check_inputs

# Calculate bootstrapped confidence intervals
def boot_ci(fun, *args, nboot = 100, alpha = 0.05):

    # Input checking and error handling
    check_inputs(args)

    num_args = len(args)
    args = pd.DataFrame(args).T
    n = len(args)

    # Check that the input function returns a numeric vector
    out = fun(args.iloc[:, 0]) if num_args < 2 else fun(args.iloc[:, 0], args.iloc[:, 1])
    if is_numeric_dtype(out) == False:
        raise Exception("Input function outputs non-numeric datatype.")

    ests = []

    # Take a random sample of input, with the same number of rows as input, with replacement.
    for i in list(range(1, nboot)):
        sample = args.sample(n = n, replace = True)
        if fun.__name__ == 'cod' or num_args == 1:
            ests.append(fun(sample.iloc[:, 0]))
        elif fun.__name__ in ['prd']:
            ests.append(fun(sample.iloc[:, 0], sample.iloc[:, 1]))
        else:
            raise Exception("Input function should be 1 dimensional or prd.")

    ests = pd.Series(ests)

    ci = [ests.quantile(alpha / 2), ests.quantile(1 - alpha / 2)]

    return ci

# Formula specific bootstrapping functions
def cod_ci(ratio, nboot = 100, alpha = 0.05):

    return boot_ci(cod, ratio, nboot = nboot, alpha = alpha)

def prd_ci(fmv, sale_price, nboot = 100, alpha = 0.05):

    return boot_ci(prd, fmv, sale_price, nboot = nboot, alpha = alpha)