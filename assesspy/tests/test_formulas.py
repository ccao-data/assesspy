# Import necessary libraries
import assesspy
import numpy as np
from numpy import testing as npt
import pandas as pd
import pytest as pt

# Load the ratios sample dataset for testing
ratios_sample = assesspy.ratios_sample()

ratio = ratios_sample.ratio
fmv = ratios_sample.assessed
sale_price = ratios_sample.sale_price

##### TEST COD #####

# Calculate COD
cod_out = assesspy.cod(ratios_sample.ratio)

class TestCOD:

    def test_cod(self): # Output equal to expected

        npt.assert_allclose(cod_out, 17.81456901196891, rtol = 0.02)

    def test_numeric_output(self): # Output is numeric

        assert type(cod_out) is np.float64

    def test_bad_input(self): # Bad input data stops execution

        with pt.raises(Exception):
            assesspy.cod([1] * 29 + [0])

        with pt.raises(Exception):
            assesspy.cod(10)

        with pt.raises(Exception):
            assesspy.cod(
                pd.concat([ratio, pd.Series(float('Inf'))])
                )

        with pt.raises(Exception):
            assesspy.cod(pd.DataFrame(ratio))

        with pt.raises(Exception):
            assesspy.cod(
                pd.concat([ratio, pd.Series(float('NaN'))])
                )

        with pt.raises(Exception):
            assesspy.cod([1] * 29 + ['1'])

    def test_cod_met(self): # Standard met function

        assert assesspy.cod_met(cod_out) == False

##### TEST PRD #####

# Calculate PRD
prd_out = assesspy.prd(fmv, sale_price)

class TestPRD:

    def test_prd(self): # Output equal to expected

        npt.assert_allclose(prd_out, 1.0484192615223522, rtol = 0.02)

    def test_numeric_output(self): # Output is numeric

        assert type(prd_out) is np.float64

    def test_bad_input(self): # Bad input data stops execution


        with pt.raises(Exception):
            assesspy.prd_ci([1] * 30, [1] * 29 + [0])

        with pt.raises(Exception):
            assesspy.prd_ci([1, 1, 1], [1, 1])

        with pt.raises(Exception):
            assesspy.prd(10, 10)

        with pt.raises(Exception):
            assesspy.prd(
                pd.concat([fmv, pd.Series(float('Inf'))]),
                pd.concat([sale_price, pd.Series(1.0)])
                )

        with pt.raises(Exception):
            assesspy.prd(pd.DataFrame(ratio))

        with pt.raises(Exception):
            assesspy.prd(
                pd.concat([fmv, pd.Series(float('NaN'))]),
                pd.concat([sale_price, pd.Series(1.0)])
                )

        with pt.raises(Exception):
            assesspy.prd([1] * 30, [1] * 29 + ['1'])

    def test_prd_met(self): # Standard met function

        assert assesspy.prd_met(prd_out) == False


##### TEST PRB #####

# Calculate PRB
prb_out = assesspy.prb(fmv, sale_price)['prb']

class TestPRB:

    def test_prb(self): # Output equal to expected

        npt.assert_allclose(prb_out, 0.0009470721642262901, rtol = 0.02)

    def test_numeric_output(self): # Output is numeric

        assert type(prb_out) is float

    def test_bad_input(self): # Bad input data stops execution

        with pt.raises(Exception):
            assesspy.prb_ci([1] * 30, [1] * 29 + [0])

        with pt.raises(Exception):
            assesspy.prb([1, 1, 1], [1, 1])

        with pt.raises(Exception):
            assesspy.prb(10, 10)

        with pt.raises(Exception):
            assesspy.prb(
                pd.concat([fmv, pd.Series(float('Inf'))]),
                pd.concat([sale_price, pd.Series(1.0)])
                )

        with pt.raises(Exception):
            assesspy.prb(pd.DataFrame(ratio))

        with pt.raises(Exception):
            assesspy.prb(
                pd.concat([fmv, pd.Series(float('NaN'))]),
                pd.concat([sale_price, pd.Series(1.0)])
                )

        with pt.raises(Exception):
            assesspy.prb([1] * 30, [1] * 29 + ['1'])

    def test_prb_met(self): # Standard met function

        assert assesspy.prb_met(prb_out) == True