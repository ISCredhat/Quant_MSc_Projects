# Quantitative Library: Fixed Income Module

## Design Philosophy
This library is built for modularity and reusability. By centralizing the `DiscountFactorCalculator` class, we ensure that pricing logic remains decoupled from data sources, allowing for consistent results across different research projects.

## Core Class: `DiscountFactorCalculator`
The `DiscountFactorCalculator` encapsulates the mathematical logic required for fixed-income analytics:

*   **`calculate_discount_factors`**: Vectorized implementation to derive DFs from yields ($DF = e^{-rt}$).
*   **`interpolate_discount_factor`**: Uses `scipy.interpolate` to construct a continuous curve for non-standard tenors.
*   **`Bond_Price`**: Calculates the fair value of a bond by discounting periodic cash flows.
*   **`Sensitivity_Analysis`**: Computes price changes based on yield curve shocks (DV01), ensuring robust risk assessment.

## Best Practices
*   **Object-Oriented Design:** Logic is encapsulated to prevent code duplication.
*   **Vectorization:** Uses NumPy/Pandas operations instead of loops to maximize computational performance.