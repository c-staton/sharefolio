from crypt import methods
from flask import Flask, jsonify, redirect, render_template, request, session
from forms import RegisterForm, LoginForm, AddSharesForm
from models import db, connect_db, User, Portfolio, Holding
from app_info import API_BASE_URL, API_SECRET_KEY
from functions import calulatePercent, get_data, updateTotalSum

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sharefolio'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "adfasdfaspkg"

connect_db(app)
db.create_all()

@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/portfolio/new', methods=['POST'])
def create_anon_portfolio():
    """create new portfolio for user"""
    newPortfolio = Portfolio()

    # if user is logged in link portfolio to user
    if session.get('user_id'):
        newPortfolio.user_id = session['user_id']

    db.session.add(newPortfolio)
    db.session.commit()
    return redirect(f'/portfolio/{newPortfolio.id}/edit')


@app.route('/portfolio/<int:folio_id>/edit', methods=['GET', 'POST'])
def edit_anon_portfolio(folio_id):

    portfolio = Portfolio.query.get_or_404(folio_id)

    # if user is not the owner can only view
    if session.get('user_id'):
        if portfolio.user_id != session['user_id']:
            return redirect(f'/portfolio/{folio_id}')

    form = AddSharesForm()
    
    holdings = Holding.query.filter_by(portfolio_id=folio_id).order_by(Holding.portfolio_percent.desc())

    if form.validate_on_submit():   
        ticker = form.symbol.data
        shares = form.shares.data

        new_holding = Holding(ticker=ticker, shares=shares, portfolio_id=folio_id)
        get_data(new_holding, portfolio)
        updateTotalSum(new_holding, portfolio)
        calulatePercent(new_holding, portfolio)
        db.session.add(portfolio)
        db.session.commit()
        db.session.add(new_holding)
        db.session.commit()

        for h in holdings: 
            calulatePercent(h, portfolio)
            db.session.add(h)  
        db.session.commit()
        return redirect(f'/portfolio/{folio_id}/edit')

    return render_template('stocks.html', form=form, holdings=holdings)

@app.route('/portfolio/<int:folio_id>')
def show_anon_portfolio(folio_id):

    portfolio = Portfolio.query.get_or_404(folio_id)

    if portfolio.user == None:
        username = 'Anonymous'
    else: 
        username = portfolio.user.username

    show_exact = portfolio.show_exact

    holdings = Holding.query.filter_by(portfolio_id=folio_id).order_by(Holding.portfolio_percent.desc())

    for h in holdings: 
        get_data(h, portfolio)
        db.session.add(h)    

    db.session.commit()

    return render_template('display-portfolio.html', username=username, holdings=holdings, show_exact=show_exact)

@app.route('/holding/<int:h_id>', methods=['DELETE'])
def delete_holding(h_id):
    """Delete holding"""

    holding = Holding.query.get_or_404(h_id)
    db.session.delete(holding)
    db.session.commit()
    return jsonify(message='deleted')

@app.route('/login', methods=['GET', 'POST'])
def show_login_page():
    """Login user: produce form & handle login"""
    form = LoginForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data

        user = User.authenticate(name,pwd)

        if user:
            session['user_id'] = user.id
            return redirect('/')
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

        session['user_id'] = user.id

        return redirect('/')
    else:
        return render_template('sign-up.html', form=form)

@app.route('/logout')
def logout():
    """Logs user out and redirects to homepage"""
    if session.get('user_id'):
        session.pop('user_id')
    return redirect('/')