import uuid
import requests
from flask import Flask, jsonify, redirect, render_template, request, session
from forms import RegisterForm, LoginForm, AddSharesForm
from models import db, connect_db, User, Portfolio, Holding
from app_info import API_BASE_URL, API_SECRET_KEY
from functions import calulatePercent, get_data, get_random_adj, updateTotalSum
from numerize import numerize
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///sharefolio')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'hellosecret1')

connect_db(app)
db.create_all()

@app.route('/')
def homepage():
    """Displays static homepage"""

    return render_template('home.html')

@app.route('/user/<username>')
def show_user(username):
    """Displays specific user profile"""

    random_adj = get_random_adj()
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user-profile.html', user=user, random_adj=random_adj)

@app.route('/portfolio/new')
def new_portfolio():
    """Display new portfolio creation form"""

    form = AddSharesForm()
    return render_template('stocks.html', form=form)

@app.route('/portfolio/create', methods=['POST'])
def create_portfolio():
    """Creates new portfolio in database with all given data"""

    incoming = request.get_json()
    data = incoming['data']
    url = uuid.uuid4().hex

    new_folio = Portfolio(show_exact = incoming['showExact'], url_string = url)

    if session.get('curr_user'):
        user = User.query.filter_by(username=session['curr_user']).first_or_404()
        new_folio.user = user

    db.session.add(new_folio)
    db.session.commit()

    for d in data:
        h = Holding(ticker=d, shares=data[d], portfolio_id=new_folio.id)
        get_data(h)
        updateTotalSum(h, new_folio)
        db.session.add(h)
    db.session.commit()

    return jsonify(url=url)

@app.route('/<url_string>/save-edits', methods=['POST'])
def commit_edits(url_string):
    """Saves all the made changes to specific portfolio"""

    portfolio = Portfolio.query.filter_by(url_string=url_string).first_or_404()

    if session.get('curr_user'):
        if portfolio.user.username != session['curr_user']:
            return redirect(f'/portfolio/{url_string}')
    

    incoming = request.get_json()
    data = incoming['data']

    portfolio.show_exact = incoming['showExact']

    db.session.add(portfolio)
    db.session.commit()

    #clear out any current holdings
    for h in portfolio.holdings:
        db.session.delete(h)
    db.session.commit()

    portfolio.total_sum = 0

    #add in all holdings
    for d in data:
        h = Holding(ticker=d, shares=data[d], portfolio_id=portfolio.id)
        get_data(h)
        updateTotalSum(h, portfolio)
        db.session.add(h)
    db.session.commit()

    for h in portfolio.holdings:
        calulatePercent(h, portfolio)

    db.session.add(portfolio)
    db.session.commit()

    return jsonify(message='Success')



@app.route('/portfolio/<url_string>')
def show_portfolio(url_string):
    """Display specific portfolio"""

    portfolio = Portfolio.query.filter_by(url_string=url_string).first_or_404()

    if portfolio.user == None:
        username = 'Anonymous'
    else: 
        username = portfolio.user.username

    show_exact = portfolio.show_exact

    holdings = Holding.query.filter_by(portfolio_id=portfolio.id).order_by(Holding.portfolio_percent.desc())

    portfolio.total_sum = 0

    for h in holdings: 
        get_data(h)
        updateTotalSum(h, portfolio)
        db.session.add(h)   

    db.session.commit()

    for h in holdings: 
        calulatePercent(h, portfolio) 

    db.session.add(portfolio)
    db.session.commit()

    return render_template('display-portfolio.html', username=username, holdings=holdings, show_exact=show_exact)

@app.route('/portfolio/<url_string>/edit')
def edit_portfolio(url_string):
    """Give portfolio author the form to edit specific portfolio"""

    portfolio = Portfolio.query.filter_by(url_string=url_string).first_or_404()

    if portfolio.user.username != session['curr_user']:
        return redirect(f'/user/{portfolio.user.username}')

    form = AddSharesForm()

    return render_template('stocks_edit.html', form=form, holdings=portfolio.holdings, show_exact=portfolio.show_exact, url_string=portfolio.url_string)

    


@app.route('/portfolio/<int:folio_id>', methods=['DELETE'])
def delete_portfolio(folio_id):
    """Delete entire portfolios"""

    portfolio = Portfolio.query.get_or_404(folio_id)

    if portfolio.user.username != session['curr_user']:
        return redirect(f'/user/{portfolio.user.username}')

    db.session.delete(portfolio)
    db.session.commit()
    return jsonify(message='deleted')

@app.route('/api/holding/<ticker>')
def get_holding_info(ticker):
    """Get and return all data about given ticker"""

    res = requests.get(f"{API_BASE_URL}/quote/{ticker}", params={'apikey': API_SECRET_KEY})
    data = res.json()
    rData = data[0]

    stock_info = {
        "name": rData['name'],
        "price": round(rData['price'],2),
        "changesPercentage": round(rData['changesPercentage'],2),
        "dayLow": round(rData['dayLow'],2),
        "dayHigh": round(rData['dayHigh'],2),
        "yearLow": round(rData['yearLow'],2),
        "yearHigh": round(rData['yearHigh'],2),
        "marketCap": numerize.numerize(rData['marketCap']),
        "volume": numerize.numerize(rData['volume'])
    }

    return stock_info

@app.route('/holding/<int:h_id>', methods=['DELETE'])
def delete_holding(h_id):
    """Delete holding"""

    holding = Holding.query.get_or_404(h_id)
    db.session.delete(holding)
    db.session.commit()
    return jsonify(message='deleted')

#######################################################
# SIGN-UP/LOGIN/LOGGOUT
#######################################################

@app.route('/login', methods=['GET', 'POST'])
def show_login_page():
    """Login user: produce form & handle login"""

    form = LoginForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data

        user = User.authenticate(name,pwd)

        if user:
            session['curr_user'] = user.username
            return redirect(f'/user/{user.username}')
        else:
            form.username.errors = ['Invalid username or password']

    return render_template('login-page.html', form=form)

@app.route('/sign-up', methods=['GET', 'POST'])
def show_sign_up():
    """Register user: produce form & handle sign up"""

    form = RegisterForm() 

    if form.validate_on_submit():
        email = form.email.data
        name = form.username.data
        pwd = form.password.data

        if User.query.filter_by(email=email).first():
            form.email.errors = ['Email already exists']
            return render_template('sign-up.html', form=form)
        if User.query.filter_by(username=name).first():
            form.username.errors = ['Username already exists']
            return render_template('sign-up.html', form=form)

        user = User.register(email,name,pwd)
        db.session.add(user)
        db.session.commit()

        session['curr_user'] = user.username

        return redirect(f'/user/{user.username}')
    else:
        return render_template('sign-up.html', form=form)

@app.route('/logout')
def logout():
    """Logs user out and redirects to homepage"""

    if session.get('curr_user'):
        session.pop('curr_user')
    return redirect('/')