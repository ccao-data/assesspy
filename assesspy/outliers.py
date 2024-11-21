import warnings

import numpy as np
import pandas as pd
from scipy import stats

from .utils import check_inputs


def _quantile_outlier(
    x: list[int] | list[float] | pd.Series,
    probs: tuple[float, float] = (0.05, 0.95),
) -> pd.Series[bool]:
    """
    Quantile method for identifying outliers. This simply identifies data
    within the percentiles specified in the ``probs`` parameter.
    """
    check_inputs(x)
    if not isinstance(x, pd.Series):
        x = pd.Series(x)

    # Determine which input values are in the valid quantile range
    valid_range = [x.quantile(q=probs[0]), x.quantile(q=probs[1])]
    out = (x < valid_range[0]) | (x > valid_range[1])

    return out


def _iqr_outlier(
    x: list[int] | list[float] | pd.Series,
    mult: int = 3
) -> pd.Series[bool]:
    """
    IQR method for identifying outliers as specified in Appendix B.1
    of the IAAO Standard on Ratio Studies.
    """
    check_inputs(x)
    if not isinstance(x, pd.Series):
        x = pd.Series(x)

    # Calculate quartiles and mult*IQR
    quartiles = [x.quantile(q=0.25), x.quantile(q=0.75)]
    iqr_mult = mult * stats.iqr(x)
    out = (x < (quartiles[0] - iqr_mult)) | (x > (quartiles[1] + iqr_mult))

    # Warn if IQR trimmed values are also within 95% CI. This indicates
    # potentially non-normal/narrow distribution of data
    if any(out & (not _quantile_outlier(x))):
        warnings.warn(
            "Some values flagged as outliers despite being within 95% CI."
            "Check for narrow or skewed distribution."
        )

    return out


def is_outlier(x, method="iqr", probs=[0.05, 0.95]):
    """
    Detect outliers in a numeric vector using standard methods.

    Certain assessment performance statistics are sensitive to extreme
    outliers. As such, it is often necessary to remove outliers before
    performing a sales ratio study.

    Standard method is to remove outliers that are 3 * IQR. Warnings are thrown
    when sample size is extremely small or when the IQR is extremely narrow. See
    IAAO Standard on Ratio Studies Appendix B. Outlier Trimming Guidelines for
    more information.

    :param x:
        A numeric vector. Must be longer than 2 and not contain
        ``Inf`` or ``NaN``.
    :param method:
        Default "iqr". String indicating outlier detection method.
        Options are ``iqr`` or ``quantile``.
    :param probs:
        Upper and lower percentiles denoting outlier boundaries.
    :type x: numeric
    :type method: str
    :type probs: list[numeric]

    :return:
        A logical vector this same length as ``x`` indicating whether or
        not each value of ``x`` is an outlier.

    :rtype: list[bool]

    :Example:

    .. code-block:: python

        # Detect outliers:
        import assesspy as ap

        ap.is_outlier(ap.ratios_sample().ratio)
    """

    out = {
        "iqr": _iqr_outlier(x),
        "quantile": _quantile_outlier(x, probs),
    }.get(method)

    # Warn about removing data from small samples, as it can severely distort
    # ratio study outcomes
    if any(out) & (len(out) < 30):
        warnings.warn(
            """Values flagged as outliers despite small sample size (N < 30).
            Use caution when removing values from a small sample."""
        )

    return out
