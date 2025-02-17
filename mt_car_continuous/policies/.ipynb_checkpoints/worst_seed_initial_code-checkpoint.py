import random

def get_action(car_position, car_velocity):
    if car_position < -0.1:  # Low position
        if car_velocity < 0:
            return 0.8  # Apply a positive force to start building momentum
        else:
            return 0.5  # Continue accelerating forward with moderate force

    elif -0.1 <= car_position < 0.3:  # Medium position
        if car_velocity < 0:
            return 0.6  # Apply a moderate positive force to help overcome the valley
        else:
            return 0.3  # Maintain momentum with less intensity

    elif 0.3 <= car_position < 0.4:  # High position
        if car_velocity < 0:
            return 0.5  # Help regain momentum
        else:
            return 0.2  # Fine-tune approach to the goal

    elif car_position >= 0.4:  # Near the goal
        if car_velocity < 0:
            return 0.3  # Ensure it reaches the goal without overshooting
        else:
            return 0.1  # Apply a very small positive force or zero force

    else:  # At the goal
        return 0.0  # No force needed as the goal is reached

    return random.uniform(-1, 1)  # Default random action if no rule is used