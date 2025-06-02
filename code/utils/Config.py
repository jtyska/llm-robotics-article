import json


class Config:
    """
    Config class that reads the configuration from a JSON file or dictionary
    and dynamically creates attributes based on the keys found in the configuration,
    creating hierarchical Config objects for nested dictionaries.
    """

    def __init__(self, config_data):
        self.load_config(config_data)

    def load_config(self, config_data):
        # For each key-value pair, set it as an attribute.
        for key, value in config_data.items():
            if isinstance(value, dict):
                # Recursively create Config objects for nested dictionaries.
                setattr(self, key, Config(value))
            else:
                setattr(self, key, value)

    def __repr__(self):
        return f"<Config object: {self.__dict__}>"

    def get_config_dict(self):
        """Returns the current configuration as a dictionary."""
        config_dict = {}
        for key, value in self.__dict__.items():
            if isinstance(value, Config):
                # Recursively get dict
                config_dict[key] = value.get_config_dict()
            else:
                config_dict[key] = value
        return config_dict

    def update_config(self, key, value):
        """Updates the config dynamically by adding or modifying an attribute."""
        setattr(self, key, value)
