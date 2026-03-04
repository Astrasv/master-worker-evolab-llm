from slm.chatgroq import GroqModel
from models.individual import IndividualResponse
def main():
    client = GroqModel("llama-3.1-8b-instant")
    messages = [
        {"role": "system", "content": "You are a Evolutionary algorithms coder."},
        {"role": "user", "content": "Write a small evoluionary algorithm python code fort 0/1 knapsack which show only genome representation. NO need other codes ."
        }
    ]
    response = client.generate_structured_response(messages, IndividualResponse)
    print(response.model_dump_json())

if __name__ == "__main__":
    main()

