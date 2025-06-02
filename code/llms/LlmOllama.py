import requests
import torch
import time
from huggingface_hub import login, logout
from transformers import pipeline

from llms.Llm import Llm


class LlmOllama(Llm):

    def __init__(self, config):
        self.__config = config

        self.__model_id = self.__config.llm_id
        # some models_id available on ollama UFSC server
        # meta-llama/Meta-Llama-3.1-8B-Instruct
        # meta-llama/Meta-Llama-3.1-70B-Instruct
        # mistralai/Mistral-7B-Instruct-v0.2
        
        if not hasattr(self.__config, "seed"):
            setattr(self.__config,'seed',99)
            
        if not hasattr(self.__config, "llm_id_coder"):
            setattr(self.__config,'llm_id_coder',self.__model_id)
            
        if not hasattr(self.__config, "temperature"):
            setattr(self.__config,'temperature',0.7)
        
        if not hasattr(self.__config, "server_address"):
            setattr(self.__config,'server_address',"YOUR SERVER ADDRESS HERE")
        
        self.base_url = self.__config.server_address

        #self.base_url = "https://ollama-dev.ceos.ufsc.br/api"
        #self.base_url = "http://dgx.vlab.ufsc.br:11434/api"
        #
        
        self.generate_url = f"{self.base_url}/generate"
        self.chat_url = f"{self.base_url}/chat"
        

        self.__context = []

        self.unload_model() #trying to avoid problems with prompt caching from previous experiments if the model was already loaded
        self.setup_model()

    def set_model_id(self, model_id):
        self.__model_id = model_id

    def setup_model(self):
        payload = {
            "model": self.__model_id
        }

        # Send the request to the Ollama API
        response = requests.post(self.generate_url, json=payload)

        # Check if the request was successful
        if response.status_code == 200:
            print(f"######### Model {self.__model_id} sucessfully loaded in the ollama server.")
        else:
            print(f"Error: {response.status_code}, {response.text}")

    def unload_model(self):
        payload = {
            "model": self.__model_id,
            "keep_alive": 0
        }

        # Send the request to the Ollama API
        response = requests.post(self.generate_url, json=payload)

        # Check if the request was successful
        if response.status_code == 200:
            print(f"######### Model {self.__model_id} sucessfully unloaded in the ollama server.")
        else:
            print(f"Error: {response.status_code}, {response.text}")            
            
    def get_context(self):
        return self.__context

    def clear_context(self):
        self.__context = []

    def set_instruction(self, instruction):
        if instruction != "":
            self.__context.append({"role": "system", "content": instruction})

    def send_prompt_context(self, prompt):
        self.__context.append({"role": "user", "content": prompt})

        # Define the payload, including the model and the conversation history
        payload = {
            "model": self.__model_id,
            "messages": self.__context,
            "stream": False
        }

        # Send the request to the Ollama API
        response = requests.post(self.chat_url, json=payload)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response and extract the LLM's reply
            response_data = response.json()
            output = response_data.get("response")
            
            # Add the LLM reply to the conversation history
            self.__context.append({"role": "assistant", "content": output})
        else:
            print(f"Error: {response.status_code}, {response.text}")

        return output

    def get_last_response(self):
        return self.__context[-1]["content"]

    def send_single_prompt(self, prompt,coder=False):
        payload = {
            "model": self.__model_id if not coder else self.__config.llm_id_coder,
            "prompt": prompt,
            "options":{
                "seed":self.__config.seed,
                "temperature":self.__config.temperature
            },
            "stream": False
        }
        
        #workaround for the endless loop that happens for qwen2.5
        #see https://github.com/open-webui/open-webui/issues/5538
        if "qwen2.5" in self.__model_id:
            payload["stop"] = '<|endoftext|>'

        for i in range(10):
            for j in range(10):
                # Send the request to the Ollama API
                try:
                    response = requests.post(self.generate_url, json=payload)
                    break
                except Exception as e:
                    print("########################################## ASDFSADFAS")
                    print(f"########################## Trying again in xyz seconds... trial #{j+1}")                
                    print(f"Generate URL: \n{self.generate_url}")
                    print(f"Error when sending prompt request to Ollama server: \n{str(e)}")
                    print(f"Prompt: \n{prompt}\n")
                    
                    print(f"########################## Error when sending prompt request to Ollama server: \n {str(e)}\n Prompt:\n {prompt} \nTrying again in 5 seconds... trial #{j+1}")                
                    
                    time.sleep(5)
                    
            # Check if the request was successful
            if response.status_code == 200:
                # Parse and print the response from the LLM
                response_data = response.json()
                output = response_data.get("response")
                break;                
            else:
                print(f"Error: \n{response.status_code}, {response.text}")
                print("##########################################")
                print(f"##################### Size of prompt in characters: {len(payload['prompt'])}")
                print("##########################################")
                print(f"########################## Trying again in 6 seconds... trial #{i+1}")                
                print("##########################################")
                time.sleep(6)                
        return output