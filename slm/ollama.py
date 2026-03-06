import instructor
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

class OllamaModel:
    def __init__(self, config):
        self.model_name = config.get("model_name") or config.get("model", "qwen2.5-coder:7b")
        self.temperature = config.get("temperature", 0.1)
        base_url = config.get("base_url", "http://localhost:11434")
        
        if not base_url.endswith("/v1"):
            base_url += "/v1"

        self.client = instructor.from_openai(
            OpenAI(
                base_url=base_url,
                api_key="ollama"
            ),
            mode=instructor.Mode.JSON
        )

    def generate_structured_response(self, messages: list, output_model: type[BaseModel]):
        response = self.client.chat.completions.create(
            model=self.model_name,
            temperature=self.temperature,
            response_model=output_model,
            messages=messages,
        )
        return response