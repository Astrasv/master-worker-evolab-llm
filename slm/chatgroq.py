import instructor
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
import os

load_dotenv()

class GroqModel:
    def __init__(self, config):
        if "GROQ_API_KEY" not in os.environ:
            raise EnvironmentError("GROQ_API_KEY not found in environment.")

        self.model_name = config.get("model_name") or config.get("model", "llama-3.1-8b-instant")
        self.temperature = config.get("temperature", 0.1)
        # groq base url logic
        base_url = config.get("base_url")
        if not base_url or "localhost" in base_url:
            base_url = "https://api.groq.com/openai/v1"

        self.client = instructor.from_openai(
            OpenAI(
                base_url=base_url,
                api_key=os.getenv("GROQ_API_KEY"),
            ),
            mode=instructor.Mode.JSON
        ) 
        
    def generate_structured_response(self, messages: list, output_model: type[BaseModel]):
        response = self.client.chat.completions.create(
            model=self.model_name,
            response_model=output_model,
            messages=messages,
            temperature=self.temperature
        )
        return response