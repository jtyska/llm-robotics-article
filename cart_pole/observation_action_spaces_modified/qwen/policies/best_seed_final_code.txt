import random

def get_action(cart_position, cart_velocity, pole_angle, pole_angular_velocity):
    if pole_angle > 3 or pole_angular_velocity > 5:
        return 2
    elif pole_angle < -3 or pole_angular_velocity < -5:
        return 1
    elif cart_position >= 20 and pole_angle <= 0:
        return 1
    elif cart_position >= 20 and pole_angle > 0:
        return 2
    elif cart_position <= -20 and pole_angle >= 0:
        return 2
    elif cart_position <= -20 and pole_angle < 0:
        return 1
    elif cart_velocity > 5 or cart_velocity < -5:
        if pole_angle > 0:
            return 2
        elif pole_angle < 0:
            return 1
    elif pole_angle > 0:
        return 2
    elif pole_angle < 0:
        return 1
    else:
        return random.randint(1, 2)