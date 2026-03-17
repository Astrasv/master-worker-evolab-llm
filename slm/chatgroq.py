import instructor
from groq import Groq
from dotenv import load_dotenv
from pydantic import BaseModel
import os

load_dotenv()

class GroqModel:
    def __init__(self, config):
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise EnvironmentError("No GROQ_API_KEY found in environment. Please set GROQ_API_KEY.")

        self.model_name = config.get("model_name") or config.get("model", "llama-3.1-8b-instant")
        self.temperature = config.get("temperature", 0.1)
        
        self.client = instructor.patch(Groq(api_key=api_key))
        
    def generate_structured_response(self, messages: list, output_model: type[BaseModel]):
        import time
        import logging
        max_attempts = 10
        for attempt in range(max_attempts):
            try:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    response_model=output_model,
                    messages=messages,
                    temperature=self.temperature
                )
                return response
            except Exception as e:
                err_str = str(e)
                if "RateLimitError" in err_str or "429" in err_str:
                    if attempt == max_attempts - 1:
                        raise e
                    sleep_time = 6 + (attempt * 2)
                    logging.warning(f"Rate limit exceeded. Sleeping for {sleep_time}s and retrying... (Attempt {attempt+1}/{max_attempts})")
                    time.sleep(sleep_time)
                else:
                    raise e
