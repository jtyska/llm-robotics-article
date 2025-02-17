import random

def get_action(cart_position, pole_angle, cart_velocity, pole_angular_velocity):
    action = 0
    
    if pole_angle > 0.015:
        action = -2.2 * pole_angle
    elif pole_angle < -0.015:
        action = 2.2 * pole_angle
    else:
        action = 0

    if cart_position > 3.0:
        action += -1.3
    elif cart_position < -3.0:
        action += 1.3

    if cart_velocity > 1.5:
        action += -0.5 * cart_velocity
    elif cart_velocity < -1.5:
        action += 0.5 * cart_velocity

    if pole_angular_velocity > 0.4:
        action += -1.5 * pole_angle
    elif pole_angular_velocity < -0.4:
        action += 1.5 * pole_angle

    action = max(-3.0, min(3.0, action))

    if abs(action) > 2.5:
        action *= 0.85
    
    return action if action is not None else random.uniform(-3, 3)