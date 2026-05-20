import numpy as np
import pandas as pd 
from scipy.interpolate import interp1d

class DiscountFactorCalculator:
    
    def __init__(self, yields_df, tenor_map):
        self.yields_df = yields_df
        self.tenor_map = tenor_map


    def calculate_discount_factors(self):
        discount_factors_df = pd.DataFrame(index=self.yields_df.index)
        for column in self.yields_df.columns:
            tenor_years = self.tenor_map[column]
            discount_factors_df.loc[:, f'{tenor_years}'] = np.exp(-self.yields_df[column] * tenor_years / 100)
        return discount_factors_df

    #interpolating the discount factors to find the discount factor for a non standard tenor
    def interpolate_discount_factor(self, discount_factors_df, target_tenor):
        # Extract tenors and corresponding discount factors
        tenors = np.array(discount_factors_df.columns, dtype=float)  # Convert column names to float for interpolation
        discount_factors = discount_factors_df.iloc[-1].values  # Use the most recent discount factors

        # Create an interpolation function
        interpolation_function = interp1d(tenors, discount_factors, kind='linear', fill_value="extrapolate")

        # Interpolate the discount factor for the target tenor
        interpolated_df = interpolation_function(target_tenor)
        
        return interpolated_df

    def Bond_Price(self, face_value, coupon_rate, maturity_years, discount_factors_df):
        # Calculate the annual coupon payment
        coupon_payment = face_value * coupon_rate / 100
        
        # Calculate the present value of the coupon payments
        pv_coupons = sum(coupon_payment * self.interpolate_discount_factor(discount_factors_df, maturity_years - i) for i in range(1, int(maturity_years) + 1))
        
        # Calculate the present value of the face value at maturity
        pv_face_value = face_value * self.interpolate_discount_factor(discount_factors_df, maturity_years)
        
        # The price of the bond is the sum of the present values of the coupons and the face value
        bond_price = pv_coupons + pv_face_value
        
        return bond_price

    def Sensitivity_Analysis(self, face_value, coupon_rate, maturity_years, discount_factors_df, yield_change_bps):
        # 1. Get original price
        original_price = self.Bond_Price(face_value, coupon_rate, maturity_years, discount_factors_df)
        
        # 2. Derive implied yields (r = -ln(DF) / t)
        tenors = np.array(discount_factors_df.columns, dtype=float)
        discount_factors = discount_factors_df.iloc[-1].values
        
        # Avoid division by zero at t=0
        implied_yields = -np.log(discount_factors) / tenors
        
        # 3. Apply shock (yield_change_bps / 10000)
        shock = yield_change_bps / 10000
        new_yields = implied_yields + shock
        
        # 4. Convert back to shocked Discount Factors
        new_dfs = np.exp(-new_yields * tenors)
        
        # 5. Create a new dataframe format for the Bond_Price function
        new_df_series = pd.DataFrame([new_dfs], columns=discount_factors_df.columns, index=discount_factors_df.index[-1:])
        
        # 6. Calc new price
        new_price = self.Bond_Price(face_value, coupon_rate, maturity_years, new_df_series)
        
        return (new_price - original_price) / original_price * 100
