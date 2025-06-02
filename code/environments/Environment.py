from abc import ABC, abstractmethod


class Environment(ABC):
    def __init__(self, json_path):
        self.__env = ""
        # Load config from file
        # Create environment
        pass

    @abstractmethod
    def create_environment(self):
        pass

    @abstractmethod
    def get_initial_observation(self):
        pass

    @abstractmethod
    def get_observation(self):
        pass

    @abstractmethod
    def set_action(self):
        pass
