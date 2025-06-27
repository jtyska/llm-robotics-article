from experiment.Experiment import Experiment
import random
import numpy as np
import types
import traceback
import re

class CreateStrategyCompareUpdateDiscretized(Experiment):
    def __init__(self,   name, json_config_file="",base_dir="",results_path=""):
        super().__init__(name, json_config_file,base_dir,results_path)
        
        self.logger.log_to_console = True
        
        self.task_description = """Consider that you are embodied in the following agent and environment. 
        
Agent: A cart over a track that has an unactuated pole attached to it. A force can be applied to the cart, left or right, to counteract the passive movement of the pole.
        
Goal: Keep the pole balanced upright as long as possible to a maximum of 500 time steps.

Observation state: A 4D vector in the following order:

Cart position, Cart velocity, Pole angle,Pole angular velocity
        
All observation variables are integer values between -50 and 50;
        
Action: Discrete:
1=move left(1)
2=move right(2)        

Negative values mean left direction, positive values right direction.

Failure Conditions: 
- Pole angle exceeds the range [-25,25]
- Cart position exceeds the range [-25,25]
"""
        
        self.trial_reward = []
        
        self.overall_strategy_reasoning = ""
        self.overall_strategy_code = ""
        self.overall_strategy_rules = ""
        self.examples = ""
        
        self.previous_overall_strategy_reasoning = ""
        self.previous_overall_strategy_code = ""
        self.previous_overall_strategy_rules = ""
        self.previous_examples = ""
        
        self.best_reward = None
        self.best_overall_strategy_reasoning = ""
        self.best_overall_strategy_code = ""
        self.best_overall_strategy_rules = ""
        self.best_examples = ""
                        
        if not hasattr(self.get_config().experiment, "steps_memory"):
            setattr(self.get_config().experiment,'steps_memory',50)
        
        #self.set_instruction("""You are an embodied agent and you will have to perform a given task.
        #""")
        
    def remove_thinking(self,input_string):
        # Regular expression to match <think>...</think> and remove it
        pattern = r"<think>.*?</think>"
        return re.sub(pattern, "", input_string, flags=re.DOTALL)

    def create_overall_strategy_reasoning(self,debug=False):
        self.logger.info("### Getting overall strategy reasoning from the LLM...")
        reasoning_prompt = f"""          
            The task description is: {self.task_description}
                      
            Briefly reflect on what could be a possible overall strategy to succeed in this task. Create a set of a few IF-THEN-ELSE rules relating the observations to the action definition. Do not use any reference to previous actions or reverse actions. The action at each time step should be defined based only on the current observation and should be either left(1) or right(2).
            """
         
        self.logger.info(reasoning_prompt)
        self.overall_strategy_reasoning = self.get_llm().send_single_prompt(reasoning_prompt)
        self.logger.info(f"############## LLM Overall strategy reasoning\n{self.overall_strategy_reasoning}")
    
    def get_rules_from_reasoning(self):
        self.logger.info("### Getting overall strategy rules from the LLM...")
        rules_prompt = f"""           
            The task description is: {self.task_description}
            
            Based on the following reasoning\n{self.overall_strategy_reasoning}
            
            Extract the IF-THEN-ELSE rules from the reasoning. Do not use any reference to previous actions or reverse actions. The action at each time step should be defined based only in the current observation and should be either left(1) or right(2). Your response should contain only the rules, no other explanation.
            """
        self.logger.info(rules_prompt)
        self.previous_overall_strategy_rules = self.overall_strategy_rules
        self.overall_strategy_rules = self.remove_thinking(self.get_llm().send_single_prompt(rules_prompt))
        self.logger.info(f"############## LLM Overall strategy rules\n{self.overall_strategy_rules}")
    
    def get_code_from_rules(self,trial_failed=False,add_mid="",add_end=""):
        prompt = f"""           
            The task description is: {self.task_description}
                        
            Here are a set of IF-THEN-ELSE rules for choosing the action based on the observation variables.
            
            {self.overall_strategy_rules}
            
            {add_mid}
            
        Represent these same rules in a function using python code. The signature of the function should be get_action(cart_position, cart_velocity, pole_angle,pole_angular_velocity), the inputs are the four observation values and the function returns the action value (1 for left; or 2 for right) using the rules above. Add a default random action (return random.randint(1, 2)) at the end of the function if no rule is used. Your response should contain only the function definition using python code. No other text or explanation, neigher formatting characters, only plain python code.
        
            {add_end}
            """
        
        if trial_failed:
            prompt += "\nYour previous python code did not work. Make sure your response will have only functional python code. No other explanation.\n"
        else:
            self.previous_overall_strategy_code = self.overall_strategy_code
        self.logger.info(prompt)
        self.overall_strategy_code = self.get_llm().send_single_prompt(prompt,coder=True).replace("```python","").replace("```","")
        self.logger.info(f"############## LLM Overall strategy code \n{self.overall_strategy_code}")
         
    def update_overall_strategy_reasoning(self,failed_reasoning=False,trial_number=1,add_end=""):
        self.logger.info("########### Getting updated overall strategy from the LLM...")
        prompt = f"""            
            The task description is:\n{self.task_description}
            
            {"" if trial_number < 2 else f'You already tried {trial_number} different strategies , and the sequence of rewards was: {self.trial_reward}'}

            Your current overall strategy was this one:\n{self.overall_strategy_rules} 
            
            Your experience with this strategy was:\n{self.examples}
            """
        if trial_number>1:
            prompt+=f"""
               Your previous overall strategy was this one:\n{self.previous_overall_strategy_rules} 
               Your experience with this strategy was:\n{self.previous_examples}
            """
            if self.overall_strategy_rules==self.best_overall_strategy_rules:
                prompt+="\nYour best strategy so far is the current strategy.\n"
            elif self.previous_overall_strategy_rules==self.best_overall_strategy_rules:
                prompt+="\nYour best strategy so far was the previous strategy.\n"
            else:
                prompt+=f"""
                   Your best overall strategy so far was this one:\n{self.best_overall_strategy_rules} 
                   Your experience with this strategy was:\n{self.best_examples}
                """
        prompt += f"""            
            Briefly reflect on your recent experiences acting on the environment with different strategies, check if your assumptions were true and which one performed the best. Choose some observations and reflect if the action taken was correct for achieving your goal, and also if they produced the effect you expected. Based on your analysis, choose the most effective strategy and update the rules for keeping the pole balanced for longer. Feel free to create a new strategy from scratch if you feel your previous strategies did not work as you desired.
            
            {add_end}
            
            """
        if failed_reasoning: prompt += "\nConsider that your last reasoning failed to produce a valid action based on observations. Make sure that your rules will produce an action that should be either 1 (left) or 2 (right).\n"
        self.logger.info(prompt)
        self.previous_overall_strategy_reasoning = self.overall_strategy_reasoning
        self.overall_strategy_reasoning = self.get_llm().send_single_prompt(prompt)
        self.logger.info(f"############## LLM UPDATED Overall strategy reasoning\n{self.overall_strategy_reasoning}")

        #self.logger.info(self.overall_strategy)
        
    def get_action_from_llm(self, observation):
        action = None
        cart_pos,cart_vel,pole_ang,pole_ang_vel = self.normalize_and_discretize(observation)                
        for count in range(10):#get_action execution errors protection
            try:
                action = get_action(cart_pos,cart_vel,pole_ang,pole_ang_vel)
                break
            except Exception as e:
                self.logger.error("#######################################################################")
                self.logger.error(f"######### EXECUTION ERROR get_action function failed run - asking the LLM for a fix #{count} ##############")
                self.logger.error("#######################################################################")
                trace = traceback.format_exc()
                self.logger.error(trace)
                self.update_overall_strategy_reasoning(add_end=f"Your previous reasoning lead to a code that generated the following error: \n{trace}\n")
                self.get_rules_from_reasoning()
                self.get_code_from_rules(add_mid=f"Your previous code was \n{self.overall_strategy_code}\n But it generated the following execution error \n{trace}\n")
                self.define_get_action(self.overall_strategy_code)
        
        for count in range(10):
            if action is None or get_action(cart_pos,cart_vel,pole_ang,pole_ang_vel) not in (1,2): #set a random action and reason again to regenerate the data                
                self.logger.error("#######################################################################")
                self.logger.error(f"######### INVALID ACTION RETURNED get_action function failed to return a valid action - trying again #{count} ##############")
                self.logger.error("#######################################################################")
                self.logger.error(f"############# OBS = {cart_pos,cart_vel,pole_ang,pole_ang_vel}; get_action return = {get_action(cart_pos,cart_vel,pole_ang,pole_ang_vel)}; action = {action}")
                self.update_overall_strategy_reasoning(add_end=f"Your previous reasoning generated an invalid action, it should be 1 (left) or 2 (right) but it was {action}")
                self.get_rules_from_reasoning()
                self.get_code_from_rules()
                self.define_get_action(self.overall_strategy_code)
                action = get_action(cart_pos,cart_vel,pole_ang,pole_ang_vel)
            else:
                break
        
        if count==10:
            self.logger.error(f"############# TOO MANY ATTEMPTS OF GENERATING A PROPER ACTION - STOPPING THE EXPERIMENT WITH THE FOLLOWING CONFIGS {self.get_config()}")
            exit(-1)
            
        return get_action(cart_pos,cart_vel,pole_ang,pole_ang_vel)-1
            
    
    def before_run_trial(self, trial_number):
        self.episode_sequence = []
        
        if trial_number == 0:
            self.create_overall_strategy_reasoning()
        else:
            if self.trial_reward[-1] < 500:                
                self.update_overall_strategy_reasoning(trial_number=trial_number)
            else:
                self.logger.info("##### ::::::: ######## Last trial got max reward and the LLM was not asked to generate a new strategy ##################")
        
        if len(self.trial_reward)==0 or self.trial_reward[-1] < 500:
            self.get_rules_from_reasoning()
            self.get_code_from_rules()
        
        #create the control function
        for i in range(10):
            try:
                self.define_get_action(self.overall_strategy_code) #this executes the code provided by the LLM, creating the function get_action(obs)
                break;
            except Exception as e:
                self.logger.error(f"Trial #{i} - Code: \n{self.overall_strategy_code}\n; Error\n {str(e)}")
                self.get_code_from_rules(add_end=f"""
Your last code was: 
{self.overall_strategy_code}
and it generated the following error:
{str(e)}
""") #try to execute again adding to the prompt the fact that it didn't work
                
    def get_last_steps_history(self):
        history = ""
        history_size = len(self.episode_sequence) 
        if history_size == 0:
            history = "The trial is starting. There is no sequence of observations and actions yet."
        elif history_size >= self.get_config().experiment.steps_memory:
            history = "\n".join(self.episode_sequence[-self.get_config().experiment.steps_memory:])
        else:
            history = "\n".join(self.episode_sequence)
        return history
    

    def after_run_trial(self, trial_number, trial_reward):
        obs_hist,act_hist = self.get_data_manager().get_last_trial_data().get_last_steps_obs_action(self.get_config().experiment.steps_memory)

        for i in range(len(obs_hist)):
            self.episode_sequence.append(f"\n{self.normalize_and_discretize(obs_hist[i])};{None if act_hist[i] is None else act_hist[i]+1}")

        self.trial_reward.append(trial_reward)
        self.previous_examples = self.examples
        self.examples = f"""
            Last {self.get_config().experiment.steps_memory if len(self.episode_sequence)>int(self.get_config().experiment.steps_memory) else len(self.episode_sequence)} steps from a trial using this strategy. The average reward in {self.get_config().experiment.estimate_reward_trials} trials was {trial_reward}/500
                {self.get_last_steps_history()}
        """
        if self.best_reward is None or trial_reward >= self.best_reward:
            self.best_reward = trial_reward
            self.best_examples = self.examples
            self.best_overall_strategy_reasoning = self.overall_strategy_reasoning
            self.best_overall_strategy_code = self.overall_strategy_code
            self.best_overall_strategy_rules = self.overall_strategy_rules
        
    def define_get_action(self, func_str):
        # Execute the function definition string
        exec(func_str, globals())
        
        # Bind the dynamically created function to the instance
        # Assume the function's name is get_action (as defined in the string)
        self.get_action = types.MethodType(get_action, self)
        

    def before_step(self, step):
        pass

    def after_step(self, step):
        pass

    def normalize_and_discretize(self, observation):
        # Define the ranges for each observation
        # [Cart Position, Cart Velocity, Pole Angle, Pole Angular Velocity]
        min_values = np.array([-4.8, -3, -0.418, -3])
        # [Cart Position, Cart Velocity, Pole Angle, Pole Angular Velocity]
        max_values = np.array([4.8, 3, 0.418, 3])

        # Normalize the observation to range [0, 1]
        normalized_observation = (observation - min_values) / (max_values - min_values)

        # Scale the normalized values to the range [0, 100]
        scaled_observation = normalized_observation * 100

        # Discretize by rounding to the nearest integer
        discretized_observation = np.round(scaled_observation).astype(int)-50

        return discretized_observation
