import click
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, User, Stock
import yfinance as yf

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

    user = User(first_name=first_name, last_name=last_name, email=email, profession=profession)
    session.add(user)
    session.commit()

    click.echo(f'User {first_name} {last_name} created successfully!')

@click.command()
def check_stock():
    ticker = click.prompt('Please enter the ticker of the stock')

    stock_info = yf.Ticker(ticker)
    stock_data = stock_info.info

    avg_daily_volume = stock_data.get('averageDailyVolume10Day')
    market_cap = stock_data.get('marketCap')
    price = stock_data.get('regularMarketPrice')

    click.echo(f'Average Daily Volume: {avg_daily_volume}')
    click.echo(f'Market Cap: {market_cap}')
    click.echo(f'Price: {price}')

cli.add_command(create_user)
cli.add_command(check_stock)

if __name__ == '__main__':
    cli()
