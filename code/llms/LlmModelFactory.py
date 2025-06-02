from llms.LlmHuggingFace import LlmHuggingFace
from llms.LlmOllama import LlmOllama
from llms.LlmHumanProxy import LlmHumanProxy


class LlmModelFactory:
    model = {}

    @staticmethod
    def get_llm_model(config):  # json object
        """
        Factory method to return an instance of the appropriate LLM model based on llm_params.

        :param llm_params: A dictionary containing parameters for the LLM, including "llm_type".
        :return: An instance of a class representing the LLM.
        """
        # json object
        # llm_type = llm_params.get("llm_type")
        llm_type = config.llm_type
        llm_id = config.llm_id

        # share llm objects, they are heavy! :)
        #if llm_id in LlmModelFactory.model:
        #    print(f"Model {llm_id} was already instantiated, reusing it.")
        #else:
        print(f"Model {llm_id} was not instantiated yet. Creating a new instance.")
        if llm_type == "huggingface":
            LlmModelFactory.model[llm_id] = LlmHuggingFace(config)
        elif llm_type == "ollama":
           LlmModelFactory.model[llm_id] = LlmOllama(config)
        elif llm_type == "human_proxy":
           LlmModelFactory.model[llm_id] = LlmHumanProxy(config)
        # elif llm_type == "openai":
        #    LlmModelFactory.model[llm_id] = LlmOpenAi(config)
        else:
            raise ValueError(f"LLM model type '{config.llm_type}' is not recognized.")

        return LlmModelFactory.model[llm_id]
