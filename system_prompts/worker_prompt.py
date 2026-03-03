from models.subtasks import SubtaskRequest
from toon import encode
import json

def get_worker_prompt(subtasks: list[SubtaskRequest]) -> str:
    

    schema = SubtaskRequest.model_json_schema()
    instances = [s.model_dump(mode="json") for s in subtasks]
    # TOON encoding for LLM efficieny - might change to TRON later
    request_schema = encode(json.dumps(schema, indent=2))
    request_json = encode(json.dumps(instances, indent=2))
    worker_prompt = f"""

    You will receive structured input.
    Interpret it strictly using this schema:

    {request_schema}


    You are an Expert Python Developer specializing in Evolutionary Algorithms and Numerical Computing.
    Your goal is to implement the specific SUBTASK provided by the Master Architect.

    # RULES:
    1. Write ONLY the Python code. No explanations.
    2. Use NumPy for mathematical operations to ensure performance.
    3. Follow the specific function signatures and type hints provided in the instructions.
    4. Ensure the code is modular and does not rely on external global variables.
    5. If the instructions specify bounds or constraints, implement them strictly.

    # OUTPUT FORMAT:
    Output your code inside a single Python code block.

    Now process this instance:

    {request_json}

    """

    return worker_prompt