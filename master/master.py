from slm.ollama import SLMModel
from slm.chatgroq import GroqModel
from system_prompts import master_prompt



class MasterAgent:
    def __init__(self, config):
        self.model = GroqModel(config["agents"]["master_orchestrator"]["model"])
        self.temperature = config["agents"]["master_orchestrator"]["temperature"]
        self.max_tokens = config["agents"]["master_orchestrator"]["max_tokens"]
        self.system_role = config["agents"]["master_orchestrator"]["system_role"]

    def plan(self, user_goal):
        messages = [
            {"role": "system", "content": master_prompt},
            {"role": "user", "content": user_goal}
        ]
        response = self.model.generate_response(messages)
        return response

