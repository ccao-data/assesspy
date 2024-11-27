import pytest as pt

import assesspy as ap


class TestCI:
    @pt.fixture(params=["cod", "prd", "prb"])
    def metric(self, request):
        return request.param

    @pt.fixture(params=[0.50, 0.20, 0.10, 0.05])
    def alpha(self, request):
        return request.param

    def test_metric_ci_output_with_alpha(self, metric, alpha, ccao_data):
        expected = {
            "cod": {
                0.50: (17.30233, 18.27170),
                0.20: (16.83710, 18.79953),
                0.10: (16.61336, 18.97916),
                0.05: (16.49595, 19.19573),
            },
            "prd": {
                0.50: (1.043290, 1.053368),
                0.20: (1.038444, 1.058439),
                0.10: (1.036563, 1.061334),
                0.05: (1.034447, 1.062625),
            },
            "prb": {
                0.50: (-0.00320422, 0.00815580),
                0.20: (-0.00831969, 0.01327127),
                0.10: (-0.01138384, 0.01633542),
                0.05: (-0.01404379, 0.01899536),
            },
        }
        ci_l, ci_u = getattr(ap, f"{metric}_ci")(
            *ccao_data, nboot=500, alpha=alpha
        )
        assert pt.approx(ci_l, rel=0.01) == expected[metric][alpha][0]
        assert pt.approx(ci_u, rel=0.01) == expected[metric][alpha][1]

    def test_metric_ci_raises_on_bad_input(self, metric, bad_input):
        with pt.raises(Exception):
            getattr(ap, f"{metric}_ci")(*bad_input, nboot=200)

    def test_metric_ci_succeeds_on_good_input(self, metric, good_input):
        result = getattr(ap, f"{metric}_ci")(*good_input, nboot=200)
        assert isinstance(result, tuple)

    @pt.mark.parametrize("metric", ["cod", "prd"])
    @pt.mark.parametrize("nboot", [0, -10])
    def test_metric_ci_raises_on_bad_nboot(self, metric, ccao_data, nboot):
        with pt.raises(Exception):
            getattr(ap, f"{metric}_ci")(*ccao_data, nboot=nboot)
