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
    """Search the user restaurant in the db."""

    # get restaurant name from the user
    restaurant_name = request.args.get("restaurant_name")

    # search restaurant in telp db and get all restaurants objects with that name
    restaurants_in_db = db.session.query(Restaurant).filter_by(name=restaurant_name).all()

    if restaurants_in_db is None:
        # if restaurant is not in telp db, search it in YELP
        restaurants_in_yelp = search_restaurants_by_name(restaurant_name)

        if restaurants_in_yelp:
            # add into telp db
            return render_template("show-restaurants.html", restaurants_in_yelp=restaurants_in_yelp)
        else:
            # show a message
            return "Not Found"
    else:
        return render_template("tip-info-calc.html", restaurants_in_db=restaurants_in_db)


#----------------------------------------------------------------------------#

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    #make sure templates, etc. are not cached in debug mode
    #app..jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
