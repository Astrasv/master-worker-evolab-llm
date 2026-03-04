import instructor
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel


load_dotenv()


class OllamaModel:
    def __init__(self, config):

        self.model_name = config.model_name
        self.temperature = config.temperature

        self.client = instructor.from_openai(
            OpenAI(
                base_url=config.base_url,
                api_key="ollama"
            ),
            mode=instructor.Mode.JSON
        )

    def generate_structured_response(self, messages, output_model: BaseModel):


        response = self.client.chat.completions.create(
            model=self.model_name,
            temperature=self.temperature,
            response_model=output_model,
            messages=messages,
        )

        return response

# if __name__ == "__main__":
#     ollama_model = OllamaModel(model_name="qwen2.5-coder:7b")
#     messages = [
#         {"role": "system", "content": genome_prompt},
#         {"role": "user", "content": "Generate a genome for a Travelling salesmen problem."}
#     ]
#     result = ollama_model.generate_structured_response(
#         messages,
#         output_model=IndividualResponse
#     )

#     print(result)