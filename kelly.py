import argparse
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
    return ann_covar

def kelly_optimize(M, C):
    results = np.linalg.inv(C) @ M
    kelly = pd.DataFrame(results.values, index=C.columns, columns=['Weights'])
    return kelly

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
        import pdb
        pdb.set_trace()
        
    kelly_weights = kelly_optimize(mu.transpose(), covar)
    print('Kelly Weights')
    print(kelly_weights)
    import pdb
    pdb.set_trace()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', action="store")
    parser.add_argument('--price_data', action="store")
    parser.add_argument('--estimation_mode', action="store")
    options = parser.parse_args()
    main()
