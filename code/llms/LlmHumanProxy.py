import requests
import torch
import time
from huggingface_hub import login, logout
from transformers import pipeline

from llms.Llm import Llm

class LlmHumanProxy(Llm):

    def __init__(self, config):
        self.__config = config

        self.__model_id = self.__config.llm_id
        # some models_id available on ollama UFSC server
        # meta-llama/Meta-Llama-3.1-8B-Instruct
        # meta-llama/Meta-Llama-3.1-70B-Instruct
        # mistralai/Mistral-7B-Instruct-v0.2
        
        if not hasattr(self.__config, "seed"):
            setattr(self.__config,'seed',99)      

        self.__context = []

        self.setup_model()

    def set_model_id(self, model_id):
        self.__model_id = model_id

    def setup_model(self):
        pass

    def get_context(self):
        return self.__context

    def clear_context(self):
        self.__context = []

    def set_instruction(self, instruction):
        if instruction != "":
            self.__context.append({"role": "system", "content": instruction})

    def send_prompt_context(self, prompt):
        self.__context.append({"role": "user", "content": prompt})
        input(f"Paste the answer of the model {self.__model_id} in the file ClipBoardArea.txt and press enter\n")
        with open('ClipBoardArea.txt', 'r') as file:
            output = file.read()
        # Add the LLM reply to the conversation history
        self.__context.append({"role": "assistant", "content": output})
        
        return output

    def get_last_response(self):
        return self.__context[-1]["content"]

    def send_single_prompt(self, prompt):
        input(f"Paste the answer of the model {self.__model_id} in the file ClipBoardArea.txt and press enter\n")
        with open('ClipBoardArea.txt', 'r') as file:
            output = file.read()
        return output
