/**
* Functions to control the map by zipcode
*/

"use strict";

let sanFrancisco = {lat: 37.7749, lng: -122.4313};

let zipcode = $("#zipcode-field").val()

function initMap(){

    let map = new google.maps.Map(document.getElementById('map'), {
        center: sanFrancisco,
        zoom: 12
    });

    let layer = new google.maps.FusionTablesLayer({
        query: {
            select: 'geometry',
            from: '1gLK5O8DPWYlHBzxKx71RNJ9lpbOZt2pk-Hx_ApdD'
        },
        styles: [{
            polygonOptions: {
                fillColor: '#C70039',
                fillOpacity: 0.2
            }
        },{
            where: 'ZIP = ' + zipcode + ' ',
            polygonOptions: {
                fillOpacity: 0.4
            }
        }]
    });

    layer.setMap(map);
}