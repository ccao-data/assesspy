# Import necessary libraries
import numpy as np
import pandas as pd
import pytest as pt
from numpy import testing as npt

import assesspy

# Load the ratios sample dataset for testing
ratios_sample = assesspy.ratios_sample()

ratio = ratios_sample.ratio
assessed = ratios_sample.assessed
sale_price = ratios_sample.sale_price

##### TEST BOOT CI ##### # noqa


class TestBOOTCI:  # Ensure input function is appropriate
    def test_in_fun(self):
        with pt.raises(Exception):
            assert assesspy.boot_ci(str, ratio=ratio)

        with pt.raises(Exception):
            assesspy.boot_ci(np.add, one=ratio, two=ratio, three=ratio)

        with pt.raises(Exception):
            assesspy.boot_ci(assesspy.prd, fmv=assessed, sale_price=sale_price)

        with pt.raises(Exception):
            assesspy.boot_ci(np.add, one=ratio, two=ratio)


##### TEST COD ##### # noqa


# Calculate COD CI
cod_ci_out_95 = assesspy.cod_ci(ratio, nboot=1000)
cod_ci_out_80 = assesspy.cod_ci(ratio, nboot=1000, alpha=0.2)


class TestCODCI:
    def test_output_type(self):  # Output is expected type
        assert type(cod_ci_out_95) is list
        assert type(cod_ci_out_95[0]) is np.float64

    def test_cod(self):  # Output equal to expected
        npt.assert_allclose(
            cod_ci_out_80, [16.89576541901062, 18.641992815316588], rtol=0.02
        )
        npt.assert_allclose(
            cod_ci_out_95, [16.32413038955943, 19.226428249424757], rtol=0.02
        )

    def test_bad_input(self):  # Bad input data stops execution
        with pt.raises(Exception):
            assesspy.cod_ci([1] * 29 + [0])

        with pt.raises(Exception):
            assesspy.cod_ci(10)

        with pt.raises(Exception):
            assesspy.cod_ci(pd.concat([ratio, pd.Series(float("Inf"))]))

        with pt.raises(Exception):
            assesspy.cod_ci(pd.DataFrame(ratio))

        with pt.raises(Exception):
            assesspy.cod_ci(pd.concat([ratio, pd.Series(float("NaN"))]))

        with pt.raises(Exception):
            assesspy.cod_ci([1] * 29 + ["1"])


##### TEST PRD ##### # noqa


# Calculate PRD CI
prd_ci_out_95 = assesspy.prd_ci(assessed, sale_price, nboot=1000)
prd_ci_out_80 = assesspy.prd_ci(assessed, sale_price, nboot=1000, alpha=0.2)


class TestPRDCI:
    def test_output_type(self):  # Output is expected type
        assert type(prd_ci_out_95) is list
        assert type(prd_ci_out_95[0]) is np.float64

    def test_prd(self):  # Output equal to expected
        npt.assert_allclose(
            prd_ci_out_80, [1.0388355155405569, 1.0588098520230935], rtol=0.02
        )
        npt.assert_allclose(
            prd_ci_out_95, [1.0333716711646226, 1.0643056985556307], rtol=0.02
        )

    def test_bad_input(self):  # Bad input data stops execution
        with pt.raises(Exception):
            assesspy.prd_ci([1] * 30, [1] * 29 + [0])

        with pt.raises(Exception):
            assesspy.prd_ci([1, 1, 1], [1, 1])

        with pt.raises(Exception):
            assesspy.prd_ci(10, 10)

        with pt.raises(Exception):
            assesspy.prd_ci(
                pd.concat([assessed, pd.Series(float("Inf"))]),
                pd.concat([sale_price, pd.Series(1.0)]),
            )

        with pt.raises(Exception):
            assesspy.prd_ci(pd.DataFrame(ratio))

        with pt.raises(Exception):
            assesspy.prd_ci(
                pd.concat([assessed, pd.Series(float("NaN"))]),
                pd.concat([sale_price, pd.Series(1.0)]),
            )

        with pt.raises(Exception):
            assesspy.prd_ci([1] * 30, [1] * 29 + ["1"])
