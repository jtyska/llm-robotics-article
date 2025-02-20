import numpy as np
import random

def get_action(cart_position, pole_angle, cart_velocity, pole_angular_velocity):
    if abs(pole_angle) > 0.15 or abs(pole_angular_velocity) > 0.25:
        angle_factor = (abs(pole_angle) - 0.15) / (0.15 * 0.25)
        velocity_factor = (abs(pole_angular_velocity) - 0.25) / (0.25 * 0.25)
        factor = min(angle_factor + velocity_factor, 2.5)
    else:
        factor = 0

    bias = 0.15 * np.sign(pole_angle)
    damping = -0.3 * pole_angular_velocity

    action = 3.0 * pole_angle + 1.3 * pole_angular_velocity + 0.2 * cart_position + 3.5 * pole_angle * factor + bias + damping
    action = max(-3.0, min(3.0, action))
    
    return action if abs(pole_angle) < 0.2 and abs(cart_position) < float('inf') and abs(cart_velocity) < float('inf') and abs(pole_angular_velocity) < float('inf') else random.uniform(-3, 3)