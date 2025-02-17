import math
import random

def get_action(cos_theta, sin_theta, angular_velocity):
    theta = math.acos(cos_theta) * (1 if sin_theta >= 0 else -1)
    
    angle_threshold = math.pi / 3.5
    velocity_threshold = 0.6
    
    if abs(theta) > angle_threshold:
        if cos_theta < 0:  # Leaning left
            torque = min(1.8, max(-1.8, 1.4 + angular_velocity))
        else:  # Leaning right
            torque = min(1.8, max(-1.8, -1.4 - angular_velocity))
    elif abs(angular_velocity) > velocity_threshold:
        if angular_velocity > 0:  # Moving clockwise
            torque = min(2.0, max(-2.0, -1.3 * abs(angular_velocity)))
        else:  # Moving counterclockwise
            torque = min(2.0, max(-2.0, 1.3 * abs(angular_velocity)))
    else:
        if angular_velocity > 0:  # Moving clockwise
            torque = -0.7
        elif angular_velocity < 0:  # Moving counterclockwise
            torque = 0.7
        else:
            torque = 0.0
    
    return torque

def get_action(cos_theta, sin_theta, angular_velocity):
    theta = math.acos(cos_theta) * (1 if sin_theta >= 0 else -1)
    
    angle_threshold = math.pi / 3.5
    velocity_threshold = 0.6
    
    if abs(theta) > angle_threshold:
        if cos_theta < 0:  # Leaning left
            torque = min(1.8, max(-1.8, 1.4 + angular_velocity))
        else:  # Leaning right
            torque = min(1.8, max(-1.8, -1.4 - angular_velocity))
    elif abs(angular_velocity) > velocity_threshold:
        if angular_velocity > 0:  # Moving clockwise
            torque = min(2.0, max(-2.0, -1.3 * abs(angular_velocity)))
        else:  # Moving counterclockwise
            torque = min(2.0, max(-2.0, 1.3 * abs(angular_velocity)))
    else:
        if angular_velocity > 0:  # Moving clockwise
            torque = -0.7
        elif angular_velocity < 0:  # Moving counterclockwise
            torque = 0.7
        else:
            torque = 0.0
    
    return torque if torque is not None else random.uniform(-2, 2)