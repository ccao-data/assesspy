# Import necessary libraries
import assesspy
import numpy as np
import pandas as pd
import pytest as pt

# Create test vectors of data with certain distributions
np.random.seed(13378)

# Normal distribution, no outliers
test_dist1 = np.random.normal(size=100)

# Normal distribution, some outliers
test_dist2 = np.append(np.random.normal(size=100), [3, 4, 5, 6, 7])

# Non-normal, super narrow distribution
test_dist3 = np.append(
    np.append(
        np.random.uniform(size=20), np.repeat(1, 50)
        ), [5, 6, 7]
        )

# Create outputs for all distributions
dist1_iqr_out = assesspy.is_outlier(test_dist1, method="iqr")
dist1_qnt_out = assesspy.is_outlier(test_dist1, method="quantile")
dist2_iqr_out = assesspy.is_outlier(test_dist2, method="iqr")
dist2_qnt_out = assesspy.is_outlier(test_dist2, method="quantile")

##### TEST OUTLIER ##### # noqa


class TestOUTTIES:

    def test_output_type(self):  # Output is logical array

        assert type(dist1_iqr_out[0]) is np.bool_
        assert type(dist1_iqr_out) is np.ndarray

        assert type(dist1_qnt_out[0]) is np.bool_
        assert type(dist1_qnt_out) is np.ndarray

    def test_output_value(self):

        assert sum(dist1_iqr_out) == 0
        assert sum(dist1_qnt_out) == 10
        assert sum(dist2_iqr_out) == 3
        assert sum(dist2_qnt_out) == 12

    def test_bad_input(self):  # Bad input data stops execution

        with pt.raises(Exception):
            assesspy.is_outlier([1] * 29 + [0])

        with pt.raises(Exception):
            assesspy.is_outlier(10)

        with pt.raises(Exception):
            assesspy.is_outlier(
                np.append(test_dist1, float('Inf'))
                )

        with pt.raises(Exception):
            assesspy.is_outlier(pd.DataFrame(test_dist1))

        with pt.raises(Exception):
            assesspy.is_outlier(
                np.append(test_dist1, float('NaN'))
                )

        with pt.raises(Exception):
            assesspy.is_outlier([1] * 29 + ['1'])

    def test_warnings(self):

        with pt.warns(UserWarning):
            assesspy.is_outlier(test_dist3, method="iqr")

        with pt.warns(UserWarning):
            assesspy.is_outlier(np.random.normal(size=20), method="quantile")
