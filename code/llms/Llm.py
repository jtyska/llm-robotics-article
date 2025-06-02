from abc import ABC, abstractmethod


class Llm(ABC):
    def __init__(self, params):
        self.__model_id = ""
        self.__params = params
        self.__context = []
        self.__model = None
    
    def clear_context(self):
        self.__context = []
        
    @abstractmethod
    def set_instruction(self, instruction):
        pass
    
    @abstractmethod
    def setup_model(self):
        pass

    @abstractmethod
    def send_prompt_context(self, prompt):
        pass

    @abstractmethod
    def send_single_prompt(self, prompt):
        pass

    @abstractmethod
    def get_last_response(self):
        pass
