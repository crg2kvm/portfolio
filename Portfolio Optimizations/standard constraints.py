import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

def calcreturns(ticker,time_frame):
    tick = yf.Ticker(ticker)
    dat = pd.DataFrame(tick.history(period=time_frame))
    price_relative = []
    price_relative = np.array(np.zeros(len(dat)-1))
    for i in range(len(dat)-1):
        prior = dat['Close'][i]
        current = dat['Close'][i+1]
        price_relative[i] = current/prior
    returns1 = np.log(price_relative) * 100
    expected_returns = returns1.mean()
    return expected_returns, returns1

def allto(stocks,timeframe):
    samp = pd.DataFrame()
    returns = []
    for i in stocks:
        e, r = calcreturns(i,timeframe)
        samp[i] = r
        returns.append(e)
    return samp.cov(), returns


def portfolio_variance(weights, cov_matrix):
    return np.dot(weights.T, np.dot(cov_matrix, weights))

def generate_portfolio_weights(num_assets, num_portfolios):
    weights_matrix = []
    for i in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights /= np.sum(weights)
        weights_matrix.append(weights)
    return weights_matrix

def portfolio_return(weights, returns):
    return np.dot(weights, returns)

"""
def curve(stocks, num_portfolios, timeframe): 
    cov_matrix, stockreturns = allto(stocks, timeframe)
    returns = stockreturns 
    weights_matrix = generate_portfolio_weights(len(stocks), num_portfolios)
    portfolio_returns = []
    portfolio_volatilities = []
    for weights in weights_matrix:
        port_return = portfolio_return(weights, returns)
        port_var = portfolio_variance(weights, cov_matrix)
        portfolio_returns.append(port_return)
        portfolio_volatilities.append(np.sqrt(port_var))
    portfolio_returns = np.array(portfolio_returns)
    portfolio_volatilities = np.array(portfolio_volatilities)
    portfolio_df = pd.DataFrame({'Returns': portfolio_returns, 'Volatility': portfolio_volatilities})
    portfolio_df.sort_values(by='Volatility', inplace=True)
    efficient_frontier = portfolio_df.groupby('Volatility')['Returns'].max().reset_index()
    plt.plot(efficient_frontier['Volatility'], efficient_frontier['Returns'])
    plt.xlabel('Risk')
    plt.ylabel('Returns')
    plt.title('Efficient Frontier')
    plt.show()
"""
def efficient_frontier(stocks, num_portfolios, timeframe, risk_free_rate=0.01): 
    cov_matrix, stockreturns = allto(stocks, timeframe)
    returns = stockreturns 
    weights_matrix = generate_portfolio_weights(len(stocks), num_portfolios)
    target_returns = np.linspace(min(stockreturns), max(stockreturns), num_portfolios)
    print(stockreturns)
    efficient_portfolio_returns = []
    efficient_portfolio_volatilities = []
    efficient_portfolio_weights = []
    for target in target_returns:
        cons = ({'type': 'eq', 'fun': lambda x: portfolio_return(x, returns) - target},   # The portfolio return must meet the target
                {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})                          # The weights must sum up to 1
        bounds = tuple((0, 1) for asset in range(len(stocks)))
        result = minimize(portfolio_variance, weights_matrix[0], args=(cov_matrix,), method='SLSQP', bounds=bounds, constraints=cons)
        efficient_portfolio_returns.append(target)
        efficient_portfolio_volatilities.append(np.sqrt(result['fun']))
        efficient_portfolio_weights.append(result['x'])
    plt.plot(efficient_portfolio_volatilities, efficient_portfolio_returns, 'b-', linewidth=2)
    plt.xlabel('Volatility')
    plt.ylabel('Expected Returns')
    plt.title('Efficient Frontier')
    plt.show()


efficient_frontier(["GOOG","AAPL","AMZN","TSLA"],1000, "1mo")