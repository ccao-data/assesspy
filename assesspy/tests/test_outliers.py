import numpy as np
import pandas as pd
import pytest as pt

import assesspy as ap


class TestOutlierDetection:
    @pt.fixture(autouse=True)
    def set_seed(self):
        np.random.seed(42)

    @pt.fixture
    def normal_dist(self):
        return np.random.normal(size=100).tolist()

    @pt.fixture
    def outlier_dist(self):
        return np.append(np.random.normal(size=100), [3, 4, 5, 6, 7]).tolist()

    @pt.fixture
    def narrow_dist(self):
        return np.append(
            np.append(np.random.uniform(size=20), np.repeat(1, 50)), [5, 6, 7]
        ).tolist()

    @pt.fixture(autouse=True)
    def setup_dists(self, normal_dist, outlier_dist, narrow_dist):
        self.normal_iqr = ap.is_outlier(normal_dist, method="iqr")
        self.normal_quantile = ap.is_outlier(normal_dist, method="quantile")
        self.outlier_iqr = ap.is_outlier(outlier_dist, method="iqr")
        self.outlier_quantile = ap.is_outlier(outlier_dist, method="quantile")

    @pt.fixture(autouse=True)
    def setup_data(self, ccao_data, quintos_data):
        self.ccao_iqr = ap.is_outlier(ccao_data[0], method="iqr")
        self.ccao_quantile = ap.is_outlier(ccao_data[0], method="quantile")
        self.quintos_iqr = ap.is_outlier(quintos_data[0], method="iqr")
        self.quintos_quantile = ap.is_outlier(quintos_data[0], method="quantile")

    def test_is_outlier_output_is_boolean_array(self):
        assert isinstance(self.normal_iqr, pd.Series)
        assert self.normal_iqr.dtype == np.bool_
        assert isinstance(self.normal_quantile, pd.Series)
        assert self.normal_quantile.dtype == np.bool_

    @pt.mark.parametrize(
        "result,expected",
        [
            ("normal_iqr", 0),
            ("normal_quantile", 10),
            ("outlier_iqr", 2),
            ("outlier_quantile", 12),
            ("ccao_iqr", 4),
            ("ccao_quantile", 98),
            ("quintos_iqr", 0),
            ("quintos_quantile", 4),
        ],
    )
    def test_is_outlier_has_outlier_counts(self, result, expected):
        assert sum(getattr(self, result)) == expected

    @pt.mark.parametrize(
        "bad_input",
        [
            10,
            pd.DataFrame([1, 2, 3]),
            [1] * 29 + ["1"],
        ],
    )
    def test_is_outlier_raises_on_bad_input(self, bad_input):
        with pt.raises(Exception):
            ap.is_outlier(bad_input)

    @pt.mark.parametrize(
        "input_data",
        [
            lambda normal_dist: np.append(normal_dist, float("Inf")),
            lambda normal_dist: np.append(normal_dist, float("NaN")),
        ],
    )
    def test_is_outlier_raises_on_invalid_values(self, input_data, normal_dist):
        with pt.raises(Exception):
            ap.is_outlier(input_data(normal_dist))

    def test_is_outlier_warns_on_narrow_distribution(self, narrow_dist):
        with pt.warns(UserWarning):
            ap.is_outlier(narrow_dist, method="iqr")

    def test_is_outlier_warns_on_small_sample(self):
        with pt.warns(UserWarning):
            ap.is_outlier(np.random.normal(size=20).tolist(), method="quantile")
