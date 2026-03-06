from slm.chatgroq import GroqModel
from slm.ollama import OllamaModel

def get_slm(agent_config, global_config):
    # merge configs, agent_config takes precedence
    merged_config = {**global_config, **agent_config}
    provider = merged_config.get("provider", "ollama").lower()
    
    if provider in ["chatgroq", "groq"]:
        return GroqModel(merged_config)
    else:
        return OllamaModel(merged_config)