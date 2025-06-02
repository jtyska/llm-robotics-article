import argparse
import logging
import os
import shutil
import warnings

from transformers import logging as transformers_logging

from experiment.ExperimentSeries import ExperimentSeries

#clearing console
# For Windows
if os.name == 'nt':
    os.system('cls')
# For Linux/Mac
else:
    os.system('clear')
# hiding useless warnings - Set transformers logging to ERROR to suppress INFO messages
# comment this if you want to see the warnings
warnings.filterwarnings("ignore")
transformers_logging.set_verbosity_error()
os.environ['TF_ENABLE_ONEDNN_OPTS'] = "0"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = "3"
###


# Constants - substitute this by a json config file with the default parameters
EXPERIMENTS_DIR = 'user_experiments'
CONFIG_FILENAME = 'config.json'

RESULTS_ROOT = "results"
LOGS_DIR = 'logs'
VIDEO_DIR= 'videos'

# Step 1: Create an ArgumentParser object
parser = argparse.ArgumentParser(description="Run series of experiments")

# Step 2: Add the --name argument
parser.add_argument('--name', type=str, required=True, help=f"Name of the experiment. It has to be equal to the folder name in {EXPERIMENTS_DIR}")

# Add the --delete_previous_result flag
parser.add_argument('--delete_previous_data', action='store_true', help='Delete the previous data')

# Add the --append_result flag
parser.add_argument('--append_results', action='store_true', help='Append to the previous result')

# Step 3: Parse the arguments from the command line
args = parser.parse_args()

# Step 4: Check if the experiment folder exists and has the config.json file
experiment_folder = os.path.join(EXPERIMENTS_DIR, args.name)
config_file = os.path.join(experiment_folder, CONFIG_FILENAME)

if not os.path.exists(experiment_folder):
    print(f"Error: The experiment folder '{experiment_folder}' does not exist.")
    exit(1)

if not os.path.isfile(config_file):
    print(f"Error: The config file '{CONFIG_FILENAME}' is missing in '{experiment_folder}'.")
    exit(1)
    
results_path = os.path.join(RESULTS_ROOT,args.name)
logs_path = os.path.join(LOGS_DIR,args.name)
videos_path = os.path.join(VIDEO_DIR,args.name)


# Check if the data directories contain files
if (os.path.exists(results_path) and any(os.scandir(results_path))) or (os.path.exists(logs_path) and any(os.scandir(logs_path))) or (os.path.exists(videos_path) and any(os.scandir(videos_path))):
    if args.delete_previous_data:
        while True:
            ans = input(f"ATTENTION: Are you sure you want to delete previous data from {args.name} experiment? (yes/no)")
            if ans.lower() not in ("yes","no"):
                print("Write yes or no")
            else:
                if ans.lower() == "no":
                    exit("Aborting by user request.")
                else:
                    break
        print(f"One or more data directories '{results_path};{logs_path};{videos_path}' are not empty. Deleting it by user request (--delete_previous_data).")
        if args.name != "": #just ensuring the root results directory won't be deleted
            if os.path.exists(results_path) and os.path.isdir(results_path):
                shutil.rmtree(results_path)
            if os.path.exists(logs_path) and os.path.isdir(logs_path):
                shutil.rmtree(logs_path)
            if os.path.exists(videos_path) and os.path.isdir(videos_path):
                shutil.rmtree(videos_path)

    else:
        if not args.append_results:
            print(f"Error: One or more data directories '{results_path};{logs_path};{videos_path}' are not empty. Please empty them before proceeding or use --delete_previous_data or --append_result.")
            exit(1)
        else:
            print(f"Appending results")
    
if not os.path.isdir(results_path):
    # Create the directory if it doesn't exist
    os.makedirs(results_path)
    print(f"The results directory '{results_path}' has been created.")
    
    
# Step 5: If everything is correct, create and run the ExperimentSeries
print(f"Running experiments for '{args.name}'...")
experiment_series = ExperimentSeries(config_file,results_path=results_path)
experiment_series.run_experiments()