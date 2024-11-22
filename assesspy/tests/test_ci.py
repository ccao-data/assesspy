import numpy as np
import pytest as pt

import assesspy as ap


class TestCI:
    @pt.fixture(params=["cod", "prd", "prb"])
    def metric(self, request):
        return request.param

    @pt.fixture(params=[0.80, 0.90, 0.95])
    def alpha(self, request):
        return request.param

    def test_metric_ci_output_with_alpha(self, metric, alpha, ccao_data):
        np.random.seed(42)
        expected = {
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
        ci_l, ci_u = getattr(ap, f"{metric}_ci")(*ccao_data, nboot=200, alpha=alpha)
        assert pt.approx(ci_l, rel=0.01) == expected[metric][alpha][0]
        assert pt.approx(ci_u, rel=0.01) == expected[metric][alpha][1]

    def test_metric_ci_raises_on_bad_input(self, metric, bad_input):
        with pt.raises(Exception):
            getattr(ap, f"{metric}_ci")(*bad_input, nboot=200)

    def test_metric_ci_succeeds_on_good_input(self, metric, good_input):
        try:
            result = getattr(ap, f"{metric}_ci")(*good_input, nboot=200)
            assert isinstance(result, tuple)
        except Exception as e:
            pt.fail(f"Unexpected exception {e}")
