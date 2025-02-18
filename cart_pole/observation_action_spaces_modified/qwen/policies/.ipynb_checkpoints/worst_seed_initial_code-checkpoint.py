import random

def get_action(cos_theta1, sin_theta1, cos_theta2, sin_theta2, ang_vel_theta1, ang_vel_theta2):
    if abs(cos_theta1 + 1) < 0.1 and abs(cos_theta2 + 1) < 0.1 and abs(ang_vel_theta1) < 0.1 and abs(ang_vel_theta2) < 0.1:
        return 0
    elif abs(cos_theta1 + 1) < 0.1 and abs(cos_theta2 + 1) < 0.1 and (ang_vel_theta1 > 0 or ang_vel_theta2 > 0):
        return 1
    elif cos_theta1 < 0 and ang_vel_theta1 > 0:
        return 2
    elif cos_theta1 < -0.5 and ang_vel_theta1 < 0:
        return 0
    elif cos_theta1 > -0.5 and (cos_theta2 + cos_theta1 * cos_theta2 - sin_theta1 * sin_theta2) > 0:
        return 2
    elif cos_theta1 > -0.5 and (cos_theta2 + cos_theta1 * cos_theta2 - sin_theta1 * sin_theta2) < -0.5 and ang_vel_theta2 > 0:
        return 1
    elif cos_theta1 > -0.5 and (cos_theta2 + cos_theta1 * cos_theta2 - sin_theta1 * sin_theta2) > -0.5:
        return 2
    elif (cos_theta1 + cos_theta2 + cos_theta1 * cos_theta2 - sin_theta1 * sin_theta2) < 1.0 and (ang_vel_theta1 > 0 or ang_vel_theta2 > 0):
        return 2
    elif (ang_vel_theta1 > 12.567 - 0.1 or ang_vel_theta2 > 28.274 - 0.1) and ((cos_theta1 + cos_theta2 + cos_theta1 * cos_theta2 - sin_theta1 * sin_theta2) < 1.0):
        return 1
    else:
        return random.randint(0, 2)