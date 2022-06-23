//data base
//'APPL': 500, 'TSLA': 300
let FOLIO = {};
let updatedValues = {};
let valuesHidden = false;
let colorChangeBool = true;
let colorClass;
const apikey = 'df3b692400bbee905ea8aa530344eced';

// async function addNewHolding(evt){
//     evt.preventDefault();
//     let ticker = $('#sym-input').val();
//     let shares = $('#share-input').val();
//     $('#sym-input').val('');
//     $('#share-input').val('');
//     try {
//         let res = await axios.get(`https://financialmodelingprep.com/api/v3/quote/${ticker}`, { params:{apikey}});
//         var rData = res.data[0] 
//         var sharePrice = rData.price;
//     }
//     catch (error) {
// 		console.log('NOT A VALID TICKER');
// 	}
//     let totalValue = sharePrice * shares;
//     updatedValues[ticker] = totalValue;
//     if(!totalValue > 0) {
//         return;
//     }
//     let newSum = await getNewSum(totalValue);
//     console.log(newSum);
//     let percent = getPercent(totalValue, newSum);
//     updateUI(newSum);
//     addToDataBase(ticker, shares);
//     colorChangeBool = !colorChangeBool;
//     colorChangeBool == true ? colorClass = 'white' : colorClass = 'gray';
//     $('.rTableBody').append(
//                             `
//                             <div class="rTableRow" id="${ticker}">
//                                 <div class="rTableCell ${colorClass}"><a href="" class="open-data">${ticker}</a></div>
//                                 <div class="rTableCell ${colorClass} percentage">${percent}%</div>
//                                 <div class="rTableCell toggle-visible ${colorClass}" style="display:none">${shares}</div>
//                                 <div class="rTableCell toggle-visible ${colorClass}" style="display:none">$${totalValue.toFixed(2)}</div>
//                                 <div class="editTabCell"><a href="" class="delete-stock">X</a></div>
//                             </div>
//                             <div class="rTableRow hidden-data">
//                                 <div class="stock-data-row">
//                                     <div class="stock-information">
//                                         <div class="name-price">
//                                             <div class="stock-name">${rData.name} (${ticker})</div>
//                                             <div class="price-area">
//                                                 <span class="main-price">$${rData.price.toFixed(2)}</span>
//                                                 <span class="day-change">(${rData.changesPercentage.toFixed(2)}%)</span>
//                                             </div>
//                                         </div>
//                                         <div class="data-container">
//                                             <div>
//                                                 <div>Day Range: <span class="data">$${rData.dayLow.toFixed(2)} - $${rData.dayHigh.toFixed(2)}</span></div>
//                                             </div>
//                                             <div>
//                                                 <div>Year Range: <span class="data">$${rData.yearLow.toFixed(2)} - $${rData.yearHigh.toFixed(2)}</span></div>
//                                             </div>
//                                             <div>
//                                                 <div>Mkt Cap: <span class="data">${abbreviateNumber(rData.marketCap)}</span></div>
//                                                 <div>Vol: <span class="data">${abbreviateNumber(rData.volume)}</span></div>
//                                             </div>
//                                         </div>
//                                     </div>
//                                 </div>
//                             </div>
//                             `
//     );
//     $('#rTableTotal').show();
//     $('#total-value-amount').text(`$${newSum.toFixed(2)}`);
// }

// $('#add-stock').on('click', addNewHolding);

async function getNewSum(newValue) {
    let sum = 0;
    for(let key in FOLIO) {
        let res = await axios.get(`https://financialmodelingprep.com/api/v3/quote/${key}`, { params:{apikey}});
        let sharePrice = res.data[0].price;
        let stockValue = sharePrice * FOLIO[key];
        updatedValues[key] = stockValue;
        sum += stockValue;
    }
    sum += newValue;
    return sum;
}

function getPercent(totalValue, sum) {
    let percent = (totalValue/sum) * 100;
    return percent.toFixed(2);
}

function updateUI(newSum) {
    //adjust other percents on screen
    for(let key in FOLIO) {
        let newPercent = (updatedValues[key] / newSum) * 100;
        $(`#${key} > .percentage`).html(newPercent.toFixed(2) + '%');
    }
}


function upperCaseF(a){
    setTimeout(function(){
        a.value = a.value.toUpperCase();
    }, 1);
}



$(".rTable").on('click', '.open-data', function(evt){
    evt.preventDefault();
    $(this).parent().parent().next().toggle();
})



async function deleteStock(evt){
    evt.preventDefault();
    const id = $(this).parent().parent().parent().data('id');
    await axios.delete(`/holding/${id}`)
    $(this).parent().parent().parent().remove();
}
$(".rTable").on('click', '.delete-stock', deleteStock)



$("#hide-exact-checkbox").on('click', function(){
    let width;
    $("#hide-exact-checkbox").is(':checked') ? width = '23%' : width = '46%'
    $('.toggle-visible').toggle();
    $('.rTableHead').width(width);
    $('.rTableCell').width(width);
})
