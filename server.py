"""Routes and helper functions for TELP project."""

import os

from datetime import datetime

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import func

from model import Restaurant, Meal, Admin, connect_to_db, db
from yelp_requests import search_restaurants_by_name, search_restaurants, search_restaurants_by_name_paginate, search_restaurants_by_id
from tip_calculator import get_tip_in_dollars, get_total_price, get_price_per_diner


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# It raises an error if you use an undefined variable in Jinja2
app.jinja_env.undefined = StrictUndefined

################################################################################
# Routes #


@app.route('/')
def homepage():
    """Show homepage."""

    return render_template("homepage.html")


@app.route('/search-restaurant', methods=['GET'])
def search_restaurant():
    """Search the user restaurant in telp_db."""

    # get restaurant name from homepage.html search_restaurant form
    restaurant_name = request.args.get("restaurant_name")

    # search restaurant in telp_db and get all restaurants objects with that name
    restaurants_in_db = db.session.query(Restaurant).\
                                filter_by(name=restaurant_name.lower()).all()

    if not restaurants_in_db:
        # if restaurant is not in telp_db, search it in YELP
        restaurants_in_yelp = search_restaurants_by_name(restaurant_name)

        if restaurants_in_yelp['total'] != 0:
            # get a list of restaurants and add restaurants into telp_db
            restaurants_in_db = create_restaurants_list_from_restaurant_json(restaurants_in_yelp)
            
            add_restaurants_to_db(restaurants_in_yelp)
        
        else:
            flash("We don't have data for {name}!"
                " You can search average tip information by zipcode.".format(name=restaurant_name))
            return redirect("/")

    return render_template("confirm-restaurant.html", 
                            restaurants_in_db=restaurants_in_db,
                            restaurant_name=restaurant_name)


@app.route('/search-zipcode', methods=['GET'])
def search_zipcode():
    """Search the user zipcode in telp_db."""
    
    # get zipcode from homepage.html search_zipcode form
    zipcode = request.args.get("zipcode")

    # search zipcode in telp_db
    zipcode_in_db = db.session.query(Meal).\
                                filter_by(zipcode=zipcode).all()

    if not zipcode_in_db:
        # if there is no zipcode in telp_db, show a message
        flash("There is no information for {zipcode}.".format(zipcode=zipcode))
        
        return redirect("/")
   
    else:
        # get average tip by zipcode and meal type
        average_tip_lunch = get_average_tip_by_zipcode(zipcode, 'lunch')
        
        average_tip_dinner = get_average_tip_by_zipcode(zipcode, 'dinner')

        # get the google api key stored in secrets.sh from os
        google_api_key = os.environ['GOOGLE_API_KEY']
        
        return render_template("telp.html",
                                zipcode=zipcode,
                                average_tip_lunch=average_tip_lunch,
                                average_tip_dinner=average_tip_dinner,
                                google_api_key=google_api_key,
                                restaurant_name=None)


@app.route('/tip-calculator', methods=['GET'])
def tip_calculator():
    """Shortcut to go straight to tip calculator"""

    return render_template("telp.html",
                            zipcode=None,
                            restaurant_name=None)


@app.route('/get-tip-info', methods=['POST'])
def get_average_tip():
    """Get average tip info from telp_db"""

    restaurant_first_search = request.form.get("restaurant")
    
    restaurant_second_search = request.form.get("possible-restaurants")
    
    restaurant_choosen = ""
    
    if restaurant_first_search is not None:
        restaurant_choosen = restaurant_first_search
        print("rest first search", restaurant_first_search)
    if restaurant_second_search is not None:
        restaurant_choosen = restaurant_second_search
        print("rest second search", restaurant_second_search)
    print("rest chosen", restaurant_choosen)
    # get restaurant from confirm-restaurant.html show_restaurants form
    restaurant_yelp_id, restaurant_name, restaurant_zipcode, restaurant_address = restaurant_choosen.split("|")
    
    # get average tip from telp_db by restaurant and meal type
    average_tip_lunch = get_average_tip_by_restaurant(restaurant_yelp_id, 'lunch')

    average_tip_dinner = get_average_tip_by_restaurant(restaurant_yelp_id, 'dinner')

    # get the google api key stored in secrets.sh from os
    google_api_key = os.environ['GOOGLE_API_KEY']

    return render_template("telp.html",
                            restaurant_id=restaurant_yelp_id,
                            restaurant_name=restaurant_name,
                            restaurant_zipcode=restaurant_zipcode,
                            average_tip_lunch=average_tip_lunch, 
                            average_tip_dinner=average_tip_dinner,
                            restaurant_address=restaurant_address,
                            google_api_key=google_api_key,
                            zipcode=None)


@app.route('/search-again', methods=['POST'])
def search_again():
    """Search restaurant by name in YELP

    return a json with all the restaurants
    """

    # get information from confirmRestaurant.js function searchAgain name_and_counter
    restaurant_name = request.form.get("name_restaurant_not_found")

    num_of_clicks = int(request.form.get("counter"))

    limit = 6
    offset = num_of_clicks * limit

    restaurants = search_restaurants_by_name_paginate(restaurant_name, limit, offset)

    add_restaurants_to_db(restaurants)
    
    return jsonify(restaurants['businesses'])


@app.route("/new-meal", methods=['POST'])
def add_meal_and_calculate():
    """Add a meal to telp_db

    return a json with tip in dollars, total price and price per diner
    """

    # get information from telp.js function submitMeal formInputs
    price = round(float(request.form.get("price")),2)

    percentage_tip = int(request.form.get("percentage_tip"))

    diners = int(request.form.get("diners"))

    restaurant_id=request.form.get("restaurant_id")

    # when user search by zipcode, there is no restaurant
    # when user search by restaurant, it is added a new meal in telp_db
    if restaurant_id:
        new_meal = Meal(yelp_restaurant_id=restaurant_id,
                    zipcode=request.form.get("restaurant_zipcode"),
                    meal_type=request.form.get("meal_type"),
                    price=price,
                    percentage_tip=percentage_tip,
                    date=datetime.now())

        db.session.add(new_meal)

        db.session.commit()

    return calculate(price, percentage_tip, diners)


@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login-form.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    username = request.form["username"]
    password = request.form["password"]

    admin = Admin.query.filter_by(username=username).first()

    if not admin:
        flash("Incorrect username")
        return redirect("/login")

    if admin.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["admin_id"] = admin.admin_id

    flash("Logged in")
    return render_template("admin.html", username=username)


@app.route('/delete', methods=['GET'])
def delete_restaurants():
    """Delete from telp db restaurants that there are not in Yelp"""

    restaurant_deleted_counter = 0

    # Search all restaurant ids in telp_db
    restaurants_in_db = db.session.query(Restaurant.yelp_restaurant_id).all()

    #restaurants_in_db is a list of tuples with the id in position 0 of each tuple
    for restaurant in restaurants_in_db:
        id_restaurant, = restaurant

        # Search all the restaurants in YELP by id
        restaurant_in_Yelp = search_restaurants_by_id(id_restaurant)

        # If there is no restaurant in YELP, delete from telp_db
        if restaurant_in_Yelp is None:
            
            db.session.delete(Restaurant.query.get(id_restaurant))

            db.session.commit()

            restaurant_deleted_counter += 1
    
    return str(restaurant_deleted_counter)


@app.route('/change-pwd', methods=['POST'])
def change_pwd():
    """Change the admin's password in telp_db."""

    new_pwd = request.form.get("new_pwd")

    admin_id = session["admin_id"]

    result = 0
    try:
        Admin.query.filter_by(admin_id=admin_id).update(dict(password=new_pwd))
        db.session.commit()
        result = 1
    except:
        pass

    return str(result)


@app.route('/logout')
def logout():
    """Log out."""

    del session["admin_id"]
    flash("Logged Out.")
    return redirect("/")


################################################################################
# Helper functions #


def create_restaurants_list_from_restaurant_json(restaurants):
    """Create restaurants list from YELP restaurants.

    restaurants(json)

    return list of restaurants
    """

    restaurants_list = []
    
    for restaurant in restaurants['businesses']:

        new_restaurant = Restaurant(yelp_restaurant_id=restaurant['id'],
                                    name=restaurant['name'].lower(),
                                    address=restaurant['location']['address1'],
                                    zipcode=restaurant['location']['zip_code'],
                                    rating=restaurant['rating'])

        restaurants_list.append(new_restaurant)

    return restaurants_list


def add_restaurants_to_db(restaurants):
    """Store restaurants from YELP into telp_db.

    restaurants(json)
    """

    new_restaurants = create_restaurants_list_from_restaurant_json(restaurants)
    
    for restaurant in new_restaurants:

        if not is_restaurant_in_db(restaurant):

            db.session.add(restaurant)

    db.session.commit()


def is_restaurant_in_db(restaurant):
    """Check if restaurant given is in telp_db.

    restaurant(list)

    Return True if already exist or False if not.
    """

    restaurant_in_db = db.session.query(Restaurant).\
                                filter(Restaurant.yelp_restaurant_id == restaurant.yelp_restaurant_id).\
                                all()

    if restaurant_in_db:
        return True

    return False


def get_average_tip_by_zipcode(zipcode, meal_type):
    """Query to telp_db to get the average tip by zipcode and meal_type

    zipcode(string)
    meal_type(string)

    return a float or NONE
    """

    average_tip = db.session.query(func.round(func.avg(Meal.percentage_tip), 2)).\
                    group_by(Meal.meal_type).\
                    having(Meal.meal_type=='{type}'.format(type=meal_type)).\
                    filter(Meal.zipcode==zipcode).\
                    first()

    if average_tip:
        # unpack the tupla (Decimal('20.67'),) and get the number
        average_tip_value, = average_tip
        
        return average_tip_value


def get_average_tip_by_restaurant(restaurant, meal_type):
    """Query to telp_db to get the average tip by restaurant and meal_type

    restaurant(string)
    meal_type(string)

    return a float or NONE
    """

    average_tip = db.session.query(func.round(func.avg(Meal.percentage_tip), 2)).\
                    join(Restaurant).\
                    group_by(Meal.yelp_restaurant_id, Meal.meal_type).\
                    having(Meal.meal_type=='{type}'.format(type=meal_type)).\
                    filter(Restaurant.yelp_restaurant_id==restaurant).\
                    first()

    if average_tip:
        # unpack the tuple (Decimal('20.67'),) and get the number
        average_tip_value, = average_tip
        
        return average_tip_value


def calculate(price, percentage_tip, diners):
    """Calculate the tip in dollars, total price and price per diner

    price(float)
    percentage_tip(integer)
    diners(integer)

    return a json

    """

    return jsonify(tip_in_dollars=get_tip_in_dollars(price, percentage_tip),
                    total_price=get_total_price(price, percentage_tip),
                    price_per_diner=get_price_per_diner(price, percentage_tip, diners))


#----------------------------------------------------------------------------#

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    #app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
