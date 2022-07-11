# sharefol.io
### Purpose
The purpose of [sharefol.io](https://www.sharefol.io/) is to make it easy to quickly and effortlessly display your investment portfolio with statistcs about each of your postitions and the ability to instantly share that portfolio accross the web.

### Features
The main feature of sharefol.io is to calculate and display the percentages that each investment holding takes up of the entire portfolio. Along with showing this percentage breackdown, sharefol.io gives indepth data about each holding. 

Privacy is important when if comes to sharing your investments, so the user has the option of hiding or showing their exact portfolio values, such as their number of shares and total holding value in dollars. 

Registration is not neccessary to simply create a portfolio and share it via URL. You can choose to create a portfolio anonymously or through a user account. The benefits of creating through an account is your portfolio's will always be editable and save to your profile for long term updating. 

Upon saving a portfolio, sharefol.io will supply the user with a unique URL that will display a read-only version of their newly made portfolio.



### Data
Using the [Financial Modeling Prep API](https://site.financialmodelingprep.com/developer/docs/), Sharefolio uses realtime stock market data to display information such as company name, share price, total market cap, etc. Along with general stock data, Sharefolio calculates what each of your holdings is worth, given ticker symbol and share amount, and will display the percentage of your entire portfolio each holding takes up.

### Technology
sharefol.io was created using Flask. Written entirly in Python, JavaScript, and HTML/CSS.