from dotenv import load_dotenv, find_dotenv
import os
from fredapi import Fred
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats


load_dotenv(find_dotenv())

fred_api_key = os.getenv("FREDAPI_Key")

fred = Fred(api_key=fred_api_key)

# Series IDs for Treasury Constant Maturity
# standard FRED IDs: 
# DGS3MO = 3-Month, DGS1 = 1-Year, DGS10 = 10-Year, etc.
tenors = {
    '3M': 'DGS3MO',
    '6M': 'DGS6MO',
    '1Y': 'DGS1',
    '2Y': 'DGS2',
    '5Y': 'DGS5',
    '10Y': 'DGS10',
    '30Y': 'DGS30'
}

# Fetch data for each 
data_dict = {}
for name, series_id in tenors.items():
    # Fetch the series
    series = fred.get_series(series_id)
    data_dict[name] = series

# Create a DataFrame and clean it
df_yields = pd.DataFrame(data_dict)

df_yields = df_yields.dropna()

df_yields.to_csv("Treasury_Bond_Yields.csv", index=True)

