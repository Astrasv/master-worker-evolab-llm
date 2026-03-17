from models.problem import ProblemRequest
from workflow.engine import GraphEngine
from utils.logging import setup_logging
from langgraph.checkpoint.memory import MemorySaver
import logging
import uuid


def run_workflow_for_user(user_id: str, problem: ProblemRequest):
    engine = GraphEngine()
    checkpointer = MemorySaver()
    app = engine.build(checkpointer=checkpointer)

    config = {"configurable": {"thread_id": user_id}}

    inputs = {
        "problem": problem,
        "verified_subtasks": [],
        "iterations": 0,
        "current_batch_index": 0,
    }

    final_state = app.invoke(inputs, config=config)
    return final_state["final_code"]


def main():
    setup_logging("app.log")
    logger = logging.getLogger(__name__)
    logger.info("Starting SLM multi-agent workflow...")

    problem = ProblemRequest(
        problem_id="tsp_001",
        problem_title="Travelling Salesman Problem for random 1000 cities",
        problem_description="find the optimal solution for the travelling salesman problem using an evolutionary algorithm.",
    )

    user_id = str(uuid.uuid4())
    logger.info(f"Processing for user: {user_id}")

    engine = GraphEngine()
    app = engine.build()

    inputs = {
        "problem": problem,
        "verified_subtasks": [],
        "iterations": 0,
        "current_batch_index": 0,
    }
    config = {"configurable": {"thread_id": user_id}}
    final_state = app.invoke(inputs, config=config)

    final_code = final_state["final_code"]
    print("\n\n============= final code =============\n")
    print(final_code)
    print("\n======================================\n")

    with open("output_code.py", "w") as f:
        f.write(final_code)
    print("output saved to output_code.py")


if __name__ == "__main__":
    main()
