# Import necessary libraries
import numpy as np
import pandas as pd
import pytest as pt
from numpy import testing as npt

import assesspy

# Load the ratios sample dataset for testing
ratios_sample = assesspy.ratios_sample()

ratio = ratios_sample.ratio
fmv = ratios_sample.assessed
sale_price = ratios_sample.sale_price

##### TEST COD ##### # noqa

# Calculate COD
cod_out = assesspy.cod(ratios_sample.ratio)


class TestCOD:
    def test_cod(self):  # Output equal to expected
        npt.assert_allclose(cod_out, 17.81456901196891, rtol=0.02)

    def test_numeric_output(self):  # Output is numeric
        assert type(cod_out) is np.float64

    def test_bad_input(self):  # Bad input data stops execution
        with pt.raises(Exception):
            assesspy.cod([1] * 29 + [0])

        with pt.raises(Exception):
            assesspy.cod(10)

        with pt.raises(Exception):
            assesspy.cod(pd.concat([ratio, pd.Series(float("Inf"))]))

        with pt.raises(Exception):
            assesspy.cod(pd.DataFrame(ratio))

        with pt.raises(Exception):
            assesspy.cod(pd.concat([ratio, pd.Series(float("NaN"))]))

        with pt.raises(Exception):
            assesspy.cod([1] * 29 + ["1"])

    def test_cod_met(self):  # Standard met function
        assert not assesspy.cod_met(cod_out)


##### TEST PRD ##### # noqa


# Calculate PRD
prd_out = assesspy.prd(fmv, sale_price)


class TestPRD:
    def test_prd(self):  # Output equal to expected
        npt.assert_allclose(prd_out, 1.0484192615223522, rtol=0.02)

    def test_numeric_output(self):  # Output is numeric
        assert type(prd_out) is np.float64

    def test_bad_input(self):  # Bad input data stops execution
        with pt.raises(Exception):
            assesspy.prd_ci([1] * 30, [1] * 29 + [0])

        with pt.raises(Exception):
            assesspy.prd_ci([1, 1, 1], [1, 1])

        with pt.raises(Exception):
            assesspy.prd(10, 10)

        with pt.raises(Exception):
            assesspy.prd(
                pd.concat([fmv, pd.Series(float("Inf"))]),
                pd.concat([sale_price, pd.Series(1.0)]),
            )

        with pt.raises(Exception):
            assesspy.prd(pd.DataFrame(ratio))

        with pt.raises(Exception):
            assesspy.prd(
                pd.concat([fmv, pd.Series(float("NaN"))]),
                pd.concat([sale_price, pd.Series(1.0)]),
            )

        with pt.raises(Exception):
            assesspy.prd([1] * 30, [1] * 29 + ["1"])

    def test_prd_met(self):  # Standard met function
        assert not assesspy.prd_met(prd_out)


##### TEST PRB ##### # noqa

# Calculate PRB
prb_out = assesspy.prb(fmv, sale_price)["prb"]


class TestPRB:
    def test_prb(self):  # Output equal to expected
        npt.assert_allclose(prb_out, 0.0009470721642262901, rtol=0.02)

    def test_numeric_output(self):  # Output is numeric
        assert type(prb_out) is float

    def test_bad_input(self):  # Bad input data stops execution
        with pt.raises(Exception):
            assesspy.prb_ci([1] * 30, [1] * 29 + [0])

        with pt.raises(Exception):
            assesspy.prb([1, 1, 1], [1, 1])

        with pt.raises(Exception):
            assesspy.prb(10, 10)

        with pt.raises(Exception):
            assesspy.prb(
                pd.concat([fmv, pd.Series(float("Inf"))]),
                pd.concat([sale_price, pd.Series(1.0)]),
            )

        with pt.raises(Exception):
            assesspy.prb(pd.DataFrame(ratio))

        with pt.raises(Exception):
            assesspy.prb(
                pd.concat([fmv, pd.Series(float("NaN"))]),
                pd.concat([sale_price, pd.Series(1.0)]),
            )

        with pt.raises(Exception):
            assesspy.prb([1] * 30, [1] * 29 + ["1"])

    def test_round(self):  # Rounding must be int
        with pt.raises(Exception):
            assesspy.prb(fmv, sale_price, "z")

        with pt.raises(Exception):
            assesspy.prb(fmv, sale_price, 1.1)

    def test_prb_met(self):  # Standard met function
        assert assesspy.prb_met(prb_out)


with open("assesspy/tests/data/mki_ki_data.csv", "r") as input_csvfile:
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

gini_data_assessed = [int(value.replace('"', "")) for value in gini_data_assessed]
gini_data_sale = [int(value.replace('"', "")) for value in gini_data_sale]

mki_out = assesspy.mki(gini_data_assessed, gini_data_sale)


class Test_MKI:
    def test_mki(self):  # Output equal to expected
        npt.assert_allclose(mki_out, 0.794, rtol=0.02)

    def test_numeric_output(self):  # Output is numeric
        assert type(mki_out) is float

        with pt.raises(Exception):
            assesspy.mki([1, 1, 1], [1, 1])

        with pt.raises(Exception):
            assesspy.mki(10, 10)

        with pt.raises(Exception):
            assesspy.mki(
                pd.concat([gini_data_assessed, pd.Series(float("Inf"))]),
                pd.concat([gini_data_sale, pd.Series(1.0)]),
            )

        with pt.raises(Exception):
            assesspy.mki(pd.DataFrame(ratio))

        with pt.raises(Exception):
            assesspy.mki(
                pd.concat([gini_data_assessed, pd.Series(float("NaN"))]),
                pd.concat([gini_data_sale, pd.Series(1.0)]),
            )

        with pt.raises(Exception):
            assesspy.mki([1] * 30, [1] * 29 + ["1"])

    def test_round(self):  # Rounding must be int
        with pt.raises(Exception):
            assesspy.mki(gini_data_assessed, sale_price, "z")

        with pt.raises(Exception):
            assesspy.mki(gini_data_assessed, sale_price, 1.1)

    def test_mki_met(self):  # Standard met function
        assert not assesspy.mki_met(mki_out)


ki_out = assesspy.ki(gini_data_assessed, gini_data_sale)


class Test_KI:
    def test_ki(self):  # Output equal to expected
        npt.assert_allclose(ki_out, -0.06, rtol=0.02)

    def test_numeric_output(self):  # Output is numeric
        assert type(ki_out) is float

        with pt.raises(Exception):
            assesspy.ki([1, 1, 1], [1, 1])

        with pt.raises(Exception):
            assesspy.ki(10, 10)

        with pt.raises(Exception):
            assesspy.ki(
                pd.concat([gini_data_assessed, pd.Series(float("Inf"))]),
                pd.concat([gini_data_sale, pd.Series(1.0)]),
            )

        with pt.raises(Exception):
            assesspy.ki(pd.DataFrame(ratio))

        with pt.raises(Exception):
            assesspy.ki(
                pd.concat([gini_data_assessed, pd.Series(float("NaN"))]),
                pd.concat([gini_data_sale, pd.Series(1.0)]),
            )

        with pt.raises(Exception):
            assesspy.ki([1] * 30, [1] * 29 + ["1"])

    def test_round(self):  # Rounding must be int
        with pt.raises(Exception):
            assesspy.ki(gini_data_assessed, gini_data_sale, "z")

        with pt.raises(Exception):
            assesspy.ki(gini_data_assessed, gini_data_sale, 1.1)
