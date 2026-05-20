import yfinance as yf
import datetime as dt
import pandas as pd

Start_Date = dt.datetime(2020, 1, 1)
End_Date = dt.datetime(2025, 12, 31) # five years of data, will probably have to get it monthly or weekly to allow for yf restrictions

tickers = [
    'AAPL',    # Tech: Consumer Electronics
    'NVDA',    # Tech: Semiconductors/AI (High Growth)
    'JPM',     # Financials: Banking
    'JNJ',     # Healthcare: Pharmaceuticals (Defensive)
    'PG',      # Consumer Staples: Household products
    'XOM',     # Energy: Oil & Gas
    'AMZN',    # Consumer Discretionary: E-commerce
    'LLY',     # Healthcare: Biotech (High Growth)
    'BRK-B',   # Financials: Multi-sector conglomerate
    'KO',      # Consumer Staples: Beverages
    'MCD',     # Consumer Discretionary: Restaurants
    'V',       # Financials: Payment processing
    'NKE',     # Consumer Discretionary: Apparel
    'GLD',     # Commodity: Gold (Inflation hedge)
    'TLT'      # Bonds: 20+ Year Treasury (Risk-off asset)
] # couple of random but different stocks to test optimisation theory on, need to be relatively uncorrelated

for ticker in tickers:
    # 1. Download the data
    df = yf.download(ticker, start=Start_Date, end=End_Date)

    # 2. Fix the MultiIndex Header
    # If the columns have two levels (Price and Ticker), we drop the Ticker level
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)  # This removes the 'GLD'/'TSLA' label from the header

    # 3. Select only the columns you want
    df = df[['Open', 'Close']]

    # 4. Save to CSV
    # This will now have headers: Date, Open, Close
    df.to_csv(f'{ticker}.csv')

    print(f"Finished {ticker}")
    print(df.head())

