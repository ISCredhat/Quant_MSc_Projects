import pandas as pd
import matplotlib.pyplot as plt
import sys
from pathlib import Path
import numpy as np
from Quant_Library.Fixed_Income.DF_Calc import DiscountFactorCalculator



def run_dashboard(df_yields, tenor_map):
    calc = DiscountFactorCalculator(df_yields, tenor_map)
    DF_df = calc.calculate_discount_factors()
    
    # visualisation
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Plot Yield Curve
    ax1.plot(tenor_map.values(), df_yields.iloc[-1], marker='o', color='blue')
    ax1.set_title("Current US Treasury Yield Curve")
    ax1.set_xlabel("Years to Maturity")
    ax1.set_ylabel("Yield (%)")
    
    # Plot Discount Curve
    ax2.plot(DF_df.columns.astype(float), DF_df.iloc[-1], marker='o', color='green')
    ax2.set_title("Derived Discount Factor Curve")
    ax2.set_xlabel("Years to Maturity")
    ax2.set_ylabel("Discount Factor")
    
    plt.tight_layout()
    plt.show()
    
    # financial report
    print("="*40)
    print("Theoretical Bond Pricing & Sensitivity Analysis")
    
    # Hypothetical Bond
    face_val = 100
    coupon = 5.0
    mat = 10.0
    
    price = calc.Bond_Price(face_val, coupon, mat, DF_df)
    sens = calc.Sensitivity_Analysis(face_val, coupon, mat, DF_df, 10) # 10bps shock
    
    print(f"Bond Details: {mat}Y Maturity, {coupon}% Coupon")
    print(f"Calculated Fair Price: ${price:.2f}")
    print(f"Price Sensitivity (+10bps shock): {sens:.4f}%")
    print("="*40)


#identify path root for treasury bond yield data
project_root = Path(__file__).parent.parent.parent 
data_dir = project_root / "Data" / "Fixed_Income"

#convert the tenors to years for use in DF formula
tenor_map = {
    '3M': 0.25,
    '6M': 0.5,
    '1Y': 1.0,
    '2Y': 2.0,
    '5Y': 5.0,
    '10Y': 10.0,
    '30Y': 30.0
}

treasury_yields = pd.read_csv(data_dir / "Treasury_Bond_Yields.csv", index_col=0, parse_dates=True)

run_dashboard(treasury_yields, tenor_map)