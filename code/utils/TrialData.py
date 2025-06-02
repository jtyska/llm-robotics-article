class TrialData:

    def __init__(self, trial_number):
        self.__trial_number = trial_number
        self.__observation_action_history = []
        self.__cum_reward = 0

    def get_trial_number(self):
        return self.__trial_number

    def record_obs_action_taken(self, observation, action, reward):
        self.__observation_action_history.append({
            "step": len(self.__observation_action_history) + 1,
            "observation": observation,
            "action": action,
            "reward": reward
        })

    def record_final_reward(self, cum_rew):
        self.__cum_reward = cum_rew

    def get_step_data(self):
        # Return a list of dictionaries where each dictionary is a step (observation, action, reward) with the trial number
        return [
            {
                "step": step["step"],
                "observation": step["observation"],
                "action": step["action"],
                "reward": step["reward"],
                "cum_reward": self.__cum_reward
            }
            for step in self.__observation_action_history
        ]
    
    def get_last_steps_obs_action(self, num_steps=20):
        """
        Retrieve the actions taken in the last `num_steps` steps of the trial.

        :param num_steps: The number of recent steps to include. Defaults to 20.
        :return: A list of actions taken in the last `num_steps` steps.
        """
        if len(self.__observation_action_history)<num_steps: num_steps = len(self.__observation_action_history)
        
        # Extract the last `num_steps` from the history
        last_steps = self.__observation_action_history[-num_steps:]
        observations = [step["observation"] for step in last_steps]
        actions = [step["action"] for step in last_steps] 
        
        # Return only the actions
        return (observations,actions)
