import random

def get_action(cart_position, pole_angle, cart_velocity, pole_angular_velocity):
    if pole_angle > 0.1 and pole_angular_velocity > 0:
        action = -3.0 * min(1.0, abs(pole_angle) + abs(pole_angular_velocity) / 2)
    elif pole_angle < -0.1 and pole_angular_velocity < 0:
        action = 3.0 * min(1.0, abs(pole_angle) + abs(pole_angular_velocity) / 2)
    elif cart_position > 0.5:
        action = -1.5
    elif cart_position < -0.5:
        action = 1.5
    else:
        action = 0.0
    return action if action is not None else random.uniform(-3, 3)