import random

def get_action(cart_position, cart_velocity, pole_angle, pole_angular_velocity):
    if pole_angle > 0.1:
        return 2
    elif pole_angle < -0.1:
        return 1
    elif cart_position > 1.8:
        return 1
    elif cart_position < -1.8:
        return 2
    elif pole_angle > 0:
        return 2
    else:
        return 1
    return random.randint(1, 2)