import random

def get_action(car_position, car_velocity):
    if abs(car_position) > 0.3:
        if car_position < -0.3 and car_velocity > 0:
            return 0.6 + 0.1 * (car_velocity / 1.0)
        elif car_position > 0.3 and car_velocity < 0:
            return -0.6 - 0.1 * (car_velocity / 1.0)
    else:
        if abs(car_position) < 0.1:
            if car_velocity > 0:
                return 0.4 + 0.2 * (car_velocity / 1.0)
            elif car_velocity < 0:
                return -0.4 - 0.2 * (car_velocity / 1.0)
        else:
            if car_position < -0.1 and car_velocity > 0:
                return 0.5 + 0.2 * (car_velocity / 1.0)
            elif car_position > 0.1 and car_velocity < 0:
                return -0.5 - 0.2 * (car_velocity / 1.0)
    if car_position < 0:
        return 0.1
    else:
        return -0.1
    return random.uniform(-1, 1)