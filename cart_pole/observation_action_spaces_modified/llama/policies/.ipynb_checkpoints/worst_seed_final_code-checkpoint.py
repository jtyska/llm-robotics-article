import math
import random

def get_action(cos_theta1, sin_theta1, cos_theta2, sin_theta2, ang_vel_theta1, ang_vel_theta2):
    angle1 = math.atan2(sin_theta1, cos_theta1)
    angle2 = math.atan2(sin_theta2, cos_theta2)

    if abs(angle1 + angle2) < 0.05 and abs(ang_vel_theta1) < 0.2:
        action = 0 if (angle1 + angle2) > 0 else 2
    elif abs(angle1 + angle2) > 0.15:
        action = 0 if (angle1 + angle2) > 0 else 2
    elif ang_vel_theta1 > 0.5:
        action = 0
    elif ang_vel_theta1 < -0.5:
        action = 2
    else:
        action = 0 if (angle1 + angle2) > 0 else 2

    return action if action is not None else random.randint(0, 2)