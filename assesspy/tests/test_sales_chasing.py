# Import necessary libraries
# Import necessary libraries
import numpy as np
import pandas as pd
import pytest as pt

import assesspy

# Create test vectors of data with certain distributions
np.random.seed(13378)

# Load the ratios sample dataset for testing
ratios_sample = assesspy.ratios_sample()

# Extract the components of the dataframe as vectors
sample_ratios = ratios_sample.ratio
normal_ratios = np.random.normal(1, 0.15, 100)
chased_ratios = np.append(np.random.normal(1, 0.15, 900), [1] * 100)

##### TEST CHASING DETECTION ##### # noqa

# Run detection
sample_out = assesspy.detect_chasing(sample_ratios)
normal_out = assesspy.detect_chasing(normal_ratios)
chased_out = assesspy.detect_chasing(chased_ratios)


class TestCHASE:
    def test_method(self):
        with pt.raises(Exception):
            assesspy.detect_chasing(sample_ratios, method="hug")

    def test_output_type(self):  # Output is logical
        assert type(sample_out) is np.bool_

    def test_output_value(self):
        assert not sample_out
        assert not normal_out
        assert chased_out

    def test_bad_input(self):  # Bad input data stops execution
        with pt.raises(Exception):
            assesspy.detect_chasing([1] * 29 + [0])

        with pt.raises(Exception):
            assesspy.detect_chasing(10)

        with pt.raises(Exception):
            assesspy.detect_chasing(np.append(sample_ratios, float("Inf")))

        with pt.raises(Exception):
            assesspy.detect_chasing(pd.DataFrame(sample_ratios))

        with pt.raises(Exception):
            assesspy.detect_chasing(np.append(sample_ratios, float("NaN")))

        with pt.raises(Exception):
            assesspy.detect_chasing([1] * 29 + ["1"])

    def test_warnings(self):  # Small sample throughs a warning
        with pt.warns(UserWarning):
            assesspy.detect_chasing(np.random.normal(size=29))
