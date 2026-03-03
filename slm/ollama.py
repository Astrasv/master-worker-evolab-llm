import ollama
class SLMModel:
    def __init__(self, model_name):
        self.model_name = model_name

    def generate_response(self, messages):
        response = ollama.chat(
            model=self.model_name,
            messages=messages
        )
        return response["message"]["content"]
    
# Main is just for checking
if __name__ == "__main__":
    model = SLMModel("phi3")
    messages = [
        {"role": "system", "content": "You are my best friend."},
        {"role": "user", "content": "Whats up my man. How ya doing?"}
    ]
    response = model.generate_response(messages)
    print(response)


