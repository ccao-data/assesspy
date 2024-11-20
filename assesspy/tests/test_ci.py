import numpy as np
import pandas as pd
import pytest as pt

import assesspy as ap

# Load random CCAO value sample
ccao_sample = ap.ccao_sample()
estimate = ccao_sample.estimate
sale_price = ccao_sample.sale_price


class TestCI:
    @pt.fixture(params=["cod", "prd", "prb"])
    def metric(self, request):
        return request.param

    @pt.fixture(params=[0.80, 0.90, 0.95])
    def alpha(self, request):
        return request.param

    def test_metric_ci(self, metric, alpha):
        np.random.seed(42)
        expected_values = {
            "cod": {
                0.50: (17.3, 18.0),
                0.80: (17.6, 18.0),
                0.90: (17.7, 18.0),
                0.95: (17.7, 17.9),
            },
            "prd": {
                0.50: (1.03, 1.06),
                0.80: (1.04, 1.06),
                0.90: (1.04, 1.05),
                0.95: (1.04, 1.05),
            },
            "prb": {
                0.50: (0.000823, 0.00107),
                0.80: (0.000823, 0.00107),
                0.90: (0.000885, 0.00100),
                0.95: (0.000916, 0.00097),
            },
        }
        ci_l, ci_u = getattr(ap, f"{metric}_ci")(estimate, sale_price, nboot=200, alpha=alpha)
        assert pt.approx(ci_l, rel=0.01) == expected_values[metric][alpha][0]
        assert pt.approx(ci_u, rel=0.01) == expected_values[metric][alpha][1]

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
            getattr(ap, f"{metric}_ci")(*bad_input, nboot=200)

    @pt.mark.parametrize(
        "good_input",
        [
            ([1e10, 2e10, 3e10], [1e10, 2e10, 3e10]),
            ([1, 2.0, 3], [1.0, 2, 3.0]),
        ],
    )
    def test_good_input(self, metric, good_input):
        try:
            result = getattr(ap, f"{metric}_ci")(*good_input, nboot=200)
            assert isinstance(result, tuple)
        except Exception as e:
            pt.fail(f"Unexpected exception {e}")
