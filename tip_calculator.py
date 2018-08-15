"""Functions to calculate tip in dollars, total price and price per diner"""


def get_tip_in_dollars(price, tip_percentage):
    """
    Calculate tip in dollars.

    price: cost in dollars
    tip_percentage: in percentage

    return float
    """

    return round(price * tip_percentage/100, 2)


def get_total_price(price, tip_percentage):
    """
    Calculate total price(after the tip).

    price: cost in dollars
    tip_percentage: in percentage

    return float
    """

    return round(price + get_tip_in_dollars(price, tip_percentage), 2)
    

def get_price_per_diner(price, tip_percentage, diner = 1):
    """
    Calculate price per diner.

    price: cost in dollars
    tip_percentage: in percentage
    diner: number of people paying (optional, default is 1)

    return float
    """
    
    return round(get_total_price(price, tip_percentage)/diner, 2)