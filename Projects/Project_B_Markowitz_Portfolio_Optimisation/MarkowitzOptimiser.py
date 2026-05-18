import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt


class MarkowitzOptimiser:

    def __init__(self, tickers, risk_free_rate):
        self.tickers = tickers
        self.stock_dfs = {}
        self.annualized_returns = {}
        self.df_returns = pd.DataFrame()
        self.df_covariance = pd.DataFrame()
        self.risk_free_rate = risk_free_rate
    
    def load_data(self):
        #maybe not the cleanest way, however it was quick, finding the daily pct change and then appending to the df to find annualised returns
        for ticker in self.tickers:
            df_loaded = pd.read_csv(f'Project_B_Markowitz_Portfolio_Optimisation/5yr Ticker Data/{ticker}.csv')
            daily_pc_change = df_loaded['Close'].pct_change()
            df_loaded.insert(2, '% Change', daily_pc_change)
            self.stock_dfs[ticker] = df_loaded
    
    def calculate_annualized_returns(self):
        # calcuating and storing annualized returns for each ticker in a dictionary
        for ticker in self.tickers:
            stock_df = self.stock_dfs[ticker]
            self.annualized_returns[ticker] = stock_df['% Change'].mean() * 252

    def calculate_covariance_matrix(self):
        # creating a single dataframe of daily returns to find covariance matrix
        for ticker in self.tickers:
            stock_df = self.stock_dfs[ticker]
            if len(self.df_returns) == 0:
                self.df_returns = pd.DataFrame(stock_df['% Change'])
                self.df_returns = self.df_returns.set_axis([f'{self.tickers[0]}'], axis = 1)
            else:
                self.df_returns.insert(self.tickers.index(f'{ticker}'), f'{ticker}', stock_df['% Change'])
        
        #finding covariance matrix to eventually use to find variance and volatility
        self.df_covariance = self.df_returns.cov()

    # found this stars and bars method for finding random divisors on stackexchange
    def constrained_sum_sample_pos(n, total):
        dividers = sorted(random.sample(range(1, total), n - 1))
        return [a - b for a, b in zip(dividers + [total], [0] + dividers)]

    def monte_carlo_simulation(self, iterations=50000):
        iteration_results = [] # storing all iteration results
        iteration_buckets = [] # storing the buckets for the iterations
        loop = 0 # counter for the while loop

        while loop < iterations:
            #defining my split of stocks for the portfolio
            buckets = MarkowitzOptimiser.constrained_sum_sample_pos(len(self.tickers), 100)
            #turning buckets into percentage values that I can use
            #probably didnt need to iterate through the buckets, but did so anyway
            for i in range(len(buckets)):
                buckets[i] = buckets[i] / 100

            #convert buckets into a series to use pd.dot() method
            buckets = pd.Series(buckets, index=self.tickers)

            #finding the variance (buckets*covariance matrix*buckets)
            #result should be a single integer
            Variance = (buckets.dot(self.df_covariance)).dot(buckets)

            Volatility = np.sqrt(Variance) * np.sqrt(252)

            #Expected return is = bucket*annualized return for all tickers and each bucket

            portfolio_return = 0
            for i in range(len(self.tickers)):
                portfolio_return += self.annualized_returns[self.tickers[i]]*buckets.iloc[i]


            #assume a risk-free rate of 5%
            r = self.risk_free_rate
            excess_return = portfolio_return - r
            Sharpe_Ratio = excess_return / Volatility

            #store results
            result = [portfolio_return, Volatility, Sharpe_Ratio]
            iteration_results.append(result)

            #store buckets for later reference
            iteration_buckets.append(buckets)
            loop += 1

        results = np.array(iteration_results) # Converting to a numpy array makes slicing easy

        # 1. Extract the columns
        port_returns = results[:, 0]
        port_volatility = results[:, 1]
        sharpe_ratios = results[:, 2]

        # 2. Find the special "Star" portfolios to highlight them
        # Find the index of the highest Sharpe Ratio
        max_sharpe_idx = np.argmax(sharpe_ratios)

        best_weights = iteration_buckets[max_sharpe_idx]

        return best_weights
    