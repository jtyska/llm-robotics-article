import random

def get_action(cart_position, cart_velocity, pole_angle, pole_angular_velocity):
    if pole_angle > 0.04:
        return 2
    elif pole_angle < -0.04:
        return 1
    elif pole_angular_velocity > 1.0:
        return 2
    elif pole_angular_velocity < -1.0:
        return 1
    elif cart_position > 0.10:
        return 2
    elif cart_position < -0.10:
        return 1
    else:
        return 2
    return random.randint(1, 2)