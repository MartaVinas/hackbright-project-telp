"""Load restaurant data into database."""

from model import Restaurant, Meal, Admin, connect_to_db, db
from server import app

#---------------------------------------------------------------------#

#def get_restaurants():
"""Load restaurants from YELP into database."""

    #restaurant = Restaurant(yelp_restaurant_id=,
    #                 name=,
    #                 address=,
    #                 zipcode=,
    #                 rating=)

    # db.session.add(restaurant)

    # db.session.commit()

#def get_meals():
"""Load meals into database."""

    #meal = Restaurant(yelp_restaurant_id=,
    #                 zipcode=,
    #                 meal_type=,
    #                 price=,
    #                 percentage_tip=,
    #                 date=)

    # db.session.add(meal)

    # db.session.commit()

#---------------------------------------------------------------------#

if __name__ == '__main__':
    connect_to_db(app)
    db.create_all()

    #get_restaurants()

    #get_meals()