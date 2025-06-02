import os
import datetime

class Logger:
    """
    A Logger class to log messages either to the console or a log file.

    Attributes:
        log_to_console (bool): If True, logs will be displayed on the console.
        log_to_file (bool): If True, logs will be saved to a file.
        log_file_path (str): Path of the log file where messages are stored.
        experiment (Experiment): The experiment instance containing the config information.
    """
    
    def __init__(self, experiment, log_to_console=False, log_to_file=True, log_file_base=''):
        """
        Initializes the Logger instance with an Experiment.

        Args:
            experiment (Experiment): The Experiment instance containing the configuration.
            log_to_console (bool): If True, logs are shown on the console.
            log_to_file (bool): If True, logs are written to a log file.
            log_file_base (str): Base name of the log file (timestamp will be added).
        """
        self.experiment = experiment
        self.log_to_console = log_to_console
        self.log_to_file = log_to_file
        self.base_path = os.path.join("logs",self.experiment.get_base_dir(),self.experiment.get_experiment_name())
        os.makedirs(self.base_path, exist_ok=True)
        if log_file_base=='':
            config = self.experiment.get_config()
            log_file_base=f"{config.experiment.prompt}_{config.llm.llm_id.replace(':','_').replace('/','_')}S{config.llm.seed}Temp{config.llm.temperature}"
        self.log_file_path = os.path.join(self.base_path,self._create_timestamped_filename(log_file_base))

        # Initialize the log file with the experiment configuration
        if self.log_to_file:
            with open(self.log_file_path, 'w') as file:
                file.write(self._get_experiment_info_header())

    def _get_timestamp(self):
        """
        Generates a timestamp for the log entry.

        Returns:
            str: Current date and time in a formatted string.
        """
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def _create_timestamped_filename(self, base_name):
        """
        Creates a unique filename by appending a timestamp to the base name.

        Args:
            base_name (str): The base name for the log file.

        Returns:
            str: A unique log file name with the current timestamp.
        """
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"{base_name}_{timestamp}.txt"

    def _get_experiment_info_header(self):
        """
        Generates the log file header with experiment configuration details.

        Returns:
            str: A formatted string with the experiment's configuration details.
        """
        config = self.experiment.get_config()
        experiment_name = self.experiment.get_experiment_name()

        header = (f"--- Logging started at {self._get_timestamp()} ---\n"
                  f"Experiment: {experiment_name}\n"
                  "Configuration Parameters:\n")
        # Recursively log the config parameters
        header += self._recursive_config_parser(config)
        header += "---\n"
        return header

    def _recursive_config_parser(self, config, indent_level=0):
        """
        Recursively parses the configuration object and formats it into a string.

        Args:
            config (dict or object): The configuration object to be parsed.
            indent_level (int): The indentation level for nested configurations.

        Returns:
            str: A formatted string with all configuration parameters.
        """
        indent = '    ' * indent_level  # Indentation for readability
        config_str = ""

        if isinstance(config, dict):
            for key, value in config.items():
                if isinstance(value, (dict, list)):
                    config_str += f"{indent}{key}:\n"
                    config_str += self._recursive_config_parser(value, indent_level + 1)
                else:
                    config_str += f"{indent}{key}: {value}\n"
        elif isinstance(config, list):
            for index, item in enumerate(config):
                config_str += f"{indent}- Item {index}:\n"
                config_str += self._recursive_config_parser(item, indent_level + 1)
        else:
            config_str += f"{indent}{config}\n"

        return config_str

    def _log(self, level, message):
        """
        Internal method to format and handle the logging message.

        Args:
            level (str): The severity level of the log (e.g., INFO, WARNING, ERROR).
            message (str): The log message to be recorded.
        """
        timestamp = self._get_timestamp()
        log_message = f"[{timestamp}] [{level}] {message}"

        # Print to console
        if self.log_to_console:
            print(log_message)

        # Write to file
        if self.log_to_file:
            with open(self.log_file_path, 'a') as file:
                file.write(log_message + '\n')

    def info(self, message):
        """
        Logs an INFO level message.

        Args:
            message (str): The informational message to log.
        """
        self._log("INFO", message)

    def warning(self, message):
        """
        Logs a WARNING level message.

        Args:
            message (str): The warning message to log.
        """
        self._log("WARNING", message)

    def error(self, message):
        """
        Logs an ERROR level message.

        Args:
            message (str): The error message to log.
        """
        self._log("ERROR", message)