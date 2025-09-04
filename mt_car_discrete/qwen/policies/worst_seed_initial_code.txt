import random

def get_action(car_position, car_velocity):
    if car_velocity <= 0 and car_position < -0.1:
        return 2
    elif car_velocity > 0 and car_position > -0.4:
        return 2
    elif car_velocity > 0 and (car_position == -0.5 or car_position < 0):
        return 1
    elif car_velocity > 0 and car_position >= 0.4:
        return 1
    elif car_velocity < 0 and car_position < 0:
        return 2
    else:
        return random.randint(0, 2)