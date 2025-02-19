import random

def get_action(cart_position, cart_velocity, pole_angle, pole_angular_velocity):
    if pole_angle > 0:
        return 2
    elif pole_angle < 0:
        return 1
    if cart_position >= 20:
        return 1
    elif cart_position <= -20:
        return 2
    if pole_angular_velocity > 10:
        return 2
    elif pole_angular_velocity < -10:
        return 1
    if cart_velocity > 10:
        return 1
    elif cart_velocity < -10:
        return 2
    if -5 <= pole_angle <= 5:
        if cart_velocity > 0:
            return 1
        elif cart_velocity < 0:
            return 2
    return random.randint(1, 2)