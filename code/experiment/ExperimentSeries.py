import os
import importlib
import json
import itertools
import copy
import traceback

class ExperimentSeries:
    """
    This class runs a series of experiments based on combinations of parameters extracted from a JSON file.

    :version: 0.1
    :author: Jonata Tyska Carvalho
    """

    def __init__(self, json_config_file,results_path=""):
        """
        Initialize the ExperimentSeries by loading the configuration from the provided JSON file.

        :param json_config_file: Path to the JSON configuration file.
        """
        self.config_file = json_config_file
        self.config = self.load_config_from_json()
        self.experiments_dir = os.path.dirname(json_config_file)
        self.experiments = []
        self.results_path = results_path

        #self.instantiate_experiments(results_path)

    def load_config_from_json(self):
        """
        Load the configuration from the provided JSON file.
        """
        try:
            with open(self.config_file, 'r') as file:
                config = json.load(file)
            return config
        except FileNotFoundError:
            print(f"Error: Config file {self.config_file} not found.")
            return None
        except json.JSONDecodeError:
            print(f"Error: Failed to decode JSON from {self.config_file}.")
            return None

    def run_experiments(self):
        """
        Instantiate experiments based on all combinations of parameters from the JSON config.
        """
        if not self.config:
            print("No configuration loaded. Aborting.")
            return
        
        experiments_configs = self.generate_config_combinations()
        
        print("###########################################################################")
        print(f"#### A series of {len(experiments_configs)} experiments will be configured and run. ################")
        print("###########################################################################")
        
        for exp_config in experiments_configs:
            try:
                # Dynamically import the experiment class (PromptA or PromptB)
                experiment_module = importlib.import_module(f"{self.experiments_dir.replace(os.path.sep, '.')}.{exp_config['experiment']['prompt']}")
                experiment_class = getattr(experiment_module, exp_config["experiment"]["prompt"])

                # Instantiate the experiment class with the combined JSON config
                experiment_instance = experiment_class(exp_config["experiment"]["prompt"],exp_config,os.path.basename(self.experiments_dir),self.results_path)
                
                print(f"Running experiment: {experiment_instance.__class__.__name__} with the following config params {experiment_instance.get_config()}")
                experiment_instance.run_experiment()
                
                ## Append the experiment instance to the list
                #self.experiments.append(experiment_instance)
                #print(f'Instantiated experiment {exp_config["experiment"]["prompt_experiment"]} with {exp_config["experiment"]["num_trials"]} trials and LLM ID {exp_config["llm"]["llm_id"]}')
            except Exception as e:
                print(f"Error instantiating and running {exp_config['experiment']['prompt']}: {str(e)}")
                print("Detailed traceback:")
                traceback.print_exc()

    def generate_config_combinations(self):
        # Extract all experiment-related, llm-related, and environment-related parameters
        experiment_params = self.config['experiment']
        llm_params = self.config['llm']
        environment_params = self.config['environment']

        # Extract keys that contain lists from experiment and llm
        experiment_keys = [k for k, v in experiment_params.items() if isinstance(v, list)]
        llm_keys = [k for k, v in llm_params.items() if isinstance(v, list)]

        # Handle environment, assuming it could be a list of dictionaries (or any list)
        if isinstance(environment_params, list):
            environment_values = environment_params  # If it's a list of environments, keep as is
        else:
            environment_values = [environment_params]  # Otherwise, wrap the single environment in a list

        # Extract the values from experiment and llm sections that are lists
        experiment_values = [experiment_params[k] for k in experiment_keys]
        llm_values = [llm_params[k] for k in llm_keys]

        # Generate all combinations of experiment, llm, and environment parameters
        all_combinations = list(itertools.product(*experiment_values, *llm_values, environment_values))

        # Prepare a list to hold the structured output
        structured_combinations = []

        # Iterate over each combination and maintain the JSON structure
        for combination in all_combinations:
            # Copy the original configuration to preserve static parameters
            combined_config = copy.deepcopy(self.config)

            # Fill in the experiment part of the combination
            for i, key in enumerate(experiment_keys):
                combined_config['experiment'][key] = combination[i]

            # Fill in the llm part of the combination (starts after experiment params)
            for i, key in enumerate(llm_keys, len(experiment_keys)):
                combined_config['llm'][key] = combination[i]

            # Fill in the environment part of the combination (after experiment and llm params)
            combined_config['environment'] = combination[-1]  # Last item in combination corresponds to the environment

            # Append the structured config with maintained hierarchy
            structured_combinations.append(combined_config)

        return structured_combinations
