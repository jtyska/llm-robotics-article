import random

def get_action(car_position, car_velocity):
    if car_position < -0.5:
        return 0.3
    elif car_position > 0.3:
        return -0.3
    else:
        if car_velocity < -0.1:
            return 0.2 + 0.1 * car_velocity
        elif car_velocity > 0.1:
            return -0.2 - 0.1 * car_velocity
        else:
            return 0.1 * car_velocity

    return random.uniform(-1, 1)