from slm import get_slm
from models.orchestrator import CodeResponse, IntegrationResponse
from system_prompts.verifiers.integrate import integration_verifier_prompt


class IntegrationVerifierAgent:
    def __init__(self, config):
        agent_config = config.get("agents", {}).get("integration_verifier", {})
        self.model = get_slm(agent_config, config)

    def run(self, code_response: CodeResponse) -> IntegrationResponse:
        user_prompt = f"Verify the integrated codebase.\n\nFull assembled code:\n{code_response.code}"
        messages = [
            {"role": "system", "content": integration_verifier_prompt},
            {"role": "user", "content": user_prompt},
        ]
        return self.model.generate_structured_response(messages, IntegrationResponse)
