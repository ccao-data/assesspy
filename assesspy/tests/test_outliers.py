import numpy as np
import pandas as pd
import pytest as pt

import assesspy as ap


class TestOutliers:
    @pt.fixture(params=["normal", "outlier", "narrow", "ccao", "quintos"])
    def distribution(self, request, ccao_data, quintos_data):
        return request.param, {
            "normal": np.random.normal(size=100).tolist(),
            "outlier": np.append(
                np.random.normal(size=100), [3, 4, 5, 6, 7]
            ).tolist(),
            "narrow": np.append(
                np.append(np.random.uniform(size=20), np.repeat(1, 100)),
                [5, 6, 7],
            ).tolist(),
            "ccao": ccao_data[0] / ccao_data[1],
            "quintos": quintos_data[0] / quintos_data[1],
        }[request.param]

    @pt.fixture(params=["iqr", "quantile"])
    def method(self, request):
        return request.param

    def test_is_outlier_output_is_boolean_array(self, request, distribution, method):
        dist_name, dist_data = distribution
        assert isinstance(ap.is_outlier(dist_data, method), pd.Series)
        assert ap.is_outlier(dist_data, method).dtype == np.bool_

    def test_is_outlier_has_expected_outlier_counts(
        self,
        distribution,
        method,
    ):
        dist_name, dist_data = distribution
        expected = {
            "normal": {"iqr": 0, "quantile": 10},
            "outlier": {"iqr": 2, "quantile": 12},
            "narrow": {"iqr": 23, "quantile": 10},
            "ccao": {"iqr": 28, "quantile": 98},
            "quintos": {"iqr": 0, "quantile": 4},
        }
        assert (
            ap.is_outlier(dist_data, method).sum()
            == expected[dist_name][method]
        )

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
            lambda x: np.append(x, float("Inf")),
            lambda x: np.append(x, float("NaN")),
        ],
    )
    def test_is_outlier_raises_on_invalid_values(
        self, input_data, distribution, method
    ):
        with pt.raises(Exception):
            dist_name, dist_data = distribution
            ap.is_outlier(input_data(dist_data), method)

    def test_is_outlier_warns_on_narrow_distribution(self, request, distribution):
        dist_name, dist_data = distribution
        if dist_name == "narrow":
            with pt.warns(UserWarning):
                ap.is_outlier(dist_data, "iqr")
        else:
            ap.is_outlier(dist_data, "iqr")

    def test_is_outlier_warns_on_small_sample(self):
        with pt.warns(UserWarning):
            ap.is_outlier(np.random.normal(size=20).tolist(), "quantile")
