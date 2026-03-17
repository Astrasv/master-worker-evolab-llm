import os
import time
import logging
from dotenv import load_dotenv
from pydantic import BaseModel
from openai import OpenAI
import instructor

load_dotenv()


class OpenRouterModel:
    def __init__(self, config):
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "No OPENROUTER_API_KEY found in environment. Please set it."
            )

        self.model_name = config.get("model_name") or config.get(
            "model", "google/gemini-flash-1.5"
        )
        print(self.model_name)
        self.temperature = config.get("temperature", 0.1)

        # OpenRouter requires the base_url to be pointed at their API
        self.client = instructor.patch(
            OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key,
            ),
            mode=instructor.Mode.JSON,
        )

    def generate_structured_response(
        self, messages: list, output_model: type[BaseModel]
    ):
        max_attempts = 10
        for attempt in range(max_attempts):
            try:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    response_model=output_model,
                    messages=messages,
                    temperature=self.temperature,
                )
                return response
            except Exception as e:
                err_str = str(e).lower()
                # OpenRouter/OpenAI 429 errors often caught here
                if "rate_limit" in err_str or "429" in err_str:
                    if attempt == max_attempts - 1:
                        raise e
                    sleep_time = 10 + (
                        attempt * 5
                    )  # OpenRouter can be strict; longer backoff
                    logging.warning(
                        f"Rate limit hit. Retrying in {sleep_time}s... ({attempt + 1}/{max_attempts})"
                    )
                    time.sleep(sleep_time)
                else:
                    raise e
