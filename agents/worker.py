from slm import get_slm
from models.subtasks import SubtaskRequest, SubtaskResponse
from models.individual import IndividualResponse
from system_prompts.worker_prompt import worker_prompt
import json

class WorkerAgent:
    def __init__(self, config):
        agent_config = config.get("agents", {}).get("worker_coder", {})
        self.model = get_slm(agent_config, config)
    
    def run(self, genome: IndividualResponse, subtask: SubtaskRequest, feedback: str = None) -> SubtaskResponse:
        context = {
            "genome": genome.model_dump(),
            "subtask": subtask.model_dump(),
            "feedback": feedback
        }
        user_prompt = f"Implement the following subtask.\n\nContext:\n{json.dumps(context, indent=2)}"
        messages = [
            {"role": "system", "content": worker_prompt},
            {"role": "user", "content": user_prompt}
        ]
        return self.model.generate_structured_response(messages, SubtaskResponse)

