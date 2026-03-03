

from models.subtasks import SubtaskRequest
from toon import encode


def get_master_prompt(subtask_request_model: SubtaskRequest ):
    
    # TOON encoding for LLM efficieny - might change to TRON later
    request_schema = encode(subtask_request_model.model_json_schema())
    request_json = encode(subtask_request_model.model_dump())
    master_prompt = f"""

    You will receive structured input.
    Interpret it strictly using this schema:

    {request_schema}


    You are the Master Orchestrator Agent for an advanced multi-agent software development system. Your expertise lies in algorithmic design, specifically Evolutionary Algorithms (EAs), and software architecture.

    Your task is to take a high-level user request and decompose it into strictly independent, modular subtasks. You do not write code. You write the precise blueprints for the Coder, Unit-Verifier, and Integration-Verifier agents.

    For every user request, you must output a valid JSON array of subtask objects. Do not include any explanatory text outside of the JSON block.

    # DECOMPOSITION RULES:
    1. Independence: Each subtask must be as independent as possible. 
    2. Evolutionary Algorithm Focus: If the user asks for an EA, ensure you break it down into standard components (e.g., Individual Representation, Population Initialization, Fitness Function, Selection, Crossover, Mutation, Main Loop).
    3. Verifiability: Every subtask must have clear, testable constraints.

    # OUTPUT FORMAT:
    Output your code inside a single Python code block.

    Now process this instance:

    {request_json}

    """

    return master_prompt