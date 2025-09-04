import random

def get_action(car_position, car_velocity):
    if car_position < 0 and car_velocity > 0:
        return 2  # Accelerate to the right
    elif car_position < 0 and car_velocity <= 0:
        return 0  # Accelerate to the left
    elif 0 <= car_position < 0.5 and car_velocity > 0:
        return 2  # Accelerate to the right
    elif 0 <= car_position < 0.5 and car_velocity <= 0:
        return 0  # Accelerate to the left
    elif car_position >= 0.5:
        return 1  # Do not accelerate (goal reached)
    else:
        return random.randint(0, 2)  # Default action: random