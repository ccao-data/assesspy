# Import necessary libraries
import pkg_resources
import pandas as pd


# Load pre-made ratios sample data.
def ratios_sample():

    """
    This sample was take from Evanston and New Trier in 2019. Ratios are
    calculated using assessor certified (post-appeal) fair market values.

    :return:
        A data frame with 979 observation and 4 variables:

        ======================== =======================================================
        **assessed** (`float`)   The fair market assessed value predicted by CCAO
                                 assessment models, including any successful appeals
        **sale_price** (`float`) The recorded sale price of this property
        **ratio** (`float`)      Sales ratio representing fair market value / sale price
        **town** (`object`)      Township name the property is in
        ======================== =======================================================

    :rtype: DataFrame
    """

    stream = pkg_resources.resource_stream(
        __name__,
        'data/ratios_sample.parquet'
        )
    return pd.read_parquet(stream)
