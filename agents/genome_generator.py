from slm import get_slm
from models.individual import IndividualResponse
from models.problem import ProblemRequest
from system_prompts.genome_prompt import genome_prompt

class GenomeGeneratorAgent:
    def __init__(self, config):
        agent_config = config.get("agents", {}).get("genome_generator", {})
        self.model = get_slm(agent_config, config)
    
    def run(self, problem: ProblemRequest) -> IndividualResponse:
        messages = [
            {"role": "system", "content": genome_prompt},
            {"role": "user", "content": problem.model_dump_json()}
        ]
        return self.model.generate_structured_response(messages, IndividualResponse)
