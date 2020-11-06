# [KellyPortfolio](https://thk3421-models.github.io/KellyPortfolio/)

## Motivation
The idea motivating this project is to separate portfolio allocation from the price prediction forecasts.  Everyone has their own view on the difficulty or outright futility of predicting future market prices (active managers vs. strict efficient market hypothesis followers).  Despite these differences, all portfolio managers are required to allocate capital among risky assets.  They are forced to answer the question: "conditional on my views of the future, what is the optimal portfolio allocation that maximizes growth?" 

The goal of this project is to provide the Kelly Portfolio allocation for users with their own views on the expected returns and covariances of future prices.  The user can input their own expected returns in a config file, and the code will download historical prices from Yahoo! Finance, calculate the covariance of daily returns, and then calculate the Kelly portfolio.  Importantly, the code assumes that the historical covariance matrix is representative of the future covariance matrix.  As an option, the user can use historical returns as the expectation of future returns, and see how that changes the Kelly Portfolio.    

## Historical Background
The Kelly Criterion was invented by Claude Shannon and popularized by Ed Thorp who used it to successfully optimize his wager sizes for gambling games that offered a positive expected value.  The Kelly Criterion is the fraction of total wealth to wager on an individual positive expected value bet such that the expected logarithm of total wealth after repeated wagers is maximized.  Smaller bet sizes lead to wins which do not compound as quickly, and larger bet sizes suffer from an increased risk of ruin.  For more details on the Kelly Criterion, see https://en.wikipedia.org/wiki/Kelly_criterion(https://en.wikipedia.org/wiki/Kelly_criterion)

Ed Thorp would later extend the mathematics of the Kelly Criterion to handle multiple correlated positive expected value bets, i.e. a portfolio of stocks.  The fraction of wealth allocated to each asset is known as the Kelly Portfolio which optimizes the long term compound growth rate of total wealth.  Thorp used the Kelly Portfolio to produce 20% annualized returns over 28 years at his asset management firm, Princeton-Newport Partners, wagering over $80 billion during those years with an average of 100 simultaneous bets of $65,000.  Legendary investors Bill Gross and Warren Buffett have also reportedly used Kelly optimal methods for portfolio management.

## Mathematical Definition
The Kelly Portfolio is defined through an optimization problem which optimizes the long term compound growth rate of total wealth.  It tends to concentrate allocations among fewer securities and is generally considered too risky.  Practitioners mitigate the risk of Kelly betting by wagering a fraction, typically 1/5 to 1/2, of the fully Kelly allocation and put the rest of the cash into a risk-free asset such as short term treasuries.  The reduced wager size leads to a slower growth rate but is compensated by a reduced risk of ruin.  

## Installation

## Configuration

## Usage



