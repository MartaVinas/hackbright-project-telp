"""Models and database functions for Telp project."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

################################################################################
# Model definitions #

class Restaurant(db.Model):
    """Restaurant"""

    __tablename__ = "restaurants"

    yelp_restaurant_id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    zipcode = db.Column(db.String(20), nullable=False)
    rating = db.Column(db.Float, nullable = False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return """<Restaurant: yelp_restaurant_id = {},
        name = {}, address = {}, zipcode = {}, rating = {}.>""".format(
            self.yelp_restaurant_id, 
            self.name, 
            self.address, 
            self.zipcode, 
            self.rating)


class Meal(db.Model):
    """Meal"""

    __tablename__ = "meals"

    meal_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True)
    yelp_restaurant_id = db.Column(db.String(100), db.ForeignKey('restaurants.yelp_restaurant_id'), nullable=False)
    zipcode = db.Column(db.String(20), nullable=False)
    meal_type = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable = False)
    percentage_tip = db.Column(db.Integer, nullable = False)
    date = db.Column(db.DateTime)

    # Define relationship to restaurant
    restaurant = db.relationship("Restaurant",
                           backref=db.backref("meals", order_by=meal_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return """<Meal: meal_id = {}, restaurant_id = {}, zipcode = {}, 
        meal_type = {}, price = {}, percentage_tip = {}, date = {}.>""".format(
            self.meal_id, 
            self.yelp_restaurant_id, 
            self.zipcode, 
            self.meal_type, 
            self.price, 
            self.percentage_tip, 
            self.date)


class Admin(db.Model):
    """Administrator."""

    __tablename__ = "admins"

    admin_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Admin: admin_id = {}, username = {}.>".format(
            self.admin_id, 
            self.username)


#####################################################################
# Helper functions

DB_URI = 'postgresql:///telp_test'
#DB_URI = 'postgresql:///telp'

def connect_to_db(app):
    """Connect the database to Flask app."""

    # Configure to use PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will
    # leave you in a state of being able to work with the database
    # directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")
