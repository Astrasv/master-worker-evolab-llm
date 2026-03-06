from slm import get_slm
from models.orchestrator import CodeResponse
from models.verifiers import UnitVerifyResponseList
from models.individual import IndividualResponse
from system_prompts.orchestrator_prompt import orchestrator_prompt
import json

class OrchestratorAgent:
    def __init__(self, config):
        agent_config = config.get("agents", {}).get("orchestrator", {})
        self.model = get_slm(agent_config, config)
    
    def run(self, genome: IndividualResponse, verified_subtasks: UnitVerifyResponseList, feedback: str = None) -> CodeResponse:
        context = {
            "genome": genome.model_dump(),
            "verified_subtasks": verified_subtasks.model_dump(),
            "integration_feedback": feedback
        }
        user_prompt = f"Assemble the verified subtasks and the genome code into a final 12-cell structured code.\n\nContext:\n{json.dumps(context, indent=2)}"
        messages = [
            {"role": "system", "content": orchestrator_prompt},
            {"role": "user", "content": user_prompt}
        ]
        return self.model.generate_structured_response(messages, CodeResponse)
