import math
import random

def get_action(cos_theta, sin_theta, angular_velocity):
    theta = math.atan2(sin_theta, cos_theta)
    
    if abs(theta) > math.pi / 4:
        torque = -1.5 * (theta + 0.1 * angular_velocity)
    elif abs(theta) > math.pi / 16:
        torque = -0.8 * (theta + 0.2 * angular_velocity)
    else:
        torque = -0.5 * angular_velocity
    
    torque = max(min(torque, 2), -2)
    
    return torque