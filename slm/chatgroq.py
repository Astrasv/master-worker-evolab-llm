# from langchain_groq import ChatGroq
import instructor
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from dotenv import load_dotenv
from openai import OpenAI
from system_prompts.genome_prompt import genome_prompt
import os
from pydantic import BaseModel

load_dotenv()


class GroqModel:
    def __init__(self, config):
        if "GROQ_API_KEY" not in os.environ:
            raise EnvironmentError("GROQ_API_KEY not found in environment.")

        self.model_name = config.model_name
        self.temperature = config.temperature

        self.client =  instructor.from_openai(
            OpenAI(
                base_url=config.base_url,
                api_key=os.getenv("GROQ_API_KEY"),
            ),
            mode=instructor.Mode.JSON
        )

    def generate_structured_response(self, messages, output_model: BaseModel):
        plan = self.client.chat.completions.create(
            model=self.model_name,
            response_model=output_model, 
            messages=messages,
        )
        
        return plan


# # Check if model works 
# if __name__ == "__main__":
#     model = GroqModel(model_name="llama-3.1-8b-instant")

#     messages = [
#         {"role": "system", "content": genome_prompt},
#         {"role": "user", "content": "Generate a genome for a Travelling salesmen problem."}
#     ]

#     structured_response = model.generate_structured_response(messages, IndividualResponse)

#     print(type(structured_response))
#     print(structured_response) 