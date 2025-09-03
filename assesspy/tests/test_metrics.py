import numpy as np
import pytest as pt

import assesspy as ap


class TestMetrics:
    @pt.fixture(params=["cod", "prd", "prb", "mki", "ki"])
    def metric(self, request):
        return request.param

    @pt.fixture
    def metric_val(self, metric, ccao_data, quintos_data):
        if metric in ["mki", "ki"]:
            return getattr(ap, metric)(*quintos_data)
        return getattr(ap, metric)(*ccao_data)

    def test_metric_value_is_correct_ccao(self, metric, metric_val):
        expected = {
            "cod": 17.81456901196891,
            "prd": 1.0484192615223522,
            "prb": 0.0024757,
            "mki": 0.794,
            "ki": -0.062,
        }
        assert pt.approx(metric_val, rel=0.01) == expected[metric]

    def test_metric_value_is_correct_iaao(
        self, metric, iaao_data_name, iaao_data
    ):
        if metric in ["mki", "ki"]:
            return None
        else:
            result = getattr(ap, metric)(*iaao_data)
            expected = {
                "1_1": {
                    "cod": 29.8,
                    "prd": 0.98,
                    "prb": 0.232,
                },
                "1_4": {
                    "cod": 14.5,
                    "prd": 0.98,
                    "prb": 0.135,
                },
                "d_1": {
                    "cod": 7.5,
                    "prd": 1.027,
                    "prb": -0.120,
                },
                "d_2": {
                    "cod": 7.8,
                    "prd": 1.056,
                    "prb": -0.011,
                },
            }
            assert (
                pt.approx(result, rel=0.02) == expected[iaao_data_name][metric]
            )

    def test_metric_has_numeric_output(self, metric_val):
        assert type(metric_val) is float

    def test_metric_raises_on_bad_input(self, metric, bad_input):
        with pt.raises(Exception):
            getattr(ap, metric)(*bad_input)

    def test_metric_succeeds_on_good_input(self, metric, good_input):
        result = getattr(ap, metric)(*good_input)
        assert type(result) is float
        assert result != float("NaN")

    def test_metric_met_function_thresholds(self, metric, metric_val):
        if metric == "ki":
            return None
        expected = {
            "cod": False,
            "prd": False,
            "prb": True,
            "mki": False,
        }
        assert getattr(ap, f"{metric}_met")(metric_val) == expected[metric]


@pt.mark.parametrize("metric", ["mki", "ki"])
def test_mki_matches_based_on_tied_sales(metric):
    """
    For the quintos dataset, MKI/KI should be identical based
    on the ordering of estimates.
    """
    sample = ap.quintos_sample()
    estimate_cols = [
        c
        for c in ["estimate", "estimate1", "estimate2"]
        if c in sample.columns
    ]

    sales = sample["sale_price"]

    # Use the first present estimate column as the reference
    ref_col = estimate_cols[0]
    ref_val = getattr(ap, metric)(sample[ref_col], sales)

    for col in estimate_cols[1:]:
        val = getattr(ap, metric)(sample[col], sales)
        assert val == ref_val, (
            f"{metric.upper()} differs between {ref_col} and {col}: "
            f"{ref_val} vs {val}"
        )
