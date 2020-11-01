import argparse
from cvxopt import matrix
from cvxopt.solvers import qp
import datetime
import json
import numpy as np
import pandas as pd
import sys
import yfinance

def load_config(path):
    with open(path) as config_file:
        data = json.load(config_file)
    return data

def load_prices(config):
    if options.price_data is not None:
        try:
            #Expects a CSV with Date column and Symbol names for the price columns, i.e. Date, AAPL, GOOGL
            price_data = pd.read_csv(options.price_data, parse_dates=['Date'])
            price_data.set_index(['Date'], inplace=True)
        except:
            print('Error loading local price data from:', options.price_data)
            sys.exit(-1)
    else:
        stock_symbols, crypto_symbols = [],[]
        start_date = (datetime.datetime.today() - datetime.timedelta(days=365*config['max_lookback_years'])).date()
        end_date   = datetime.datetime.today().date() - datetime.timedelta(days=1)
        try:
            if 'stock_symbols' in config['assets'].keys():
                stock_symbols = config['assets']['stock_symbols']
            if 'crypto_symbols' in config['assets'].keys():
                crypto_symbols = config['assets']['crypto_symbols']
            symbols = sorted(stock_symbols + crypto_symbols)
        except:
            print('Error retrieving symbols from config file. Config file should be formatted in JSON such that \
                   config[\'assets\'][\'stock_symbols\'] is valid. See example config file from GitHub')
            sys.exit(-1)
        if len(symbols) > 0:
            print('Downloading adjusted daily close data from Yahoo! Finance')
            try:
                price_data = yfinance.download(symbols, start=str(start_date), end=str(end_date), 
                                                interval='1d', auto_adjust=True, threads=True)
            except:
                print('Error downloading data from Yahoo! Finance')
                sys.exit(-1)
            cols = [('Close', x) for x in symbols]
            price_data = price_data[cols]
            price_data.columns = price_data.columns.get_level_values(1)
            price_data.to_csv('sample_data.csv', header=True)
    price_data = price_data.sort_index()
    return price_data

def annual_excess_returns(prices, config):
    #Stock data only changes on weekdays. Crypto data is available all days. 
    #Compute daily returns using Friday to Monday returns for all data
    returns = prices[prices.index.dayofweek < 5].pct_change(1)
    excess_returns = returns - config['annual_risk_free_rate'] / 252
    return returns

def annual_covar(excess_returns):    
    ann_covar = excess_returns.cov() * 252
    print('Condition number of annualized covariance matrix is:', np.linalg.cond(ann_covar))
    try:
        eigvals, eigvecs = np.linalg.eig(ann_covar)
    except:
        print('Error in Eigen decomposition of covariance matrix')
        eigvals = []
        pass
    if min(eigvals) <= 0:
        print('Error!  Negative eigenvalues in covariance matrix detected!')
        sys.exit(-1)
    return ann_covar

def kelly_optimize_normal(M, C):
    results = np.linalg.inv(C) @ M
    kelly = pd.DataFrame(results.values, index=C.columns, columns=['Weights'])
    return kelly

def kelly_optimize(M_df, C_df, config):
    #objective function to maximize is: g(F) = r + F^T(M-R) - F^TCF/2 
    r = config['annual_risk_free_rate']
    M = M_df.to_numpy()
    C = C_df.to_numpy()

    n = M.shape[0]
    A = matrix(1.0, (1,n))
    b = matrix(1.0)
    G = matrix(0.0, (n,n))
    G[::n+1] = -1.0
    if config['allow_short_selling'] == 'True':
        h = matrix(9999999999999.0, (n,1))
    else:
        h = matrix(0.0, (n,1))
    S = matrix((1.0 / ((1 + r) ** 2)) * C)
    q = matrix((1.0 / (1 + r)) * (M - r))
    sol = qp(S, -q, G, h, A, b)
    kelly = np.array([sol['x'][i] for i in range(n)])
    kelly = pd.DataFrame(kelly, index=C_df.columns, columns=['Weights'])
    return kelly

def display_results(df, config, msg):
    df['Capital_Allocation'] = df['Weights'] * config['capital']
    print(msg)
    print(df.round(2))
    cash = config['capital'] - df['Capital_Allocation'].sum()
    print('Cash:', np.round(cash))
    print('*'*100)

def kelly_implied(covar, config):
    #mu = C*F*
    F = pd.DataFrame.from_dict(config['position_sizes'], orient='index').transpose()
    F = F[covar.columns]
    implied_mu = covar @ F.transpose()
    implied_mu.columns = ['implied_return_rate']
    return implied_mu

def main():
    config  = load_config(options.config)
    prices  = load_prices(config)
    excess_returns = annual_excess_returns(prices, config)
    covar = annual_covar(excess_returns)
    mu = pd.DataFrame(columns=covar.columns)
    if options.estimation_mode == 'identical':
        rate  = config['identical_annual_excess_return_rate']
        mu.loc[0] = rate
    elif options.estimation_mode == 'historical':
        mu.loc[0] = excess_returns.mean()*252
    elif options.estimation_mode == 'custom':
        rates = config['expected_annual_excess_return_rates']
        mu = pd.DataFrame.from_dict(rates, orient='index').transpose()
    mu = mu[covar.columns]

    if options.implied is not None and options.implied.upper() == 'TRUE':
        implied_returns = kelly_implied(covar, config)
        print('*'*100)
        print(implied_returns.round(2))
        return 0
    print('*'*100)
    ann_excess_returns = mu.transpose()
    ann_excess_returns.columns = ['Annualized Excess Returns']
    print(ann_excess_returns)
    print('*'*100)
    print('Estimated Covariance Matrix of Annualized Excess Returns (rounded to 2 decimal places)')
    print(covar.round(2))
    print('*'*100)
    gbm_kelly_weights = kelly_optimize_normal(mu.transpose(), covar)
    display_results(gbm_kelly_weights, config, 'GBM Kelly Weights')
    print('Begin optimization')
    kelly_weights = kelly_optimize(mu.transpose(), covar, config)
    print('*'*100)
    display_results(kelly_weights, config, 'Allocation With Full Kelly Weights')
    for kelly_fraction in reversed([0.15, 0.25, 0.333, 0.4, 0.5]):
        partial_kelly = kelly_fraction*kelly_weights
        display_results(partial_kelly, config, 'Allocation With Partial Kelly Fraction:'+str(kelly_fraction))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', action="store")
    parser.add_argument('--price_data', action="store")
    parser.add_argument('--implied', action="store")
    parser.add_argument('--estimation_mode', action="store")
    options = parser.parse_args()
    main()
