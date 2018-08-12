"""routes for TELP project."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import Restaurant, Meal, Admin, connect_to_db, db

from yelp_requests import search_restaurants_by_name, search_restaurants


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """Show homepage."""

    return render_template("homepage.html")


@app.route('/search-restaurant', methods=['GET'])
def search_restaurant():
    """Search the user restaurant in telp_db."""

    # get restaurant name from the user
    restaurant_name = request.args.get("restaurant_name")

    # search restaurant in telp_db and get all restaurants objects with that name
    restaurants_in_db = db.session.query(Restaurant).filter_by(name=restaurant_name).all()

    if not restaurants_in_db:
        # if restaurant is not in telp_db, search it in YELP
        restaurants_in_yelp = search_restaurants_by_name(restaurant_name)

        if restaurants_in_yelp['total'] != 0:
            # add restaurant into telp_db
            #add_restaurants_to_db(restaurants_in_yelp)

            return render_template("show-restaurants.html", restaurants_in_yelp=restaurants_in_yelp)
        else:
            # show a message
            flash("The restaurant {name} doesn't exist in YELP. You could search average tip information by zipcode.".format(name=restaurant_name))
            return redirect("/")
    else:
        return render_template("tip-info-calc.html", restaurants_in_db=restaurants_in_db)


def add_restaurants_to_db(restaurants):
    """Store restaurants from YELP into telp_db.

    restaurants from YELP(json)
    """

    for restaurant in restaurants['businesses']:

        if not is_restaurant_in_db(restaurant):

            new_restaurant = Restaurant(yelp_restaurant_id=restaurant['id'],
                                        name=restaurant['name'],
                                        address=restaurant['location']['address1'],
                                        zipcode=restaurant['location']['zip_code'],
                                        rating=restaurant['rating'])

            db.session.add(new_restaurant)

    db.session.commit()


def is_restaurant_in_db(restaurant):
    """Check if restaurant given is in telp_db.

    restaurant(dictionary)

    Return True if already exist or False if not.
    """

    restaurant_in_db = db.session.query(Restaurant).filter(Restaurant.yelp_restaurant_id == restaurant['id']).all()

    if restaurant_in_db:
        return True

    return False


#----------------------------------------------------------------------------#

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
