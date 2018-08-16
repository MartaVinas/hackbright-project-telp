/**
* Functions to control the tip calculator
*/

"use strict";

function showResults(results){ 
    // get the results from /new-meal and set it into the browser elements
    $("#tip_in_dollars").html(results["tip_in_dollars"]);
    $("#total_price").html(results["total_price"]);
    $("#price_per_diner").html(results["price_per_diner"]);
}


function submitMeal(evt) {
    evt.preventDefault();
    
    let formInputs;
    // find inputs and selects of the form meal
    $('#meal').find('input, select').each(function(){
        
        let required = $(this).prop('required');
        let there_is_value = $(this).val();

        let proceed = true;
        // if they are required and there is no value show an alert
        if(required){
            if(!there_is_value){
                proceed = false;
                alert($(this).attr('name') + " is required");
            } else {
                proceed = true;
            }
        }

        if(proceed){
            // get the information from the browser
            formInputs = {
                "restaurant_id": $("#restaurant-id-field").val(),
                "restaurant_zipcode": $("#restaurant-zipcode-field").val(),
                "price": $("#price-field").val(),
                "percentage_tip": $("#percentage-tip-field").val(),
                "diners": $("#diners-field").val(),
                "meal_type": $("#meal-type-field").val(),
            };
        }       
    });
    // pass formInputs to /new-meal and call showResults
    $.post("/new-meal", formInputs, showResults);  
}

// when the user click calculate, we call submitMeal
$("#calculate").on("click", submitMeal);