import gym
from environments.Environment import Environment
import os

class EnvironmentGym(Environment):
    def __init__(self, config):
        self.__done = False
        self.__config = config
        self.create_environment(self.__config)
        
        if not hasattr(self.__config, "mujoco_rendering"):
            setattr(self.__config,'mujoco_rendering',False)
        
        if not self.__config.mujoco_rendering:
            os.environ["MUJOCO_GL"] = "osmesa"

    def create_environment(self, config):
        self.__env = gym.make(config.task, render_mode=config.render_mode)

    def get_initial_observation(self):
        self.__initial_observation = self.__env.reset()[0]
        self.__last_reward = None
        self.__info = None
        self.__terminated = False
        self.__truncated = False
        return self.__initial_observation
    
    def step(self):
        self.__current_observation, self.__last_reward, self.__terminated, self.__truncated, self.__info = self.__env.step(self.__next_action)

    def get_observation(self):
        return self.__current_observation

    def get_reward(self):
        return self.__last_reward

    def is_done(self):
        return (self.__terminated or self.__truncated) 

    def get_info(self):
        return self.__info

    def set_action(self, action):
        self.__next_action = action
    
    def render(self):
        return self.__env.render()
        
