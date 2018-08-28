"""Load restaurant data into database. Create fake meals in database"""

import random
from datetime import datetime

from model import Restaurant, Meal, Admin, connect_to_db, db
from server import app, add_restaurants_to_db
from yelp_requests import search_restaurants

#---------------------------------------------------------------------#

def get_restaurants():
    """Load restaurants from YELP into database."""
    
    jsons_restaurants_list = search_restaurants()

    for json_restaurants in jsons_restaurants_list:
        add_restaurants_to_db(json_restaurants)

def get_meals():
    """Load fake meals into database."""

    restaurants_in_db = db.session.query(
                        Restaurant.yelp_restaurant_id, 
                        Restaurant.zipcode, 
                        Restaurant.rating).all()

    meal_types = ['dinner', 'lunch']

    for restaurant in restaurants_in_db:

        (restaurant_id, zipcode, rating) = restaurant

        meal_type = random.choice(meal_types)

        price = round(random.uniform(10,80),2)

        percentatge_tip = create_tip_from_rating(rating)

        meal = Meal(yelp_restaurant_id=restaurant_id,
                        zipcode=zipcode,
                        meal_type=meal_type,
                        price=price,
                        percentage_tip=percentatge_tip,
                        date=datetime.now())

        db.session.add(meal)

    db.session.commit()


def create_tip_from_rating(rating):
    """create the percentage tip based on rating"""

    percentage_tip = 0

    if rating >= 5.0 :
        percentage_tip = random.randint(25,30)
    elif rating >= 4.5:
        percentage_tip = random.randint(20,25)
    elif rating >= 4.0:
        percentage_tip = random.randint(18,20)
    elif rating >= 3.5:
        percentage_tip = random.randint(15,18)
    elif rating >= 3.0:
        percentage_tip = random.randint(10,15)
    elif rating >= 2.5:
        percentage_tip = random.randint(5,10)
    else:
        percentage_tip = random.randint(0,5)

    return percentage_tip


#---------------------------------------------------------------------#

if __name__ == '__main__':
    connect_to_db(app)
    
    db.create_all()

    get_restaurants()

    get_meals()