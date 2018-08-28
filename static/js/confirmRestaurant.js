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
        console.log(id)
        let rest_name = restaurant['name'];
        console.log(rest_name)

        let zipcode = restaurant['location']['zip_code'];
        console.log(zipcode)

        let address = restaurant['location']['address1'];
        console.log(address)

        let restaurant_option = strOrigin.concat(id, pip, rest_name, pip, zipcode, pip, address, strFinal) + rest_name + "(" + address + ")</option>";
        console.log(restaurant_option)

        $("#possible-restaurants").append(restaurant_option);
    }
}


function searchAgain(evt) {
    evt.preventDefault();

    // get the restaurant name from the browser
    let restaurant_name = {
        "name_restaurant_not_found": $("#restaurant-not-found-field").val()
    }
    
    console.log("name", restaurant_name)

    // pass restaurant_name to /search-again and call showResults
    $.post("/search-again", restaurant_name, showResults);
}


// when the user click notFound, we call searchAgain
 $("#notFound-button").on("click", searchAgain);