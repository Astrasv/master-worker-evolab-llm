from slm.slm import SLMModel
def main():
    client = SLMModel("phi3")
    messages = [
        {"role": "system", "content": "You are a Evolutionary algorithms coder."},
        {"role": "user", "content": "Write a small evoluionary algorithm python code fort 0/1 knapsack ."
        }
    ]
    response = client.generate_response(messages)
    print(response)

if __name__ == "__main__":
    main()

