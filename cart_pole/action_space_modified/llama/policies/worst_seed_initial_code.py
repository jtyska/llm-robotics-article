import random

def get_action(cart_position, cart_velocity, pole_angle, pole_angular_velocity):
    if pole_angle < 0 and pole_angular_velocity < 0:
        return 1
    if cart_position > 1.5 or cart_velocity > 0:
        return 1
    if pole_angle > 0 and pole_angular_velocity > 0:
        return 2
    if cart_position < -1.5 or cart_velocity < 0:
        return 2
    else:
        if pole_angle > 0:
            return 2
        elif pole_angle < 0:
            return 1
    return random.randint(1, 2)