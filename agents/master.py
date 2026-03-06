from slm import get_slm
from models.subtasks import SubtaskRequestList
from models.problem import ProblemRequest
from models.individual import IndividualResponse
from system_prompts.master_prompt import master_prompt
import json

class MasterAgent:
    def __init__(self, config):
        agent_config = config.get("agents", {}).get("master", {})
        self.model = get_slm(agent_config, config)
        self.ea_defaults = config.get("ea_defaults", {})
    
    def run(self, problem: ProblemRequest, genome: IndividualResponse) -> SubtaskRequestList:
        context = {
            "problem": problem.model_dump(),
            "genome": genome.model_dump(),
            "ea_defaults": self.ea_defaults
        }
        messages = [
            {"role": "system", "content": master_prompt},
            {"role": "user", "content": f"Please decompose the following problem into subtasks given the genome code.\n\nContext:\n{json.dumps(context, indent=2)}"}
        ]
        return self.model.generate_structured_response(messages, SubtaskRequestList)

