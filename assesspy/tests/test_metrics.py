import pandas as pd
import pytest as pt

import assesspy as ap

ratios_sample = ap.ratios_sample()
estimate = ratios_sample.estimate
sale_price = ratios_sample.sale_price


class TestMetrics:
    @pt.fixture(params=["cod", "prd", "prb"])
    def metric(self, request):
        return request.param

    @pt.fixture
    def metric_val(self, metric):
        return getattr(ap, metric)(estimate, sale_price)

    def test_metric(self, metric, metric_val):
        expected_values = {
            "cod": 17.81456901196891,
            "prd": 1.0484192615223522,
            "prb": 0.0009470721642262903,
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
        expected_values = {
            "cod": False,
            "prd": False,
            "prb": True,
        }
        assert (
            getattr(ap, f"{metric}_met")(metric_val) == expected_values[metric]
        )


with open("assesspy/data/mki_ki.csv", "r") as input_csvfile:
    # Create a list to store the extracted columns
    gini_data_sale = []
    gini_data_assessed = []

    # Iterate through each line in the input CSV
    for line in input_csvfile:
        columns = line.strip().split(",")

        first_column = columns[0].split('"')[1]
        second_column = columns[1]

        gini_data_sale.append(first_column)
        gini_data_assessed.append(second_column)

gini_data_assessed = [
    int(value.replace('"', "")) for value in gini_data_assessed
]
gini_data_sale = [int(value.replace('"', "")) for value in gini_data_sale]

mki_out = ap.mki(gini_data_assessed, gini_data_sale)


class Test_MKI:
    def test_mki(self):  # Output equal to expected
        npt.assert_allclose(mki_out, 0.794, rtol=0.02)

    def test_numeric_output(self):  # Output is numeric
        assert type(mki_out) is float

        with pt.raises(Exception):
            ap.mki([1, 1, 1], [1, 1])

        with pt.raises(Exception):
            ap.mki(10, 10)

        with pt.raises(Exception):
            ap.mki(
                pd.concat([gini_data_assessed, pd.Series(float("Inf"))]),
                pd.concat([gini_data_sale, pd.Series(1.0)]),
            )

        with pt.raises(Exception):
            ap.mki(pd.DataFrame(ratio))

        with pt.raises(Exception):
            ap.mki(
                pd.concat([gini_data_assessed, pd.Series(float("NaN"))]),
                pd.concat([gini_data_sale, pd.Series(1.0)]),
            )

        with pt.raises(Exception):
            ap.mki([1] * 30, [1] * 29 + ["1"])

    def test_round(self):  # Rounding must be int
        with pt.raises(Exception):
            ap.mki(gini_data_assessed, sale_price, "z")

        with pt.raises(Exception):
            ap.mki(gini_data_assessed, sale_price, 1.1)

    def test_mki_met(self):  # Standard met function
        assert not ap.mki_met(mki_out)


ki_out = ap.ki(gini_data_assessed, gini_data_sale)


class Test_KI:
    def test_ki(self):  # Output equal to expected
        npt.assert_allclose(ki_out, -0.06, rtol=0.02)

    def test_numeric_output(self):  # Output is numeric
        assert type(ki_out) is float

        with pt.raises(Exception):
            ap.ki([1, 1, 1], [1, 1])

        with pt.raises(Exception):
            ap.ki(10, 10)

        with pt.raises(Exception):
            ap.ki(
                pd.concat([gini_data_assessed, pd.Series(float("Inf"))]),
                pd.concat([gini_data_sale, pd.Series(1.0)]),
            )

        with pt.raises(Exception):
            ap.ki(pd.DataFrame(ratio))

        with pt.raises(Exception):
            ap.ki(
                pd.concat([gini_data_assessed, pd.Series(float("NaN"))]),
                pd.concat([gini_data_sale, pd.Series(1.0)]),
            )

        with pt.raises(Exception):
            ap.ki([1] * 30, [1] * 29 + ["1"])

    def test_round(self):  # Rounding must be int
        with pt.raises(Exception):
            ap.ki(gini_data_assessed, gini_data_sale, "z")

        with pt.raises(Exception):
            ap.ki(gini_data_assessed, gini_data_sale, 1.1)
