# Fixed-Income Term Structure Engine

## Overview
This project constructs a continuous **Zero-Coupon Yield Curve** from raw US Treasury market data. It serves as a foundational engine for fixed-income analysis, enabling the pricing of coupon-bearing bonds and the assessment of interest rate sensitivity (DV01).

## Key Features
*   **Automated Data Ingestion:** Fetches real-time Constant Maturity Treasury (CMT) yields from the Federal Reserve (FRED).
*   **Term Structure Construction:** Transforms discrete yield data into a continuous discount factor curve using linear interpolation.
*   **Bond Pricing Engine:** Implements a Present Value (PV) model for coupon-bearing bonds.
*   **Risk Analysis:** Quantifies portfolio sensitivity to interest rate shifts (DV01) via scenario analysis.

## Visualizations
![Yield Curves](yield_curve_and_discount_factors.png)
*Figure: The current term structure of US Treasuries and the derived discount factor curve.*

## Usage
1. Configure your environment variable `FRED_API_KEY` in the project root.
2. Run `Discount_Factor&Interpolation.py` to generate the curve and run pricing scenarios.