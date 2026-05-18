import pandas as pd
import numpy as np

df_loaded = pd.read_csv('NVDA.csv')

#find daily percentage change of price
pct_change = df_loaded['Close'].pct_change()

#annualized returns
average_pct_change = pct_change.mean()

#standard deviation, multiplied by the square root of number of trading days to find volatility/year
volatility = pct_change.std()

#Z-Score for 95% confidence interval
Z_score = 1.645

#formula for parametric VaR is = mu - (SD * Z-Score)
parametric_VaR = average_pct_change - (Z_score * volatility)

print(f'95% of the time, losses on any one day will not exceed {parametric_VaR*100:.2f}%.')