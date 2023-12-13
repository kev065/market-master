from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Table, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum
from datetime import datetime, timedelta

Base = declarative_base()

# Defines the Rating Enum
class Rating(enum.Enum):
    STRONG_SELL = '1'
    UNDERPERFORM = '2'
    HOLD = '3'
    OUTPERFORM = '4'
    STRONG_BUY = '5'

user_stock_association = Table('user_stock', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('stock_id', Integer, ForeignKey('stocks.id')),
    Column('date_added', DateTime)
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    date_of_account_creation = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(hours=3))
    profession = Column(String)
    username = Column(String)
    password = Column(String)

    market_data = relationship('MarketData', back_populates='user')
    stocks = relationship('Stock', secondary=user_stock_association, back_populates='users')

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def favorite_stock(self):
        return max(self.stocks, key=lambda stock: stock.rating)

    def add_market_data(self, stock, rating):
        new_market_data = MarketData(stock_id=stock.id, user_id=self.id, rating=rating)
        self.market_data.append(new_market_data)

    def delete_market_data(self, stock):
        self.market_data = [data for data in self.market_data if data.stock_id != stock.id]

class Stock(Base):
    __tablename__ = 'stocks'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    ticker = Column(String)
    opening_price = Column(Float)
    closing_price = Column(Float)
    moving_average_90d = Column(Float, name='90-D MA')
    market_data = relationship('MarketData', back_populates='stock')
    users = relationship('User', secondary=user_stock_association, back_populates='stocks')

    @classmethod
    def highest_price(cls):
        return session.query(cls).order_by(cls.price.desc()).first()

    def all_market_data(self):
        return [f"Market Data for {self.name} by {data.user.full_name()}: {data.rating} stars." for data in self.market_data]

class MarketData(Base):
    __tablename__ = 'market_data'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    stock_id = Column(Integer, ForeignKey('stocks.id'))
    rating = Column(Enum(Rating))
    comment = Column(String)
    user = relationship('User', back_populates='market_data')
    stock = relationship('Stock', back_populates='market_data')

    def full_market_data(self):
        return f"Market Data for {self.stock.name} by {self.user.full_name()}: {self.rating.name}. Comment: {self.comment}"
