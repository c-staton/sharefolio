import json
from unittest import TestCase

from flask import session
from app import app
from models import db, User, Portfolio, Holding

# use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sharefolio_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make flask errors be real errors 
app.config['TESTING'] = True

db.drop_all()
db.create_all()

class ViewTestCase(TestCase):
    """Test for views of user"""

    def setUp(self):
        """add sample data"""

        User.query.delete()

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

        p1 = Portfolio(show_exact = True, total_sum = 5000, holdings = [h1,h2,h3], url_string = 'abcdefghijklmnop', user=u)

        db.session.add(p1)
        db.session.commit()

        self.username = u.username
        self.port_url = p1.url_string

    def test_homepage(self):
        """Test the homepage display"""

        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<p>Make a shareable investment portfolio in seconds</p>', html)

    def test_show_user(self):
        """Test the display of user profile"""

        with app.test_client() as client:
            resp = client.get(f'/user/{self.username}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('AAPL', html)
            self.assertIn('SQ', html)
            self.assertIn('TSLA', html)

    def test_new_portfolio(self):
        """Test the new portfolio builder page"""

        with app.test_client() as client:
            resp = client.get('/portfolio/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<p>Create Your New Portfolio</p>', html)

    def test_create_portfolio(self):
        """Test the creation process of a new portfolio"""

        with app.test_client() as client:
            resp = client.post('/portfolio/create', json={'data': {'GOOG': 5, 'AAPL': 56, 'SQ': 84}, 'showExact': 1}, content_type='application/json')

            self.assertEqual(resp.status_code, 200)

            res_url = resp.json['url']

            resp_get_portfolio = client.get(f'/portfolio/{res_url}')
            html = resp_get_portfolio.get_data(as_text=True)

            self.assertEqual(resp_get_portfolio.status_code, 200)
            self.assertIn('GOOG', html)
            self.assertIn('AAPL', html)
            self.assertIn('SQ', html)

    def test_commit_edits(self):
        """Test the editing of a existing portfolio"""

        with app.test_client() as client:
            resp = client.post(f'/{self.port_url}/save-edits',  json={'data': {'AAPL': 56, 'SQ': 84}, 'showExact': 0}, content_type='application/json')

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json['message'], 'Success')

    def test_show_portfolio(self):
        """Test the portfolio view page"""

        with app.test_client() as client:
            resp = client.get(f'/portfolio/{self.port_url}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(self.username, html)
            self.assertIn('AAPL', html)
            self.assertIn('SQ', html)
            self.assertIn('TSLA', html)