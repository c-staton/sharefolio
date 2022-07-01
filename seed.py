from flask import session
from models import Holding, Portfolio, User, db
from app import app

db.drop_all()
db.create_all()

h1 = Holding(ticker = 'AAPL', shares = 5)
h2 = Holding(ticker = 'SQ', shares = 15)
h3 = Holding(ticker = 'TSLA', shares = 70)

db.session.add(h1)
db.session.add(h2)
db.session.add(h3)
db.session.commit()

u = User.register('toast@gmail.com','toast', 'toast')
db.session.add(u)
db.session.commit()

p1 = Portfolio(show_exact = True, total_sum = 5000, holdings = [h1,h2], url_string = 'abcdefghijklmnop', user=u)

db.session.add(p1)
db.session.commit()