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
            "ki": -0.06,
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

def test_quintos_mki_ki_match():
    """MKI and KI results should be identical regardless of estimate1/2/3."""
    sample = ap.quintos_sample()
    estimates = [sample["estimate1"], sample["estimate2"], sample["estimate3"]]
    sales = sample["sale_price"]

    # Compute MKI + KI for each estimate column
    results = []
    for est in estimates:
        mki_val = ap.mki(est, sales)
        ki_val = ap.ki(est, sales)
        results.append((mki_val, ki_val))

    # Use the first as reference and check all others match
    ref_mki, ref_ki = results[0]
    for i, (mki_val, ki_val) in enumerate(results[1:], start=2):
        assert mki_val == ref_mki, f"MKI differs for estimate{i}"
        assert ki_val == ref_ki, f"KI differs for estimate{i}"
