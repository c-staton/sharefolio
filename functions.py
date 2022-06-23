import requests
from app_info import API_BASE_URL, API_SECRET_KEY
from numerize import numerize

def get_data(h, portfolio):
    res = requests.get(f"{API_BASE_URL}/quote/{h.ticker}", params={'apikey': API_SECRET_KEY})
    data = res.json()
    rData = data[0]
    h.name = rData['name']
    h.price = round(rData['price'],2)
    h.changesPercentage = round(rData['changesPercentage'],2)
    h.dayLow = round(rData['dayLow'],2)
    h.dayHigh = round(rData['dayHigh'],2)
    h.yearLow = round(rData['yearLow'],2)
    h.yearHigh = round(rData['yearHigh'],2)
    h.marketCap = numerize.numerize(rData['marketCap'])
    h.volume = numerize.numerize(rData['volume'])
    h.total_value = round(float(h.price) * float(h.shares),2)
    h.display_shares = round(h.shares,0)

def updateTotalSum(h, portfolio):
    portfolio.total_sum = portfolio.total_sum + h.total_value

def calulatePercent(h, portfolio):
    h.portfolio_percent = round(((h.total_value / portfolio.total_sum) * 100),2)
