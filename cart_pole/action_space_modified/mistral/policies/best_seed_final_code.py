import random

def get_action(cart_position, cart_velocity, pole_angle, pole_angular_velocity):
    dynamic_threshold = 0.5 if abs(cart_velocity) < 2 else 1.0

    if abs(pole_angle) > dynamic_threshold:
        return 2 if pole_angle > 0 else 1

    weighted_integral_error = (pole_angle * 0.7) + (pole_angular_velocity * 0.3)
    if weighted_integral_error > 0.5:
        return 2
    elif weighted_integral_error < -0.5:
        return 1

    if abs(cart_velocity) > 2:
        damping_factor = 0.8 if (cart_velocity * pole_angle) > 0 else 1.2
        return int(damping_factor * cart_velocity / abs(cart_velocity))

    adaptive_control = (pole_angle + pole_angular_velocity + cart_velocity) / 3
    if adaptive_control > 0:
        return 2
    elif adaptive_control < 0:
        return 1

    return random.randint(1, 2)