#!/usr/bin/env python
# coding: utf-8

# # Financial Planning with APIs and Simulations
# 
# In this Challenge, you’ll create two financial analysis tools by using a single Jupyter notebook:
# 
# Part 1: A financial planner for emergencies. The members will be able to use this tool to visualize their current savings. The members can then determine if they have enough reserves for an emergency fund.
# 
# Part 2: A financial planner for retirement. This tool will forecast the performance of their retirement portfolio in 30 years. To do this, the tool will make an Alpaca API call via the Alpaca SDK to get historical price data for use in Monte Carlo simulations.
# 
# You’ll use the information from the Monte Carlo simulation to answer questions about the portfolio in your Jupyter notebook.
# 
# 

# In[ ]:


# Import the required libraries and dependencies
import os
import requests
import json
import pandas as pd
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi
from MCForecastTools import MCSimulation
import datetime;

get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


# Ignore miscellaneous warnings from Jupiter Lab that clutter up the output (e.g. future methods that will be deprecated)
import warnings
warnings.filterwarnings('ignore')


# In[ ]:


# Load the environment variables from the .env file
#by calling the load_dotenv function
load_dotenv('api.env')


# ## Part 1: Create a Financial Planner for Emergencies

# ### Evaluate the Cryptocurrency Wallet by Using the Requests Library
# 
# In this section, you’ll determine the current value of a member’s cryptocurrency wallet. You’ll collect the current prices for the Bitcoin and Ethereum cryptocurrencies by using the Python Requests library. For the prototype, you’ll assume that the member holds the 1.2 Bitcoins (BTC) and 5.3 Ethereum coins (ETH). To do all this, complete the following steps:
# 
# 1. Create a variable named `monthly_income`, and set its value to `12000`.
# 
# 2. Use the Requests library to get the current price (in US dollars) of Bitcoin (BTC) and Ethereum (ETH) by using the API endpoints that the starter code supplies.
# 
# 3. Navigate the JSON response object to access the current price of each coin, and store each in a variable.
# 
#     > **Hint** Note the specific identifier for each cryptocurrency in the API JSON response. The Bitcoin identifier is `1`, and the Ethereum identifier is `1027`.
# 
# 4. Calculate the value, in US dollars, of the current amount of each cryptocurrency and of the entire cryptocurrency wallet.
# 
# 

# In[ ]:


# The current number of coins for each cryptocurrency asset held in the portfolio.
btc_coins = 1.2
eth_coins = 5.3


# #### Step 1: Create a variable named `monthly_income`, and set its value to `12000`.

# In[ ]:


# The monthly amount for the member's household income
monthly_income = 12000


# #### Review the endpoint URLs for the API calls to Free Crypto API in order to get the current pricing information for both BTC and ETH.

# In[ ]:


# The Free Crypto API Call endpoint URLs for the held cryptocurrency assets
btc_url = "https://api.alternative.me/v2/ticker/Bitcoin/?convert=USD"
eth_url = "https://api.alternative.me/v2/ticker/Ethereum/?convert=USD"


# #### Step 2. Use the Requests library to get the current price (in US dollars) of Bitcoin (BTC) and Ethereum (ETH) by using the API endpoints that the starter code supplied.

# In[ ]:


# Using the Python requests library, make an API call to access the current price of BTC
btc_response = requests.get(btc_url).json()

# Use the json.dumps function to review the response data from the API call
# Use the indent and sort_keys parameters to make the response object readable
print(json.dumps(btc_response, indent=4, sort_keys=True))


# In[ ]:


# Using the Python requests library, make an API call to access the current price ETH
eth_response = requests.get(eth_url).json()

# Use the json.dumps function to review the response data from the API call
# Use the indent and sort_keys parameters to make the response object readable
print(json.dumps(eth_response, indent=4, sort_keys=True))


# #### Step 3: Navigate the JSON response object to access the current price of each coin, and store each in a variable.

# In[ ]:


# Navigate the BTC response object to access the current price of BTC
btc_price = btc_response['data']['1']['quotes']['USD']['price']

# Print the current price of BTC
print(f"The price for BTC is ${btc_price}")


# In[ ]:


# Navigate the BTC response object to access the current price of ETH
eth_price = eth_response['data']['1027']['quotes']['USD']['price']

# Print the current price of ETH
print(f"The price for ETH is ${eth_price}")


# ### Step 4: Calculate the value, in US dollars, of the current amount of each cryptocurrency and of the entire cryptocurrency wallet.

# In[ ]:


# Compute the current value of the BTC holding 
btc_value = btc_price * btc_coins

# Print current value of your holding in BTC
print(f"The current value of the {btc_coins} BTC coins is ${btc_value:0.2f}")


# In[ ]:


# Compute the current value of the ETH holding 
eth_value = eth_price * eth_coins

# Print current value of your holding in ETH
print(f"The current value of the {eth_coins} ETH coins is ${eth_value:0.2f}")


# In[ ]:


# Compute the total value of the cryptocurrency wallet
# Add the value of the BTC holding to the value of the ETH holding
total_crypto_wallet = btc_value + eth_value

# Print current cryptocurrency wallet balance
print(f"The current value of the crypto wallet is ${total_crypto_wallet:0.2f}")


# ### Evaluate the Stock and Bond Holdings by Using the Alpaca SDK
# 
# In this section, you’ll determine the current value of a member’s stock and bond holdings. You’ll make an API call to Alpaca via the Alpaca SDK to get the current closing prices of the SPDR S&P 500 ETF Trust (ticker: SPY) and of the iShares Core US Aggregate Bond ETF (ticker: AGG). For the prototype, assume that the member holds 110 shares of SPY, which represents the stock portion of their portfolio, and 200 shares of AGG, which represents the bond portion. To do all this, complete the following steps:
# 
# 1. In the `Starter_Code` folder, create an environment file (`.env`) to store the values of your Alpaca API key and Alpaca secret key.
# 
# 2. Set the variables for the Alpaca API and secret keys. Using the Alpaca SDK, create the Alpaca `tradeapi.REST` object. In this object, include the parameters for the Alpaca API key, the secret key, and the version number.
# 
# 3. Set the following parameters for the Alpaca API call:
# 
#     - `tickers`: Use the tickers for the member’s stock and bond holdings.
# 
#     - `timeframe`: Use a time frame of one day.
# 
#     - `start_date` and `end_date`: Use the same date for these parameters, and format them with the date of the previous weekday (or `2020-08-07`). This is because you want the one closing price for the most-recent trading day.
# 
# 4. Get the current closing prices for `SPY` and `AGG` by using the Alpaca `get_bars` function. Format the response as a Pandas DataFrame by including the `df` property at the end of the `get_bars` function.
# 
# 5. Navigating the Alpaca response DataFrame, select the `SPY` and `AGG` closing prices, and store them as variables.
# 
# 6. Calculate the value, in US dollars, of the current amount of shares in each of the stock and bond portions of the portfolio, and print the results.
# 

# #### Review the total number of shares held in both (SPY) and (AGG).

# In[ ]:


# Current amount of shares held in both the stock (SPY) and bond (AGG) portion of the portfolio.
spy_shares = 110
agg_shares = 200


# #### Step 1: In the `Starter_Code` folder, create an environment file (`.env`) to store the values of your Alpaca API key and Alpaca secret key.

# #### Step 2: Set the variables for the Alpaca API and secret keys. Using the Alpaca SDK, create the Alpaca `tradeapi.REST` object. In this object, include the parameters for the Alpaca API key, the secret key, and the version number.

# In[ ]:


# Set the variables for the Alpaca API and secret keys
alpaca_api_key = os.getenv("ALPACA_API_KEY")
alpaca_secret_key = os.getenv("ALPACA_SECRET_KEY")

# Check the values were imported correctly by evaluating the type of each
display(type(alpaca_api_key))
display(type(alpaca_secret_key))
        
# Create the Alpaca tradeapi.REST object
alpaca = tradeapi.REST(
    alpaca_api_key,
    alpaca_secret_key,
    api_version="v2")


# #### Step 3: Set the following parameters for the Alpaca API call:
# 
# - `tickers`: Use the tickers for the member’s stock and bond holdings.
# 
# - `timeframe`: Use a time frame of one day.
# 
# - `start_date` and `end_date`: Use the same date for these parameters, and format them with the date of the previous weekday (or `2020-08-07`). This is because you want the one closing price for the most-recent trading day.
# 

# In[ ]:


# Set the tickers for both the bond and stock portion of the portfolio
tickers = ["SPY", "AGG"]

# Set timeframe to 1Day
timeframe = "1Day"

# Get the last/previous business day
# ... first, get current date
curent_date_time = pd.Timestamp(datetime.datetime.now())
# ... second, determine offset in days to get to last business day
# ... (e.g. on Sat - offset = 1, on Sun - offset = 2)
offset = pd.tseries.offsets.BusinessDay(n=1)
# ... third, subtract offset from current date to get to previous business date
prev_bizday_date_time = curent_date_time - offset
# ... fourth, remove time (to get only date) and convert to ISO format (returns str)
prev_bizday_date = prev_bizday_date_time.date().isoformat()

# Format current date as ISO format
# Set both the start and end date at the date of your prior weekday 
# This will give you the closing price of the previous trading day
# Alternatively you can use a start and end date of 2020-08-07
start_date = pd.Timestamp(str(prev_bizday_date), tz="America/New_York").isoformat()
end_date = pd.Timestamp(str(prev_bizday_date), tz="America/New_York").isoformat()

display(start_date)
display(end_date)


# #### Step 4: Get the current closing prices for `SPY` and `AGG` by using the Alpaca `get_bars` function. Format the response as a Pandas DataFrame by including the `df` property at the end of the `get_bars` function.

# In[ ]:


# Method 1: Separating and concatenating each ticker separately

# Use the Alpaca get_bars function to get current closing prices the portfolio
# Be sure to set the `df` property after the function to format the response object as a DataFrame
df_portfolio = alpaca.get_bars(
    tickers,
    timeframe,
    start = start_date,
    end = end_date
).df

# Reorganize the DataFrame
# Separate ticker data
SPY = df_portfolio[df_portfolio['symbol']=='SPY'].drop('symbol', axis=1)
AGG = df_portfolio[df_portfolio['symbol']=='AGG'].drop('symbol', axis=1)

# Concatenate the ticker DataFrames
df_portfolio_separate = pd.concat([SPY,AGG],axis=1, keys=['SPY','AGG'])

# Review the first 5 rows of the Alpaca DataFrame
display(df_portfolio_separate)


# In[ ]:


# Method 2: A more generic way to get current closing prices of the portfolio with the symbols in ticker list
# (i.e. by iterating over the symbols in the ticket list)

# Create an empty list to hold the DataFrame of prices for each ticker
ticker_df_list = []

# Iterate over each ticker symbol in the tickers list
for ticker in tickers:
    # Reorganize the DataFrame
    ticker_df = df_portfolio[df_portfolio['symbol']==ticker].drop('symbol', axis=1)    
    # Append the DataFrame to the list
    ticker_df_list.append(ticker_df)
    
# Concatenate the ticker DataFrames
df_portfolio = pd.concat(ticker_df_list,axis=1, keys=tickers)

# Review the first 5 rows of the Alpaca DataFrame
display(df_portfolio)


# #### Step 5: Navigating the Alpaca response DataFrame, select the `SPY` and `AGG` closing prices, and store them as variables.

# In[ ]:


# Access the closing price for AGG from the Alpaca DataFrame
# Converting the value to a floating point number
agg_close_price_srs = df_portfolio["AGG"]["close"]
agg_close_price = agg_close_price_srs[0]

# Print the AGG closing price
display(f"The current price of AGG is ${agg_close_price:0.2f}")


# In[ ]:


# Access the closing price for SPY from the Alpaca DataFrame
# Converting the value to a floating point number
spy_close_price_srs = df_portfolio["SPY"]["close"]
spy_close_price = spy_close_price_srs[0]

# Print the SPY closing price
display(f"The current price of SPY is ${spy_close_price:0.2f}")


# #### Step 6: Calculate the value, in US dollars, of the current amount of shares in each of the stock and bond portions of the portfolio, and print the results.

# In[ ]:


# Calculate the current value of the bond portion of the portfolio
agg_value = agg_close_price * agg_shares

# Print the current value of the bond portfolio
print(f"The current value of the {agg_shares} AGG shares is ${agg_value:0.2f}")


# In[ ]:


# Calculate the current value of the stock portion of the portfolio
spy_value = spy_close_price * spy_shares

# Print the current value of the stock portfolio
print(f"The current value of the {spy_shares} SPY shares is ${spy_value:0.2f}")


# In[ ]:


# Calculate the total value of the stock and bond portion of the portfolio
total_stocks_bonds = agg_value + spy_value

# Print the current balance of the stock and bond portion of the portfolio
print(f"The current value of the stock and bond portfolio is ${total_stocks_bonds:0.2f}")


# In[ ]:


# Calculate the total value of the member's entire savings portfolio
# Add the value of the cryptocurrency walled to the value of the total stocks and bonds
total_portfolio = total_crypto_wallet + total_stocks_bonds

# Print current cryptocurrency wallet balance
print(f"The current value of the entire savings portfolio is ${total_portfolio:0.2f}")


# ### Evaluate the Emergency Fund
# 
# In this section, you’ll use the valuations for the cryptocurrency wallet and for the stock and bond portions of the portfolio to determine if the credit union member has enough savings to build an emergency fund into their financial plan. To do this, complete the following steps:
# 
# 1. Create a Python list named `savings_data` that has two elements. The first element contains the total value of the cryptocurrency wallet. The second element contains the total value of the stock and bond portions of the portfolio.
# 
# 2. Use the `savings_data` list to create a Pandas DataFrame named `savings_df`, and then display this DataFrame. The function to create the DataFrame should take the following three parameters:
# 
#     - `savings_data`: Use the list that you just created.
# 
#     - `columns`: Set this parameter equal to a Python list with a single value called `amount`.
# 
#     - `index`: Set this parameter equal to a Python list with the values of `crypto` and `stock/bond`.
# 
# 3. Use the `savings_df` DataFrame to plot a pie chart that visualizes the composition of the member’s portfolio. The y-axis of the pie chart uses `amount`. Be sure to add a title.
# 
# 4. Using Python, determine if the current portfolio has enough to create an emergency fund as part of the member’s financial plan. Ideally, an emergency fund should equal to three times the member’s monthly income. To do this, implement the following steps:
# 
#     1. Create a variable named `emergency_fund_value`, and set it equal to three times the value of the member’s `monthly_income` of $12000. (You set this earlier in Part 1).
# 
#     2. Create a series of three if statements to determine if the member’s total portfolio is large enough to fund the emergency portfolio:
# 
#         1. If the total portfolio value is greater than the emergency fund value, display a message congratulating the member for having enough money in this fund.
# 
#         2. Else if the total portfolio value is equal to the emergency fund value, display a message congratulating the member on reaching this important financial goal.
# 
#         3. Else the total portfolio is less than the emergency fund value, so display a message showing how many dollars away the member is from reaching the goal. (Subtract the total portfolio value from the emergency fund value.)
# 

# #### Step 1: Create a Python list named `savings_data` that has two elements. The first element contains the total value of the cryptocurrency wallet. The second element contains the total value of the stock and bond portions of the portfolio.

# In[ ]:


# Consolidate financial assets data into a Python list
savings_data = [total_crypto_wallet, total_stocks_bonds]

# Review the Python list savings_data
display(savings_data)    


# #### Step 2: Use the `savings_data` list to create a Pandas DataFrame named `savings_df`, and then display this DataFrame. The function to create the DataFrame should take the following three parameters:
# 
# - `savings_data`: Use the list that you just created.
# 
# - `columns`: Set this parameter equal to a Python list with a single value called `amount`.
# 
# - `index`: Set this parameter equal to a Python list with the values of `crypto` and `stock/bond`.
# 

# In[ ]:


# Create a Pandas DataFrame called savings_df 
savings_df = pd.DataFrame(savings_data, columns=["amount"], index=["crypto", "stock/bond"])

# Display the savings_df DataFrame
display(savings_df)


# #### Step 3: Use the `savings_df` DataFrame to plot a pie chart that visualizes the composition of the member’s portfolio. The y-axis of the pie chart uses `amount`. Be sure to add a title.

# In[ ]:


# Plot the total value of the member's portfolio (crypto and stock/bond) in a pie chart
savings_df.plot.pie(y='amount', title='Portfolio Composition - Crytpo & Stock/Bond')


# #### Step 4: Using Python, determine if the current portfolio has enough to create an emergency fund as part of the member’s financial plan. Ideally, an emergency fund should equal to three times the member’s monthly income. To do this, implement the following steps:
# 
# Step 1. Create a variable named `emergency_fund_value`, and set it equal to three times the value of the member’s `monthly_income` of 12000. (You set this earlier in Part 1).
# 
# Step 2. Create a series of three if statements to determine if the member’s total portfolio is large enough to fund the emergency portfolio:
# 
# * If the total portfolio value is greater than the emergency fund value, display a message congratulating the member for having enough money in this fund.
# 
# * Else if the total portfolio value is equal to the emergency fund value, display a message congratulating the member on reaching this important financial goal.
# 
# * Else the total portfolio is less than the emergency fund value, so display a message showing how many dollars away the member is from reaching the goal. (Subtract the total portfolio value from the emergency fund value.)
# 

# ##### Step 4-1: Create a variable named `emergency_fund_value`, and set it equal to three times the value of the member’s `monthly_income` of 12000. (You set this earlier in Part 1).

# In[ ]:


# Create a variable named emergency_fund_value
emergency_fund_value = 3 * monthly_income


# ##### Step 4-2: Create a series of three if statements to determine if the member’s total portfolio is large enough to fund the emergency portfolio:
# 
# * If the total portfolio value is greater than the emergency fund value, display a message congratulating the member for having enough money in this fund.
# 
# * Else if the total portfolio value is equal to the emergency fund value, display a message congratulating the member on reaching this important financial goal.
# 
# * Else the total portfolio is less than the emergency fund value, so display a message showing how many dollars away the member is from reaching the goal. (Subtract the total portfolio value from the emergency fund value.)

# In[ ]:


# Evaluate the possibility of creating an emergency fund with 3 conditions:

print()
print("Summary:")
print("--------")
print(f"The current value of the entire savings portfolio is ${total_portfolio:0.2f}")
print(f"Required emergency fund is ${emergency_fund_value:0.2f}")
print("--------")

if (total_portfolio > emergency_fund_value):
    print("Congratulations!  You have enough funds in your portfolio to fund your emergency portfolio")  
elif (total_portfolio == emergency_fund_value):
    print("Congratulations, you have reached enough funds in your portfolio to match your emergency portfolio")  
else:
    print(f"Unfortunately, you do not have enough funds in your portfolio to fund your emergency portfolio.  You will need an additional ${(emergency_fund_value - total_portfolio):.2f}")  
print("--------")
print()


# ## Part 2: Create a Financial Planner for Retirement

# ### Create the Monte Carlo Simulation
# 
# In this section, you’ll use the MCForecastTools library to create a Monte Carlo simulation for the member’s savings portfolio. To do this, complete the following steps:
# 
# 1. Make an API call via the Alpaca SDK to get 3 years of historical closing prices for a traditional 60/40 portfolio split: 60% stocks (SPY) and 40% bonds (AGG).
# 
# 2. Run a Monte Carlo simulation of 500 samples and 30 years for the 60/40 portfolio, and then plot the results.The following image shows the overlay line plot resulting from a simulation with these characteristics. However, because a random number generator is used to run each live Monte Carlo simulation, your image will differ slightly from this exact image:
# 
# ![A screenshot depicts the resulting plot.](Images/5-4-monte-carlo-line-plot.png)
# 
# 3. Plot the probability distribution of the Monte Carlo simulation. Plot the probability distribution of the Monte Carlo simulation. The following image shows the histogram plot resulting from a simulation with these characteristics. However, because a random number generator is used to run each live Monte Carlo simulation, your image will differ slightly from this exact image:
# 
# ![A screenshot depicts the histogram plot.](Images/5-4-monte-carlo-histogram.png)
# 
# 4. Generate the summary statistics for the Monte Carlo simulation.
# 
# 

# #### Step 1: Make an API call via the Alpaca SDK to get 3 years of historical closing prices for a traditional 60/40 portfolio split: 60% stocks (SPY) and 40% bonds (AGG).

# In[ ]:


# Set start and end dates of 3 years back from your current date
# Alternatively, you can use an end date of 2020-08-07 and work 3 years back from that date 

# Determine end date
# ... from earlier in the challenge above, have already defined the current data/time ("curent_date_time = pd.Timestamp(datetime.datetime.now())")
# ... offset -1 day
end_date_time = curent_date_time - datetime.timedelta(days = 1)
# Determine start date 
# ... minus 3 years (3 * 365 days) from current/end date
start_date_time = end_date_time - datetime.timedelta(days = (3 * 365))
# Remove time (to get only date) and convert to ISO format (returns str)
start_date = start_date_time.date().isoformat()
end_date = end_date_time.date().isoformat()

display(type(start_date))
display(type(end_date))
print(f"start_date = {start_date}")
print(f"end_date = {end_date}")


# In[ ]:


# Use the Alpaca get_bars function to make the API call to get the 3 years worth of pricing data
# The tickers and timeframe parameters should have been set in Part 1 of this activity 
# The start and end dates should be updated with the information set above
# Remember to add the df property to the end of the call so the response is returned as a DataFrame

portfolio_prices_df = alpaca.get_bars(
    tickers,
    timeframe,
    start = start_date,
    end = end_date
).df


# Method 1: Separating and concatenating each ticker separately

# Reorganize the DataFrame
# Separate ticker data
SPY = portfolio_prices_df[portfolio_prices_df['symbol']=='SPY'].drop('symbol', axis=1)
AGG = portfolio_prices_df[portfolio_prices_df['symbol']=='AGG'].drop('symbol', axis=1)

# Concatenate the ticker DataFrames
df_portfolio_df_separate = pd.concat([SPY,AGG],axis=1, keys=['SPY','AGG'])

# Display both the first and last five rows of the DataFrame
print("Method 1")
display(df_portfolio_df_separate.head())
display(df_portfolio_df_separate.tail())
print()

# Method 2: A more generic way to get current closing prices of the portfolio with the symbols in ticker list
# (i.e. by iterating over the symbols in the ticket list)

# Create an empty list to hold the DataFrame of prices for each ticker
ticker_df_list = []

# Iterate over each ticker symbol in the tickers list
for ticker in tickers:
    # Reorganize the DataFrame
    ticker_df = portfolio_prices_df[portfolio_prices_df['symbol']==ticker].drop('symbol', axis=1)    
    # Append the DataFrame to the list
    ticker_df_list.append(ticker_df)
    
# Concatenate the ticker DataFrames
portfolio_prices_df = pd.concat(ticker_df_list,axis=1, keys=tickers)

# Review the first 5 rows of the Alpaca DataFrame
print("Method 2")
display(portfolio_prices_df.head())
display(portfolio_prices_df.tail())
print()


# #### Step 2: Run a Monte Carlo simulation of 500 samples and 30 years for the 60/40 portfolio, and then plot the results.

# In[ ]:


# Configure the Monte Carlo simulation to forecast 30 years cumulative returns
# The weights should be split 40% to AGG and 60% to SPY.
# Run 500 samples.
MC_60stock_40bond_30yr_weight = MCSimulation(
    portfolio_data = portfolio_prices_df,
    weights = [.60,.40],
    num_simulation = 500,
    num_trading_days = 252*30
)

# Review the simulation input data
MC_60stock_40bond_30yr_weight.portfolio_data.head()


# In[ ]:


# Run the Monte Carlo simulation to forecast 30 years cumulative returns
MC_60stock_40bond_30yr_weight.calc_cumulative_return()


# In[ ]:


# Visualize the 30-year Monte Carlo simulation by creating an
# overlay line plot
line_plot_60stock_40bond_30yr_plot = MC_60stock_40bond_30yr_weight.plot_simulation()


# In[ ]:


line_plot_60stock_40bond_30yr_plot.get_figure().savefig('Images/line_plot_60stock_40bond_30yr_plot.png', bbox_inches = 'tight')


# #### Step 3: Plot the probability distribution of the Monte Carlo simulation.

# In[ ]:


# Visualize the probability distribution of the 30-year Monte Carlo simulation 
# by plotting a histogram
distribution_plot_60stock_40bond_30yr_plot = MC_60stock_40bond_30yr_weight.plot_distribution()


# In[ ]:


distribution_plot_60stock_40bond_30yr_plot.get_figure().savefig('Images/distribution_plot_60stock_40bond_30yr_plot.png', bbox_inches = 'tight')


# #### Step 4: Generate the summary statistics for the Monte Carlo simulation.

# In[ ]:


# Generate summary statistics from the 30-year Monte Carlo simulation results
# Save the results as a variable
table_60stock_40bond_30yr_weight = MC_60stock_40bond_30yr_weight.summarize_cumulative_return()


# Review the 30-year Monte Carlo summary statistics
print(table_60stock_40bond_30yr_weight)


# ### Analyze the Retirement Portfolio Forecasts
# 
# Using the current value of only the stock and bond portion of the member's portfolio and the summary statistics that you generated from the Monte Carlo simulation, answer the following question in your Jupyter notebook:
# 
# -  What are the lower and upper bounds for the expected value of the portfolio with a 95% confidence interval?
# 

# In[ ]:


# Print the current balance of the stock and bond portion of the members portfolio
print(f"The current value of the stock and bond portfolio is ${total_stocks_bonds:0.2f}")


# In[ ]:


# Use the lower and upper `95%` confidence intervals to calculate the range of the possible outcomes for the current stock/bond portfolio

ci_lower_95per = table_60stock_40bond_30yr_weight[8]
ci_upper_95per = table_60stock_40bond_30yr_weight[9]

ci_lower_thirty_cumulative_return = round(ci_lower_95per * total_stocks_bonds, 2)
ci_upper_thirty_cumulative_return = round(ci_upper_95per * total_stocks_bonds, 2)

# Print the result of your calculations
print()
print(f"There is a 95% chance that the current stock and bond portfolio value of ${total_stocks_bonds:0.2f},"
      f" invested in 60% stocks and 40% bonds over the next 30 years will end within the range of"
      f" ${ci_lower_thirty_cumulative_return:0.2f} and ${ci_upper_thirty_cumulative_return:0.2f}.")


# ### Forecast Cumulative Returns in 10 Years
# 
# The CTO of the credit union is impressed with your work on these planning tools but wonders if 30 years is a long time to wait until retirement. So, your next task is to adjust the retirement portfolio and run a new Monte Carlo simulation to find out if the changes will allow members to retire earlier.
# 
# For this new Monte Carlo simulation, do the following: 
# 
# - Forecast the cumulative returns for 10 years from now. Because of the shortened investment horizon (30 years to 10 years), the portfolio needs to invest more heavily in the riskier asset&mdash;that is, stock&mdash;to help accumulate wealth for retirement. 
# 
# - Adjust the weights of the retirement portfolio so that the composition for the Monte Carlo simulation consists of 20% bonds and 80% stocks. 
# 
# - Run the simulation over 500 samples, and use the same data that the API call to Alpaca generated.
# 
# - Based on the new Monte Carlo simulation, answer the following questions in your Jupyter notebook:
# 
#     - Using the current value of only the stock and bond portion of the member's portfolio and the summary statistics that you generated from the new Monte Carlo simulation, what are the lower and upper bounds for the expected value of the portfolio (with the new weights) with a 95% confidence interval?
# 
#     - Will weighting the portfolio more heavily toward stocks allow the credit union members to retire after only 10 years?
# 

# In[ ]:


# Configure a Monte Carlo simulation to forecast 10 years cumulative returns
# The weights should be split 20% to AGG and 80% to SPY.
# Run 500 samples.
MC_80stock_20bond_10yr_weight = MCSimulation(
    portfolio_data = portfolio_prices_df,
    weights = [.80,.20],
    num_simulation = 500,
    num_trading_days = 252*10
)

# Review the simulation input data
MC_80stock_20bond_10yr_weight.portfolio_data.head()


# In[ ]:


# Run the Monte Carlo simulation to forecast 10 years cumulative returns
MC_80stock_20bond_10yr_weight.calc_cumulative_return()


# In[ ]:


# Visualize the 10-year Monte Carlo simulation by creating an
# overlay line plot
line_plot_80stock_20bond_10yr_plot = MC_80stock_20bond_10yr_weight.plot_simulation()


# In[ ]:


line_plot_80stock_20bond_10yr_plot.get_figure().savefig('Images/line_plot_80stock_20bond_10yr_plot.png', bbox_inches = 'tight')


# In[ ]:


# Visualize the probability distribution of the 10-year Monte Carlo simulation 
# by plotting a histogram
distribution_plot_80stock_20bond_10yr_plot = MC_80stock_20bond_10yr_weight.plot_distribution()


# In[ ]:


distribution_plot_80stock_20bond_10yr_plot.get_figure().savefig('Images/distribution_plot_80stock_20bond_10yr_plot.png', bbox_inches = 'tight')


# In[ ]:


# Generate summary statistics from the 10-year Monte Carlo simulation results
# Save the results as a variable
table_80stock_20bond_10yr_weight = MC_80stock_20bond_10yr_weight.summarize_cumulative_return()


# Review the 10-year Monte Carlo summary statistics
print(table_80stock_20bond_10yr_weight)


# ### Answer the following questions:

# #### Question: Using the current value of only the stock and bond portion of the member's portfolio and the summary statistics that you generated from the new Monte Carlo simulation, what are the lower and upper bounds for the expected value of the portfolio (with the new weights) with a 95% confidence interval?

# In[ ]:


# Print the current balance of the stock and bond portion of the members portfolio
print(f"The current value of the stock and bond portfolio is ${total_stocks_bonds:0.2f}")


# In[ ]:


# Use the lower and upper `95%` confidence intervals to calculate the range of the possible outcomes for the current stock/bond portfolio

ci_lower_95per = table_80stock_20bond_10yr_weight[8]
ci_upper_95per = table_80stock_20bond_10yr_weight[9]

ci_lower_thirty_cumulative_return = round(ci_lower_95per * total_stocks_bonds, 2)
ci_upper_thirty_cumulative_return = round(ci_upper_95per * total_stocks_bonds, 2)

# Print the result of your calculations
print()
print(f"There is a 95% chance that the current stock and bond portfolio value of ${total_stocks_bonds:0.2f},"
      f" invested in 80% stocks and 20% bonds over the next 10 years will end within the range of"
      f" ${ci_lower_thirty_cumulative_return:0.2f} and ${ci_upper_thirty_cumulative_return:0.2f}.")


# #### Question: Will weighting the portfolio more heavily to stocks allow the credit union members to retire after only 10 years?
**Answer** Well, this will really depend on the individual and his requirements.  Interestingly, the lower bound of both investment strategies are approximately the same.  However, the upper bound is more significant/higher in the 60%/40% stocks to bond ratio over 30 years with a value of $769,892.88 versus less than half of this value in the 80%/20% stocks to bond ratio invested over 10 years with a value of $307,191.38.  So in my opinion, the answer would be no, weighting the portfolio more heavily to stocks will not allow the credit union member to retire after only 10 years

*** NOTE, the numbers shown above do change with every new run of the MC simulation, as expected, it generates the probabiblity of the returns over the next 30 and 10 years, respectively.  However, the numbers are still close enough to each other to make the same informed decision - again, as expected ***
# In[ ]:




