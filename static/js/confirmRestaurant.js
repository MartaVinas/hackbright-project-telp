/**
* Functions to keep searching the restaurant
*/

"use strict";


function showResults(results){ 
    
    let restaurants = results;

    let strOrigin = "<option value='";
    let pip = "|";
    let strFinal = "'>";

    for (let restaurant of restaurants) {
        
        let id = restaurant['id'];
      
        let rest_name = restaurant['name'];

        let zipcode = restaurant['location']['zip_code'];

        let address = restaurant['location']['address1'];

        let restaurant_option = strOrigin.concat(id, pip, rest_name, pip, zipcode, pip, address, strFinal) + rest_name + "(" + address + ")</option>";

        $("#possible-restaurants").prepend(restaurant_option);
    }
}

let count = 0;

function searchAgain(evt) {
    evt.preventDefault();

    count = count + 1;

    // get the restaurant name from confirm-restaurant.html restaurant_not_found form
    let name_and_counter = {
        "name_restaurant_not_found": $("#restaurant-not-found-field").val(),
        "counter": count
    }
    
    // pass name_and_counter to /search-again and call showResults
    $.post("/search-again", name_and_counter, showResults);
}


// when the user click notFound, we call searchAgain
 $("#notFound-button").on("click", searchAgain);