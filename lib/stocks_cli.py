import click
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, User, Stock
import yfinance as yf
import pprint

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
            user.stocks.append(stock)

    session.commit()

    click.echo(f'User {username} created successfully!')

@click.command()
def check_stock():
    ticker = click.prompt('Please enter the ticker of the stock')

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

cli.add_command(create_user)
cli.add_command(check_stock)

if __name__ == '__main__':
    cli()
