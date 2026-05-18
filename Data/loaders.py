import pandas as pd
from pathlib import Path

def load_equity_dict(tickers: list, data_dir: str = "../Data/5yr Ticker Data"):
    data_path = Path(data_dir)
    all_csvs = {}

    for ticker in tickers:
        file_path = data_path / f"{ticker}.csv"
        if file_path.exists():
            df = pd.read_csv(file_path, index_col='Date', parse_dates=True)
            all_csvs[ticker] = df
        else:
            print(f"Warning: {ticker}.csv not found in {data_dir}")
            
    return all_csvs
