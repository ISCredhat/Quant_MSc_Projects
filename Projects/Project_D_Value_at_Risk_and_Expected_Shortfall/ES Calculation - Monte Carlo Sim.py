import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#yfinance data already stored as CSV, chose NVDA to test with, 5 years of daily data
ticker = 'NVDA'
df_loaded = pd.read_csv('NVDA.csv')

#S0 = last close price of the dataset
S0 = df_loaded['Close'].iloc[-1]

#final year of data, purely for graphing purposes later
actual_prices = df_loaded['Close'].tail(252).values

#to find annual return and volatility
daily_pc_change = df_loaded['Close'].pct_change()

#annualized returns
annualized_returns = daily_pc_change.mean() * 252

#standard deviation, multiplied by the square root of number of trading days to find volatility/year
volatility = daily_pc_change.std() * np.sqrt(252)

#function for geometric brownian motion, the time step is 1/252 (1 trading day in a full year) but probably should have used a variable in case I wanted to simulate over different periods of time
def GBM(S0):

    S1 = S0 * np.exp(((annualized_returns - volatility**2/2) * (1/252) + volatility*np.sqrt(1/252)*np.random.normal()))

    return S1

# simulation loop, simulating 1 year of potential price movement using the GBM function 1000 times to find the mean movement

loop = 0
simulation_array = []
while loop < 1000:
    price_array = [S0]
    day = 0
    while day < 252:
        S1 = GBM(price_array[-1])
        price_array.append(S1)
        day += 1
    simulation_array.append(price_array)
    loop += 1

simulation_matrix = np.array(simulation_array)

PnL_array = []
for i in range(len(simulation_matrix)):
    PnL = float((simulation_matrix[i][-1] - simulation_matrix[i][0])/simulation_matrix[i][0])
    PnL_array.append(PnL)

PnL_array.sort()

Expected_Shortfall = np.array(PnL_array[:int(len(PnL_array)*0.05)]).mean()

print(Expected_Shortfall)