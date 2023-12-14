import click
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, insert
from models import Base, User, Stock, MarketData, user_stock_association
import yfinance as yf
import pprint
from datetime import datetime


engine = create_engine('sqlite:///stocks.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

@click.group()
def cli():
    pass

@click.command()
def create_user():
    first_name = click.prompt('Please enter your first name')
    last_name = click.prompt('Please enter your last name')
    email = click.prompt('Please enter your email')
    profession = click.prompt('Please enter your profession')
    username = click.prompt('Please enter your preferred username')
    password = click.prompt('Please enter your preferred password') 

    user = User(first_name=first_name, last_name=last_name, email=email, profession=profession, username=username, password=password)
    session.add(user)
    session.commit()

    tickers = click.prompt('Please enter the tickers of the stocks you want to add to your watchlist, separated by commas')
    tickers = [ticker.strip() for ticker in tickers.split(',')]

    for ticker in tickers:
        stock = session.query(Stock).filter_by(ticker=ticker).first()
        if stock is not None:
            insert_stmt = insert(user_stock_association).values(user_id=user.id, stock_id=stock.id, date_added=datetime.now())
            session.execute(insert_stmt)

    session.commit()

    click.echo(f'User {username} created successfully!')

@click.command()
@click.argument('user_id', type=int)  # Adds a click argument for user_id
def check_stock(user_id):
    user = session.query(User).filter_by(id=user_id).first()

    ticker = click.prompt('Please enter the ticker of the stock that you want to analyze')

    stock_info = yf.Ticker(ticker)
    stock_data = stock_info.info

    pprint.pprint(stock_data)

    avg_daily_volume = stock_data.get('averageDailyVolume10Day')
    market_cap = stock_data.get('marketCap')
    price = stock_data.get('regularMarketPrice')
    open_price = stock_data.get('regularMarketOpen')
    day_high = stock_data.get('dayHigh')
    day_low = stock_data.get('dayLow')
    ninety_day_avg = stock_data.get('average90Vol')
    pe_ratio = stock_data.get('trailingPE')
    fifty_two_week_high = stock_data.get('fiftyTwoWeekHigh')
    fifty_two_week_low = stock_data.get('fiftyTwoWeekLow')
    five_year_change = stock_data.get('fiveYearAvgDividendYield')

    click.echo(f'Average Daily Volume: {avg_daily_volume}')
    click.echo(f'Market Cap: {market_cap}')
    click.echo(f'Price: {price}')
    click.echo(f'Opening Price: {open_price}')
    click.echo(f'Highest Price of the Day: {day_high}')
    click.echo(f'Lowest Price of the Day: {day_low}')
    click.echo(f'90 Day Average: {ninety_day_avg}')
    click.echo(f'Price to Earnings Ratio: {pe_ratio}')
    click.echo(f'52 Week High: {fifty_two_week_high}')
    click.echo(f'52 Week Low: {fifty_two_week_low}')
    click.echo(f'5 Year Change: {five_year_change}')

    if click.confirm('Would you like to leave a rating and comment on this stock\'s performance?'):
        rating = click.prompt('Please enter your rating', type=click.Choice(['STRONG SELL', 'UNDERPERFORM', 'HOLD', 'OUTPERFORM', 'STRONG BUY'], case_sensitive=False))
        comment_text = click.prompt('Please enter your comment')

        # Assign the retrieved stock
        stock = session.query(Stock).filter_by(ticker=ticker).first()

        # Update the comment and rating association only if the stock exists
        if stock:
            market_data = session.query(MarketData).filter_by(user_id=user.id, stock_id=stock.id).first()
            
            # If market_data doesn't exist, create a new MarketData object
            if market_data is None:
                market_data = MarketData(user_id=user.id, stock_id=stock.id)
                session.add(market_data)

            market_data.comment = comment_text
            market_data.rating = rating  # Set the rating
            session.commit()

        click.echo(f'Your rating and comment have been saved!')

@click.command()
def view_best_worst_stocks():
    # Define the tickers of the 30 stocks in the DJIA
    tickers = ['MMM', 'AXP', 'AAPL', 'BA', 'CAT', 'CVX', 'CSCO', 'KO', 'DOW', 'XOM', 'GS', 'HD', 'IBM', 'INTC', 'JNJ', 'JPM', 'MCD', 'MRK', 'MSFT', 'NKE', 'PFE', 'PG', 'TRV', 'UNH', 'RTX', 'VZ', 'V', 'WBA', 'WMT', 'DIS']

    # Fetch the data for each ticker
    data = yf.download(tickers, period='1d')

    # Calculate the daily returns for each ticker
    returns = data['Adj Close'].pct_change()

    # Find the best and worst performing stocks
    best_stock = returns.idxmax()
    worst_stock = returns.idxmin()

    click.echo(f'Best performing stock: {best_stock}')
    click.echo(f'Worst performing stock: {worst_stock}\n')

cli.add_command(create_user)
cli.add_command(check_stock)
cli.add_command(view_best_worst_stocks)

if __name__ == '__main__':
    cli()
