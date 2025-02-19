import random

def get_action(cart_position, cart_velocity, pole_angle, pole_angular_velocity):
    if pole_angle < -5:
        return 2
    elif pole_angle > 5:
        return 1
    elif cart_position < -5 and pole_angle <= 0:
        return 2
    elif cart_position > 5 and pole_angle >= 0:
        return 1
    elif (pole_angle < -2 and cart_velocity > 2) or (cart_position < -5):
        return 2
    elif (pole_angle > 2 and cart_velocity < -2) or (cart_position > 5):
        return 1
    elif pole_angular_velocity < 0:
        return 2
    elif pole_angular_velocity > 0:
        return 1
    else:
        return random.randint(1, 2)