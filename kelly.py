import argparse
import datetime
import json
import pandas as pd
import sys
import yfinance

def load_config(path):
    with open(path) as config_file:
        data = json.load(config_file)
    return data

def load_prices(config):
    if args.price_data is not None:
        try:
            """Expects a CSV with Date column and Symbol names for the price columns, i.e. Date, AAPL, GOOGL"""
            price_data = pd.read_csv(args.price_data, parse_dates=['Date'])
            price_data.set_index(['Date'], inplace=True)
        except:
            print('Error loading local price data from:', args.price_data)
            sys.exit(-1)
    else:
        symbols = []
        start_date = (datetime.datetime.today() - datetime.timedelta(days=365*config['max_lookback_years'])).date()
        end_date   = datetime.datetime.today().date()
        try:
            symbols = sorted(set(config['assets']['yahoo_finance_symbols']))
        except KeyError:
            print('No symbols found in config file. Config file should be formatted in JSON such that \
                   config[\'assets\'][\'yahoo_finance_symbols\'] is valid. See example config file from GitHub')
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
    return price_data

def main():
    config = load_config(args.config)
    prices = load_prices(config)
    import pdb
    pdb.set_trace()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', action="store")
    parser.add_argument('--price_data', action="store")
    args = parser.parse_args()
    main()
