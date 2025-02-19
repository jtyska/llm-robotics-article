import random

def get_action(cart_position, cart_velocity, pole_angle, pole_angular_velocity):
    if pole_angle > 0:
        action = 1  # Move cart to the left to counteract right tilt
    else:
        action = 2  # Move cart to the right to counteract left tilt

    # Adjust based on angular velocity
    if abs(pole_angular_velocity) > 10:
        if pole_angle > 0 and pole_angular_velocity > 5:
            action = 1  # More aggressive move to the left
        elif pole_angle < 0 and pole_angular_velocity < -5:
            action = 2  # More aggressive move to the right

    # Adjust based on cart position
    if abs(cart_position) > 10:
        if cart_position > 10:
            action = 1  # Move cart to the left to stay within bounds
        elif cart_position < -10:
            action = 2  # Move cart to the right to stay within bounds

    # Adjust based on cart velocity
    if abs(cart_velocity) > 5:
        if cart_velocity > 5:
            action = 1  # Slow down by moving left
        elif cart_velocity < -5:
            action = 2  # Slow down by moving right

    return action