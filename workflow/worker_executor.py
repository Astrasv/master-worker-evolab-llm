from typing import Any, Dict
import logging

logger = logging.getLogger(__name__)


class WorkerExecutor:
    def __init__(self, worker, unit_verifier, max_retries: int = 3):
        self.worker = worker
        self.unit_verifier = unit_verifier
        self.max_retries = max_retries

    def execute(self, subtask: Any, genome: Any) -> Dict[str, Any]:
        feedback = None
        for attempt in range(self.max_retries):
            logger.info(f"[{subtask.subtask_title}] Worker attempt {attempt + 1}")
            worker_response = self.worker.run(genome, subtask, feedback)
            logger.info(
                f"[{subtask.subtask_title}] Generated Code Attempt {attempt + 1}:\n{worker_response.code}\n"
            )

            logger.info(f"[{subtask.subtask_title}] Verifying attempt {attempt + 1}...")
            verification = self.unit_verifier.run(worker_response, subtask)

            if verification.verified:
                logger.info(f"[{subtask.subtask_title}] Unit Verification SUCCESS!")
                return {"verified_subtasks": [verification]}
            else:
                logger.warning(
                    f"[{subtask.subtask_title}] Unit Verification FAILED. Feedback: {verification.feedback}"
                )
                feedback = verification.feedback

        logger.error(
            f"[{subtask.subtask_title}] Max retries reached. Using last unverified code."
        )
        return {"verified_subtasks": [verification]}
