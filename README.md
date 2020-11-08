<script type="text/javascript"
        src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.0/MathJax.js?config=TeX-AMS_CHTML"></script>
        
# [KellyPortfolio](https://thk3421-models.github.io/KellyPortfolio/)

## Motivation
The goal of this project is to assist an investor by calculating the Kelly optimal portfolio allocation, *conditional on the investor's view of expected returns and covariance* of the assets. It is logical to separate portfolio allocation from the price prediction forecasts.  Everyone has their own view on the difficulty or outright futility of predicting future market prices (active managers vs. strict efficient market hypothesis followers).  Despite these differences, all portfolio managers are required to allocate capital among risky assets.  They are forced to answer the question: "conditional on my views of the future, what is the optimal portfolio allocation that maximizes growth?" 

This project provides the Kelly Portfolio allocation for users with their own views (forecasts) on the expected returns and covariances of future prices.  The user can input their own expected returns in a config file, and the code will download historical prices from Yahoo! Finance, calculate the covariance of daily returns, and then calculate the Kelly portfolio.  Importantly, the code assumes that the historical covariance matrix is representative of the future covariance matrix.  As an option, the user can use historical returns as the expectation of future returns, and see how that changes the Kelly Portfolio.  See the Usage section for detail on how to set up the config file.    

## Historical Background
The Kelly Criterion was invented by Claude Shannon and popularized by Ed Thorp who used it to successfully optimize his wager sizes for gambling games that offered a positive expected value.  The Kelly Criterion is the optimal fraction of total wealth to wager on an individual positive expected value bet such that the expected logarithm of total wealth after repeated wagers is maximized.  Smaller than optimal bet sizes lead to smaller wins which do not compound as quickly, whereas larger than optimal bet sizes suffer from an increased risk of ruin.  For more details on the Kelly Criterion, see https://en.wikipedia.org/wiki/Kelly_criterion(https://en.wikipedia.org/wiki/Kelly_criterion)

Ed Thorp would later extend the mathematics of the Kelly Criterion to handle multiple correlated positive expected value bets, i.e. a portfolio of stocks.  The fraction of wealth allocated to each asset is known as the Kelly Portfolio which optimizes the long term compound growth rate of total wealth.  Thorp used the Kelly Portfolio to produce 20% annualized returns over 28 years at his asset management firm, Princeton-Newport Partners, wagering over $80 billion during those years with an average of 100 simultaneous bets of $65,000.  Legendary investors Bill Gross and Warren Buffett have also reportedly used Kelly optimal methods for portfolio management.  There is no free lunch of course; investors will always struggle to find investments that are positive expected value with as little variance as possible.  However, *given the expected returns and expected covariance*, there is an allocation that maximizes the long term growth rate, i.e. the Kelly Portfolio.  

Many investors instead of choose to allocate the portfolio such that the mean/covariance of the returns is maximal.  This is implicitly a one-period optimization, whereas the Kelly portfolio optimizes the multi-period compounded rate of return.  The Mean-Variance Optimal portfolio was popularized by Markowitz and would later earn him the Nobel prize.  Under certain conditions and an investor's choice of utility function, the Kelly portfolio allocation and the Constant Relative Risk Aversion (CRRA) allocations are identical.  An excellent discussion and comparison of the two porfolio allocation strategies was written up by the quants at PIMCO [here](https://www.pimco.com/handlers/displaydocument.ashx?fn=PIMCO_QRA_Baz_Guo_Oct2017.pdf&id=zdVcShqiEMNUg7uf5lz9gz/fdtpZAxKCLsuDGmVqEEL9K6VxjAwuETyKmVNZSF6m%2BcwmMMY724kVAjVehk1ya6fz3ELNCiDJbrNwMbtWtozAkjCDLNE6JnGRN4SvPkXrkfMXXWZ/G9JbK0YT7CTnR/cjuIae6UxSAOryZ9paMv43z9Pw8Gj%2BLuiecPrLww1GSf9Bg8QJS6U2TKYW3hVWzNnBiL8bJqdyQdpq1Iq9DaHVgZrBy9mDO9%2BdvQPj92C%2Bl0MhLO5N5cPnVMJS%2Bb0wu6v9BG3xxstLvA97HCuTXcABp7JfFBOYW7d9P3Z%2BWJ%2BNmEKPHJ6a8ri4nTG1ukQhiWfHc4nGkiJXce%2B8yhNEIAIHD%2B72bje2mUtwwHGN6J55650cijqBM3Bnfmx6I2MFpd64vnSIJo3KkRU1DKzU9JmtjcmpidVQeKtlw0uMaUEx)

Regardless of the portfolio allocation strategy an investory employs, it is worthwhile and interesting to know how it deviates from the Kelly optimal allocation.  This tool provides that information, and a portfolio manager is free to use it however he pleases to bias his allocations in hopes of increasing the long term growth rate.

## Mathematical Definition
The Kelly Portfolio is defined through an optimization problem which optimizes the long term compound growth rate of total wealth, or equivalently (see literature refs <add here>) the log of the total expected wealth.  For a set of correlated assets $$S_k$$, a risk-free bond with interest rate $$r_f$$, the vector of expected returns for each asset $$r_k$$, then the vector of portfolio weights $$u^* = [u_1, \ldots, u_n]$$ given by:
$$u^* = \arg\max_u \mathbb{E}\left[ \ln(1 + r_f) + \sum_{k=1}^n u_k(r_k - r_f) \right]$$
is the Kelly Portfolio.  The expectation can be rewritten using a Taylor series expansion as:
$$u^* = \arg\max_u \mathbb{E}\left[\ln(1+r_f) + \sum_{k=1}^{n} \frac{u_k(r_k -r_f)}{1+r} - \frac{1}{2}\sum_{k=1}^{n}\sum_{j=1}^{n}u_k u_j \frac{(r_k-r_f)(r_j-r_f)}{(1+r_f)^2} \right]$$
which is written more compactly using the usual matrix, covariance notation:
$$u^* = \arg\max_u \mathbb{E}\left[\ln(1+r_f) + \frac{1}{1+r}((r - r_f)^T u - \frac{1}{2(1+r_f)^2)}u^T \Sigma \u}\right]$$
        

The Kelly Portfolio tends to concentrate allocations among fewer securities and is generally considered too risky.  Practitioners mitigate the risk of Kelly betting by wagering a fraction, typically 1/5 to 1/2, of the fully Kelly allocation and put the rest of the cash into a risk-free asset such as short term treasuries.  The reduced wager size leads to a slower growth rate but is compensated by a reduced risk of ruin.  

## Installation

## Configuration

## Usage



