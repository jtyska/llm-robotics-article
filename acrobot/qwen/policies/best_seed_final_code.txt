import math
import random

def get_action(cos_theta1, sin_theta1, cos_theta2, sin_theta2, ang_vel_theta1, ang_vel_theta2):
    angle1 = math.atan2(sin_theta1, cos_theta1)
    angle2 = math.atan2(sin_theta2, cos_theta2)

    angle_threshold = 0.05
    angular_velocity_threshold = 0.05

    if abs(angle1) > angle_threshold or abs(ang_vel_theta1) > angular_velocity_threshold:
        if ang_vel_theta1 > 0:
            action = 0  # Apply left torque
        else:
            action = 2  # Apply right torque
    else:
        action = 1  # No torque

    return action if action is not None else random.randint(0, 2)