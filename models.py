from email.policy import default
from enum import unique
from turtle import title
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database"""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """Site User"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)

    email = db.Column(db.Text, nullable = False, unique = True)

    username = db.Column(db.Text, nullable = False, unique = True)

    password = db.Column(db.Text, nullable = False)

    # portfolios = db.relationship('Portfolio', cascade="all,delete", backref='user')

    @classmethod
    def register(cls, email, username, pwd):
        """Register user w/ hashed password & return user"""

        hashed = bcrypt.generate_password_hash(pwd)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        #return instance of user w/ username and hashed pwd
        return cls(email=email, username=username, password=hashed_utf8)

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists and password is correct"""

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False


class Portfolio(db.Model):
    __tablename__ = 'portfolios'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)

    url_string = db.Column(db.Text, nullable=False, unique = True)

    title = db.Column(db.Text, default = 'Untitled')

    description = db.Column(db.Text, default = '')

    show_exact = db.Column(db.Boolean, default = False)

    total_sum = db.Column(db.Float, default = 0)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id',  ondelete='CASCADE'), default = None)

    user = db.relationship('User', backref='portfolios')
    

class Holding(db.Model):
    __tablename__ = 'holdings'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)

    ticker = db.Column(db.Text, nullable = False)

    shares = db.Column(db.Float, nullable = False)

    total_value = db.Column(db.Float)

    portfolio_percent = db.Column(db.Float)

    name = db.Column(db.Text)

    price = db.Column(db.Float)

    changesPercentage = db.Column(db.Float)

    dayLow = db.Column(db.Float)

    dayHigh = db.Column(db.Float)

    yearLow = db.Column(db.Float)

    yearHigh = db.Column(db.Float)

    marketCap = db.Column(db.Text)

    volume = db.Column(db.Text)

    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolios.id',  ondelete='CASCADE'))

    portfolio = db.relationship('Portfolio', backref = 'holdings')

    
