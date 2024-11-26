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

    def test_iaao_metrics(self, IAAO_sample):
        """
        Test that COD, PRB, and PRD for the IAAO_sample return expected values.
        """
        estimates, sale_prices = IAAO_sample

        # Calculate COD
        cod = round(ap.cod(estimates, sale_prices), 1)

        # Calculate PRB
        prb = round(ap.prb(estimates, sale_prices), 3)

        # Calculate PRD
        prd = round(ap.prd(estimates, sale_prices), 2)

        assert cod == 14.5, f"Expected COD to be 14.5, but got {cod}"
        assert prb == 0.001, f"Expected PRB to be .001, but got {prb}"
        assert prd == 0.98, f"Expected PRD to be 0.98, but got {prd}"

    def test_mki(self, quintos_data):
        """
        Test that MKI for the quintos_sample returns the expected value.
        """
        estimates, sale_prices = quintos_data

        # Calculate MKI
        mki = round(ap.mki(estimates, sale_prices), 2)
        ki = round(ap.ki(estimates, sale_prices), 2)

        assert mki == 0.79, f"Expected MKI to be 0.79, but got {mki}"
        assert ki == -0.06, f"Expected KI to be -0.06, but got {ki}"

    def test_metric_value_is_correct(self, metric, metric_val):
        expected = {
            "cod": 17.81456901196891,
            "prd": 1.0484192615223522,
            "prb": 0.0009470721642262903,
            "mki": 0.794,
            "ki": -0.06,
        }
        assert pt.approx(metric_val, rel=0.02) == expected[metric]

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
            pt.skip("Skipping test for 'ki' metric (ki_met does not exist)")
        expected = {
            "cod": False,
            "prd": False,
            "prb": True,
            "mki": False,
        }
        assert getattr(ap, f"{metric}_met")(metric_val) == expected[metric]
