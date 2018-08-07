def get_tip_in_dollars(price, tip_percentage):
    """Calculate tip in dollars, 
    price and tip in percentage given"""

    return round(price * tip_percentage/100,2)


def get_total_price(price, tip_percentage):
    """Calculate total price(after the tip), 
    price and tip in percentage given"""

    return round(price + get_tip_in_dollars(price, tip_percentage),2)
    

def get_price_per_diner(price, tip_percentage, diner = 1):
    """Calculate price per diner, 
    price and tip in percentage given"""
    
    return round(get_total_price(price, tip_percentage)/diner,2)