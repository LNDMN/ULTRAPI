from datetime import datetime
from pony.orm import *


db = Database()


class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    nickname = Optional(str)
    username = Optional(str)
    user_id = Required(str)
    first_date = Optional(datetime)
    last_date = Optional(datetime)
    limit_level = Required(int, default=0)
    channels = Set('Channel')
    chats = Set('Chat')
    bots = Set('Bot')
    partnerships = Optional('Partnership', reverse='user')
    is_referral_of = Optional('Partnership', reverse='referrals')
    messages = Set('Message')
    tokens = Optional(int)
    wallet = Set('Wallet')
    investment = Optional('Investment')
    is_active = Optional(bool, default=False)
    is_premium = Optional(bool, default=False)
    end_of_premium = Optional(datetime)


class Bot(db.Entity):
    id = PrimaryKey(int, auto=True)
    token = Optional(str)
    name = Optional(str)
    username = Optional(str)
    id_of_bot = Optional(int)
    users = Set(User)
    type_of_bot = Optional(str)
    messages = Set('Message')


class Channel(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    channel_id = Required(str)
    users = Set(User)


class Partnership(db.Entity):
    id = PrimaryKey(int, auto=True)
    user = Required(User, reverse='partnerships')
    referrals = Set(User, reverse='is_referral_of')
    total_referrals = Optional(int)
    total_earned = Optional(str)
    total_invested_by_referrals = Optional(float)


class Wallet(db.Entity):
    id = PrimaryKey(int, auto=True)
    user = Required(User)
    balance = Required(float)
    currency = Optional(str)
    address = Required(str)
    addictional_wallet_info = Optional(str)
    total_received = Optional(int)
    total_withdrawn = Optional(float)


class Investment(db.Entity):
    id = PrimaryKey(int, auto=True)
    investment_fund = Required('InvestmentFund')
    user = Required(User)
    total_invested = Optional(float)
    total_profit = Optional(float)


class InvestmentFund(db.Entity):
    id = PrimaryKey(int, auto=True)
    investments = Set(Investment)
    total_invested = Required(float, default=0)
    total_withdrawn = Optional(float)
    total_users_profit = Optional(float)
    balance = Required(float, default=0)


class Message(db.Entity):
    id = PrimaryKey(int, auto=True)
    message_id = Optional(int)
    bot = Optional(Bot)
    user = Required(User)
    content = Optional(str)
    content_type = Optional(str)
    content_path = Optional(str)
    chat = Optional('Chat')


class Chat(db.Entity):
    id = PrimaryKey(int, auto=True)
    chat_id = Optional(str)
    users = Set(User)
    messages = Set(Message)



db.bind(provider='sqlite', filename='db.sqlite', create_db=True)
db.generate_mapping(create_tables=True)
