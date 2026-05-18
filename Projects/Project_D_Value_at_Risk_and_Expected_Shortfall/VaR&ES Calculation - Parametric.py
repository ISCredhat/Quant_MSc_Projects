import pandas as pd
import numpy as np

from Quant_Library.Portfolio.MarkowitzOptimiser import MarkowitzOptimiser
from Data.loaders import load_equity_dict

from pathlib import Path
import sys

#starting off by optmising a portfolio of 15 stocks, using the Markowitz Optimiser class I created for Project B - Markowitz Portfolio Optimisation, to find the optimal weights for the stocks in the portfolio, which I will then use to calculate the VaR and ES of the portfolio using the historical method
project_root = Path(__file__).parent.parent.parent 
data_dir = project_root / "Data" / "5yr Ticker Data"

tickers = ['AAPL','NVDA','JPM','JNJ','PG','XOM','AMZN','LLY','BRK-B','KO','MCD','V','NKE','GLD','TLT']

ticker_dfs = load_equity_dict(tickers, data_dir)

optimizer = MarkowitzOptimiser(tickers, ticker_dfs, 0.05)

#Once best weights calculated, can then find the VaR using the historical method over the past 5 years of data
best_weights = optimizer.Calc_Best_Weights()

returns_df = optimizer.df_returns

def portfolio_returns(weights, returns_df):
    # Calculate the portfolio daily percentage returns as a weighted sum of the individual stock percentage returns each day
    return returns_df.dot(weights)

portfolio = portfolio_returns(best_weights, returns_df).tail(252) # only looking at the last year of data to find the parametric VaR, as I want to use the most recent data to find the annualised mean and volatility for the parametric method, as opposed to using all 5 years of data for the historical method

#mean return of portfolio each day
average_pct_change = portfolio.mean()

#daily volatility
volatility = portfolio.std() 

#Z-Score for 95% confidence interval
Z_score = 1.645

#formula for parametric VaR is = mu - (SD * Z-Score)
parametric_VaR = average_pct_change - (Z_score * volatility)

print(f'95% of the time, losses on any one day will not exceed {parametric_VaR*100:.2f}%.')