"""Functions to search restaurants in YELP API"""

import os

import requests


def call_yelp_api(url):
    """Make a request to YELP API with url given.

    url(url string)

    return json or NONE
    """

    headers = {}

    headers["Authorization"] = "Bearer {API_KEY}".format(API_KEY=os.environ['YELP_API_KEY'])

    r = requests.get(url,headers=headers)

    if r.ok:
        return r.json()
    else:
        return None


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
                    },
                    {other restaurant}
                    ...
                ]
    'total': value
    'region': value
    }

    """

    url = "https://api.yelp.com/v3/businesses/search?categories=restaurants,bars,coffee&term={name}&location={city}".format(name=name, city=city)
    
    return call_yelp_api(url)


def search_restaurants_by_name_paginate(name, offset, city = "San Francisco"):
    """Search restaurant by name and city in YELP API,
    the search in YELP is not precise, so normally there are more than one
    restaurant in the response.

    name(string)
    offset(integer)
    city(string) San Francisco by default

    Return json or NONE. Structure of json:

    {'businesses':[
                    {'id': value, 'name': value, 'rating': value,
                    'location': {'address1': value, 'zip_code': value}
                    },
                    {other restaurant}
                    ...
                ]
    'total': value
    'region': value
    }

    """

    url = "https://api.yelp.com/v3/businesses/search?categories=restaurants,bars,coffee&term={name}&location={city}&offset={offset}".format(name=name, city=city, offset=offset)
    
    return call_yelp_api(url)


def search_restaurants(city = "San Francisco"):
    """Search restaurants by city in YELP API

    city(string) San Francisco by default

    Return a list of json or empty list. Structure of the return:

    [
        {'businesses':[
                        {'id': value, 'name': value, 'rating': value,
                        'location': {'address1': value, 'zip_code': value}
                        },
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

    restaurants = []

    limit =20

    num_requests = 2

    offset = 0

    i = 0
    while i < num_requests:
        url = "https://api.yelp.com/v3/businesses/search?categories=restaurants,bars,coffee&location={city}&limit={limit}&offset={offset}".format(city=city, limit=limit, offset=offset)
        
        j = call_yelp_api(url)
        
        if j is not None:
            restaurants.append(j)
        else:
            break
        
        offset += limit

        i += 1

    return restaurants


def search_restaurants_by_id(id_restaurant):
    """Search restaurant by id

    id_restaurant(string)

    Return json or NONE.

    """

    url = "https://api.yelp.com/v3/businesses/{id}".format(id=id_restaurant)
    
    return call_yelp_api(url)


    
