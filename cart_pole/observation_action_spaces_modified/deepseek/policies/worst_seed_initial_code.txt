import random

def get_action(cart_position, cart_velocity, pole_angle, pole_angular_velocity):
    if abs(pole_angle) > 20 and pole_angle > 0:
        return 1
    elif abs(pole_angle) > 20 and pole_angle < 0:
        return 2
    elif abs(cart_position) > 15 and cart_position > 0:
        return 1
    elif abs(cart_position) > 15 and cart_position < 0:
        return 2
    elif pole_angle > 0 and pole_angular_velocity > 0:
        return 1
    elif pole_angle < 0 and pole_angular_velocity < 0:
        return 2
    else:
        return random.randint(1, 2)