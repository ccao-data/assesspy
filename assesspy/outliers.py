import warnings

import pandas as pd

from .utils import check_inputs


def _quantile_outlier(
    x: list[int] | list[float] | pd.Series,
    probs: tuple[float, float] = (0.05, 0.95),
) -> pd.Series:
    """
    Quantile method for identifying outliers. This simply identifies data
    within the percentiles specified in the ``probs`` parameter.
    """
    check_inputs(x, check_gt_zero=False)
    x = pd.Series(x)

    # Determine which input values are in the valid quantile range
    valid_range = [x.quantile(q=probs[0]), x.quantile(q=probs[1])]
    out = (x < valid_range[0]) | (x > valid_range[1])

    return out


def _iqr_outlier(
    x: list[int] | list[float] | pd.Series, mult: float = 3.0
) -> pd.Series:
    """
    IQR method for identifying outliers as specified in Appendix B.1
    of the IAAO Standard on Ratio Studies.
    """
    check_inputs(x, check_gt_zero=False)
    x = pd.Series(x)

    quartiles = [x.quantile(q=0.25), x.quantile(q=0.75)]
    iqr_mult = mult * (quartiles[1] - quartiles[0])
    out = (x < (quartiles[0] - iqr_mult)) | (x > (quartiles[1] + iqr_mult))

    return out


def is_outlier(
    x: list[int] | list[float] | pd.Series,
    method: str = "iqr",
    probs: tuple[float, float] = (0.05, 0.95),
    mult: float = 3.0,
) -> pd.Series:
    """
    Detect outliers in numeric values using standard methods.

    Certain assessment performance statistics are sensitive to extreme
    outliers. As such, it is often necessary to remove outliers before
    performing a sales ratio study.

    The IAAO standard method is to remove outliers that are 3 * IQR. Warnings
    are thrown when sample size is extremely small or when the IQR is extremely
    narrow. See IAAO Standard on Ratio Studies Appendix B. Outlier Trimming
    Guidelines for more information.

    :param x:
        A list or ``pd.Series`` of numeric values, typically sales ratios.
        Must be longer than 2 and cannot contain ``Inf`` or ``NaN`` values.
    :param method:
        Default ``iqr``. String indicating outlier detection method.
        Options are ``iqr`` or ``quantile``.
    :param probs:
        Upper and lower percentiles boundaries for the ``quantile`` method.
    :param mult:
        Default ``3``. Multiple of IQR to use as the outlier detection
        threshold.
    :type x: list[int] | list[float] | pd.Series,
    :type method: str
    :type probs: tuple[float]
    :type mult: float

    :return:
        A boolean ``pd.Series`` the same length as ``x`` indicating whether or
        not each value of ``x`` is an outlier.
    :rtype: pd.Series

    :Example:

    .. code-block:: python

        # Detect outliers:
        import assesspy as ap

        ap.is_outlier(ap.ccao_sample().estimate)
    """
    if method == "iqr":
        out = _iqr_outlier(x, mult)
        iqr_quant = out & ~_quantile_outlier(x)
        if any(iqr_quant):
            warnings.warn(
                f"{iqr_quant.sum()} values flagged as outliers despite being "
                "within 95% CI. Check for narrow or skewed distribution."
            )
    elif method == "quantile":
        out = _quantile_outlier(x, probs)
    else:
        raise ValueError("Method must be either 'iqr' or 'quantile'")

    # Warn about removing data from small samples, as it can severely distort
    # ratio study outcomes
    if any(out) & (out.size < 30):
        warnings.warn(
            f"{out.sum()} flagged as outliers despite small sample size "
            "(N < 30). Use caution when removing values from a small sample."
        )

    return out
