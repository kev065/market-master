import yfinance as yf
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Stock, MarketData

engine = create_engine('sqlite:///stocks.db') 
Session = sessionmaker(bind=engine)
session = Session()

# Create some users
user1 = User(first_name='John', last_name='Doe', email='john@example.com', date_of_account_creation='2023-12-11', profession='Engineer')
user2 = User(first_name='Jane', last_name='Doe', email='jane@example.com', date_of_account_creation='2023-12-11', profession='Doctor')

# Add and commit the users
session.add(user1)
session.add(user2)
session.commit()

# List of stock tickers to fetch data for
tickers = ['AAPL', 'MSFT', 'GOOGL']

for ticker in tickers:
    # Fetch stock data using yfinance
    stock_info = yf.Ticker(ticker)
    stock_data = stock_info.info

    # Create a new stock instance
    stock = Stock(
        name=stock_data['shortName'],
        price=stock_data['regularMarketPrice'],
        ticker=ticker,
        opening_price=stock_data['regularMarketOpen'],
        closing_price=stock_data['regularMarketPreviousClose']
    )

    # Add and commit the stock
    session.add(stock)
    session.commit()

    # Create some market data
    market_data1 = MarketData(user=user1, stock=stock, rating=5)
    market_data2 = MarketData(user=user2, stock=stock, rating=4)

    # Add and commit the market data
    session.add(market_data1)
    session.add(market_data2)
    session.commit()
