/**
* Functions to control the map by restaurant
*/

"use strict";


let restaurantAddress = $("#restaurant-address-field").val() + " " + $("#restaurant-zipcode-field").val();

function initMap(){

    let geocoder = new google.maps.Geocoder();

    let request = geocoder.geocode( { 'address': restaurantAddress},
        function(results, status){
            if (status === 'OK') {
                let marker = new google.maps.Marker({
                    position: results[0].geometry.location,
                    map: new google.maps.Map(document.getElementById('map'), {
                        center: results[0].geometry.location,
                        zoom: 16
                    }),
                    title:'restaurant'
                });
            } else {
                alert('Restaurant not found');
            }
        });
}