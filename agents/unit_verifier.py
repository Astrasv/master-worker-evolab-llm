from slm import get_slm
from models.verifiers import UnitVerifyResponse
from models.subtasks import SubtaskResponse, SubtaskRequest
from system_prompts.verifiers.unit import unit_verifier_prompt
import json

class UnitVerifierAgent:
    def __init__(self, config):
        agent_config = config.get("agents", {}).get("unit_verifier", {})
        self.model = get_slm(agent_config, config)
        self.unit_verifier_prompt = unit_verifier_prompt
    
    def run(self, subtask_response: SubtaskResponse, subtask_request: SubtaskRequest) -> UnitVerifyResponse:
        context = {
            "subtask_request": subtask_request.model_dump(),
            "subtask_response": subtask_response.model_dump()
        }
        user_prompt = f"Verify the following subtask code.\n\nContext:\n{json.dumps(context, indent=2)}"
        messages = [
            {"role": "system", "content": self.unit_verifier_prompt},
            {"role": "user", "content": user_prompt}
        ]
        return self.model.generate_structured_response(messages, UnitVerifyResponse)