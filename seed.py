from flask import session
from models import Holding, Portfolio, db
from app import app

db.drop_all()
db.create_all()

h1 = Holding(ticker = 'AAPL', shares = 5)
h2 = Holding(ticker = 'SQ', shares = 15)

db.session.add(h1)
db.session.add(h2)
db.session.commit()

p1 = Portfolio(show_exact = False, total_sum = 5000, holdings = [h1,h2])

db.session.add(p1)
db.session.commit()