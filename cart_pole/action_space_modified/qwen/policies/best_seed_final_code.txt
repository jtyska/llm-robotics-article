import random

def get_action(cart_position, cart_velocity, pole_angle, pole_angular_velocity):
    if pole_angle < -0.05:
        return 1
    elif pole_angle > 0.05:
        return 2
    elif pole_angular_velocity < -0.3:
        return 1
    elif pole_angular_velocity > 0.3:
        return 2
    elif cart_position < -1.8:
        return 2
    elif cart_position > 1.8:
        return 1
    elif cart_velocity < -0.5:
        return 1
    elif cart_velocity > 0.5:
        return 2
    else:
        if pole_angular_velocity < -0.15:
            return 1
        elif pole_angular_velocity > 0.15:
            return 2
        elif cart_velocity < -0.3:
            return 1
        elif cart_velocity > 0.3:
            return 2
        else:
            return random.randint(1, 2)