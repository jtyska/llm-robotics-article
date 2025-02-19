import random

def get_action(cart_position, cart_velocity, pole_angle, pole_angular_velocity):
    if pole_angle <= -20:
        action = 2
    elif pole_angle >= 20:
        action = 1
    elif cart_position <= -15:
        action = 2
    elif cart_position >= 15:
        action = 1
    elif pole_angular_velocity > 5 and pole_angular_velocity > 0:
        action = 1
    elif pole_angular_velocity > 5 and pole_angular_velocity < 0:
        action = 2
    else:
        if cart_velocity > 0:
            action = 1
        elif cart_velocity < 0:
            action = 2
        else:
            action = random.randint(1, 2)
    return action