# Data Ingestion: Fixed Income

## Purpose
This module handles the extraction and pre-processing of historical yield data. It ensures data is clean, aligned, and ready for quantitative modeling.

## Engineering Standards
*   **Security:** Uses `.env` files to manage API credentials. Ensure you have a `.env` file in the project root containing `FRED_API_KEY`.
*   **Reproducibility:** The script performs data validation (checking for missing values/NaNs) to ensure the term structure construction does not break during interpolation.

## Configuration
Add your API key to a `.env` file in the root directory:
```text
FRED_API_KEY=your_key_here