import math
import random

def get_action(cos_theta, sin_theta, angular_velocity):
    theta = math.atan2(sin_theta, cos_theta)
    
    if abs(theta) > math.pi / 4:
        if cos_theta < 0:
            torque = min(2.0, 1.5 * abs(cos_theta))
        elif cos_theta > 0:
            torque = max(-2.0, -1.5 * abs(cos_theta))
    else:
        if angular_velocity > 0:
            torque = max(-2.0, -0.5 * angular_velocity)
        elif angular_velocity < 0:
            torque = min(2.0, 0.5 * abs(angular_velocity))
        else:
            if cos_theta < 0:
                torque = min(2.0, 0.1 * abs(cos_theta))
            elif cos_theta > 0:
                torque = max(-2.0, -0.1 * abs(cos_theta))
    return torque if torque is not None else random.uniform(-2, 2)