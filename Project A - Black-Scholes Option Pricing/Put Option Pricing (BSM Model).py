import numpy as np
import scipy.stats

#BSM Model (Call Option)

def put_option_price():
    S=float(input('Enter the stock price: ')) # current asset price
    K=float(input('Enter the strike price: ')) # strike price of call option
    t=float(input('Enter the expiration (decimal): ')) # time to expiry, % of year
    r=float(input('Enter the risk-free rate (decimal): ')) # risk-free interest rate, % per annum
    q=float(input('Enter the dividend yield (decimal): ')) # dividend yield, % per annum
    v=float(input('Enter the volatility (decimal): ')) # volatility

    def d1(S, K, t, r, q, v):
        return (np.log(S / K) + t * (r - q + (v * v) / 2)) / (v * np.sqrt(t))

    d1 = d1(S, K, t, r, q, v)

    def d2(d1, v, t):
        return (d1 - v * np.sqrt(t))

    d2 = d2(d1, v, t)

    C = -S*np.exp(-q*t)*scipy.stats.norm.cdf(-d1) + K*np.exp(-r*t)*scipy.stats.norm.cdf(-d2)
    return C

PutOptionPrice = put_option_price()

print(f'${PutOptionPrice}')


