import subprocess
import sys

# Function to install requirements from requirements.txt


def install_requirements():
    try:
        # Run 'pip install -r requirements.txt'
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "setup_requirements.txt"])
        print("Requirements installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install requirements: {e}")

# Main setup function


def setup():
    install_requirements()


if __name__ == "__main__":
    setup()
