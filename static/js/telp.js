"use strict";

function showResults(results){
    console.log(results);
    
    // alert(result);
    let tip_in_dollars = results["tip_in_dollars"];
    let total_price = results["total_price"];
    let price_per_diner = results["price_per_diner"];

    $("#tip_in_dollars").html(tip_in_dollars);
    $("#total_price").html(total_price);
    $("#price_per_diner").html(price_per_diner);

}


function submitMeal(evt) {
    evt.preventDefault();
    
    let formInputs = {
        "restaurant_id": $("#restaurant-id-field").val(),
        "restaurant_zipcode": $("#restaurant-zipcode-field").val(),
        "price": $("#price-field").val(),
        "percentage_tip": $("#percentage-tip-field").val(),
        "diners": $("#diners-field").val(),
        "meal_type": $("#meal-type-field").val(),
    };
    
    $.post("/new-meal", formInputs, showResults);
    
}


$("#calculate").on("click", submitMeal);