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

#---------------------------------------------------------------------#

if __name__ == '__main__':
    connect_to_db(app)
    db.create_all()

    # new_rest = Restaurant(yelp_restaurant_id='rest', name='cafe', address='Sutton', zipcode='94118', rating=4.5)

    # db.session.add(new_rest)
    # db.session.commit()

    #get_restaurants()