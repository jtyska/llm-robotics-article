import pickle

import pandas as pd
import os
import time

from utils.Config import Config
from utils.TrialData import TrialData


class DataManager:
    """
    DataManager class that handles the management and saving of TrialData.
    This class is responsible for saving the list of trial data to disk.
    """

    def __init__(self, experiment,results_path):
        self.__experiment = experiment
        
        self.__results_path = results_path
        self.check_results_path() #create if it does not exist
        
        self.__trial_data = []
        
    def check_results_path(self):
        # Check if the results directory exists
        if not os.path.exists(self.__results_path):
            # Create the directory if it doesn't exist
            os.makedirs(self.__results_path)
            print(f"The results directory '{self.__results_path}' didn't exist and has been created.")

    def add_new_trial_data(self, trial_number):
        """Adds a new TrialData object to the list."""
        self.__trial_data.append(TrialData(trial_number))

    def record_step_data(self, observation, action, reward):
        """Adds Trial step data. By default it is added in the last trial object added to the list."""
        self.__trial_data[-1].record_obs_action_taken(observation, action, reward)

    def record_trial_reward(self, reward):
        self.__trial_data[-1].record_final_reward(reward)

    def get_trial_data(self,trial_number=None):
        """Returns the trial data list."""
        if trial_number is None:
            return self.__trial_data
        else:
            return self.__trial_data[trial_number]
    
    def get_last_trial_data(self):
        return self.__trial_data[-1]

    def flatten_config(self, config, parent_key='', sep='_'):
        """Recursively flattens the nested config structure."""
        items = {}
        for key, value in config.__dict__.items():
            new_key = f"{parent_key}{sep}{key}" if parent_key else key
            if isinstance(value, Config):  # If nested Config, recursively flatten
                items.update(self.flatten_config(value, new_key, sep=sep))
            else:
                items[new_key] = value
        return items

    def save_results(self):
        """Saves the trial data to disk in CSV and Pickle formats."""
        data = []
                
        #the literal results should go to the default values configuration (probably a singleton class)
        filename = os.path.join(self.__results_path,"results")

        # Iterate over each TrialData object and its corresponding trial number
        for trial in self.__trial_data:
            trial_number = trial.get_trial_number()
            step_data = trial.get_step_data()

            for step in step_data:
                data.append({
                    "trial_number": trial_number,
                    "step": step["step"],
                    "observation": step["observation"],
                    "action": step["action"],
                    "reward": step["reward"],
                    "cum_reward": step["cum_reward"]
                })

        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(data)
                
        # Dynamically flatten and add all the configuration parameters from self.__config
        config_dict = self.flatten_config(self.__experiment.get_config())

        # Add the flattened config parameters as columns in the DataFrame
        for key, value in config_dict.items():
            df[key] = value

        # If CSV file exists, read it and concatenate the new data
        csv_file = f"{filename}.csv"
        lock_file = f"{filename}.lock"

        # Wait for the lock to be released if it exists
        while os.path.exists(lock_file):
            time.sleep(1)  # Sleep briefly to avoid busy-waiting
        try:
            # Create the lock file
            open(lock_file, 'w').close()

            # If CSV file exists, read it and concatenate the new data
            if os.path.exists(csv_file):
                existing_df = pd.read_csv(csv_file)
                df = pd.concat([existing_df, df], ignore_index=True)

            # Save the DataFrame to a CSV file
            df.to_csv(csv_file, index=False)
        finally:
            # Remove the lock file to release the lock
            if os.path.exists(lock_file):
                os.remove(lock_file)
                
        #uncomment to save using pickle
        ## If Pickle file exists, load it and concatenate the new data
        #pickle_file = f"{filename}.pkl"
        #if os.path.exists(pickle_file):
        #    with open(pickle_file, 'rb') as f:
        #        existing_df = pickle.load(f)
        #        df = pd.concat([existing_df, df], ignore_index=True)

        # Save the DataFrame to a binary file (Pickle format)
        #with open(pickle_file, 'wb') as f:
        #    pickle.dump(df, f)
