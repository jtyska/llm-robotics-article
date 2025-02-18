import random

def get_action(cart_position, cart_velocity, pole_angle, pole_angular_velocity):
    if pole_angle > 0.2:
        return 1
    elif pole_angle < -0.2:
        return 2
    if cart_position < -2.4:
        return 2
    elif cart_position > 2.4:
        return 1
    if pole_angular_velocity < -0.5 and pole_angle < -0.3:
        return 2
    elif pole_angular_velocity > 0.5 and pole_angle > 0.3:
        return 1
    if cart_velocity < -1.5:
        return 2
    elif cart_velocity > 1.5:
        return 1
    if -0.1 <= pole_angle <= 0.1 and -1 <= cart_position <= 1:
        if cart_velocity > 0:
            return 1
        else:
            return 2
    return random.randint(1, 2)