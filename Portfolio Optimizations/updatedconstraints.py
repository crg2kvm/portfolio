import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

def calcreturns(ticker,time_frame):
    tick = yf.Ticker(ticker)
    dat = pd.DataFrame(tick.history(period=time_frame))
    price_relative = []
    price_relative = np.array(np.zeros(len(dat)-2))
    for i in range(len(dat)-2):
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



def efficient_frontier(stocks, num_portfolios, timeframe, weights, security_type = None, stock_weight = None, bond_weight = None):
    if security_type is not None: 
        security_type.sort()
        num_stock = security_type.count("Stock")
    
    print(security_type)
    cov_matrix, stockreturns = allto(stocks, timeframe)
    returns = stockreturns 
    weights_matrix = generate_portfolio_weights(len(stocks), num_portfolios)
    target_returns = np.linspace(min(stockreturns), max(stockreturns), num_portfolios)
    print(cov_matrix)
    print(stockreturns)
    efficient_portfolio_returns = []
    efficient_portfolio_volatilities = []
    efficient_portfolio_weights = []
    weights_matrix[0] = weights
    """
    def min_func(weights):
        return portfolio_variance(weights, cov_matrix)
    for idx, target in enumerate(target_returns):
    # Using different weights for each optimization
        initial_guess = weights_matrix[idx]
        if security_type is not None:
            cons = ({'type': 'eq', 'fun': lambda x: portfolio_return(x, returns) - target},   
                    {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
                    {'type': 'eq', 'fun': lambda x: np.sum(x[:num_stock]) - stock_weight},  
                    {'type': 'eq', 'fun': lambda x: np.sum(x[num_stock:]) - bond_weight}) 
        else:
            cons = ({'type': 'eq', 'fun': lambda x: portfolio_return(x, returns) - target},   
                    {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})

        bounds = tuple((0, 1) for asset in range(len(stocks)))
        result = minimize(min_func, initial_guess, method='SLSQP', bounds=bounds, constraints=cons)
        efficient_portfolio_returns.append(target)
        efficient_portfolio_volatilities.append(np.sqrt(result['fun']))
        efficient_portfolio_weights.append(result['x'])
    """
    for target in target_returns:
        if security_type is not None:
            cons = ({'type': 'eq', 'fun': lambda x: portfolio_return(x, returns) - target},   
                    {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
                    #{'type': 'eq', 'fun': lambda x: np.sum(x[:num_stock]) - bond_weight},  
                    {'type': 'eq', 'fun': lambda x: np.sum(x[num_stock:]) - stock_weight}
                    ) 
        else:
            cons = ({'type': 'eq', 'fun': lambda x: portfolio_return(x, returns) - target},   
                    {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
                    #{'type': 'ineq', 'fun': lambda x: portfolio_return(x, returns)}
                    )
        bounds = tuple((0, 1) for asset in range(len(stocks)))
        result = minimize(portfolio_variance, weights_matrix[0], args=(cov_matrix,), method='SLSQP', bounds=bounds, constraints=cons, options={'maxiter': 100000, 'ftol': 1e-9})
        efficient_portfolio_returns.append(target)
        efficient_portfolio_volatilities.append(np.sqrt(result['fun']))
        efficient_portfolio_weights.append(result['x'])
    #print("Success: ", result.success)
    print("Message: ", result.message)
    
    #plt.scatter(efficient_portfolio_volatilities, efficient_portfolio_returns)
    #plt.xlabel('Volatility')
    #plt.ylabel('Expected Returns')
    #plt.title('Efficient Frontier')
    #plt.show()
    
    return efficient_portfolio_returns,efficient_portfolio_volatilities


#efficient_frontier(["XLP","XLE","XOP","TLT","AGG","SHY"], 1000, "1y",security_type=["Stock","Stock","Stock","Bond","Bond","Bond"],stock_weight=0.55,bond_weight=0.45)

def graphit(portfolios,stocks, security_type, time_frame, noconstraints = False):
    if noconstraints == False:
        weights = np.random.random(len(stocks))
        weights = [1/len(stocks)] * len(stocks)
        z = [1/6,1/6,1/6,1/6,1/6,1/6]
        x2, y2 = efficient_frontier(stocks, portfolios, time_frame,z,security_type,0.60,0.40)
        x1, y1 = efficient_frontier(stocks, portfolios, time_frame,z,security_type,0.55,0.45)
        test = pd.DataFrame()
        one = np.ones(portfolios)
        zero = np.zeros(portfolios)
        #test["returns"] = np.append(x1,x2)
        #test["risk"] = np.append(y1,y2)
        #test["colors"] = np.append(zero,one)
        plt.plot(y2,x2,label = "60-40")
        plt.plot(y1,x1,label = "55-45")
        plt.legend()
        plt.show()
    else:
        weights = np.random.random(len(stocks))
        weights = [1/len(stocks)] * len(stocks)
        z = weights
        x2, y2 = efficient_frontier(stocks, portfolios, time_frame,z,security_type,0.60,0.40)
        x1, y1 = efficient_frontier(stocks, portfolios, time_frame,z,security_type,0.55,0.45)
        x3, y3 = efficient_frontier(stocks, portfolios, time_frame,z)


        plt.plot(y2,x2,label = "60-40")
        plt.plot(y1,x1,label = "55-45")
        plt.plot(y3,x3,label = "No Constraints")
        plt.legend()
        plt.show()
        

graphit(1000,["TLT","AGG","SHY","XLP","XLE","XOP"],["Bond","Bond","Bond","Stock","Stock","Stock"],"1mo",True)