<script type="text/javascript"
        src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.0/MathJax.js?config=TeX-AMS_CHTML"></script>
        
# [KellyPortfolio](https://thk3421-models.github.io/KellyPortfolio/)
Thomas Kirschenmann  
thk3421@gmail.com

## Motivation
The goal of this project is to assist an investor by calculating the Kelly optimal portfolio allocation, *conditional on the investor's view of expected returns and covariance* of the assets. It is logical to separate portfolio allocation from the price prediction forecasts.  Everyone has their own view on the difficulty or outright futility of predicting future market prices (active managers vs. strict efficient market hypothesis followers).  Despite these differences, all portfolio managers are required to allocate capital among risky assets.  They are forced to answer the question: "conditional on my views of the future, what is the optimal portfolio allocation that maximizes growth?" 

This project provides the Kelly Portfolio allocation for users with their own views (forecasts) on the expected returns and covariances of future prices.  The user can input their own expected returns in a config file, and the code will download historical prices from Yahoo! Finance, calculate the covariance of daily returns, and then calculate the Kelly portfolio.  Importantly, the code assumes that the historical covariance matrix is representative of the future covariance matrix.  As an option, the user can use historical returns as the expectation of future returns, and see how that changes the Kelly Portfolio.  See the Usage section for detail on how to set up the config file.    

The intended usage of this program is to view the Kelly Portfolio for the securities under consideration, and then consider biasing the real allocations toward the Kelly percentages in hopes of increasing the long term growth rate.  Careful consideration should be applied because the results are widely known to be extremely sensitive to errors in the estimated return rates, and approximately 20 times more sensitive than to errors in the covariance matrix.  Clearly, this is for informational purposes only and not intended as a sole-guide to portfolio allocation. Additionally, please see the discussion below for risk-return discussion around using fractional Kelly to slightly reduce expected growth while dramatically reducing the expected variance.

This is primarily inspired by the fantastic collection of academic papers in:     
![](http://www.edwardothorp.com/wp-content/uploads/2016/11/kelly-capital-growth-investment-criterion-420x634.jpg)

## Historical Background
The Kelly Criterion was invented by Claude Shannon and popularized by Ed Thorp who used it to successfully optimize his wager sizes for gambling games that offered a positive expected value.  The Kelly Criterion is the optimal fraction of total wealth to wager on an individual positive expected value bet such that the expected logarithm of total wealth after repeated wagers is maximized.  Smaller than optimal bet sizes lead to smaller wins which do not compound as quickly, whereas larger than optimal bet sizes suffer from an increased risk of ruin.  For more details on the Kelly Criterion, see [https://en.wikipedia.org/wiki/Kelly_criterion](https://en.wikipedia.org/wiki/Kelly_criterion)

Ed Thorp would later extend the mathematics of the Kelly Criterion to handle multiple correlated positive expected value bets, i.e. a portfolio of stocks.  The fraction of wealth allocated to each asset is known as the Kelly Portfolio which optimizes the long term compound growth rate of total wealth.  Thorp used the Kelly Portfolio to produce 20% annualized returns over 28 years at his asset management firm, Princeton-Newport Partners, wagering over $80 billion during those years with an average of 100 simultaneous bets of $65,000.  Legendary investors Bill Gross and Warren Buffett have also reportedly used Kelly optimal methods for portfolio management.  There is no free lunch of course; investors will always struggle to find investments that are positive expected value with as little variance as possible.  However, *given the expected returns and expected covariance*, there is an allocation that maximizes the long term growth rate, i.e. the Kelly Portfolio.  

Many investors instead choose to allocate such that the mean/covariance of the returns is maximal.  This is implicitly a one-period optimization, whereas the Kelly portfolio optimizes the multi-period compounded rate of return.  The Mean-Variance Optimal portfolio was popularized by Markowitz and would later earn him the Nobel prize.  Under certain conditions and an investor's choice of utility function, the Kelly portfolio allocation and the Constant Relative Risk Aversion (CRRA) allocations are identical.  An excellent discussion and comparison of the two porfolio allocation strategies was written up by a quant group at PIMCO [here](https://www.pimco.com/handlers/displaydocument.ashx?fn=PIMCO_QRA_Baz_Guo_Oct2017.pdf&id=zdVcShqiEMNUg7uf5lz9gz/fdtpZAxKCLsuDGmVqEEL9K6VxjAwuETyKmVNZSF6m%2BcwmMMY724kVAjVehk1ya6fz3ELNCiDJbrNwMbtWtozAkjCDLNE6JnGRN4SvPkXrkfMXXWZ/G9JbK0YT7CTnR/cjuIae6UxSAOryZ9paMv43z9Pw8Gj%2BLuiecPrLww1GSf9Bg8QJS6U2TKYW3hVWzNnBiL8bJqdyQdpq1Iq9DaHVgZrBy9mDO9%2BdvQPj92C%2Bl0MhLO5N5cPnVMJS%2Bb0wu6v9BG3xxstLvA97HCuTXcABp7JfFBOYW7d9P3Z%2BWJ%2BNmEKPHJ6a8ri4nTG1ukQhiWfHc4nGkiJXce%2B8yhNEIAIHD%2B72bje2mUtwwHGN6J55650cijqBM3Bnfmx6I2MFpd64vnSIJo3KkRU1DKzU9JmtjcmpidVQeKtlw0uMaUEx)

Regardless of the portfolio allocation strategy an investory employs, it is worthwhile and interesting to know how it deviates from the Kelly optimal allocation.  This tool provides that information, and a portfolio manager is free to use it however he pleases.  Likely usage would be to view the Kelly Portfolio for the stocks under consideration, and then bias his allocations towards the Kelly allocation percentages in hopes of increasing the long term growth rate.

## Mathematical Definition
The Kelly Portfolio is defined through an optimization problem which optimizes the long term compound growth rate of total wealth, or equivalently (see literature refs <add here>) the log of the total expected wealth.  For a set of correlated assets S_k, a risk-free bond with interest rate r_f, the vector of expected returns for each asset r_k, then the vector of portfolio weights $$u^* = [u_1, \ldots, u_n]$$ given by:
$$u^* = \arg\max_u \mathbb{E}\left[ \ln \left ( (1 + r_f) + \sum_{k=1}^n u_k(r_k - r_f) \right ) \right]$$
is the Kelly Portfolio.  The expectation can be rewritten using a Taylor series expansion as:
$$u^* = \arg\max_u \mathbb{E}\left[\ln(1+r_f) + \sum_{k=1}^{n} \frac{u_k(r_k -r_f)}{1+r_f} - \frac{1}{2}\sum_{k=1}^{n}\sum_{j=1}^{n}u_k u_j \frac{(r_k-r_f)(r_j-r_f)}{(1+r_f)^2} \right]$$
which is written more compactly using the usual matrix, covariance notation:
$$u^* = \arg\max_u E \left[\ln(1+r_f) + \frac{1}{1+r_f}(r - r_f)^T u - \frac{1}{2(1+r_f)^2}u^T \Sigma u \right]$$
This is a straight forward quadratic optimization, which can be solved using a convex optimization package (I used cvxopt).  There are constraints to consider however, such as whether to allow short-selling or leverage.  In this program, I've enforced the long-only constraint and disallowed any leverage, i.e. $$u_k >= 0  \hspace{2cm} \sum_{k=1}^{n} u_k = 1$$ which is the most widely applicable situation for non-institutional investors.   
        
In the case of no constraints, there is an analytical solution: $$u^* = (1+r_f) \Sigma^{-1}(r-r_f)$$  
which will often have both positive and negative weights indicating short sales, and will have no restriction on the total leverage.  

The Kelly Portfolio tends to concentrate allocations among fewer securities and is generally considered too risky.  Practitioners mitigate the risk of Kelly betting by wagering a fraction, typically 1/5 to 1/2, of the fully Kelly allocation and put the rest of the cash into a risk-free asset such as short term treasuries.  The reduced wager size leads to a slower growth rate but is compensated by a reduced risk of ruin.  The reduction in expected return and expected variance is not linear!  In simulations, 1/4 Kelly approximately reduces the expected return by 20% but reduces the variance by a whopping 80%!  The math outlined above is trivially modified to accommodate a fractional Kelly portfolio by simply scaling the total capital by the Kelly fraction and then allocating the appropriate percentages.  The code in this project takes a user's input choice of Kelly fraction from the config file and handles everything automatically. 

## Installation
<pre>
There are a few required modules to ensure are installed first.  
Pop open a terminal and run this command:    
        pip install argparse datetime json sys numpy pandas yfinance cvxopt   
To install the code, simply clone the repo by running this command:    
        git clone https://github.com/thk3421-models/KellyPortfolio.git      
</pre>
## Configuration
The user must specify several self-explanatory items in the configuration file using the JSON format.  Most importantly, the user can input their expected annual returns for each security. Capital is the total cash amount to be allocated and kelly_fraction is the percentage of the fully Kelly portfolio to allocate.  The symbols used must be valid Yahoo! Finance symbols.  Max_lookback_years is the number of years of daily data requested from Yahoo!.  The max_position_size is optional, and should be used with care because imposing a position size constraint can dramatically change the result, effectively nullyfing the optimality of the Kelly criterion.  

The position_sizes element is optional, and is only used if the user wants to invert the problem and see what the implied annual-return values are *given* then position_sizes.  The identical_annual_excess_return_rate is optional, and is used if the user wishes to apply the same return rate to all securities and simply let the covariance matrix determine the optimization results.

<pre>
A sample config file looks like this:   
{  
    "assets":  
    {   
        "stock_symbols": ["SPY", "TLT", "XOM", "AAPL"],  
        "crypto_symbols": ["BTC-USD", "ETH-USD"]  
    },  
    "kelly_fraction": 0.15,  
    "max_lookback_years": 5,  
    "annual_risk_free_rate": 0.008,  
    "identical_annual_excess_return_rate": 0.03,  
    "expected_annual_excess_return_rates": {  
        "SPY": 0.05,  
        "TLT": 0.02,  
        "XOM": 0.03,  
        "AAPL": 0.07,  
        "BTC-USD": 0.07,  
        "ETH-USD": 0.07  
    },  
    "max_position_size", 0.99,
    "capital": 1000000,  
    "position_sizes": {  
        "SPY": 0.40,  
        "TLT": 0.20,  
        "XOM": 0.10,  
        "AAPL": 0.15,  
        "BTC-USD": 0.10,  
        "ETH-USD": 0.05   
    }  
}  
</pre>
## Options, Usage, and Example Output
<pre>
The progam is run in the usual way and the options are specified in the cmd line.  
        (required) --config           path to config.json    
        (required) --estimation_mode  custom, historical, identical 
                                      custom uses the user-specified return rates from the config file
                                      historical uses the historical mean return rate for each security
                                      identical uses same return rate for all securities (specified in config file)
        (optional) --price_data       path to alternative price data CSV instead of using Yahoo! Finance (see code to ensure same column headers)   
        (optional) --implied          True or False.  Program will calculate implied returns based on user-input allocations from config file  
</pre>
A simple example using AAPL, SPY, TLT, XOM, BTC-USD, and ETH-USD:
<pre>
python kelly.py --config config.json --estimation_mode custom

Downloading adjusted daily close data from Yahoo! Finance   
[*********************100%***********************]  6 of 6 completed  
Condition number of annualized covariance matrix is: 217.06317751637496  
****************************************************************************************************  
         Annualized Excess Returns  
AAPL                          0.07  
BTC-USD                       0.07  
ETH-USD                       0.07  
SPY                           0.05  
TLT                           0.02  
XOM                           0.03  
****************************************************************************************************  
Estimated Correlation Matrix of Annualized Excess Returns (rounded to 2 decimal places)  
         AAPL  BTC-USD  ETH-USD   SPY   TLT   XOM  
AAPL     1.00     0.12     0.12  0.76 -0.30  0.43  
BTC-USD  0.12     1.00     0.51  0.15 -0.03  0.12  
ETH-USD  0.12     0.51     1.00  0.14 -0.01  0.11   
SPY      0.76     0.15     0.14  1.00 -0.41  0.70  
TLT     -0.30    -0.03    -0.01 -0.41  1.00 -0.35  
XOM      0.43     0.12     0.11  0.70 -0.35  1.00  
****************************************************************************************************  
Unconstrained Kelly Weights (no constraints on shorting or leverage)  
         Weights  Capital_Allocation  
AAPL        0.14           142747.62  
BTC-USD     0.08            83347.47  
ETH-USD    -0.02           -15931.34  
SPY         2.30          2295577.46  
TLT         2.20          2200074.94  
XOM        -0.40          -400766.44  
Cash: -3305050.0  
****************************************************************************************************  
Begin optimization  
     pcost       dcost       gap    pres   dres  
 0: -1.7847e-02 -1.0474e+00  1e+00  1e-16  3e+00  
 1: -1.9991e-02 -5.4564e-02  3e-02  5e-17  1e-01  
 2: -2.8018e-02 -3.2738e-02  5e-03  4e-17  2e-17  
 3: -2.9596e-02 -2.9967e-02  4e-04  6e-17  8e-18  
 4: -2.9719e-02 -2.9751e-02  3e-05  2e-16  2e-17  
 5: -2.9738e-02 -2.9741e-02  4e-06  1e-16  3e-17  
 6: -2.9740e-02 -2.9741e-02  1e-07  8e-17  1e-17  
 7: -2.9741e-02 -2.9741e-02  1e-09  6e-17  8e-18  
Optimal solution found.  
****************************************************************************************************  
Allocation With Full Kelly Weights  
         Weights  Capital_Allocation  
AAPL        0.39           386897.09  
BTC-USD     0.06            57991.59  
ETH-USD     0.00                0.43  
SPY         0.33           326538.36  
TLT         0.23           228572.53  
XOM         0.00                0.00  
Cash: 0.0  
****************************************************************************************************  
Allocation With Partial Kelly Fraction:0.15  
         Weights  Capital_Allocation  
AAPL        0.06            58034.56  
BTC-USD     0.01             8698.74  
ETH-USD     0.00                0.06  
SPY         0.05            48980.75  
TLT         0.03            34285.88  
XOM         0.00                0.00  
Cash: 850000.0  
****************************************************************************************************  
</pre>
