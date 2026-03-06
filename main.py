from models.problem import ProblemRequest
from workflow.engine import GraphEngine
from utils.logging import setup_logging
import logging

def main():
    setup_logging("app.log")
    logger = logging.getLogger(__name__)
    logger.info("Starting SLM multi-agent workflow...")
    
    problem = ProblemRequest(
        problem_id="tsp_001",
        problem_title="Travelling Salesman Problem for random 1000 cities",
        problem_description="find the optimal solution for the travelling salesman problem using an evolutionary algorithm."
    )
    
    engine = GraphEngine()
    app = engine.build()
    
    inputs = {"problem": problem, "verified_subtasks": [], "iterations": 0}
    final_state = app.invoke(inputs)
    
    final_code = final_state["final_code"]
    print("\n\n============= final code =============\n")
    print(final_code)
    print("\n======================================\n")
    
    with open("output_code.py", "w") as f:
        f.write(final_code)
    print("output saved to output_code.py")

if __name__ == "__main__":
    main()