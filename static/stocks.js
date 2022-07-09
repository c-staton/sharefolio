const domain = 'https://www.sharefol.io';

function upperCaseF(a){
    setTimeout(function(){
        a.value = a.value.toUpperCase();
    }, 1);
}

$(".rTable").on('click', '.open-data', function(evt){
    evt.preventDefault();
    $(this).parent().parent().next().toggle();
})


function setWidth(){
    let width;
    $("#hide-exact-checkbox").is(':checked') ? width = '23%' : width = '46%';
    $('.toggle-visible').toggle();
    $('.rTableHead').width(width);
    $('.rTableCell').width(width);
}

$("#hide-exact-checkbox").on('click', setWidth)

let folioSum = parseFloat($('#total-value-amount').text());
let FOLIO = {};

async function addNewHolding(evt){
    evt.preventDefault();
    $('.error-msg').text('');

    let ticker = $('#symbol').val();
    const shares = $('#shares').val();

    if(ticker === '' || shares === '') {
        $('.error-msg').text(`Fields can't be empty`);
        return;
    }

    if(shares <= 0) {
        $('.error-msg').text(`Must enter an amount greater than 0`);
        return;
    }

    if($('#investments').val() === 'crypto'){
        ticker = ticker + 'USD';
    }

    try {
        data = await getStockData(ticker);
    } catch (err) {
        $('.error-msg').text(`Unknown ticker: '${ticker}'`)
        return
    }

    if(FOLIO[ticker]) {
        $('.error-msg').text(`'${ticker}' already added - delete holding and add again`);
        return;
    } else {
        FOLIO[ticker] = shares;
    }

    $("#save-to-profile").show();
    appendToPage(ticker,shares, data);
    updateTotalDisplay();
    updateAllPercentages();
    $('#symbol').val('');
    $('#shares').val('');
}

$('#add-stock').on('click', addNewHolding)


async function getStockData(ticker){
    res = await axios.get(`/api/holding/${ticker}`);
    return res.data;
}

function updateTotalDisplay(){
    $('#total-value-amount').text(Math.round(folioSum * 100) / 100);
}

function updateAllPercentages(){
    let holdings = $('.rTableBody').children()

    for(let h of holdings) {
        percent = $(h).children().children()[1];
        newPercent = (h.dataset.value/folioSum) * 100;
        roundPercent = Math.round(newPercent * 100) / 100;
        $(percent).text(`${roundPercent}%`);
    }
}

function appendToPage(ticker, shares, data){
    let totalValue = shares * data.price;
    folioSum += totalValue;

    //round total value for display
    totalValue = Math.round(totalValue * 100) / 100;

    let percentColor;
    let ifPos = '';
    if(data.changesPercentage >= 0) {
        percentColor = 'day-change-pos';
        ifPos = '+';
    } else {
        percentColor = 'day-change-neg';
    }
    
    let styleHide;
    $("#hide-exact-checkbox").is(':checked') ? styleHide = '' : styleHide = 'display:none';

    $('.rTableBody').append(
        `
        <div data-value="${totalValue}" data-ticker="${ticker}">
            <div class="rTableRow">
                <div class="rTableCell"><a href="" class="open-data">${ticker}</a></div>
                <div class="rTableCell">${(totalValue/folioSum)*100}%</div>
                <div class="rTableCell toggle-visible" style="${styleHide}">${shares}</div>
                <div class="rTableCell toggle-visible" style="${styleHide}">$${totalValue}</div>
                <div class="editTabCell"><a href="" class="delete-stock">X</a></div>
            </div>
            <div class="rTableRow hidden-data">
                <div class="stock-data-row">
                    <div class="stock-information">
                        <div class="name-price">
                            <div class="stock-name">${data.name}</div>
                            <div class="price-area">
                                <span class="main-price">$${data.price}</span>
                                <span class="${percentColor}">(${ifPos}${data.changesPercentage}%)</span>
                            </div>
                        </div>
                        <div class="data-container">
                            <div>
                                <div>Day Range: <span class="data">$${data.dayLow} - $${data.dayHigh}</span></div>
                            </div>
                            <div>
                                <div>Year Range: <span class="data">$${data.yearLow} - $${data.yearHigh}</span></div>
                            </div>
                            <div>
                                <div>Mkt Cap: <span class="data">${data.marketCap}</span></div>
                                <div>Vol: <span class="data">${data.volume}</span></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        `
    )
        //set width on most recent child of rTbody to match the other rows
        let width;
        if($("#hide-exact-checkbox").is(':checked')){
            width = '23%';
        } else {
            width = '46%';
        }
        $('.rTableBody:last-child .rTableCell').width(width);
}

async function deleteStock(evt){
    evt.preventDefault();

    totalValue = $(this).parent().parent().parent().attr("data-value");
    folioSum -= totalValue;

    ticker = $(this).parent().parent().parent().attr("data-ticker");
    delete FOLIO[ticker];

    $(this).parent().parent().parent().remove();
    updateTotalDisplay();
    updateAllPercentages();
}
$(".rTable").on('click', '.delete-stock', deleteStock)

async function sendToDB(){
    if(Object.keys(FOLIO).length === 0){
        return
    }
    let showExact;
    $("#hide-exact-checkbox").is(':checked') ? showExact = 1 : showExact = 0;
    const res = await axios.post('/portfolio/create', {'data': FOLIO, 'showExact': showExact});
    const url = res.data.url;
    $('#share-url').val(`${domain}/portfolio/${url}`)
    $('#share-url').show()
    $('#copy-url').show()
    $('#save-to-profile').hide()

    $("#symbol").prop("disabled", true);
    $("#shares").prop("disabled", true);
    $("#add-stock").prop("disabled", true);
    $("#investments").prop("disabled", true);
    $("#hide-exact-checkbox").prop("disabled", true);
}

$("#save-to-profile").on('click', sendToDB)


async function sendEditsToDB(){
    let url = $('.rTable').attr("data-url");
    let showExact;
    $("#hide-exact-checkbox").is(':checked') ? showExact = 1 : showExact = 0;
    const res = await axios.post(`/${url}/save-edits`, {'data': FOLIO, 'showExact': showExact});
    $('#share-url').val(`${domain}/portfolio/${url}`)
    $('#share-url').show()
    $('#copy-url').show()
    $('#save-edits').hide()
}

$("#save-edits").on('click', sendEditsToDB)

function copyToClipboard(){
    const copyText = document.getElementById("share-url");
    copyText.select();
    copyText.setSelectionRange(0, 99999);
    navigator.clipboard.writeText(copyText.value);
    $('#copy-url').text('Copied!')
    $('#copy-url').addClass('clicked')
    $('#copy-url').removeClass('btn-green')
}

$('#copy-url').on('click', copyToClipboard)


function changeInvestmentType(){
    if($('#investments').val() === 'stocks'){
        $("#symbol").attr("placeholder", "ex: AAPL");

        $("#shares-label").text('Shares:')
        $("#shares").attr("placeholder", "ex: 25");
    }
    else if($('#investments').val() === 'crypto'){
        $("#symbol").attr("placeholder", "ex: BTC");

        $("#shares-label").text('Coins:')
        $("#shares").attr("placeholder", "ex: 0.39");
    }    
}

$('#investments').on('change', changeInvestmentType)

let children = $('.rTableBody').children();
for(c of children){
    let ticker = $(c).attr("data-ticker");
    let shares = $(c).attr("data-shares");
    FOLIO[ticker] = shares;
}
updateAllPercentages();