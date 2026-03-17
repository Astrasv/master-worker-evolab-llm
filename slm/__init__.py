from slm.chatgroq import GroqModel
from slm.ollama import OllamaModel
from slm.openrouter import OpenRouterModel

def get_slm(agent_config, config):
    active_provider = config.get("active_provider", "ollama").lower()
    provider_settings = config["llm_providers"][active_provider]
    
    model_alias = agent_config.get("model", "default")
    model_name = provider_settings["models"].get(model_alias, model_alias)
    
    merged_config = {
        "model_name": model_name,
        "base_url": provider_settings.get("base_url"),
        "temperature": agent_config.get("temperature"),
    }
    
    if active_provider in ["chatgroq", "groq"]:
        return GroqModel(merged_config)
    elif active_provider == "openrouter":
        return OpenRouterModel(merged_config)
    elif active_provider == "ollama":
        return OllamaModel(merged_config)
    else:
        raise ValueError(f"Unknown provider: {active_provider}")
