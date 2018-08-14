"use strict";

function showResults(results){
    console.log(results)
    let tip_in_dollars = results["tip_in_dollars"];
    let total_price = results["total_price"];
    let price_per_diner = results["price_per_diner"];

    $("#tip_in_dollars").html(tip_in_dollars);
    $("#total_price").html(total_price);
    $("#price_per_diner").html(price_per_diner);

}


function calculate(evt) {
    // evt.preventDefault();

    $.get("/calculate", showResults);
    
}


$("#calculate").on("click", calculate);