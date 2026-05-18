import pandas as pd
from Quant_Library.Portfolio.MarkowitzOptimiser import MarkowitzOptimiser
from Data.loaders import load_equity_dict
import sys
from pathlib import Path

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

portfolio = portfolio_returns(best_weights, returns_df)

sorted_portfolio_returns = portfolio.sort_values()
# 5% quantile for 95% VaR
var_95 = sorted_portfolio_returns.quantile(0.05)
print(f'95% VaR: {var_95:.2%}')
# 1% quantile for 99% VaR
var_99 = sorted_portfolio_returns.quantile(0.01)
print(f'99% VaR: {var_99:.2%}')

