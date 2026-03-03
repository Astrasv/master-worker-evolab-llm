from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from dotenv import load_dotenv

from models.subtasks import SubtaskRequestList

import os
from pydantic import BaseModel, Field

load_dotenv()


class GroqModel:
    def __init__(self, model_name, temperature=0.2):
        if "GROQ_API_KEY" not in os.environ:
            raise EnvironmentError("GROQ_API_KEY not found in environment.")

        self.model_name = model_name
        self.temperature = temperature

        self.client = ChatGroq(
            model=self.model_name,
            temperature=self.temperature,
            api_key=os.getenv("GROQ_API_KEY")
        )

    def generate_response(self, messages):
        prompt = self._convert_messages_to_prompt(messages)
        response = self.client.invoke(prompt)
        return response.content
    
    def generate_structured_response(self, messages, output_model: BaseModel):

        lc_messages = self._convert_to_langchain_messages(messages)

        structured_llm = self.client.with_structured_output(output_model)

        response = structured_llm.invoke(lc_messages)

        return response 

    def _convert_to_langchain_messages(self, messages):
        role_map = {
            "user": HumanMessage,
            "system": SystemMessage,
            "assistant": AIMessage
        }

        lc_messages = []
        for msg in messages:
            
            role = msg["role"]
            content = msg["content"]

            if role not in role_map:
                raise ValueError(f"Unsupported role: {role}")

            lc_messages.append(role_map[role](content=content))

        return lc_messages

if __name__ == "__main__":
    model = GroqModel(model_name="llama-3.1-8b-instant")

    messages = [
        {"role": "system", "content": "You are a strict API that returns structured data."},
        {"role": "user", "content": "Write a hello world program in Java."},
    ]

    structured_response = model.generate_structured_response(messages, SubtaskRequestList)

    print(type(structured_response))
    print(structured_response) 