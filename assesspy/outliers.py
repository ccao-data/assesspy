# Import necessary libraries
from pandas.api.types import is_numeric_dtype
import numbers
import numpy as np
from scipy import stats
import warnings
from .utils import check_inputs

# Outlier functions
def quantile_outlier(x, probs = [0.05, 0.95]):

    check_inputs(x)

    # Determine valid range of the data
    range = [
        np.quantile(a = x, q = probs[0]),
        np.quantile(a = x, q = probs[1])
    ]

    # Determine which input values are in range
    out = (x < range[0]) | (x > range[1])

    return out

def iqr_outlier(x, mult = 3):

    check_inputs(x)

    # Check that inputs are well-formed numeric vector
    if isinstance(mult, numbers.Number) & mult > 0:

        # Calculate quartiles and mult*IQR
        quartiles = [
            np.quantile(a = x, q = 0.25),
            np.quantile(a = x, q = 0.75)
            ]

        iqr_mult = mult * stats.iqr(x)

        # Find values that are outliers
        out = (x < (quartiles[0] - iqr_mult)) | (x > (quartiles[1] + iqr_mult))

        # Warn if IQR trimmed values are within 95% CI. This indicates potentially
        # non-normal/narrow distribution of data
        if any(out & quantile_outlier(x) == False):

            warnings.warn(
            """Some values flagged as outliers despite being within 95% CI.
            Check for narrow or skewed distribution."""
            )

        return out

def is_outlier(x, method = 'iqr', probs = [0.05, 0.95]):

    out = {
            'iqr': iqr_outlier(x),
            'quantile': quantile_outlier(x, probs)
        }.get(method)

    # Warn about removing data from small samples, as it can severely distort
    # ratio study outcomes
    if any(out) & (len(out) < 30):

       warnings.warn(
            """Values flagged as outliers despite small sample size (N < 30).
            Use caution when removing values from a small sample."""
            )

    return out