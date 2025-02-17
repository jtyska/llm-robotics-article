
import random

def get_action(car_position, car_velocity):
    max_velocity = 1.0  # Assuming a maximum velocity for normalization
    
    if car_position < -0.4 and car_velocity < 0.05:
        return 0.8
    elif car_position > 0 and car_velocity > 0:
        return 0.5 + 0.3 * (car_velocity / max_velocity)
    elif car_position >= 0.4 and car_position < 0.45 and car_velocity > 0:
        return 0.2 + 0.3 * (car_velocity / max_velocity)
    elif car_position <= 0 and car_velocity < 0:
        return 0.8
    elif car_velocity > 0.5 and car_position < 0.45:
        return 0.2 + 0.1 * (car_velocity / max_velocity)
    elif car_position >= 0.45:
        return 0.1
    else:
        return random.uniform(-1, 1)