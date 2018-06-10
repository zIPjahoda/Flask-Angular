# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""All the database related entities are in this module."""
import datetime

from flask import Flask
from flask_login import UserMixin
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_security import RoleMixin, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship

from backend.flask_app.lib import AlchemyEncoder

engine = create_engine('mysql+pymysql://kokot@localhost:3307/cryptofund', pool_size=20, max_overflow=100)

# db.Model = declarative_base()
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()

app = Flask(__name__)
app.config.from_json('config.json')
app.json_encoder = AlchemyEncoder

db = SQLAlchemy(app)
engine = create_engine('mysql+pymysql://kokot@localhost:3307/cryptofund', echo=True)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


class Base(db.Model):
    """Base class for all the tables.
    Consists of two default columns `created_at` and `modified_at` .
    """

    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    modified_at = db.Column(db.DateTime,
                            default=db.func.current_timestamp(),
                            onupdate=db.func.current_timestamp())


roles_users = db.Table('roles_users', db.Column('user_id', db.Integer(),
                                                db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(),
                                 db.ForeignKey('role.id')))


class Coin(db.Model):
    __tablename__ = 'coin'

    id = db.Column(db.Integer, primary_key=True)
    id_name = db.Column(db.String(200))
    name = db.Column(db.String(200))
    symbol = db.Column(db.String(10))
    rank = db.Column(db.Integer)
    price_usd = db.Column(db.Float)  # zavislost na te tabulce
    total_supply = db.Column(db.Integer)
    image_url = db.Column(db.String(500))

    def __init__(self, data):
        self.id_name = str.lower(data['id_name'])
        self.name = data['name']
        self.symbol = str.upper(data['symbol'])
        self.rank = data['rank']
        self.price_usd = data['price_usd']
        self.total_supply = 0
        self.image_url = ''

    def __json__(self):
        return ['name', 'symbol', 'image_url']

    @staticmethod
    def add(data):
        currency = Coin(data)
        session.add(currency)
        session.commit()
        return currency


class TickerCoin(db.Model):
    __tablename__ = 'tickercoin'

    id = db.Column(db.Integer, primary_key=True)
    id_coin = db.Column(db.Integer, db.ForeignKey("coin.id"))
    last_updated = db.Column(db.Integer)
    price_usd = db.Column(db.Float)
    price_btc = db.Column(db.Float)
    market_cap_usd = db.Column(db.BigInteger)
    percent_change_1h = db.Column(db.Float)
    percent_change_6h = db.Column(db.Float)
    percent_change_12h = db.Column(db.Float)
    percent_change_24h = db.Column(db.Float)
    percent_change_7d = db.column(db.Float)

    coin = relationship("Coin", foreign_keys=[id_coin])

    def __init__(self, data):
        self.id_coin = data['id_coin']
        self.last_updated = data['last_updated']
        self.price_usd = data['price_usd']
        self.price_btc = data['price_btc']
        self.market_cap_usd = data['market_cap_usd']
        self.percent_change_1h = data['percent_change_1h']
        self.percent_change_6h = data['percent_change_6h']
        self.percent_change_12h = data['percent_change_12h']
        self.percent_change_24h = data['percent_change_24h']
        self.percent_change_7d = data['percent_change_7d']

    @staticmethod
    def add(data):
        ticker = TickerCoin(data)
        session.add(ticker)
        session.commit()
        return ticker.id


class Exchange(db.Model):
    __tablename__ = 'exchange'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    api_url = db.Column(db.String(255))
    api_key = db.Column(db.String(500))
    api_secret = db.Column(db.String(500))


class ExchangeCoin(db.Model):
    __tablename__ = 'exchangecoin'

    id = db.Column(db.Integer, primary_key=True)
    id_exchange = db.Column(db.Integer, db.ForeignKey("exchange.id"))
    id_coin = db.Column(db.Integer, db.ForeignKey("coin.id"))

    exchange = relationship("Exchange", foreign_keys=[id_exchange])
    coin = relationship("Coin", foreign_keys=[id_coin])

    def __init__(self, data):
        self.id_exchange = data['id_exchange']
        self.id_coin = data['id_coin']

    @staticmethod
    def add(data):
        exchangecoin = ExchangeCoin(data)
        session.add(exchangecoin)
        session.commit()
        return exchangecoin.id


class Wallet(db.Model):
    __tablename__ = 'wallet'

    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey("user.id"))
    id_coin = db.Column(db.Integer, db.ForeignKey("coin.id"))
    id_exchange = db.Column(db.Integer, db.ForeignKey("exchange.id"))
    deposit = db.Column(db.Float)
    address = db.Column(db.String(500), default=None)

    user = relationship("User", foreign_keys=[id_user])

    def __init__(self, data):
        self.id_user = data['id_user']
        self.id_coin = data['id_coin']
        self.id_exchange = data['id_exchange']
        self.deposit = data['deposit']
        self.address = data['address']

    @staticmethod
    def add(data):
        wallet = Wallet(data)
        session.add(wallet)
        session.commit()
        return wallet.id


        # @staticmethod
        # def update(data):
        #     task = Tasks.query.filter_by(id=id).first()
        #     task.comp = True
        #     session.commit()


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    __searchable__ = ['username']

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True)
    email = db.Column(db.String(250), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean(), default=True)
    confirmed_at = db.Column(db.DateTime, default=False)
    phone = db.Column(db.Integer)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    token = db.Column(db.String(550))
    valid_to = db.Column(db.Integer)

    def __init__(self, data):
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.confirmed_at = datetime.datetime.now().time().strftime('%Y-%m-%d %H:%M:%S')
        self.token = data['token']
        self.valid_to = 0

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s',active='%s',)>" % (
            self.username, self.email, self.password, self.active)

    @staticmethod
    def get_user(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def add(data):
        user = User(data)
        session.add(user)
        session.commit()
        return user


class User_exchange(db.Model):
    __tablename__ = 'user_exchange'

    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey("user.id"))
    id_exchange = db.Column(db.Integer, db.ForeignKey("exchange.id"))
    api_secret = db.Column(db.String(255))
    api_key = db.Column(db.String(255))
    enabled = db.Column(db.Boolean, default=True)

    exchange = relationship("Exchange", foreign_keys=[id_exchange])

    def __init__(self, data):
        self.id_user = data['id_user']
        self.id_exchange = data['id_exchange']
        self.api_secret = data['api_secret']
        self.api_key = data['api_key']

    @staticmethod
    def add(data):
        user_exchange = User_exchange(data)
        session.add(user_exchange)
        session.commit()
        return user_exchange.id


class Withdraw(db.Model):
    __tablename__ = 'withdraw'

    id = db.Column(db.Integer, primary_key=True)
    id_exchange = db.Column(db.Integer, db.ForeignKey("exchange.id"))
    id_coin = db.Column(db.Integer, db.ForeignKey("coin.id"))
    avaible = db.Column(db.Float)
    is_online = db.Column(db.Boolean, default=False)
    fess = db.Column(db.Float)


user_datastore = SQLAlchemyUserDatastore(db, User, Role)

if __name__ == '__main__':
    manager.run()
