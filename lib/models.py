from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    date_of_account_creation = Column(DateTime)
    profession = Column(String)
    market_data = relationship('MarketData', back_populates='user')
    stocks = relationship('Stock', secondary='market_data')

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
    price = Column(Integer)
    ticker = Column(String)
    opening_price = Column(Float)
    closing_price = Column(Float)
    market_data = relationship('MarketData', back_populates='stock')

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
    rating = Column(Integer)
    user = relationship('User', back_populates='market_data')
    stock = relationship('Stock', back_populates='market_data')

    def full_market_data(self):
        return f"Market Data for {self.stock.name} by {self.user.full_name()}: {self.rating} stars."