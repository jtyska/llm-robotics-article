import random

def get_action(cart_position, cart_velocity, pole_angle, pole_angular_velocity):
    if abs(pole_angle) > 15 or abs(pole_angular_velocity) > 30:
        action = 2 if pole_angle < -15 or pole_angular_velocity < -30 else 1
    elif abs(cart_position) > 4 or abs(cart_velocity) > 6:
        action = 2 if cart_position < -4 or cart_velocity < -6 else 1
    elif abs(pole_angle) > 5:
        action = 2 if (pole_angle < -5 and pole_angular_velocity < 0) or (pole_angle > 5 and pole_angular_velocity > 0) else 1
    elif abs(cart_position) > 3 or abs(cart_velocity) > 4.5:
        action = 2 if cart_position < -3 or cart_velocity < -4.5 else 1
    else:
        prediction = (cart_position * 0.4 +
                      cart_velocity * 0.3 +
                      pole_angle * 0.6 +
                      pole_angular_velocity * 0.7)
        action = 1 if prediction < 0 else 2
    return action