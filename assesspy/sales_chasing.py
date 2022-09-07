# Import necessary libraries
import numpy as np
from statsmodels.distributions.empirical_distribution import ECDF
import warnings
from .utils import check_inputs


# Sales chasing functions
def detect_chasing_cdf(ratio, bounds=[0.98, 1.02], cdf_gap=0.03):
    # CDF gap method for detecting sales chasing.

    # Input checking and error handling
    check_inputs(ratio)

    # Sort the ratios
    sorted_ratio = np.sort(np.array(ratio))

    # Calculate the CDF of the sorted ratios and extract percentile ranking
    cdf = ECDF(sorted_ratio)(sorted_ratio)

    # Calculate the difference between each value and the next value, the
    # largest difference will be the CDF gap
    diffs = np.diff(cdf)

    # Check if the largest difference is greater than the threshold and make
    # sure it's within the specified boundaries
    diff_loc = sorted_ratio[np.argmax(diffs)]
    out = (max(diffs) > cdf_gap) & (
        (diff_loc > bounds[0]) & (diff_loc < bounds[1])
        )

    return out


def detect_chasing_dist(ratio, bounds=[0.98, 1.02]):
    # Distribution comparison method for detecting sales chasing.

    # Input checking and error handling
    check_inputs(ratio)

    ratio = np.array(ratio)

    # Return the percentage of x within the specified range
    def pct_in_range(x, min, max):
        out = np.mean(((x >= min) & (x <= max)))
        return out

    # Calculate the ideal normal distribution using observed values from input
    ideal_dist = np.random.normal(
        np.mean(ratio),
        np.std(ratio),
        10000
        )

    # Determine what percentage of the data would be within the specified
    # bounds in the ideal distribution
    pct_ideal = pct_in_range(ideal_dist, bounds[0], bounds[1])

    # Determine what percentage of the data is actually within the bounds
    pct_actual = pct_in_range(ratio, bounds[0], bounds[1])

    return pct_actual > pct_ideal


def detect_chasing(ratio, method='both'):

    """
    Sales chasing is when a property is selectively reappraised to
    shift its assessed value toward its actual sale price. Sales chasing is
    difficult to detect. This function is NOT a statistical test and does
    not provide the probability of the given result. Rather, it combines two
    novel methods to roughly estimate if sales chasing has occurred.

    The first method (dist) uses the technique outlined in the
    `IAAO Standard on Ratio Studies`_ Appendix E, Section 4. It compares the
    percentage of real data within +-2% of the mean ratio to the percentage
    of data within the same bounds given a constructed normal distribution
    with the same mean and standard deviation. The intuition here is that
    ratios that are sales chased may be more "bunched up" in the center
    of the distribution.

    The second method (cdf) detects discontinuities in the cumulative
    distribution function (CDF) of the input vector. Ratios that are not sales
    chased should have a fairly smooth CDF. Discontinuous jumps in the CDF,
    particularly around 1, may indicate sales chasing. This can usually be seen
    visually as a "flat spot" on the CDF.

    .. _IAAO Standard on Ratio Studies: https://www.iaao.org/media/standards/Standard_on_Ratio_Studies.pdf

    :param ratio:
        A numeric vector of ratios centered around 1, where the
        numerator of the ratio is the estimated fair market value and the
        denominator is the actual sale price.
    :param method:
        Default "both". String indicating sales chasing detection
        method. Options are ``cdf``, ``dist``, or ``both``.
    :type ratio: numeric
    :type method: str

    :return:
        A logical value indicating whether or not the input ratios may
        have been sales chased.
    :rtype: bool

    :Example:

    .. code-block:: python

        import assesspy as ap
        import numpy as np
        from statsmodels.distributions.empirical_distribution import ECDF
        from matplotlib import pyplot

        # Generate fake data with normal vs chased ratios
        normal_ratios = np.random.normal(1, 0.15, 10000)
        chased_ratios = list(np.random.normal(1, 0.15, 900)) + [1] * 100

        # Plot to view discontinuity
        ecdf = ECDF(normal_ratios)
        pyplot.plot(ecdf.x, ecdf.y)
        pyplot.show()
        ap.detect_chasing(normal_ratios)

        ecdf = ECDF(chased_ratios)
        pyplot.plot(ecdf.x, ecdf.y)
        pyplot.show()
        ap.detect_chasing(chased_ratios)
    """

    if method not in ('both', 'cdf', 'dist'):
        raise Exception('Unrecognized method.')

    if len(ratio) < 30:
        warnings.warn(
            """
            Sales chasing detection can be misleading when applied to small
            samples (N < 30). Increase N or use a different statistical test.
            """
            )

        out = None

    else:
        out = {
            'cdf': detect_chasing_cdf(ratio),
            'dist': detect_chasing_dist(ratio),
            'both': (detect_chasing_cdf(ratio) & detect_chasing_dist(ratio))
        }.get(method)

    return out
