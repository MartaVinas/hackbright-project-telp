/**
* Functions to control the tip calculator
*/

"use strict";


function showResults(results){ 
    // get the results from /new-meal and set it into the browser elements(telp.html)
    $("#tip_in_dollars").val(results["tip_in_dollars"]);
    $("#total_price").val(results["total_price"]);
    $("#price_per_diner").val(results["price_per_diner"]);
}


function submitMeal(evt) {
    evt.preventDefault();

    $('#results').removeAttr('hidden');
    
    let formInputs;
    let requirementsOK = checkRequirements();
  
    // if all requirements are OK, get the information from telp.html meal form
    if(requirementsOK){
        formInputs = {
            "restaurant_id": $("#restaurant-id-field").val(),
            "restaurant_zipcode": $("#restaurant-zipcode-field").val(),
            "price": parseFloat($("#price-field").val()).toFixed(2),
            "percentage_tip": parseInt($("#percentage-tip-field").val()),
            "diners": parseInt($("#diners-field").val()),
            "meal_type": getMealType(),
        };

        // pass formInputs to /new-meal and call showResults
        $.post("/new-meal", formInputs, showResults);
    } 
}


// when the user click calculate, we call submitMeal
$("#calculate").on("click", submitMeal);


function checkRequirements(){

    let requirementsOK = true;

    // find 'inputs' and 'selects' from telp.html meal form
    // and check for requirements
    $('#meal').find('input, select').each(function(){
        
        let value = $(this).val();

        let required = $(this).prop('required');

        // if it is required and there is no value, shows an alert
        if(required){
            if(!value){
                requirementsOK = false;
                alert($(this).attr('name') + " is required");
            }
        }

        let typeOfValue = $(this).attr('type');

        // if it is a number check differents things
        if(typeOfValue == 'number'){

            // shows an alert if it should be positive
            if(value < 0){
                requirementsOK = false;
                alert($(this).attr('name') + " should be positive");
            }

            let step = $(this).attr('step');
            let integer, decimals;
            [integer, decimals] = value.split('.');

            // shows an alert if it should have more than 2 decimals
            if(step == '0.01' && decimals){         
                if(decimals.length > 2){
                    requirementsOK = false;
                    alert($(this).attr('name') + " should have 2 decimals");
                }
            }
            // shows an alert if it should be an integer
            if(step == '1'){
                if(decimals){
                    requirementsOK = false;
                    alert($(this).attr('name') + " should be an integer");
                }
            }

            let maxLength = $(this).attr('maxlength');
            // shows an alert if it is too long
            if(value.length > maxLength){
                requirementsOK = false;
                alert($(this).attr('name') + " it is too long");
            }
        }  
    });

    return requirementsOK;
}


function getMealType(){

    let meal_type;

    if(document.getElementById('lunch-field').checked) {
        // lunch radio button has been selected
        meal_type = $("#lunch-field").val();
    }else if(document.getElementById('dinner-field').checked) {
        // dinner radio button has been selected
        meal_type = $("#dinner-field").val();
    }

    return meal_type;
}