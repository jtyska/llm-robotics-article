import torch
from huggingface_hub import login, logout
from transformers import pipeline

from llms.Llm import Llm


class LlmHuggingFace(Llm):

    def __init__(self, config):
        self.__config = config

        self.__model_id = self.__config.llm_id
        # some models_id available on hugging face hub
        # meta-llama/Meta-Llama-3.1-8B-Instruct
        # meta-llama/Meta-Llama-3.1-70B-Instruct
        # mistralai/Mistral-7B-Instruct-v0.2

        self.__context = []

        if hasattr(config, "hugging_face_token"):
            self.__hugging_face_token = self.__config.hugging_face_token
        else:
            self.__hugging_face_token = "ADD YOUR HF TOKEN HERE"

        if hasattr(config, "max_new_tokens"):
            self.__max_new_tokens = self.__.config.max_new_tokens
        else:
            self.__max_new_tokens = 1300
            
        if not hasattr(self.__config, "temperature"):
            setattr(self.__config,'temperature',0.7)

        self.setup_model()

    def set_model_id(self, model_id):
        self.__model_id = model_id

    def setup_model(self):
        login(self.__hugging_face_token)

        self.__model = pipeline(
            "text-generation",
            model=self.__model_id,
            # improve this, not configurable yet through json
            model_kwargs={
                "torch_dtype": torch.bfloat16,
                "temperature": self.__config.temperature},
            device_map="auto"
        )

    def get_context(self):
        return self.__context

    def clear_context(self):
        self.__context = []

    def set_instruction(self, instruction):
        if instruction != "":
            self.__context.append({"role": "system", "content": instruction})

    def send_prompt_context(self, prompt):
        self.__context.append({"role": "user", "content": prompt})

        outputs = self.__model(self.__context, max_new_tokens=self.__max_new_tokens)

        self.__context.append(outputs[0]["generated_text"][-1])

        return outputs[0]["generated_text"][-1]["content"]

    def get_last_response(self):
        return self.__context[-1]["content"]

    def send_single_prompt(self, prompt):
        outputs = self.__model([{"role": "user", "content": prompt}], max_new_tokens=self.__max_new_tokens)
        return outputs[0]["generated_text"][1]["content"]

    def hugging_face_logout():
        logout()
