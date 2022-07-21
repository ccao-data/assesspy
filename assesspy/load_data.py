# Import necessary libraries
import pkg_resources
import pandas as pd


# Load pre-made ratios sample data.
def ratios_sample():

    stream = pkg_resources.resource_stream(
        __name__,
        'data/ratios_sample.parquet'
        )
    return pd.read_parquet(stream)
