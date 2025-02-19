import random

def get_action(cart_position, cart_velocity, pole_angle, pole_angular_velocity):
    if -5 <= cart_position <= 5 and -10 <= pole_angle <= 10:
        if cart_velocity > 2 or cart_velocity < -2:
            return 1 if cart_velocity > 0 else 2
        elif pole_angular_velocity > 5 or pole_angular_velocity < -5:
            return 1 if pole_angular_velocity > 0 else 2
    elif cart_position < -5 or cart_position > 5 or pole_angle < -10 or pole_angle > 10:
        if pole_angle > 2 and pole_angular_velocity > 3:
            return 2
        elif pole_angle < -2 and pole_angular_velocity < -3:
            return 1
        elif pole_angle > 6 or pole_angle < -6:
            return 2 if pole_angle > 0 else 1
    else:
        return 1 if cart_velocity >= 0 else 2

    return random.randint(1, 2)