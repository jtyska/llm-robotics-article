import random

def get_action(cart_position, pole_angle, cart_velocity, pole_angular_velocity):
    action = 0
    
    if pole_angle > 0.1:
        action = -2.5 * pole_angle
    elif pole_angle < -0.1:
        action = 2.5 * pole_angle
    else:
        action = 0

    if cart_position > 3.0:
        action = -2.5
    elif cart_position < -3.0:
        action = 2.5

    if cart_velocity > 1.0:
        action = -1.5
    elif cart_velocity < -1.0:
        action = 1.5

    if pole_angular_velocity > 1.0:
        action = -2.0 * pole_angle
    elif pole_angular_velocity < -1.0:
        action = 2.0 * pole_angle

    action = max(-3.0, min(3.0, action))
    
    return action if action is not None else random.uniform(-3, 3)