# Market Master - Stock Market Analysis CLI Application

This application provides users with tools to analyze the stock market. It's designed to help users make sense of complex financial data and provide insights into which stocks to buy or sell.

## Features
1. **User Creation and Watchlist**: After creating a new user profile, users are prompted to add stocks to their watchlist. Users can enter the tickers of the stocks they are interested in, and these tickers are stored in the `user_stock` table in the database associated with their user ID and the stock ID.

2. **Stock Checking, Comments and Ratings**: Users can check the current status of a particular stock. They will be prompted to enter the ticker of the stock they want to analyze. The application will fetch the data from the Yahoo Finance API and display various metrics about the stock, such as average daily volume, the market cap, price, opening price, highest price of the day, lowest price of the day, 90-day moving average, price to earnings ratio, 52-week high, 52-week low, and 5-year change.

After viewing a stock, users are prompted to enter a rating and a comment. The rating can be one of five options: ‘STRONG SELL’, ‘UNDERPERFORM’, ‘HOLD’, ‘OUTPERFORM’, or ‘STRONG BUY’. The rating and comment are stored in the `MarketData` table in the database, associated with the user’s ID and the stock’s ID.

3. **Best and Worst Stocks View**: Users can view the best and worst performing days for each individual stock in the **Dow Jones Industrial Average** . The application fetches data for each ticker for the last 5 business days, calculates the daily returns for each ticker, and identifies the best and worst performing days for each stock.

4. **Data Analysis - Stock Metrics View**: Users can view various metrics of a particular stock. The application utilizes the [numpy](https://numpy.org/) library to fetch data for each ticker for the last 5 years, calculates the daily returns for each ticker, and calculates and displays the average returns and volatility for each stock.

## Usage
You will need to have all the Python packages listed in the [Pipfile](https://github.com/kev065/market-master/blob/main/Pipfile) installed in your python environment to run the script.

To launch the application, navigate to the directory containing the Python files in your terminal, and then run the script using this command:
    ```
    python3 stocks_cli.py 
    ```

The application will display a list of options and wait for the user to enter a number corresponding to the option they want to select:

```
Please select an option:
1. Create user
2. Check stock
3. View the best and worst stocks
4. View stock metrics
5. Exit
Please enter a number:
```

For example, if you want to create a user, you would type 1 at the prompt.

### Technologies used 
- [Python](https://www.python.org/)
- [Numpy](https://github.com/numpy/numpy/) - used to perform advanced calculations on the downloaded financial data.
- [yfinance](https://github.com/ranaroussi/yfinance/) - I used this to download current and historical market data from Yahoo Finance.
- [Click](https://github.com/pallets/click/)
- [SQLAlchemy](https://www.sqlalchemy.org/)

### Licence
This project is licenced under the [MIT Licence](https://github.com/kev065/market-master/blob/main/LICENSE/)