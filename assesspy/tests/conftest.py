import pathlib

import numpy as np
import pandas as pd
import pytest as pt

import assesspy as ap

FIXTURE_DIR = pathlib.Path(__file__).parent / "fixtures"


@pt.fixture(autouse=True, scope="function")
def set_seed() -> None:
    np.random.seed(42)
    return None


@pt.fixture(scope="session")
def ccao_data() -> tuple:
    sample = ap.ccao_sample()
    return sample.estimate, sample.sale_price


@pt.fixture(scope="session")
def quintos_data() -> tuple:
    sample = ap.quintos_sample()
    return sample.estimate, sample.sale_price


@pt.fixture(scope="session", params=["1_1", "1_4", "d_1", "d_2"])
def iaao_data_name(request):
    return request.param


@pt.fixture(scope="session")
def iaao_data(iaao_data_name) -> tuple:
    sample = pd.read_csv(FIXTURE_DIR / f"iaao_table_{iaao_data_name}.csv")
    return sample.estimate, sample.sale_price


@pt.fixture(
    scope="session",
    params=[
        ([1] * 30, [1] * 29),
        ([0, 0, 0], [0, 0, 0]),
        ([-1, -2, -3], [-1, -2, -3]),
        ([], []),
        ([1], [1]),
        (
            pd.concat(
                [ap.ccao_sample()["estimate"], pd.Series([1.0], dtype="float")]
            ),
            pd.concat(
                [
                    ap.ccao_sample()["sale_price"],
                    pd.Series([float("Inf")], dtype="float"),
                ]
            ),
        ),
        (
            pd.concat(
                [ap.ccao_sample()["estimate"], pd.Series([1.0], dtype="float")]
            ),
            pd.concat(
                [
                    ap.ccao_sample()["sale_price"],
                    pd.Series([float("NaN")], dtype="float"),
                ]
            ),
        ),
    ],
)
def bad_input(request) -> tuple:
    return request.param


@pt.fixture(
    scope="session",
    params=[
        ([1e10, 2e10, 3e10], [1e10, 2e10, 3e10]),
        ([1, 2.0, 3], [1.0, 2, 3.0]),
        (ap.ccao_sample()["estimate"], ap.ccao_sample()["sale_price"]),
        (
            ap.ccao_sample()["estimate"].set_axis(
                pd.Index(
                    np.random.permutation(ap.ccao_sample()["estimate"].index)
                )
            ),
            ap.ccao_sample()["sale_price"].set_axis(
                pd.Index(
                    np.random.permutation(ap.ccao_sample()["sale_price"].index)
                )
            ),
        ),
    ],
)
def good_input(request) -> tuple:
    return request.param
