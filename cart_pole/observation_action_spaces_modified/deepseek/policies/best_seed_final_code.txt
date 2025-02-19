import random

def get_action(cart_position, cart_velocity, pole_angle, pole_angular_velocity):
    if pole_angular_velocity > 9:
        action = 2
    elif pole_angular_velocity < -9:
        action = 1
    elif pole_angle > 1:
        action = 2
    elif pole_angle < -1:
        action = 1
    elif cart_position > 10:
        action = 1
    elif cart_position < -10:
        action = 2
    else:
        action = random.randint(1, 2)
    return action