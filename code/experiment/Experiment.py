from abc import ABC, abstractmethod

from environments.EnvironmentFactory import EnvironmentFactory
from llms.LlmModelFactory import LlmModelFactory
from utils.Config import Config
from utils.DataManager import DataManager
from utils.Logger import Logger
import imageio
import os
import numpy as np

class Experiment(ABC):

    """
    :version: 0.1
    :author: Jonata Tyska Carvalho
    """

    def __init__(self, name, json_config_file, base_dir,results_path=""):
        self.__experiment_name = name
        self.__base_dir = base_dir
        self.__debug = True
        
        self.__instruction = ""

        self.__config = Config(json_config_file)
        
        if not hasattr(self.get_config().experiment, "estimate_reward_trials"):
            setattr(self.get_config().experiment,'estimate_reward_trials',1)
        
        self.estimation_reward = [0 for _ in range(self.get_config().experiment.estimate_reward_trials)]
        self.estimation_experience = ["" for _ in range(self.get_config().experiment.estimate_reward_trials)]
        
        if not hasattr(self.get_config().experiment, "generate_videos"):
            setattr(self.get_config().experiment,'generate_videos',True)
        
        self.__data_manager = DataManager(self,results_path)

        self.instantiate_environment()
        self.instantiate_llm_model()
        
        self.logger = Logger(self)
        
        if self.get_config().experiment.generate_videos:
            #this should be refactored for a VideoDataManager
            self.video_path = os.path.join("videos",base_dir)
            os.makedirs(self.video_path, exist_ok=True)
        
         
    
    def get_data_manager(self):
        return self.__data_manager
        
    def get_experiment_name(self):
        return self.__experiment_name
    
    def get_base_dir(self):
        return self.__base_dir
    
    def set_instruction(self, instruction):
        self.__instruction = instruction
    
    def get_instruction(self):
        return self.__instruction

    def get_config(self):
        return self.__config

    def instantiate_environment(self):
        self.__environment = EnvironmentFactory.get_environment(
            self.__config.environment)

    def get_environment(self):
        return self.__environment

    def instantiate_llm_model(self):
        self.__llm_model = LlmModelFactory.get_llm_model(self.__config.llm)

    def get_llm(self):
        return self.__llm_model

    def set_debug(self, boolean):
        self.__debug = boolean

    def run_experiment(self):
        #this is important because the llm models objects are shared among experiments and needs to be reset
        self.get_llm().clear_context()
        self.get_llm().set_instruction(self.__instruction)
        for trial_number in range(self.__config.experiment.num_trials):
            if self.__debug:
                self.logger.info(f"Starting trial {trial_number+1}/{self.__config.experiment.num_trials}...")

            self.before_run_trial(trial_number)

            trial_reward = self.run_trial(trial_number)
            
            self.after_run_trial(trial_number, trial_reward)

            if self.__debug:
                self.logger.info(f" ...trial {trial_number+1}/{self.__config.experiment.num_trials} finished.\n")

        self.__data_manager.save_results()

    def run_trial(self, trial_number):
        cum_reward = 0
        self.__data_manager.add_new_trial_data(trial_number)
        v_obs = []
        v_act = []
        v_rew = []
        worst_trial = 0
        worst_reward = None

        for v in range(self.__config.experiment.estimate_reward_trials):
            self.estimation_experience[v]="step number: observation; action; step reward\n"
            v_obs.append([])
            v_act.append([])
            v_rew.append([])
            
            step = 0
            trial_reward = 0
            
            if self.get_config().experiment.generate_videos:
                video_filename = f"{self.__config.llm.llm_id}_{self.__config.experiment.prompt}_s{self.__config.llm.seed}tpt{self.__config.llm.temperature}t{trial_number}v{v}".replace(":","_").replace("/","_")
                video_full_path = os.path.join(self.video_path,f"{video_filename}")
                video_writer = imageio.get_writer(video_full_path+".mp4", fps=30,macro_block_size=1, ffmpeg_log_level='error')

            observation = self.get_environment().get_initial_observation()
            while not self.get_environment().is_done():
                if self.get_config().experiment.generate_videos:
                    img = self.get_environment().render()
                    img = np.ascontiguousarray(img)
                    video_writer.append_data(img)

                # get the next action from the llm
                action = self.get_action_from_llm(observation)
                self.get_environment().set_action(action)

                self.before_step(step)

                self.get_environment().step()

                self.after_step(step)

                # accumulate the reward from each step
                step_reward = self.get_environment().get_reward()
                trial_reward += step_reward
                
                v_obs[v].append(observation)
                v_act[v].append(action)
                v_rew[v].append(step_reward)
                
                act = action[0] if type(action)==list else action
                self.estimation_experience[v]+=f"Step {step}: {', '.join([f'{x:.2f}' for x in observation])}; {act:.2f}; {step_reward:.2f}\n"                

                if self.__debug:
                    print(f"#--#--#--# Step {step}: Observation: {observation}; Action = {action}")

                # get the next observation
                observation = self.get_environment().get_observation()

                step += 1
            v_obs[v].append(observation)
            v_act[v].append(None)
            v_rew[v].append(self.get_environment().get_reward())
            self.estimation_experience[v]+=f"Step {step}: {', '.join([f'{x:.2f}' for x in observation])}; {act:.2f}; {step_reward:.2f}\n"


            if self.get_config().experiment.generate_videos:
                video_writer.close()
                os.rename(video_full_path+".mp4",video_full_path+"_r"+str(int(trial_reward))+".mp4")
            
            self.estimation_reward[v] = trial_reward

            if v==0:
                worst_reward = trial_reward
                best_reward = trial_reward
                self.best_estimation_trial = self.worst_estimation_trial = 0
            else:
                if trial_reward<worst_reward:
                    worst_reward = trial_reward
                    self.worst_estimation_trial = v
                elif trial_reward>best_reward:
                    best_reward = trial_reward
                    self.best_estimation_trial = v
            
            

            if self.__debug:
                self.logger.info(f"Trial {trial_number+1}: Reward = {trial_reward}")
            
            cum_reward += trial_reward
        
        #saving the data of the worst trial
        for i in range(len(v_obs[self.worst_estimation_trial])):
            self.__data_manager.record_step_data(v_obs[self.worst_estimation_trial][i], v_act[self.worst_estimation_trial][i], v_rew[self.worst_estimation_trial][i])
        
        cum_reward /= self.__config.experiment.estimate_reward_trials
        
        self.__data_manager.record_trial_reward(cum_reward)
        
        return cum_reward


    # these are the methods that have to be written for each experiment
    @abstractmethod
    def get_action_from_llm(self, observation):
        # this is the method responsible to defining a prompt, pass it to the llm model and get an action as answer
        pass

    def before_run_trial(self, trial_number):
        pass

    def after_run_trial(self, trial_number):
        pass

    def before_step(self, step):
        pass

    def after_step(self, step):
        pass
