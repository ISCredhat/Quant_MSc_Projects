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

# Used AI to write the visualisation code, was more interested in experimenting/coding the simulation
# plots the final year of data then on the end plots the simulation results, needs higher resolution on the axis
# identifies mean simulation, however in practice would want to be able to identify probability of price being x% above or below starting price from simulation

simulation_matrix = np.array(simulation_array)
future_days = 252
history = df_loaded['Close'].tail(252).values
days_history = np.arange(0, 252)
# The x-axis for the future starts at day 251 and goes to 503
# This ensures the lines connect perfectly
days_future = np.arange(251, 251 + future_days + 1)


plt.figure(figsize=(14, 7))

# Plot History
plt.plot(days_history, history, color='black', lw=2, label='Actual History (Past Year)')

# Plot Simulations
# We plot the transpose, but we provide the offset x-axis 'days_future'
plt.plot(days_future, simulation_matrix.T, color='blue', alpha=0.02)

# Plot the Future Mean (The Expected Trend)
plt.plot(days_future, np.mean(simulation_matrix, axis=0), color='cyan', lw=2, label='Simulated Expected Path')

# Formatting for Clarity
plt.axvline(x=251, color='red', linestyle='--', alpha=0.5) # The "Today" line
plt.text(251, plt.ylim()[1]*0.9, ' TODAY', color='red', fontweight='bold')

plt.title(f'Continuous Stock Forecast: {ticker} (History + 1,000 GBM Simulations)')
plt.xlabel('Trading Days')
plt.ylabel('Price ($)')
plt.legend(loc='upper left')
plt.grid(True, alpha=0.2)

plt.show()
