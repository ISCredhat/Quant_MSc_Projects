import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt

tickers = ['AAPL','NVDA','JPM','JNJ','PG','XOM','AMZN','LLY','BRK-B','KO','MCD','V','NKE','GLD','TLT'      ]

stock_dfs = {}

#maybe not the cleanest way, however it was quick, finding the daily pct change and then appending to the df to find annualised returns
for ticker in tickers:
    df_loaded = pd.read_csv(f'5yr Ticker Data/{ticker}.csv')
    daily_pc_change = df_loaded['Close'].pct_change()
    df_loaded.insert(2, '% Change', daily_pc_change)
    stock_dfs[ticker] = df_loaded

# calcuating and storing annualized returns for each ticker in a dictionary
annualized_returns = {}
for ticker in tickers:
    stock_df = stock_dfs[ticker]
    annualized_returns[ticker] = stock_df['% Change'].mean() * 252

# creating a signle dataframe of daily returns to find covariance matrix
df_returns = pd.DataFrame()
for ticker in tickers:
    stock_df = stock_dfs[ticker]
    if len(df_returns) == 0:
        df_returns = pd.DataFrame(stock_df['% Change'])
        df_returns = df_returns.set_axis([f'{tickers[0]}'], axis = 1)
    else:
        df_returns.insert(tickers.index(f'{ticker}'), f'{ticker}', stock_df['% Change'])

#finding covariance matrix to eventually use to find variance and volatility
df_covariance = df_returns.cov()

# found this stars and bars method for finding random divisors on stackexchange
def constrained_sum_sample_pos(n, total):
    dividers = sorted(random.sample(range(1, total), n - 1))
    return [a - b for a, b in zip(dividers + [total], [0] + dividers)]

#monte carlo simulation to find optimal portfolio

loop = 0 # counter for the while loop

iteration_results = [] # storing all iteration results
iteration_buckets = [] # storing the buckets for the iterations
while loop<50000:
    #defining my split of stocks for the portfolio
    buckets = constrained_sum_sample_pos(len(tickers), 100)
    #turning buckets into percentage values that I can use
    #probably didnt need to iterate through the buckets, but did so anyway
    for i in range(len(buckets)):
        buckets[i] = buckets[i] / 100

    #convert buckets into a series to use pd.dot() method
    buckets = pd.Series(buckets, index=tickers)

    #finding the variance (buckets*covariance matrix*buckets)
    #result should be a single integer
    Variance = (buckets.dot(df_covariance)).dot(buckets)

    Volatility = np.sqrt(Variance) * np.sqrt(252)

    #Expected return is = bucket*annualized return for all tickers and each bucket

    portfolio_return = 0
    for i in range(len(tickers)):
        portfolio_return += annualized_returns[tickers[i]]*buckets[i]


    #assume a risk-free rate of 5%
    r = 0.05
    excess_return = portfolio_return - r
    Sharpe_Ratio = excess_return / Volatility

    #store results
    result = [portfolio_return, Volatility, Sharpe_Ratio]
    iteration_results.append(result)

    #store buckets for later reference
    iteration_buckets.append(buckets)
    loop += 1
    if loop % 10000 == 0:
        print(loop)

# Used AI to write the graphing code, was more interested in experimenting/writing the code to actually optimise and run the simulation

# Format: [[ret1, vol1, sharpe1], [ret2, vol2, sharpe2], ...]
results = np.array(iteration_results) # Converting to a numpy array makes slicing easy

# 1. Extract the columns
port_returns = results[:, 0]
port_volatility = results[:, 1]
sharpe_ratios = results[:, 2]

# 2. Find the special "Star" portfolios to highlight them
# Find the index of the highest Sharpe Ratio
max_sharpe_idx = np.argmax(sharpe_ratios)
max_sharpe_return = port_returns[max_sharpe_idx]
max_sharpe_vol = port_volatility[max_sharpe_idx]

# Find the index of the lowest Volatility
min_vol_idx = np.argmin(port_volatility)
min_vol_return = port_returns[min_vol_idx]
min_vol_vol = port_volatility[min_vol_idx]

# 3. Create the plot
plt.figure(figsize=(10, 7))

# Create the scatter plot
# c=sharpe_ratios tells it to color the dots based on the Sharpe value
# cmap='viridis' is a professional looking color scheme
plt.scatter(port_volatility, port_returns, c=sharpe_ratios, cmap='viridis', marker='o', s=10, alpha=0.3)

# Add a colorbar to show what the colors mean
plt.colorbar(label='Sharpe Ratio')

# 4. Mark the "Best" Portfolios with Stars
# The red star is the Maximum Sharpe portfolio
plt.scatter(max_sharpe_vol, max_sharpe_return, color='r', marker='*', s=200, label='Maximum Sharpe')

# The green star is the Minimum Volatility portfolio
plt.scatter(min_vol_vol, min_vol_return, color='g', marker='*', s=200, label='Minimum Volatility')

# 5. Add labels and titles
plt.title('Efficient Frontier: Portfolio Optimization')
plt.xlabel('Volatility (Annualized Risk)')
plt.ylabel('Expected Annual Return')
plt.legend(labelspacing=0.8)

plt.grid(True)

# Retrieve the specific weights Series using the max_sharpe index
best_weights = iteration_buckets[max_sharpe_idx]

print("\n" + "="*45)
print("🏆 OPTIMAL PORTFOLIO WEIGHTS (RED STAR) 🏆")
print("="*45)
print(f"Expected Annual Return: {max_sharpe_return * 100:.2f}%")
print(f"Annualized Volatility:  {max_sharpe_vol * 100:.2f}%")
print(f"Sharpe Ratio:           {sharpe_ratios[max_sharpe_idx]:.2f}")
print("-" * 45)

# Loop through the Series and print the ticker and percentage
# We multiply the weight by 100 and use .0f to format it cleanly as a whole percentage
for ticker, weight in best_weights.items():
    print(f"{ticker:<6}: {weight * 100:>5.0f}%")

print("="*45)

plt.show()
