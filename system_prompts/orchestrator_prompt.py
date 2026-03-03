from models.subtasks import SubtaskRequest
from toon import encode # Or whichever custom encoder you might use

def get_worker_prompt(subtask_request_model: SubtaskRequest) -> str:
    """
    Generates the strict system and operational prompt for the Worker SLMs.
    Takes a Pydantic model and injects the JSON and schema string into the prompt.
    """
    
    # TOON encoding for LLM efficiency
    request_schema = encode(subtask_request_model.model_json_schema())
    request_json = encode(subtask_request_model.model_dump())
    
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