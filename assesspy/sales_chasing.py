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

    if method not in ('both', 'cdf', 'dist'):
        raise Exception('Unrecognized method.')

    if len(ratio) < 30:
        warnings.warn(
            """Sales chasing detection can be misleading when applied to small samples (N < 30).
            Increase N or use a different statistical test."""
            )

        out = None

    else:
        out = {
            'cdf': detect_chasing_cdf(ratio),
            'dist': detect_chasing_dist(ratio),
            'both': (detect_chasing_cdf(ratio) & detect_chasing_dist(ratio))
        }.get(method)

    return out
