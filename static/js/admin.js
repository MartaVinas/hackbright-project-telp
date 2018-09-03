/**
* Functions to control admin functions
*/

"use strict";

/****** delete restaurants from the db that there are not in YELP ******/

function showNumRestDeleted(results){

     $("#restaurants-deleted").html("Congratulations! the database has been updated: " + results + " restaurants deleted.")
}

// when the user click delete, we call delete route and showNumRestDeleted
$("#delete").on("click", (evt) => $.get("/delete", showNumRestDeleted));


/****** show the form to change the password ******/

// when the user click change-pwd, we show the form
$("#change-pwd").on("click", () => $('#change-pwd-form').removeAttr('hidden'));


/****** change the password ******/

function showPwdChanged(results){
    if(results=='1'){
        $("#pwd-changed").html("Password has been changed successfully!");
    }else{
        alert("Something failed")
    }  
}

function updatePwd(evt){
    evt.preventDefault();

    let formInputs;
    let requirementsOK = checkRequirements();
    
    // if all requirements are OK, get the information from the form
    if(requirementsOK){

        let formInput = {"new_pwd": $("#pwd-field").val()};
        // pass formInputs to /new-meal and call showResults
        $.post("/change-pwd", formInput, showPwdChanged);
    }
}

// when the user click update-pwd, we call updatePwd
$("#update-pwd").on("click", updatePwd);


function checkRequirements(){

    let requirementsOK = true;
    
    let value = $("#pwd-field").val();

    let required = $("#pwd-field").prop('required');

    // if it is required and there is no value, shows an alert
    if(required){
        if(!value){
            requirementsOK = false;
            alert($("#pwd-field").attr('name') + " is required");
        }
    }
    return requirementsOK;
}
