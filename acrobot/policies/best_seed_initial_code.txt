import random

def get_action(cos_theta1, sin_theta1, cos_theta2, sin_theta2, ang_vel_theta1, ang_vel_theta2):
    if cos_theta1 > 0.95 and ang_vel_theta1 < 2:
        return 0
    elif cos_theta1 > 0 and cos_theta1 < 0.5 and ang_vel_theta1 >= 2 and ang_vel_theta1 <= 8:
        return 0
    elif cos_theta1 < 0 and ang_vel_theta1 > 8:
        return 2
    elif -cos_theta1 - cos_theta2 * cos_theta1 + sin_theta2 * sin_theta1 > 0.5:
        if ang_vel_theta1 < 0:
            return 0
        else:
            return 1
    elif -cos_theta1 - cos_theta2 * cos_theta1 + sin_theta2 * sin_theta1 > 0.9:
        return 1
    elif cos_theta1 < -0.8 and ang_vel_theta1 > 8:
        return 2
    else:
        return random.randint(0, 2)