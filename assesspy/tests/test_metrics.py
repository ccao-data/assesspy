import pandas as pd
import pytest as pt

import assesspy as ap

# Load random CCAO value sample
ccao_sample = ap.ccao_sample()
estimate = ccao_sample.estimate
sale_price = ccao_sample.sale_price

# Load MKI / KI data from Quintos paper
gini_data = ap.quintos_sample()
gini_estimate = gini_data.estimate
gini_sale_price = gini_data.sale_price


class TestMetrics:
    @pt.fixture(params=["cod", "prd", "prb", "mki", "ki"])
    def metric(self, request):
        return request.param

    @pt.fixture
    def metric_val(self, metric):
        if metric in ["mki", "ki"]:
            return getattr(ap, metric)(gini_estimate, gini_sale_price)
        return getattr(ap, metric)(estimate, sale_price)

    def test_metric(self, metric, metric_val):
        expected_values = {
            "cod": 17.81456901196891,
            "prd": 1.0484192615223522,
            "prb": 0.0009470721642262903,
            "mki": 0.794,
            "ki": -0.06,
        }
        assert pt.approx(metric_val, rel=0.02) == expected_values[metric]

    def test_numeric_output(self, metric_val):
        assert type(metric_val) is float

    @pt.mark.parametrize(
        "bad_input",
        [
            ([1] * 30, [1] * 29),
            ([0, 0, 0], [0, 0, 0]),
            ([-1, -2, -3], [-1, -2, -3]),
            ([], []),
            ([1], [1]),
            (
                pd.concat([estimate, pd.Series([1.0], dtype="float")]),
                pd.concat(
                    [sale_price, pd.Series([float("Inf")], dtype="float")]
                ),
            ),
            (
                pd.concat([estimate, pd.Series([1.0], dtype="float")]),
                pd.concat(
                    [sale_price, pd.Series([float("NaN")], dtype="float")]
                ),
            ),
        ],
    )
    def test_bad_input(self, metric, bad_input):
        with pt.raises(Exception):
            getattr(ap, metric)(*bad_input)

    @pt.mark.parametrize(
        "good_input",
        [
            ([1e10, 2e10, 3e10], [1e10, 2e10, 3e10]),
            ([1, 2.0, 3], [1.0, 2, 3.0]),
        ],
    )
    def test_good_input(self, metric, good_input):
        try:
            result = getattr(ap, metric)(*good_input)
            assert type(result) is float
        except Exception as e:
            pt.fail(f"Unexpected exception {e}")

    def test_metric_met(self, metric, metric_val):
        if metric == "ki":
            pt.skip("Skipping test for 'ki' metric (ki_met does not exist)")
        expected_values = {
            "cod": False,
            "prd": False,
            "prb": True,
            "mki": False,
        }
        assert (
            getattr(ap, f"{metric}_met")(metric_val) == expected_values[metric]
        )
