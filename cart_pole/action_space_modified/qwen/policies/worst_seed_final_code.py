import random

def get_action(cart_position, cart_velocity, pole_angle, pole_angular_velocity):
    if pole_angle > 0.15:
        return 2
    elif pole_angle < -0.15:
        return 1
    elif cart_position > 1.8:
        return 1
    elif cart_position < -1.8:
        return 2
    elif pole_angle > 0.07:
        return 2
    elif pole_angle < -0.07:
        return 1
    elif cart_position > 1.4:
        return 1
    elif cart_position < -1.4:
        return 2
    else:
        return random.randint(1, 2)