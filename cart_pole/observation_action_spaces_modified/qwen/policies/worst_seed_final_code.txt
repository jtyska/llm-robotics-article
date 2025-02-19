import random

def get_action(cart_position, cart_velocity, pole_angle, pole_angular_velocity):
    if abs(pole_angle) > 15:
        return 1 if pole_angle < 0 else 2
    elif abs(cart_position) > 24:
        return 1 if cart_position < 0 else 2
    elif abs(pole_angular_velocity) > 5:
        return 1 if pole_angular_velocity < 0 else 2
    elif abs(cart_velocity) > 5:
        return 1 if cart_velocity < 0 else 2
    elif abs(pole_angle) > 3 or abs(pole_angular_velocity) > 2:
        return 1 if pole_angle < -3 or pole_angular_velocity < -2 else 2
    elif cart_velocity > 0.5:
        return 2
    elif cart_velocity < -0.5:
        return 1
    else:
        return random.randint(1, 2)