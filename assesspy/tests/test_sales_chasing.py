import numpy as np
import pandas as pd
import pytest as pt

import assesspy as ap


class TestSalesChasing:
    @pt.fixture
    def sample_dist(self, ccao_data):
        estimate, sale_price = ccao_data
        ratio = estimate / sale_price
        return ratio

    @pt.fixture(params=["normal", "chased", "sample"])
    def distribution_name(self, request):
        return request.param

    @pt.fixture
    def distribution(self, distribution_name, ccao_data, sample_dist):
        return {
            "normal": np.random.normal(1, size=1000).tolist(),
            "chased": np.append(
                np.random.normal(1, 0.15, 900), [1] * 100
            ).tolist(),
            "sample": sample_dist,
        }[distribution_name]

    @pt.fixture(params=["cdf", "dist", "both"])
    def method(self, request):
        return request.param

    def test_is_sales_chased_output_is_boolean(self, distribution, method):
        assert isinstance(ap.is_sales_chased(distribution, method), bool)

    def test_is_sales_chased_has_expected_output(
        self, distribution_name, distribution, method
    ):
        expected = {
            "normal": {"cdf": False, "dist": False, "both": False},
            "chased": {"cdf": True, "dist": True, "both": True},
            "sample": {"cdf": False, "dist": True, "both": False},
        }
        assert (
            ap.is_sales_chased(distribution, method)
            == expected[distribution_name][method]
        )

    @pt.mark.parametrize(
        "bad_input",
        [10, pd.DataFrame([1, 2, 3]), [1] * 29 + ["1"], None],
    )
    def test_is_sales_chased_raises_on_bad_input(self, bad_input):
        with pt.raises(Exception):
            ap.is_sales_chased(bad_input)

    @pt.mark.parametrize(
        "input_data",
        [
            lambda x: np.append(x, float("Inf")),
            lambda x: np.append(x, float("NaN")),
        ],
    )
    def test_is_sales_chased_raises_on_invalid_values(
        self, input_data, distribution, method
    ):
        with pt.raises(Exception):
            ap.is_outlier(input_data(distribution), method)

    def test_is_sales_chased_raises_on_invalid_method(self, distribution):
        with pt.raises(Exception):
            ap.is_sales_chased(distribution, method="hug")

    def test_is_sales_chased_warns_on_small_sample(self):
        with pt.warns(UserWarning):
            ap.is_sales_chased(np.random.normal(size=29).tolist())

    @pt.mark.parametrize(
        "bounds",
        [(0.0, 0.0), [0.5, 0.4], (2.0, 1.0), (2.0, "1.0"), None, "2.0"],
    )
    def test_is_sales_chased_raises_on_invalid_bounds(self, bounds):
        with pt.raises(Exception):
            ap.is_sales_chased(
                np.random.normal(size=40).tolist(), bounds=bounds
            )

    @pt.mark.parametrize(
        "gap",
        [0, 1, -1, 2, float("NaN"), float("Inf"), None],
    )
    def test_is_sales_chased_raises_on_invalid_gap(self, gap):
        with pt.raises(Exception):
            ap.is_sales_chased(np.random.normal(size=40).tolist(), gap=gap)
