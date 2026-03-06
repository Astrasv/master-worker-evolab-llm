from slm import get_slm
from models.orchestrator import CodeResponse, IntegrationResponse
from system_prompts.verifiers.integrate import integration_verifier_prompt
import json

class IntegrationVerifierAgent:
    def __init__(self, config):
        agent_config = config.get("agents", {}).get("integration_verifier", {})
        self.model = get_slm(agent_config, config)
    
    def run(self, code_response: CodeResponse) -> IntegrationResponse:
        context = {
            "assembled_code": code_response.model_dump()
        }
        user_prompt = f"Verify the integrated codebase.\n\nContext:\n{json.dumps(context, indent=2)}"
        messages = [
            {"role": "system", "content": integration_verifier_prompt},
            {"role": "user", "content": user_prompt}
        ]
        return self.model.generate_structured_response(messages, IntegrationResponse)