import yfinance as yf
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models import Base, User, Stock, MarketData, user_stock_association, Rating
import random

date_of_account_creation = datetime(2023, 12, 11)

engine = create_engine('sqlite:///stocks.db', echo=True) 

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Clear the database before each new seed
session.execute(user_stock_association.delete())
session.query(MarketData).delete()
session.query(User).delete()
session.query(Stock).delete()
session.commit()

# Create some users
user1 = User(first_name='John', last_name='Deere', email='john@gmail.com', date_of_account_creation=date_of_account_creation, profession='Engineer')
user2 = User(first_name='Jane', last_name='Dawg', email='inher@live.com', date_of_account_creation=date_of_account_creation, profession='Doctor')

# Add and commit the users
session.add(user1)
session.add(user2)
session.commit()

# List of stock tickers to fetch data for
tickers = ['AAPL', 'MSFT', 'GOOGL', 'MMM', 'AXP', 'AMGN', 'BA', 'CAT', 'CVX', 'CSCO', 'KO', 'DOW', 'GS', 'HD', 'HON', 'IBM', 'INTC', 'JNJ', 'JPM', 'MCD', 'MRK', 'MSFT', 'NKE', 'PG', 'CRM', 'TRV', 'UNH', 'VZ', 'V', 'WBA', 'WMT', 'DIS']

# List of comments
comments = ['Great performance!', 'Good potential.', 'Steady growth.', 'Impressive returns.', 'Strong buy.', 'Outperforming the market.', 'Could do better.', 'Not meeting expectations.', 'Showing promise.', 'A safe bet.', 'I live off the dividends paid by this stock.', 'God bless the executives and employees of this company.']

for ticker in tickers:
    # Fetching stock data using yfinance 
    stock_info = yf.Ticker(ticker)
    stock_data = stock_info.info

    # Fetch historical market data for the past 90 days
    history = stock_info.history(period='90d')

    # Calculate the 90-day moving average from the closing prices
    moving_average_90d = history['Close'].mean()

    # Check if the keys exist in the dictionary before accessing them
    name = stock_data.get('shortName', 'N/A')
    opening_price = stock_data.get('regularMarketOpen', 0)
    closing_price = stock_data.get('regularMarketPreviousClose', 0)

    # Create a new stock instance
    stock = Stock(
        name=name,
        moving_average_90d=moving_average_90d,
        ticker=ticker,
        opening_price=opening_price,
        closing_price=closing_price
    )

    # Add and commit the stock
    session.add(stock)
    session.commit()

    # Add stock to user's watchlist
    user1.stocks.append(stock)
    user2.stocks.append(stock)

    # Set the date_added column in the user_stock association table
    insert_stmt = insert(user_stock_association).values(user_id=user1.id, stock_id=stock.id, date_added=datetime.now())
    session.execute(insert_stmt)
    insert_stmt = insert(user_stock_association).values(user_id=user2.id, stock_id=stock.id, date_added=datetime.now())
    session.execute(insert_stmt)

    # Creates some market data with comments
    market_data1 = MarketData(user=user1, stock=stock, rating=Rating.STRONG_BUY, comment=random.choice(comments))
    market_data2 = MarketData(user=user2, stock=stock, rating=Rating.OUTPERFORM, comment=random.choice(comments))

    # Add and commit the market data
    session.add(market_data1)
    session.add(market_data2)
    session.commit()
