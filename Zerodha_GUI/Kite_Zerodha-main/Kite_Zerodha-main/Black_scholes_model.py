import numpy as np
from scipy.stats import norm
from scipy import stats
import scipy
import time
from py_vollib.black_scholes import black_scholes as bs
from py_vollib.black_scholes.greeks.analytical import delta, gamma, vega, theta, rho

# def blackScholes_2(r, S, K, T, sigma, Instrument):
#     "Calculate BS price of call/put"
#     d1 = (np.log(S/K) + (r + sigma**2/2)*T)/(sigma*np.sqrt(T))
#     d2 = (np.log(S/K) + (r - sigma**2/2)*T)/(sigma*np.sqrt(T))
#     nd1=stats.norm.cdf(d1)
#     nd2=stats.norm.cdf(d2)
#     n_d1=stats.norm.cdf(-1*d1)
#     n_d2=stats.norm.cdf(-1*d2)

#     if Instrument=="C":
#         call_price=round((S*nd1)-(K*np.exp(-1*r*T)*nd2),2)
#         return call_price
#     elif Instrument=="P":
#         put_price=round((K*np.exp(-1*r*T)*n_d2)-(S*n_d1),2)
#         return put_price


def implied_vol(r, S, K, T, option_price, Right):

    def blackScholes_2(sigma):
        "Calculate BS price of call/put"
        d1 = (np.log(S/K) + (r + sigma**2/2)*T)/(sigma*np.sqrt(T))
        d2 = (np.log(S/K) + (r - sigma**2/2)*T)/(sigma*np.sqrt(T))
        nd1=stats.norm.cdf(d1)
        nd2=stats.norm.cdf(d2)
        n_d1=stats.norm.cdf(-1*d1)
        n_d2=stats.norm.cdf(-1*d2)

        if Right=="c":
            opt_price=round((S*nd1)-(K*np.exp(-1*r*T)*nd2),2)
        elif Right=="p":
            opt_price=round((K*np.exp(-1*r*T)*n_d2)-(S*n_d1),2)
        
        return option_price-opt_price
    try:
        return scipy.optimize.brentq(blackScholes_2,0.05,0.99,maxiter=10000)
    except ValueError:
        print("Solution not found.")
        return None

def option_greeks(right,Sp,S,T,rate,predicted_implied_volatility):
    Delta=delta(right,Sp,S,T,rate,predicted_implied_volatility)
    Gamma=gamma(right,Sp,S,T,rate,predicted_implied_volatility)
    Vega=vega(right,Sp,S,T,rate,predicted_implied_volatility)
    Theta=theta(right,Sp,S,T,rate,predicted_implied_volatility)
    Rho=rho(right,Sp,S,T,rate,predicted_implied_volatility)

    return Delta,Gamma, Vega, Theta, Rho



# rate=0.068
# Sp=22493.55
# T=7/365
# S=23200
# Vol=0.1761
# option_price=2.15
# right='c'



# predicted_implied_volatility=(implied_vol(rate,Sp,S,T,option_price,right))
# print("The Predicted Implied Volatility is ",predicted_implied_volatility)
# implied_volatility_accuracy=((predicted_implied_volatility-Vol)/Vol)*100
# print(f"The Accuracy of the predicted Implied Volatility is: {implied_volatility_accuracy}")

# # print("the Option Price from equation 2: ",predicted_option_price)

# # print(f'The predicetd option price from the library bs equation is {bs("c",Sp,S,T,rate,Vol)}')
# print(f'Delta of the strike is {delta(right,Sp,S,T,rate,predicted_implied_volatility)}')
# print(f'Gamma of the strike is {gamma(right,Sp,S,T,rate,predicted_implied_volatility)}')
# print(f'Vega of the strike is {vega(right,Sp,S,T,rate,predicted_implied_volatility)}')
# print(f'Theta of the strike is {theta(right,Sp,S,T,rate,predicted_implied_volatility)}')
# print(f'rho of the strike is {rho(right,Sp,S,T,rate,predicted_implied_volatility)}')

# # option_price_accuracy=((predicted_option_price-option_price)/option_price)*100


# # print(f"The Accuracy of the predicted option price is: {option_price_accuracy}")


if __name__=='__main__':
    pass