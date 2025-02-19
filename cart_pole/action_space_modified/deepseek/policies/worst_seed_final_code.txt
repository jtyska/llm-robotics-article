import random

def get_action(cart_position, cart_velocity, pole_angle, pole_angular_velocity):
    if cart_position > 2:
        return 2
    elif cart_position < -2:
        return 1
    elif pole_angle > 0 and pole_angular_velocity > 0:
        return 2
    elif pole_angle < 0 and pole_angular_velocity < 0:
        return 1
    elif cart_velocity > 10:
        return 1
    elif cart_velocity < -10:
        return 2
    else:
        return random.randint(1, 2)