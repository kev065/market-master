import yfinance as yf
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models import Base, User, Stock, MarketData

date_of_account_creation = datetime(2023, 12, 11)

engine = create_engine('sqlite:///stocks.db', echo=True) 

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Create some users
user1 = User(first_name='John', last_name='Doe', email='john@example.com', date_of_account_creation=date_of_account_creation, profession='Engineer')
user2 = User(first_name='Jane', last_name='Doe', email='jane@example.com', date_of_account_creation=date_of_account_creation, profession='Doctor')

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

    # Check if the keys exist in the dictionary before accessing them
    name = stock_data.get('shortName', 'N/A')
    price = stock_data.get('regularMarketPrice', 0)
    opening_price = stock_data.get('regularMarketOpen', 0)
    closing_price = stock_data.get('regularMarketPreviousClose', 0)

    # Create a new stock instance
    stock = Stock(
        name=name,
        price=price,
        ticker=ticker,
        opening_price=opening_price,
        closing_price=closing_price
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
