from importlib.resources import as_file, files

import pandas as pd


def ccao_sample() -> pd.DataFrame:
    """
    Sample of sales and estimated market values taken from Evanston and New
    Trier in 2019. Estimates are Assessor certified (post-appeal) fair market
    values.

    :return:
        A Pandas DataFrame with 979 observation and 3 variables:

        ============================== ============================================
        **estimate** (`float`)         Fair market value predicted by CCAO
                                       assessment models, after any successful appeals
        **sale_price** (`float`)       Recorded sale price of this property
        **township_name** (`object`)   Name of the township containing the property
        ============================== ============================================

    :rtype: pd.DataFrame
    """
    source = files("assesspy").joinpath("data/ccao_sample.parquet")
    with as_file(source) as file:
        return pd.read_parquet(file)


def IAAO_sample_1_4() -> pd.DataFrame:
    """
    Sample of sales and estimated market values provided in table 1.4 by the IAAO in the following report:

    .. IAAO. (2013). Standard on Ratio Studies. https://www.iaao.org/wp-content/uploads/Standard_on_Ratio_Studies.pdf

    :return:
        A Pandas DataFrame with 18 observation and 2 variables:

        ======================== =====================================================
        **estimate** (`float`)       Assessed fair market value
        **sale_price** (`float`)     Recorded sale price of this property
        ======================== =====================================================

    :rtype: pd.DataFrame
    """
    source = files("assesspy").joinpath("data/IAAO_sample_1_4.csv")
    with as_file(source) as file:
        return pd.read_csv(file)


def IAAO_sample_d_1() -> pd.DataFrame:
    """
    Sample of sales and estimated market values provided in table D.1 by the IAAO in the following report:

    .. IAAO. (2013). Standard on Ratio Studies. https://www.iaao.org/wp-content/uploads/Standard_on_Ratio_Studies.pdf

    :return:
        A Pandas DataFrame with 25 observation and 2 variables:

        ======================== =====================================================
        **estimate** (`float`)       Assessed fair market value
        **sale_price** (`float`)     Recorded sale price of this property
        ======================== =====================================================

    :rtype: pd.DataFrame
    """
    source = files("assesspy").joinpath("data/IAAO_sample_d_1.csv")
    with as_file(source) as file:
        return pd.read_csv(file)
    

def quintos_sample() -> pd.DataFrame:
    """
    Sample of sales and estimated market values provided by Quintos in the
    following MKI papers:

    .. Quintos, C. (2020). A Gini measure for vertical equity in property
        assessments. https://researchexchange.iaao.org/jptaa/vol17/iss2/2

    .. Quintos, C. (2021). A Gini decomposition of the sources of inequality in
        property assessments. https://researchexchange.iaao.org/jptaa/vol18/iss2/6

    :return:
        A Pandas DataFrame with 30 observation and 2 variables:

        ======================== =====================================================
        **estimate** (`float`)       Assessed fair market value
        **sale_price** (`float`)     Recorded sale price of this property
        ======================== =====================================================

    :rtype: pd.DataFrame
    """
    source = files("assesspy").joinpath("data/quintos_sample.csv")
    with as_file(source) as file:
        return pd.read_csv(file)
