"""Functions to search restaurants in YELP API"""

import os

import requests

def search_restaurants_by_name(name, city = "San Francisco"):
    """Search restaurant by name and city in YELP API,
    the search in YELP is not precise, so normally there are more than one
    restaurant in the response.

    name(string)
    city(string) San Francisco by default

    Return json or NONE. Structure of json:

    {'businesses':[
                    {'id': value, 'name': value, 'rating': value,
                    'location': {'address1': value, 'zip_code': value}
                    }
                    {other restaurant}
                    ...
                ]
    'total': value
    'region': value
    }

    """

    url = "https://api.yelp.com/v3/businesses/search?categories=restaurants,bars,coffee&term={name}&location={city}".format(name=name, city=city)
    
    headers = {}

    headers["Authorization"] = "Bearer {API_KEY}".format(API_KEY=os.environ['YELP_API_KEY'])

    r = requests.get(url,headers=headers)

    if r.ok:
        return r.json()
    else:
        return None


def search_restaurants(city = "San Francisco"):
    """Search restaurants by city in YELP API

    city(string) San Francisco by default

    Return a list of json or NONE. Structure of the return:

    [
        {'businesses':[
                        {'id': value, 'name': value, 'rating': value,
                        'location': {'address1': value, 'zip_code': value}
                        }
                        {other restaurant} since limit
                        ...
                    ]
        'total': value
        'region': value
        }
        {another json} since num_requests
        ...
    ]

    """
    
    headers = {}

    headers["Authorization"] = "Bearer {API_KEY}".format(API_KEY=os.environ['YELP_API_KEY'])

    restaurants = []

    limit = 50

    # make the first request to get the first 50 restaurants 
    # (limit = 50 but without offset)
    url = "https://api.yelp.com/v3/businesses/search?categories=restaurants,bars,coffee&location={city}&limit={limit}".format(city=city, limit=limit)
    
    r = requests.get(url,headers=headers)

    if r.ok:
        j = r.json()
        restaurants.append(j)
    else:
        return None

    # make the rest of the requests starting from restaurant 51st 
    # (limit = 50 and offset = limit + 1)
    num_requests = 2

    offset = limit + 1

    i = 0
    while i < num_requests:
        url = "https://api.yelp.com/v3/businesses/search?categories=restaurants,bars,coffee&location={city}&limit={limit}&offset={offset}".format(city=city, limit=limit, offset=offset)
        
        r = requests.get(url,headers=headers)
        
        if r.ok:
            j = r.json()
            restaurants.append(j)
        
        offset += limit

        i += 1

    return restaurants
    
