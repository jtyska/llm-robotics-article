from environments.EnvironmentGym import EnvironmentGym


class EnvironmentFactory:
    @staticmethod
    def get_environment(config):
        """
        Factory method to return an instance of the appropriate Simulator based on the simulator_params.

        :param environment_params: A dictionary containing parameters for the environment, including "environment_name".
        :return: An instance of an environment class.
        """

        if config.environment_name == "gym":
            return EnvironmentGym(config)
        # elif environment_name == "webots":
        #    return EnvironmentWeBots(config)
        else:
            raise ValueError(
                f"Enviroment {config.environment_name} is not recognized.")
