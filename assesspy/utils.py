# Import necessary libraries
import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype


def check_inputs(*args):
    out = [""]

    for x in args:
        # *args passed into *args can created nested tuples - unnest
        if isinstance(x, tuple):
            args = x

    for x in args:
        if type(x) == pd.core.frame.DataFrame:
            raise Exception("Input cannot be a dataframe.")

        check = pd.Series(x)

        if not is_numeric_dtype(check):
            raise Exception("All input vectors must be numeric.")
        if check.isnull().values.any():
            out.append("\nInput vectors contain null values.")
        if len(check) <= 1:
            out.append("\nAll input vectors must have length greater than 1.")
        if not all(np.isfinite(check) | check.isnull()):
            out.append("\nInfinite values in input vectors.")
        if any(check == 0):
            out.append("\nInput vectors cannot contain values of 0.")

    out = set(out)

    if len(out) > 1:
        raise Exception("".join(map(str, out)))
