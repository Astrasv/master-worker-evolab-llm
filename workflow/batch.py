from langgraph.types import Send
from typing import List, Any
import logging

logger = logging.getLogger(__name__)


def get_batch(subtasks: list, batch_index: int, num_workers: int) -> list:
    start_idx = batch_index * num_workers
    end_idx = min(start_idx + num_workers, len(subtasks))
    return subtasks[start_idx:end_idx]


def create_sends_for_batch(state: dict, batch: list, config: dict = None) -> list:
    return [
        Send(
            "worker_node",
            {"subtask": s, "genome": state["genome"], "config": config},
        )
        for s in batch
    ]


def has_more_batches(subtasks: list, batch_index: int, num_workers: int) -> bool:
    processed_count = batch_index * num_workers
    return processed_count < len(subtasks)


def log_batch_info(
    subtasks: list, batch_index: int, num_workers: int, prefix: str = ""
):
    batch = get_batch(subtasks, batch_index, num_workers)
    total = len(subtasks)
    start = batch_index * num_workers + 1
    end = start + len(batch) - 1
    logger.info(
        f"{prefix}Processing batch {batch_index + 1}: subtasks {start} to {end} of {total} (workers: {num_workers})"
    )
