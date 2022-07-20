# Import necessary libraries
from logging import exception
import numpy as np
import statsmodels.api as sm
from .utils import check_inputs

# COD, PRD, PRB functions
def cod(ratio):

    # Input checking and error handling
    check_inputs(ratio)

    ratio = np.array(ratio)

    n = ratio.size
    median_ratio = np.median(ratio)
    cod = 100 / median_ratio * (sum(abs(ratio - median_ratio)) / n)

    return cod

def prd(fmv, sale_price):

    fmv = np.array(fmv)
    sale_price = np.array(sale_price)

    # Input checking and error handling
    check_inputs(fmv, sale_price)

    ratio = fmv / sale_price
    prd = ratio.mean() / np.average(a = ratio, weights = sale_price)

    return prd

def prb(fmv, sale_price):

    fmv = np.array(fmv)
    sale_price = np.array(sale_price)

    # Input checking and error handling
    check_inputs(fmv, sale_price)

    ratio = fmv / sale_price
    median_ratio = np.median(ratio)

    lhs = (ratio - median_ratio) / median_ratio
    rhs = np.log(((fmv / median_ratio) + sale_price) / 2) / np.log(2)

    lhs = np.array(lhs)
    rhs = np.array(rhs)

    prb_model = sm.OLS(lhs, rhs).fit()

    prb_val = float(prb_model.params)
    prb_ci = prb_model.conf_int(alpha = 0.05)[0].tolist()

    return {"prb" : prb_val, "95% ci" : prb_ci}

# Functions to determine whether assessment fairness criteria has been met
cod_met = lambda x: 5 <= x <= 15

prd_met = lambda x: 0.98 <= x <= 1.03

prb_met = lambda x: -0.05 <= x <= 0.05